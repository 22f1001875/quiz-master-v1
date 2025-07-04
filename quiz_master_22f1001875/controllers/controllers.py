from flask import Flask,render_template,request,redirect,url_for,session
from flask import current_app as app
from models.models import *
from datetime import date,datetime

today = date.today()
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    messages=None
    if request.method=="POST":
        mail=request.form.get("mail")
        pwd=request.form.get("pwd")
        usr=Users.query.filter_by(mail=mail,pwd=pwd).first()
        if usr and usr.is_superuser:
            session['id']=usr.id
            session['user']=usr.f_name
            session['sup']=usr.is_superuser
            return redirect(url_for("admin", name=usr.f_name))
        elif usr and usr.is_superuser==0:
            session['id']=usr.id
            session['user']=usr.f_name
            session['sup']=usr.is_superuser
            return redirect(url_for("user",name=usr.f_name))
        else:
            messages="Something went wrong. Try again"
    return render_template("login.html",messages=messages)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/register",methods=["GET","POST"])
def register():
    message=None
    if request.method=="POST":
        mail=request.form.get("mail")
        pwd=request.form.get("pwd")
        fname=request.form.get("fname")
        qual=request.form.get("qual")
        dob=request.form.get("dob")
        da=dob.split("-")
        dateofb=date(int(da[0]),int(da[1]),int(da[2]))
        if not Users.query.filter_by(mail=mail).first():
            new_user=Users(mail=mail,pwd=pwd,f_name=fname,qual=qual,dob=dateofb)
            db.session.add(new_user)
            db.session.commit()
        else:
            message="User Already Exists"
            return render_template("register.html",mesa=message)
        return redirect("/login")
    return render_template("register.html",mesa=message)

@app.route("/admin/<name>")
def admin(name):
    subs = Subject.query.all()
    return render_template("admin_dashboard.html",user=name,subjects=subs)

@app.route("/addsub",methods=["GET","POST"])
def addsub():
    user = session.get('user')
    if 'user' in session:
        if session['sup']!=1:
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
    sup=session.get('sup')
    return render_template("addsubs.html")

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
    return render_template("addchap.html",sub_id=sub_id, message=message)

@app.route("/dels/<int:id>",methods=["GET","POST"])
def dels(id):
    user=session.get('user')
    chaps=Chapter.query.filter_by(s_id=id).all()
    if chaps:
        for chap in chaps:
            quis=Quiz.query.filter_by(c_id=chap.id).all()
            if quis:
                for qui in quis:
                    Questions.query.filter_by(q_id=qui.id).delete()
            Quiz.query.filter_by(c_id=chap.id).delete()
    Chapter.query.filter_by(s_id=id).delete()
    Subject.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin",name=user))

@app.route("/delc/<int:id>")
def delc(id):
    user=session.get('user')
    quis=Quiz.query.filter_by(c_id=id).all()
    if quis:
        for qui in quis:
            Questions.query.filter_by(q_id=qui.id).delete()
    Quiz.query.filter_by(c_id=id).delete()
    Chapter.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for("admin",name=user))

@app.route("/qdisplay/<int:c_id>",methods=["GET","POST"])
def qdisplay(c_id):
    if request.method=="POST":
        tt=request.form.get('timed')
        doq=request.form.get('doq')
        da=doq.split("-")
        dateofq=date(int(da[0]),int(da[1]),int(da[2]))
        remarks=request.form.get('remarks')
        new_quiz=Quiz(date=dateofq,time_duration=tt,remarks=remarks,c_id=c_id)
        db.session.add(new_quiz)
        db.session.commit()
        quizzes=Quiz.query.filter_by(c_id=c_id).all()
        return redirect(url_for('qdisplay', c_id=c_id))
    quizzes = Quiz.query.filter_by(c_id=c_id, date=today).all()
    quizprev=Quiz.query.filter(Quiz.c_id == c_id, Quiz.date < today).all()
    quizupcoming=Quiz.query.filter(Quiz.c_id == c_id, Quiz.date > today).all()
    return render_template("quizzdash.html",quizzes=quizzes,c_id=c_id,quizprev=quizprev,quizupcoming=quizupcoming)

