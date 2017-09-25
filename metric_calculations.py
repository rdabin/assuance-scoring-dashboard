# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:30:14 2017
metric_calculations
A module for functions that will calculate useful metrics (e.g. false positive
and true positive rates)
@author: Tom Wakeford
"""
import pandas as pd

# Calculates the true positive rate and false positive rate
# for each unique score in the input dataframe
# df: a dataframe with columns 'class' and 'score'
# returns roc_df, a dataframe with columns 'threshold', 'TPR', 'FPR'
def build_roc_data(df):
    roc_list = []
    # Use the unique list of scores as a set of thresholds
    threshold_set = set(df['score'])
    # Make sure that we include 0 and 1
    threshold_set.update([0, 1])
    for threshold in threshold_set:
        TP, FP, TN, FN = confusion_matrix(df, threshold)
        TPR = TP / (TP + FN)
        FPR = FP / (FP + TN)
        roc_list.append([threshold, TPR, FPR])
        roc_df = pd.DataFrame(roc_list, columns=['threshold', 'TPR', 'FPR'])
    return roc_df

# Calculates the elements of the confusion matrix
# df: a dataframe with columns 'class' and 'score'
# 'class' is 0/1 for the negative/positive class respectively
# threshold: scores below the threshold are negative, above or equal to the threshold are positive
# returns a tuple of counts: true positive, false positive, true negative, false negative
def confusion_matrix(df, threshold):
    # A slice containing records scored as positive (i.e. above the threshold)
    positive_df = df[df['score']>=threshold]
    # A slice containing records scored as negative (i.e. below the threshold)    
    negative_df = df[df['score']<threshold]
    
    # True positives have been scored positive and really are positive
    TP_count = positive_df[positive_df['class']==1].shape[0]
    # False positive have been scored positive but aren't really 
    FP_count = positive_df[positive_df['class']==0].shape[0]
    # True negatives have been scored negative and reallyl are negative
    TN_count = negative_df[negative_df['class']==0].shape[0]
    # False negatives have been scored negative but aren't really
    FN_count = negative_df[negative_df['class']==1].shape[0]
    
    return TP_count, FP_count, TN_count, FN_count
    
