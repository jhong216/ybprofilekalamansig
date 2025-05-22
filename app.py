from flask import *
from routes.voters import voters
from routes.profile import profile
from routes.reports import report
from routes.cluster import c
from dash.dash import dash

app=Flask(__name__)
app.register_blueprint(voters)
app.register_blueprint(profile)
app.register_blueprint(report)
app.register_blueprint(dash)
app.register_blueprint(c)

@app.route('/')
def home():
   return render_template('home.html')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port='99')

