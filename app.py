import numpy as np
import pandas as pd
import pickle
from flask import Flask, jsonify, render_template, request,redirect,url_for,session,g,flash
from flask_ngrok import run_with_ngrok
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import h5py
from keras.models import load_model
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import pytz
import math

local_tz = pytz.timezone('Asia/Calcutta')

# load the dataset but only keep the top n words, zero the rest
top_words = 10000
max_words = 500

#load the csv file saved

df = pd.read_csv('./data/movie_data.csv', encoding='utf-8')
def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%A %d %B %Y %H:%M:%S')


tokenizer_obj = Tokenizer(num_words=top_words)
tokenizer_obj.fit_on_texts(df.loc[:50000, 'review'].values)

def pred(usermoviereview):
    test_samples = [usermoviereview]
    review_tokens = tokenizer_obj.texts_to_sequences(test_samples)
    review_tokens_pad = pad_sequences(review_tokens, maxlen=max_words)

    print("call predict")
    # Load in pretrained model
    loaded_model = load_model('./models/movie_sa_model.h5')
    print("Loaded model from disk")
    sentiment = loaded_model.predict(x=review_tokens_pad)
    print(sentiment)
    if sentiment[0] > 0.5:
        sentiment_s = float(sentiment[0])
    else:
        sentiment_s = float(sentiment[0])
    return sentiment_s

# webapp
app = Flask(__name__, template_folder='./') 

app.secret_key= 'somesecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'reel2reeal'
app.config['MAIL_PASSWORD'] = 'muskiloveshritik'


db = SQLAlchemy(app)

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.before_request
def before_request():
    if 'user_id' in session:
        user = register.query.filter_by(id=session['user_id']).first()
        g.user = user


run_with_ngrok(app)

@app.route("/delete", methods=["POST"])
def delete():
    if 'sd_rev_id' in request.form :
        rev_id = request.form.get("sd_rev_id")
        del_rev = shakuntala.query.filter_by(sd_id=rev_id).first()
        db.session.delete(del_rev)
        db.session.commit()
        return redirect(url_for('admin'))
    
    if 'ch_rev_id' in request.form :
        rev_id = request.form.get("ch_rev_id")
        del_rev = chhalaang.query.filter_by(ch_id=rev_id).first()
        db.session.delete(del_rev)
        db.session.commit()
        return redirect(url_for('admin')) 
    
    if 'av_rev_id' in request.form :
        rev_id = request.form.get("av_rev_id")
        del_rev = avengers.query.filter_by(av_id=rev_id).first()
        db.session.delete(del_rev)
        db.session.commit()
        return redirect(url_for('admin'))
    
    if 'hp_rev_id' in request.form :
        rev_id = request.form.get("hp_rev_id")
        del_rev = harry.query.filter_by(hp_id=rev_id).first()
        db.session.delete(del_rev)
        db.session.commit()
        return redirect(url_for('admin'))
    
    if 'lx_rev_id' in request.form :
        rev_id = request.form.get("lx_rev_id")
        del_rev = laxmii.query.filter_by(lx_id=rev_id).first()
        db.session.delete(del_rev)
        db.session.commit()
        return redirect(url_for('admin'))

class shakuntala(db.Model):
    sd_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))
    user_id = db.Column(db.Integer, db.ForeignKey('register.id'))

class chhalaang(db.Model):
    ch_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))
    user_id = db.Column(db.Integer, db.ForeignKey('register.id'))

class harry(db.Model):
    hp_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))
    user_id = db.Column(db.Integer, db.ForeignKey('register.id'))

class avengers(db.Model):
    av_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Integer)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))
    user_id = db.Column(db.Integer, db.ForeignKey('register.id'))

class laxmii(db.Model):
    lx_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    review = db.Column(db.String(500))
    percent = db.Column(db.Float)
    date_entered = db.Column(db.String, default=aslocaltimestr(datetime.now()))
    user_id = db.Column(db.Integer, db.ForeignKey('register.id'))

def shakuntala_rev(request):
    sentiment_s = pred(str(request.form['message']))
    register = g.user
    rev = shakuntala(name=register.username, review=request.form['message'], percent=sentiment_s,user_id=register.id)
    db.session.add(rev)
    db.session.commit()


def hp_rev(request):
    sentiment_s = pred(request.form['message'])
    register = g.user
    rev = harry(name=register.username, review=request.form['message'], percent=sentiment_s,user_id=register.id)
    db.session.add(rev)
    db.session.commit()


def avengers_rev(request):
    sentiment_s = pred(request.form['message'])
    register = g.user
    rev = avengers(name=register.username, review=request.form['message'], percent=sentiment_s,user_id=register.id)
    db.session.add(rev)
    db.session.commit()


