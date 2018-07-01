from flask import Flask, jsonify, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello():
    return '<a href="/index">Hello World!</a>'

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
        areaName=request.form.get('AreaName')
        districtName=request.form.get('DistrictName')
        streetName=request.form.get('StreetName')
        dishName=request.form.get('DishName')
        styleName=request.form.get('StyleName')
        restaurantName=request.form.get('RestaurantName')
        rating=request.form.get('Rating')
        paymentName=request.form.get('PaymentName')

        conn = sqlite3.connect('./data.db')
        cursor = conn.cursor()
        #insecure
        # sql_result = cursor.execute('SELECT * FROM %s' % (table_name))
        # sql_result = cursor.execute( 'SELECT * FROM Address WHERE Area=\'{}\''.format(areaName))
        # sql_result = cursor.execute( 'SELECT * FROM Address WHERE District=\'{}\''.format(districtName))
        # sql_result = cursor.execute( 'SELECT * FROM Address WHERE Street LIKE \'%{}%\''.format(streetName))
        # sql_result = cursor.execute( 'SELECT * FROM Dish WHERE Name LIKE \'%{}%\''.format(dishName))
        # sql_result = cursor.execute( 'SELECT * FROM Style WHERE Style LIKE \'%{}%\''.format(styleName))
        # sql_result = cursor.execute( 'SELECT * FROM Restaurant WHERE Name LIKE \'%{}%\''.format(restaurantName))
        # sql_result = cursor.execute( 'SELECT * FROM Review WHERE Rating >= {}'.format(rating))
        # sql_result = cursor.execute( 'SELECT * FROM Payment WHERE Method=\'{}\''.format(paymentName))
        sql = 'SELECT Name,OT,Style.style,Area,District,Street,Rating FROM Restaurant INNER join Style ON Restaurant.Style = StyleID INNER join Address ON Restaurant.Name = Address.RestaurantName INNER join Review ON Restaurant.Name = Review.Restaurant '
        w=''
        if areaName : w+='Area=\'{}\' AND '.format(areaName)
        if districtName : w+='District=\'{}\' AND '.format(districtName)
        if streetName : w+='Street LIKE \'%{}%\' AND '.format(streetName)
        if styleName : w+='Style.Style LIKE \'%{}%\' AND '.format(styleName)
        if restaurantName : w+='Restaurant.Name LIKE \'%{}%\' AND '.format(restaurantName)
        if rating : w+='Rating >= {} AND '.format(rating)
        if w : w='WHERE '+w[:-4]
        sql+=w
        print(sql)
        sql_result = cursor.execute(sql)

        final_result = sql_result.fetchall()
        cursor.close()
        conn.close()
        # return jsonify(final_result)
        r=''
        for i in final_result:
            r+='<h1><a href=\"/showR/{}\">{}</a></h1>'.format(i[0],i[0])
            r+='<p>Rating: {}</p>'.format(i[6])
            r+='<p>Open: {}</p>'.format(i[1])
            r+='<p>Style: {}</p>'.format(i[2])
            r+='<p>Address: {}</p>'.format(' '.join(i[3:-1]))
            r+='<br>'

        if not r : r='No result.'
        return r
    # return '<p hidden id='result'>{}</p>'.format(final_result)
    # return '<script > var r=JSON.parse(\'{}\'); </script>'.format(final_result)

