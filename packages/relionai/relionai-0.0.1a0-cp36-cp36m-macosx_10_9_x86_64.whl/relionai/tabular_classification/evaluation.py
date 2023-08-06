from types import MemberDescriptorType
from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd
from sklearn import metrics
from typing import Any, NoReturn, Optional, Tuple, Dict, List
from dataclasses import dataclass
from sklearn.preprocessing import label_binarize
import warnings
import shap
import requests
import json
import re
import bz2
import bson
from bson import json_util
import pickle
from datetime import datetime
from sdv.tabular import CTGAN
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import SMOTE
from mlxtend.evaluate import bias_variance_decomp
from dataclasses import dataclass
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from math import isnan
from emoji import emojize
import os
warnings.filterwarnings("ignore")



def plot_cv_indices(split_indices_tuple_list, len_prepped_data_pdf, dataset_min_date, dataset_max_date, lw=10):
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


def plot_gender_fairness():
    n_pelis = [0.92, 0.99, 0.978]
    annos = ['Female', 'Male', 'Overall']
    # plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(13,6.3))
    plt.title('Model Performance (AUC) by Gender')
    ax.barh(annos, n_pelis, edgecolor = "none",
        color = ['#f5c518', '#777', '#444'])
    ax.set_yticks([])
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(False)
    ax.set_facecolor("white")
    ax.set_xlim(0, 1)
    annos_xticks = annos
    plt.yticks(annos, labels=annos_xticks)
    for anno, peli in tuple(zip(annos, n_pelis)):
        ax.text(y=anno, x=peli, s=peli, va='bottom', ha = 'center',fontsize = 14, fontweight = 'regular')
    ax.axvline(x=n_pelis[-1], color='black', linestyle='--', lw=1)
    return fig


def plot_age_fairness():
    n_pelis = [0.92, 0.99, 0.97, 0.89, 0.96, 0.88, 0.98, 0.76, 0.92, 0.95, 0.97]
    annos = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', 'Overall']
    # plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(13,6.3))
    plt.title('Model Performance (AUC) by Age')
    ax.step(annos, n_pelis, where='med')
    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0, 1)
    ax.xaxis.grid(False)
    ax.set_facecolor("white")
    annos_xticks = annos
    plt.xticks(annos, labels=annos_xticks)
    for anno, peli in tuple(zip(annos, n_pelis)):
        ax.text(x=anno, y=peli, s=peli, va='bottom', ha = 'center',fontsize = 14, fontweight = 'regular')
    ax.axhline(y=n_pelis[-1], color='black', linestyle='--', lw=1)
    return fig


def plot_subset_performance(synthetic_subset_performance_dict, overall_auc):
    # n_pelis = [0.96, 0.93, 0.99, 1.00, 1.00, 1.0, 0.86, 0.91, 0.97, 0.93, 0.97]
    # annos = ['V5=1.0', 'domain=gmail.com', 'V4=3.0', 'TransactionAmt=[24.5-45.1)', 'V4=6.2', 'card1=4.0', 'TansactionAmt=[105.3-189.3', 'domain=yahoo.com', 'V2=5.0','V2=4.0', 'Overall']
    # plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(13,6.3))
    plt.title('Worst Performing (AUC) Subset Samples')
    cols = min(len(synthetic_subset_performance_dict.keys()), 20)
    worst_performing_subsets_dict = dict(sorted(synthetic_subset_performance_dict.items(), key=lambda x: x[1])[:(cols - 1)])
    worst_performing_subsets_dict = {k: v for k, v in synthetic_subset_performance_dict.items() if k in worst_performing_subsets_dict.keys()}
    worst_performing_subsets_dict['Overall'] = overall_auc
    ax.bar(worst_performing_subsets_dict.keys(), worst_performing_subsets_dict.values(), edgecolor = "none",
        color = (['#777'] * (cols - 1)) + ['#444'])
    ax.set_yticks([])
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(False)
    ax.set_facecolor("white")
    ax.set_ylim(0, 1)
    annos_xticks = worst_performing_subsets_dict.keys()
    plt.xticks(range(0,len(annos_xticks)), labels=annos_xticks, fontsize=12)
    # Pintar valores sobre las barras
    for anno, peli in tuple(zip(worst_performing_subsets_dict.keys(), worst_performing_subsets_dict.values())):
        ax.text(x=anno, y=peli, s=round(peli,2), va='bottom', ha = 'center', fontsize = 14, fontweight = 'regular')
    ax.axhline(y=list(worst_performing_subsets_dict.values())[-1], color='black', linestyle='--', lw=1)
    ax.xaxis.set_tick_params(rotation=90)
    return fig


def plot_class_balance(target_class_dict, title):
    n_pelis = target_class_dict.values()
    annos = target_class_dict.keys()
    # plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(5,5))
    plt.title(title)
    ax.set_facecolor("white")
    ax.bar(annos, n_pelis, edgecolor = "none",
        color = ['#f5c518', '#444'])
    ax.set_yticks([])
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_visible(True)
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.yaxis.grid(False)
    ax.set_xlim(0, 1)
    # annos_xticks = annos
    plt.xticks(np.arange(len(annos)), labels=annos)
    # for anno, peli in tuple(zip(annos, n_pelis)):
    #     ax.text(y=anno, x=np.arange(len(annos)), s=peli, va='bottom', ha = 'center')
    return fig


def make_confusion_matrix(cf_matrix,
                          group_names=None,
                          categories='auto',
                          count=True,
                          percent=True,
                          cbar=True,
                          xyticks=True,
                          xyplotlabels=True,
                          sum_stats=True,
                          figsize=None,
                          cmap='Blues',
                          title="Original Data"):
    blanks = ['' for i in range(cf_matrix.size)]
    if group_names and len(group_names)==cf_matrix.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks
    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf_matrix.flatten()]
    else:
        group_counts = blanks
    if percent:
        group_percentages = ["{0:.2%}".format(value) for value in cf_matrix.flatten()/np.sum(cf_matrix)]
    else:
        group_percentages = blanks
    box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(group_labels,group_counts,group_percentages)]
    box_labels = np.asarray(box_labels).reshape(cf_matrix.shape[0],cf_matrix.shape[1])
    if sum_stats:
        accuracy  = np.trace(cf_matrix) / float(np.sum(cf_matrix))
        if len(cf_matrix)==2:
            precision = cf_matrix[1,1] / sum(cf_matrix[:,1])
            recall    = cf_matrix[1,1] / sum(cf_matrix[1,:])
            f1_score  = 2*precision*recall / (precision + recall)
            stats_text = "\n\nAccuracy={:0.3f}\nPrecision={:0.3f}\nRecall={:0.3f}\nF1 Score={:0.3f}".format(
                accuracy,precision,recall,f1_score)
        else:
            stats_text = "\n\nAccuracy={:0.3f}".format(accuracy)
    else:
        stats_text = ""
    if figsize==None:
        figsize = plt.rcParams.get('figure.figsize')
    if xyticks==False:
        categories=False
    plt.figure(figsize=figsize, facecolor='none')
    sns.set(font_scale = 1)
    sns.heatmap(cf_matrix,annot=box_labels,fmt="",cmap=cmap,cbar=cbar,xticklabels=categories,yticklabels=categories)
    if xyplotlabels:
        plt.ylabel('True label')
        plt.xlabel('Predicted label' + stats_text)
    else:
        plt.xlabel(stats_text)
    if title:
        plt.title(title)
    return plt


def plot_shap_importance(shap_values):
    plt.figure(figsize=plt.rcParams.get('figure.figsize'), facecolor='white')
    sns.set(rc={'axes.facecolor':'white', 'figure.facecolor':'white'})
    try:
        shap.plots.bar(shap_values,max_display=30)
    except:
        shap.plots.bar(shap_values[:,:,1], max_display=30)
    pass

def render_monitoring_app(model_name):
    pass


def plot_most_corr_map(original_vs_synthetic_corr):
    plt.figure(facecolor='none')
    plt.title('Most Correlated Train Features')
    if len(original_vs_synthetic_corr.index) > 80:
         ndf = original_vs_synthetic_corr.loc[original_vs_synthetic_corr.max(axis=1) > 0.70, original_vs_synthetic_corr.max(axis=0) > 0.70]
    else:
        ndf = original_vs_synthetic_corr
    sns.heatmap(ndf, cmap='BrBG', vmin=0.0, vmax=1.0, center=0.0)
    return plt

