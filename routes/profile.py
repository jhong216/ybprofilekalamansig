from flask import *
import sqlite3
from db.db import connection,barangay,coordinator_type

profile=Blueprint("profile",__name__,template_folder='../templates/profiles',static_folder='../static', url_prefix="/Profile")

@profile.route('/')
def home():
    return render_template('profiles_home.html')


@profile.route('/Entry',methods=['get','post'])
def profile_entry():
    if request.method=='POST':
        try:
            cri=request.values.get('cri')
            db=connection()
            cur=db.cursor()
            cur.execute("Select * from voters where fullname like '%"+cri+"%' order by fullname")
            rw=cur.fetchall()
            return jsonify({'html':render_template('profile_voters_table.html',rw=rw)}) 
        except Exception as e:
            msg=f"<p class='pmessage>{str(e)}</p>"
            return jsonify({'html':msg})
    else:
        db=connection()
        cur=db.cursor()
        cur.execute("Select id,Name from Coordinator order by name")
        rw=cur.fetchall()
        return render_template('profile_entry.html',rw=rw)
    

@profile.route('/Profile_Entry_Save',methods=['get','post'])
def profile_save():
    if request.method=='POST':
        try:
            coor=request.values.get('coor')
            fn=request.values.get('fn')
            precint=request.values.get('precint')
            purok=request.values.get('purok')
            barangay=request.values.get('barangay')
            code=request.values.get('code')
            gender=request.values.get('gender')
            status=request.values.get('status')
            birthday=request.values.get('birthday')
            occupation=request.values.get('occupation')
            type=request.values.get('type')
            db=connection()
            cur=db.cursor()
            cur.execute("""INSERT INTO PROFILE(COOR,FULLNAME,PRECINT,SITIO,BARANGAY,
                        GENDER,CODE,STATUS,BIRTHDAY,OCCUPATION,TYPE)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?)""",(coor,fn,precint,purok,barangay,gender,code,status,birthday,occupation,type))
            db.commit()

            cur.execute("Select * from profile where code='"+code+"'")
            rw=cur.fetchall()
            return jsonify({'msg':"Data Successfully Save!",'html':render_template('profile_entry_list.html',rw=rw)})
        except sqlite3.IntegrityError as e:
            msg=f"<p class='pmessage'>ERROR : Duplicate value! <strong>{fn.upper()}</strong> is already exist!</p>"

            db.close()
            return jsonify({'msg':msg})
        
        except Exception as e:
            msg=f"ERROR : {str(e)}"
            return jsonify({'msg':msg})
    else:
        return redirect(url_for('profile_entry'))
    
@profile.route('/profile_verification')
def profile_verification():
    return render_template('profile_verification.html')

@profile.route('/profile_verification_result',methods=['get','post'])
def profile_verification_result():
    if request.method=='POST':
        cri=request.values.get('cri')
        db=connection()
        cur=db.cursor()
        cur.execute("Select * from profile inner join coordinator on coor=coordinator.ID where fullname like '%"+cri+"%' OR code like '%"+cri+"%' order by fullname limit 500")
        rw=cur.fetchall()
        cur.execute("Select ID,NAME from Coordinator")
        crw=cur.fetchall()
        return jsonify({'html':render_template('verify_result.html',rw=rw,crw=crw)})
    else:
        return redirect(url_for('profile.profile_verification'))
    
@profile.route('/profile_verification_result_coordinator',methods=['get','post'])
def profile_verification_coordinator():
    if request.method=='POST':
        cri=request.values.get('cri')
        db=connection()
        cur=db.cursor()
        cur.execute("Select * from coordinator where name like '%"+cri+"%' or barangay like '%"+cri+"%' order by name limit 500")
        rw=cur.fetchall()
        db=connection()
        cur=db.cursor()
        cur.execute("select distinct barangay from voters")
        b=cur.fetchall()
        t=coordinator_type()
        return jsonify({'html':render_template('coordinator_list_result.html',rw=rw,b=b,t=t)})
    else:
        return redirect(url_for('profile.profile_coordinator'))

@profile.route('/profile_delete',methods=['get','post'])
def profile_delete():
    if request.method=='POST':
        aydi=request.values.get('aydi')
        cri=request.values.get('cri')
        try:
            db=connection()
            cur=db.cursor()
            cur.execute("Delete from profile where id='"+ aydi+"'")
            db.commit()
            cur.execute("Select * from profile where fullname like '%"+cri+"%' or code like '"+cri+"' order by fullname limit 200")
            rw=cur.fetchall()
            return jsonify({'msg':"Data Successfuly Deleted!",'html':render_template('verify_result.html',rw=rw)})
        except Exception as e:
            msg=f'ERROR : {str(e)}'
            return jsonify({'msg':msg})
    else:
        return redirect(url_for('profile.profile_verification'))
    

