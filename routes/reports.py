from flask import *
from db.db import connection



report=Blueprint('report',__name__,template_folder='../templates/reports',url_prefix='/reports')

@report.route('/')
def home():
    return render_template('reports_home.html')


@report.route('/barangay_figure')
def report_barangay_figure():
    db=connection()
    cur=db.cursor()
    cur.execute("Select barangay, count(id) as Figure from profile group by barangay")
    rw=cur.fetchall()
    cur2=db.execute("select count(id) as figure from profile")
    rw2=cur2.fetchall()[0][0]
    return render_template('barangay_figure.html',rw=rw,rw2=rw2)


@report.route('/print_brgy_list/<cri>')
def brgy_list_report(cri):
    db=connection()
    cur=db.cursor()
    cur.execute("select * from profile where barangay = '"+cri+"' ORDER BY SITIO,FULLNAME")
    rw=cur.fetchall()
    return render_template('brgy_list_report.html',rw=rw)

@report.route('/print_brgy_list_hh/<cri>')
def brgy_list_hh(cri):
    db=connection()
    cur=db.cursor()
    cur.execute("select * from profile where coordinator = '"+cri+"' ORDER BY FULLNAME")
    rw=cur.fetchall()
    return render_template('brgy_list_hh.html',rw=rw)


@report.route('/report_group_figure')
def report_group_figure():
    db=connection()
    cur=db.cursor()
    cur.execute("Select coordinator,barangay,sitio, count(id) as Figure from profile group by barangay,Coordinator order by coordinator,barangay,sitio")
    rw=cur.fetchall()
    cur2=db.execute("select count(id) as figure from profile")
    rw2=cur2.fetchall()[0][0]
    return render_template('coordinator_list_figure.html',rw=rw,rw2=rw2)

@report.route('/print_grouping_brgy_list/<brgy>/<group>')
def brgy_groupingbarangay_report(brgy,group):
    db=connection()
    cur=db.cursor()
    cur.execute("select * from profile where barangay = '"+brgy+"'  and coordinator = '"+group+"' ORDER BY SITIO,FULLNAME")
    rw=cur.fetchall()
    return render_template('brgy_list_report.html',rw=rw,title=group)


@report.route('/report_purok_figure/<brgy>')
def report_purok_figure(brgy):
    db=connection()
    cur=db.cursor()
    cur.execute("Select barangay,sitio, count(id) as Figure from profile  where barangay='"+brgy+"' group by sitio order by sitio")
    rw=cur.fetchall()
    cur2=db.execute("select count(id),barangay as figure from profile where barangay='"+brgy+"'")
    rw2=cur2.fetchall()[0][0]
    return render_template('purok_figure.html',rw=rw,rw2=rw2)

@report.route('/print_purok_brgy_list/<brgy>/<prk>/')
def brgy_purok_report(brgy,prk):
    db=connection()
    cur=db.cursor()
    cur.execute("select * from profile where barangay = '"+brgy+"'  and sitio = '"+prk+"' ORDER BY SITIO,FULLNAME")
    rw=cur.fetchall()
    return render_template('brgy_list_report.html',rw=rw)

@report.route('/print_brgy_list/<cri>/')
def coor_alllist_report(cri):
    db=connection()
    cur=db.cursor()
    cur.execute("select * from profile where coordinator ='"+cri+"' ORDER BY SITIO,FULLNAME")
    rw=cur.fetchall()
    t="COORDINATOR"
    return render_template('brgy_list_report.html',rw=rw,title=cri,t=t)

@report.route('/household_figure/<brgy>')
def report_hh_figure(brgy):
    db=connection()
    cur=db.cursor()
    cur.execute("Select Barangay,code, count(id) as Figure  from profile where barangay ='"+brgy+"' group by code")
    rw=cur.fetchall()
    cur2=db.execute("select count(id) as figure  from profile where barangay ='"+brgy+"'")
    rw2=cur2.fetchall()[0][0]
    return render_template('householdfigures.html',rw=rw,rw2=rw2)


@report.route('/household_report/<hh>')
def report_hhlist(hh):
    db=connection()
    cur=db.cursor()
    cur.execute("Select *  from profile where code ='"+hh+"' order by fullname")
    rw=cur.fetchall()
    return render_template('hhlist.html',rw=rw,hh=hh)
