from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'webapp_db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'pitchersData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'MLB Pitcher Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPitchersImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, pitchers=result)


@app.route('/view/<int:pitcher_id>', methods=['GET'])
def record_view(pitcher_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPitchersImport WHERE id=%s', pitcher_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', pitcher=result[0])


@app.route('/edit/<int:pitcher_id>', methods=['GET'])
def form_edit_get(pitcher_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPitchersImport WHERE id=%s', pitcher_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', pitcher=result[0])


@app.route('/edit/<int:pitcher_id>', methods=['POST'])
def form_update_post(pitcher_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Team'), request.form.get('Position'),
                 request.form.get('Height_in'), request.form.get('Weight_lb'), request.form.get('Age'), pitcher_id)
    sql_update_query = """UPDATE tblPitchersImport t SET t.Name = %s, t.Team = %s, t.Position = %s, t.Height_in = 
    %s, t.Weight_lb = %s, t.Age = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/pitchers/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Pitcher Form')


@app.route('/pitchers/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Team'), request.form.get('Position'),
                 request.form.get('Height_in'), request.form.get('Weight_lb'),
                 request.form.get('Age'))
    sql_insert_query = """INSERT INTO tblPitchersImport (Name,Team,Position,Height_in,Weight_lb,Age) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:pitcher_id>', methods=['POST'])
def form_delete_post(pitcher_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblPitchersImport WHERE id = %s """
    cursor.execute(sql_delete_query, pitcher_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/pitchers', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPitchersImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/pitchers/<int:pitcher_id>', methods=['GET'])
def api_retrieve(pitcher_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPitchersImport WHERE id=%s', pitcher_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/pitchers/<int:pitcher_id>', methods=['PUT'])
def api_edit(pitcher_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Name'], content['Team'], content['Position'], content['Height_in'], content['Weight_lb'], content['Age'],pitcher_id)
    sql_update_query = """UPDATE tblPitchersImport t SET t.Name = %s, t.Team = %s, t.Position = %s, t.Height_in = 
        %s, t.Weight_lb = %s, t.Age = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/pitchers', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Name'], content['Team'], content['Position'],
                 content['Height_in'], content['Weight_lb'],
                 content('Age'))
    sql_insert_query = """INSERT INTO tblPitchersImport (Name,Team,Position,Height_in,Weight_lb,Age) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/pitchers/<int:pitcher_id>', methods=['DELETE'])
def api_delete(pitcher_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblPitchersImport WHERE id = %s """
    cursor.execute(sql_delete_query, pitcher_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
