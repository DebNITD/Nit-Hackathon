# Nit-Hackathon

Welcome to Project ................MaapYantra................

================================================Problem Statement================================================================
Development of an Online Verification System for Weighing and Measuring Instruments


============================================Real Life Problem-Our Story==========================================================

Imagine a shopkeeper, Rahul, who needs his weighing machine verified.

Today:
Rahul → paperwork/application → waiting → admin processes it → officer gets assigned → physical verification → manual calculations → paper certificate.

This creates delays, paperwork, difficulty tracking applications, and chances of manual errors.

=======================================================Our Solution==============================================================

We build one online verification platform:

Owner → Registers instrument
→ Uploads documents
→ Applies for verification

Admin → Reviews application
→ Assigns verification officer

Officer → Views assigned instrument
→ Performs verification
→ Enters test readings
→ System helps calculate errors/result

System → Generates digital certificate
→ Adds QR code

Public/Owner → Scans QR → checks whether the certificate is genuine/valid

====================================================Methodology==================================================================
Development of an Online Verification System for Weighing and Measuring Instruments:
(Smart Automation, Ministry of
Consumer Affairs,Food & Public)

Everyday business, selling buying of goods, essential commodities, heavily depends on accurate usage of proper Instruments. Without Instruments daily life becomes ugly. However, getting it verified can involve a cumbersome process.

We propose an Online Verification System for Measuring Instruments to make the process simpler,faster, more transparent. Especially making it available to local shops and businesses. People from rural areas can access our website with their smart phones, and login to their profiles using Aadhar ID and phone number. Users will make their account with email, username and password. All data about owner's Instruments will be added to their profiles.

At present, verifying instrument involves  complicated paperwork, huge time processing,offline reporting, creating extra work for both owners and verification officers.  

Our project provides a single easy-to-use digital platform connecting all users and Verification Officers. The Officer can view all data provided by user, perform verification tests and publish the result.

After successful verification , a digital certificate can be generated with a QR code. The QR code sent in a PDF can be scanned to check the certificate and all data submitted. This reduces paperwork, improves efficiency and simplifies verification process.

=================================================How to Use This=================================================================
# 👨‍⚖️ How to Use PARAKH — For Judges & Evaluators

## 📌 Project Overview

PARAKH is an online verification system for weighing and measuring instruments.

The system digitizes the complete verification workflow:
Register Instrument
        ↓
Submit Verification Application
        ↓
Application Review
        ↓
Officer Assignment
        ↓
Field Verification
        ↓
Enter Test Readings
        ↓
Automatic Error Calculation
        ↓
PASS / FAIL
        ↓
Digital Certificate
        ↓
QR-based Verification

💻 System Requirements

To run and evaluate the project, the following are recommended:

Windows / Linux / macOS
Python 3.x
Node.js 18+
Git
Internet connection
Modern web browser

No special hardware is required to run the software prototype.

📥 1. Clone the Repository

Open a terminal / command prompt and run:

git clone https://github.com/DebNITD/Nit-Hackathon.git

Enter the project directory:

cd Nit-Hackathon
📁 2. Project Structure

The project is organized into the following major components:
Nit-Hackathon/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── docs/
│   └── ...
│
├── README.md
└── .gitignore

⚙️ 3. Start the Backend

Open a terminal inside the backend directory:

cd backend

Create a Python virtual environment:

python -m venv .venv
Windows

Activate the virtual environment:

.venv\Scripts\activate
Linux / macOS
source .venv/bin/activate

Install the required Python packages:

pip install -r requirements.txt

Start the FastAPI backend:

python -m uvicorn main:app --reload

The backend will run at:

http://127.0.0.1:8000
