# 🤖 Multifunctional Telegram Bot with Django Admin Panel

## 📋 Project Description

A Telegram bot built with Python that serves as a personal assistant: it evaluates mathematical expressions, delivers random motivational quotes, and stores the user's calculation history. Every user interaction is logged to a SQLite database via Django ORM, and administrators can monitor activity through the built-in Django admin panel.

---

## 🛠 Technologies Used

| Technology       | Version  | Purpose                   |
|---               |---       |---                        |
| Python           | 3.14     | Core programming language |
| pyTelegramBotAPI | 4.21.0   | Telegram Bot API wrapper  |
| Django           | 5.0.6    | ORM + admin panel         |
| SQLite           | built-in | Data storage              |

---

## 📁 Project Structure

```
project/
├── adminpanel/              # Django settings package
│   ├── __init__.py
│   ├── settings.py          # Settings (DB, apps, language)
│   ├── urls.py              # URL routes (admin)
│   └── wsgi.py
├── queries/                 # Django application
│   ├── migrations/          # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Admin panel configuration
│   ├── apps.py
│   └── models.py            # UserQuery model
├── db.sqlite3               # SQLite database
├── manage.py                # Django CLI
├── quotes.json              # Quotes data file
├── requirements.txt         # Dependencies
├── tg_bot.py                # Main bot file
└── README.md
```

---

## ⚙️ Installation Guide

### 1. Download and extract the project archive

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser for the admin panel

```bash
python manage.py createsuperuser
```

---

## 🚀 Running the Project

### Start the Telegram bot

```bash
python tg_bot.py
```

You will see in the terminal: `Bot is running...`

### Start the Django admin panel (in a separate terminal)

```bash
python manage.py runserver
```

Open in your browser: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 💬 Bot Commands and Examples

| Command / Input    | Description                      | Example Response                                |
|---                 |---                               |---                                              |
| `/start`           | Greeting and command list        | `Hello, Alex! 👋 I'm a multifunctional bot...` |
| `/help`            | Help information                 | List of all commands with descriptions          |
| `/calc 2+2`        | Evaluate an expression           | `🧮 2+2 = 4`                                    |
| `/calc sqrt(16)`   | Square root                      | `🧮 sqrt(16) = 4`                               |
| `/calc sin(pi/2)`  | Trigonometry                     | `🧮 sin(pi/2) = 1`                              |
| `/quote`           | Random motivational quote        | `💬 Knowledge is power. — Francis Bacon`        |
| `/history`         | Last 10 calculations             | List with date and result                       |
| `/clear`           | Clear calculation history        | `🗑 History cleared (5 records deleted).`        |
| `2 * (3 + 4)`      | Auto-calculation without command | `🧮 2 * (3 + 4) = 14`                           |
| Unknown text       | Unknown command handling         | `❓ Unknown command. Type /help`                |

### Supported Mathematical Functions

```
+, -, *, /    — basic arithmetic
^             — exponentiation  (2^10 = 1024)
sqrt(x)       — square root
sin(x)        — sine
cos(x)        — cosine
tan(x)        — tangent
log(x)        — natural logarithm
log10(x)      — base-10 logarithm
abs(x)        — absolute value
round(x)      — rounding
pi            — π ≈ 3.14159
e             — Euler's number ≈ 2.71828
```

---

## 🗄 Data Storage

Every user request is saved to the SQLite database. The `UserQuery` model stores:

- `user_id` — Telegram user ID
- `username` — Telegram username (@username)
- `first_name` — user's first name
- `command` — command type (`/calc`, `/quote`, `/history`, etc.)
- `text` — full message text
- `result` — bot's response
- `created_at` — date and time of the request

---

## 🛡 Error Handling

| Situation           | Bot Behavior                                               |
|---                  |---                                                         |
| Division by zero    | `Error: division by zero`                                  |
| Invalid expression  | `Error: invalid expression`                                |
| Empty `/calc` input | `✏️ Please provide an expression. Example: /calc 2 + 2`    |
| Empty history       | `📋 History is empty.`                                     |
| Unknown command     | `❓ Unknown command. Type /help`                           |

---

## 🖥 Admin Panel

The Django admin panel allows viewing all user requests with:

- Filtering by command type and date
- Search by username and message text
- Date hierarchy navigation
- Detailed view of each individual request

URL: ` `

---

## 👤 Author
This project was developed as a final assignment for the course **"Programming in Python"**.
