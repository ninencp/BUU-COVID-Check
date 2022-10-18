from flask import Flask, render_template, request, redirect, url_for, flash, session
from flaskext.mysql import MySQL
import pymysql
import re

import os
from werkzeug.utils import secure_filename

#--- Folder to upload atk img ----#
UPLOAD_FOLDER = 'static/assets/atk_submit/'
ALLOWED_EXTENSIONS = {'png','jpeg','jpg'}
#---------------------------------#

app = Flask(__name__)
app.secret_key = 'buu-covidcheck'

mysql = MySQL()

#MySQL Configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'covid19_check'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql.init_app(app)

#--------------------- normal user section ------------------------------#

@app.route("/")
def Index():
    db = mysql.connect()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT COUNT(id) FROM atk")
    data = cursor.fetchall()

    cursor.execute("SELECT faculties.name, atk.userID\
                    FROM atk\
                    INNER JOIN faculties ON atk.facultyID=faculties.ID")
    covidPlace = cursor.fetchall()
    print(covidPlace)

    cursor.close()
    return render_template("index.html", value=data)

@app.route("/faqs")
def Faqs():
    return render_template("faq.html")

@app.route("/infected", methods=['POST','GET'])
def Infected():
#     # try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         if request.method == 'POST':
#             draw = request.form('draw')
#             row = int(request.form['start'])
#             rowperpage = int(request.form('length'))
#             searchValue = request.form("search[value]")
#             print(draw)
#             print(row)
#             print(rowperpage)
#             print(searchValue)

#             cursor.execute("SELECT count(*) as allcount from atk")
#             rsallcount = cursor.fetchone()
#             totalRecords = rsallcount['allcount']
#             print(totalRecords)

#             cursor.execute("SELECT atk.send_date, atk.end_date, atk.id, atk.facultyID, faculties.name\
#                         FROM atk\
#                         INNER JOIN faculties ON atk.facultyID=faculties.ID")
#             covidPlace = cursor.fetchall()

#             likeString = "%" + searchValue + "%"
#             cursor.execute("SELECT count(*) as allcount WHERE name LIKE %s OR position LIKE %s OR ")
    return render_template("infected.html")

# http://127.0.0.1:3000/login <-- login page

@app.route("/login", methods=["GET","POST"])
def Login():
    # Connect to database server
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Message if something wrong
    msg = ''

    # If "username" and "password" POST requests exist (user submitted form)
    if request.method == "POST" and 'username' in request.form and 'password' in request.form :
        # Create variable for easy access (don't have to type request.form['username'])
        username = request.form['username']
        password = request.form['password']
        # Check if accounts exist in MySQL
        cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
        # Fetch one record
        account = cursor.fetchone()

        # If account exists in database
        if account:
            # Create session data to access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            # return 'Logged in successfully'
            return redirect((url_for('Home')))
        else:
            msg = 'Incorrect username or password'
    return render_template("login.html", msg=msg)

@app.route("/register", methods=['GET', 'POST'])
def Register():
    # Connect to database server
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Message if something wrong
    msg = ''

    # If "username" and "password" POST requests exist (user submitted form)
    if request.method == "POST" and 'email' in request.form and 'username' in request.form and 'password' in request.form and 'conf_password' in request.form:
        # Create variable for easy access (don't have to type request.form['username'])
        username = request.form['username']
        password = request.form['password']
        conf_password = request.form['conf_password']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        
        # Check if accounts exist in MySQL
        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username, ))
        # Fetch one record
        account = cursor.fetchone()

        # If account exists in database show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers'
        elif not re.match(r'[0-9]+', phone):
            msg = 'Phone number must contain only numbers'
        elif not password == conf_password:
            msg = 'Password did not match. Please try again'
        elif not username or not password or not email or not name or not phone:
            msg = 'Please fill out the form!'
        else:
            # Account dosen't exist
            cursor.execute("INSERT INTO accounts (name, phone, email, username, password, conf_password) VALUES (%s, %s, %s, %s, %s, %s)", (name, phone, email, username, password, conf_password))
            conn.commit()
            msg = 'You have successfully registered!'
            
    elif request.method == "POST":
        # Empty form
        msg = 'Please fill out the form!'

    return render_template("register.html", msg=msg)

#--------------------------------------------------------------------#


#--------------------- members section ------------------------------#

@app.route("/home")
def Home():
    db = mysql.connect()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT COUNT(id) FROM atk")
    data = cursor.fetchall()

    cursor.close()
    # Check if user is logged in
    if 'loggedin' in session:
        # if user logged in show them homepage
        return render_template('home.html', username=session['username'], value=data)
    # if user isn't logged in return to login page
    return redirect(url_for('Login'))

@app.route("/members/faqs")
def MemFaq():
    # Check if user is logged in
    if 'loggedin' in session:
        # if user logged in show them homepage
        return render_template('faq_members.html', username=session['username'])
    return redirect(url_for('Index'))


