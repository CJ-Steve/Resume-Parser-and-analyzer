import re
import spacy
from pdfminer.high_level import extract_text
from spacy.matcher import Matcher
import argparse

nlp = spacy.load("en_core_web_sm")

def process_resume(file_path):
    extracted_text = extract_text(file_path)
    return extracted_text
def extract_contact_number_from_resume(text):
    if text == '':
        return None

    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number
def extract_skills_from_resume(text, skills_list):
    extracted_skills = []

    for skill in skills_list:
        # Use case-insensitive search for each skill in the text
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            extracted_skills.append(skill)
    return extracted_skills

def extract_soft_skills_from_resume(text, soft_skills_list):
    extracted_soft_skills = []

    for soft_skill in soft_skills_list:
        # Use case-insensitive search for each skill in the text
        if re.search(r'\b' + re.escape(soft_skill) + r'\b', text, re.IGNORECASE):
            extracted_soft_skills.append(soft_skill)

    return extracted_soft_skills

def extract_hobbies_from_resume(text, hobby):
    hobbies = []

    for ho in hobby:
        if re.search(r'\b' + re.escape(ho) + r'\b', text, re.IGNORECASE):
            hobbies.append(ho)

    return hobbies
def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email
def extract_education_from_resume(text, education_keywords):
    education = []

    # List of education keywords to match against

    for keyword in education_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        match = re.search(pattern, text)
        if match:
            education.append(match.group())

    return education
def extract_name_from_resume(text):
    doc = nlp(text)

    # Initialize a variable to store the first detected full name
    name = None
    
    # Initialize a flag to indicate if we are currently extracting a full name
    extracting_name = False
    
    # Iterate over the tokens in the text
    for token in doc:
        # If the token is labeled as "PERSON" and we are not already extracting a name
        if token.ent_type_ == "PERSON" and not extracting_name:
            # Start extracting the full name
            name = token.text
            extracting_name = True
        # If the token is labeled as "PERSON" and we are currently extracting a name
        elif token.ent_type_ == "PERSON" and extracting_name:
            # Append the token to the full name
            name += " " + token.text
        # If the token is not labeled as "PERSON" and we are currently extracting a name
        elif token.ent_type_ != "PERSON" and extracting_name:
            # Stop extracting the full name
            break
    return name


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        text = extract_text(file)
    return text

if __name__ == '__main__':

    text = ""
    
    contact_number = extract_contact_number_from_resume(text)
    if contact_number:
        print("Contact Number:", contact_number)
    else:
        print("No contact number found")

    
    email = extract_email_from_resume(text)
    if email:
        print("Email:", email)
    else:
        print("No email found")

    
    education_keywords = ['Bsc', 'B. Pharmacy', 'B Pharmacy', 'Msc', 'M. Pharmacy', 'Ph.D', 'Bachelor', 'Master','B.sc','M.sc','MCA','M.Tech','M.tech']
    education = extract_education_from_resume(text, education_keywords)
    if education:
        print("Education:", education)
    else:
        print("No education found")

    

    name = extract_name_from_resume(text)

    if name:
        print("Name:", name)
    else:
        print("Name not found")


    soft_skills_list = ['communication']
    extracted_soft_skills = extract_soft_skills_from_resume(text, soft_skills_list)

    if extracted_soft_skills:
        print("Skills:", extracted_soft_skills)
    else:
        print("No skills found")
    


    skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau', 'Clojure', 'Python', 'Go', 'Java', 'LaTeX', 'NodeJS','Clojure', 'Django', 'Express','React.js', 'jQuery', 'Bootstrap', 'Bulma', 'HTML5','HTML', 'SASS','Wordpress', 'Wagtail', 'dokuWiki', 'Ghost', 'Drupal', 'Hugo','Ansible', 'Bash', 'supervisord', 'awk', 'sed cron', 'systemd', 'ZFS','Ubuntu', 'Arch Linux','Linux', 'OpenSUSE', 'Debian', 'Gentoo', 'FreeBSD','OSM Data processing', 'QGIS', 'JOSM', 'PostGIS','Postgresql', 'MySQL', 'MariaDB', 'SQLite' ,'NoSQL', 'MongoDB', 'ElasticSearch','Fail2Ban', 'iptables', 'LetsEncrypt', 'Tor', 'ufw', 'OpenSSH', 'rsync', 'Nginx', 'Apache', 'Gunicorn', 'Jetty', 'uWSGI', 'Immutant','Azure', 'AWS', 'Inkscape', 'Git']
    extracted_skills = extract_skills_from_resume(text, skills_list)

    if extracted_skills:
        print("Skills:", extracted_skills)
    else:
        print("No skills found")
        
    

    hobby = ["Reading","Writing","Drawing","Painting","Photography","Cooking","Baking","Gardening","Hiking","Cycling","Running","Swimming","Yoga","Meditation","Traveling","travelling","Camping","Fishing","Knitting","Crocheting","Sewing","Woodworking","Pottery","Playing Guitar","Playing Piano","Singing","Dancing","Acting","Video Gaming","Board Games","Puzzles","Chess","Martial Arts","Bird Watching","Astronomy","Volunteering","Blogging","Vlogging","Podcasting","DIY Projects","Collecting Stamps","Collecting Coins","Collecting Antiques","Scrapbooking","Origami","Calligraphy","Language Learning","Playing Tennis","Playing Soccer","Playing Basketball","Playing Baseball","Playing Volleyball","Surfing","Snowboarding","Skiing","Skateboarding","Rollerblading","Mountain Climbing","Rock Climbing","Scuba Diving","Snorkeling"]
    hobbies = extract_hobbies_from_resume(text, hobby)
    if hobbies:
        print("Hobbies :", hobbies)
    else:
        print("No Hobbies found")
        
