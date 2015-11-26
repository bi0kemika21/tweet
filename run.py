#!flask/bin/python
from app import app

# import tweet


app.run(debug = True, port = 3000,threaded = True)
