from microdot import send_file, Microdot, Response
import ujson

settings = {}
#read json using ujson 
with open('settings.json') as f:
    settings = ujson.load(f)

# check if initial boot
if settings['initial_boot']:
    # do initial boot stuff
    pass
if not settings['initial_boot']:
    # do normal boot stuff
    pass

app = Microdot()

@app.route('/')           
def index(request):
    return send_file('./pages/home.html')

@app.route('/api/<path>')
def api(request, path):
    if path == "editor":
        return "/pages/editor.html"  # Return the URL to the HTML page instead of the file content

@app.route('/assets/<path>')
def assets(request, path):
    return send_file('./assets/' + path)

@app.route('/pages/<path>')
def pages(request, path):
    return send_file('./pages/' + path)

@app.route('ide/save', methods=['POST'])
def save(request):
    print(request.json)
    name = request.json['name']
    code = request.json['code']
    # save code to file using name constant as name 
    with open(name + '.py', 'w') as f:
        f.write(code)
    return Response('OK')


app.run()
