from app.Database.connection import SessionLocal

from app.models.competency import Competency
from app.models.course import Course, CourseCompetency


def seed_database():
    db = SessionLocal()
    try:
        # -------------------------------------------------
        # 1. Competencies
        # -------------------------------------------------

        competencies_data = [
            {
                "name": "Sampling",
                "description": "Knowledge of sampling methods and sampling design",
                "required_level": 4
            },
            {
                "name": "Survey Design",
                "description": "Designing and planning statistical surveys",
                "required_level": 4
            },
            {
                "name": "Data Quality",
                "description": "Assessment and improvement of statistical data quality",
                "required_level": 4
            },
            {
                "name": "Statistical Analysis",
                "description": "Statistical methods for analysing official statistics",
                "required_level": 4
            },
            {
                "name": "SDG Indicators",
                "description": "Understanding and interpreting Sustainable Development Goal indicators",
                "required_level": 3
            },
            {
                "name": "Data Visualization",
                "description": "Presenting statistical information using effective visualizations",
                "required_level": 3
            }
        ]

        competencies = {}

        for data in competencies_data:

            competency = (
                db.query(Competency)
                .filter(
                    Competency.name == data["name"]
                )
                .first()
            )

            if competency is None:
                competency = Competency(**data)
                db.add(competency)
                db.flush()

            competencies[
                data["name"]
            ] = competency


        # -------------------------------------------------
        # 2. Courses
        # -------------------------------------------------

        courses_data = [
            {
                "title": "Sampling Fundamentals",
                "description": "Introduction to sampling methods used in statistical surveys",
                "provider": "NSSTA",
                "difficulty": "beginner",
                "duration_hours": 6,
                "source": "nssta"
            },
            {
                "title": "Advanced Sampling Techniques",
                "description": "Advanced sampling design and estimation methods",
                "provider": "iGOT",
                "difficulty": "advanced",
                "duration_hours": 12,
                "source": "igot"
            },
            {
                "title": "Data Quality Management",
                "description": "Methods for measuring, validating and improving statistical data quality",
                "provider": "iGOT",
                "difficulty": "intermediate",
                "duration_hours": 8,
                "source": "igot"
            },
            {
                "title": "Survey Design Principles",
                "description": "Fundamentals of designing effective statistical surveys",
                "provider": "NSSTA",
                "difficulty": "beginner",
                "duration_hours": 7,
                "source": "nssta"
            },
            {
                "title": "SDG Indicators and Statistics",
                "description": "Understanding SDG indicators and their statistical measurement",
                "provider": "iGOT",
                "difficulty": "intermediate",
                "duration_hours": 8,
                "source": "igot"
            }
        ]

        courses = {}

        for data in courses_data:

            course = (
                db.query(Course)
                .filter(
                    Course.title == data["title"]
                )
                .first()
            )

            if course is None:
                course = Course(**data)
                db.add(course)
                db.flush()

            courses[
                data["title"]
            ] = course


        # -------------------------------------------------
        # 3. Course ↔ Competency mapping
        # -------------------------------------------------

        mappings = [
            (
                "Sampling Fundamentals",
                "Sampling",
                2
            ),
            (
                "Advanced Sampling Techniques",
                "Sampling",
                4
            ),
            (
                "Data Quality Management",
                "Data Quality",
                4
            ),
            (
                "Survey Design Principles",
                "Survey Design",
                4
            ),
            (
                "SDG Indicators and Statistics",
                "SDG Indicators",
                3
            )
        ]

        for course_name, competency_name, target_level in mappings:

            course = courses[course_name]
            competency = competencies[competency_name]

            existing_mapping = (
                db.query(CourseCompetency)
                .filter(
                    CourseCompetency.course_id == course.id,
                    CourseCompetency.competency_id
                    == competency.id
                )
                .first()
            )

            if existing_mapping is None:

                mapping = CourseCompetency(
                    course_id=course.id,
                    competency_id=competency.id,
                    target_level=target_level
                )

                db.add(mapping)


        db.commit()

        print("Database seeded successfully.")


    except Exception as e:

        db.rollback()

        print("Error while seeding database:")
        print(e)

    finally:

        db.close()


if __name__ == "__main__":
    seed_database()