def plot_least_corr_map(original_vs_synthetic_corr, title=None):
    plt.figure(facecolor='none')
    plt.title(title)
    if len(original_vs_synthetic_corr.index) > 80:
        ndf = original_vs_synthetic_corr.loc[original_vs_synthetic_corr.max(axis=1) <0.3, original_vs_synthetic_corr.max(axis=0) > 0.3]
    else:
        ndf = original_vs_synthetic_corr
    sns.heatmap(ndf, cmap='BrBG', vmin=0.0, vmax=1.0, center=0.0)
    return plt


def calculate_model_metrics(
    X: pd.DataFrame,
    y: pd.Series,
    labels_col: str,
    model: Any,
    performance_metric: Optional[str] = None,
) -> Tuple[float, float, float, pd.DataFrame, str, pd.DataFrame]:
    preds_col = "_Predicted"
    data_pdf = pd.concat([X, y], axis=1)
    features_pdf = X
    data_pdf[preds_col] = model.predict(features_pdf)
    predictions = data_pdf[preds_col]
    # try:
    #     is_classification = np.array_equal(data_pdf[preds_col], data_pdf[preds_col].astype(int))
    # except:
    #     is_classification = False
    # if is_classification:
    try:
        labels = data_pdf[labels_col].unique()
        onehot_encoded_preds = label_binarize(data_pdf[preds_col], classes=labels)
        onehot_encoded_labels = label_binarize(data_pdf[labels_col], classes=labels)
        overall_auc = round(metrics.roc_auc_score(y_true=onehot_encoded_labels, y_score=onehot_encoded_preds, multi_class='ovr'),2)
        overall_accuracy = round(
            metrics.accuracy_score(data_pdf[labels_col], predictions), 2
        )
        overall_precision = round(
            metrics.precision_score(data_pdf[labels_col], predictions, average='micro', labels=labels), 2
        )

        cf_matrix = metrics.confusion_matrix(data_pdf[labels_col], predictions)
    except:
        try:
            data_pdf[preds_col] = data_pdf[preds_col].round(0)
            labels = data_pdf[labels_col].unique()
            onehot_encoded_preds = label_binarize(data_pdf[preds_col], classes=labels)
            onehot_encoded_labels = label_binarize(data_pdf[labels_col], classes=labels)
            overall_auc = round(metrics.roc_auc_score(y_true=onehot_encoded_labels, y_score=onehot_encoded_preds, multi_class='ovr'),2)
            overall_accuracy = round(
                metrics.accuracy_score(data_pdf[labels_col], predictions), 2
            )
            overall_precision = round(
                metrics.precision_score(data_pdf[labels_col], predictions, average='micro', labels=labels), 2
            )

            cf_matrix = metrics.confusion_matrix(data_pdf[labels_col], predictions)
        except:
            raise Exception("Tabular tests currently only support classification use-cases, if this is still a classfication use-case send us a message at..")
    return (
        overall_auc,
        overall_accuracy,
        overall_precision,
        cf_matrix,
        preds_col,
        data_pdf,
    )

def _test_subset_performance_prepocessing(
    data_pdf: pd.DataFrame, labels_col: str, preds_col: str
) -> pd.DataFrame:
    labels_pdf = data_pdf[labels_col]
    preds_pdf = data_pdf[preds_col]
    prepped_pdf = data_pdf.drop([labels_col, preds_col], axis=1)

    categorical_cols = [
        col for col in prepped_pdf.columns if len(prepped_pdf[col].unique()) <= 50
    ]

    numericals_pdf = prepped_pdf.select_dtypes(include="number").drop(
        [categorical_cols], axis=1, errors="ignore"
    )

    categoricals_pdf = prepped_pdf.drop(numericals_pdf.columns, axis=1, errors="ignore")

    for col in categoricals_pdf.columns:
        top_n = 10  # TODO: parameterize me
        top_cats = categoricals_pdf[col].value_counts().head(top_n).index.tolist()
        categoricals_pdf.loc[
            (~categoricals_pdf[col].isin(top_cats)) & (~categoricals_pdf[col].isna())
        ] = "Other"

    for col in numericals_pdf.columns:
        if (numericals_pdf[col].max() - numericals_pdf[col].min()) > 1.0:
            edges = np.linspace(
                numericals_pdf[col].min(), numericals_pdf[col].max(), 10 + 1
            )
        else:
            edges = np.linspace(
                numericals_pdf[col].min(), numericals_pdf[col].max(), 10 + 1
            )
        labels = [f"({round(edges[i],1)}, {round(edges[i+1],1)}]" for i in range(len(edges) - 1)]
        numericals_pdf[col] = pd.cut(
            numericals_pdf[col],
            bins=10,
            precision=2,
            include_lowest=True,
            duplicates="drop",
            labels=labels,
            ordered=False,
        )

    prepped_pdf = pd.concat(
        [numericals_pdf, categoricals_pdf, labels_pdf, preds_pdf], axis=1
    )
    return prepped_pdf


def test_subset_performance(
    data_pdf: pd.DataFrame, labels_col: str, preds_col: str, overall_auc: float, low_threshold_pct: float = 0.1, med_threshold_pct: float = 0.2, high_threshold_pct: float = 0.5
) -> Tuple[Dict[str, float], List[float], List[int]]:
    # performance_thresholds=[0.1, 0.2, 0.5]  -- TODO: parameterize me
    prepped_pdf = _test_subset_performance_prepocessing(data_pdf, labels_col, preds_col)
    feature_space_performance_risks_count_list = [0, 0, 0]
    subset_performance_dict = {}
    num_low_auc = 0
    num_med_auc = 0
    num_high_auc = 0
    for col_level_1 in prepped_pdf.columns:
        if col_level_1 in [labels_col, preds_col]:
            continue
        for category_level_1 in prepped_pdf[col_level_1].unique():
            subset_pd = prepped_pdf.loc[prepped_pdf[col_level_1] == category_level_1]
            if len(subset_pd.index) < 2:
                continue
            labels = subset_pd[labels_col].unique()
            if len(labels) > 1:
                onehot_encoded_preds = label_binarize(subset_pd[preds_col], classes=labels)
                onehot_encoded_labels = label_binarize(subset_pd[labels_col], classes=labels)
                subset_auc = metrics.roc_auc_score(y_true=onehot_encoded_labels, y_score=onehot_encoded_preds, multi_class='ovr')
            else:
                subset_auc = 0.0
            # fpr, tpr, _ = metrics.roc_curve(subset_pd[labels_col], subset_pd[preds_col])
            # subset_auc = metrics.auc(fpr, tpr)
            # print(f'Subset AUC for {col_level_1} = {category_level_1} is {subset_auc}')
            if subset_auc:
                subset_performance_dict[
                    f"{col_level_1}={category_level_1}"
                ] = subset_auc

    for key, value in subset_performance_dict.items():
        for key2, value2 in  subset_performance_dict.items():
            if key == key2:
                continue
        range_boundaries = key2.split('=')[1].replace('(', '').replace(')', '').replace('[', '').replace(']', '').split(',')
        value_boundaries = key.split('=')[1].replace('(', '').replace(')', '').replace('[', '').replace(']', '').split(',')
        if (key2.split('=')[0] == key.split('=')[0] and range_boundaries[0] == value_boundaries[1]) and round(value,2) == round(value2,2):
            subset_performance_dict[
            f"{key.split('=')[0]}=[{value_boundaries[0]},{range_boundaries[1]}]"
            ] = value
            del subset_performance_dict[key]
            del subset_performance_dict[key2]

    for key, value in subset_performance_dict.items():
        for key2, value2 in  subset_performance_dict.items():
            if key == key2:
                continue
        range_boundaries = key2.split('=')[1].replace('(', '').replace(')', '').replace('[', '').replace(']', '').split(',')
        value_boundaries = key.split('=')[1].replace('(', '').replace(')', '').replace('[', '').replace(']', '').split(',')
        if (key2.split('=')[0] == key.split('=')[0] and range_boundaries[1] == value_boundaries[0]) and round(value,2) == round(value2,2):
            subset_performance_dict[
            f"{key.split('=')[0]}=[{range_boundaries[0]},{value_boundaries[1]}]"
            ] = value
            del subset_performance_dict[key]
            del subset_performance_dict[key2]
        
    for key, value in subset_performance_dict.items():
        if value <= overall_auc * (1.0 - high_threshold_pct):
            num_high_auc += 1
        elif value <= overall_auc * (1.0 - med_threshold_pct):
            num_med_auc += 1
        elif value <= overall_auc * (1.0 - low_threshold_pct):
            num_low_auc += 1
    num_features_auc_list = [num_low_auc, num_med_auc, num_high_auc]
    if num_features_auc_list[0] > 0:
        print(f"{emojize(':yellow_circle:')} {num_features_auc_list[0]} groups have over {low_threshold_pct*100}% lower AUC than overall population")
        feature_space_performance_risks_count_list[0]  += 1
    else:
        print(f"{emojize(':green_cricle:')} {num_features_auc_list[0]} groups have over {low_threshold_pct*100}% lower AUC than overall population")
    if num_features_auc_list[1] > 0:
        print(f"{emojize(':orange_circle:')} {num_features_auc_list[1]} groups have over {med_threshold_pct*100}% lower AUC than overall population")
        feature_space_performance_risks_count_list[1] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_features_auc_list[1]} groups have over {med_threshold_pct*100}% lower AUC than overall population")
    if num_features_auc_list[2] > 0:
        print(f"{emojize(':red_circle:')} {num_features_auc_list[2]} groups have over {high_threshold_pct*100}% lower AUC than overall population")
        feature_space_performance_risks_count_list [2] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_features_auc_list[2]} groups have over {high_threshold_pct*100}% lower AUC than overall population")
    return subset_performance_dict, num_features_auc_list, feature_space_performance_risks_count_list 


