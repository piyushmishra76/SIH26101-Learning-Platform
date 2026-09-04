# SIH26101 — AI-Enabled Learning Platform for Statistical Capacity Building

Backend prototype for **SIH26101**, an AI-enabled learning platform intended to strengthen capacity building within India's Official Statistical System.

The current implementation provides the core backend foundation: authentication, role-based authorization, competency profiles, skill-gap calculation, course cataloguing, recommendation logic, training history, and quiz creation/evaluation. The document-to-MCQ AI pipeline and external iGOT integration are planned next and are **not represented as completed features** in this README.

## Current Backend Status

### Implemented
- FastAPI application with Swagger/OpenAPI documentation
- SQLite database with SQLAlchemy ORM
- User registration and login
- Password hashing using `pwdlib` with Argon2
- JWT-based authentication
- Protected user profile endpoint
- Role-based authorization for learners, trainers, and admins
- Competency catalogue
- User competency scores and competency levels
- Skill-gap calculation
- Course catalogue
- Course-to-competency mapping
- Rule-based personalized course recommendation engine (V1)
- Training history tracking
- Quiz, question, and quiz-attempt data models
- Quiz creation and question management
- Published-quiz question retrieval
- Quiz submission and score calculation
- Competency score update from quiz performance
- Database seed script for initial competencies and courses

### Planned / In Progress
- AI generation of MCQs and quizzes from uploaded PDF/PPT/DOCX learning material
- Document text extraction, chunking, and validation pipeline
- AI-generated-question review/approval workflow
- Advanced recommendation signals such as training history and semantic similarity
- iGOT Karmayogi integration through an integration/adapter layer
- NSSTA course/training integration as supported by available interfaces/data
- Admin analytics and workforce-level dashboards
- Database migrations with Alembic
- Production deployment, monitoring, and centralized logging

## Architecture

```text
                    Frontend
                       |
                       v
                  FastAPI Backend
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
 Authentication   Core APIs      Recommendation
        |              |              |
        v              v              v
       JWT         SQLAlchemy     Skill-gap logic
                       |              |
                       +------+-------+
                              |
                              v
                         SQLite (dev)
```

Planned AI flow:

```text
Learning Material (PDF/PPT/DOCX)
                |
                v
        Text Extraction
                |
                v
       Cleaning / Chunking
                |
                v
          LLM / AI Layer
                |
                v
       Structured MCQs/Quiz
                |
                v
          Validation/Review
                |
                v
       Questions + Quiz DB
                |
                v
         Learner Assessment
                |
                v
       Competency Update
                |
                v
      Skill Gap Recalculation
                |
                v
        New Recommendations
```

## Repository Structure

```text
SIH26101/
|
+-- SIH26101_backend/
|   |
|   +-- app/
|   |   +-- api/
|   |   |   +-- auth.py
|   |   |   +-- users.py
|   |   |   +-- competencies.py
|   |   |   +-- courses.py
|   |   |   +-- recommendations.py
|   |   |   +-- quizzes.py
|   |   |   +-- admin.py
|   |   |
|   |   +-- database/
|   |   |   +-- connection.py
|   |   |
|   |   +-- models/
|   |   |   +-- user.py
|   |   |   +-- competency.py
|   |   |   +-- course.py
|   |   |   +-- training.py
|   |   |   +-- quiz.py
|   |   |
|   |   +-- schemas/
|   |   +-- services/
|   |   +-- utils/
|   |   +-- main.py
|   |
|   +-- seed.py
|   +-- requirements.txt
|   +-- .gitignore
|   +-- venvBackend/        # local only; not committed
|   +-- sih26101.db         # local development DB; not committed
|
+-- SIH26101_frontend/      # planned / team frontend
+-- docs/                    # planned project documentation
+-- README.md
```

> **Note:** On the current Windows development setup, the database package may appear as `Database` rather than `database`. Keep import paths consistent with the actual folder name on your checkout. For production/Linux, using lowercase package names consistently is recommended.

## Technology Stack

### Backend
- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite (development)
- PyJWT
- pwdlib + Argon2

### Planned AI / Data Layer
- PDF/PPT/DOCX parsing
- LLM API
- Embeddings / vector retrieval where needed
- Structured JSON validation for generated questions

## Local Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SIH26101/SIH26101_backend
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venvBackend
.\venvBackend\Scripts\Activate.ps1
```

If the environment already exists:

```powershell
.\venvBackend\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Seed development data

The seed script inserts the initial competency and course catalogue used by the current recommendation prototype.

```bash
python seed.py
```

Expected output:

```text
Database seeded successfully.
```

### 5. Start the API

```bash
uvicorn app.main:app --reload
```

API base URL:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Core API Endpoints

The exact endpoint set may evolve as the project develops. The current backend includes the following core routes.

