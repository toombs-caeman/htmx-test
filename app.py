# Flask app.py
import sqlite3
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

# replaces flask-htmx extension
htmx = type('',(), {
    '__bool__': lambda _: ('hx-request' in request.headers)
})()

def render(name, *args, **kwargs):
    """
    render an html or htmx template depending on context
    """
    template = f"{name}.htm{'x' if htmx else 'l'}"
    return render_template(template, *args, **kwargs)

def DB(dict=False):
    db = sqlite3.connect("chinook.db")
    if dict:
        db.row_factory = sqlite3.Row
    return db


def q(sql, *params, dict=False):
    """Shorthand query function"""
    with DB(dict) as db:
        return db.execute(sql, params)

def paginate(sql, *params, dict=False):
    """Shorthand for paginated query"""
    sql += ' limit ? offset ?'
    limit = request.args.get('limit', '100')
    offset = request.args.get('offset', '0')
    params += limit, offset
    return q(sql, *params, dict=dict)

@app.route("/")
def index():
    return render("index")

@app.route("/tracks")
def tracks():
    if not htmx:
        return render('tracks')
    data = paginate(
        'select TrackId from tracks order by TrackId'
    ).fetchall()
    result = ''.join(track(id) for (id,) in data)
    # if we haven't reached the end, then put another trigger to keep loading results
    if len(data) == int(request.args.get('limit', '100')):
        result += f"""<tr hx-get="/tracks?offset={data[-1][0]}" hx-trigger="revealed" hx-swap="outerHTML"> <td>loading...</td> </tr>"""
    return result



@app.route("/track/<id>")
def track(id):
    return render('track', **q(
        """select
                TrackId,
                b.AlbumId,
                b.ArtistId,
                t.Name as track,
                b.Title as album,
                a.Name as artist
                from tracks as t
                join albums as b on t.AlbumId = b.AlbumId
                join artists as a on b.ArtistID = a.ArtistId
                where t.TrackId = ?
                """,
        id,
        dict=True
    ).fetchone())


@app.route("/artist/<id>")
def artist(id):
    return render('artist', **q(
        "select Name from artists where ArtistId = ?",
        id,
        dict=True
    ).fetchone())

@app.route("/artist/<id>/tracks")
def tracksByArtist(id):
    return render('artist', **q(
        "select Name from artists where ArtistId = ?",
        id,
        dict=True
    ).fetchone())

@app.route("/artists")
def artists():
    return render('artists')
