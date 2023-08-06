import pandas as pdx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import seaborn as sns 
import pandas as pd
import datetime
from datetime import datetime as dt
from dateutil.relativedelta import *
import numpy as np 
import pandas as pd
from sklearn import metrics
from pymongo import MongoClient
from dataclasses import dataclass
import warnings
import shap
import requests
import json
import re
import bz2
import bson
import pickle
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, drange

warnings.filterwarnings("ignore")

from relionai.timeseries_regression.timeseries_splits import TimeBasedBlockSplits, TimeBasedCalibrationSplits, TimeBasedHoldoutSplits

@dataclass
class Configuration:
    account_name: str
    account_secret: str
    user_name: str
    client: any = None

CONFIG_SINGLETON = None


def mape(predictions_list, actuals_list):
    error_predictions_actuals = 0.0
    for i in range(len(predictions_list)):
        error_predictions_actuals += ((actuals_list[i] - predictions_list[i]) / actuals_list[i])
    return (1.0 / len(predictions_list)) * abs(error_predictions_actuals)


def wape(predictions_list, actuals_list):
    difference_predictions_actuals = 0.0
    for i in range(len(predictions_list)):
        difference_predictions_actuals += actuals_list[i] - predictions_list[i]
    sum_actuals = sum(actuals_list)
    return (abs(difference_predictions_actuals) / abs(sum_actuals))

def mae(predictions_list, actuals_list):
    difference_predictions_actuals = 0.0
    for i in range(len(predictions_list)):
        difference_predictions_actuals += actuals_list[i] - predictions_list[i]
    return abs(difference_predictions_actuals) / len(predictions_list)


def prep_data_pdf_for_overall_evals( data_pdf, date_col, quantity_col):
    prepped_data_pdf = data_pdf
    prepped_data_pdf[date_col] = pd.to_datetime(prepped_data_pdf[date_col], errors='coerce')
    prepped_data_pdf = prepped_data_pdf.groupby(date_col).sum([quantity_col]).reset_index()
    return  prepped_data_pdf


def prep_data_pdf_for_segment_evals(data_pdf, date_col, quantity_col, segmentation_col, segmentation_col_value):
    filtered_data_pdf = data_pdf[data_pdf[segmentation_col] == segmentation_col_value]
    filtered_data_pdf[date_col] = pd.to_datetime(filtered_data_pdf[date_col], errors='coerce')
    filtered_prepped_data_pdf = filtered_data_pdf.groupby(date_col).sum([quantity_col]).reset_index()
    return filtered_prepped_data_pdf


def split_strategy(prepped_data_pdf, date_col, train_period, test_period,  freq='days', validation_split_date=None, strategy=TimeBasedBlockSplits):
    tscv = strategy(train_period=train_period, test_period=test_period, freq=freq)
    split_indices_tuple_list = tscv.split(prepped_data_pdf, validation_split_date=validation_split_date, date_column=date_col)
    return split_indices_tuple_list


