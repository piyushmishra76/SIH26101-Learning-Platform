# SIH26101 — AI-Enabled Learning Platform for Statistical Capacity Building

Backend prototype for **SIH26101**, an AI-enabled learning platform intended to strengthen capacity building within India's Official Statistical System.

The platform is designed to support:

- Employee competency profiling
- Skill-gap identification
- Personalized training recommendations
- Course enrollment and progress tracking
- Competency-based assessments
- Learning analytics
- AI-generated quizzes from learning materials
- Future integration with iGOT Karmayogi and other learning resources

> > **Current status:** The core backend, learning-management functionality, document management, and AI-assisted assessment pipeline are implemented and tested. The platform currently supports PDF-based MCQ generation, trainer/admin review and approval, role-based AI access, and competency-aware question generation. Live iGOT integration, production deployment, and advanced personalization remain future work.

---

# Current Backend Status

## Implemented
### AI-Assisted Assessment Generation

- PDF text extraction
- Text cleaning
- Text chunking
- Gemini-based MCQ generation
- Structured MCQ output
- MCQ validation
- Exact duplicate removal
- AI-generated explanations
- Competency-aware question generation
- Trainer/admin-only AI generation
- Trainer/admin question approval
- Approved questions stored in the existing quiz question database
### Backend Foundation

- FastAPI application
- Swagger/OpenAPI documentation
- SQLite database for development
- SQLAlchemy ORM
- Pydantic schemas
- JWT-based authentication
- Password hashing using `pwdlib` with Argon2
- Role-based authorization
- Database seed script

### User & Authentication

- User registration
- User login
- JWT access tokens
- Protected user profile endpoint
- Learner, trainer, and admin roles
- User-specific protected APIs

### Competency Management

- Competency catalogue
- User competency profiles
- Competency scores
- Competency levels
- Skill-gap calculation
- Competency-based learning structure

### Course Management

- Course catalogue
- Course information
- Course-to-competency mapping
- Course difficulty and duration
- Course provider/source information
- External course URL support
- Active/inactive course status

### Recommendation Engine

- Rule-based personalized recommendation engine (V1)
- Skill-gap based course recommendations
- Course competency matching
- Completed-course filtering
- Recommendation scoring
- Recommendation ranking
- Top course recommendations

### Training Management

- Course enrollment
- Training progress tracking
- Training completion status
- Completion percentage tracking
- Training history
- User-specific training history
- Course completion timestamp

### Quiz & Assessment

- Quiz creation
- Question creation
- Question-to-competency mapping
- Published quiz retrieval
- Quiz question retrieval
- Quiz submission
- Automatic score calculation
- Quiz percentage calculation
- Competency performance calculation
- Competency score updates
- Quiz attempt storage
- User-specific quiz attempt history

### Learning Analytics

- Total courses enrolled
- Completed courses
- In-progress courses
- Average course completion percentage
- Total quiz attempts
- Average quiz percentage

### Document Management

- PDF document upload
- Document metadata storage
- Uploader tracking
- Document upload timestamp
- Document review status
- Trainer/admin document listing
- Document approval and rejection
- Learner document submission support
---

# Project Progress

## Phase 1 — Core Backend ✅

- [x] User authentication with JWT
- [x] Role-based authorization
- [x] User profiles
- [x] Competency profiles
- [x] Skill-gap calculation
- [x] Course catalogue
- [x] Course-competency mapping
- [x] Rule-based course recommendations
- [x] Quiz creation and evaluation
- [x] Database and seed data

## Phase 2 — Learning Platform

- [x] Course enrollment
- [x] Training progress tracking
- [x] Training history
- [x] Quiz attempt history
- [x] Learning analytics
- [x] Admin management

## Phase 3 — AI Assessment Pipeline

- [x] PDF upload
- [x] Document metadata management
- [x] Document approval/rejection workflow
- [x] PDF text extraction
- [x] Text cleaning
- [x] Text chunking
- [x] AI-based MCQ generation
- [x] Generated-question validation
- [x] Exact duplicate removal
- [x] AI-generated explanations
- [x] Competency-aware question generation
- [x] Trainer/admin review and approval
- [x] Approved question storage
- [x] Quiz publishing
## Phase 4 — Advanced Recommendations

- [ ] Training-history based recommendation signals
- [ ] Quiz-performance based recommendations
- [ ] Role relevance
- [ ] Semantic similarity
- [ ] More advanced personalization

