from flask import Flask, render_template, redirect, url_for, request, redirect
import flask
from pymongo import MongoClient
import pymongo
import requests

client = pymongo.MongoClient("mongodb+srv://satish_kumar:B01eLT0oS2PpnTso@cluster0.s71eb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
dbname = client['Movlib']
user_details = dbname["user"]
list_details=dbname["movlist"]

loggeduser=''
search=''


app = Flask(__name__)
app.config['SECRET_KEY'] = 'C8HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

@app.route('/', methods=['GET', 'POST'])
def login():
    global loggeduser
    loggeduser=''
    return render_template('index.html' ,wro="")

@app.route('/login', methods=['GET', 'POST'])
def login_check():
    us=request.form['email']
    pas=request.form['password']
    query = user_details.find_one({'email':us,'pass':pas})
    if query==None:
        wro="Wrong details try again"
        return render_template('index.html',wro=wro)
    else:
        global loggeduser
        loggeduser=query['email']
        return flask.redirect('/home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    #for retriving logged user list
    query = list_details.find({'user_id':loggeduser})
    count=len(list(query))
    playlist=list()
    for document in query:
        playlist.append(document['playlist'])
    x=set(playlist)
    pli=list(x)
    p=len(pli)
    if p>3:
        p=3
    movlist=list()
    for i in pli:
        temp=[]
        query = list_details.find({'playlist':i},{'movie':1})
        apiKey = '60eaea0b'
        data_URL = 'http://www.omdbapi.com/?apikey='+apiKey
        for j in query:
            params = {'i':j['movie'] }
            response = requests.get(data_URL,params=params).json()
            temp.append([response['Title'],response['Poster']])
        movlist.append(temp)
    
    #for retriving other user public list
    query2 = list_details.find({"$and": [{"scope": 'public'},{'user_id':{'$ne':'suresh@gmail.com'}} ]})
    count2=len(list(query2))
    oplaylist=list()
    for document in query2:
        oplaylist.append(document['playlist'])
    x=set(oplaylist)
    opli=list(x)
    op=len(opli)
    if op>3:
        op=3
    omovlist=list()
    for i in opli:
        temp=[]
        query2 = list_details.find({'playlist':i},{'movie':1})
        apiKey = '60eaea0b'
        data_URL = 'http://www.omdbapi.com/?apikey='+apiKey
        for j in query2:
            params = {'i':j['movie'] }
            response = requests.get(data_URL,params=params).json()
            temp.append([response['Title'],response['Poster']])
        omovlist.append(temp)

    return render_template('home.html', plist=pli,mlist=movlist,pn=count,plen=p,oplist=opli,omlist=omovlist,opn=count2,oplen=op)

@app.route('/register', methods=['GET', 'POST'])
def register():
    na=request.form['fullname']
    us=request.form['email']
    ph=request.form['phone']
    pas=request.form['pass']
    queryObject = {
        'name': na,
        'email': us,
        'phone':ph,
        'pass':pas
    }
    try:
        query = user_details.insert_one(queryObject)
        return render_template('index.html',wro="Successfully registered")
    except:
        return render_template('signup.html',wro="Something went wrong")

@app.route('/search', methods=['GET', 'POST'])
def search():
    sa=request.form['search']
    global search
    search=sa
    apiKey = '60eaea0b'
    data_URL = 'http://www.omdbapi.com/?apikey='+apiKey
    year = ''
    movieTitle = sa
    params = {
    's':movieTitle,
    'type':'movie',
    'y':year    
    }
    res=[]
    try:
        response = requests.get(data_URL,params=params).json()
        res=response['Search']
        count=len(res)
        return render_template('search.html',mlist=res,resnum=count)
    except:
        count=0
        return render_template('search.html',mlist=res,resnum=count)

@app.route('/info', methods=['GET', 'POST'])
def add_list():
    sa=request.form['submit']
    apiKey = '60eaea0b'
    data_URL = 'http://www.omdbapi.com/?apikey='+apiKey
    params = {
    'i':sa   
    }
    res=[]
    res = requests.get(data_URL,params=params).json()
    return render_template('add_list.html',minfo=res,wro='')

@app.route('/result', methods=['GET', 'POST'])
def add_success():
    mid=request.form['submit']
    scope=request.form['scope']
    lnamee=request.form['listname']
    queryObject = {
        'user_id': loggeduser,
        'playlist': lnamee,
        'scope':scope,
        'movie':mid
    }
    try:
        query = list_details.insert_one(queryObject)
        return flask.redirect('/home')
    except:
        return render_template('add_list.html',wro="Something went wrong")
    


if __name__ == '__main__':
    app.run(debug=True)