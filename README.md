# Lead Automation System

A web-based lead follow-up and appointment management system built with Python, Flask, SQLite, APScheduler, and Resend.

The application captures customer leads, allows businesses to manage lead statuses and appointments through a protected dashboard, and automatically sends follow-up and appointment reminder emails.

## Features

- Public lead submission form
- Password-protected business dashboard
- Lead status management
- SQLite database storage
- Appointment booking
- Double-booking prevention
- Automated lead follow-up emails
- Automated appointment reminder emails
- Follow-up tracking
- Reminder tracking to prevent duplicate reminders
- Background scheduling with APScheduler
- Email delivery using the Resend API
- Environment variables for sensitive credentials
- Timezone-aware scheduling
- Cloud deployment on Railway

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- APScheduler
- Resend API
- Railway
- Git / GitHub

## How It Works

1. A customer submits their contact information and requested service through the public web form.
2. The lead is stored in the SQLite database with a `NEW` status.
3. The business can log into the dashboard and update the lead's status.
4. When a lead is marked as `CONTACTED`, the system begins tracking follow-up timing.
5. Follow-up emails are automatically sent if the lead has not progressed.
6. The business can book an appointment through the dashboard.
7. The system automatically sends an appointment reminder before the scheduled appointment.
8. Follow-up and reminder information is stored in the database to prevent duplicate messages.

## Lead Statuses

The system currently supports:

- `NEW`
- `CONTACTED`
- `FOLLOW-UP`
- `BOOKED`
- `COMPLETED`
- `LOST`

## Project Structure

```text
lead-automation/
│
├── app.py
├── main.py
├── email_utils.py
├── requirements.txt
├── Procfile
├── README.md
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   └── login.html
│
└── static/
    └── style.css
```

## Environment Variables

The application uses environment variables for sensitive configuration.

Example:

```text
RESEND_API_KEY=your_resend_api_key
DASHBOARD_PASSWORD=your_dashboard_password
SECRET_KEY=your_secret_key
DATABASE_PATH=leads.db
```

Do not commit your `.env` file or API keys to GitHub.

## Local Setup

Clone the repository:

```bash
git clone <repository-url>
cd lead-automation
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file containing the required environment variables.

Run the application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The business dashboard is available at:

```text
http://127.0.0.1:5000/dashboard
```

Users who are not logged in are redirected to the dashboard