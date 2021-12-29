#connect db
import re
from typing import Collection
import pymongo
client = pymongo.MongoClient("mongodb+srv://root:root123@mycluster.j1zwl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.member_system
print("Connect Success!!")

from flask import *
app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key="123456"

#route
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html")
    else :
        return redirect("/")

# / error?msg="error message"
@app.route("/error")
def error():
    msg = request.args.get("msg","Error")
    return render_template("error.html",message=msg)

@app.route("/signup",methods=["POST"])
def signup():
    #get info
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    #check info
    colletion = db.user
    result = colletion.find_one({
        "email":email
    })
    if result!=None:
        return redirect("/error?msg=Email already exists.")
        # return Response({"text":"Email already exists."}, status=409, mimetype='application/json')
    #post data
    colletion.insert_one({
        "nickname":nickname,
        "email":email,
        "password":password
    })
    return redirect("/")

@app.route("/signin",methods=["POST"])
def signin():
    #get input email and password
    email = request.form["email"]
    password = request.form["password"]
    #check user
    colletion = db.user
    #check password
    result = colletion.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    if result == None:
        return redirect("/error?msg=Login Failed.")
    session["nickname"] = result["nickname"]
    return redirect("/member") 

@app.route("/signout")
def signout():
    del session["nickname"]
    return redirect("/")

app.run(port=8080)