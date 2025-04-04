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
python manage.py makemigrations core
```
```sh
python manage.py migrate
```

### 6. Collect Static Files
```sh
python manage.py collectstatic
```
> If prompted with a warning about overwriting files, type `yes`.

### 7. Load Exercises to Database
```sh
python manage.py load_exercises
```

### 8. Run the Development Server
```sh
python manage.py runserver
```

### 9. Access the Application
Open a web browser and go to:
```
http://127.0.0.1:8000/
```

## Testing on Mobile

### 1. Run server
```sh
python manage.py runserver 0.0.0.0:8000
```
This allows connections from other devices on the same network.

### 2. Find your Local IP Address
On Windows, open Command Prompt and run:
```sh
ipconfig
```
On Mac/Linux, use:
```sh
ifconfig | grep inet
```
or
```sh
ip a | grep inet
```
Look for your IPv4 Address under your active network (e.g., `192.168.1.X`).

### 3. Connect Your Mobile Device to the Same Network
Make sure your mobile device is connected to the same Wi-Fi network as your development machine.

### 4. Open the Project on Your Mobile Browser
On your mobile device, open a browser (Chrome, Safari, Firefox) and enter:
```cpp
http://<your-ip>:8000/
```
Example:
```cpp
http://192.168.1.2:8000/
=======
## Reset Database Instructions
**WARNING: Only follow this if you wish to reset the database.**

### 1. Create a Backup of the Database
```sh
copy db.sqlite3 db_backup.sqlite3
```

### 2. Delete `__pycache__` and `\migrations` on all directories
Manually delete all `__pycache__` and `\migrations` on all directories

### 3. Apply Migrations
```sh
python manage.py makemigrations core
```
```sh
python manage.py migrate
```

### 4. Load Exercises to Database
```sh
python manage.py load_exercises
```

### 5. Create a superuser
```sh
python manage.py createsuperuser
```

## Reset Database Instructions
**WARNING: Only follow this if you wish to reset the database.**

### 1. Create a Backup of the Database
```sh
copy db.sqlite3 db_backup.sqlite3
```

### 2. Delete `__pycache__` and `\migrations` on all directories
Manually delete all `__pycache__` and `\migrations` on all directories

### 3. Apply Migrations
```sh
python manage.py makemigrations core
```
```sh
python manage.py migrate
```

### 4. Load Exercises to Database
```sh
python manage.py load_exercises
```

### 5. Create a superuser
```sh
python manage.py createsuperuser
```