from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import hashlib
import config
import requests
import datetime
from datetime import date

APP_ID = config.ak4
APP_KEY = config.ak5
api_endpoint = "https://api.edamam.com/api/nutrition-details"

url = api_endpoint + "?app_id=" + APP_ID + "&app_key=" + APP_KEY
headers = {
    'Content-type': 'application/json'
}

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = config.ak2
app.config['MYSQL_PASSWORD'] = config.ak3
app.config['MYSQL_DB'] = config.ak2
mysql = MySQL(app)
app.secret_key = 'a'


def sendgridmail(user, TEXT, sub):
    sg = sendgrid.SendGridAPIClient(config.ak1)
    from_email = Email(config.em)  # Change to your verified sender
    to_email = To(user)  # Change to your recipient
    subject = sub
    content = Content("text/plain", TEXT)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)


@app.route('/', methods=['GET', 'POST'])
def homer():
    return render_template('homepage.html')


@app.route('/homepage.html', methods=['GET', 'POST'])
def home():
    return render_template('homepage.html')


@app.route('/signupd.html')
def supd():
    return render_template('signupd.html')


@app.route('/validate1', methods=['GET', 'POST'])
def supd1():
    if request.method == 'POST':
        email = request.form['did']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT email FROM doctor WHERE email = %s', (email,))
        acc = cursor.fetchone()
        if acc != None:
            return render_template('signupd.html', er="ACCOUNT Already Exists")
        tex = "Hello Doctor,\n Thank you for registering with us. Please kindly fill the given form: \n https://forms.office.com/r/THiq7iYVHF \nSo that we can verify and give you the login credentials."
        sub = "Thank You"
        sendgridmail(email, tex, sub)
    return render_template('thank.html')


@app.route('/signupp.html', methods=['GET', 'POST'])
def supp():
    return render_template('signupp.html',)


@app.route('/validate2', methods=['GET', 'POST'])
def supp1():
    if request.method == 'POST':
        email = request.form['pid']
        name = request.form['name']
        phone = request.form['phone']
        date = request.form['d1']
        gen = request.form['gender']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT email FROM patient WHERE email = %s', (email,))
        acc = cursor.fetchone()
        if acc != None:
            return render_template('signupp.html', er="ACCOUNT Already Exists")
        currentKey = hashlib.sha1((email+name).encode())
        pid = "PAT"+str(currentKey.hexdigest())[:10]
        psw = str(hashlib.sha1(
            str(currentKey.hexdigest()).encode()).hexdigest())[:20]
        tex = "Hello Patient, \n Username: " + email + " \n and Your Password: "+psw
        sendgridmail(email, tex, "Credentials for logging in!")
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO patient VALUES (% s, % s, % s,% s, % s, % s, % s)',
                       (pid, name, email, psw, phone, gen, date))
        mysql.connection.commit()
    return render_template('login.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/validate', methods=['GET', 'POST'])
def logvalid():
    if request.method == 'POST':
        email = request.form['xid']
        id = request.form['identity']
        cursor = mysql.connection.cursor()
        f = 0
        if id == "doc":
            cursor.execute(
                'SELECT did FROM doctor WHERE email = %s', (email,))
            dd = cursor.fetchone()
            if dd != None:
                xid = dd[0]
                f = 1
        elif id == "pat":
            cursor.execute(
                'SELECT pid FROM patient WHERE email = %s', (email,))
            dd = cursor.fetchone()
            if dd != None:
                xid = dd[0]
                f = 1
        if f != 1:
            return render_template('login.html', er="ACCOUNT NOT FOUND")
        psw = request.form['psw']
        session['username'] = xid
        st = xid[0:3]

        if st == "DOC":
            cursor.execute(
                'SELECT password FROM doctor WHERE did = %s', (xid,))
            acc = cursor.fetchone()
            if acc != None:
                account = acc[0]
                if psw == account:
                    return redirect("/dashboardd")
        elif st == "PAT":
            cursor.execute('SELECT psw FROM patient WHERE pid = %s', (xid,))
            acc = cursor.fetchone()
            if acc != None:
                account = acc[0]
                if psw == account:
                    return redirect("/dashboardp")
    return render_template('login.html', er="WRONG PASSWORD")


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    return render_template('admin_login.html')


@app.route('/adminpage', methods=['GET', 'POST'])
def adminpage():
    if request.method == 'POST':
        xid = request.form['xid']
        psw = request.form['psw']
        if xid == "ADMIN1001" and psw == "1001":
            return render_template('admin.html')
    return render_template('admin_login.html', er="Account not found")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session["username"] = None
    session['temp'] = None
    session['date'] = None
    return redirect("/login.html")


