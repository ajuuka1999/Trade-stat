#!/usr/bin/python3
import code
import email
from flask import Flask,redirect,url_for,render_template,request,flash,session,send_file
import sqlite3
from urllib.parse import urlparse
import os
import sys
import time
import yagmail
from searchapi import *

#from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__,template_folder='template')
app.secret_key = 'trade statistics'
Codes =[]
Codeset =set()
dbconnectemail = str()
username = str()
setalert = 0
alertcode = ""

@app.route("/mainpage", methods=["refresh=GET","GET","PUT"])
def mainpage():
    return render_template("mainpage_ex.html")

@app.route("/refresh", methods=["POST","GET", "registernew=registernewPOST","refresh=GET","refresh=POST"])
def refresh():

    print("refresh")

    global Codes
    global Codeset
    global dbconnectemail
    global username
    print("dbconnectemail",dbconnectemail)
    print("username", username)

    try:
        con = sqlite3.connect("trade.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE email = '"+dbconnectemail+"'")
        profile = cur.fetchall()
    except:
        flash("DB not connected")
        return "DB not connected"

    codesindb = profile[0][5]
    print(codesindb)

    if codesindb != None:

        dbcodes = codesindb.split("+")
        Codeset.update(dbcodes)
        print("dbcodes",dbcodes)
        print("Codeset",Codeset)
    else:
        Codeset=[]

    printstock =[]

    if len(Codeset)==0:
        return redirect(url_for("mainpage"))

    for code in Codeset:

        if code == "NONE":
            flash('Hello ' + username)
            return render_template("mainpage_ex.html")

        STCK = search(code)
        if STCK == False:
            return "Invalid Symbol"
        printstock+=STCK
        print(printstock)


    if len(Codeset)==1:
        return render_template("onestock.html",Company=printstock[0],Date=printstock[1],Open=printstock[2],High=printstock[3],Low=printstock[4],Close=printstock[5],Volume=printstock[6])
    if len(Codeset)==2:
        return render_template("twostock.html",Company1=printstock[0],Date1=printstock[1],Open1=printstock[2],High1=printstock[3],Low1=printstock[4],Close1=printstock[5],Volume1=printstock[6],
        Company2=printstock[7],Date2=printstock[8],Open2=printstock[9],High2=printstock[10],Low2=printstock[11],Close2=printstock[12],Volume2=printstock[13])
    if len(Codeset)==3:
        return render_template("threestock.html",Company1=printstock[0],Date1=printstock[1],Open1=printstock[2],High1=printstock[3],Low1=printstock[4],Close1=printstock[5],Volume1=printstock[6],
        Company2=printstock[7],Date2=printstock[8],Open2=printstock[9],High2=printstock[10],Low2=printstock[11],Close2=printstock[12],Volume2=printstock[13],Company3=printstock[14],Date3=printstock[15],
        Open3=printstock[16],High3=printstock[17],Low3=printstock[18],Close3=printstock[19],Volume3=printstock[20])
    if len(Codeset)==4:
        return render_template("fourstcok.html",Company1=printstock[0],Date1=printstock[1],Open1=printstock[2],High1=printstock[3],Low1=printstock[4],Close1=printstock[5],Volume1=printstock[6],
        Company2=printstock[7],Date2=printstock[8],Open2=printstock[9],High2=printstock[10],Low2=printstock[11],Close2=printstock[12],Volume2=printstock[13],Company3=printstock[14],Date3=printstock[15],
        Open3=printstock[16],High3=printstock[17],Low3=printstock[18],Close3=printstock[19],Volume3=printstock[20],Company4=printstock[21],Date4=printstock[22],Open4=printstock[23],High4=printstock[24],
        Low4=printstock[25],Close4=printstock[26],Volume4=printstock[27])

    if len(Codeset)==5:
        return render_template("fivestock.html",Company1=printstock[0],Date1=printstock[1],Open1=printstock[2],High1=printstock[3],Low1=printstock[4],Close1=printstock[5],Volume1=printstock[6],
        Company2=printstock[7],Date2=printstock[8],Open2=printstock[9],High2=printstock[10],Low2=printstock[11],Close2=printstock[12],Volume2=printstock[13],Company3=printstock[14],Date3=printstock[15],
        Open3=printstock[16],High3=printstock[17],Low3=printstock[18],Close3=printstock[19],Volume3=printstock[20],Company4=printstock[21],Date4=printstock[22],Open4=printstock[23],High4=printstock[24],
        Low4=printstock[25],Close4=printstock[26],Volume4=printstock[27],Company5=printstock[28],Date5=printstock[29],Open5=printstock[30],High5=printstock[31],Low5=printstock[32],Close5=printstock[33],Volume5=printstock[34])

    if len(Codeset)>=6:
        return "maximum 5 companies allowed"
    else:
        return "printstock"



@app.route("/registernew", methods=["POST","GET"])
def registernew():

    print("registernew")

    global Codes
    global Codeset
    global dbconnectemail
    global username

    print("dbconnectemail",dbconnectemail)
    time.sleep(1)
    flash('Hello ' + username)
    return render_template("mainpage_ex.html")

def startalert():
    global alertcode
    global setalert
    print(alertcode,setalert)


