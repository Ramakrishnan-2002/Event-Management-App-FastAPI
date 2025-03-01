
Planify - Event Creation, Management, and Tracking App
A full-stack web application for event and task creation and tracking, built using FastAPI, HTML, CSS, JavaScript, and SQLite3. The app allows users to create, manage, and keep track of events and tasks (personal, professional, travel-related, or anything else) while receiving email notifications about event creation and reminders.

✨ Features
✅ Event Creation & Management – Users can create events with a name, date, time, and description.
✅ User Authentication – Secure login with JWT-based authentication.
✅ Email Notifications – Email alerts for event creation and upcoming reminders.
✅ Real-Time Event Countdown – Displays a countdown timer for each event.
✅ User-Friendly UI – Simple and intuitive interface using HTML, CSS, and JavaScript.
✅ Backend API – RESTful API with CRUD operations using FastAPI.
✅ SQLite3 Integration – Lightweight database for local storage.
🛠 Tech Stack
Frontend (event-frontend 🎨)
HTML5 – Structure of the web pages
CSS3 – Styling and responsive design
Vanilla JavaScript – Interactivity and event handling
Backend (event-backend 🛢️)
FastAPI – High-performance backend API
SQLite3 – Lightweight database storage
SQLAlchemy – ORM for database interaction
JWT Authentication – Secure login system
Pydantic – Request validation
Jinja2 – Templating and rendering HTML pages
Uvicorn – ASGI server for running FastAPI
🚀 Deployment
Frontend & Backend – Deployed on Render



📜 How to Run Locally

    1️⃣ Clone the repository
    
    git clone https://github.com/your-username/Event-Management-App-FastAPI.git
    cd Event-Management-App-FastAPI
    
    2️⃣ Create a Virtual Environment & Install Dependencies
    
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    3️⃣ Run the Application
    
    uvicorn main:app --reload
    4️⃣ Access the App : https://event-management-app-fastapi.onrender.com/