@profile.route('/profile_list_delete]',methods=['get','post'])
def profile_list_delete():
    if request.method=='POST':
        aydi=request.values.get('aydi')
        code=request.values.get('code')
        try:
            db=connection()
            cur=db.cursor()
            cur.execute("Delete from profile where id='"+ aydi+"'")
            db.commit()
            cur.execute("Select * from profile where code='"+code+"'")
            rw=cur.fetchall()
            return jsonify({'msg':"Data Successfully Deleted!",'html':render_template('profile_entry_list.html',rw=rw)})
        except sqlite3.IntegrityError as e:
            msg=f"<p class='pmessage'>ERROR : {e.Title()}</p>"
            return jsonify({'msg':msg})
        
        except Exception as e:
            msg=f"ERROR : {str(e)}"
            return jsonify({'msg':msg})
    else:
        return redirect(url_for('profile_entry'))
    
@profile.route('/profile_update',methods=['get','post'])
def profile_update():
    if request.method=='POST':
        id=request.values.get('id')
        coor=request.values.get('coor')
        code=request.values.get('code')
        cri=request.values.get('cri')
        try:
            db=connection()
            cur=db.cursor()
            cur.execute("UPDATE PROFILE SET CODE=?,COOR=? WHERE ID=?",(code,coor,id))
            db.commit()
            db.close()
            db2=connection()
            cur1=db2.cursor()
            cur1.execute("Select * from profile inner join coordinator on coor=coordinator.ID where fullname like '%"+cri+"%' OR code like '%"+cri+"%' order by fullname limit 500")
            rw=cur1.fetchall()
            return jsonify({'msg':f'Code : {code} & Leader {coor} successfully updated!','html':render_template('verify_result.html',rw=rw)})
        except Exception as e:
            return jsonify({'msg':f'Something Error : {e}'})
            
#COORDINATOR =============================================================
    
@profile.route('/profile_coordinator')
def profile_coordinator():
    return render_template('profile_coordinator.html')

@profile.route('/profile_coordinator_new')
def profile_coordinator_new():
    db=connection()
    cur=db.cursor()
    cur.execute("select distinct barangay from voters")
    a=cur.fetchall()

    f1=open("./db/type.txt","r",encoding="utf8")
    c=f1.readlines()
    f1.close
    return render_template('profile_coordinator_entry.html',b=a,t=c)

@profile.route('/Profile_coordinator_Save',methods=['get','post'])
def coordinator_save():
    if request.method=='POST':
        try:
            name=request.values.get('name')
            type=request.values.get('type')
            address=request.values.get('address')
            brgy=request.values.get('brgy')
            db=connection()
            cur=db.cursor()
            cur.execute("""INSERT INTO COORDINATOR(NAME,TYPE,ADDRESS,BARANGAY)
                        VALUES(?,?,?,?)""",(name,type,address,brgy))
            db.commit()
            return jsonify({'msg':"Data Successfully Save!"})
        except sqlite3.IntegrityError as e :
            msg=f"<p class='pmessage'>ERROR : Duplicate value! <strong>{name.upper()}</strong> is already exist!</p>"
            return jsonify({'msg':msg})
        
        except Exception as e:
            msg=f"ERROR : {str(e)}"
            return jsonify({'msg':msg})
    else:
        return redirect(url_for('profile_coordinator_new'))


@profile.route('/coordinators_list')
def coordinators_list():
    db=connection()
    cur=db.cursor()
    cur.execute("select distinct barangay from voters")
    b=cur.fetchall()
    t=coordinator_type()
    db=connection()
    cur=db.cursor()
    cur.execute("Select * from coordinator order by name")
    rw=cur.fetchall()
    return render_template('coordinator_list.html',b=b,rw=rw,t=t)


@profile.route('/coordinators_delete',methods=['get','post'])
def coordinator_delete():
    if request.method=='POST':
        idd=request.values.get('idd')
        db=connection()
        cur=db.cursor()
        db.execute('PRAGMA foreign_keys=ON')
        cur.execute("Delete  from coordinator where id='"+idd+"'")
        db.commit()
        cur.execute("Select * from coordinator order by name")
        rw=cur.fetchall()
        return jsonify({'html':render_template('coordinator_list2.html',rw=rw)})
    else:
        b=barangay()
        t=coordinator_type()
        db=connection()
        cur=db.cursor()
        cur.execute("Select * from coordinator order by name")
        rw=cur.fetchall()
        return jsonify({'html':render_template('coordinator_list2.html',rw=rw)})
    
@profile.route('/coordinators_update',methods=['get','post'])
def coordinator_update():
    if request.method=='POST':
        id=request.values.get('id')
        fn=request.values.get('fn')
        typ=request.values.get('typ')
        add=request.values.get('add')
        bgy=request.values.get('bgy')
        db=connection()
        cur=db.cursor()
        cur.execute("UPDATE COORDINATOR SET NAME=?,TYPE=?,ADDRESS=?,BARANGAY=? WHERE ID=?",(fn,typ,add,bgy,id))
        db.commit()
        
        db.commit()
        cur.execute("Select * from coordinator order by name")
        rw=cur.fetchall()
        return jsonify({'html':render_template('coordinator_list2.html',rw=rw)})
    else:
        db=connection()
        cur=db.cursor()
        cur.execute("select distinct barangay from voters")
        b=cur.fetchall()
        t=coordinator_type()
        db=connection()
        cur=db.cursor()
        cur.execute("Select * from coordinator order by name")
        rw=cur.fetchall()
        return jsonify({'html':render_template('coordinator_list2.html',rw=rw,b=b)})
    