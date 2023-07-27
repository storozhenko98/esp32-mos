from microdot import send_file, Microdot

app = Microdot()

@app.route('/')           
def index(request):
    return send_file('./pages/home.html')


@app.route('/api/<path>')
def api(request, path):
    if path == 'settings':
        return 'test'

@app.route('/assets/<path>')  
def assets(request, path):
    return send_file('./assets/' + path)



app.run()