#web applications, web apis, machine learning apps-flask usage
#flask - web application framework written in python
#based on wsgi(web server gateway interface- standard protocol) concept. 
#based on jinja2 template engine

#clients request for web server to access a web application using http requests(happens in www).
# a protocol is required to communicate with the web server and web application-wsgi used 

#jinja2 template engine
#web templating sysetm used for python
#combines web template with a data source
#renders dynamic pages(getting data from sql db or ml model when web app needs data)


# ------ http verbs GET and POST ---------


'''
To print output coming from routes,
{%...%} conditions, for loop
{{    }} epressions to print output
{#  #} comments
'''

from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import os
import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
import pandas as pd

date = datetime.now()
print(date)


#to serve a html page using flask, u need a function: render_template
#render_template needs a folder 'templates'
# REQUEST helps u read the posted values from form
#create a var..pass name of module to the class
#session is a type of dictionary
#session used so that user cant enter home without login and login page shld not have login details. user shldnt be directly able to go to home w/o login
#create a connection object conn

conn=mysql.connector.connect(user='root',password='Tjss@2020',host='localhost',database='Library')
#cursor-used to communicate with database
cursor=conn.cursor()

app = Flask(__name__, static_url_path='/static')

app.secret_key=os.urandom(24)

#creating a decorator
@app.route('/') #if anyone heyJzdHVkZW50X0lkIjoiUzAxIn0.Zgcfvw.dB1fj3xVGmGd6piWgx5o49Ua_wwits our websites url or ip adress i.e 127.0.0.1:5000/ then return
def login(): #function
    return render_template('login.html')

#another route
@app.route('/register') #decorator
def about():
    return render_template('register.html')

#user enters home after login
@app.route('/home')
def home():
    
    if 'student_id' in session: #this will be true only if user has logged in
        return render_template('home.html')
    else:
        return redirect('/') #not registered student will be redirected the login page
    #return render_template('home.html')
    
#when u send data from filling html forms to server->data travels through post method
#when u send data through url -> get method
#form->post method
#url->get method

