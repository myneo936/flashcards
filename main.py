from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db1.sqlite3'
app.config['SECRET_KEY']='HELLO@54'
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()


@app.before_request
def require_login():
    allowed_routes=['login','register']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

    


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        conn=sqlite3.connect("db1.sqlite3")
        cur=conn.cursor()
        query="""SELECT * FROM users WHERE username=? AND password=?"""
        cur.execute(query,(username,password))
        rows=cur.fetchall()
        if len(rows) ==1:
            session['username']=username
            return redirect(url_for('dashboard',username=username))
        else:
            return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        try:
            username=request.form['username']
            password=request.form['password']
            conn=sqlite3.connect("db1.sqlite3")
            cur=conn.cursor()
            query="""INSERT INTO users (username,password) VALUES (?,?)"""
            cur.execute(query,(username,password))
            conn.commit()
            if cur.rowcount == 1:
                return "Registered successfully <a href='/login'>Go to Login</a>"
            else:
                return "Username already exists <a href='/register'>Try Register again</a>"
        except:
            return "Something wrong"
    return render_template('register.html')

@app.route('/')
def index():
    return redirect(url_for('dashboard',username='USERNAMENOTGIVENTHINREDIRECTTOLOGINPAGE'))

@app.route('/<username>')
def dashboard(username='USERNAMENOTGIVENTHINREDIRECTTOLOGINPAGE'):
    if username=='USERNAMENOTGIVENTHINREDIRECTTOLOGINPAGE':
        return redirect(url_for('login'))
    conn=sqlite3.connect("db1.sqlite3")
    cur=conn.cursor()
    global u
    u=username
    print(u)
    query=("""SELECT u_score FROM users WHERE username=?""")
    cur.execute(query,[username])
    score=cur.fetchone()
    return render_template('dashboard.html',u_score=score)

@app.route('/updatedeck',methods=['GET','POST'])
def updatedeck():
    if request.method=="POST":
        o_c_name=request.form['old']
        c_name=request.form['c_name']
        c_image=request.form['c_image']
        c_population=request.form['c_population']
        c_area=request.form['c_area']
        conn=sqlite3.connect("db1.sqlite3")
        cur=conn.cursor()
        query="""UPDATE country SET c_name=?,c_image=?,c_population=?,c_area=? WHERE c_name=?"""
        cur.execute(query,(c_name,c_image,c_population,c_area,o_c_name))
        conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('updatedeck.html')


@app.route('/review')
def review():
    global u
    score=0
    conn=sqlite3.connect("db1.sqlite3")
    cur=conn.cursor()
    query="""SELECT * FROM country WHERE c_image IS NOT NULL ORDER BY RANDOM()"""
    cur.execute(query,())
    rows=cur.fetchone()
    if request.method=='POST':
        ans=request.form['answer']
        query1="""UPDATE users SET u_score=? WHERE username=?"""
        cur.execute(query1,(score,u))
        conn.commit()
        if rows[0]==ans:
            score+=1   
    if rows is not None:
        return render_template('review.html',rows=rows,username=u)
    else:
        return redirect(url_for('dashboard'))


@app.route('/addcard',methods=['GET','POST'])
def addcard():
    if request.method=="POST":
        c_image=request.form['c_image']
        c_name=request.form['c_name']
        c_population=request.form['c_population']
        c_area=request.form['c_area']
        conn=sqlite3.connect("db1.sqlite3")
        cur=conn.cursor()
        query="""INSERT INTO country (c_name,c_population,c_area,c_image) VALUES (?,?,?,?)"""
        cur.execute(query,(c_name,c_population,c_area,c_image))
        conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('addcard.html')

@app.route('/viewdeck',methods=['GET'])
def view():
    conn=sqlite3.connect("db1.sqlite3")
    cur=conn.cursor()
    cur.execute("""SELECT * FROM COUNTRY""")
    rows=cur.fetchall()
    return render_template('viewdeck.html',rows=rows)


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False,port='8080')