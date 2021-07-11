from flask import Flask, render_template, url_for, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)

bookmarks = []
app.config['SECRET_KEY'] = b"\x1f\xd59d\xfb2N\xc7\x96\x93\xa18#\x99\xe3(\xd4'8%4\x94]Y"

def store_bookmark(url):
    bookmarks.append(dict(
        url = url,
        user = "reindert",
        date = datetime.utcnow()
    ))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Title passed from view to template" ,text=["1", "2"])

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        url = request.form['url']
        store_bookmark(url)
        flash("Stored bookmark '{}'".format(url))
        return redirect(url_for('index'))
    return render_template('add.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
