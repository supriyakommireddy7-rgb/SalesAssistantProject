# Email AI Sales Assistant - Architecture

## Tech Stack
- **Frontend**: React, Vite, Tailwind CSS, React Router.
- **Backend**: Python Flask, Flask-SQLAlchemy.
- **Database**: MySQL.
- **APIs**: Gmail API, Google Gemini API.

## Workflow
1. The backend cron job (or manual sync via UI) uses the Gmail API to fetch unread emails.
2. The emails are parsed and saved to the MySQL database.
3. The content is sent to the Gemini API with a strict real estate prompt.
4. If Gemini replies confidently, the reply is sent back via Gmail API.
5. If Gemini is not confident or fails, the Rule Engine falls back to checking Knowledge Base FAQs.
6. If the Rule Engine fails, the email is marked as "Awaiting Human Response" for a Sales Executive.
7. Everything is logged in the Conversations and ActivityLogs tables.