@app.route('/validate3', methods=['GET', 'POST'])
def logvaliddoc():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        phone = request.form['phone']
        spec = request.form['special']
        deg = request.form['deg']
        gen = request.form['gender']
        loc = request.form['loc']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT email FROM doctor WHERE email = %s', (email,))
        acc = cursor.fetchone()
        if acc != None:
            return render_template('admin.html', er="ACCOUNT Already Exists")
        currentKey = hashlib.sha1(email.encode())
        did = "DOC"+str(currentKey.hexdigest())[:10]
        psw = str(hashlib.sha1(
            str(currentKey.hexdigest()).encode()).hexdigest())[:20]
        tex = "Hello Doctor, \n Username: " + email + "\n and Your Password: " + \
            psw+" , \n Please signin to the login portal using these credentials."
        sendgridmail(email, tex, "Credentials for logging in!")
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO doctor (did, name, email, password, phone, special, degree, gender, location) VALUES (% s, % s, % s, %s, %s, %s, %s, %s, %s)",
                       (did, name, email, psw, phone, spec.upper(), deg, gen, loc))
        mysql.connection.commit()
    return render_template('admin.html')


@app.route('/validate4', methods=['GET', 'POST'])
def npass():
    if request.method == 'POST':
        xid = session["username"]
        current = request.form['psw']
        npsw = request.form['npsw']
        cpsw = request.form['cpsw']
        if cpsw != npsw:
            return render_template('change_password_patient.html', er="New password and Confirm password are not the same")
        st = xid[0:3]
        cursor = mysql.connection.cursor()
        if st == "PAT":
            cursor.execute('SELECT psw FROM patient WHERE pid = %s', (xid,))
            acc = cursor.fetchone()
            if acc != None:
                account = acc[0]
                if current != account:
                    return render_template('change_password_patient.html', er="Current password is not right")
            else:
                return render_template('change_password_patient.html', er="Wrong ID")
            cursor.execute(
                'Update patient set psw=%s WHERE pid = %s', (npsw, xid,))
    mysql.connection.commit()
    return render_template('patient/password_change_confirm_pat.html')


@app.route('/validate5', methods=['GET', 'POST'])
def npassdoc():
    if request.method == 'POST':
        xid = session["username"]
        current = request.form['psw']
        npsw = request.form['npsw']
        cpsw = request.form['cpsw']
        if cpsw != npsw:
            return render_template('change_password_doc.html', er="New password and Confirm password are not the same")
        st = xid[0:3]
        cursor = mysql.connection.cursor()
        if st == "DOC":
            cursor.execute(
                'SELECT password FROM doctor WHERE did = %s', (xid,))
            acc = cursor.fetchone()
            if acc != None:
                account = acc[0]
                if current != account:
                    return render_template('change_password_doc.html', er="Current password is not right")
            else:
                return render_template('change_password_doc.html', er="Wrong ID")
            cursor.execute(
                'Update doctor set password=%s WHERE did = %s', (npsw, xid,))
    mysql.connection.commit()
    return render_template('doctor/index_doc.html')


@app.route('/nutrition.html', methods=['GET', 'POST'])
def nutrition():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/nutrition.html')


@app.route('/nutrition_doc.html', methods=['GET', 'POST'])
def nutrition_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/nutrition_doc.html')


@app.route('/analyze1', methods=['GET', 'POST'])
def analyze_doc():
    if request.method == 'POST':
        title = request.form['title']
        ingred = request.form['ingred']
        i = ingred.split(',')
        recipe = {'title': title, 'ingr': i}
        r = requests.post(url, headers=headers, json=recipe)
        items = r.json()
        it = items['totalNutrients']
    return render_template('patient/nutrition.html', val=it, title=title.upper(), item=ingred)


@app.route('/analyze2', methods=['GET', 'POST'])
def analyze_pat():
    if request.method == 'POST':
        title = request.form['title']
        ingred = request.form['ingred']
        i = ingred.split(',')
        recipe = {'title': title, 'ingr': i}
        r = requests.post(url, headers=headers, json=recipe)
        items = r.json()
        it = items['totalNutrients']
    return render_template('doctor/nutrition_doc.html', val=it, title=title.upper(), item=ingred)


# doctor routing
@app.route('/appointments_doc.html')
def call_appointments_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/appointments_doc.html')


@app.route('/change_password_doc.html')
def call_change_password_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/change_password_doc.html')


@app.route('/connect_doc.html')
def call_connect_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/connect_doc.html')


@app.route('/doctor_cancellation_form.html')
def call_doctor_cancellation_form():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/doctor_cancellation_form.html')


