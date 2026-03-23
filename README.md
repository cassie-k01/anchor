# ⚓ ANCHOR
### Anonymous Peer Support Platform for ALU Students

ANCHOR is a web-based platform that allows African Leadership University students to anonymously share experiences, seek advice, and support each other. It addresses the stigma around mental health and academic struggles by providing a safe, peer-driven space.

---

## Tech Stack

- **Backend:** Python / Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** JWT (JSON Web Tokens)
- **Password Security:** Bcrypt

---

## Project Structure
```
anchor/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── __init__.py      # App factory
│   └── config.py        # Configuration
├── frontend/
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   ├── index.html       # Login & Register
│   ├── feed.html        # Posts feed
│   ├── post.html        # Single post & comments
│   ├── create-post.html # Create a post
│   ├── resources.html   # Resources page
│   └── admin.html       # Moderation dashboard
├── run.py               # Entry point
└── requirements.txt     # Dependencies
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/cassie-k01/anchor.git
cd anchor
```

### 2. Create and activate a virtual environment
```bash
# Mac / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python run.py
```

The server will start at **http://localhost:5000**

### 5. Open the app
Go to your browser and open:
```
http://localhost:5000/frontend/index.html
```

---

## Using the App

### As a Student
- Register with your ALU email (`@alustudent.com` or `@alustaff.com`)
- Browse the anonymous feed
- Create posts anonymously or with your name
- Comment and reply to other posts
- Report harmful content
- Browse resources shared by senior students

### As a Moderator
- Login with a moderator account
- Access the admin dashboard
- Review, resolve and act on reported content
- Remove harmful posts or comments
- Suspend users who violate community guidelines

### Creating a Moderator Account
Register a normal account first, then run this command to upgrade it:
```bash
python -c "from app import create_app, db; from app.models.user import User; app = create_app(); app.app_context().push(); user = User.query.filter_by(email='your@email.com').first(); user.role = 'moderator'; db.session.commit(); print('Done!')"
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register a new student |
| POST | /api/auth/login | Login and get JWT token |
| GET  | /api/auth/me | Get current user info |
| GET  | /api/posts | Get all posts |
| POST | /api/posts | Create a post |
| GET  | /api/posts/:id | Get a single post |
| GET  | /api/posts/:id/comments | Get comments for a post |
| POST | /api/posts/:id/comments | Add a comment |
| POST | /api/reports | Submit a report |
| GET  | /api/admin/reports | View reports (moderator only) |
| GET  | /api/resources | Get all resources |
| POST | /api/resources | Add a resource (mentor/admin only) |

---

## User Roles

| Role | Permissions |
|------|-------------|
| Student | Post, comment, report content |
| Mentor | Everything above + add resources |
| Moderator | Everything above + manage reports, remove content, suspend users |
| Admin | Full access |

---

## Author
**Cassie Keza Kivuye**
