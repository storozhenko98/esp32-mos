from microdot import send_file, Microdot, Response
import ujson
import os
import network 
import machine

#boot stuff
settings = {}
#read json using ujson 
with open('settings.json') as f:
    settings = ujson.load(f)

####\/\/\/\/\/\/\/#####BOOT#####
#set up wifi
if settings['initial_boot'] == True:
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='MyESP32AP', password='mysecretpassword')
    print('network config:', ap.ifconfig())
    print('remember to put ip followed by port, mine was port :5000')

if settings['initial_boot'] == False:
    ssid = settings['ssid']
    wifi_password = settings['wifi_password']
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, wifi_password)
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())
    print('remember to put ip followed by port, mine was port :5000')

###^^^^^^#####
#init microdot
app = Microdot()
#home page
@app.route('/')           
def index(request):
    if settings['initial_boot'] == True:
        return send_file('./pages/settings.html')
    else:
        return send_file('./pages/home.html')
#APIs
@app.route('/api/<path>')
def api(request, path):
    if path == "editor":
        return "/pages/editor.html"  # Return the URL to the HTML page instead of the file content
    if path == "fileBrowser":
        return "/pages/fileBrowser.html"
    if path == "hypercard":
        return "/pages/hypercard.html"
    if path == "settings":
        return "/pages/settings.html"
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

###hypercard
@app.route('/publish', methods=['POST'])
def publish(request):
    print(request.json)
    reqOBJ = request.json
    name = reqOBJ['author']
    title = reqOBJ['title']
    html = reqOBJ['html']
    #remove white space from title
    title = title.replace(' ', '')
    name = name.replace(' ', '')
    with open('./cards/' + name + '_' + title + '.html', 'w') as f:
        f.write(html)
    return Response('OK')

##return list of all cards and by name and title
@app.route('/cards')
def cards(request):
    # Create list of files
    files = [{"title": f, "author": f, "link": '../cards/' + f} for f in os.listdir('./cards') if f.endswith('.html')]
    print('Array of files: ' + str(files) + '\n')
    #clean up names 
    for i in files:
        i['title'] = i['title'].split('_')[1]
        #remove html from title name 
        i['title'] = i['title'].split('.')[0]
        i['author'] = i['author'].split('_')[0]
    # Convert list of files to JSON
    files_json = ujson.dumps(files)
    print('JSON of files: ' + str(files_json) + '\n')
    
    return Response(files_json, headers={'Content-Type': 'application/json'})

#cards req
@app.route('/cards/<path>')
def cards(request, path):
    print(path)
    print('test')
    return send_file('./cards/' + path)

#browse page get 
@app.route('/browse')
def browse(request):
    return send_file('./pages/cardBrowser.html')


###settings json update 
@app.route('/settings', methods=['POST'])
def settingsReq(request):
    print(request.json)
    reqOBJ = request.json
    with open('settings.json', 'w') as f:
        ujson.dump(reqOBJ, f)
    machine.reset()
    return Response('OK')

###settings json get
@app.route('/get_data')
def get_data(request):
    print('test')
    openAI_model = settings['openAI_model']
    print(openAI_model)
    openAI_key = settings['openAI_key']
    #to json
    payload = {'openAI_model': openAI_model, 'openAI_key': openAI_key}
    payload_json = ujson.dumps(payload)
    print(payload_json)
    return Response(payload_json, headers={'Content-Type': 'application/json'})

app.run()