## Phase 5 — External Learning Integration

- [ ] iGOT Karmayogi integration
- [ ] Integration/adapter layer
- [ ] NSSTA course/training integration where supported by available interfaces/data

## Phase 6 — Production Readiness

- [ ] Alembic database migrations
- [ ] PostgreSQL production database
- [ ] Centralized logging
- [ ] Production monitoring
- [ ] Security hardening
- [ ] Production deployment

## Phase 7 — Final Integration

- [ ] Frontend integration
- [ ] End-to-end testing
- [ ] Backend/frontend integration testing
- [ ] Final deployment
- [ ] SIH demonstration setup

---

# Architecture

## Current Backend Architecture

```text
                         Frontend
                            |
                            v
                    FastAPI Backend
                            |
        +-------------------+-------------------+
        |                   |                   |
        v                   v                   v
 Authentication        Core APIs          Recommendation
        |                   |                   |
        v                   v                   v
       JWT              SQLAlchemy        Skill-gap Logic
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
           Users         Courses       Training
                                        |
                                        v
                                     Quizzes
                                        |
                                        v
                                    Analytics
                                        |
                                        v
                                  SQLite (dev)
```

---

# Learning Flow

The current platform follows this learning flow:

```text
User Registration
       |
       v
User Profile
       |
       v
Competency Assessment
       |
       v
Skill-Gap Identification
       |
       v
Personalized Course Recommendations
       |
       v
Course Enrollment
       |
       v
Training Progress Tracking
       |
       v
Quiz / Assessment
       |
       v
Quiz Performance
       |
       v
Competency Update
       |
       v
Skill-Gap Recalculation
       |
       v
Updated Recommendations
```

---

# Planned AI Flow

The document-to-MCQ pipeline is planned as follows:

```text
Learning Material
(PDF / PPT / DOCX)
        |
        v
Document Upload
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
Structured MCQs
        |
        v
Validation
        |
        v
Trainer/Admin Review
        |
        v
Quiz + Questions Database
        |
        v
Learner Assessment
        |
        v
Competency Update
        |
        v
Skill-Gap Recalculation
        |
        v
New Recommendations
```

> The core PDF-to-MCQ AI pipeline is currently implemented. PDF/PPT/DOCX support is not yet complete; the current implementation supports PDF documents.

---

# Repository Structure

```text
SIH26101/
|
+-- SIH26101_backend/
|   |
|   +-- app/
|   |   |
|   |   +-- api/
|   |   |   +-- auth.py
|   |   |   +-- users.py
|   |   |   +-- competencies.py
|   |   |   +-- courses.py
|   |   |   +-- recommendations.py
|   |   |   +-- quizzes.py
|   |   |   +-- training.py
|   |   |   +-- admin.py
|   |   |   +-- document.py
|   |   |   +-- ai.py
|   |   +-- Database/
|   |   |   +-- connection.py
|   |   |
|   |   +-- models/
|   |   |   +-- user.py
|   |   |   +-- competency.py
|   |   |   +-- course.py
|   |   |   +-- training.py
|   |   |   +-- quiz.py
|   |   |   +-- document.py
|   |   |
|   |   +-- schemas/
|   |   |   +-- mcq.py
|   |   |   +-- ai_question.py
|   |   |
|   |   +-- services/
|   |   |   +-- gemini_service.py
|   |   |
|   |   +-- utils/
|   |   |   +-- chunk.py
|   |   |   +-- mcq_validator.py
|   |   |   +-- mcq_dedup.py
|   |   |   +-- text_preprocessing.py
|   |   |
|   |   +-- main.py
|   |
|   +-- seed.py
|   +-- requirements.txt
|   +-- .gitignore
|   +-- venvBackend/       # local only; not committed
|   +-- sih26101.db        # local development DB; not committed
|
+-- SIH26101_frontend/     # planned / team frontend
|
+-- docs/                  # planned project documentation
|
+-- README.md
```

> Keep Python import paths consistent with the actual package name on the development system. The current project uses `Database` as the database package name.

---

# Technology Stack

## Backend

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite (development)
- PyJWT
- pwdlib
- Argon2

## Planned AI / Data Layer

- PDF/PPT/DOCX parsing
- LLM API
- Structured JSON validation
- Embeddings
- Vector retrieval where required

---

# Local Setup

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>

cd SIH26101/SIH26101_backend
```

## 2. Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv venvBackend
.\venvBackend\Scripts\Activate.ps1
```

