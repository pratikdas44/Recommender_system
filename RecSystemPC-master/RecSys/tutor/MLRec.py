import pandas as pd
import _sqlite3 as sq3
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
import os
import tutor.Recommenders as Recommenders
# import Evaluation as Evaluation

def renamer(data):
    for s in data:
        sorg = s
        s = s.upper()
        s = s.strip()
        if (s.find(' ') > 0):
            s = s.replace(" ", '_', 2)
            if (s.find(' ') > 0):
                s = s[:(s.find(' '))]
        if (s.find('/') > 0):
            s = s[:(s.find('/'))]
        data.rename(columns={sorg: s}, inplace=True)


def like_dislike(data):
    dataDict = list(data.T.to_dict().values())
    newDataDict = []
    for row in dataDict:
        count = 0
        if type(row["TEACHERS_YOU_LIKED"]) == str:
            for tl in row["TEACHERS_YOU_LIKED"].split(","):
                row2 = row.copy()
                row2["TEACHER_NAME"] = tl.strip()
                row2["LIKE"] = 1
                #             print(row2)
                count = count + 1
                newDataDict.append(row2)
        if type(row["TEACHERS_YOU_DISLIKED"]) == str:
            for tl in row["TEACHERS_YOU_DISLIKED"].split(","):
                row2 = row.copy()
                row2["TEACHER_NAME"] = tl.strip()
                row2["LIKE"] = -1
                count = count + 1
                newDataDict.append(row2)
        if count == 0:
            row2 = row.copy()
            row2["TEACHER_NAME"] = ""
            row2["LIKE"] = 0
            newDataDict.append(row2)
    data2 = pd.DataFrame(newDataDict)
    del data2["TEACHERS_YOU_LIKED"]
    del data2["TEACHERS_YOU_DISLIKED"]
    return data2


data = None

def convertData(data):
    list = []
    fn = "../db.sqlite3"
    fn = os.path.join(os.path.abspath(os.path.dirname(__file__)), fn)
    con = sq3.connect(fn)
    for i, row in data.iterrows():
        cur = con.cursor()
        cur.execute("SELECT teacher_name FROM tutor_teacher where id = %s" % row["TEACHER_NAME"])
        dbrows = cur.fetchall()
        row["DISPLAY_NAME"] = dbrows[0][0]
        # dbrows[0]["TEACHER_NAME"]
        list.append(row)
    return list

def training():
    global data

    # ##csv code
    # fn = "./teach_rec.csv"
    # fn = os.path.join(os.path.abspath(os.path.dirname(__file__)), fn)
    # data = pd.read_csv(fn)
    # # labEnc = LabelEncoder()
    # renamer(data)
    # if "ID" in data:
    #     del data["ID"]
    # data["STUDENT_ID"] = data.index.values
    # del data["TIMESTAMP"]
    # #  del data["STUDENT_NAME"]
    # # del data["TEACHER_YOU_WANT"]
    # del data["COLLEGE_NAME"]  # may be usefull later todo
    # del data["MEDIUM"]  # may be usefull later todo
    # data = like_dislike(data)

    #db code
    fn = "../db.sqlite3"
    fn = os.path.join(os.path.abspath(os.path.dirname(__file__)), fn)
    con = sq3.connect(fn)
    data = pd.read_sql_query("select tf.*, tul.teacher_id as TEACHER_NAME, tt.TEACHER_NAME as DISPLAY_NAME, 1 as `LIKE` from tutor_teacherfeedback as tf INNER JOIN tutor_teacherfeedback_TEACHERS_YOU_LIKED tul on tf.id = tul.teacherfeedback_id INNER JOIN tutor_teacher tt on tul.teacher_id = tt.id union select tf.*, tul.teacher_id as TEACHER_NAME, tt.TEACHER_NAME as DISPLAY_NAME, -1 as `LIKE` from tutor_teacherfeedback as tf INNER JOIN tutor_teacherfeedback_TEACHERS_YOU_DISLIKED tul on tf.id = tul.teacherfeedback_id  INNER JOIN tutor_teacher tt on tul.teacher_id = tt.id", con)
    data["STUDENT_ID"] = data["id"]
    if "id" in data:
        del data["id"]
    del data["TIMESTAMP"]
    del data["COLLEGE_NAME"]  # may be usefull later todo
    del data["MEDIUM"]  # may be usefull later todo
    # data = like_dislike(data)


def popularity_based_sug():
    pm = Recommenders.popularity_recommender_py()
    pm.create(globals()["data"], 'LIKE', 'TEACHER_NAME')
    rec = pm.recommend(0)
    # for e in rec:
    #     print(e)
    return convertData(rec)

