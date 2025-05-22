from datetime import date
import datetime
import pdfkit
from flask import make_response,render_template
import pyodbc
# from flask_session import session
 
def calculateAge(birthDate):
    b=birthDate.replace("/",",")
    days_in_year = 365.2425  
    print(datetime.date.b).days 
    # age = int((date.today() - datetime.date.b).days) /days_in_year
    # return int(age)

# from dateutil.relativedelta import relativedelta


# def calculate_date_date(date_str, format_str):
#     start_date = datetime.datetime.strptime(date_str, format_str)
#     return relativedelta(datetime.datetime.now(), start_date).years


def render_pdf_landscape(h):
            patha=r'C:\\Program Files\\wkhtmltopdf\bin\\wkhtmltopdf.exe'
            config=pdfkit.configuration(wkhtmltopdf=patha)
            options = {
            'page-size': 'A4',
            'orientation': 'landscape',
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.3in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'footer-right':'Page  [PAGE] of [topage]',
            'footer-left':'Page  [PAGE] of [topage]',
            'title':"GENERATED PROFILING MASTERLIST",
            'footer-Font-size':'8',
                }
            htm=render_template(h)
            pdf= pdfkit.from_file(htm,False,configuration=config,options=options,verbose=True)
            response=make_response(pdf)
            response.headers['Content-Type']="application/pdf"
            response.headers['Content-Disposition']="inline;filename="+f"Generated-Report.pdf"
            return response

def render_pdf_a5(h):
            patha=r'C:\\Program Files\\wkhtmltopdf\bin\\wkhtmltopdf.exe'
            config=pdfkit.configuration(wkhtmltopdf=patha)
            options = {
            'page-size': 'A5',
            'orientation': 'landscape',
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.3in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'footer-right':'Page  [PAGE] of [topage]',
            'footer-left':'Powered by: YB IT Solution TIN: 741-539-024-000',
            'title':"GENERATED PROFILING MASTERLIST",
            'footer-Font-size':'6',
                }
            pdf= pdfkit.from_string(h,False,configuration=config,options=options,verbose=True)
            response=make_response(pdf)
            response.headers['Content-Type']="application/pdf"
            response.headers['Content-Disposition']="inline;filename="+f"Generated-Report.pdf"
            return response


def render_pdf_portrait_a4(h):
            patha=r'C:\\Program Files\\wkhtmltopdf\bin\\wkhtmltopdf.exe'
            config=pdfkit.configuration(wkhtmltopdf=patha)
            options = {
            'page-size': 'A4',
            'orientation': 'portrait',
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.3in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'footer-right':'Page  [PAGE] of [topage]',
            'title':"GENERATED LIST",
            'footer-Font-size':'6',
                }
            pdf= pdfkit.from_string(h,False,configuration=config,options=options,verbose=True)
            response=make_response(pdf)
            response.headers['Content-Type']="application/pdf"
            response.headers['Content-Disposition']="inline;filename="+f"Generated-Report.pdf"
            return response

def voters_validity(voters):
    db=pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\KAPAMILYA\KAPAMILYA.accdb;')
    dbcursor=db.cursor()
    dbcursor.execute("Select voters_name from voters where voters_name=?",voters)
    result=dbcursor.fetchone()
    if result:
        return result
    else:
        return str(Exception)
    
def render_pdf_landscape_a4(h):
            patha=r'C:\\Program Files\\wkhtmltopdf\bin\\wkhtmltopdf.exe'
            config=pdfkit.configuration(wkhtmltopdf=patha)
            options = {
            'page-size': 'folio',
            'orientation': 'landscape',
            'margin-top': '0.2in',
            'margin-right': '0.2in',
            'margin-bottom': '0.3in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            'enable-local-file-access': True,
            'footer-right':'Page  [PAGE] of [topage]',
            'title':"GENERATED LIST",
            'footer-Font-size':'6',
                }
            pdf= pdfkit.from_string(h,False,configuration=config,options=options,verbose=True)
            response=make_response(pdf)
            response.headers['Content-Type']="application/pdf"
            response.headers['Content-Disposition']="inline;filename="+f"Generated-Report.pdf"
            return response

