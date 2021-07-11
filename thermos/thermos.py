import os
from flask import Flask, render_template, url_for, request, redirect, url_for, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from forms import BookmarkForms
import models

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

bookmarks = []
app.config['SECRET_KEY'] = b"\x1f\xd59d\xfb2N\xc7\x96\x93\xa18#\x99\xe3(\xd4'8%4\x94]Y"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
db = SQLAlchemy(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
    new_bookmarks=models.Bookmark.newest(5)
    )

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForms()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = models.Bookmark(url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