def laxmii_rev(request):
    sentiment_s = pred(request.form['message'])
    register = g.user
    rev = laxmii(name=register.username, review=request.form['message'], percent=sentiment_s,user_id=register.id)
    db.session.add(rev)
    db.session.commit()



def chhalaang_rev(request):
    sentiment_s = pred(request.form['message'])
    register = g.user
    rev = chhalaang(name=register.username, review=request.form['message'], percent=sentiment_s,user_id=register.id)
    db.session.add(rev)
    db.session.commit()

#login form----------------------------------->


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['name']=='' and request.form['email']=='':
            return render_template("login.html",message='Please enter a username or email')
        if request.form['password'] == '':
            return render_template("login.html",message='Please enter your password')

        if request.form['name'] == 'Admin' or request.form['email'] == 'admin@blockbuster.in':
            if request.form['password'] == '@dmin':
                return redirect(url_for('admin'))

        if request.form['name'] != '':
            user_name = register.query.filter_by(username=request.form['name']).first()
            if user_name:
                if request.form['password'] == user_name.password:
                    session['user_id'] = user_name.id
                    return redirect(url_for('dashboard'))
        
        if request.form['email'] != '':
            user_email = register.query.filter_by(email=request.form['email']).first()
            if user_email:
                if request.form['password'] == user_email.password:
                    session['user_id'] = user_email.id
                    return redirect(url_for('dashboard'))
        
        return render_template("login.html", message='Incorrect Password!')
        
    return render_template("login.html", message='')

#signup form-------------------------------->

class register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    review_sd = db.relationship('shakuntala',backref='register',uselist=False)
    review_hp = db.relationship('harry',backref='register',uselist=False)
    review_av = db.relationship('avengers',backref='register',uselist=False)
    review_ch = db.relationship('chhalaang',backref='register',uselist=False)
    review_lx = db.relationship('laxmii',backref='register',uselist=False)
    


message_list = {}

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        message_list = {}
        count = 0
        test_str = ''
        usrname = request.form['name']
        if usrname == test_str or usrname.strip() == test_str:
            message_list["no_usr"] = "Please enter a username"
            count += 1
        if len(usrname) > 30:
            message_list["long_name"] = "Max 30 characters"
            count += 1

        email = request.form['email']
        if email == test_str or email.strip() == test_str:
            message_list["no_email"] = "Please enter an email"
            count += 1
        if register.query.filter_by(email=email).first():
            message_list["email_exits"] = "This email is  already registered"
            count += 1
        if len(email) > 40:
            message_list["long_email"] = "Max 40 characters"
            count += 1
        password = request.form['password']
        if ('' and password.strip()):
            message_list["no_pass"] = "Please add a password"
            count += 1
        if len(password) > 20:
            message_list["long_pass"] = "Max 20 characters"
            count += 1
        if count == 0:
            usr = register(username=usrname, email=email, password=password)
            db.session.add(usr)
            db.session.commit()
            message_list["success"] ="Registration Successful!"
        else: 
            message_list["fail"] = "User didn't register"

        return render_template("signup.html", message_list=message_list)
        
    return render_template("signup.html", message_list={})


@app.route('/admin', methods=['GET'])
def admin() :
    all_users = register.query.all()
    sd_revs = shakuntala.query.all()
    ch_revs = chhalaang.query.all()
    av_revs = avengers.query.all()
    hp_revs = harry.query.all()
    lx_revs = laxmii.query.all()
    return render_template('admin.html', all_users=all_users,sd_revs=sd_revs,ch_revs=ch_revs,av_revs=av_revs,hp_revs=hp_revs,lx_revs=lx_revs)

def truncate(number) -> float:
    stepper = 10
    return math.trunc(stepper * number) / stepper