@app.route("/quizdelete/<int:q_id>")
def quizdelete(q_id):
    c_id=Quiz.query.filter_by(id=q_id).first().c_id
    Questions.query.filter_by(q_id=q_id).delete()
    Quiz.query.filter_by(id=q_id).delete()
    db.session.commit()
    return redirect(url_for("qdisplay",c_id=c_id))

@app.route("/question/<int:q_id>",methods=["POST","GET"])
def questions(q_id):
    quests=Questions.query.filter_by(q_id=q_id)
    if request.method=="POST":
        question=request.form.get('question')
        op1=request.form.get('op1')
        op2=request.form.get('op2')
        op3=request.form.get('op3')
        op4=request.form.get('op4')
        cop=request.form.get('inlineRadioOptions')
        new_question=Questions(q_id=q_id,question=question,op1=op1,op2=op2,op3=op3,op4=op4,cop=cop)
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for("questions",q_id=q_id))
    return render_template("questiondash.html",quests=quests,q_id=q_id)

@app.route("/questdel/<int:questid>")
def questdel(questid):
    q_id=Questions.query.filter_by(id=questid).first().q_id
    Questions.query.filter_by(id=questid).delete()
    db.session.commit()
    return redirect(url_for("questions",q_id=q_id))

@app.route("/subjedit/<int:sub_id>",methods=["POST","GET"])
def subjedit(sub_id):
    s=Subject.query.filter_by(id=sub_id).first()
    if request.method=="POST":
        s.name=request.form.get('sname')
        s.description=request.form.get('description')
        db.session.commit()
        return redirect(url_for("admin",name=user))
    return render_template("subjedit.html",sub_id=sub_id)

@app.route("/chapedit/<int:id>",methods=["GET","POST"])
def chapedit(id):
    c=Chapter.query.filter_by(id=id).first()
    if request.method=="POST":
        c.name=request.form.get('cname')
        db.session.commit()
        return redirect(url_for("admin",name=user))
    return render_template("chapedit.html",c_id=id)

@app.route("/quizedit/<int:id>",methods=["GET","POST"])
def quizedit(id):
    user=session.get('user')
    c_id=Quiz.query.filter_by(id=id).first().c_id
    q=Quiz.query.filter_by(id=id).first()
    if request.method=="POST":
        q.time_duration=request.form.get('timed')
        doq=request.form.get('doq')
        da=doq.split("-")
        q.date=date(int(da[0]),int(da[1]),int(da[2]))
        q.remarks=request.form.get('remarks')
        q.c_id=c_id
        db.session.commit()
        return redirect(url_for('qdisplay', c_id=c_id))  
    return render_template("quizedit.html",user=user,q_id=id)


@app.route("/questedit/<int:id>",methods=["POST","GET"])
def questedit(id):
    q_id=Questions.query.filter_by(id=id).first().q_id
    q=Questions.query.filter_by(id=id).first()
    if request.method=="POST":
        q.question=request.form.get('question')
        q.op1=request.form.get('op1')
        q.op2=request.form.get('op2')
        q.op3=request.form.get('op3')
        q.op4=request.form.get('op4')
        q.cop=request.form.get('inlineRadioOptions')
        q.q_id=q_id
        db.session.commit()
        return redirect(url_for("questions",q_id=q_id))  
    return render_template("questedit.html",id=id)


@app.route("/user/<name>")
def user(name):
    message=None
    if 'messages' in session:
        message=session['messages']
        session['messages']=[]
    subs = Subject.query.all()
    return render_template("user_mainpage.html",user=name,subjects=subs,message=message)


@app.route('/attempt', methods=['POST'])
def attempt_redirect():
    quizid = request.form.get("quizid")
    clicked_time = datetime.now().strftime("%H:%M:%S").split(':')
    teme=int(clicked_time[0])*3600+int(clicked_time[1])*60+int(clicked_time[2])
    session['tume'] = int(teme)
    return redirect(url_for('quizattempt', id=quizid))


