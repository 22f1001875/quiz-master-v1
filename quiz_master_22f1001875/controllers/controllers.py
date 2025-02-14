from flask import Flask,render_template,request,redirect
from flask import current_app as app
from models.models import *
from datetime import date
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        mail=request.form.get("mail")
        pwd=request.form.get("pwd")
        usr=Users.query.filter_by(mail=mail,pwd=pwd).first()
        if usr and usr.is_superuser:
            return render_template("admin_dashboard.html",name=usr.f_name)
        else:
            return render_template("user_mainpage.html",name=usr.f_name)
    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        mail=request.form.get("mail")
        pwd=request.form.get("pwd")
        fname=request.form.get("fname")
        qual=request.form.get("qual")
        dob=request.form.get("dob")
        da=dob.split("-")
        dateofb=date(int(da[0]),int(da[1]),int(da[2]))
        new_user=Users(mail=mail,pwd=pwd,f_name=fname,qual=qual,dob=dateofb)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")