@app.route('/doctor_cancel', methods=['GET', 'POST'])
def call_doc_cancel_form():
    if session["username"] != None and session["username"][0:3] == "DOC":
        date = request.form['date']
        stime = request.form['stime']
        etime = request.form['etime']
        now1 = datetime.datetime.strptime(date, '%Y-%m-%d')
        formatted_date = now1.strftime('%Y-%m-%d')
        now2 = datetime.datetime.strptime(stime, '%H:%M')
        s1 = now2.strftime('%H:%M:%S')
        now3 = datetime.datetime.strptime(etime, '%H:%M')
        s2 = now3.strftime('%H:%M:%S')
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT pid FROM event WHERE did = %s and DATE(start_date) = %s and TIME(start_date)>=%s and TIME(end_date)<=%s', (session["username"], formatted_date, s1, s2,))
        acc = cursor.fetchall()
        if len(acc) == 0:
            return render_template('doctor/doctor_cancellation_form.html', err="No appointments found")
        p = []
        for i in acc:
            p.append(i[0])
        email = []
        for i in p:
            cursor.execute(
                'SELECT email FROM patient WHERE pid = %s', (i,))
            acc = cursor.fetchone()
            email.append(acc[0])
        text = "Due to unseen circumstances, your appointment has been cancelled by the doctor. The refund process will be completed in a few days. You can schedule an appointment once again from the  booking page. \n Thank You."
        sub = "Appointment Cancelled"
        for i in email:
            sendgridmail(i, text, sub)
        cursor.execute('delete from event where did = %s and DATE(start_date) = %s and TIME(start_date)>=%s and TIME(end_date)<=%s',
                       (session["username"], formatted_date, s1, s2,))
        mysql.connection.commit()
        return render_template('doctor/index_doc.html')


@app.route('/video_doc.html')
def call_video_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        cursor = mysql.connection.cursor()
        today = date.today()
        d = today.strftime("%y-%m-%d")
        h = today.strftime("%H")
        cursor.execute(
            "SELECT url from event where did=%s and DATE(start_date) = %s and HOUR(TIME(start_date))>=%s order by start_date", (session["username"], d, h,))
        rows = cursor.fetchone()
        if rows == None:
            return render_template('doctor/connect_doc.html', er="No meeting found, please wait for your slot timing...")
        return redirect(rows[0])


@app.route('/files_doc.html')
def call_files_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/files_doc.html')


@app.route('/dashboardd')
def dash1():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/index_doc.html')


@app.route('/index_doc.html')
def dash5():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/index_doc.html')


@app.route('/password_change_confirm.html')
def call_password_change_confirm():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/password_change_confirm.html')


@app.route('/settings_doc.html')
def call_settings_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/settings_doc.html')


@app.route('/view_doc.html')
def call_view_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT dname,pname,start_date FROM event WHERE did = %s', (session["username"],))
        acc = cursor.fetchall()
        d = []
        if acc != None:
            for i in acc:
                d.append([i[0], i[1], i[2].strftime("%d/%m/%Y, %H:%M:%S")])
        return render_template('doctor/view_doc.html', val=d)


@app.route('/newsd.html')
def call_news_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        response = requests.get(
            "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey="+config.ak6)
        news = response.json()
        return render_template('doctor/news_doc.html', news=news['articles'])


@app.route('/calendard.html')
def call_calendar_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/calendar_events_doc.html')


@app.route('/calendar-eventsd')
def call_calendar_eved():
    if session["username"] != None and session["username"][0:3] == "DOC":
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT id, title, url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as end FROM event where did=%s", (session["username"],))
            rows = cursor.fetchall()
            l = []
            for i in rows:
                l.append(dict({'id': i[0], 'title': i[1], 'url': i[2],
                         'class': i[3], 'start': i[4], 'end': i[5]}))
            resp = jsonify({'success': 1, 'result': l})
            resp.status_code = 200
            return resp
        except Exception as e:
            print(e)


@app.route('/faqbot_doc.html')
def call_faqbot_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        return render_template('doctor/faqbot_doc.html')


# patient routing
@app.route('/dashboardp')
def dash2():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/index.html')


@app.route('/index.html')
def indexp():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/index.html')


@app.route('/alert_cancel.html')
def alertc():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/alert_cancel.html')


@app.route('/appointments.html')
def appointmentsp():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/appointments.html')


@app.route('/search_doctor.html')
def search_doctorp():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/search_doctor.html')


