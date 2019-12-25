from flask import Flask, render_template,url_for,request,redirect
import smtplib
from email.message import EmailMessage
import csv
from string import Template
from pathlib import Path #os.path
app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def about(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt',mode='a') as database:
        email = data['email']
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'\n{email},{subject},{message}')

def write_to_csv(data):
    with open('database.csv', newline='', mode='a') as database2:
        email = data['email']
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])
def send_email(data):
    email = EmailMessage()
    email['from'] = 'xiaoshiyilangtxy@gmail.com'
    email['to'] = 'yuan1z@bu.edu'
    email['subject'] = data['email'] +" subject "+ data['subject']
    email.set_content(data['message'])

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('', '')
        smtp.send_message(email)
    return None

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        #send_email(data)
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return "something is wrong here"