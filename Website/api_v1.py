from flask import *
import os

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'

@app.route("/")
def index():
    with open("HTML/index.html") as file:
        html = file.read()
    return html

@app.route("/redirect")
def redirect():
    with open("HTML/redirect.html") as file:
        html = file.read()
    return html

@app.route("/qr")
def qr():
    with open("HTML/qr.html") as file:
        html = file.read()
    return html

@app.route("/api/v1/create")
def create():
    randChar = str(request.args.get('randChar'))
    url = str(request.args.get('url'))

    with open(f"Links/{randChar}.json", "w") as file:
        file.write(json.dumps({"url": url}))
    return url

@app.errorhandler(404)
def not_found(e):
    linkPath = (request.path).split("/")[1] + '.json'
    linksDir = os.listdir("Links")

    for i in linksDir:
        if i == linkPath:
            break
    else:
        return "Can't find url to redirect to!"

    with open(f"Links/{i}", "r") as file:
        url = file.read()
    url = json.loads(url)['url']
    if len(url) == 0:
        return "Can't find url to redirect to!"
    else:
        html = '''<html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=0"><script>function redirect() {window.location.href = '';}</script></head><body onload="redirect()"><div>Redirecting...</div></body></html>'''
        html = html.split("window.location.href = '")
        html = html[0] + "window.location.href = '" + url + html[1]
        return html

if __name__ == "__main__":
    app.run()
