import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('arvoitus.html')


@app.route('/team/', methods=['GET'])
def team():
    return render_template('team.html')

app.secret_key = 'super secret'
app.run()
