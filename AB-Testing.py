
#####################################################
# Business Problem
#####################################################

"""

Facebook recently introduced a new bidding type, "average bidding", as an alternative to the existing bidding type called "maximumbidding".
Our customers decided to test this new feature and want to do an A/B test to see if averagebidding converts more than maximumbidding.
A/B testing has been going on for 1 month and customers now ask you to analyze the results of this A/B test. waiting. The ultimate success criterion is Purchase.
Therefore, the focus should be on the Purchase metric for statistical testing.

"""

# Features:

"""

# impression: Ad views count
# Click: Number of clicks on the displayed ad
# Purchase: The number of products purchased after the ads clicked
# Earning: Earnings after purchased products

"""

############################################
# Importing Library and Functions
############################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal

pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: "%.4f" % x)


dataframe_control = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
dataframe_test = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

# Check DataFrame - Function

def check_df(dataframe,head =5):
    print("############################### Shape ###############################")
    print(dataframe.shape)
    print("############################### Types ###############################")
    print(dataframe.dtypes)
    print("############################### Head ###############################")
    print(dataframe.head(head))
    print("############################### Tail ###############################")
    print(dataframe.tail(head))
    print("############################### NA ###############################")
    print(dataframe.isnull().sum())
    print("############################### Quantiles ###############################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)


#  Combine the control and test group data

df_control["Group"] = "control"
df_test["Group"] = "test"
df = pd.concat([df_control, df_test], axis=0, ignore_index=False)

df.head()

#####################################################
# A/B Testinin Hipotezinin Tanımlanması
#####################################################


# Define the hypothesis.

# Problem: The company wants to find out if the new feature, averageidding,  converts more than maximumbidding.

# Hypothesis:

# H0: M1 = M2 (There is no difference between the purchasing averages of the control group and the test group.)
# H1: M1 != M2 (There is a difference between the purchasing averages of the control group and the test group.)


# Analyze the purchase (gain) averages for the control and test group

print("Control group mean: %.4f" %df_control["Purchase"].mean())
print("Test group mean: %.4f" %df_test["Purchase"].mean())


#####################################################
# Performing Hypothesis Testing
#####################################################

# Check the assumptions before testing the hypothesis. These are Assumption of Normality and Homogeneity of Variance.
# Test separately whether the control and test groups comply with the assumption of normality over the Purchase variable.


############################
# Normallik Varsayımı
############################

# H0: Normal distribution assumption is provided.
# H1: Assumption of normal distribution not provided
# p < 0.05 H0 REJECTED
# p > 0.05 H0 CANNOT BE REJECTED
# Is the assumption of normality provided for the control and test groups according to the test result?

test_stat, pvalue = shapiro(df.loc[df["Group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value = 0.5891
# HO cannot be denied. It provides the assumption of normal distribution.

############################
# Variance Homogeneity Assumption
############################

# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.
# p < 0.05 H0 REJECTED
# p > 0.05 H0 CANNOT BE REJECTED
# Test whether the homogeneity of variance is provided for the control and test groups over the Purchase variable.


test_stat, pvalue = levene(df.loc[df["Group"] == "control", "Purchase"],
                           df.loc[df["Group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# # p-value=0.1083
# HO cannot be denied. The values of the Control and Test groups provide the assumption of variance homogeneity.
# Variances are Homogeneous.

# Since the assumptions are provided, an independent two-sample t-test (parametric test) is performed.

test_stat, pvalue = ttest_ind(df.loc[df["Group"] == "control", "Purchase"],
                              df.loc[df["Group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Considering the p-value obtained as a result of the test, interpret whether there is a statistically significant difference between the purchasing averages of the control and test groups.
# p-value=0.3493
# HO cannot be denied. There is no statistically significant difference between the control and test group purchasing averages.

