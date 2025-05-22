from flask import *
from db.db import connection
from routes.functions import render_pdf_portrait_a4


voters=Blueprint('voters',__name__,template_folder="../templates/voters", static_folder='../static',url_prefix='/Voters')

@voters.route('/')
def home():
    return render_template('voters_home.html')

@voters.route('/voters_figure')
def voters_figure():
    db=connection()
    cur=db.cursor()
    cur.execute("Select * from Figure_barangay")
    rw=cur.fetchall()
    cur.execute("Select * from voters")
    total=cur.fetchall()
    return render_template('voters_table.html',rw=rw,total=len(total))

@voters.route('/voters_list_barangay/<brgy>')
def voters_list_barangay(brgy):
    db=connection()
    cur=db.cursor()
    cur.execute("Select * from voters where barangay='"+brgy+"' order by purok,fullname")
    rw=cur.fetchall()
    html=render_template('voters_list_barangay.html',rw=rw)
    return render_pdf_portrait_a4(html)

@voters.route('/verification')
def voters_verify():
    return render_template('voters_verification.html')


@voters.route('/voters_list_verification/',methods=['get','post'])
def voters_list_verification():
    if request.method=='POST':
        cri=request.values.get('cri')
        db=connection()
        cur=db.cursor()
        cur.execute("Select * from voters where fullname like '%"+cri+"%' or precint like '%"+cri+"%' order by fullname limit 500")
        rw=cur.fetchall()
        return jsonify({'html':render_template('voters_table_verification.html',rw=rw)})
    else:
        return str('xcfasda')