@app.route('/showR/<name>')
def profile(name):
    conn = sqlite3.connect('./data.db')
    cursor = conn.cursor()
    sql = 'SELECT Restaurant.Name,Dish.Name FROM Restaurant INNER join Style ON Restaurant.Style = Style.StyleID Left OUTER join Dish ON Dish.Style = Style.StyleID where Restaurant.Name = \'{}\' '.format(name)
    sql_result = cursor.execute(sql)

    final_result = sql_result.fetchall()
    cursor.close()
    conn.close()
    r='<h1>{}</h1>'.format(final_result[0][0])
    for i in final_result:
        r+='<p>Dish: {}</p>'.format(i[1])

    return r

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
            if table_name == 'Address':
                Area = request.form.get('add_Area')
                District = request.form.get('add_District')
                Street = request.form.get('add_Street')
                RestaurantName = request.form.get('add_Name')
                #insecure
                #sql = cursor.execute('INSERT INTO WORKS_ON (PNAME, PNNUMBER, PLOCATION, DNUM) VALUES (%s, %s, %s);' % (PNAME, PNUMBER, PLOCATION, DNUM))
                sql = 'INSERT INTO Address (Area, District, Street, RestaurantName) VALUES (?, ?, ?, ?);'
                cursor.execute(sql, (Area, District, Street, RestaurantName))
            elif table_name == 'Dish':
                Name = request.form.get('dish_Name')
                Style = request.form.get('dish_Style')
                sql = 'INSERT INTO Dish (Name, Style) VALUES (?, ?);'
                cursor.execute(sql, (Name, Style,))
            elif table_name == 'Restaurant':
                Name = request.form.get('rest_name')
                Phone = request.form.get('rest_phone')
                Style = request.form.get('rest_style')
                OT = request.form.get('rest_OT')
                Facebook = request.form.get('rest_fb')
                Payment = request.form.get('rest_payment')
                Line = request.form.get('rest_line')
                sql = 'INSERT INTO Restaurant (Name, Phone, Style, OT, Facebook, Payment, Line) VALUES (?, ?, ?, ?, ?, ?, ?, ?);'
                cursor.execute(sql, (Name, Phone, Style, OT, Facebook, Seat, Payment, Line))
            elif table_name == 'Review':
                Review = request.form.get('rev_review')
                Restaurant = request.form.get('rev_rest')
                Comment = request.form.get('rev_comment')
                Reply = request.form.get('rev_reply')
                Rating = request.form.get('rev_rating')
                sql = 'INSERT INTO Review (Review, Restaurant, Comment, Reply, Rating) VALUES (?, ?, ?, ?, ?);'
                cursor.execute(sql, (Review, Restaurant, Comment, Reply, Rating))

        elif operation == 'DELETE':
            if table_name == 'Address':
                Area = request.form.get('add_Area')
                District = request.form.get('add_District')
                Street = request.form.get('add_Street')
                RestaurantName = request.form.get('add_Name')
                sql = 'DELETE FROM Address WHERE Area=? and District=? and Street=? and RestaurantName=?;'
                cursor.execute(sql, (Area, District, Street, RestaurantName))
            elif table_name == 'Dish':
                Name = request.form.get('dish_Name')
                Style = request.form.get('dish_Style')
                sql = 'DELETE FROM Dish WHERE Name=? and Style=?;'
                cursor.execute(sql, (Name, Style,))
            elif table_name == 'Restaurant':
                Name = request.form.get('rest_name')
                Phone = request.form.get('rest_phone')
                Style = request.form.get('rest_style')
                OT = request.form.get('rest_OT')
                Facebook = request.form.get('rest_fb')
                Payment = request.form.get('rest_payment')
                Line = request.form.get('rest_line')
                sql = 'DELETE FROM Restaurant WHERE Name=? and Phone=? and Style=? and OT=? and Facebook=? and Payment=? and Line=?;'
                cursor.execute(sql, (Name, Phone, Style, OT, Facebook, Seat, Payment, Line))
            elif table_name == 'Review':
                Review = request.form.get('rev_review')
                Restaurant = request.form.get('rev_rest')
                Comment = request.form.get('rev_comment')
                Reply = request.form.get('rev_reply')
                Rating = request.form.get('rev_rating')
                sql = 'DELETE FROM Review WHERE Review=? and Restaurant=? and Comment=? and Reply=? and Rating=?;'
                cursor.execute(sql, (Review, Restaurant, Comment, Reply, Rating))

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
        conn = sqlite3.connect('./data.db')
        cursor = conn.cursor()

        if table_name == 'Address':
            Area = request.form.get('add_Area')
            District = request.form.get('add_District')
            Street = request.form.get('add_Street')
            RestaurantName = request.form.get('add_Name')
            sql = 'UPDATE Address SET Area=? and District=? and Street=? and RestaurantName=?;'
            cursor.execute(sql, (Area, District, Street, RestaurantName))
        elif table_name == 'Dish':
            Name = request.form.get('dish_Name')
            Style = request.form.get('dish_Style')
            sql = 'UPDATE Dish SET Name=? and Style=?;'
            cursor.execute(sql, (Name, Style,))
        elif table_name == 'Restaurant':
            Name = request.form.get('rest_name')
            Phone = request.form.get('rest_phone')
            Style = request.form.get('rest_style')
            OT = request.form.get('rest_OT')
            Facebook = request.form.get('rest_fb')
            Payment = request.form.get('rest_payment')
            Line = request.form.get('rest_line')
            sql = 'UPDATE Restaurant SET Name=? and Phone=? and Style=? and OT=? and Facebook=? and Payment=? and Line=?;'
            cursor.execute(sql, (Name, Phone, Style, OT, Facebook, Seat, Payment, Line))
        elif table_name == 'Review':
            Review = request.form.get('rev_review')
            Restaurant = request.form.get('rev_rest')
            Comment = request.form.get('rev_comment')
            Reply = request.form.get('rev_reply')
            Rating = request.form.get('rev_rating')
            sql = 'UPDATE Review SET Review=? and Restaurant=? and Comment=? and Reply=? and Rating=?;'
            cursor.execute(sql, (Review, Restaurant, Comment, Reply, Rating))

    cursor.close()
    conn.commit()
    conn.close()
    return redirect('/data_update')

if __name__=='__main__':
    app.run(debug=True)
    # conn = sqlite3.connect('./data.db')
    # cursor = conn.cursor()
    # sql = 'UPDATE Restaurant SET Payment = \'d\' WHERE Style <3;'
    # sql_result = cursor.execute(sql)
    # sql = 'UPDATE Restaurant SET Payment = \'abc\' WHERE Style >3;'
    # sql_result = cursor.execute(sql)
    # sql = 'UPDATE Restaurant SET Payment = \'ade\' WHERE Style >10;'
    # sql_result = cursor.execute(sql)
    # sql = 'UPDATE Restaurant SET Payment = \'fg\' WHERE Style >15;'
    # sql_result = cursor.execute(sql)
    #
    # cursor.close()
    # conn.close()
