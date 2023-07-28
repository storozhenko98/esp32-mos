from microdot import send_file, Microdot, Response
import ujson
import os
#boot stuff
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
#init microdot
app = Microdot()
#home page
@app.route('/')           
def index(request):
    return send_file('./pages/home.html')
#APIs
@app.route('/api/<path>')
def api(request, path):
    if path == "editor":
        return "/pages/editor.html"  # Return the URL to the HTML page instead of the file content
    if path == "fileBrowser":
        return "/pages/fileBrowser.html"
#assets
@app.route('/assets/<path>')
def assets(request, path):
    return send_file('./assets/' + path)
#pages
@app.route('/pages/<path>')
def pages(request, path):
    return send_file('./pages/' + path)
#IDE & Executing Code on Device
@app.route('ide/save', methods=['POST'])
def save(request):
    print(request.json)
    name = request.json['name']
    code = request.json['code']
    # save code to file using name constant as name 
    with open('./programs/' + name + '.py', 'w') as f:
        f.write(code)
    return Response('OK')
##fetching code from device
@app.route('/programs')
def programs(request):
    # Create list of files
    files = [{"name": f, "path": './programs/' + f} for f in os.listdir('./programs') if f.endswith('.py')]
    print('Array of files: ' + str(files) + '\n')
    
    # Convert list of files to JSON
    files_json = ujson.dumps(files)
    print('JSON of files: ' + str(files_json) + '\n')
    
    return Response(files_json, headers={'Content-Type': 'application/json'})

##running code on device
@app.route('/run', methods=['POST'])
def run(request):
    print(request.json)
    path = request.json['path']
    # Read and execute the Python file
    with open(path, 'r') as f:
        code = f.read()
        exec(code)
    return Response('OK')



app.run()
