#!/usr/bin/python3.5
"""linear regression"""

import pandas as pd
import quandl as quandl
import math
import numpy as np
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression as lr

import matplotlib.pyplot as plt
from matplotlib import style
import datetime

class linearRegression:
            
    def runLinearReg(self, classifier):    
        df = quandl.get("WIKI/GOOGL")
        df = df[['Adj. Open',  'Adj. High',  'Adj. Low',  'Adj. Close', 'Adj. Volume']]
        
        df['HL_PCT']=((df['Adj. High']-df['Adj. Low'])/df['Adj. Low'])*100
        df['OC_PCT']=((df['Adj. Close']-df['Adj. Open'])/df['Adj. Open'])*100
        
        df = df[['Adj. Close','HL_PCT','OC_PCT', 'Adj. Volume']]
        
        #fill NaNs with some outliers like 99999 here
        forecast_col = 'Adj. Close'
        df.fillna(value=-99999, inplace=True)
        
        #forecast_out is the length of forecast data points
        forecast_out = int(math.ceil(0.01 * len(df)))
        
        df.dropna(inplace=True)

        #label is the column to predict
        df['label'] = df[forecast_col].shift(-forecast_out)
 
        # X is conventionally features
        X = np.array(df.drop(['label'], 1))
        
        # features are usually kept between -1 to 1. speed up processing and accuracy
        X = preprocessing.scale(X)
        X_lately = X[-forecast_out:]
        X = X[:-forecast_out]        
        
        # y is conventionally label
        y = np.array(df['label'])
        y = y[:-forecast_out] 
        #split the data into train and test
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
        
        #define your classifier
        if(classifier == 'SVR'):
            clf = svm.SVR(kernel='linear')
        elif(classifier == 'linearRegression'):
            clf = lr()
            
        clf.fit(X, y)
        
        #how well did classifier do against test features and labels
        print(clf.score(X_test, y_test))
        
        #predict
        X_forecast = clf.predict(X_lately)
        df['Forecast']=np.nan
        ## plotting
        
        # get last date in df
        last_date = df.iloc[-1].name
        last_ts = last_date.timestamp()
        one_day_ts = 86400
        next_ts = last_ts + one_day_ts
        
        #plot predicted values incrementing each day
        for i in X_forecast:
            next_date = datetime.datetime.fromtimestamp(next_ts)
            next_ts += one_day_ts
            df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]
        
        df['Adj. Close'].plot()
        df['Forecast'].plot()
        plt.legend(loc=4)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()
        
        