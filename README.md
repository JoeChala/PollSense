# PollSense — Dynamic Survey & Analytics Platform

PollSense is a production-style survey platform built with Django and FastAPI that allows administrators to create dynamic surveys with configurable question types, anonymous public submissions, real-time analytics dashboards, and Excel report exports.

The system is designed with a modular architecture and follows real-world SaaS backend patterns including dynamic form generation, data aggregation, abuse protection, and microservice integration.

---

## Features

### 🔹 Survey Builder (Admin)

- Create and manage surveys
- Configure survey limits (response limits, IP limits, time windows)
- Add dynamic questions with multiple question types
- Configure which questions generate charts

### 🔹 Dynamic Question Engine

- Supports multiple question types:
  - Text
  - Number
  - Multiple choice
  - Checkbox
  - Rating scale
- Dynamic form rendering
- Automatic validation
- Analytics-aware question mapping

### 🔹 Anonymous Public Submissions

- Public survey links
- Anonymous responses
- IP-based abuse protection
- Rate limiting
- Optional CAPTCHA support

### 🔹 Analytics Dashboard

- Real-time response tracking
- Automatic aggregation
- Configurable charts (bar, pie, line)
- Per-question statistics

### 🔹 Excel Export

- One-click export of survey results
- Clean tabular format
- Ready for Excel, PowerBI, or Google Sheets

### 🔹 Scalable Architecture

- Django backend for business logic & admin
- FastAPI microservice for analytics & exports
- PostgreSQL database
- Redis for caching & rate limiting
- Designed for Railway deployment

---

## Core Design

| App       | Description                       |
| --------- | --------------------------------- |
| surveys   | Survey creation and configuration |
| questions | Dynamic question engine           |
| responses | Anonymous submissions             |
| analytics | Statistics & chart generation     |
| exports   | Excel export system               |
| limits    | Abuse protection & rate limiting  |
| accounts  | Admin users & permissions         |
| common    | Shared utilities                  |

---

## Tech Stack

- **Backend:** Django, FastAPI
- **Database:** PostgreSQL
- **Caching & Rate Limiting:** Redis
- **Charts:** Chart.js
- **Exports:** OpenPyXL / Pandas
- **Deployment:** Railway
- **Containerization:** Docker

---

## 📂 Project Structure

```
pollsense/
├── manage.py
├── config/
├── surveys/
├── questions/
├── responses/
├── analytics/
├── exports/
├── limits/
├── accounts/
├── common/
├── templates/
├── static/
└── fastapi_service/
```

---



## Security & Abuse Protection

- IP hashing for anonymous users
- Survey response limits
- Rate limiting
- CAPTCHA support
- Encrypted database backups
