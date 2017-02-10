import os

# Set environmental variable for FLASK_APP
os.environ['FLASK_APP'] = 'application.py'

# Set environmental variable for DEBUG
#os.environ['FLASK_DEBUG'] = '1'

# Spawn shell process for Flask
os.system('flask run')