def getRecByItemSim(user_id):
    global data
    is_model = Recommenders.item_similarity_recommender_py()
    is_model.create(data[data['LIKE'] == 1], 'STUDENT_ID', 'TEACHER_NAME')
    user_items = is_model.get_user_items(user_id)
    print("------------------------------------------------------------------------------------")
    print("Training data songs for the user userid: %s:" % user_id)
    print("------------------------------------------------------------------------------------")
    for user_item in user_items:
        print(user_item)
    print("----------------------------------------------------------------------")
    print("Recommendation process going on:")
    print("----------------------------------------------------------------------")
    # Recommend songs for the user using personalized model
    recm1 = is_model.recommend(user_id)

    is_model2 = Recommenders.item_similarity_recommender_py()
    is_model2.create(data[data['LIKE'] == -1], 'STUDENT_ID', 'TEACHER_NAME')
    user_items = is_model2.get_user_items(user_id)
    print("------------------------------------------------------------------------------------")
    print("Neg:: Training data songs for the user userid: %s:" % user_id)
    print("------------------------------------------------------------------------------------")
    for user_item in user_items:
        print(user_item)
    print("----------------------------------------------------------------------")
    print("Neg:: Recommendation process going on:")
    print("----------------------------------------------------------------------")
    # Recommend songs for the user using personalized model
    recm2 = is_model2.recommend(user_id)
    disLikedSet = data[data['STUDENT_ID'] == user_id]
    disLikedSet = data[data['LIKE'] == -1]
    disLikedSet = set(disLikedSet["TEACHER_NAME"])
    recmDisLike = {}
    if type(recm2) != int:
        recmDisLike = set(recm2["item"])
    if type(recm1) != int:
        for e in recmDisLike:
            recm1 = recm1[recm1["item"] != e]
        for e in disLikedSet:
            recm1 = recm1[recm1["item"] != e]
    print("$"*100)
    # print(recm1.head(5))
    recm1.rename(columns={"item":"TEACHER_NAME"}, inplace=True)
    return convertData(recm1)
# getRecByItemSim(data, 16)

def get_similar(item_id):
    global data
    item_model = Recommenders.item_similarity_recommender_py()
    item_model.create(data[data['LIKE'] == 1], 'STUDENT_ID', 'TEACHER_NAME')
    list1 = item_model.get_similar_items([item_id])
    item_model2 = Recommenders.item_similarity_recommender_py()
    item_model2.create(data[data['LIKE'] == -1], 'STUDENT_ID', 'TEACHER_NAME')
    list2 = item_model2.get_similar_items([item_id])
    finalList = pd.concat([list1, list2])

    finalList = finalList.groupby(['item']).agg({'score': 'sum'}).reset_index()
    finalList = finalList.sort_values(['score'], ascending=[0])
    if len(finalList) > 4:
        finalList = finalList[:4]
    finalList.rename(columns={"item":"TEACHER_NAME"}, inplace=True)
    finalList = convertData(finalList)
    return finalList

def get_rec_by_similar_users(student_id):
    global  data
    teachers_grouped = Recommenders.get_rec_by_similar_users(data, "STUDENT_ID", student_id)
    teachers_grouped = convertData(teachers_grouped)
    return teachers_grouped

def getRecBySimUserItemSim(user_id):
    global data
    is_model = Recommenders.user_item_similarity_recommender_py()
    is_model.create(data[data['LIKE'].isin((1, 0))], 'STUDENT_ID', 'TEACHER_NAME')
    user_items = is_model.get_user_items(user_id )
    for user_item in user_items:
        print(user_item)
    #Recommend songs for the user using personalized model
    recm1 = is_model.recommend(user_id)
    is_model2 = Recommenders.user_item_similarity_recommender_py()
    is_model2.create(data[data['LIKE'].isin((-1,0))], 'STUDENT_ID', 'TEACHER_NAME')
    user_items = is_model2.get_user_items(user_id )
    for user_item in user_items:
        print(user_item)
    #Recommend songs for the user using personalized model
    recm2 = is_model2.recommend(user_id)
    disLikedSet = data[data['STUDENT_ID'] == user_id]
    disLikedSet = disLikedSet[data['LIKE']==-1]
    disLikedSet = set(disLikedSet["TEACHER_NAME"])
    recmDisLike = set(recm2["item"])
    for e in recmDisLike:
        recm1 = recm1[recm1["item"] != e]
    for e in disLikedSet:
        recm1 = recm1[recm1["item"] != e]

    recm1.rename(columns={"item":"TEACHER_NAME"}, inplace=True)
    recm1 = convertData(recm1)
    return recm1
# getRecBySimUserItemSim(data, 16)


# if __name__ == "__main__":
training()
# getRecBySimUserItemSim(data, 16)


if __name__ == "__main__":
    data = popularity_based_sug()
