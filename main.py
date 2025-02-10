from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')


@app.route('/')
def hello():
    return render_template('home.html')


#TODO
# Database - when will be some data to be stored
# UI - acording to app progress
# Scraping - NOW
# AI with Pytorch - Last Step
