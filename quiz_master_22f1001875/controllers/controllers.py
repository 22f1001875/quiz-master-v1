from flask import Flask,render_template,request,redirect,url_for,session
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
            session['user']=usr.f_name
            session['sup']=usr.is_superuser
            return redirect(url_for("admin", name=usr.f_name))
        else:
            session['user']=usr.f_name
            return render_template("user_mainpage.html",user=usr.f_name)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


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

@app.route("/admin/<name>")
def admin(name):
    subs = Subject.query.all()
    return render_template("admin_dashboard.html",user=name,subjects=subs)

@app.route("/addsub",methods=["GET","POST"])
def addsub():
    user = session.get('user')
    if 'sup' not in session and 'user' in session:
        return render_template('user_mainpage.html',user=user)
    elif 'user' not in session:
        return redirect("/login")
    if request.method=="POST":
        name=request.form.get("sname")
        description=request.form.get("description")
        new_sub=Subject(name=name,description=description)
        db.session.add(new_sub)
        db.session.commit()
        sub_id=Subject.query.filter_by(name=name).first().id
        return redirect(url_for("addchap",sub_id=sub_id))
    return render_template("addsubs.html",user=user)

@app.route("/addchap/<int:sub_id>",methods=["POST","GET"])
def addchap(sub_id):
    message=None
    user = session.get('user')
    if 'sup' not in session and 'user' in session:
        return render_template('user_mainpage.html',user=user)
    elif 'user' not in session:
        return redirect("/login")
    if request.method=="POST":
        name=request.form.get("cname")
        new_chap=Chapter(name=name,s_id=sub_id)
        db.session.add(new_chap)
        db.session.commit()
        message="Successfully added"
    return render_template("addchap.html",sub_id=sub_id, message=message,user=user)

@app.route("/dels/<int:id>",methods=["GET","POST"])
def dels(id):
    user=session.get('user')
    Chapter.query.filter_by(s_id=id).delete()
    Subject.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin",name=user))

@app.route("/delc/<int:id>")
def delc(id):
    user=session.get('user')
    Chapter.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin",name=user))

