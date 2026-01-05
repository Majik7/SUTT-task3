# StudyDeck Forum

Akshat Ranjan

---

## Setup Instructions

Follow these steps to set up the project locally on your machine.

### 1. Prerequisites
- Python
- Git

### 2. Virtual Environment & Installation
Clone the repository and set up the Python environment:
```bash
git clone <your-repo-url>
cd studydeck_forum

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Environment Variables
Put this in a .env file
```env
GOOGLE_CLIENT_ID = google_client_id
GOOGLE_CLIENT_SECRET = google_client_secret
EMAIL-ADDRESS = email_id_to_send_notifs_from
EMAIL-APP-PASSWORD = gmail_app_password
POSTGRES-EXTERNAL-URL = ...
POSTGRES-INTERNAL-URL = ...
ALLOWED_HOSTS = allowed hosts separted by space
DEBUG = True
```

### 4. Database Migrations
Run the migrations to set up your local database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Running the Application
To start the local development server, run:
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000 in a browser

## 🛠 Feature Walkthrough

### Authentication
* **Google OAuth Integration:** The platform is configured to restrict sign-ups to `@bits-pilani.ac.in` email domains.
* **User Profiles:** Every student has a dedicated profile page

### Forum & Discussions
* **Thread Creation:** Users can initiate discussions by making threads
* **Real-time Interaction:** Post authors are notified via email when their posts receive comments
