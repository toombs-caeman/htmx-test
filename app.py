# Flask app.py
import sqlite3
from flask import Flask, redirect, render_template, request, url_for

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

def paginate(item_format, sql, *params):
    """Shorthand for paginated query"""
    sql += ' limit ? offset ?'
    limit = request.args.get('limit', '100')
    offset = request.args.get('offset', '0')
    params += limit, offset
    data = q(sql, *params, dict=True).fetchall()
    result = ''.join(
        item_format(**row) for row in data
    )
    if len(data) == int(limit):
        result += more(url_for(request.endpoint, offset=data[-1][0]))
    return result

def more(url, tag='tr'):
    """scroll trigger"""
    return f"""<{tag} hx-get="{url}" hx-trigger="revealed" hx-swap="outerHTML"></{tag}>"""

@app.route("/")
def index():
    return render("index")

@app.route("/tracks")
def tracks():
    if not htmx:
        return render('tracks')
    return paginate(track,
        'select TrackId as id from tracks order by TrackId'
    )

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

@app.route("/artists")
def artists():
    if not htmx:
        return render('artists')
    return paginate(
        artist,
        'select ArtistId as id from artists order by ArtistId'
    )

@app.route("/artist/<id>")
def artist(id):
    return render('artist', **q(
        "select ArtistId, Name from artists where ArtistId = ?",
        id,
        dict=True
    ).fetchone())

@app.route("/artist/<id>/tracks")
def tracksByArtist(id):
    if not htmx:
        redirect(url_for('artist', id=id))

    return paginate(
        lambda **r:render('track', **r),
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
                where b.ArtistId = ?
                """,
        id,
    )