@app.route('/', methods=['GET','POST'])
def main():
    
    avg_sd = 0
    avg_ch = 0
    avg_hp = 0
    avg_av = 0
    avg_lx = 0
    sdf = shakuntala.query.all()
    count = 0
    for q in sdf:
        avg_sd += q.percent
        count += 1
    if count != 0:
        avg_sd /= count
        avg_sd *= 10

    sdf2 = chhalaang.query.all()
    count = 0
    for q in sdf2:
        avg_ch += q.percent
        count += 1
    if count != 0:
        avg_ch /= count
        avg_ch *= 10

    sdf3 = avengers.query.all()
    count = 0
    for q in sdf3:
        avg_av += q.percent
        count += 1
    if count != 0:
        avg_av /= count
        avg_av *= 10

    sdf4 = harry.query.all()
    count = 0
    for q in sdf4:
        avg_hp += q.percent
        count += 1
    if count != 0:
        avg_hp /= count
        avg_hp *= 10

    sdf5 = laxmii.query.all()
    count = 0
    for q in sdf5:
        avg_lx += q.percent
        count += 1
    if count != 0:
        avg_lx /= count
        avg_lx *= 10
    
    avg_sd = truncate(avg_sd)
    avg_ch = truncate(avg_ch)
    avg_av = truncate(avg_av)
    avg_hp = truncate(avg_hp)
    avg_lx = truncate(avg_lx)

    avg_sd_int = int(avg_sd)
    avg_ch_int = int(avg_ch)
    avg_av_int = int(avg_av)
    avg_hp_int = int(avg_hp)
    avg_lx_int = int(avg_lx)
    
    count_sd = shakuntala.query.count()
    count_ch = chhalaang.query.count()
    count_av = avengers.query.count()
    count_hp = harry.query.count()
    count_lx = laxmii.query.count()
    return render_template('home1.html',revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5, avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int,count_sd=count_sd,count_ch=count_ch,count_av=count_av,count_hp=count_hp,count_lx=count_lx)


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    
    avg_sd = 0
    avg_ch = 0
    avg_hp = 0
    avg_av = 0
    avg_lx = 0
    # count_sd = 0
    # count_ch = 0
    # count_av = 0
    # count_hp = 0
    # count_lx = 0
    sdf = shakuntala.query.all()
    count = 0
    for q in sdf:
        avg_sd += q.percent
        count += 1
    if count != 0:
        avg_sd /= count
        avg_sd *= 10

    sdf2 = chhalaang.query.all()
    count = 0
    for q in sdf2:
        avg_ch += q.percent
        count += 1
    if count != 0:
        avg_ch /= count
        avg_ch *= 10

    sdf3 = avengers.query.all()
    count = 0
    for q in sdf3:
        avg_av += q.percent
        count += 1
    if count != 0:
        avg_av /= count
        avg_av *= 10

    sdf4 = harry.query.all()
    count = 0
    for q in sdf4:
        avg_hp += q.percent
        count += 1
    if count != 0:
        avg_hp /= count
        avg_hp *= 10

    sdf5 = laxmii.query.all()
    count = 0
    for q in sdf5:
        avg_lx += q.percent
        count += 1
    if count != 0:
        avg_lx /= count
        avg_lx *= 10
    
    avg_sd = truncate(avg_sd)
    avg_ch = truncate(avg_ch)
    avg_av = truncate(avg_av)
    avg_hp = truncate(avg_hp)
    avg_lx = truncate(avg_lx)

    avg_sd_int = int(avg_sd)
    avg_ch_int = int(avg_ch)
    avg_av_int = int(avg_av)
    avg_hp_int = int(avg_hp)
    avg_lx_int = int(avg_lx)

    count_sd = shakuntala.query.count()
    count_ch = chhalaang.query.count()
    count_av = avengers.query.count()
    count_hp = harry.query.count()
    count_lx = laxmii.query.count()

    if request.method == "POST":
        if 'user_id' not in session and request.form['message'] == '':
            return redirect(url_for('dashboard'))
        sdf = shakuntala.query.all()
        count = 0
        avg_sd = 0
        for q in sdf:
            avg_sd += q.percent
            count += 1
        if count != 0:
            avg_sd /= count
            avg_sd *= 10

        sdf2 = chhalaang.query.all()
        count = 0
        avg_ch = 0

        for q in sdf2:
            avg_ch += q.percent
            count += 1
        if count != 0:
            avg_ch /= count
            avg_ch *= 10

        sdf3 = avengers.query.all()
        count = 0
        avg_av = 0
        for q in sdf3:
            avg_av += q.percent
            count += 1
        if count != 0:
            avg_av /= count
            avg_av *= 10

        sdf4 = harry.query.all()
        count = 0
        avg_hp = 0
        for q in sdf4:
            avg_hp += q.percent
            count += 1
        if count != 0:
            avg_hp /= count
            avg_hp *= 10

        sdf5 = laxmii.query.all()
        count = 0
        avg_lx = 0
        for q in sdf5:
            avg_lx += q.percent
            count += 1
        if count != 0:
            avg_lx /= count
            avg_lx *= 10
        
        avg_sd = truncate(avg_sd)
        avg_ch = truncate(avg_ch)
        avg_av = truncate(avg_av)
        avg_hp = truncate(avg_hp)
        avg_lx = truncate(avg_lx)

        avg_sd_int = int(avg_sd)
        avg_ch_int = int(avg_ch)
        avg_av_int = int(avg_av)
        avg_hp_int = int(avg_hp)
        avg_lx_int = int(avg_lx)

        count_sd = shakuntala.query.count()
        count_ch = chhalaang.query.count()
        count_av = avengers.query.count()
        count_hp = harry.query.count()
        count_lx = laxmii.query.count()
        if 'sd' in request.form:
            shakuntala_rev(request)

            sdf = shakuntala.query.all()
            count = 0
            avg_sd = 0
            for q in sdf:
                avg_sd += q.percent
                count += 1
            if count != 0:
                avg_sd /= count
                avg_sd *= 10


            avg_sd = truncate(avg_sd)
            avg_sd_int = int(avg_sd)
            count_sd = shakuntala.query.count()

            return render_template("home.html", revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int,count_sd=count_sd,count_ch=count_ch,count_av=count_av,count_hp=count_hp,count_lx=count_lx)
        if 'hp' in request.form:
            hp_rev(request)
            sdf4 = harry.query.all()
            count = 0
            avg_hp = 0
            for q in sdf4:
                avg_hp += q.percent
                count += 1
            if count != 0:
                avg_hp /= count
                avg_hp *= 10

            avg_hp = truncate(avg_hp)
            
            avg_hp_int = int(avg_hp)
            count_hp = harry.query.count()
            return render_template("home.html",revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int,count_sd=count_sd,count_ch=count_ch,count_av=count_av,count_hp=count_hp,count_lx=count_lx)
        if 'av' in request.form:
            avengers_rev(request)

            sdf3 = avengers.query.all()
            count = 0
            avg_av = 0
            for q in sdf3:
                avg_av += q.percent
                count += 1
            if count != 0:
                avg_av /= count
                avg_av *= 10


            avg_av = truncate(avg_av)
            avg_av_int = int(avg_av)
            count_av = avengers.query.count()
            return render_template("home.html", revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int,count_sd=count_sd,count_ch=count_ch,count_av=count_av,count_hp=count_hp,count_lx=count_lx)
        if 'ch' in request.form:
            chhalaang_rev(request)
            sdf2 = chhalaang.query.all()
            count = 0
            avg_ch = 0
            for q in sdf2:
                avg_ch += q.percent
                count += 1
            if count != 0:
                avg_ch /= count
                avg_ch *= 10

            avg_ch = truncate(avg_ch)
            avg_ch_int = int(avg_ch)
            count_ch = chhalaang.query.count()
            
            return render_template("home.html", revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int,count_sd=count_sd,count_ch=count_ch,count_av=count_av,count_hp=count_hp,count_lx=count_lx)
        if 'laxmii' in request.form:
            laxmii_rev(request)

            sdf5 = laxmii.query.all()
            count = 0
            avg_lx = 0
            for q in sdf5:
                avg_lx += q.percent
                count += 1
            if count != 0:
                avg_lx /= count
                avg_lx *= 10

            avg_lx = truncate(avg_lx)
            avg_lx_int = int(avg_lx)
            count_lx = laxmii.query.count()
            return render_template("home.html",revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5,avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int,count_sd=count_sd,count_ch=count_ch,count_av=count_av,count_hp=count_hp,count_lx=count_lx)
    
    return render_template('home.html',revs1=sdf, revs2=sdf2, revs3=sdf3, revs4=sdf4, revs5=sdf5, avg_sd=avg_sd, avg_av=avg_av, avg_ch=avg_ch, avg_hp=avg_hp, avg_lx=avg_lx,avg_sd_int=avg_sd_int,avg_ch_int=avg_ch_int,avg_av_int=avg_av_int,avg_hp_int=avg_hp_int,avg_lx_int=avg_lx_int,count_sd=count_sd,count_ch=count_ch,count_av=count_av,count_hp=count_hp,count_lx=count_lx)