If the environment already exists:

```powershell
.\venvBackend\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Seed Development Data

The seed script inserts initial competencies, courses, and course-competency mappings used for development and recommendation testing.

```bash
python seed.py
```

Expected output:

```text
Database seeded successfully.
```

## 5. Start the API

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

---

# Core API Endpoints
## Documents

```http
POST  /documents/upload
POST  /documents/extract/{filename}
GET   /documents/
PATCH /documents/{document_id}/status

## Authentication

```http
POST /auth/register
POST /auth/login
```

## User

```http
GET  /users/me
POST /users/me/competencies
GET  /users/me/competencies
GET  /users/me/skill-gaps
GET  /users/me/recommendations/
```

## Competencies

```http
GET  /competencies/
POST /competencies/
```

## Courses

```http
GET  /courses/
POST /courses/
GET  /courses/{course_id}
POST /courses/{course_id}/competencies
```

## Training

```http
POST  /training/enroll/{course_id}
PATCH /training/{training_id}/progress
GET   /training/my-history
GET   /training/analytics
```

### Training API Responsibilities

```text
POST /training/enroll/{course_id}
        |
        +--> Creates a training record for the current user

PATCH /training/{training_id}/progress
        |
        +--> Updates completion percentage
        +--> Updates training status
        +--> Stores completion timestamp when completed

GET /training/my-history
        |
        +--> Returns current user's training records

GET /training/analytics
        |
        +--> Returns learning statistics for current user
```

## Quizzes

```http
POST /quizzes/
GET  /quizzes/
GET  /quizzes/{quiz_id}
POST /quizzes/{quiz_id}/questions
GET  /quizzes/{quiz_id}/questions
POST /quizzes/{quiz_id}/submit
GET  /quizzes/my-attempts
```

## Admin

```http
GET /admin/users
```

Additional admin endpoints will be added as the admin management workflow is completed.

---
POST /ai/generate-mcqs
POST /ai/generate-mcqs-from-pdf/{filename}
POST /ai/quizzes/{quiz_id}/approve-mcqs

# Authentication and Authorization

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

Authentication answers:

> **Who is the user?**

Authorization answers:

> **What is the user allowed to do?**

The backend uses protected dependencies to restrict access to user-specific and role-specific operations.

---

# Database Design

The backend uses SQLAlchemy ORM to interact with the database.

Important entities include:

```text
User
 |
 +---- Competency Profile
 |
 +---- TrainingHistory
 |          |
 |          +---- Course
 |
 +---- QuizAttempt
            |
            +---- Quiz
```

Additional relationships include:

```text
Course
 |
 +---- CourseCompetency
            |
            +---- Competency

Quiz
 |
 +---- Question
            |
            +---- Competency
```

The application uses these relationships to support:

- Competency tracking
- Course recommendations
- Training enrollment
- Training progress
- Quiz attempts
- Learning analytics
- Competency updates after assessments

---

# Recommendation Engine (V1)

The current recommendation engine is intentionally transparent and deterministic.

It is **not a trained machine-learning recommender**.

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

The current scoring logic uses competency gap and course-level fit.

This is a baseline that can later be extended using:

- Role relevance
- Training history
- Quiz performance
- Learning progress
- Semantic similarity

---

# Competency Levels

The current backend maps competency scores to levels as follows:

| Score | Level |
|------:|------:|
| 0–39 | 1 |
| 40–59 | 2 |
| 60–74 | 3 |
| 75–89 | 4 |
| 90–100 | 5 |

Skill gap is currently calculated as:

```text
max(required_level - current_level, 0)
```

---

# Training Management

The training system uses the `TrainingHistory` model to track the learner's relationship with courses.

A training record stores information such as:

- User
- Course
- Training status
- Completion percentage
- Enrollment timestamp
- Completion timestamp

Current training statuses include:

```text
enrolled
in_progress
completed
```

Current flow:

```text
Course
  |
  v
Enrollment
  |
  v
TrainingHistory
  |
  v
Progress Updates
  |
  +---- 0–99% --> in_progress
  |
  +---- 100% --> completed
```

---

# Quiz Evaluation

A quiz question can be linked to a competency.

During quiz submission, the backend:

1. Evaluates submitted answers against stored correct answers.
2. Calculates the overall quiz score.
3. Calculates the quiz percentage.
4. Groups performance by competency where `competency_id` is present.
5. Updates the learner's competency score and level.
6. Stores the quiz attempt.
7. Makes the updated competency profile available to the recommendation engine.