def evaluate_section(prepped_data_pdf, date_col, quantity_col, split_indices_tuple_list, model):
    plt.ioff()
    scores_per_split_tuple_list = []
    pickled_figures_list = pickle.dumps(None)
    if len(split_indices_tuple_list) > 0:
        fig, axes = plt.subplots(len(split_indices_tuple_list), 1, figsize=(12, 14))
        for i, [train_index, test_index] in enumerate(split_indices_tuple_list):
            # print(f"train_index = {len(train_index)} and test_index = {len(test_index)}")
            train, test = prepped_data_pdf.loc[train_index], prepped_data_pdf.loc[test_index]
            train.index = train[date_col]
            train = train[quantity_col]
            test.index = test[date_col]
            test = test[quantity_col]
            train.index = pd.DatetimeIndex(train.index).to_period('D')
            test.index = pd.DatetimeIndex(test.index).to_period('D')
            trained_model = model(train).fit()
            # print(f"test index [0] = {test.index[0]} and test.index[-1] = {test.index[-1]}")
            predictions = trained_model.predict(start=0, end=len(test.index)-1)
            scores_per_split_tuple_list.append([test, predictions])
            predictions_pdf = pd.DataFrame({'predictions': predictions, date_col: test.index.values})
            if len(split_indices_tuple_list) > 1:
                ax1 = sns.lineplot(data=prepped_data_pdf, x=date_col, y=quantity_col, ax=axes[i], label='other', color='tab:blue')
                ax2 = sns.lineplot(data=prepped_data_pdf.iloc[train_index], x=date_col, y=quantity_col, ax=axes[i], label='calibration', color='tab:green')
                ax3 = sns.lineplot(data=prepped_data_pdf.iloc[test_index], x=date_col, y=quantity_col, ax=axes[i], label='holdout actual', color='tab:red')
                ax4 = sns.lineplot(data=predictions_pdf, x=date_col, y='predictions', ax=axes[i], label='holdout predicted', color='tab:purple')
                tl = ((ax1.get_xlim()[1] - ax1.get_xlim()[0])*0.015 + ax1.get_xlim()[0],(ax4.get_ylim()[1] - ax1.get_ylim()[0])*0.8 + ax1.get_ylim()[0])
                ax1.text(tl[0], tl[1], f'MAE: {round(mae(predictions, test),1)}, MAPE: {round(mape(predictions, test),1)*100}%, WAPE: {round(wape(predictions, test),1)*100}%')
                try:
                    ax1.get_legend().remove()
                    ax2.get_legend().remove()
                    ax3.get_legend().remove()
                    ax4.get_legend().remove()
                except:
                    pass 
                axes[i].set_xticklabels(date_col)
                axes[i].xaxis.set_major_locator(YearLocator())
                axes[i].xaxis.set_minor_locator(MonthLocator())
                axes[i].xaxis.set_major_formatter(DateFormatter('%Y'))
                axes[len(split_indices_tuple_list) - 1].set_ylabel(quantity_col)
                ax4.lines[3].set_linestyle("--")
                axes[i].axvspan(train.index[0], train.index[-1],  facecolor='r', alpha=0.2)
                axes[i].axvspan(test.index[0], test.index[-1],  facecolor='g', alpha=0.2)
            else:
                ax1 = sns.lineplot(data=prepped_data_pdf, x=date_col, y=quantity_col, ax=axes, label='other', color='tab:blue')
                ax2 = sns.lineplot(data=prepped_data_pdf.iloc[train_index], x=date_col, y=quantity_col, ax=axes, label='calibration', color='tab:green')
                ax3 = sns.lineplot(data=prepped_data_pdf.iloc[test_index], x=date_col, y=quantity_col, ax=axes, label='holdout actual', color='tab:red')
                ax4 = sns.lineplot(data=predictions_pdf, x=date_col, y='predictions', ax=axes, label='holdout predicted', color='tab:purple')
                tl = ((ax1.get_xlim()[1] - ax1.get_xlim()[0])*0.015 + ax1.get_xlim()[0],(ax4.get_ylim()[1] - ax1.get_ylim()[0])*0.8 + ax1.get_ylim()[0])
                ax1.text(tl[0], tl[1], f'MAE: {round(mae(predictions, test),1)}, MAPE: {round(mape(predictions, test)*100,1)}%, WAPE: {round(wape(predictions, test)*100,1)}%')
                try:
                        ax1.get_legend().remove()
                        ax2.get_legend().remove()
                        ax3.get_legend().remove()
                        ax4.get_legend().remove()
                except:
                    pass
                ax4.lines[3].set_linestyle("--")
                axes.set_xticklabels(date_col)
                axes.xaxis.set_major_locator(YearLocator())
                axes.xaxis.set_minor_locator(MonthLocator())
                axes.xaxis.set_major_formatter(DateFormatter('%Y'))
                axes.set_ylabel(quantity_col)
                axes.axvspan(train.index[0], train.index[-1],  facecolor='g', alpha=0.2)
                axes.axvspan(test.index[0], test.index[-1],  facecolor='r', alpha=0.2)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.6),fancybox=True, shadow=True, ncol=4)
        pickled_figures_list = pickle.dumps(fig)
        plt.ion()
    return scores_per_split_tuple_list, pickled_figures_list