@app.route("/quizattempt/<int:id>",methods=["GET","POST"])
def quizattempt(id):
    quest=Questions.query.filter_by(q_id=id).all()
    sc=0
    tt=0
    if request.method=="POST":
        session['wa']=[]
        clicked_time = datetime.now().strftime("%H:%M:%S").split(':')
        teme=int(clicked_time[0])*3600+int(clicked_time[1])*60+int(clicked_time[2])
        k=teme-session['tume']
        if Quiz.query.filter_by(id=id).first().time_duration*60>k:
            for i in request.form:
                tt+=1
                if Questions.query.filter_by(id=int(i)).first().cop==int(request.form.get(i)):
                    sc+=1
                else:
                    session['wa'].append(int(i))
            u_id=session.get('id')
            nscore=Scores.query.filter_by(u_id=u_id,q_id=id).first()
            if nscore:
                nscore.score=sc
            else:
                new_score=Scores(u_id=u_id,q_id=id,score=sc)
                db.session.add(new_score)
            session['sc'] = sc
            session['tt'] = tt
            db.session.commit()
            return redirect(url_for("quiz_results"))
        else:
            session['messages']="Time Limit Exceeded"
            return redirect(url_for("user",name=session['user']))
    return render_template("quizattempt.html",questions=quest,q_id=id)

@app.route("/quizresults")
def quiz_results():
    wa_ids = session.pop('wa', [])
    sc = session.pop('sc', 0)
    tt = session.pop('tt', 0)
    wa = Questions.query.filter(Questions.id.in_(wa_ids)).all()
    return render_template("quizresults.html", wa=wa, sc=sc, tt=tt)

@app.route("/allquizres")
def allqres():
    id=session.get('id')
    results=db.session.query(Subject.name, Chapter.name, Quiz.id, Scores.score).join(Chapter, Subject.id==Chapter.s_id).join(Quiz, Quiz.c_id==Chapter.id).join(Scores,Scores.q_id==Quiz.id).filter(Scores.u_id==id).all()
    chart=db.session.query(Chapter.name,Quiz.id,Scores.score).join(Quiz,Chapter.id==Quiz.c_id).join(Scores,Quiz.id==Scores.q_id).filter(Scores.u_id==id).all()
    labels=[]
    scores=[]
    for i in chart:
        labels.append(i[0])
        scores.append(i[2])
    return render_template("quizresults.html",qres=results,labels=labels,scores=scores)

@app.route("/search")
def search():
    message=None
    searchchap=None
    searchsub=None
    searchquestion=None
    searchquiz=None
    searchuser=None
    query = request.args.get('query', '')
    sup=session.get('sup')
    if query!='':
        if sup==1:
            searchsub=Subject.query.filter(Subject.name.ilike("%"+query+"%")).all()
            searchchap=Chapter.query.filter(Chapter.name.ilike("%"+query+"%")).all()
            searchquiz=Quiz.query.filter(Quiz.remarks.ilike("%"+query+"%")).all()
            searchuser=Users.query.filter(Users.f_name.ilike("%"+query+"%")).all()
            searchquestion=Questions.query.filter(Questions.question.ilike("%"+query+"%")).all()
        elif sup==0:
            searchsub=Subject.query.filter(Subject.name.ilike("%"+query+"%")).all()
            searchquiz=Quiz.query.filter(Quiz.remarks.ilike("%"+query+"%")).all()
        else:
            return redirect(url_for("login"))

    if searchsub == None and searchchap==None and searchquestion==None and searchquiz==None and searchuser==None or searchsub == [] and searchchap==[] and searchquestion==[] and searchquiz==[] and searchuser==[]:
        message="Found Nothing"
    return render_template("searchres.html",sub=searchsub,chap=searchchap,message=message,quiz=searchquiz,use=searchuser,question=searchquestion)

@app.route("/adminsummary")
def adminsumm():
    results = db.session.query(Users.f_name, Chapter.name, Quiz.id, Scores.score).join(Scores, Users.id == Scores.u_id).join(Quiz, Scores.q_id == Quiz.id).join(Chapter, Quiz.c_id == Chapter.id).all()
    labels=[]
    scores=[]
    users=[]
    for i in results:
        labels.append(i[0])
        scores.append(i[3])
        users.append(i[1])
    return render_template("adminsumm.html",qres=results,labels=labels,scores=scores,users=users)