This creates the current adaptive-learning loop:

```text
Quiz Attempt
      |
      v
Competency Performance
      |
      v
Updated Competency Level
      |
      v
New Skill Gap
      |
      v
Updated Recommendation
```

---

# Learning Analytics

The current learning analytics endpoint is:

```http
GET /training/analytics
```

It provides user-specific learning statistics including:

```text
Total Courses Enrolled
Completed Courses
In-Progress Courses
Average Course Progress
Total Quiz Attempts
Average Quiz Percentage
```

Example response:

```json
{
    "total_courses": 4,
    "completed_courses": 2,
    "in_progress_courses": 2,
    "average_progress": 72.5,
    "quizzes_attempted": 5,
    "average_quiz_percentage": 81.4
}
```

The values depend on the user's actual training and quiz activity.

---

# Seed Data

`seed.py` creates initial development data for competencies and courses and maps courses to competencies.

The current seed data includes competencies such as:

- Sampling
- Survey Design
- Data Quality
- Statistical Analysis
- SDG Indicators
- Data Visualization

Example development courses include:

- Sampling Fundamentals
- Advanced Sampling Techniques
- Data Quality Management
- Survey Design Principles
- SDG Indicators and Statistics

The seed data is intended for development and demonstration purposes.

It is **not a replacement for production data management or live iGOT/NSSTA data**.

---

# Database

SQLite is used for the current development prototype because it is simple to run locally.

The development database file is intentionally ignored by Git:

```gitignore
*.db
```

The virtual environment is also ignored:

```gitignore
venvBackend/
```

Do not commit:

```text
venvBackend/
.env
*.db
API keys
JWT secrets
__pycache__/
```

Teammates should recreate the environment using:

```bash
pip install -r requirements.txt
```

and initialise development data using:

```bash
python seed.py
```

For production, the project is expected to move to PostgreSQL and use Alembic migrations.

---

# Team Development Guidelines

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

Recommended workflow:

```text
main
 |
 +---- feature/backend
 |
 +---- feature/frontend
 |
 +---- feature/ai-mcq
 |
 +---- feature/admin
```

Changes should be reviewed before being merged into `main`.

---

# Frontend Integration

The frontend is being developed separately by the team.

Once the backend API structure is stable, the backend team will provide an API contract containing:

- Endpoint
- HTTP method
- Authentication requirements
- User role requirements
- Request body
- Path/query parameters
- Response structure
- Error responses
- Example requests and responses

The frontend can then consume the FastAPI endpoints through HTTP requests.

Basic communication flow:

```text
Frontend
    |
    | HTTP Request
    v
FastAPI Backend
    |
    v
Business Logic
    |
    v
SQLAlchemy
    |
    v
Database
    |
    v
JSON Response
    |
    v
Frontend UI
```

---

# Current Scope vs Target Scope

The project is being built incrementally.

## Current Scope

The backend currently provides the foundation for:

- Users
- Authentication
- Competencies
- Skill gaps
- Courses
- Recommendations
- Training
- Quizzes
- Learning analytics

## Target Scope

The complete SIH solution is planned to support:

```text
Official / Employee Profile
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
        |
        v
External Learning Platform Integration
```

---

# Future Enhancements

The following features are planned for future development:

## In AI-Based Assessment
- OCR for scanned PDFs
- Semantic duplicate detection
- Reliable page-level source tracking
- Improved competency mapping
- Retry/fallback handling for AI quota/errors
- PPT/DOCX support

## Advanced Personalization

- Learning history
- Quiz performance
- Role relevance
- Course similarity
- Semantic search
- Improved recommendation ranking

## Integration

- iGOT Karmayogi integration
- NSSTA-related learning resources where supported
- External course synchronization

## Administration

- Course management
- Quiz management
- User management
- Trainer workflows
- Workforce-level analytics

## Production

- PostgreSQL
- Alembic migrations
- Centralized logging
- Monitoring
- Secure configuration
- Deployment
- Scalability improvements

---

# Project Disclaimer

This repository currently contains a **working prototype backend**, not a production-ready government deployment.

Any future claim of:

- iGOT integration
- NSSTA integration
- AI-generated assessment
- Production security
- Scalability
- Government deployment

should be backed by the corresponding implemented service, interface, or authorized integration.

The current course and competency seed data is intended for development and demonstration purposes.