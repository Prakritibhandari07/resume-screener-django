# Resume Screening App — Django + Machine Learning

A full-stack Django web application that classifies resumes into job categories using a trained machine learning model (TF-IDF + classifier). Unlike a standalone notebook or quick Streamlit demo, this version includes user authentication and persistent prediction history backed by a database — closer to how ML models are actually deployed in production.

## Features

- 🔐 User authentication (signup/login/logout) using Django's built-in auth system
- 📄 Upload a resume (PDF or TXT) or paste text directly
- 🤖 ML-powered job category prediction using TF-IDF vectorization and a trained classifier
- 📊 Prediction history — every classification is saved to the database and tied to the logged-in user
- 🎯 24 job categories supported (IT, HR, Finance, Engineering, Healthcare, and more)

## Tech Stack

- **Backend:** Django 5.2
- **ML:** scikit-learn, TF-IDF vectorization
- **PDF parsing:** pypdf
- **Database:** SQLite (development)

## Project Structure
