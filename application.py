import urllib.request
import urllib.error
import json
import datetime

from flask import Flask
from flask import render_template

app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Setup var for SQLite database, enable access from multiple threads.
# conn = sqlite3.connect('dashboard.db', check_same_thread=False)
# db = conn.cursor()

output = None

def fetchStatus():
    # Fetch JSON from Status API.
    try:
        response = urllib.request.urlopen("http://onhub.here/api/v1/status").read()
        global output 
        output = json.loads(response.decode("utf8"))
        upstatus = True
    except urllib.error.URLError:
        # Assume OnHub is down or other connectivity issues.
        upstatus = False

fetchStatus()

# Set vars against status JSON.
try:
    if output['system']:
        system = output['system']
        deviceId = system['deviceId']
        groupRole = system['groupRole']
        hardwareId = system['hardwareId']
        modelId = system['modelId']
        uptime = str(datetime.timedelta(seconds=system['uptime']))

    if output['wan']:
        wan = output['wan']
        captivePortal = wan['captivePortal']
        ethernetLink = wan['ethernetLink']
        gatewayIpAddress = wan['gatewayIpAddress']
        invalidCredentials = wan['invalidCredentials']
        ipAddress = wan['ipAddress']
        ipMethod = wan['ipMethod']
        ipPrefixLength = wan['ipPrefixLength']
        leaseDurationSeconds = wan['leaseDurationSeconds']
        localIpAddress = wan['localIpAddress']
        nameServers = wan['nameServers']
        online = wan['online']
        pppoeDetected = wan['pppoeDetected']

    if output['software']:
        software = output['software']
        softwareVersion = software['softwareVersion']
        updateChannel = software['updateChannel']
        updateNewVersion = software['updateNewVersion']
        updateProgress = software['updateProgress']
        updateStatus = software['updateStatus']
except:
    pass

@app.route('/')
def index():

    fetchStatus()
    return render_template('index.html', output=output)


@app.template_filter('uptime')
def uptime(seconds):
    daySeconds = 86400
    hourSeconds = 3600
    minuteSeconds = 60

    if seconds >= daySeconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

    return "%d days, %d hours, %d minutes, %d seconds." % (d, h, m, s)
