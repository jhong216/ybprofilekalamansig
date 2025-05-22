from flask import *
from db.db import connection


dash=Blueprint('dash',__name__,template_folder='../dash/templates',url_prefix='/dashboard')

@dash.route('/dashboard')
def dashboard():
    db=connection()
    cur=db.cursor()
    cur.execute("""select voters.BARANGAY,count(voters.id)AS FIGURE,(cast((count(voters.id)*.64056) as integer)) AS TARGET ,COUNT(PROFILE.ID) as CAPTURE,
(cast((count(voters.id)*.64) as integer))-COUNT(PROFILE.ID)  AS UNCAPTURED from voters left join profile on voters.FULLNAME=PROFILE.FULLNAME

 GROUP by voters.BARANGAY""")
    rw=cur.fetchall()

    cur.execute("""select count(VOTERS.id),cast((count(voters.id)*.64056) as integer),count(profile.id),
                cast((count(voters.id)*.64056) as integer)-count(profile.id)  from voters
                left join profile on 
                profile.FULLNAME = voters.FULLNAME
    """)
    trw=cur.fetchall()
    return render_template('dash.html',rw=rw,trw=trw)