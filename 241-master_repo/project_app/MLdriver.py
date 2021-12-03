#import tensorflow as tf
import keras
from tensorflow.keras import layers
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
from upload import *
from download import *
#from prophet import Prophet
import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import math
import sys, getopt

global_bucket = 'coen241_core'
global_path = 'code/'

def download_files(parent_project_name):
    if download(global_path + parent_project_name + ".csv", parent_project_name + ".csv", global_bucket):
        pass
    else:
        return False
    if download(global_path + parent_project_name + "_config.json", parent_project_name + "_config.json", global_bucket):
        pass
    else:
        return False

    return True

def upload_files(parent_project_name):
    if upload(parent_project_name + ".png", parent_project_name + ".png", global_bucket):
        pass
    else:
        return False
    if upload(parent_project_name + ".h5", parent_project_name + ".h5", global_bucket):
        pass
    else:
        return False

    return True


def mapping(data,feature):
    featureMap=dict()
    count=0
    for i in sorted(data[feature].unique(),reverse=True):
        featureMap[i]=count
        count=count+1
    data[feature]=data[feature].map(featureMap)
    return data

def get_model_seq(arr):
    model=Sequential()
    for i in range(len(arr)):
        if i!=0 and i!=len(arr)-1:
            if i==1:
                model.add(Dense(arr[i],input_dim=arr[0],kernel_initializer='normal', activation='relu'))
            else:
                model.add(Dense(arr[i],activation='relu'))
    model.add(Dense(arr[-1],kernel_initializer='normal',activation="sigmoid"))
    model.compile(loss="binary_crossentropy",optimizer='rmsprop',metrics=['accuracy'])
    return model

def main(parent_project_name):
    parent_project_name = parent_project_name.strip()
    download_files(parent_project_name)
    config = open(parent_project_name + "_config.json",)
    data = json.load(config)

    df = pd.read_csv(parent_project_name + ".csv")
    if data["type"] == "seq":
        # run keras
        # create leyers
        df = df.drop(data["struct"]["drop cols"], axis = 1)

        for entry in data["struct"]["binary encode"]:
            df=mapping(df,feature=entry)

        model = Sequential()
        train, test = train_test_split(df, test_size =(data["struct"]["split"]/100))

        X=df.drop(["diagnosis"],axis=1)
        y=df["diagnosis"]

#divide dataset into training set, cross validation set, and test set
        trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.2, random_state=42)
        trainX, valX, trainY, valY = train_test_split(trainX, trainY, test_size=0.2, random_state=42)

        model = get_model_seq(data["struct"]["nodes"])

        model.compile(optimizer='adam', loss="binary_crossentropy", metrics=["accuracy"])

        h = model.fit(trainX, trainY, epochs = data["struct"]["epochs"], validation_data=(testX, testY))

        plt.plot(h.history['accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'accuracy'], loc='upper left')
        plt.savefig(parent_project_name + '.png')

        model.save(parent_project_name + '.h5')
        del model

        upload_files(parent_project_name)

        return True

    #elif data["type"] == "fbprofit":
        # run fbprofit
    else:
        print("unsupported type")
        return False
