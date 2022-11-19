from flask import *
from flask import Flask, render_template
from urllib3 import *
import requests
from bs4 import BeautifulSoup
import re
import pymongo


app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def search_box():
    if request.method == "POST":
        searchstring = request.form["content"].replace(" ","")
        try:
            dbconn = pymongo.MongoClient("mongodb://localhost:27017/")
            db = dbconn["Scrapper-macbook"]
            reviews = db[searchstring]
        except:
            return "somethiing is wrong"
    else:
        return render_template("Layout.html")

if __name__ == "__main__":
    app.run(debug = True)