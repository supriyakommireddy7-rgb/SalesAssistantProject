# Email AI Sales Assistant

A full-stack CRM application designed to automate real estate sales emails using AI.

## Features
- Fetches unread emails using Gmail API.
- Automatically generates replies using Google Gemini API.
- Rule-based fallback system via custom Knowledge Base FAQs.
- Human handover for complex queries.
- Admin dashboard to manage Customers, Emails, Knowledge Base, and Reports.

## Technology Stack
- React, Vite, Tailwind CSS
- Python, Flask, SQLAlchemy, MySQL

## Folder Structure
- `frontend/`: React Vite application
- `backend/`: Flask application
- `docs/`: Architecture documentation
- `tests/`: Unit tests

## Setup Instructions

### Database Setup
1. Install MySQL.
2. Create a database named `email_ai_sales`.

### Backend Setup
1. Navigate to the `backend/` directory.
2. Create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in:
   - MySQL connection details.
   - `JWT_SECRET`
   - `GEMINI_API_KEY`
5. Place your Gmail API `credentials.json` in the `backend/` directory.
6. Run the application: `python app.py`

### Frontend Setup
1. Navigate to the `frontend/` directory.
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

## API Overview
- `/api/auth/*`: Admin authentication.
- `/api/customers/*`: Customer CRUD operations.
- `/api/emails/*`: Email fetching, manual sync, manual reply.
- `/api/conversations/*`: View AI/Rule/Human conversation logs.
- `/api/knowledge_base/*`: FAQ CRUD.
- `/api/dashboard/*`: Key metrics for the dashboard.
- `/api/reports/*`: Generate and retrieve CSV reports.
