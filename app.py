import sys
from flask import Flask, request, render_template, redirect, url_for
import os
from resume_parser import process_resume
from werkzeug.utils import secure_filename
from resume_parser import *
import csv
import io
import requests
import json
import base64
import matplotlib.pyplot as plt

sys.setrecursionlimit(3000)

app = Flask(__name__)


UPLOAD_FOLDER = 'C:/nlp_project/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSION = {'pdf', 'txt','docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

def check_duplicate_email(email):
    with open('database.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == email:  # Assuming email is in the second column
                return True
    return False

def insert_data_to_csv(name, email, contact_number, education, skills, soft_skills, hobbies):
    if check_duplicate_email(email):
        print(f"Email {email} already exists in the database. Skipping insertion.")
        return

    data = [[name, email, contact_number, education, skills, soft_skills, hobbies]]

    with open('database.csv', 'a', newline='') as file:
        write = csv.writer(file)
        write.writerows(data)
        print(f"Data for {email} inserted successfully.")

extracted_soft_skills=[]
extracted_skills=[]
education=[]

def plot_bar_chart(extracted_skills, extracted_soft_skills, education):
    # Count the number of elements in the lists
    skills_count = len(extracted_skills)
    soft_skills_count = len(extracted_soft_skills)
    education_count = len(education)

    # Data for plotting
    x_labels = ['Skills', 'Soft Skills', 'Education']
    y_values = [skills_count, soft_skills_count, education_count]

    # Plotting the bar chart
    plt.bar(x_labels, y_values, color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Count')
    plt.title('Counts of Skills, Soft Skills, and Education')

    # Adding the count values on top of the bars
    for i, v in enumerate(y_values):
        plt.text(i, v + 0.1, str(v), ha='center')

    # Save the plot to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    return image_png


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/submit', methods=['POST'])
def submit():
    return render_template("parsing_page.html")

@app.route('/dashboard', methods=['POST'])
def disp():
    if request.method == 'POST':
        return render_template('dashboard.html',name=name,email=email,contact_number=contact_number,education=education,extracted_skills=extracted_skills,extracted_soft_skills=extracted_soft_skills,hobbies=hobbies)
        
@app.route('/back', methods=['POST'])
def back():

    return render_template('index.html')

@app.route('/analyzer', methods=['POST'])
def analyze():
    image = plot_bar_chart(extracted_skills, extracted_soft_skills, education)
    return f'<img src="data:image/png;base64,{base64.b64encode(image).decode()}">'

@app.route('/upload', methods=['POST'])
def upload_file():


    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the uploaded file
        text = extract_text_from_pdf(file_path)
        education_keywords = ['Bsc', 'B. Pharmacy', 'Msc', 'Ph.D', 'Bachelor', 'Master','B.sc','M.sc','MCA','M.Tech','B.Tech','M.tech']
        skills_list = ['Data Analysis','Arduino','embedded C','js','c','c++', 'Machine Learning',"PHP", "JavaScript"  ,"Oracle DB ",'Deep Learning', 'SQL', 'Tableau', 'Clojure', 'Python', 'Go', 'Java', 'LaTeX', 'NodeJS','Clojure', 'css','Django', 'Express','React.js', 'jQuery', 'Bootstrap', 'Bulma', 'HTML5','HTML', 'SASS','Wordpress', 'Wagtail', 'dokuWiki', 'Ghost', 'Drupal', 'Hugo','Ansible', 'Bash', 'supervisord', 'awk', 'sed cron', 'systemd', 'ZFS','Ubuntu', 'Arch Linux','Linux', 'OpenSUSE', 'Debian', 'Gentoo', 'FreeBSD','OSM Data processing', 'QGIS', 'JOSM', 'PostGIS','Postgresql', 'MySQL', 'MariaDB', 'SQLite' ,'NoSQL', 'MongoDB', 'ElasticSearch','Fail2Ban', 'iptables', 'LetsEncrypt', 'Tor', 'ufw', 'OpenSSH', 'rsync', 'Nginx', 'Apache', 'Gunicorn', 'Jetty', 'uWSGI', 'Immutant','Azure', 'AWS', 'Inkscape', 'Git','data structure']
        hobby = ["Reading","Writing","Drawing","Painting","Photography","Cooking","Baking","Gardening","Hiking","Cycling","Running","Swimming","Yoga","Meditation","Traveling","travelling","Camping","Fishing","Knitting","Crocheting","Sewing","Woodworking","Pottery","Playing Guitar","Playing Piano","Singing","Dancing","Acting","Video Gaming","Board Games","Puzzles","Chess","Martial Arts","Bird Watching","Astronomy","Volunteering","Blogging","Vlogging","Podcasting","DIY Projects","Collecting Stamps","Collecting Coins","Collecting Antiques","Scrapbooking","Origami","Calligraphy","Language Learning","Playing Tennis","Playing Soccer","Playing Basketball","Playing Baseball","Playing Volleyball","Surfing","Snowboarding","Skiing","Skateboarding","Rollerblading","Mountain Climbing","Rock Climbing","Scuba Diving","Snorkeling"]
        soft_skills_list = ["Communication","Creative writing","Problem solving" , "Teamwork", "Problem-solving", "Adaptability", "Creativity", "Leadership", "Critical Thinking", "Emotional Intelligence", "Conflict Resolution","Decision Making", "Active Listening", "Empathy", "Stress Management", "Networking","Negotiation", "Collaboration", "Attention to Detail", "Interpersonal Skills", "Flexibility","Resilience", "Open-mindedness", "Patience", "Public Speaking", "Customer Service","Organizational Skills", "Self-Motivation", "Positive Attitude", "Professionalism", "Time Management","Work Ethic", "Adaptability", "Work-Life Balance", "Conflict Management", "Cultural Awareness","Ethical Decision Making", "Feedback Acceptance", "Goal Setting", "Innovation", "Mentoring","Persuasion", "Risk Management", "Self-Confidence", "Strategic Thinking", "Tolerance","Workplace Diversity"]

        

        # Extract information from the text
        contact_number = extract_contact_number_from_resume(text)
        email = extract_email_from_resume(text)
        global education
        education = extract_education_from_resume(text, education_keywords)
        name = extract_name_from_resume(text)
        global extracted_skills
        extracted_skills = extract_skills_from_resume(text, skills_list)
        global extracted_soft_skills
        extracted_soft_skills = extract_soft_skills_from_resume(text, soft_skills_list)
        hobbies = extract_hobbies_from_resume(text, hobby)



        #insert extracted text
        insert_data_to_csv(name, email, contact_number, education, extracted_skills, extracted_soft_skills, hobbies)

        return render_template('dashboard.html', name=name, email=email, contact_number=contact_number, education=education, extracted_skills=extracted_skills,extracted_soft_skills=extracted_soft_skills, hobbies=hobbies)

    return "Invalid file format"



@app.route('/redir', methods=['POST'])
def redir():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