@app.route('/forgot-password', methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        user = register.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='email-confirm')

            msg = Message('Click on this link to reset your password ', sender='reel2reeal@gmail.com', recipients=[email])

            link = url_for('change_password', token=token, _external=True)

            msg.body = ' link : {}'.format(link)

            mail.send(msg)
            flash('A link has been sent to the specified email. Please Check!', 'info')
            return redirect(url_for('forgot'))
        flash('This email id is not registered')
        return redirect(url_for('forgot'))
    return render_template("forgot.html")

@app.route('/change_password/<token>', methods=['GET',"POST"])
def change_password(token):
    if request.method == 'POST':
        try:
            email = s.loads(token, salt='email-confirm', max_age=3600)
            user = register.query.filter_by(email=email).first()
            if request.form['password'] != request.form['confirm_password']:
                flash('Passwords do not match')
                return redirect(url_for('change_password',token=token))
            
            if request.form['password'] == user.password:
                flash('Choose a different password')
                return redirect(url_for('change_password',token=token))
            user.password = request.form['password']
            db.session.commit()
            flash('Password has been changed successfully!')
            flash('login to continue.')
            return redirect(url_for('login'))
        except SignatureExpired:
            return '<h1>The token is expired!</h1>'
    else:
        return render_template('change.html')

if __name__ == '__main__':
    app.run()