@app.route("/logout")
def Logout():
    # Remove session data. This will log user out.
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to index
    return redirect(url_for('Index'))

@app.route("/profile")
def Profile():
    # Check if account existing in MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is logged in
    if 'loggedin' in session:
        # select all info of user's account
        cursor.execute("SELECT * FROM accounts WHERE id = %s", [session['id']])
        account = cursor.fetchone()
        print(account)

        cursor.execute("SELECT accounts.name, atk.send_date, atk.end_date, atk.id, atk.facultyID, faculties.name\
                        FROM atk\
                        INNER JOIN accounts ON atk.userID=%s\
                        INNER JOIN faculties ON atk.facultyID=faculties.id",[session['id']])
        atk_data = cursor.fetchone()

        if atk_data:
            cursor.execute("SELECT DATEDIFF(%s,CURDATE())",(atk_data['end_date']))
            cur_date = cursor.fetchone()
            isolation=list(cur_date.values())[0]
            
            if isolation > 0:
                return render_template('profile.html', account = account, username=session['username'], atk=atk_data, isolation=isolation)
            else:
                cursor.execute("DELETE FROM atk_img WHERE aID=%s",[atk_data['id']])
                cursor.execute("DELETE FROM atk WHERE userID=%s",[session['id']])
                conn.commit()
                return render_template('profile.html', account = account, username=session['username'], atk=atk_data)

        else:
            return render_template('profile.html', account = account, username=session['username'], atk=atk_data)
    # user isn't logged in return to index page
    return redirect(url_for('Index'))

@app.route("/edit/<id>", methods=['GET','POST'])
def GetUser(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM accounts WHERE id = %s", (id))
    data = cursor.fetchall()
    cursor.close()
    print(data[0])
    return render_template('edit.html', user=data[0])

@app.route("/update/<id>", methods=['POST'])
def Update(id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""
                        UPDATE accounts 
                        SET name = %s,
                            phone = %s,
                            email = %s
                        WHERE id = %s
                        """, (name, phone, email, id))
        flash("Updated successfully")
        conn.commit()
        return redirect(url_for('Profile'))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/submit")
def Submit():
    # Check if account existing in MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is logged in
    if 'loggedin' in session:
        # select all info of user's account
        cursor.execute("SELECT * FROM accounts WHERE id = %s", [session['id']])
        cursor.execute("SELECT * FROM faculties")
        data = cursor.fetchall()
        account = cursor.fetchone()
        # show on profile page
        return render_template('submit.html', account = account, username=session['username'], data=data)
    # user isn't logged in return to index page
    return redirect(url_for('Index'))

@app.route("/submit", methods=['GET','POST'])
def upload_image():
    # Check if account existing in MySQL
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Check if user is logged in
    if 'loggedin' in session:
        # select all info of user's account
        cursor.execute("SELECT * FROM accounts WHERE id = %s", [session['id']])
        account = cursor.fetchone()
        uID = session['id']
        cursor.execute("SELECT * FROM faculties")
        data = cursor.fetchall()
        # print("data: ",data)


    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename) and request.method == 'POST':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)

        send = request.form['date']
        faculty = request.form['faculty']
        print(faculty)
        f_ID = cursor.execute("SELECT id FROM faculties WHERE name = %s",(faculty))
        print(f_ID)
        cursor.execute("INSERT INTO atk(send_date, userID, end_date, facultyID) VALUES(%s,%s,DATE_ADD(%s,INTERVAL 10 DAY),%s)", (send,uID,send,f_ID))

        cursor.execute("SELECT id FROM atk WHERE userID = %s", [session['id']])
        val = cursor.fetchone()
        print(val)
        aID = val['id']
        cursor.execute("INSERT INTO atk_img (aid, name) VALUES (%s, %s)", (aID, filename))
        conn.commit()

        flash('Image successfully uploaded')
        return render_template('submit.html', account = account, username=session['username'], data=data, filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)

#--------------------------------------------------------------------#

# admin section
# @app.route("/admin/login")
# def AdminLogin():
#     # Connect to database server
#     conn = mysql.connect()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)

#     # Message if something wrong
#     msg = ''

#     # If "username" and "password" POST requests exist (user submitted form)
#     if request.method == "POST" and 'username' in request.form and 'password' in request.form :
#         # Create variable for easy access (don't have to type request.form['username'])
#         username = request.form['username']
#         password = request.form['password']
#         # Check if accounts exist in MySQL
#         cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
#         # Fetch one record
#         account = cursor.fetchone()

#         # If account exists in database
#         if account:
#             # Create session data to access this data in other routes
#             session['loggedin'] = True
#             session['id'] = account['id']
#             session['username'] = account['username']
#             # Redirect to home page
#             # return 'Logged in successfully'
#             return redirect((url_for('Home')))
#         else:
#             msg = 'Incorrect username or password'
#     return render_template("login.html", msg=msg)

# start app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