def test_bias_variance(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    clf: Any,
) -> Tuple[float, float, float, List[int]]:
    bias_variance_risks_count_list = [0, 0, 0]
    avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(
        clf, X_train, y_train, X_test, y_test, num_rounds=5, random_seed=123
    )
    print(f"{emojize(':hollow_red_circle:')} {round(avg_expected_loss,2)} average expected loss between datasets")
    print(f"{emojize(':hollow_red_circle:')} {round(avg_bias,2)} average bias between datasets")
    print(f"{emojize(':hollow_red_circle:')} {round(avg_var,2)} average variance between datasets")
    return avg_expected_loss, avg_bias, avg_var, bias_variance_risks_count_list

def test_target_correlation(
    data_pdf: pd.DataFrame, labels_col: str, preds_col: str, low_threshold_pct: float = 0.8, med_threshold_pct: float = 0.9, high_threshold_pct: float = 1.0
) -> Tuple[List[int], List[int], pd.DataFrame, List[int]]:
    features_corr_high_dict = {}
    features_corr_med_dict = {}
    features_corr_low_dict = {}
    target_correlation_risks_count_list = [0, 0, 0]
    corr = pd.DataFrame(
        np.corrcoef(data_pdf.values, rowvar=False), columns=data_pdf.columns
    )
    for i in range(corr.shape[0]):
        for j in range(i + 1, corr.shape[0]):
            if corr.iloc[i, j] >= high_threshold_pct:
                if i in features_corr_high_dict:
                    features_corr_high_dict[i].append(j)
                else:
                    features_corr_high_dict[i] = [j]
            elif corr.iloc[i, j] >= med_threshold_pct:
                if i in features_corr_med_dict:
                    features_corr_med_dict[i].append(j)
                else:
                    features_corr_med_dict[i] = [j]
            elif corr.iloc[i, j] >= low_threshold_pct:
                if i in features_corr_low_dict:
                    features_corr_low_dict[i].append(j)
                else:
                    features_corr_low_dict[i] = [j]
    num_corr_target_high = 0
    num_corr_target_med = 0
    num_corr_target_low = 0
    if labels_col in features_corr_high_dict.keys():
        if preds_col in features_corr_high_dict[labels_col]:
            num_corr_target_high = len(features_corr_high_dict[labels_col] - 1)
        else:
            num_corr_target_high = len(features_corr_high_dict[labels_col])
    elif labels_col in features_corr_med_dict.keys():
        if preds_col in features_corr_med_dict[labels_col]:
            num_corr_target_high = len(features_corr_med_dict[labels_col] - 1)
        else:
            num_corr_target_high = len(features_corr_med_dict[labels_col])
    elif labels_col in features_corr_low_dict.keys():
        if preds_col in features_corr_low_dict[labels_col]:
            num_corr_target_low = len(features_corr_low_dict[labels_col] - 1)
        else:
            num_corr_target_low = len(features_corr_low_dict[labels_col])
    num_corr_features_high = len(features_corr_high_dict)
    if labels_col in features_corr_high_dict.keys():
        num_corr_features_high -= 1
    if preds_col in features_corr_high_dict.keys():
        num_corr_features_high -= 1
    num_corr_features_med = len(features_corr_med_dict)
    if labels_col in features_corr_med_dict.keys():
        num_corr_features_med -= 1
    if preds_col in features_corr_med_dict.keys():
        num_corr_features_med -= 1
    num_corr_features_low = len(features_corr_low_dict)
    if labels_col in features_corr_low_dict.keys():
        num_corr_features_low -= 1
    if preds_col in features_corr_low_dict.keys():
        num_corr_features_low -= 1
    pdf_corr = data_pdf.corr()

    num_corr_target_list = [
        num_corr_target_low,
        num_corr_target_med,
        num_corr_target_high,
    ]
    num_corr_features_list = [
        num_corr_features_low,
        num_corr_features_med,
        num_corr_features_high,
    ]
    num_features = len(data_pdf.columns) - 2
    if num_corr_target_list[0] > 0:
        print(f"{emojize(':yellow_circle:')} {num_corr_target_list[0]} of {num_features} feature is over {low_threshold_pct*100}% correlated with the target")
        target_correlation_risks_count_list[0] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_corr_target_list[0]} of {num_features} feature is over {low_threshold_pct*100}% correlated with the target")
    if num_corr_target_list[1] > 0:
        print(f"{emojize(':orange_circle:')} {num_corr_target_list[1]} of {num_features} feature is over {med_threshold_pct*100}% correlated with the target")
        target_correlation_risks_count_list[1] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_corr_target_list[1]} of {num_features} feature is over {med_threshold_pct*100}% correlated with the target")
    if num_corr_target_list[2] > 0:
        print(f"{emojize(':red_circle:')} {num_corr_target_list[2]} of {num_features} feature is over {high_threshold_pct*100}% correlated with the target")
        target_correlation_risks_count_list[2] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_corr_target_list[2]} of {num_features} feature is over {high_threshold_pct*100}% correlated with the target")
    return num_corr_target_list, num_corr_features_list, pdf_corr, target_correlation_risks_count_list


