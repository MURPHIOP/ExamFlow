from __future__ import annotations

from decimal import Decimal

from app.db.session import SessionLocal
from app.models import (
    CentreStatus,
    ExamFee,
    ExamSession,
    ExamSessionStatus,
    GradeLevel,
    Subject,
    User,
    UserRole,
    ExamCentre,
)
from app.core.security import hash_password


def seed_users(session):
    users = [
        {
            "full_name": "Super Admin",
            "email": "superadmin@mbtechnosoft.com",
            "phone": "+919000000001",
            "role": UserRole.SUPER_ADMIN,
            "is_verified": True,
        },
        {
            "full_name": "Admin Employee",
            "email": "admin@mbtechnosoft.com",
            "phone": "+919000000002",
            "role": UserRole.ADMIN,
            "is_verified": True,
        },
        {
            "full_name": "Examiner",
            "email": "examiner@mbtechnosoft.com",
            "phone": "+919000000003",
            "role": UserRole.EXAMINER,
            "is_verified": True,
        },
    ]

    for payload in users:
        existing = session.query(User).filter(User.email == payload["email"]).first()
        if existing:
            continue
        session.add(
            User(
                full_name=payload["full_name"],
                email=payload["email"],
                phone=payload["phone"],
                password_hash=hash_password("Admin@12345"),
                role=payload["role"],
                is_active=True,
                is_verified=payload["is_verified"],
            )
        )


def seed_subjects(session):
    subject_names = [
        ("Music", "MUSIC", "Performing Arts"),
        ("Dance", "DANCE", "Performing Arts"),
        ("Drawing", "DRAWING", "Fine Arts"),
        ("Painting", "PAINTING", "Fine Arts"),
        ("Karate", "KARATE", "Martial Arts"),
        ("Tabla", "TABLA", "Music"),
        ("Vocal", "VOCAL", "Music"),
        ("Instrumental", "INSTRUMENTAL", "Music"),
        ("Rabindra Sangeet", "RABINDRA_SANGEET", "Music"),
        ("Classical Dance", "CLASSICAL_DANCE", "Dance"),
        ("Fine Arts", "FINE_ARTS", "Fine Arts"),
    ]

    for name, code, category in subject_names:
        existing = session.query(Subject).filter(Subject.code == code).first()
        if existing:
            continue
        session.add(Subject(name=name, code=code, category=category, is_active=True))


def seed_exam_session(session):
    code = "BSP-ANNUAL-2026"
    existing = session.query(ExamSession).filter(ExamSession.code == code).first()
    if existing:
        return existing

    exam_session = ExamSession(
        name="Annual Examination 2026",
        code=code,
        year=2026,
        status=ExamSessionStatus.DRAFT,
        description="Development seed exam session",
    )
    session.add(exam_session)
    session.flush()
    return exam_session


def seed_centres(session):
    centres = [
        ("Kolkata Centre", "KOL-CTR", "Kolkata"),
        ("Howrah Centre", "HOW-CTR", "Howrah"),
        ("Bardhaman Centre", "BRD-CTR", "Bardhaman"),
        ("Siliguri Centre", "SLG-CTR", "Siliguri"),
        ("Durgapur Centre", "DGP-CTR", "Durgapur"),
    ]

    for name, code, district in centres:
        existing = session.query(ExamCentre).filter(ExamCentre.code == code).first()
        if existing:
            continue
        session.add(
            ExamCentre(
                name=name,
                code=code,
                address_line_1=f"{name} Main Campus",
                district=district,
                state="West Bengal",
                pincode="700001",
                capacity=500,
                status=CentreStatus.ACTIVE,
            )
        )


def seed_grade_levels_and_fees(session, exam_session: ExamSession):
    subject_codes = ["MUSIC", "DANCE", "VOCAL", "TABLA"]
    grade_defs = [
        ("Prarambhik", "PRARAMBHIK", 1, Decimal("500.00")),
        ("First Year", "YEAR_1", 2, Decimal("700.00")),
        ("Second Year", "YEAR_2", 3, Decimal("850.00")),
    ]

    for code in subject_codes:
        subject = session.query(Subject).filter(Subject.code == code).first()
        if not subject:
            continue

        for grade_name, grade_code, order, fee_amount in grade_defs:
            grade = (
                session.query(GradeLevel)
                .filter(GradeLevel.subject_id == subject.id, GradeLevel.code == grade_code)
                .first()
            )
            if not grade:
                grade = GradeLevel(
                    subject_id=subject.id,
                    name=grade_name,
                    code=grade_code,
                    display_order=order,
                    default_fee=fee_amount,
                    is_active=True,
                )
                session.add(grade)
                session.flush()

            fee = (
                session.query(ExamFee)
                .filter(
                    ExamFee.exam_session_id == exam_session.id,
                    ExamFee.subject_id == subject.id,
                    ExamFee.grade_level_id == grade.id,
                )
                .first()
            )
            if fee:
                continue

            session.add(
                ExamFee(
                    exam_session_id=exam_session.id,
                    subject_id=subject.id,
                    grade_level_id=grade.id,
                    amount=fee_amount,
                    late_fee_amount=Decimal("100.00"),
                    currency="INR",
                    is_active=True,
                )
            )


def run_seed() -> None:
    session = SessionLocal()
    try:
        seed_users(session)
        seed_subjects(session)
        session.flush()

        exam_session = seed_exam_session(session)
        seed_centres(session)
        seed_grade_levels_and_fees(session, exam_session)

        session.commit()
        print("Seed data inserted successfully.")
    except Exception as exc:
        session.rollback()
        print(f"Seed failed: {exc}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run_seed()
