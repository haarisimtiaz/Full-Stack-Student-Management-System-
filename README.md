Full Stack Student Management System
A full stack web application for managing student records, built as a first-year engineering project..
Originally developed as a C++ console application, then converted into a live web application with a Python backend and deployed to the cloud.
Live Demo at: **[https://web-production-ca379.up.railway.app](https://web-production-ca379.up.railway.app)**
Features:
1) Student Portal
- Login with Roll Number
- View personal profile and grades
- Subject-wise performance analysis
- Compare marks against section average
- View section grade distribution statistics

2) Admin Portal (Admin password is: Admin@123)
- Password protected admin access
- View all student records
- Search by Roll Number, Section, or Grade
- Add new student records
- Update existing records
- Delete records

Tech Stack:
Frontend: HTML, CSS, JavaScript
Backend: Python (Flask) 
Data Storage: Text file (SampleData.txt) 
Deployment: Railway.app 
Version Control: Git & GitHub

How to Run Locally:
1 — Copy the repository:
git clone https://github.com/haarisimtiaz/Full-Stack-Student-Management-System-.git
cd Full-Stack-Student-Management-System-

2 — Install dependencies:
pip install flask

3 — Run the app:
python app.py

4 — Open in browser:
http://localhost:8080

Project Journey:
This project went through 5 major phases:

1. C++ Console App — original application with cin/cout and text file storage
2. Web Conversion — C++ backend with cpp-httplib + HTML/JS frontend
3. Windows Debugging — fixed linker errors, MinGW path issues, CORS problems
4. CORS Fix — added Access-Control-Allow-Origin headers, served HTML from backend
5. Cloud Deployment — rewrote backend in Python (Flask), deployed to Railway via GitHub

Grade Calculation Formula

ENA: 40% 
CP: 30% 
Ideology: 10%
Quran: 10% 
Islamiat: 10% 

90 - 100: A 
80 - 89: B 
60 - 79: C 
40 - 59: D 
Below 40: F 

License:
This project is open source and available under the [MIT License](LICENSE).
