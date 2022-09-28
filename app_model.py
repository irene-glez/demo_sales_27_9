from flask import Flask, request, jsonify
import os
import pickle
from sklearn.model_selection import cross_val_score
import pandas as pd
import sqlite3

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

# 1. endpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada (/predict):
@app.route('/predict', methods=['GET'])
def predict():
    model = pickle.load(open('advertising_model','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)
    prediction = model.predict([[tv,radio,newspaper]])
    return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

# ejemplo input: https://ireneglez.pythonanywhere.com/predict?tv=200&radio=33&newspaper=44


# # 2. endpoint para almacenar nuevos registros en la base de datos que deberá estar previamente creada. (/ingest_data)
@app.route('/ingest_data', methods=['GET'])
def retrain():
    connection = sqlite3.connect("my_database.db")
    crsr = connection.cursor()

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)
    sales = request.args.get('sales', None)

    insertion = "INSERT INTO advertising (TV, radio, newspaper, sales) VALUES ('tv' , 'radio' , 'newspaper' , 'sales')"
    crsr.execute(insertion)
    connection.commit()

    return print(crsr.rowcount, "record inserted.")

#     df = pd.read_csv('data/Advertising.csv', index_col=0)
#     X = df.drop(columns=['sales'])
#     y = df['sales']

#     model = pickle.load(open('data/advertising_model','rb'))
#     model.fit(X,y)
#     pickle.dump(model, open('data/advertising_model_v1','wb'))

#     scores = cross_val_score(model, X, y, cv=10, scoring='neg_mean_absolute_error')

#     return "New model retrained and saved as advertising_model_v1. The results of MAE with cross validation of 10 folds is: " + str(abs(round(scores.mean(),2)))


# app.run()