import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.preprocessing import LabelEncoder, Imputer, OneHotEncoder
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
import pickle
import  os


def renamer(data):
    for s in data:
        sorg = s
        s = s.upper()
        s = s.strip()
        if(s.find(' ')>0):
            s = s.replace(" ", '_', 1)
            if(s.find(' ')>0):
                s = s[:(s.find(' '))]
        if(s.find('/')>0):
                s = s[:(s.find('/'))]
        data.rename(columns = {sorg:s}, inplace = True)

def dictLabelAll(df, d2):
    for cn in d2:
        dtmp = {}
        i = 0
        for e in d2[cn]:
            dtmp[e] = i
            i = i + 1
        dictLabel(df, dtmp, cn)

def dictLabel(df, d1, cn):
    df[cn] = df[cn].map(d1)


def training():
    data = pd.read_csv("edu_sur.csv")
    # labEnc = LabelEncoder()
    renamer(data)
    data['DUE_DATE'] = pd.to_datetime(data['DUE_DATE'], errors = 'coerce')
    data.dropna(subset=['AS_PER'], inplace =True)
    # if "id" in data:
    #     del data["id"]
    del data["TIMESTAMP"]
    del data["STUDENT_NAME"]
    del data["SUBJECT_NAME"]  # todo dont delete once we have lots of data for each sub
    del data["EDUCATION_TYPE"]  # todo dont delete once we have lots of data for each type
    del data["SEMESTER"]  # todo dont delete once we have lots of data for each sem
    del data["DUE_DATE"]  # todo dont delete once we have lots of data for each sem
    # start deletion
    allClms = data.columns
    lof = LocalOutlierFactor(n_neighbors=5, contamination=0.1055)
    print(data.shape)
    X2 = pd.DataFrame([])
    X2["AVERAGE_READING"] = data["AVERAGE_READING"]
    X2["NUMBER_OF"] = data["NUMBER_OF"]
    X2["AS_PER"] = data["AS_PER"]
    outlier = lof.fit_predict(X2)
    data['tmp'] = outlier
    print(outlier)
    data = data[outlier != -1]
    del data['tmp']
    data[data["AVERAGE_READING"] <= 0] = data["AVERAGE_READING"].mean()
    data[data["NUMBER_OF"] < 0] = data["NUMBER_OF"].mean()
    data[data["AS_PER"] < 0] = data["AS_PER"].mean()
    # end deletion

    # start split
    X = data.iloc[:, :-1]
    Y = data.iloc[:, -1]
    # end split

    # start encoding
    tmpDict = {'TOUGHNESS_LEVEL': ["Easy", "Medium", "Hard"],
               'SUBJECT_SYLLABUS': ["Short", "Medium (400+ pages)", "Lengthy (600+ pages)", "Very Lengthy (800+ pages)"],
               'INTEREST_LEVEL': ["Very Interesting", "Interesting", "Normal", "Boring"],
               'SUPPORTING_KNOWLEDGE': ["Expert", "Intermediate", "Beginner", "None"],
               'CHECKING_LEVEL': ["Lenient", "Normal", "Strict"]}
    dictLabelAll(X, tmpDict)
    columns = ['TYPE_OF', 'PREFERRED_READING']
    X = pd.get_dummies(X, columns=columns, prefix=columns)
    oneHotDict = {
        'TYPE_OF': (("Theoritical", "Theoritical"), ("Practical","Practical"), ("Numerical","Numerical") , ("Other","Other")),
        'PREFERRED_READING': (("Notes","Notes"), ("Book", "Book"), ("Video","Video"), ("Multiple","Multiple"))
    }
    for k in oneHotDict:
        listOp = oneHotDict[k]
        for e in listOp:
            clm = "%s_%s" % (k, e[0])
            if not clm in X:
                X[clm] = 0
    # end encoding


    allClms = X.columns
    # scaling
    sc = StandardScaler()

    sc.fit(X)
    pkl_filename2 = "pickle_scaler.pkl"
    with open(pkl_filename2, 'wb') as file:
        pickle.dump(sc, file)
    X = pd.DataFrame(sc.transform(X), columns=allClms)
    X.describe()
    # end scaling

    # start train test split
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)
    X_train.head(4)
    # end train test split

    reg = RandomForestRegressor(n_estimators=32)
    # reg.fit(X_train, y_train)
    reg.fit(X, Y)


    y_pred = reg.predict(X_test)
    ac = accuracy_score(np.round(y_test), np.round(y_pred))
    print(ac*100)
    print(y_pred)
    print("="*10)
    print(y_test)
    pkl_filename = "pickle_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(reg, file)


def pred(data2):
    # df = pd.DataFrame([[getattr(i, j) for j in variables] for i in arr], columns=variables)
    print("="*100)
    keys = list(data2.to_dict().keys())
    values = [list(data2.to_dict().values())]
    print(keys)
    print(values)
    data = pd.DataFrame(values, columns=keys)
    # end scaling
    print("="*100)
    print(data.shape)
    for e in data:
        print(data[e])

    pkl_filename = "./pickle_model.pkl"
    pkl_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), pkl_filename)
    with open(pkl_filename, 'rb') as file:
        reg = pickle.load(file)

    # if "id" in data:
    #     del data["id"]
    del data["TIMESTAMP"]
    del data["STUDENT_NAME"]
    del data["SUBJECT_NAME"]  # todo dont delete once we have lots of data for each sub
    del data["EDUCATION_TYPE"]  # todo dont delete once we have lots of data for each type
    del data["SEMESTER"]  # todo dont delete once we have lots of data for each sem
    del data["DUE_DATE"]  # todo dont delete once we have lots of data for each sem
    del data["AS_PER"]  # todo dont delete once we have lots of data for each sem
    # start encoding
    tmpDict = {'TOUGHNESS_LEVEL': ["Easy", "Medium", "Hard"],
               'SUBJECT_SYLLABUS': ["Short", "Medium (400+ pages)", "Lengthy (600+ pages)", "Very Lengthy (800+ pages)"],
               'INTEREST_LEVEL': ["Very Interesting", "Interesting", "Normal", "Boring"],
               'SUPPORTING_KNOWLEDGE': ["Expert", "Intermediate", "Beginner", "None"],
               'CHECKING_LEVEL': ["Lenient", "Normal", "Strict"]}
    X = data
    dictLabelAll(X, tmpDict)
    columns = ['TYPE_OF', 'PREFERRED_READING']
    X = pd.get_dummies(X, columns=columns, prefix=columns)
    oneHotDict = {
        'TYPE_OF': (("Theoritical", "Theoritical"), ("Practical","Practical"), ("Numerical","Numerical") , ("Other","Other")),
        'PREFERRED_READING': (("Notes","Notes"), ("Book", "Book"), ("Video","Video"), ("Multiple","Multiple"))
    }

    print("="*100)
    for k in oneHotDict:
        listOp = oneHotDict[k]
        for e in listOp:
            clm = "%s_%s" % (k, e[0])
            if not clm in X:
                X[clm] = 0
    # end encoding
    X["id"] = 0

    print("*"*100)
    print(X.shape)
    for e in X:
        print(X[e])


    allClms = X.columns
    print(allClms)

    # scaling

    pkl_filename2 = "./pickle_scaler.pkl"
    pkl_filename2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), pkl_filename2)
    with open(pkl_filename2, 'rb') as file:
        sc = pickle.load(file)
    X = pd.DataFrame(sc.transform(X), columns=allClms)
    X.describe()


    y = reg.predict(X)
    return y

if __name__ == "__main__":
    training()