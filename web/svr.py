#! /usr/bin/python3

from bottle import get, post, run, request

from db import init_db, add_one_url


def html_head():
    return """
        <html>
        <head><title>You-Get</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf8">
        </head>
        <body>
        """


def html_foot():
    return "</body></html>"


def html_form():
    return """
        <form action="/" method="post">
            URL: <input name="aviurl" type="text" size=60 /><br>
            TITLE: <input name="avitil" type="text" size=60 />
            <input value="Submit" type="submit" />
        </form>
        """


@get('/<:re:.*>')
def index():
    return html_head() + html_form() + html_foot()


@post('/')  # or @route('/login', method='POST')
def do_post():
    aviurl = request.forms.get('aviurl')
    avitil = request.forms.get('avitil')
    print(avitil)
    add_one_url(aviurl, avitil)
    #fout = open("url_post.txt", "a")
    #fout.write(aviurl + "\n")
    #fout.close()
    return html_head() + index() + (
           "<br>got<p>%s<br>%s</p>" % (avitil, aviurl)) + html_foot()


init_db()
#run(host='localhost', port=8080)
run(host='', port=8080)
