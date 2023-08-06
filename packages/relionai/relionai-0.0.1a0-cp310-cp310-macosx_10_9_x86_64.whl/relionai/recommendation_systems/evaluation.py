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


from reclist.datasets import CoveoDataset
from reclist.recommenders.prod2vec import CoveoP2VRecModel
from reclist.reclist import CoveoCartRecList

def main():
    # get the coveo data challenge dataset as a RecDataset object
    coveo_dataset = CoveoDataset()

    # re-use a skip-gram model from reclist to train a latent product space, to be used
    # (through knn) to build a recommender
    model = CoveoP2VRecModel()
    model.train(coveo_dataset.x_train)

    # instantiate rec_list object, prepared with standard quantitative tests
    # and sensible behavioral tests (check the paper for details!)
    rec_list = CoveoCartRecList(
        model=model,
        dataset=coveo_dataset
    )
    # invoke rec_list to run tests
    rec_list(verbose=True)

main()

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
    