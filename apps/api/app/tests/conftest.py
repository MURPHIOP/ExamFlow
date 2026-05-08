"""Pytest configuration and fixtures for the test suite."""
import os
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.db.base import Base
from app.models.exam import ExamSession, Subject, GradeLevel, ExamFee
from app.models.centre import ExamCentre
from app.models.user import User
from app.models.application import Application
from app.models.enums import (
    UserRole,
    Gender,
    ApplicationStatus,
    CentreStatus,
)

# Load environment variables before importing app configs
load_dotenv()

# Ensure test Razorpay keys are set
os.environ.setdefault("RAZORPAY_KEY_ID", "rzp_test_your_key_id_here")
os.environ.setdefault("RAZORPAY_KEY_SECRET", "your_razorpay_key_secret_here")
os.environ.setdefault("RAZORPAY_WEBHOOK_SECRET", "your_razorpay_webhook_secret_here")


@pytest.fixture(scope="session")
def test_db_engine():
    """Create test database engine."""
    # Use SQLite in-memory for faster tests
    database_url = "sqlite:///:memory:"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    engine.dispose()


@pytest.fixture(scope="function")
def db(test_db_engine) -> Session:
    """Create test database session."""
    connection = test_db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_admin_user(db: Session) -> User:
    """Create a test admin user."""
    user = User(
        id=uuid4(),
        email="admin@test.com",
        full_name="Admin User",
        phone="+919876543210",
        password_hash="hashed_password",
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def test_student_user(db: Session) -> User:
    """Create a test student user."""
    user = User(
        id=uuid4(),
        email="student@test.com",
        full_name="Student User",
        phone="+919876543211",
        password_hash="hashed_password",
        role=UserRole.STUDENT,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def test_institution_user(db: Session) -> User:
    """Create a test institution user."""
    user = User(
        id=uuid4(),
        email="institution@test.com",
        full_name="Institution User",
        phone="+919876543212",
        password_hash="hashed_password",
        role=UserRole.INSTITUTION,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def test_exam_session(db: Session) -> ExamSession:
    """Create a test exam session."""
    session = ExamSession(
        id=uuid4(),
        name="Exam Session 2026",
        year=2026,
        start_date=datetime(2026, 5, 1).date(),
        end_date=datetime(2026, 6, 30).date(),
        application_start=datetime(2026, 3, 1).date(),
        application_end=datetime(2026, 4, 30).date(),
        result_date=datetime(2026, 7, 15).date(),
        is_active=True,
    )
    db.add(session)
    db.commit()
    return session


@pytest.fixture
def test_subject(db: Session) -> Subject:
    """Create a test subject."""
    subject = Subject(
        id=uuid4(),
        code="BSP-VOC",
        name="Vocal Music",
        category="MUSIC",
        description="Bangiya Sangeet Parishad Vocal Music Exam",
        is_active=True,
    )
    db.add(subject)
    db.commit()
    return subject


@pytest.fixture
def test_grade_level(db: Session) -> GradeLevel:
    """Create a test grade level."""
    grade = GradeLevel(
        id=uuid4(),
        code="G1",
        name="Grade 1",
        level=1,
        description="First grade level",
        is_active=True,
    )
    db.add(grade)
    db.commit()
    return grade


@pytest.fixture
def test_exam_centre(db: Session, test_exam_session: ExamSession) -> ExamCentre:
    """Create a test exam centre."""
    centre = ExamCentre(
        id=uuid4(),
        code="MBT-CENTER-001",
        name="Main Exam Centre",
        address_line_1="123 Main Street",
        address_line_2="", 
        district="Kolkata",
        state="West Bengal",
        pincode="700001",
        contact_person_name="John Doe",
        contact_person_phone="+919876543210",
        latitude=22.5726,
        longitude=88.3639,
        capacity=100,
        status=CentreStatus.ACTIVE,
    )
    db.add(centre)
    db.commit()
    return centre


@pytest.fixture
def test_exam_fee(
    db: Session,
    test_exam_session: ExamSession,
    test_subject: Subject,
    test_grade_level: GradeLevel,
) -> ExamFee:
    """Create a test exam fee."""
    fee = ExamFee(
        id=uuid4(),
        exam_session_id=test_exam_session.id,
        subject_id=test_subject.id,
        grade_level_id=test_grade_level.id,
        amount=Decimal("500.00"),
        description="Exam fee for vocal music grade 1",
        is_active=True,
    )
    db.add(fee)
    db.commit()
    return fee


@pytest.fixture
def test_application_draft(
    db: Session,
    test_student_user: User,
    test_exam_session: ExamSession,
    test_subject: Subject,
) -> Application:
    """Create a draft application."""
    app = Application(
        id=uuid4(),
        student_user_id=test_student_user.id,
        exam_session_id=test_exam_session.id,
        subject_id=test_subject.id,
        status=ApplicationStatus.DRAFT,
        application_number=f"MBT-BSP-2026-{uuid4().hex[:6].upper()}",
    )
    db.add(app)
    db.commit()
    return app


@pytest.fixture
def test_application_payment_pending(
    db: Session,
    test_student_user: User,
    test_exam_session: ExamSession,
    test_subject: Subject,
    test_grade_level: GradeLevel,
    test_exam_fee: ExamFee,
) -> Application:
    """Create an application in payment_pending status."""
    app = Application(
        id=uuid4(),
        student_user_id=test_student_user.id,
        exam_session_id=test_exam_session.id,
        subject_id=test_subject.id,
        grade_level_id=test_grade_level.id,
        status=ApplicationStatus.PAYMENT_PENDING,
        fee_amount=Decimal("500.00"),
        application_number=f"MBT-BSP-2026-{uuid4().hex[:6].upper()}",
    )
    db.add(app)
    db.commit()
    return app


@pytest.fixture
def test_application_paid(
    db: Session,
    test_student_user: User,
    test_exam_session: ExamSession,
    test_subject: Subject,
    test_grade_level: GradeLevel,
) -> Application:
    """Create an application in paid status."""
    app = Application(
        id=uuid4(),
        student_user_id=test_student_user.id,
        exam_session_id=test_exam_session.id,
        subject_id=test_subject.id,
        grade_level_id=test_grade_level.id,
        status=ApplicationStatus.PAID,
        fee_amount=Decimal("500.00"),
        application_number=f"MBT-BSP-2026-{uuid4().hex[:6].upper()}",
    )
    db.add(app)
    db.commit()
    return app
