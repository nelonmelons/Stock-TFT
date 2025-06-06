# ---------------------------------------------------#
#
#   File       : Data-Preprocessing.py
#   Author     : Soham Deshpande
#   Date       : May 2021
#   Description: Handle CSV files
#                Normalise the dataset so that all
#                values lie in between 0 and 1
#

# ----------------------------------------------------#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class CSVHandler:
    """
    Split and extract columns
    Provide information about the data

    """
    def __init__(self, filename, header):
        self.data = pd.read_csv(filename, header=header)

    # @property
    def read(self):
        return self.data

    @property
    def datatype(self):
        return type(self.data)

    @property
    def datahead(self):
        return self.data.head()

    def extractcolumns(self, column):
        return self.data[column].tolist()


def splitcolumns(filename, headers, columns):
    rawdata = CSVHandler(filename, headers)
    datalist = []
    print(len(columns))
    for i in columns:
        columni = rawdata.extractcolumns(str(i))
        datalist.append(columni)
    return datalist


class Normalise:
    """
    Normalise all the data between 0 and 1
    Incorporate batch normalisation
   """
    def __init__(self):
        super().__init__()

    def normalise(self, rdatasplit):
        self.data = rdatasplit
        self.norm = np.linalg.norm(rdatasplit)
        self.normalised = rdatasplit / self.norm
        return self.normalised#.tolist()

    def batchnormforward(self, gamma, beta, eps=1e-5):
        N, D = self.shape

        sample_mean = self.mean(axis=0)
        sample_var = self.var(axis=0)

        std = np.sqrt(sample_var + eps)
        x_centered = self - sample_mean
        x_norm = x_centered / std
        out = gamma * x_norm + beta

        cache = (x_norm, x_centered, std, gamma)

        return out, cache

        return self.normalised.tolist()



def normalisedata(columnnames):
    rdata = splitcolumns(
            '/home/soham/Documents/PycharmProjects/NEA/Data/Testing-Data.csv',
            0, columnnames)
    normal = Normalise()  # rawdata
    ndata = normal.normalise(rdata)  # normalised data
    return ndata


def data_preprocess_complete():
    ColumnNames = ['Open','High', 'Low', 'Close', 'Volume']
    test = normalisedata(ColumnNames)
    #print(ColumnNames)
    #print(test)
    df = pd.DataFrame(test, ColumnNames)
    #print(df)
    df = df.transpose()
    print(df.describe())
    df.plot(y='Open', kind='line')
    plt.show()
    return df
    #print(df)


data_preprocess_complete()



ColumnNames = ['Open', 'Open', 'High', 'Low', 'Close']
print(normalisedata(ColumnNames))

