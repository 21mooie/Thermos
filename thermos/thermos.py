from flask import Flask, render_template, url_for, request, redirect, url_for, flash
from datetime import datetime

from forms import BookmarkForms

app = Flask(__name__)

bookmarks = []
app.config['SECRET_KEY'] = b"\x1f\xd59d\xfb2N\xc7\x96\x93\xa18#\x99\xe3(\xd4'8%4\x94]Y"

def store_bookmark(url, description):
    bookmarks.append(dict(
        url = url,
        user = "muata",
        description = description,
        date = datetime.utcnow()
    ))

def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
    new_bookmarks=new_bookmarks(5)
    )

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForms()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmark(url, description)
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
