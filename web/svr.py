#! /usr/bin/python3

from bottle import get, post, run, request

from db import init_db, add_one_url


@get('/<:re:.*>')
def index():
    return """
        <form action="/" method="post">
            URL: <input name="aviurl" type="text" size=60 /><br>
            TITLE: <input name="avitil" type="text" size=60 />
            <input value="Submit" type="submit" />
        </form>
        """


@post('/')  # or @route('/login', method='POST')
def do_post():
    aviurl = request.forms.get('aviurl')
    avitil = request.forms.get('avitil')
    add_one_url(aviurl, avitil)
    #fout = open("url_post.txt", "a")
    #fout.write(aviurl + "\n")
    #fout.close()
    return index() + ("<br>got<p>%s<br>%s</p>" % (avitil, aviurl))


init_db()
#run(host='localhost', port=8080)
run(host='', port=8080)
