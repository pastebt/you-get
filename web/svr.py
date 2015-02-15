#! /usr/bin/python3

from bottle import get, post, request
from bottle import run, template, route, redirect
from bottle import static_file

from db import init_db, add_one_url, query_urls, set_flag
from dwn import Manager


def html_head():
    return """
        <html>
        <head><title>You_Get</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf8">
        </head>
        <body>
        """


def html_foot():
    return "</body></html>"


def html_form():
    return """
        <form action="/" method="post">
        <table>
            <tr><td>URL:</td>
                <td><input name="aviurl" type="text" size=60 /></td>
            </tr>
            <tr><td>TITLE:</td>
                <td><input name="avitil" type="text" size=60 /></td>
            </tr>
            <tr><td> </td><td><input value="Submit" type="submit" /></td>
            </tr>
        </table>
        </form>
        """


def html_list():
    return template("""
        <% from db import STOP, WAIT, WORK, FAIL, DONE %>
        %if urls:
        <table border=1>
        <thead><tr>
            <td>Title</td>
            <td>add date</td>
            <td>url</td>
            <td>flag</td>
        <tr></thead>
        <tbody>
        %for url in urls:
            <tr>
                <td>{{url.name}}</td>
                <td>{{url.updt}}</td>
                <td>{{url.url}}</td>
                <td>\\\\
                    %if url.flag is None or url.flag == STOP:
"""                  """<a href=/rest?mid={{url.rowid}}&act=start>start</a>\\\\
                    %elif url.flag == WAIT:
"""                  """waiting\\\\
                    %elif url.flag == WORK:
"""                  """<a href=/rest?mid={{url.rowid}}&act=start>working</a>\\\\
                    %elif url.flag == FAIL:
"""                  """<a href=/rest?mid={{url.rowid}}&act=start>retry</a>\\\\
                    %elif url.flag == DONE:
"""                  """<a href=/movies/{{url.rowid}}>Done</a>\\\\
                    %else:
"""                  """FF\\\\
                    %end
"""          """</td>
            </tr>
        %end
        </tbody>
        </table>
        %end
        """, urls=query_urls())


def conv(src):
    return [ord(x) for x in src]


@route('/movies/<mid>')
def server_static(mid):
    return static_file(filename, root='/path/to/your/static/files')


@get('/rest')
def rest():
    mid = request.query.mid
    act = request.query.act
    print("rest: mid=%s, act=%s" % (mid, act))
    if act in ("start",):
        set_flag(mid, act)
        mon.s2m.put(mid)
    redirect("/")


@get('/<:re:.*>')
def index():
    return html_head() + html_form() + html_list() + html_foot()


@post('/')  # or @route('/login', method='POST')
def do_post():
    aviurl = request.forms.get('aviurl')
    rtitle = request.forms.get('avitil')
    avitil = bytearray(conv(rtitle)).decode("utf8")

    add_one_url(aviurl, avitil)
    #fout = open("url_post.txt", "a")
    #fout.write(aviurl + "\n")
    #fout.close()
    body = template('Got:<br>Title: {{title}}<br>URL:{{url}}',
                    title=avitil, url=aviurl)
    return html_head() + body + html_form() + html_list() + html_foot()


init_db()
mon = Manager()
mon.start()
#mon.s2m.put(1)   start 
#run(host='localhost', port=8080)
run(host='', port=8080)
mon.s2m.put(None)
