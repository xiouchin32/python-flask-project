#connect db
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
    return render_template("member.html")

# / error?msg="error message"
@app.route("/error")
def error():
    msg = request.args.get("msg","Error")
    return render_template("error.html",message=msg)


app.run(port=8080)