@app.route('/profile_doc.html')
def call_profile_doc():
    if session["username"] != None and session["username"][0:3] == "DOC":
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT name,email,phone,special,degree,gender,location,startm,endm,starte,ende,ratings from doctor where did=%s", (session["username"],))
        rows = cursor.fetchone()
        l = [i for i in rows]
        return render_template('doctor/profile_doc.html', prof=l)


@app.route('/query_doctor', methods=['GET', 'POST'])
def query_doctorp():
    if session["username"] != None and session["username"][0:3] == "PAT":
        d = request.form['doctorlist']
        di = '%'+d.upper()+'%'
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT did,name,special,degree,gender from doctor where special like %s", (di,))
        rows = cursor.fetchall()  # if no results found condition missing
        if rows == None:
            li = [['No results found']]
            return render_template('patient/search_doctor.html', docs=li)
        li = []
        for i in rows:
            li.append([j for j in i])
        return render_template('patient/search_doctor.html', docs=li)


@app.route('/book_appointment.html', methods=['GET', 'POST'])
def book():
    if session["username"] != None and session["username"][0:3] == "PAT":
        did = request.form['submit_button']
        session['temp'] = did
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT name,email,special,degree,gender,location,startm,endm,starte,ende,ratings from doctor where did=%s", (did,))
        row = cursor.fetchone()
        li = [i for i in row]
        return render_template('patient/book_appointment.html', l=li)


