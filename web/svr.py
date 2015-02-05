#! /usr/bin/python3

from bottle import get, post, run, request

from db import init_db


@get('/<:re:.*>')
def index():
    return """
        <form action="/" method="post">
            URL: <input name="aviurl" type="text" size=60 />
            <input value="Submit" type="submit" />
        </form>
        """


@post('/')  # or @route('/login', method='POST')
def do_post():
    aviurl = request.forms.get('aviurl')
    fout = open("url_post.txt", "a")
    fout.write(aviurl + "\n")
    fout.close()
    return index() + "<br>got <p>%s</p>" % aviurl


init_db()
#run(host='localhost', port=8080)
run(host='', port=8080)