### Authentication

```http
POST /auth/register
POST /auth/login
```

### User

```http
GET  /users/me
POST /users/me/competencies
GET  /users/me/competencies
GET  /users/me/skill-gaps
GET  /users/me/recommendations/
```

### Competencies

```http
GET  /competencies/
POST /competencies/
```

### Courses

```http
GET  /courses/
POST /courses/
GET  /courses/{course_id}
POST /courses/{course_id}/competencies
```

### Quizzes

```http
POST /quizzes/
GET  /quizzes/
GET  /quizzes/{quiz_id}
POST /quizzes/{quiz_id}/questions
GET  /quizzes/{quiz_id}/questions
POST /quizzes/{quiz_id}/submit
```

### Admin

```http
GET /admin/users
```

Additional admin endpoints will be added as the admin workflow is completed.

## Authentication and Authorization

Authentication is JWT-based.

After login, the client receives an access token:

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

Protected endpoints use the HTTP `Authorization` header:

```http
Authorization: Bearer <JWT>
```

Current application roles:

```text
learner
trainer
admin
```

Authentication answers **who the user is**; authorization answers **what the user is allowed to do**.

## Recommendation Engine (V1)

The current recommendation engine is intentionally transparent and deterministic. It is **not a trained machine-learning recommender**.

Current flow:

```text
Current Competency
        |
        v
Required Competency
        |
        v
     Skill Gap
        |
        v
Find Courses Mapped to Competency
        |
        v
Remove Completed Courses
        |
        v
Calculate Recommendation Score
        |
        v
Rank Courses
        |
        v
Return Top Recommendations
```

The current scoring logic uses competency gap and course-level fit. This is a baseline that can later be extended with role relevance, quiz performance, training history, and semantic similarity.

## Competency Levels

The current backend maps percentage scores to competency levels as follows:

| Score | Level |
|---:|---:|
| 0–39 | 1 |
| 40–59 | 2 |
| 60–74 | 3 |
| 75–89 | 4 |
| 90–100 | 5 |

Skill gap is currently calculated as:

```text
max(required_level - current_level, 0)
```

## Quiz Evaluation

A quiz question can be linked to a competency. During submission, the backend:

1. Evaluates submitted answers against the stored correct answers.
2. Calculates the overall quiz score.
3. Groups performance by competency where `competency_id` is present.
4. Updates the learner's competency score and level.
5. Stores the quiz attempt.
6. Allows the recommendation engine to use the updated competency profile.

This creates the current adaptive-learning loop:

```text
Quiz Attempt
    -> Competency Performance
    -> Updated Competency Level
    -> New Skill Gap
    -> Updated Recommendation
```

## Seed Data

`seed.py` creates initial development data for competencies and courses and maps courses to competencies. It is intended for development/demo setup, not as a substitute for production data management.

The current seed data includes competencies such as:

- Sampling
- Survey Design
- Data Quality
- Statistical Analysis
- SDG Indicators
- Data Visualization

and example courses from iGOT/NSSTA-style sources used for prototype testing.

## Database

SQLite is used for the current development prototype because it is simple to run locally.

The development database file is intentionally ignored by Git:

```gitignore
*.db
```

The virtual environment is also ignored:

```gitignore
venvBackend/
```

Teammates should recreate the environment with `requirements.txt` and initialise development data with `python seed.py`.

For production, the project is expected to move to PostgreSQL and use Alembic migrations.

## Team Development Guidelines

Use feature branches instead of committing directly to `main` for larger changes.

Example:

```bash
git checkout -b feature/quiz-history
git add .
git commit -m "Add quiz history API"
git push origin feature/quiz-history
```

Then open a Pull Request for review.

Before starting new work:

```bash
git pull
```

Do **not** commit:

- `venvBackend/`
- `.env`
- `*.db`
- API keys or JWT secrets
- `__pycache__/`

## Current Scope vs. Target Scope

The project is being built incrementally.

### Current

The backend already provides the platform foundation needed for learners, competencies, courses, recommendations, and quizzes.

### Target

The complete SIH solution will add:

```text
Official/Employee Profile
        |
        v
Competency Assessment
        |
        v
Skill-Gap Identification
        |
        v
Personalized Training Recommendations
        |
        v
Learning Material Upload
        |
        v
AI MCQ / Quiz Generation
        |
        v
Trainer Review / Approval
        |
        v
Learner Assessment
        |
        v
Competency Update
        |
        v
Adaptive Recommendations
        |
        v
Admin / Workforce Analytics
```

## Project Disclaimer

This repository currently contains a **working prototype backend**, not a production-ready government deployment. Any future claim of iGOT integration, NSSTA integration, AI-generated assessment, production security, scalability, or deployment should be backed by the corresponding implemented service/interface and authorized access.