@app.route("/setalerts", methods=["POST","GET","registernew=registernewPOST"])
def registeralerts():

    print("registeralerts")

    global Codes
    global Codeset
    global dbconnectemail
    global username
    global alertcode
    global setalert
    sender_email = 'sampleemail@gmail.com'
    sender_password = 'password'
    receiver_email = dbconnectemail
    yag = yagmail.SMTP(user=sender_email, password=sender_password)

    print("dbconnectemail",dbconnectemail)
    print(request.form)
    code_comp = request.form["code_comp"]
    value = request.form["value"]
    print(code_comp,value)
    print(Codeset)
    time.sleep(1)
    try:
        con = sqlite3.connect("trade.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE email = '" + dbconnectemail + "'")
        profile = cur.fetchall()
    except:
        flash("DB not connected")
        return "DB not connected"

    codesindb = profile[0][5]
    dbcodes = codesindb.split("+")
    Codeset.update(dbcodes)
    print("dbcodes",dbcodes)
    print("Codeset",Codeset)
    if code_comp in Codeset:
        print("code is registered")
        alertcode = code_comp.upper()
        contents = ['Alert is started for {}.Your target is $ {}'.format(alertcode,value)]
        Subject = "Trade Alert"
        setalert = 1
        yag.send(to=receiver_email, subject=Subject, contents=contents)
        STCK = search(code_comp.upper())
        if float(STCK[5]) >= int(value):
            contents = ['Your targte for {} is reached'.format(alertcode)]
            yag.send(to=receiver_email, subject=Subject, contents=contents)
            setalert = 0





    flash('Hello ' + username)
    return render_template("mainpage_ex.html")



@app.route("/sp_list")
def sp_list():
    return render_template("tables.html")



@app.route("/add_code", methods=["POST", "GET","refresh=POST","registernew=registernewPOST"])
def add_code():
    print("in add_code")
    global Codes
    global Codeset
    global dbconnectemail
    print("dbconnectemail",dbconnectemail)
    try:
        con = sqlite3.connect("trade.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM user WHERE email = '"+dbconnectemail+"'")
        profile = cur.fetchall()
    except:
        flash("DB not connected")
        return "DB not connected"

    print(profile)
    codesindb = profile[0][5]

    if codesindb == 'NONE':
        print("test")
        Codeset = set()
    else:
        dbcodes = codesindb.split("+")
        Codeset.update(Codes)

    print("Codeset",Codeset)

    code_comp = request.form["code_comp"]
    print("code_comp",code_comp)
    Codes = code_comp.split(",")
    if len(Codeset) < 5:
        Codeset.update(Codes)
        code_comp_db = str()
        for x in Codeset:
            goodcode = validatecode(x)
            if goodcode is True:
                code_comp_db = x+"+"+ code_comp_db
            else:
                print("{} is not a valide code".format(x))
                Codeset= Codeset.remove(x)


        code_comp_db =code_comp_db.strip("+")
        print("code_comp_db", code_comp_db)
        cur.execute("UPDATE user SET comp_code = (?) WHERE email = (?)", (code_comp_db, dbconnectemail))
        con.commit()
        cur.execute("SELECT * FROM user WHERE email = '"+dbconnectemail+"'")
        updatecheck=cur.fetchall()
        if code_comp_db in updatecheck[0][5]:
            return redirect(url_for("mainpage"))
        else:
            return "Update Failed"
    else:
        return redirect(url_for("mainpage"))



@app.route("/logout", methods=["POST", "GET"])
def logout():
    return render_template ("logout.html")


#Sign In

@app.route("/signin", methods=["POST", "GET"])
def signin():
    global dbconnectemail
    global username
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
                dbconnectemail = email
                session["username"] = i[1]
                username = i[1]
                print ("verification success")
                flash('Hello '+session["username"])

                return redirect(url_for("mainpage"))
            else:
                flash("Please enter valid email and password")
                return redirect(url_for("signin"))
    return render_template("login.html")

#Sign In End


@app.route("/remove", methods=["POST","GET"])
def remove():
    print("im in remove")
    global Codeset
    print(request.form)
    Code = request.form["remove"]
    print("Code before",Code)
    print("Codeset before",Codeset)
    Code = Code.strip("remove").strip(" ")
    Codeset.remove(Code)
    print(Codeset)
    code_comp_db = str()
    if len(Codeset) == 0:
        code_comp_db = "NONE"
    else:
        for x in Codeset:
            goodcode = validatecode(x)
            if goodcode is True:
                code_comp_db = x+"+"+ code_comp_db
            else:
                print("{} is not a valide code".format(x))

        code_comp_db =code_comp_db.strip("+")

    print(code_comp_db)
    try:
        con = sqlite3.connect("trade.db")
        cur = con.cursor()
    except:
        flash("DB not connected")
        return "DB not connected"

    cur.execute("UPDATE user SET comp_code = (?) WHERE email = (?)", (code_comp_db, dbconnectemail))
    con.commit()
    cur.execute("SELECT * FROM user WHERE email = '"+dbconnectemail+"'")
    updatecheck=cur.fetchall()
    if code_comp_db in updatecheck[0][5]:
        return redirect(url_for("mainpage"))
    else:
        return "Update Failed"


#Registering the account

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
            cur.execute("INSERT OR REPLACE into user (name, email, country, password, comp_code) values (?, ?, ?, ?, ?)", (name, email, country, hashed, 'NONE'))
            print ("inserting into table")
            con.commit()
            return redirect(url_for("signin"))
        except:
            con.rollback()
            flash("Sorry failed")
            return redirect(url_for("register"))
    return render_template("register.html")

#Registering Ending



@app.route("/market")
def market():
    return render_template("market.html")

@app.route("/")
def index():
    #return index page
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")
@app.route("/about")
def about():
    #return about page
    return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True)
