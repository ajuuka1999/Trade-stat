import code
#from crypt import methods
from flask import Flask,redirect,url_for,render_template,request,flash,session,send_file
import sqlite3
import bcrypt
from fpdf import FPDF
from urllib.parse import urlparse
import os
import sys
import time
import yagmail
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__,template_folder='template')
app.secret_key = 'trade statistics'

@app.route("/mainpage")
def mainpage():
    return render_template("mainpage.html")

@app.route("/sp_list")
def sp_list():
    return render_template("tables.html")
    
@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
    
        try:
            con = sqlite3.connect("trade.db")
            cur=con.cursor()
            cur.execute("SELECT * FROM user WHERE email = '"+email+"' and password = '"+password+"'")
            r = cur.fetchall()
        except:
            flash("Does not connect to Database")

        for i in r:
            if (email == i[2] and password == i[4]):
                session["logedin"] = True
                session["email"] = email
                session["username"] = i[1]
                flash('Hello '+session["username"])

                return redirect(url_for("mainpage"))
            else:
                flash("Please enter valid email and password")
                return redirect(url_for("signin"))
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        country = request.form["country"]
        hashed = request.form["password"]
        try:
            con=  sqlite3.connect("trade.db")
            cur = con.cursor()
            cur.execute("INSERT OR REPLACE into user (name, email, country, password) values (?, ?, ?, ?)", (name, email, country, hashed))
            print ("inserting into table")
            con.commit()
            return redirect(url_for("signin"))
        except:
            con.rollback()
            flash("Sorry failed")
            return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/")
def index():
    #return 'Hello'
    return render_template("index.html")

if __name__ == "__main__":
    app.run()