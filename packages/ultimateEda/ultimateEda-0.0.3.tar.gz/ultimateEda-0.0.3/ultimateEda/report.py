
from statistics import *
from unittest import result
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
class eda:
    def __init__(self):
        self.self=self
    def EDA(df):
        """
        This function is used to do EDA on the dataframe.
        Here Df is the dataframe
        """
        col_min,IQR,col_max,percentile_5th,percentile_95th,Q1,Q2,range_=[],[],[],[],[],[],[],[]
        median_,mean_,std_,skew_,kurtosis_=[],[],[],[],[]
        Coefficient_of_variation,Median_Absolute_Deviation,Variance,uniq=[],[],[],[]
        uniq_value_,miss=[],[]
        
        for i in df.columns:
            sns.set_style('whitegrid')
            sns.set_context('poster')
            plt.style.use('ggplot')
            plt.rcParams['figure.figsize']=(8,6)
            plt.rcParams['font.size']=12
            plt.rcParams['font.family']='serif'
            uniq.append(len(df[i].unique()))
            uniq_value_.append(len(df[i].unique())/len(df[i]))
            miss.append(df[i].isnull().sum())
            if df[i].dtype!='object':
                col_m=df[i].min()
                col_min.append(col_m)
                print("minimun value of {} is {}".format(i,col_m))
                col_mx=df[i].max()
                col_max.append(col_mx)
                print("maximum value of {} is {}".format(i,col_mx))
                col_q1=df[i].quantile(0.25)
                Q1.append(col_q1)
                print("Q1 of {} is {}".format(i,col_q1))
                col_q2=df[i].quantile(0.75)
                Q2.append(col_q2)
                print("Q2 of {} is {}".format(i,col_q2))
                _5th=df[i].quantile(0.05)
                percentile_5th.append(_5th)
                print("5th percentile of {} is {}".format(i,_5th))
                _95th=df[i].quantile(0.95)
                percentile_95th.append(_95th)
                print("95th percentile of {} is {}".format(i,_95th))
                iqqr=col_q2-col_q1
                IQR.append(iqqr)
                print("IQR of {} is {}".format(i,iqqr))
                rng=col_mx-col_m
                range_.append(rng)
                print("range of {} is {}".format(i,rng))
                ######
                median_.append(df[i].median())
                print("median of {} is {}".format(i,df[i].median()))
                mean_.append(df[i].mean())
                print("mean of {} is {}".format(i,df[i].mean()))
                std_.append(df[i].std())
                print("standard deviation of {} is {}".format(i,df[i].std()))
                skew_.append(df[i].skew())
                print("skewness of {} is {}".format(i,df[i].skew()))
                kurtosis_.append(df[i].kurtosis())
                print("kurtosis of {} is {}".format(i,df[i].kurtosis()))
                cv=df[i].std()/df[i].mean()
                Coefficient_of_variation.append(cv)
                print("Coefficient of variation of {} is {}".format(i,cv))
                mad=df[i].mad()
                Median_Absolute_Deviation.append(mad)
                print("Median Absolute Deviation of {} is {}".format(i,mad))
                var=df[i].var()
                Variance.append(var)
                print("Variance of {} is {}".format(i,var))

                print("\n")
                print("Plot of → {}".format(i))
                sns.histplot(df[i],bins=20,label=i)
                plt.legend()
                plt.show()
            elif df[i].dtype=='object':
                sns.set_style('whitegrid')
                sns.set_context('talk')
                plt.rcParams['figure.figsize']=(8,6)
                plt.rcParams['font.size']=12
                plt.rcParams['font.family']='serif'
                val=df[i].value_counts()
                print("value count of {} is {}".format(i,val))
                col_min.append(np.nan)
                col_max.append(np.nan)
                Q1.append(np.nan)
                Q2.append(np.nan)
                percentile_5th.append(np.nan)
                percentile_95th.append(np.nan)
                IQR.append(np.nan)
                median_.append(np.nan)
                mean_.append(np.nan)
                std_.append(np.nan)
                skew_.append(np.nan)
                kurtosis_.append(np.nan)
                range_.append(np.nan)
                Coefficient_of_variation.append(np.nan)
                Median_Absolute_Deviation.append(np.nan)
                Variance.append(np.nan)
                print("\n")
                print("Plot of → {}".format(i))
                val=df[i].value_counts()
                val_normalize=df[i].value_counts(normalize=True)
                sns.set_style("whitegrid")
                plt.figure(figsize=[12,4])
                sns.countplot(x=df[i],data=df)
                vv=list(val)
                if len(vv)<5:
                    plt.plot(val,color='red',label=val)
                    plt.xlabel(i,)
                    plt.xticks(rotation=75)
                    plt.legend()
                    plt.show()
                else:
                    plt.plot(val,color='red')
                    plt.xlabel(i,)
                    plt.xticks(rotation=75)
                    plt.legend()
                    plt.show()
                print("Result end  for → ",i)
                print("____________________________________________________________________________________________")
                print("\n")
        result=pd.DataFrame({'column':df.columns,'uniq':uniq,'uniq_value_%':uniq_value_,
        'miss':miss,'min':col_min,'max':col_max,'Q1':Q1,'Q2':Q2,'5th':percentile_5th,
        '95th':percentile_95th,'IQR':IQR,'range':range_,'median':median_,'mean':mean_,
        'Standard deviation':std_,'skew':skew_,'kurtosis':kurtosis_,
        'Coefficient_of_variation':Coefficient_of_variation,
        'Median_Absolute_Deviation':Median_Absolute_Deviation,'Variance':Variance})
        return result
        



            