#===COORDINATOR============================================================================
@report.route('/coor_figure/')
def coor_figure():
    db=connection()
    cur=db.cursor()
    cur.execute("select BARANGAY,address,count(id) from COORDINATOR GROUP by BARANGAY,ADDRESS")
    rw=cur.fetchall()
    return render_template('/coordinator/coor_figure.html',rw=rw)

@report.route('/coor_figure_barangay/<brgy>/')
def coor_figure_brgy(brgy):
    db=connection()
    cur=db.cursor()
    cur.execute("select barangay,address,count(id) from COORDINATOR where barangay='"+ brgy + "' GROUP by BARANGAY,ADDRESS")
    rw=cur.fetchall()
    return render_template('/coordinator/coor_figure.html',rw=rw)

@report.route('/overall_list_coordinator/<brgy>/<prk>/')
def list_coordinator(brgy,prk):
    db=connection()
    cur=db.cursor()
    cur.execute("select coordinator.id,COORDINATOR.name,COORDINATOR.TYPE,COORDINATOR.ADDRESS,COORDINATOR.BARANGAY,coalesce(count(profile.id),0) as figure from COORDINATOR left join profile ON COORDINATOR.ID=profile.COOR WHERE COORDINATOR.BARANGAY=? and COORDINATOR.ADDRESS=? GROUp by COORDINATOR.name",(brgy,prk))
    rw=cur.fetchall()
    return render_template('/coordinator/coor_list.html',rw=rw)

@report.route('/overall_list_coordinator_brgy/<brgy>/')
def list_coordinator_brgy(brgy):
    db=connection()
    cur=db.cursor()
    cur.execute("select coordinator.id,COORDINATOR.name,COORDINATOR.TYPE,COORDINATOR.ADDRESS,COORDINATOR.BARANGAY,coalesce(count(profile.id),0) as figure from COORDINATOR left join profile ON COORDINATOR.ID=profile.COOR WHERE COORDINATOR.BARANGAY='"+brgy+"' GROUp by COORDINATOR.name")
    rw=cur.fetchall()
    return render_template('/coordinator/coor_list.html',rw=rw)


@report.route('/coordinator_members_list/<c>/')
def coor_members_list(c):
    try:
        db=connection()
        cur=db.cursor()
        cur.execute("SELECT PROFILE.FULLNAME,PROFILE.PRECINT, PROFILE.SITIO, PROFILE.BARANGAY,COORDINATOR.ID,COORDINATOR.name,PROFILE.TYPE,PROFILE.CODE FROM PROFILE INNER JOIN COORDINATOR WHERE COORDINATOR.ID=PROFILE.COOR  AND COORDINATOR.ID='"+c+"'")
        rw=cur.fetchall()
        for i in rw:
            cor=f'{i[5]}'
        return render_template('/coordinator/coor_members.html',rw=rw,cor=cor)
    except Exception as e:
        return str(e)

@report.route('/household_list/<brgy>')
def household_list_brgy(brgy):
    db=connection()
    cur=db.cursor()
    cur.execute("Select *,coordinator.id,coordinatoR.name from Profile inner join coordinator where coordinator.id=profile.coor and profile.barangay='"+brgy+"'")
    rw=cur.fetchall()
    return render_template('/brgy_list_hh.html',rw=rw)


#LEADER================================================================================
@report.route('/leaderlist/<brgy>/')
def leaderlist_brgy(brgy):
    db=connection()
    cur=db.cursor()
    cur.execute("""Select profile.fullname,profile.precint,coordinator.name,profile.sitio,profile.barangay from profile
                inner join coordinator on coordinator.id=profile.coor
                  where coordinator.barangay='"""+brgy+"""'""")
    rw=cur.fetchall()
    return render_template('/coordinator/leader.html',rw=rw,brgy=brgy)

@report.route('/leaderlist/<brgy>/<prk>/')
def leaderlist_prk(brgy,prk):
    db=connection()
    cur=db.cursor()
    cur.execute("""Select profile.fullname,profile.precint,coordinator.name,profile.sitio,profile.barangay,
                coordinator.address,coordinator.barangay               
                 from profile
                inner join coordinator on coordinator.id=profile.coor
                  where coordinator.barangay='"""+brgy+"""' and coordinator.address='"""+prk+"""'""")
    rw=cur.fetchall()
    return render_template('/coordinator/leader.html',rw=rw,brgy=brgy)

