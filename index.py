#!/usr/bin/env python

from flask import (Flask, request, Response, render_template, 
        redirect, url_for)
from flask.ext.pymongo import PyMongo


from config import config
from formbuilder import formLoader
import json

app = Flask(__name__, static_folder='src')
app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT=27017,
    MONGO_USERNAME='formbase',
    MONGO_PASSWORD='111111',
    MONGO_DBNAME='flask'
)

mongo = PyMongo(app)

app.secret_key = 'Sh3r1n4Mun4F'
mysession = {}
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    #print 'save called'
    if request.method == 'POST':
        formData = request.form.get('formData')

        if formData == 'None':
            return 'Error processing request'

        mysession['form_data'] = formData
        # print formData
        formDict = json.loads(formData)
        mongo.db.form.insert_one(formDict)
        return 'OK'

@app.route('/render')
def render():
    print 'render directed'
    if not mysession.get('form_data'):
        return redirect('/')

    form_data = mysession.get('form_data')
    mysession['form_data'] = None

    form_loader = formLoader(form_data, url_for('submit'))
    render_form = form_loader.render_form()

    return render_template('render.html', render_form=render_form)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        form = json.dumps(request.form)

        return form

if __name__ == '__main__':
    app.debug = True
    app.run()