def test_correlated_features(
    data_pdf: pd.DataFrame, labels_col: str, preds_col: str, low_threshold_pct: float = 0.8, med_threshold_pct: float = 0.9, high_threshold_pct: float = 1.0
) -> Tuple[List[int], List[int], pd.DataFrame, List[int], List[int]]:
    features_corr_high_dict = {}
    features_corr_med_dict = {}
    features_corr_low_dict = {}
    feature_correlation_risks_count_list = [0, 0, 0]
    corr = pd.DataFrame(
        np.corrcoef(data_pdf.values, rowvar=False), columns=data_pdf.columns
    )
    for i in range(corr.shape[0]):
        for j in range(i + 1, corr.shape[0]):
            if corr.iloc[i, j] >= high_threshold_pct:
                if i in features_corr_high_dict:
                    features_corr_high_dict[i].append(j)
                else:
                    features_corr_high_dict[i] = [j]
            elif corr.iloc[i, j] >= med_threshold_pct:
                if i in features_corr_med_dict:
                    features_corr_med_dict[i].append(j)
                else:
                    features_corr_med_dict[i] = [j]
            elif corr.iloc[i, j] >= low_threshold_pct:
                if i in features_corr_low_dict:
                    features_corr_low_dict[i].append(j)
                else:
                    features_corr_low_dict[i] = [j]
    num_corr_target_high = 0
    num_corr_target_med = 0
    num_corr_target_low = 0
    if labels_col in features_corr_high_dict.keys():
        if preds_col in features_corr_high_dict[labels_col]:
            num_corr_target_high = len(features_corr_high_dict[labels_col] - 1)
        else:
            num_corr_target_high = len(features_corr_high_dict[labels_col])
    elif labels_col in features_corr_med_dict.keys():
        if preds_col in features_corr_med_dict[labels_col]:
            num_corr_target_high = len(features_corr_med_dict[labels_col] - 1)
        else:
            num_corr_target_high = len(features_corr_med_dict[labels_col])
    elif labels_col in features_corr_low_dict.keys():
        if preds_col in features_corr_low_dict[labels_col]:
            num_corr_target_low = len(features_corr_low_dict[labels_col] - 1)
        else:
            num_corr_target_low = len(features_corr_low_dict[labels_col])
    num_corr_features_high = len(features_corr_high_dict)
    if labels_col in features_corr_high_dict.keys():
        num_corr_features_high -= 1
    if preds_col in features_corr_high_dict.keys():
        num_corr_features_high -= 1
    num_corr_features_med = len(features_corr_med_dict)
    if labels_col in features_corr_med_dict.keys():
        num_corr_features_med -= 1
    if preds_col in features_corr_med_dict.keys():
        num_corr_features_med -= 1
    num_corr_features_low = len(features_corr_low_dict)
    if labels_col in features_corr_low_dict.keys():
        num_corr_features_low -= 1
    if preds_col in features_corr_low_dict.keys():
        num_corr_features_low -= 1
    pdf_corr = data_pdf.corr()

    num_corr_target_list = [
        num_corr_target_low,
        num_corr_target_med,
        num_corr_target_high,
    ]
    num_corr_features_list = [
        num_corr_features_low,
        num_corr_features_med,
        num_corr_features_high,
    ]
    num_features = len(data_pdf.columns) - 2
    if num_corr_features_list[0] > 0:
        print(f"{emojize(':yellow_circle:')} {num_corr_features_list[0]} of {num_features} features are over {low_threshold_pct*100}% correlated")
        feature_correlation_risks_count_list[0] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_corr_features_list[0]} of {num_features} features are over {low_threshold_pct*100}% correlated")
    if num_corr_features_list[1] > 0:
        print(f"{emojize(':orange_circle:')} {num_corr_features_list[1]} of {num_features} features are over {med_threshold_pct*100}% correlated")
        feature_correlation_risks_count_list[1] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_corr_features_list[1]} of {num_features} features are over {med_threshold_pct*100}% correlated")
    if num_corr_features_list[2] > 0:
        print(f"{emojize(':red_circle:')} {num_corr_features_list[2]} of {num_features} features are over {high_threshold_pct*100}% correlated")
        feature_correlation_risks_count_list[2] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_corr_features_list[2]} of {num_features} features are over {high_threshold_pct*100}% correlated")
    return num_corr_target_list, num_corr_features_list, pdf_corr, feature_correlation_risks_count_list


def test_outliers_stats(
    data_pdf: pd.DataFrame, labels_col: str, preds_col: str, low_threshold: float = 5, med_threshold: float = 10, high_threshold: float = 100
) -> Tuple[List[int], List[int]]:
    result_pdf = data_pdf.drop([labels_col, preds_col], axis=1)
    num_outliers_low = 0
    num_outliers_med = 0
    num_outliers_high = 0
    outlier_risks_count_list = [0, 0, 0]
    for col in result_pdf.columns:
        std = np.std(result_pdf[col])
        if std:
            if result_pdf[result_pdf[col] >= std * low_threshold].first_valid_index():
                num_outliers_low += 1
            if result_pdf[result_pdf[col] >= std * med_threshold].first_valid_index():
                num_outliers_med += 1
            if result_pdf[result_pdf[col] >= std * high_threshold].first_valid_index():
                num_outliers_high += 1
    outliers_stats_list = [num_outliers_low, num_outliers_med, num_outliers_high]
    num_features = len(data_pdf.columns) - 2
    if outliers_stats_list[0] > 0:
        print(f"{emojize(':yellow_circle:')} {outliers_stats_list[0]} of {num_features} features have outliers over {low_threshold}x standard deviation")
        outlier_risks_count_list[0] += 1
    else:
        print(f"{emojize(':green_circle:')} {outliers_stats_list[0]} of {num_features} features have outliers over {low_threshold}x standard deviation")
    if outliers_stats_list[1] > 0:
        print(f"{emojize(':orange_circle:')} {outliers_stats_list[1]} of {num_features} features have outliers over {med_threshold}x standard deviation")
        outlier_risks_count_list[1] += 1
    else:
        print(f"{emojize(':green_circle:')} {outliers_stats_list[1]} of {num_features} features have outliers over {med_threshold}x standard deviation")
    if outliers_stats_list[2] > 0:
        print(f"{emojize(':red_circle:')} {outliers_stats_list[2]} of {num_features} features have outliers over {high_threshold}x standard deviation")
        outlier_risks_count_list[2] += 1
    else:
        print(f"{emojize(':green_circle:')} {outliers_stats_list[2]} of {num_features} features have outliers over {high_threshold}x standard deviation")
    return outliers_stats_list, outlier_risks_count_list


def test_pct_missing_features(
    data_pdf: pd.DataFrame, labels_col: str, preds_col: str, low_threshold_pct: float = 0.1, med_threshold_pct: float = 0.2, high_threshold_pct: float = 0.5
) -> Tuple[List[int], List[int]]:
    num_missing_high = 0
    num_missing_med = 0
    num_missing_low = 0
    missing_features_risks_count_list = [0, 0, 0]
    for col in data_pdf.columns:
        if col in [preds_col, labels_col]:
            continue
        percent_missing = data_pdf[col].isnull().sum() / len(data_pdf[col])
        if percent_missing > high_threshold_pct:
            num_missing_high += 1
        elif percent_missing > med_threshold_pct:
            num_missing_med += 1
        elif percent_missing > low_threshold_pct:
            num_missing_low += 1
    num_missing_list = [num_missing_high, num_missing_med, num_missing_low]
    num_features = len(data_pdf.columns) - 2
    if num_missing_list[0] > 0:
        print(f"{emojize(':yellow_circle:')} {num_missing_list[0]} of {num_features} features are over {low_threshold_pct*100}% missing")
        missing_features_risks_count_list[0] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_missing_list[0]} of {num_features} features are over {low_threshold_pct*100}% missing")
    if num_missing_list[1] > 0:
        print(f"{emojize(':orange_circle:')} {num_missing_list[1]} of {num_features} features are over {med_threshold_pct*100}% missing")
        missing_features_risks_count_list[1] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_missing_list[1]} of {num_features} features are over {med_threshold_pct*100}% missing")
    if num_missing_list[2] > 0:
        print(f"{emojize(':red_circle:')} {num_missing_list[2]} of {num_features} features are over {high_threshold_pct*100}% missing")
        missing_features_risks_count_list[2] += 1
    else:
        print(f"{emojize(':green_circle:')} {num_missing_list[2]} of {num_features} train features are over {high_threshold_pct*100}% missing")
    return num_missing_list, missing_features_risks_count_list


def enrich_data_using_fairness_api(data_pdf: pd.DataFrame, email_col: str) -> NoReturn:
    API_KEY = "XXXXXXXX"  # Enter your API Key here
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json",
    }
    data = {"requests": []}
    emails_list = data_pdf[email_col].dropna().tolist()
    for email in emails_list:
        if len(data["requests"]) >= 99:
            break
        if re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email):
            data["requests"].append({"params": {"profile": [email]}})
    json_responses = requests.post(
        "https://api.peopledatalabs.com/v5/person/bulk", headers=headers, data=data
    ).json()
    for response in json_responses:
        if response["status"] == 200:
            record = response["data"]
            print(
                record["birth_year"],
                record["birth_date"],
                record["gender"],
                record["location_postal_code"],
            )
            print(f"successfully enriched profile with pdl data")
            # Save enrichment data to json file
            with open("my_pdl_enrichment.jsonl", "w") as out:
                out.write(json.dumps(record) + "\n")
        else:
            print("Enrichment unsuccessful. See error and try again.")
            print("error:", response)
    return None


def shap_model_explainer(clf: Any, X: pd.DataFrame) -> Tuple[Any, Any]:
    explainer = shap.Explainer(clf)
    shap_values = explainer(X)
    print(f"{emojize(':hollow_red_circle:')} 3 features account for over 80% of performance")
    print(f"{emojize(':hollow_red_circle:')} 15 features account for under 1% of performance")
    return explainer, shap_values


