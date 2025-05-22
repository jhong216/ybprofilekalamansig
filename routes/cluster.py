from flask import *
from db.db import connection
from .functions import *

c=Blueprint('c',__name__,template_folder='../templates/cluster',url_prefix='/cluster')

@c.route('/')
def cluster_figures():
    db=connection()
    cur=db.cursor()
    cur.execute("""Select cluster,count(voters.id),
                       cast((count(voters.id)*.64056) as integer),
                       count(profile.id)
                
                        from VOTERS
                left join profile on profile.FULLNAME=VOTERS.FULLNAME GROUP by cluster order by cast(cluster as integer)""")
    rw=cur.fetchall()
    cur.execute("""
                select count(VOTERS.id),cast((count(voters.id)*.64056) as integer),count(profile.id)
                from voters
                left join profile on 
                profile.FULLNAME = voters.FULLNAME""")
    trw=cur.fetchall()
    return render_template('cluster/cluster_figure.html',rw=rw,trw=trw)

@c.route('/uncapture_list/<int:p>')
def cluster_uncaptured(p):
    t=f'KAMALAYAN KALAMANSIG UNCAPTURED VOTERS'
    db=connection()
    cur=db.cursor()
    cur.execute("""
                select voters.fullname,voters.precint,cluster.no,voters.purok,voters.barangay from PROFILE
                RIGHT JOIN VOTERS ON VOTERS.FULLNAME=PROFILE.FULLNAME
                LEFT JOIN CLUSTER ON VOTERS.PRECINT=CLUSTER.PRECINT
                WHERE PROFILE.FULLNAME IS NULL AND CLUSTER.NO="""+ str(p) +"""
""")
    rw=cur.fetchall()
    html=render_template('/cluster/cluster_list.html',rw=rw,T=t,cls=p)
    return render_pdf_portrait_a4(html)


@c.route('/capture_list/<int:p>')
def cluster_captured(p):
    t=f'KAMALAYAN KALAMANSIG CAPTURED VOTERS'
    db=connection()
    cur=db.cursor()
    cur.execute("""
                select voters.fullname,voters.precint,cluster.no,voters.purok,voters.barangay from PROFILE
                inner JOIN VOTERS ON VOTERS.FULLNAME=PROFILE.FULLNAME
                LEFT JOIN CLUSTER ON VOTERS.PRECINT=CLUSTER.PRECINT
                where CLUSTER.NO="""+ str(p) +"""
""")
    rw=cur.fetchall()
    html=render_template('/cluster/cluster_list.html',rw=rw,T=t,cls=p)
    return render_pdf_portrait_a4(html)

#PRECINCTS FIGURES =========================================================================

@c.route('/clustered_precincts')
def clustered_precincts():
    db=connection()
    cur=db.cursor()
    cur.execute("select distinct no from cluster")
    crw=cur.fetchall()
    return render_template('cluster/precint_figure.html',crw=crw)