@app.route('/login_validation',methods=['POST']) # to receive data coming through post,methods=['POST']
def login_validation():
    userid=request.form.get('userid')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""SELECT * FROM `student` WHERE `Email` LIKE '{}' and `password` LIKE '{}'""".format(email,password))
    #return """SELECT * FROM `student` WHERE `email` LIKE {} AND `password` LIKE {}""".format(email,password)
    user=cursor.fetchall()
    
    #print(user)


    if len(user)>0:
        global id
        id=session['student_id']=user[0][0]
        print(id)
        return redirect('/home')
        #return render_template('home.html')
    else:
        return redirect('/')
        #return render_template('login.html')
    

# [(),(),()]  --> List of tuples

#adding new registrations into the dats=base
@app.route('/add_student',methods=['POST'])
def add_student():
    name=request.form.get('username')
    email=request.form.get('useremail')
    password=request.form.get('userpassword')
    city=request.form.get('city')
    state=request.form.get('state')
    zip=request.form.get('zip')
    id=request.form.get('id')
    college=request.form.get('college')
    
    cursor.execute("""INSERT INTO `student` (`StudentId`,`Student_Name`,`State`,`City`,`ZipCode`,`Email`,`College`,`password`) 
                   VALUES('{}','{}','{}','{}','{}','{}','{}','{}')""".format(id,name,state,city,zip,email,college,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `student` WHERE `Email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['student_id']=myuser[0][0]
    return redirect("/home")

@app.route('/search_book',methods=['POST'])
def search_book():
    conn=mysql.connector.connect(user='root',password='Tjss@2020',host='localhost',database='Library')
    cursor=conn.cursor()
    searchType=request.form.get('searchType')
    searchValue=request.form.get('searchValue')
    if searchType == "Name":
        cursor.execute("""SELECT * FROM `books` WHERE `title` LIKE '%{}%'""".format(searchValue))
    elif searchType == "Genre":
        cursor.execute("""SELECT * FROM `books` natural join `genre` WHERE `genre` LIKE '%{}%'""".format(searchValue))
    else:
        cursor.execute("""SELECT * FROM `books` WHERE `book_id` LIKE '%{}%'""".format(searchValue))

    global book_id
    
    #cursor.execute("""SELECT * FROM `books` WHERE `title` LIKE '%{}%'""".format(searchValue))
    mybook=cursor.fetchone()
    book_id=mybook[0]
    #cursor.execute("""SELECT * FROM `books`""")
    conn.commit()
    #print(type(searchType))
    return render_template("books.html",mybook=mybook)
    #print(searchType)
    #return searchType



#issue
@app.route('/insert_issue',methods=['POST'])
def insert_issue():
    conn=mysql.connector.connect(user='root',password='Tjss@2020',host='localhost',database='Library')
    #cursor-used to communicate with database
    cursor=conn.cursor()
     #YYYY-MM-DD format
    
    cursor.execute("""SELECT * FROM `books` WHERE `book_id` LIKE '{}'""".format(book_id))
    mybook=cursor.fetchone()

    date='2024-04-1'
    if 'issue' in request.form:
        #print(book_id)
        #print(id)
        
        cursor.execute("""INSERT INTO `issues` (`StudentId`,`book_id`,`issue_date`) 
                    VALUES('{}','{}',curdate())""".format(id,book_id))
        conn.commit()
        #print(id)
        return """
            <html>
            <head><title>Issue Confirmation</title></head>
            <body>
                <h1>Book Issued Successfully</h1>
                <p>Book Title: {}</p>
                <p>Book ID: {}</p>
                <p>Issue Date: {}</p>
            </body>
            </html>
        """.format(mybook[2], mybook[0], '2024-04-01') 
        return render_template("issue.html",mybook=mybook)
        return "isssue successfull "
    elif 'return' in request.form:
        
        #print(return_date=(issue_date + datetime.timedelta(days=30)))
        # cursor.execute("""SELECT book_id,issue_date FROM `issues` WHERE `book_id` LIKE '{}'""".format(book_id))
        # data=cursor.fetchone()
        due=0
        # issue_date=data[1]
        # print(type(issue_date))
        # return_date = pd.to_datetime(issue_date) + pd.DateOffset(days=30)
        # return_date=return_date.date()
        # print(type(return_date))
        # cursor.close()

        conn=mysql.connector.connect(user='root',password='Tjss@2020',host='localhost',database='Library')
        cursor=conn.cursor()
        cursor.execute("""INSERT INTO `returnss` (`StudentId`,`book_id`,`actual_return_date`,`return_date`,`due`) 
                   VALUES('{}','{}',curdate(),DATE_ADD(curdate(),INTERVAL 30 DAY),'{}')""".format(id,book_id,due))
        
        conn.commit()
        return """
            <html>
            <head><title>Issue Confirmation</title></head>
            <body>
                <div class="container">
                <h1>Book Successfully Returned</h1>
                <p>Book Title: {}</p>
                <p>Book ID: {}</p>
                <p>Issue Date: {}</p>
                </div>
            </body>
            </html>
        """.format(mybook[2], mybook[0], '2024-04-01') 
        #return render_template("issue.html",mybook=mybook)
        #return render_template("return.html",mybook=mybook)
        #return "RETURNED SUCCESSFULLY"
    
    
@app.route('/profile')
def profile():
    conn=mysql.connector.connect(user='root',password='Tjss@2020',host='localhost',database='Library')
    cursor=conn.cursor()
    
    cursor.execute("""SELECT * FROM `student` WHERE `StudentId` LIKE '%{}%'""".format(id))
    
    global book_id
    
    user=cursor.fetchone()
    conn.commit()

    return render_template("index.html",user=user)
        
#logout
@app.route('/logout')
def logout():
    session.pop('student_id')

    return redirect('/')


if __name__=="__main__":
    app.run(debug=True) #debug=True.. if u make changes to your code,u neednt run ur code again and again to reload on browser.
    
    #It will generate a url(127.0.0.1) where hello world will get printed. Flask is assaigned 5000
