from flask import Flask,render_template, request, jsonify
from flask_mysqldb import MySQL
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import json
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'aicovid'

mysql = MySQL(app)

app.run(debug = True)


@app.route("/")
def hello_world():

    #Creating a connection cursor
    # cursor = mysql.connection.cursor()
    #Executing SQL Statements
    # cursor.execute(''' INSERT INTO test VALUES(%s, %s) ''',(["","sudan"]))


    #Saving the Actions performed on the DB
    # mysql.connection.commit()

    #Closing the cursor
    # cursor.close()
    return "<p>Hello, World!</p>"

@app.route("/index", methods=['GET', 'POST'])
def index():
    df = pd.read_csv('covid.csv')
    df.head(2)
    X = df[['RRI','TR','SP','PC','AQP','IR','NI','FR','ND']]
    y = df[['MRT','PHW','PE','SB','MPM']]
    y.head(2)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred

    # data = request.get_json(silent=False)
    data = json.loads(request.data, strict=False)

    # paper input
    test_data = [[data['RRI'],data['TR'],data['SP'],data['PC'],data['AQP'],data['IR'],data['NI'],data['FR'],data['ND']]]
    test_data = np.array(test_data)
    res = model.predict(test_data)
    result = res[0].tolist()
    return jsonify({"result":result})

if __name__ == "__main__":
     app.run(debug=True ,port=8080,use_reloader=True)





