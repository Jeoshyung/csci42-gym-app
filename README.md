# Trackfit Setup Guide

## Prerequisites
Make sure you have the following installed:
- Python (3.11 or later recommended)
- pip (Python package manager)
- virtualenv (for creating a virtual environment)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <repository_url>
cd <project_directory>
```

### 2. Create and Activate a Virtual Environment
```sh
python -m venv env  # Create virtual environment
```
#### **Windows:**
```sh
env\Scripts\activate  # Activate venv on Windows
```
#### **Mac/Linux:**
```sh
source env/bin/activate  # Activate venv on Mac/Linux
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Django Settings
In `settings.py`, ensure the following configurations:
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 5. Apply Migrations
```sh
python manage.py migrate
```

### 6. Collect Static Files
```sh
python manage.py collectstatic
```
> If prompted with a warning about overwriting files, type `yes`.

### 7. Run the Development Server
```sh
python manage.py runserver
```

### 8. Access the Application
Open a web browser and go to:
```
http://127.0.0.1:8000/
```
