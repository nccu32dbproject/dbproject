from flask import Flask, jsonify, render_template, request, redirect, flash
import sqlite3

  
app = Flask(__name__)


@app.route('/')
def hello():    
    return "Hello World!"

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search_table')
def search_table():
    return render_template('search_table.html')

@app.route('/show_table',methods=['POST'])
def show_table():
    if request.method == 'POST':
        table_name = request.form.get('table_name')
        conn = sqlite3.connect('./data.sqlite')
        cursor = conn.cursor()
        #insecure
        #result = cursor.execute('SELECT * FROM %s' % (table_name,))
        sql_result = cursor.execute( 'SELECT * FROM {}'.format(table_name))
        final_result = sql_result.fetchall()
        cursor.close()
        conn.close()
        return jsonify(final_result)
    
@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/modify', methods=['POST'])
def modify():
    if request.method == 'POST':
        table_name = request.form.get('table_name')
        operation = request.form.get('operation')
        conn = sqlite3.connect('./data.sqlite')
        cursor = conn.cursor()
        if operation == 'INSERT':
            if table_name == 'Project':
                PNAME = request.form.get('pro_PNAME')
                PNUMBER = request.form.get('pro_PNUMBER')
                PLOCATION = request.form.get('pro_PLOCATION')
                DNUM = request.form.get('pro_DNUM')
                #insecure
                #sql = cursor.execute('INSERT INTO WORKS_ON (PNAME, PNNUMBER, PLOCATION, DNUM) VALUES (%s, %s, %s);' % (PNAME, PNUMBER, PLOCATION, DNUM))
                sql = 'INSERT INTO Project (PANME, PNUMBER, PLOCATION, DNUM) VALUES (?, ?, ?, ?);'
                cursor.execute(sql, (PNAME, PNUMBER, PLOCATION, DNUM))
            elif table_name == 'WORKS_ON':
                ESSN = request.form.get('work_ESSN')
                PNO = request.form.get('work_PNO')
                HOURS = request.form.get('work_HOURS')
                sql = 'INSERT INTO WORKS_ON (ESSN, PNO, HOURS) VALUES (?, ?, ?);'
                cursor.execute(sql, (ESSN, PNO, HOURS,))
        elif operation == 'DELETE':
            if table_name == 'Project':
                PNAME = request.form.get('pro_PNAME')
                PNUMBER = request.form.get('pro_PNUMBER')
                PLOCATION = request.form.get('pro_PLOCATION')
                DNUM = request.form.get('pro_DNUM')                
                sql = 'DELETE FROM Project WHERE PANME=? and PNUMBER=? and PLOCATION=? and DNUM=?;'
                cursor.execute(sql, (PNAME, PNUMBER, PLOCATION, DNUM))
            elif table_name == 'WORKS_ON':
                ESSN = request.form.get('work_ESSN')
                PNO = request.form.get('work_PNO')
                HOURS = request.form.get('work_HOURS')
                sql = 'DELETE FROM WORKS_ON WHERE ESSN=? and PNO=? and HOURS=?;'
                cursor.execute(sql, (ESSN, PNO, HOURS,))
        cursor.close()
        conn.commit()
        conn.close()
    return redirect('/data')
    

@app.route('/data_update')
def data_update():
    return render_template('data_update.html')

@app.route('/update', methods=['POST'])
def update():
    
    if request.method == 'POST':
        table_name = request.form.get('table_name')
        operation = request.form.get('operation')
        conn = sqlite3.connect('./data.sqlite')
        cursor = conn.cursor()
        
        if table_name == 'Project':
            PNAME = request.form.get('pro_PNAME')
            PNUMBER = request.form.get('pro_PNUMBER')
            PLOCATION = request.form.get('pro_PLOCATION')
            DNUM = request.form.get('pro_DNUM')
            rowid = request.form.get('pro_rowid')
            sql = 'UPDATE Project SET PANME = ?, PNUMBER = ?, PLOCATION = ?, DNUM = ? WHERE rowid = ?'
            cursor.execute(sql, (PNAME, PNUMBER, PLOCATION, DNUM, rowid,))
            
        elif table_name == 'WORKS_ON':
            ESSN = request.form.get('work_ESSN')
            PNO = request.form.get('work_PNO')
            HOURS = request.form.get('work_HOURS')
            rowid = request.form.get('work_rowid')
            sql = 'UPDATE WORKS_ON SET ESSN = ?, PNO = ?, HOURS = ? WHERE rowid = ?'
            cursor.execute(sql, (ESSN, PNO, HOURS, rowid,))
    cursor.close()
    conn.commit()
    conn.close()    
    return redirect('/data_update')

if __name__=='__main__':
    app.run(debug=True)