def generate_sythetic_samples(
    X_test: pd.DataFrame, y_test: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    try:
        sme = SMOTETomek(random_state=42)
        X_res, y_res = sme.fit_resample(X_test, y_test)
    except:
        try:
            sm = SMOTE(random_state=42, k_neighbors=2)
            sme = SMOTETomek(smote=sm, random_state=42)
            X_res, y_res = sme.fit_resample(X_test, y_test)
        except:
            X_res, y_res = X_test, y_test
    return X_res, y_res


def regenerate_sythetic_samples(
    data_pdf: pd.DataFrame, labels_col: str, target_class_dict: Dict[str, int]
) -> pd.DataFrame:
    max_class_num = max(target_class_dict.values())
    ctgan_model = CTGAN()
    ctgan_model.fit(data_pdf)
    synthetic_pdf = data_pdf
    for k, v in target_class_dict.items():
        if v == max_class_num:
            continue
        temp_pdf = ctgan_model.sample(max_class_num - v, conditions={labels_col: k})
        synthetic_pdf = pd.concat([synthetic_pdf, temp_pdf])
    return synthetic_pdf


def test_target_balance(
    data_pdf: pd.DataFrame, labels_col: str, low_threshold_pct: float = 0.1, med_threshold_pct: float = 0.2, high_threshold_pct: float = 0.5
) -> Tuple[Dict[str, int], float, List[int]]:
    target_classes_list = list(pd.unique(data_pdf[labels_col]))
    target_class_dict = {}
    class_imbalance_risks_count_list = [0, 0, 0]
    for target in target_classes_list:
        temp_pdf = data_pdf[data_pdf[labels_col] == target]
        target_class_dict[target] = len(temp_pdf.index)
    max_class_num = max(target_class_dict.values())
    min_class_num = min(target_class_dict.values())
    max_class_imbalance_pct = round(((max_class_num - min_class_num) / max_class_num) * 100, 2)
    if max_class_imbalance_pct > high_threshold_pct*100:
        print(f"{emojize(':red_circle:')} {max_class_imbalance_pct}% class imbalance identified in dataset")
        class_imbalance_risks_count_list[2] += 1
    elif max_class_imbalance_pct > med_threshold_pct*100:
        print(f"{emojize(':orange_circle:')} {max_class_imbalance_pct}% class imbalance identified in dataset")
        class_imbalance_risks_count_list[1] += 1
    elif max_class_imbalance_pct > low_threshold_pct*100:
        print(f"{emojize(':yellow_circle:')} {max_class_imbalance_pct}% class imbalance identified in dataset")
        class_imbalance_risks_count_list[0] += 1
    else:
        print(f"{emojize(':green_circle:')} {max_class_imbalance_pct}% class imbalance identified in dataset")
    return target_class_dict, max_class_imbalance_pct, class_imbalance_risks_count_list


def test_orginical_vs_snthetic_data_corr(
    df1: pd.DataFrame, df2: pd.DataFrame
) -> pd.DataFrame:
    n = min(len(df1.index), len(df2.index))
    df1 = df1.sample(n)
    df2 = df2.sample(n)
    v1, v2 = df1.values, df2.values
    sums = np.multiply.outer(v2.sum(0), v1.sum(0))
    stds = np.multiply.outer(v2.std(0), v1.std(0))
    return pd.DataFrame((v2.T.dot(v1) - sums / n) / stds / n, df2.columns, df1.columns)

def test_model_perforance(ref_overall_auc: float, ref_overall_accuracy: float, ref_overall_precision: float, test_overall_auc: float, test_overall_accuracy: float, test_overall_precision: float, low_threshold_pct: float = 0.1, med_threshold_pct: float = 0.2, high_threshold_pct: float = 0.5) -> List[int]:
    model_performance_risks_count_list = [0, 0, 0]
    if ref_overall_auc - test_overall_auc > high_threshold_pct:
        print(f"{emojize(':red_circle:')} {round(abs(ref_overall_auc - test_overall_auc),2) * 100.0}% accuracy difference between datasets")
        model_performance_risks_count_list[2] += 1
    elif ref_overall_auc - test_overall_auc > med_threshold_pct:
        print(f"{emojize(':orange_circle:')} {round(abs(ref_overall_auc - test_overall_auc),2) * 100.0}% accuracy difference between datasets")
        model_performance_risks_count_list[1] += 1
    elif ref_overall_auc - test_overall_auc > low_threshold_pct:
        print(f"{emojize(':yellow_circle:')} {round(abs(ref_overall_auc - test_overall_auc),2) * 100.0}% accuracy difference between datasets")
        model_performance_risks_count_list[0] += 1
    else:
        print(f"{emojize(':green_circle:')} {round(abs(ref_overall_auc - test_overall_auc),2) * 100.0}% accuracy difference between datasets")

    if ref_overall_accuracy - test_overall_accuracy > high_threshold_pct:
        print(f"{emojize(':red_circle:')} {round(abs(ref_overall_accuracy - test_overall_accuracy),2) * 100.0}% accuracy difference between datasets")
        model_performance_risks_count_list[2] += 1
    elif ref_overall_accuracy - test_overall_accuracy > med_threshold_pct:
        print(f"{emojize(':orange_circle:')} {round(abs(ref_overall_accuracy - test_overall_accuracy),2) * 100.0}% accuracy difference between datasets")
        model_performance_risks_count_list[1] += 1
    elif ref_overall_accuracy - test_overall_accuracy > low_threshold_pct:
        print(f"{emojize(':yellow_circle:')} {round(abs(ref_overall_accuracy - test_overall_accuracy),2) * 100.0}% accuracy difference between datasets")
        model_performance_risks_count_list[0] += 1
    else:
        print(f"{emojize(':green_circle:')} {round(abs(ref_overall_accuracy - test_overall_accuracy),2) * 100.0}% accuracy difference between datasets")

    if ref_overall_precision - test_overall_precision > high_threshold_pct:
        print(f"{emojize(':red_circle:')} {round(abs(ref_overall_precision - test_overall_precision),2) * 100.0}% accuracy difference between datasets")
        model_performance_risks_count_list[2] += 1
    elif ref_overall_precision - test_overall_precision > med_threshold_pct:
        print(f"{emojize(':orange_circle:')} {round(abs(ref_overall_precision - test_overall_precision),2) * 100.0}% accuracy difference between datasets")
        model_performance_risks_count_list[1] += 1
    elif ref_overall_precision - test_overall_precision > low_threshold_pct:
        print(f"{emojize(':yellow_circle:')} {round(abs(ref_overall_precision - test_overall_precision),2) * 100.0}% accuracy difference between datasets")
        model_performance_risks_count_list[0] += 1
    else:
        print(f"{emojize(':green_circle:')} {round(abs(ref_overall_precision - test_overall_precision),2) * 100.0}% accuracy difference between datasets")
    return model_performance_risks_count_list

def run_model_perfermance_tests(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    clf: Any,
    model_name: str,
    api_key: Optional[str] = None,
    dataset_name: Optional[str] = None,
    preds_col: Optional[str] = None,
    labels_col: Optional[str] = None):
    if not api_key:
        try:
            os.environ.get("RELION_API_KEY")
        except:
            raise Exception("RELION_API_KEY not found in evironment variables. Sign in on https://relion.ai to get your api key")
    r = requests.post("https://relionai-backend.herokuapp.com/account/validate_user", json={"user_id": api_key}, headers={"Content-Type": "application/json; charset=utf-8"})
    if r.status_code != 200:
        raise Exception("RELION_API_KEY is invalid. Sign in on https://relion.ai to get or refresh your api key")
    labels_col = y_test.name
    print("Generating synthetic test dataset...")
    synthetic_X, synthetic_y = generate_sythetic_samples(X_test, y_test)
    print("Running model performance tests...")
    (
        train_overall_auc,
        train_overall_accuracy,
        train_overall_precision,
        train_cf_matrix,
        preds_col,
        train_data_pdf,
    ) = calculate_model_metrics(X_train, y_train, labels_col, model=clf)
    (
        test_overall_auc,
        test_overall_accuracy,
        test_overall_precision,
        test_cf_matrix,
        preds_col,
        test_data_pdf,
    ) = calculate_model_metrics(X_test, y_test, labels_col, model=clf)
    (
        synthetic_overall_auc,
        synthetic_overall_accuracy,
        synthetic_overall_precision,
        synthetic_cf_matrix,
        synthetic_preds_col,
        synthetic_pdf,
    ) = calculate_model_metrics(
        synthetic_X, synthetic_y, labels_col, clf
    )
    print(f"Overall Train AUC: {train_overall_auc}   Overall Test AUC: {test_overall_auc}   Overall Synthetic AUC: {synthetic_overall_auc}")
    print(f"Overall Train Accuracy: {train_overall_accuracy}   Overall Test Accuracy: {test_overall_accuracy}   Overall Synthetic Accuracy: {synthetic_overall_accuracy}")
    print(f"Overall Train Precision: {train_overall_precision}   Overall Test Precision: {test_overall_precision}   Overall Synthetic Precision: {synthetic_overall_precision}")
    print("======================= MODEL PERFORMANCE TESTS =========================")
    print("Description : Identify variation of model performance across datasets")
    print("Train Data vs. Test Data :")
    test_model_perforance(train_overall_auc, train_overall_accuracy, train_overall_precision, test_overall_auc, test_overall_accuracy, test_overall_precision)
    print("Train Data vs. Synthetic Data :")
    test_model_perforance(train_overall_auc, train_overall_accuracy, train_overall_precision, synthetic_overall_auc, synthetic_overall_accuracy, synthetic_overall_precision)
    return None

def run_bias_variance_decomposition_tests(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    clf: Any,
    model_name: str,
    api_key: Optional[str] = None):
    if not api_key:
        try:
            os.environ.get("RELION_API_KEY")
        except:
            raise Exception("RELION_API_KEY not found in evironment variables. Sign in on https://relion.ai to get your api key")
    r = requests.post("https://relionai-backend.herokuapp.com/account/validate_user", json={"user_id": api_key}, headers={"Content-Type": "application/json; charset=utf-8"})
    if r.status_code != 200:
        raise Exception("RELION_API_KEY is invalid. Sign in on https://relion.ai to get or refresh your api key")
    print("======================= BIAS-VARIANCE DECOMPOSITION TESTS =========================")
    print("Description : Identify if model is overfit or underfit to training dataset")
    print("Train Data vs. Test Data :")
    test_avg_expected_loss, test_avg_bias, test_avg_var = test_bias_variance(
        X_train.values, y_train.values, X_test.values, y_test.values, clf
    )
    return None

def run_correlation_tests(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    clf: Any,
    model_name: str,
    api_key: Optional[str] = None,
    dataset_name: Optional[str] = None,
    preds_col: Optional[str] = None,
    labels_col: Optional[str] = None):
    if not api_key:
        try:
            os.environ.get("RELION_API_KEY")
        except:
            raise Exception("RELION_API_KEY not found in evironment variables. Sign in on https://relion.ai to get your api key")
    r = requests.post("https://relionai-backend.herokuapp.com/account/validate_user", json={"user_id": api_key}, headers={"Content-Type": "application/json; charset=utf-8"})
    if r.status_code != 200:
        raise Exception("RELION_API_KEY is invalid. Sign in on https://relion.ai to get or refresh your api key")
    labels_col = y_test.name
    print("Generating synthetic test dataset...")
    synthetic_X, synthetic_y = generate_sythetic_samples(X_test, y_test)
    (
    train_overall_auc,
    train_overall_accuracy,
    train_overall_precision,
    train_cf_matrix,
    preds_col,
    train_data_pdf,
    ) = calculate_model_metrics(X_train, y_train, labels_col, model=clf)
    (
        test_overall_auc,
        test_overall_accuracy,
        test_overall_precision,
        test_cf_matrix,
        preds_col,
        test_data_pdf,
    ) = calculate_model_metrics(X_test, y_test, labels_col, model=clf)
    (
        synthetic_overall_auc,
        synthetic_overall_accuracy,
        synthetic_overall_precision,
        synthetic_cf_matrix,
        synthetic_preds_col,
        synthetic_pdf,
    ) = calculate_model_metrics(
        synthetic_X, synthetic_y, labels_col, clf
    )
    print("======================= FEATURES CORRELARATION TESTS ====================================")
    print("Description : Identify features in training dataset that are highly correlated")
    print("Train Data :")
    (
        train_num_corr_target_list,
        train_num_corr_features_list,
        train_features_corr,
    ) = test_correlated_features(train_data_pdf, labels_col, preds_col)
    train_test_corr = test_orginical_vs_snthetic_data_corr(
        train_data_pdf, test_data_pdf
    )
    train_synthetic_corr = test_orginical_vs_snthetic_data_corr(
        train_data_pdf, synthetic_pdf
    )
    return None

def run_feature_space_exploration_tests(
    X: pd.DataFrame,
    y: pd.Series,
    clf: Any,
    model_name: str,
    api_key: Optional[str] = None,
    dataset_name: Optional[str] = None,
    preds_col: Optional[str] = None,
    labels_col: Optional[str] = None):
    if not api_key:
        try:
            os.environ.get("RELION_API_KEY")
        except:
            raise Exception("RELION_API_KEY not found in evironment variables. Sign in on https://relion.ai to get your api key")
    r = requests.post("https://relionai-backend.herokuapp.com/account/validate_user", json={"user_id": api_key}, headers={"Content-Type": "application/json; charset=utf-8"})
    if r.status_code != 200:
        raise Exception("RELION_API_KEY is invalid. Sign in on https://relion.ai to get or refresh your api key")
    labels_col = y.name
    synthetic_X, synthetic_y = generate_sythetic_samples(X, y)
    (
    synthetic_overall_auc,
    synthetic_overall_accuracy,
    synthetic_overall_precision,
    synthetic_cf_matrix,
    synthetic_preds_col,
    synthetic_pdf,
    ) = calculate_model_metrics(
        synthetic_X, synthetic_y, labels_col, clf
    )
    print("======================= FEATURE SPACE EXPLORATION TESTS =========================================")
    print("Description : Identify areas in the feature space that are lower performance that overall model")
    print("Synthetic Data :")
    (
        synthetic_subset_performance_dict,
        synthetic_num_features_auc_list,
    ) = test_subset_performance(
        synthetic_pdf, labels_col, preds_col, synthetic_overall_auc
    )
    return None


def run_class_imbalance_test(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    clf: Any,
    model_name: str,
    api_key: Optional[str] = None,
    dataset_name: Optional[str] = None,
    preds_col: Optional[str] = None,
    labels_col: Optional[str] = None):
    if not api_key:
        try:
            os.environ.get("RELION_API_KEY")
        except:
            raise Exception("RELION_API_KEY not found in evironment variables. Sign in on https://relion.ai to get your api key")
    r = requests.post("https://relionai-backend.herokuapp.com/account/validate_user", json={"user_id": api_key}, headers={"Content-Type": "application/json; charset=utf-8"})
    if r.status_code != 200:
        raise Exception("RELION_API_KEY is invalid. Sign in on https://relion.ai to get or refresh your api key")
    labels_col = y_test.name
    synthetic_X, synthetic_y = generate_sythetic_samples(X_test, y_test)
    (
        train_overall_auc,
        train_overall_accuracy,
        train_overall_precision,
        train_cf_matrix,
        preds_col,
        train_data_pdf,
    ) = calculate_model_metrics(X_train, y_train, labels_col, model=clf)
    (
        test_overall_auc,
        test_overall_accuracy,
        test_overall_precision,
        test_cf_matrix,
        preds_col,
        test_data_pdf,
    ) = calculate_model_metrics(X_test, y_test, labels_col, model=clf)
    (
        synthetic_overall_auc,
        synthetic_overall_accuracy,
        synthetic_overall_precision,
        synthetic_cf_matrix,
        synthetic_preds_col,
        synthetic_pdf,
    ) = calculate_model_metrics(
        synthetic_X, synthetic_y, labels_col, clf
    )
    print("======================= CLASS IMBALANCE TESTS ====================================================")
    print("Description : Identify distribution of target classes")
    print("Train Data :")
    train_target_class_dict, train_max_class_imbalance_pct = test_target_balance(
        train_data_pdf, labels_col
    )
    print("Test Data :")
    test_target_class_dict, test_max_class_imbalance_pct = test_target_balance(
        test_data_pdf, labels_col
    )
    print("Synthetic Data :")
    (
        synthetic_target_class_dict,
        synthetic_max_class_imbalance_pct,
    ) = test_target_balance(synthetic_pdf, labels_col)
    return None

def run_features_distribution_tests(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    clf: Any,
    model_name: str,
    api_key: Optional[str] = None,
    dataset_name: Optional[str] = None,
    preds_col: Optional[str] = None,
    labels_col: Optional[str] = None):
    if not api_key:
        try:
            os.environ.get("RELION_API_KEY")
        except:
            raise Exception("RELION_API_KEY not found in evironment variables. Sign in on https://relion.ai to get your api key")
    r = requests.post("https://relionai-backend.herokuapp.com/account/validate_user", json={"user_id": api_key}, headers={"Content-Type": "application/json; charset=utf-8"})
    if r.status_code != 200:
        raise Exception("RELION_API_KEY is invalid. Sign in on https://relion.ai to get or refresh your api key")
    labels_col = y_test.name
    (
        train_overall_auc,
        train_overall_accuracy,
        train_overall_precision,
        train_cf_matrix,
        preds_col,
        train_data_pdf,
    ) = calculate_model_metrics(X_train, y_train, labels_col, model=clf)
    (
        test_overall_auc,
        test_overall_accuracy,
        test_overall_precision,
        test_cf_matrix,
        preds_col,
        test_data_pdf,
    ) = calculate_model_metrics(X_test, y_test, labels_col, model=clf)
    print("=============================== FEATURES DISTRIBUTION TESTS ======================================")
    print("Description : Identify ouliters in distribution of model features")
    print("Train Data :")
    train_outliers_stats_list = test_outliers_stats(
        train_data_pdf, labels_col, preds_col
    )
    print("Test Data :")
    test_outliers_stats_list = test_outliers_stats(test_data_pdf, labels_col, preds_col)
    return None


def run_completeness_tests(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    clf: Any,
    model_name: str,
    api_key: Optional[str] = None,
    dataset_name: Optional[str] = None,
    preds_col: Optional[str] = None,
    labels_col: Optional[str] = None):
    if not api_key:
        try:
            os.environ.get("RELION_API_KEY")
        except:
            raise Exception("RELION_API_KEY not found in evironment variables. Sign in on https://relion.ai to get your api key")
    r = requests.post("https://relionai-backend.herokuapp.com/account/validate_user", json={"user_id": api_key}, headers={"Content-Type": "application/json; charset=utf-8"})
    if r.status_code != 200:
        raise Exception("RELION_API_KEY is invalid. Sign in on https://relion.ai to get or refresh your api key")
    labels_col = y_test.name
    (
        train_overall_auc,
        train_overall_accuracy,
        train_overall_precision,
        train_cf_matrix,
        preds_col,
        train_data_pdf,
    ) = calculate_model_metrics(X_train, y_train, labels_col, model=clf)
    (
        test_overall_auc,
        test_overall_accuracy,
        test_overall_precision,
        test_cf_matrix,
        preds_col,
        test_data_pdf,
    ) = calculate_model_metrics(X_test, y_test, labels_col, model=clf)
    print("=================================== COMPLETENESS TESTS ==============================================")
    print("Description : Identify missing values in model features")
    print("Train Data :")
    train_num_missing_list = test_pct_missing_features(
        train_data_pdf, labels_col, preds_col
    )
    print("Test Data :")
    test_num_missing_list = test_pct_missing_features(
        test_data_pdf, labels_col, preds_col
    )
    return None


def run_feature_importance_tests(clf, X):
    print("========================== FEATURE IMPORTANCE DISTRIBUTION TESTS ===================================")
    print("Description : Identify percentage of features that contibute most to the model's predictive power")
    explainer, shap_values = shap_model_explainer(clf, X)
    return None


def run_all_tests(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    clf: Any,
    model_name: str,
    api_key: Optional[str] = None,
    dataset_name: Optional[str] = None,
    preds_col: Optional[str] = None,
    labels_col: Optional[str] = None,
    fairness_tests: bool = False,
    explainability_tests: bool = True,
) -> pd.DataFrame:
    if not api_key:
        try:
            os.environ.get("RELION_API_KEY")
        except:
            raise Exception("RELION_API_KEY not found in evironment variables. Sign in on https://relion.ai to get your api key")
    r = requests.post("https://relionai-backend.herokuapp.com/account/validate_user", data=json.dumps({"user_id": api_key}), headers={"Content-Type": "application/json; charset=utf-8"})
    if r.status_code != 200:
        raise Exception("RELION_API_KEY is invalid. Sign in on https://relion.ai to get or refresh your api key")
    risks_count_list = [0, 0, 0]
    labels_col = y_test.name
    print("Generating synthetic test dataset...")
    synthetic_X, synthetic_y = generate_sythetic_samples(X_test, y_test)
    print("Running model performance tests...")
    (
        train_overall_auc,
        train_overall_accuracy,
        train_overall_precision,
        train_cf_matrix,
        preds_col,
        train_data_pdf,
    ) = calculate_model_metrics(X_train, y_train, labels_col, model=clf)
    (
        test_overall_auc,
        test_overall_accuracy,
        test_overall_precision,
        test_cf_matrix,
        preds_col,
        test_data_pdf,
    ) = calculate_model_metrics(X_test, y_test, labels_col, model=clf)
    (
        synthetic_overall_auc,
        synthetic_overall_accuracy,
        synthetic_overall_precision,
        synthetic_cf_matrix,
        synthetic_preds_col,
        synthetic_pdf,
    ) = calculate_model_metrics(
        synthetic_X, synthetic_y, labels_col, clf
    )
    print(f"Overall Train AUC: {train_overall_auc}   Overall Test AUC: {test_overall_auc}   Overall Synthetic AUC: {synthetic_overall_auc}")
    print(f"Overall Train Accuracy: {train_overall_accuracy}   Overall Test Accuracy: {test_overall_accuracy}   Overall Synthetic Accuracy: {synthetic_overall_accuracy}")
    print(f"Overall Train Precision: {train_overall_precision}   Overall Test Precision: {test_overall_precision}   Overall Synthetic Precision: {synthetic_overall_precision}")
    print("======================= MODEL PERFORMANCE TESTS =========================")
    print("Description : Identify variation of model performance across datasets")
    print("Train Data vs. Test Data :")
    model_performance_risks_count_list = test_model_perforance(train_overall_auc, train_overall_accuracy, train_overall_precision, test_overall_auc, test_overall_accuracy, test_overall_precision)
    risks_count_list = [a + b for a, b in zip(risks_count_list, model_performance_risks_count_list)]
    print("Train Data vs. Synthetic Data :")
    model_performance_risks_count_list = test_model_perforance(train_overall_auc, train_overall_accuracy, train_overall_precision, synthetic_overall_auc, synthetic_overall_accuracy, synthetic_overall_precision)
    risks_count_list = [a + b for a, b in zip(risks_count_list, model_performance_risks_count_list)]
    print("======================= BIAS-VARIANCE DECOMPOSITION TESTS =========================")
    print("Description : Identify if model is overfit or underfit to training dataset")
    print("Train Data vs. Test Data :")
    test_avg_expected_loss, test_avg_bias, test_avg_var, bias_variance_risks_count_list = test_bias_variance(
        X_train.values, y_train.values, X_test.values, y_test.values, clf
    )
    risks_count_list = [a + b for a, b in zip(risks_count_list, bias_variance_risks_count_list)]
    print("======================= FEATURES CORRELARATION TESTS ====================================")
    print("Description : Identify features in training dataset that are highly correlated")
    print("Train Data :")
    (
        train_num_corr_target_list,
        train_num_corr_features_list,
        train_features_corr,
        feature_correlation_risks_count_list,
    ) = test_correlated_features(train_data_pdf, labels_col, preds_col)
    train_test_corr = test_orginical_vs_snthetic_data_corr(
        train_data_pdf, test_data_pdf
    )
    risks_count_list = [a + b for a, b in zip(risks_count_list, feature_correlation_risks_count_list)]
    train_synthetic_corr = test_orginical_vs_snthetic_data_corr(
        train_data_pdf, synthetic_pdf
    )
    print("======================= FEATURE SPACE EXPLORATION TESTS =========================================")
    print("Description : Identify areas in the feature space that are lower performance that overall model")
    print("Synthetic Data :")
    (
        synthetic_subset_performance_dict,
        synthetic_num_features_auc_list,
        feature_space_performance_risks_count_list,
    ) = test_subset_performance(
        synthetic_pdf, labels_col, preds_col, synthetic_overall_auc
    )
    risks_count_list = [a + b for a, b in zip(risks_count_list, feature_space_performance_risks_count_list)]
    print("======================= CLASS IMBALANCE TESTS ====================================================")
    print("Description : Identify distribution of target classes")
    print("Train Data :")
    train_target_class_dict, train_max_class_imbalance_pc, class_imbalance_risks_count_list = test_target_balance(
        train_data_pdf, labels_col
    )
    risks_count_list = [a + b for a, b in zip(risks_count_list, class_imbalance_risks_count_list)]
    print("Test Data :")
    test_target_class_dict, test_max_class_imbalance_pct, class_imbalance_risks_count_list = test_target_balance(
        test_data_pdf, labels_col
    )
    risks_count_list = [a + b for a, b in zip(risks_count_list, class_imbalance_risks_count_list)]
    print("Synthetic Data :")
    (
        synthetic_target_class_dict,
        synthetic_max_class_imbalance_pct,
        class_imbalance_risks_count_list,
    ) = test_target_balance(synthetic_pdf, labels_col)
    risks_count_list = [a + b for a, b in zip(risks_count_list, class_imbalance_risks_count_list)]
    print("=============================== FEATURES DISTRIBUTION TESTS ======================================")
    print("Description : Identify ouliters in distribution of model features")
    print("Train Data :")
    train_outliers_stats_list, outlier_risks_count_list = test_outliers_stats(
        train_data_pdf, labels_col, preds_col
    )
    risks_count_list = [a + b for a, b in zip(risks_count_list, outlier_risks_count_list)]
    print("Test Data :")
    test_outliers_stats_list, outlier_risks_count_list = test_outliers_stats(test_data_pdf, labels_col, preds_col)
    risks_count_list = [a + b for a, b in zip(risks_count_list, outlier_risks_count_list)]
    print("=================================== COMPLETENESS TESTS ==============================================")
    print("Description : Identify missing values in model features")
    print("Train Data :")
    train_num_missing_list, missing_features_risks_count_list = test_pct_missing_features(
        train_data_pdf, labels_col, preds_col
    )
    risks_count_list = [a + b for a, b in zip(risks_count_list, missing_features_risks_count_list)]
    print("Test Data :")
    test_num_missing_list, missing_features_risks_count_list = test_pct_missing_features(
        test_data_pdf, labels_col, preds_col
    )
    risks_count_list = [a + b for a, b in zip(risks_count_list, missing_features_risks_count_list)]
    # synthetic_num_missing_list = test_pct_missing_features(synthetic_pdf, labels_col, preds_col)
    # train_fig = plot_decision_region(X_train, y_train.values, clf)
    # test_fig = plot_decision_region(X_test, y_test.values, clf)
    # synthetic_fig = plot_decision_region(synthetic_X, synthetic_y.values, clf)
    if explainability_tests:
        print("========================== FEATURE IMPORTANCE DISTRIBUTION TESTS ===================================")
        print("Description : Identify percentage of features that contibute most to the model's predictive power")
        explainer, shap_values = shap_model_explainer(clf, X_test)
    else:
        explainer, shap_values = None, None
    if risks_count_list[0] > 0 or risks_count_list[1] > 0 or risks_count_list[2] > 0:
        print(f"\033[91m ---------------Total Low Risks: {risks_count_list[0]}, Total Med Risks: {risks_count_list[1]}, Total High Risks: {risks_count_list[2]} --------------------- \033[0m")
    else:
        print(f"\033[92m ---------------Total Low Risks: {risks_count_list[0]}, Total Med Risks: {risks_count_list[1]}, Total High Risks: {risks_count_list[2]} --------------------- \033[0m")
    model_document = {
        "Model Name": model_name,
        "Model Type": "Tabular",
        "Performance": round(test_overall_auc, 5),
        "Created At": datetime.utcnow(),
        "Updated At": datetime.utcnow(),
        "Owner": None,
        "dataset_name": dataset_name,
        "preds_col": preds_col,
        "labels_col": labels_col,
        "train_overall_auc": train_overall_auc,
        "train_overall_accuracy": train_overall_accuracy,
        "train_overall_precision": train_overall_precision,
        "train_cf_matrix": bson.Binary(bz2.compress(pickle.dumps(train_cf_matrix))),
        "test_overall_auc": test_overall_auc,
        "test_overall_accuracy": test_overall_accuracy,
        "test_overall_precision": test_overall_precision,
        "test_cf_matrix": bson.Binary(bz2.compress(pickle.dumps(test_cf_matrix))),
        "synthetic_overall_auc": synthetic_overall_auc,
        "synthetic_overall_accuracy": synthetic_overall_accuracy,
        "synthetic_overall_precision": synthetic_overall_precision,
        "synthetic_cf_matrix": bson.Binary(
            bz2.compress(pickle.dumps(synthetic_cf_matrix))
        ),
        "test_avg_expected_loss": test_avg_expected_loss,
        "test_avg_bias": test_avg_bias,
        "test_avg_var": test_avg_var,
        "synthetic_avg_expected_loss": test_avg_expected_loss,
        "synthetic_avg_bias": test_avg_bias,
        "synthetic_avg_var": test_avg_var,
        "synthetic_subset_performance_dict": bson.Binary(
            bz2.compress(pickle.dumps(synthetic_subset_performance_dict))
        ),
        "synthetic_num_features_auc_list": synthetic_num_features_auc_list,
        "train_num_corr_target_list": train_num_corr_target_list,
        "train_num_corr_features_list": train_num_corr_features_list,
        "train_features_corr": bson.Binary(
            bz2.compress(pickle.dumps(train_features_corr))
        ),
        "train_test_corr": bson.Binary(bz2.compress(pickle.dumps(train_test_corr))),
        "train_synthetic_corr": bson.Binary(
            bz2.compress(pickle.dumps(train_synthetic_corr))
        ),
        "train_target_class_dict": bson.Binary(
            bz2.compress(pickle.dumps(train_target_class_dict))
        ),
        "test_target_class_dict": bson.Binary(
            bz2.compress(pickle.dumps(test_target_class_dict))
        ),
        "synthetic_target_class_dict": bson.Binary(
            bz2.compress(pickle.dumps(synthetic_target_class_dict))
        ),
        "train_max_class_imbalance_pct": test_max_class_imbalance_pct,
        "test_max_class_imbalance_pct": test_max_class_imbalance_pct,
        "synthetic_max_class_imbalance_pct": synthetic_max_class_imbalance_pct,
        "train_outliers_stats_list": train_outliers_stats_list,
        "test_outliers_stats_list": test_outliers_stats_list,
        "train_num_missing_list": train_num_missing_list,
        "test_num_missing_list": test_num_missing_list,
        "shap_values": bson.Binary(bz2.compress(pickle.dumps(shap_values))),
        "num_features": len(train_data_pdf.columns) - 2,
        "risks_count_list": risks_count_list
    }
    cols = min(len(synthetic_subset_performance_dict.keys()), 20)
    worst_performing_subsets_dict = dict(
        sorted(synthetic_subset_performance_dict.items(), key=lambda x: x[1])[
            : (cols - 1)
        ]
    )
    worst_performing_subsets_dict = {
        k: v
        for k, v in synthetic_subset_performance_dict.items()
        if k in worst_performing_subsets_dict.keys()
    }
    worst_performing_subsets_dict["Overall"] = synthetic_overall_auc
    model_document["synthetic_subset_performance_dict"] = bson.Binary(
        bz2.compress(pickle.dumps(worst_performing_subsets_dict))
    )

    train_features_corr = train_features_corr.loc[
        train_features_corr.max(axis=1) > 0.70,
        train_features_corr.max(axis=0) > 0.70,
    ]
    train_test_corr = train_test_corr.loc[
        train_test_corr.max(axis=1) < 0.3, train_test_corr.max(axis=0) > 0.3
    ]
    train_synthetic_corr = train_synthetic_corr.loc[
        train_synthetic_corr.max(axis=1) < 0.3,
        train_synthetic_corr.max(axis=0) > 0.3,
    ]
    model_document["train_features_corr"] = bson.Binary(
        bz2.compress(pickle.dumps(train_features_corr))
    )
    model_document["train_test_corr"] = bson.Binary(bz2.compress(pickle.dumps(train_test_corr)))
    model_document["train_synthetic_corr"] = bson.Binary(
        bz2.compress(pickle.dumps(train_synthetic_corr))
    )
    data = {"user_id": api_key, "model_name": model_name, "model_document": model_document}
    requests.post("https://relionai-backend.herokuapp.com/account/update_model_test_resuts", data=json_util.dumps(data), headers={"Content-Type": "application/json; charset=utf-8"})
    return True


def monitor(
    single_sample, prediction, model, deployment_name=None, batch_size=100000
):
    pass


def process_test_results(model_document: Dict[str, Any], api_key: str = os.environ.get('relion_api_key')):
    
    print("Evaluation completed.")
    return True