@app.route('/search_slots', methods=['GET', 'POST'])
def sslots():
    if session["username"] != None and session["username"][0:3] == "PAT":
        date = request.form['date']
        pref = request.form['appointment_for']
        now1 = datetime.datetime.strptime(date, '%Y-%m-%d')
        formatted_date = now1.strftime('%Y-%m-%d')
        session['date'] = formatted_date
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT name,email,special,degree,gender,location,startm,endm,starte,ende,ratings from doctor where did=%s", (session['temp'],))
        row = cursor.fetchone()
        li = [i for i in row]
        cursor.execute(
            "SELECT start_date from event where did=%s and DATE(start_date) = %s", (session['temp'], formatted_date,))
        rows = cursor.fetchall()
        input = []
        for i in rows:
            input.append(i[0])
        working_hours = [row[-5].seconds//3600, row[-4].seconds //
                         3600, row[-3].seconds//3600, row[-2].seconds//3600]
        apts = []
        wh = []
        ms = []
        ms = []
        es = []
        total = []
        for i in input:
            apts.append(int(i.strftime('%H')))
        for i in working_hours:
            wh.append(i)
        for i in range(wh[0], wh[1]):
            if i not in apts:
                total.append(str(i)+":00")
                ms.append(str(i)+":00")
        for i in range(wh[2], wh[3]):
            if i not in apts:
                total.append(str(i)+":00")
                es.append(str(i)+":00")
        if len(total) == 0:
            return render_template('patient/book_appointment.html', l=li, er="No available slots on this date")
        best = []
        if pref == "morning":
            if len(ms) <= 2:
                for i in ms:
                    best.append(i)
            else:
                for i in range(0, 2):
                    best.append(ms[i])
            for i in es:
                if len(best) == 3:
                    break
                best.append(i)
        else:
            if len(es) <= 2:
                for i in es:
                    best.append(i)
            else:
                for i in range(0, 2):
                    best.append(es[i])
            for i in ms:
                if len(best) == 3:
                    break
                best.append(i)
        return render_template('patient/book_appointment.html', l=li, t=total, best=best)


@app.route('/book_slot', methods=['GET', 'POST'])
def bookslots():
    if session["username"] != None and session["username"][0:3] == "PAT":
        date = session['date']
        did = session['temp']
        pid = session['username']
        title = "Meeting"
        url = 'https://docit-videocall.herokuapp.com/'+pid+did
        clas = 'event'
        time = request.form['slots'] + ':00'
        stime = date+' '+time
        now = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
        formatted_date1 = now.strftime('%Y-%m-%d %H:%M:%S')
        etime = date+' '+time
        now1 = datetime.datetime.strptime(etime, '%Y-%m-%d %H:%M:%S')
        formatted_date2 = now1.strftime('%Y-%m-%d %H:%M:%S')
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT name from doctor where did=%s", (session['temp'],))
        row = cursor.fetchone()
        dname = row[0]
        cursor.execute(
            "SELECT name from patient where pid=%s", (pid,))
        row = cursor.fetchone()
        pname = row[0]
        cursor.execute(
            "insert into event values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", ("1", title, url, clas, formatted_date1, formatted_date2, pid, did, pname, dname))
        mysql.connection.commit()
        return redirect('https://docit-payment.netlify.app/')


@app.route('/change_password_patient.html')
def change_passwordp():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/change_password_patient.html')


@app.route('/connect.html')
def connectp():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/connect.html')


@app.route('/files.html')
def filesp():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/files.html')


@app.route('/settings.html')
def call_settings_pat():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/settings.html')


@app.route('/profiles_page_patient.html')
def call_profile_page_patient():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/settings.html')


@app.route('/patient_cancellation_info_page.html', methods=['GET', 'POST'])
def call_patient_cancellation_info_page():
    if session["username"] != None and session["username"][0:3] == "PAT":
        date = request.form['date']
        stime = request.form['stime']
        etime = request.form['etime']
        now1 = datetime.datetime.strptime(date, '%Y-%m-%d')
        formatted_date = now1.strftime('%Y-%m-%d')
        now2 = datetime.datetime.strptime(stime, '%H:%M')
        s1 = now2.strftime('%H:%M:%S')
        now3 = datetime.datetime.strptime(etime, '%H:%M')
        s2 = now3.strftime('%H:%M:%S')
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT id FROM event WHERE pid = %s and DATE(start_date) = %s and TIME(start_date)>=%s and TIME(end_date)<=%s', (session["username"], formatted_date, s1, s2,))
        acc = cursor.fetchall()
        if len(acc) == 0:
            return render_template('patient/patient_cancellation_form.html', err="No appointments found")
        cursor.execute('delete from event where pid = %s and DATE(start_date) = %s and TIME(start_date)>=%s and TIME(end_date)<=%s',
                       (session["username"], formatted_date, s1, s2,))
        mysql.connection.commit()
        return render_template('patient/patient_cancellation_info_page.html')


@app.route('/patient_cancellation_form.html', methods=['GET', 'POST'])
def call_patient_cancellation_form():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/patient_cancellation_form.html')


@app.route('/password_change_confirm_pat.html')
def call_password_change_confirm_pat():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/password_change_confirm_pat.html')


@app.route('/modify_appointments.html')
def call_modify_appointments():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/modify_appointments.html')


@app.route('/view.html')
def call_view_pat():
    if session["username"] != None and session["username"][0:3] == "PAT":
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT pname,dname,start_date FROM event WHERE pid = %s', (session["username"],))
        acc = cursor.fetchall()
        d = []
        if acc != None:
            for i in acc:
                d.append([i[0], i[1], i[2].strftime("%d/%m/%Y, %H:%M:%S")])
        return render_template('patient/view.html', val=d)


@app.route('/faqbot.html')
def call_faqbot_pat():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/faqbot.html')

# Help me-- https://forms.office.com/r/93det4YdVg


@app.route('/calendarp.html')
def call_calendar_pat():
    if session["username"] != None and session["username"][0:3] == "PAT":
        return render_template('patient/calendar_events.html')


@app.route('/calendar-eventsp')
def call_calendar_eve():
    if session["username"] != None and session["username"][0:3] == "PAT":
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT id, title, url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as end FROM event where pid=%s", (session["username"],))
            rows = cursor.fetchall()
            l = []
            for i in rows:
                l.append(dict({'id': i[0], 'title': i[1], 'url': i[2],
                         'class': i[3], 'start': i[4], 'end': i[5]}))
            resp = jsonify({'success': 1, 'result': l})
            resp.status_code = 200
            # i[4,5]-86400000
            return resp
        except Exception as e:
            print(e)


@app.route('/newsp.html')
def call_news_pat():
    if session["username"] != None and session["username"][0:3] == "PAT":
        response = requests.get(
            "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey="+config.ak6)
        news = response.json()
        return render_template('patient/news.html', news=news['articles'])


@app.route('/profile.html')
def call_profile_pat():
    if session["username"] != None and session["username"][0:3] == "PAT":
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT name,email,phone,gender,date from patient where pid=%s", (session["username"],))
        rows = cursor.fetchone()
        l = [i for i in rows]
        return render_template('patient/profile.html', prof=l)


@app.route('/video.html')
def call_video_pat():
    if session["username"] != None and session["username"][0:3] == "PAT":
        cursor = mysql.connection.cursor()
        today = date.today()
        d = today.strftime("%y-%m-%d")
        h = today.strftime("%H")
        cursor.execute(
            "SELECT url from event where pid=%s and DATE(start_date) = %s and HOUR(TIME(start_date))>=%s order by start_date", (session["username"], d, h,))
        rows = cursor.fetchone()
        if rows == None:
            return render_template('patient/connect.html', er="No meeting found, please wait for your slot timing...")
        return redirect(rows[0])


if __name__ == '__main__':
    app.run()