def plot_cv_indices(split_indices_tuple_list, len_prepped_data_pdf, lw=10):
    """Create a sample plot for indices of a cross-validation object."""
    cmap_cv = plt.cm.coolwarm
    fig, ax = plt.subplots()
    # Generate the training/testing visualizations for each CV split
    for ii, (tr, tt) in enumerate(split_indices_tuple_list):
        # Fill in indices with the training/test groups
        indices = np.array([np.nan] * len_prepped_data_pdf)
        indices[tt] = 1
        indices[tr] = 0

        # Visualize the results
        ax.scatter(
            range(len(indices)),
            [ii + 0.5] * len(indices),
            c=indices,
            marker="_",
            lw=lw,
            cmap=cmap_cv,
            vmin=-0.2,
            vmax=1.2,
        )
    ax.legend([Patch(color=cmap_cv(.8)), Patch(color=cmap_cv(.02))],
            ['Testing set', 'Training set'])
    plt.tight_layout()
    return ax


def plot_cv_indices(split_indices_tuple_list, len_prepped_data_pdf, dataset_min_date, dataset_max_date, lw=10):
    """Create a sample plot for indices of a cross-validation object."""
    start = pd.Timestamp(dataset_min_date)
    end = pd.Timestamp(dataset_max_date)
    t = np.linspace(start.value, end.value, len_prepped_data_pdf)
    dates_range_list = pd.to_datetime(t).to_list()
    cmap_cv = plt.cm.coolwarm
    fig, ax = plt.subplots()
    ii = 0
    split_indices_tuple_list_ = list(split_indices_tuple_list[0])
    split_indices_tuple_list_.reverse()
    for ttrr in split_indices_tuple_list_:
        # Fill in indices with the training/test groups
        indices = np.array([np.nan] * len_prepped_data_pdf)
        indices[ttrr[0]] = 1
        indices[ttrr[1]] = 0

        # Visualize the results
        ax.scatter(
            range(len(indices)),
            [ii + 0.5] * len(indices),
            c=indices,
            marker="_",
            lw=lw,
            cmap=cmap_cv,
            vmin=-0.2,
            vmax=1.2,
        )
        ii += 1
    ax.legend([Patch(color=cmap_cv(.8)), Patch(color=cmap_cv(.02))],
            ['Calibration set', 'Holdout set'])
    plt.tight_layout()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Formatting
    yticklabels = list(range(len(split_indices_tuple_list_)))
    ax.set(
        yticks=np.arange(len(split_indices_tuple_list_)) + 0.5,
        yticklabels=yticklabels,
        xticklabels=indices,
        xlabel="Time",
        ylabel="Test Number",
        ylim=[len(split_indices_tuple_list_), -0.2],
    )
    plt.show()



def timeseries_initialize(account_name, account_secret, user_name):
    try:
        client = MongoClient(f"mongodb+srv://{account_name}:{account_secret}@cluster0.gqqhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        client.server_info()
    except:
        raise Exception('Unable to initialize Wizard AI agent. Contact the friendly folks at support@thewizard.ai for help')
    config = Configuration(account_name,account_secret, user_name, client)
    return config


def full_evaluation(prepped_data_pdf, model, date_col, quantity_col, train_period, test_period,  strategy, freq='days', validation_split_date=None):
    len_prepped_data_pdf = len(prepped_data_pdf.index)
    split_indices_tuple_list = split_strategy(prepped_data_pdf, date_col, train_period, test_period,  freq=freq, validation_split_date=validation_split_date, strategy=strategy)
    # THIS WILL FAIL, FIX IT TO STATSMODEL SYNTAX FOR TESTING
    split_scores_tuple_list, pickled_figures_list = evaluate_section(prepped_data_pdf, date_col, quantity_col, split_indices_tuple_list, model)
    #TODO: ADD THESE TO PLOT AS FLOATING NUMBER LABELS
    splits_mae_list = []
    splits_mape_list = []
    splits_wape_list = []
    for pred, actual in split_scores_tuple_list:
        splits_mae_list.append(mae(pred, actual))
        splits_mape_list.append(mape(pred, actual))
        splits_wape_list.append(wape(pred, actual))
    return len_prepped_data_pdf, split_indices_tuple_list, splits_mae_list, splits_mape_list, splits_wape_list, pickled_figures_list



def timeseries_evaluate(model, model_name, data_pdf, date_col, quantity_col, train_period, test_period, segmentation_col=None, config=None, freq='days', validation_split_date=None, dataset_name=None):
    if not config:
        raise Exception("Agent not initialized. Please initialize using initialize()")
    overall_prepped_data_pdf = prep_data_pdf_for_overall_evals( data_pdf, date_col, quantity_col)
    dataset_min_date = overall_prepped_data_pdf[date_col].min().strftime("%Y-%m-%d")
    dataset_max_date = overall_prepped_data_pdf[date_col].max().strftime("%Y-%m-%d")
    overall_block_len_prepped_data_pdf, overall_block_split_indices_tuple_list, overall_block_splits_mae_list, overall_block_splits_mape_list, overall_block_splits_wape_list, overall_block_pickled_figures_list = full_evaluation(overall_prepped_data_pdf, model, date_col, quantity_col, train_period, test_period,  TimeBasedBlockSplits, freq=freq, validation_split_date=validation_split_date)
    overall_holdout_len_prepped_data_pdf, overall_holdout_split_indices_tuple_list, overall_holdout_splits_mae_list, overall_holdout_splits_mape_list, overall_holdout_splits_wape_list, overall_holdout_pickled_figures_list = full_evaluation(overall_prepped_data_pdf, model, date_col, quantity_col, train_period, test_period,  TimeBasedHoldoutSplits, freq=freq, validation_split_date=validation_split_date)
    overall_calibration_len_prepped_data_pdf, overall_calibration_split_indices_tuple_list,overall_calibration_splits_mae_list, overall_calibration_splits_mape_list, overall_calibration_splits_wape_lis, overall_calibration_pickled_figures_list = full_evaluation(overall_prepped_data_pdf, model, date_col, quantity_col, train_period, test_period,  TimeBasedCalibrationSplits, freq=freq, validation_split_date=validation_split_date)
    # TODO: PLOTTING AND RULES

    segmentation_performance_dict = {}
    if segmentation_col:
        for segment in list(data_pdf[segmentation_col].unique()):
            overall_prepped_data_pdf = prep_data_pdf_for_segment_evals(data_pdf, date_col, quantity_col, segmentation_col, segment)
            overall_block_len_prepped_data_pdf, overall_block_split_indices_tuple_list, overall_block_splits_mae_list, overall_block_splits_mape_list, overall_block_splits_wape_list, overall_block_pickled_figures_list = full_evaluation(overall_prepped_data_pdf, model, date_col, quantity_col, train_period, test_period,  TimeBasedBlockSplits, freq=freq, validation_split_date=validation_split_date)
            overall_holdout_len_prepped_data_pdf, overall_holdout_split_indices_tuple_list, overall_holdout_splits_mae_list, overall_holdout_splits_mape_list, overall_holdout_splits_wape_list, overall_holdout_pickled_figures_list = full_evaluation(overall_prepped_data_pdf, model, date_col, quantity_col, train_period, test_period,  TimeBasedHoldoutSplits, freq=freq, validation_split_date=validation_split_date)
            overall_calibration_len_prepped_data_pdf, overall_calibration_split_indices_tuple_list, overall_calibration_splits_mae_list, overall_calibration_splits_mape_list, overall_calibration_splits_wape_list, overall_calibration_pickled_figures_list = full_evaluation(overall_prepped_data_pdf, model, date_col, quantity_col, train_period, test_period,  TimeBasedCalibrationSplits, freq=freq, validation_split_date=validation_split_date)
            segmentation_performance_dict[segment] = {
                "overall_block_len_prepped_data_pdf": overall_block_len_prepped_data_pdf,
                "overall_block_split_indices_tuple_list": overall_block_split_indices_tuple_list,
                "overall_block_splits_mae_list": overall_block_splits_mae_list,
                "overall_block_splits_mape_list": overall_block_splits_mape_list,
                "overall_block_splits_wape_list": overall_block_splits_wape_list,
                "overall_block_pickled_figures_list": overall_block_pickled_figures_list,
                "overall_calibration_len_prepped_data_pdf": overall_calibration_len_prepped_data_pdf,
                "overall_calibration_split_indices_tuple_list": overall_calibration_split_indices_tuple_list,
                "overall_calibration_splits_mae_list": overall_calibration_splits_mae_list,
                "overall_calibration_splits_mape_list": overall_calibration_splits_mape_list,
                "overall_calibration_splits_wape_list": overall_calibration_splits_wape_list,
                "overall_calibration_pickled_figures_list": overall_calibration_pickled_figures_list,
                "overall_holdout_len_prepped_data_pdf": overall_holdout_len_prepped_data_pdf,
                "overall_holdout_split_indices_tuple_list": overall_holdout_split_indices_tuple_list,
                "overall_holdout_splits_mae_list": overall_holdout_splits_mae_list,
                "overall_holdout_splits_mape_list": overall_holdout_splits_mape_list,
                "overall_holdout_splits_wape_list": overall_holdout_splits_wape_list,
                "overall_holdout_pickled_figures_list": overall_holdout_pickled_figures_list
            }


    for seg in segmentation_performance_dict.keys():
        # TODO: PLOTTING AND RULES
        pass


    model_document = {
        "Model Name": model_name,
        "Model Type": "Timeseries",
        "Performance": 2,
        "Robustness Score": 2,
        "Fairness Score": 2,
        "Auditability Score": 2,
        "Created At": datetime.utcnow(),
        "Updated At": datetime.utcnow(),
        "Owner": config.user_name,
        "dataset_name": dataset_name,
        "date_col": date_col,
        "quantity_col": quantity_col,
        "segmentation_col": segmentation_col,
        "train_period": train_period,
        "test_period": test_period,
        "freq": freq,
        "dataset_min_date": dataset_min_date,
        "dataset_max_date": dataset_max_date,
        "overall_block_splits_mae_list": overall_block_splits_mae_list,
        "overall_block_splits_mape_list": overall_block_splits_mape_list,
        "overall_block_splits_wape_list": overall_block_splits_wape_list,
        "overall_block_len_prepped_data_pdf": overall_block_len_prepped_data_pdf,
        "overall_block_split_indices_tuple_list": overall_block_split_indices_tuple_list,
        "overall_block_pickled_figures_list": overall_block_pickled_figures_list,
        "overall_calibration_splits_mae_list": overall_calibration_splits_mae_list,
        "overall_calibration_splits_mape_list": overall_calibration_splits_mape_list,
        "overall_calibration_splits_wape_list": overall_calibration_splits_wape_list,
        "overall_calibration_len_prepped_data_pdf": overall_calibration_len_prepped_data_pdf,
        "overall_calibration_split_indices_tuple_list": overall_calibration_split_indices_tuple_list,
        "overall_calibration_pickled_figures_list": overall_calibration_pickled_figures_list,
        "overall_holdout_splits_mae_list": overall_holdout_splits_mae_list,
        "overall_holdout_splits_mape_list": overall_holdout_splits_mape_list,
        "overall_holdout_splits_wape_list": overall_holdout_splits_wape_list,
        "overall_holdout_len_prepped_data_pdf": overall_holdout_len_prepped_data_pdf,
        "overall_holdout_split_indices_tuple_list": overall_holdout_split_indices_tuple_list,
        "overall_holdout_pickled_figures_list": overall_holdout_pickled_figures_list,
        "segmentation_performance_dict": bson.Binary(bz2.compress(pickle.dumps(segmentation_performance_dict))),

    }
    database = config.client["wizarddb"]
    models_collection = database["evaluationstore"]
    if models_collection.find_one({"model_name": model_name, "Owner": config.user_name}):
        print(f"Found existing model with the name '{model_name}' belonging to user {config.username} in store. Updating evaluation...")
        _ = model_document.pop('Created At', None)
    models_collection.update_one({"Model Name": model_name, "Owner": config.user_name}, {"$set": model_document}, upsert=True)
    return None
    