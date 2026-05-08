"""Tests for application workflows."""
import pytest
from decimal import Decimal
from uuid import uuid4
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.models.enums import (
    UserRole,
    ApplicationStatus,
    ExamSessionStatus,
    InstitutionStatus,
)
from app.models.user import User
from app.models.student import StudentProfile
from app.models.institution import Institution
from app.models.exam import ExamSession, Subject, GradeLevel, ExamFee
from app.models.centre import ExamCentre
from app.models.application import Application
from app.services.application_service import ApplicationService
from app.services.application_number_service import ApplicationNumberService
from app.repositories.application_repository import ApplicationRepository


@pytest.fixture
def test_student_user(db: Session) -> User:
    """Create a test student user."""
    from app.core.security import hash_password

    user = User(
        full_name="Test Student",
        email="student@test.com",
        phone="+919999999999",
        password_hash=hash_password("Password@123"),
        role=UserRole.STUDENT,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.flush()

    profile = StudentProfile(
        user_id=user.id,
        date_of_birth="2005-09-30",
        district="Kolkata",
        state="West Bengal",
        pincode="700001",
    )
    db.add(profile)
    db.commit()
    return user


@pytest.fixture
def test_institution_user(db: Session) -> User:
    """Create a test institution user."""
    from app.core.security import hash_password

    user = User(
        full_name="Test Institution",
        email="institution@test.com",
        phone="+918888888888",
        password_hash=hash_password("Password@123"),
        role=UserRole.INSTITUTION,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    db.flush()

    institution = Institution(
        user_id=user.id,
        institution_name="Test Academy",
        district="Kolkata",
        state="West Bengal",
        status=InstitutionStatus.APPROVED,
    )
    db.add(institution)
    db.commit()
    return user


@pytest.fixture
def test_admin_user(db: Session) -> User:
    """Create a test admin user."""
    from app.core.security import hash_password

    user = User(
        full_name="Test Admin",
        email="admin@test.com",
        phone="+917777777777",
        password_hash=hash_password("Password@123"),
        role=UserRole.ADMIN,
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
        session_name="Test Session 2026",
        year=2026,
        status=ExamSessionStatus.ACTIVE,
        start_date=datetime.utcnow().date(),
        end_date=(datetime.utcnow() + timedelta(days=30)).date(),
        application_start_date=datetime.utcnow().date(),
        application_end_date=(datetime.utcnow() + timedelta(days=15)).date(),
    )
    db.add(session)
    db.commit()
    return session


@pytest.fixture
def test_subject(db: Session) -> Subject:
    """Create a test subject."""
    subject = Subject(
        subject_name="Mathematics",
        subject_code="MATH101",
        is_active=True,
    )
    db.add(subject)
    db.commit()
    return subject


@pytest.fixture
def test_grade_level(db: Session) -> GradeLevel:
    """Create a test grade level."""
    grade = GradeLevel(
        grade_name="Grade 10",
        grade_code="G10",
        is_active=True,
    )
    db.add(grade)
    db.commit()
    return grade


@pytest.fixture
def test_exam_fee(
    db: Session,
    test_exam_session: ExamSession,
    test_subject: Subject,
    test_grade_level: GradeLevel,
) -> ExamFee:
    """Create a test exam fee."""
    fee = ExamFee(
        exam_session_id=test_exam_session.id,
        subject_id=test_subject.id,
        grade_level_id=test_grade_level.id,
        amount=Decimal("500.00"),
        currency="INR",
        late_fee_amount=Decimal("100.00"),
        is_active=True,
    )
    db.add(fee)
    db.commit()
    return fee


@pytest.fixture
def test_exam_centre(db: Session) -> ExamCentre:
    """Create a test exam centre."""
    centre = ExamCentre(
        centre_name="Test Centre",
        centre_code="TC001",
        district="Kolkata",
        state="West Bengal",
        is_active=True,
    )
    db.add(centre)
    db.commit()
    return centre


class TestApplicationNumberService:
    """Tests for application number generation."""

    def test_generate_application_number_format(self, db: Session):
        """Test that application number is generated in correct format."""
        service = ApplicationNumberService(db)
        app_number = service.generate_application_number(exam_session_year=2026)

        assert app_number.startswith("MBT-BSP-2026-")
        parts = app_number.split("-")
        assert len(parts) == 4
        assert len(parts[3]) == 6  # 6-digit sequence
        assert parts[3].isdigit()

    def test_generate_application_number_uniqueness(self, db: Session):
        """Test that generated numbers are unique."""
        service = ApplicationNumberService(db)
        app_number1 = service.generate_application_number(exam_session_year=2026)
        app_number2 = service.generate_application_number(exam_session_year=2026)

        assert app_number1 != app_number2


class TestApplicationService:
    """Tests for application service."""

    def test_create_student_application(
        self,
        db: Session,
        test_student_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
        test_grade_level: GradeLevel,
        test_exam_fee: ExamFee,
    ):
        """Test creating a student application."""
        service = ApplicationService(db)

        result = service.create_student_application(
            student_user=test_student_user,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
        )

        assert result["status"] == ApplicationStatus.DRAFT
        assert result["application_number"].startswith("MBT-BSP-")
        assert Decimal(result["fee_amount"]) == Decimal("500.00")

    def test_create_student_application_no_fee_configured(
        self,
        db: Session,
        test_student_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
    ):
        """Test that creation fails if fee is not configured."""
        service = ApplicationService(db)

        with pytest.raises(ValueError) as exc_info:
            service.create_student_application(
                student_user=test_student_user,
                exam_session_id=test_exam_session.id,
                subject_id=test_subject.id,
            )

        assert "not configured" in str(exc_info.value)

    def test_create_duplicate_active_application_blocked(
        self,
        db: Session,
        test_student_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
        test_grade_level: GradeLevel,
        test_exam_fee: ExamFee,
    ):
        """Test that duplicate active application is blocked."""
        service = ApplicationService(db)

        # Create first application
        service.create_student_application(
            student_user=test_student_user,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
        )

        # Try to create duplicate
        with pytest.raises(ValueError) as exc_info:
            service.create_student_application(
                student_user=test_student_user,
                exam_session_id=test_exam_session.id,
                subject_id=test_subject.id,
                grade_level_id=test_grade_level.id,
            )

        assert "already exists" in str(exc_info.value)

    def test_submit_application_with_fee_becomes_payment_pending(
        self,
        db: Session,
        test_student_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
        test_grade_level: GradeLevel,
        test_exam_fee: ExamFee,
    ):
        """Test that submitting application with fee moves to payment_pending."""
        service = ApplicationService(db)

        # Create application
        result = service.create_student_application(
            student_user=test_student_user,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
        )

        app_id = result["id"]

        # Submit application
        result = service.submit_application(
            application_id=app_id,
            user=test_student_user,
            confirmation=True,
            declaration_accepted=True,
        )

        assert result["status"] == ApplicationStatus.PAYMENT_PENDING

    def test_list_student_applications(
        self,
        db: Session,
        test_student_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
        test_grade_level: GradeLevel,
        test_exam_fee: ExamFee,
    ):
        """Test listing student applications."""
        service = ApplicationService(db)

        # Create application
        service.create_student_application(
            student_user=test_student_user,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
        )

        # List applications
        result = service.list_student_applications(
            student_user=test_student_user,
            page=1,
            page_size=20,
        )

        assert result["total"] == 1
        assert len(result["items"]) == 1
        assert result["items"][0]["status"] == ApplicationStatus.DRAFT

    def test_admin_request_correction(
        self,
        db: Session,
        test_student_user: User,
        test_admin_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
        test_grade_level: GradeLevel,
        test_exam_fee: ExamFee,
    ):
        """Test admin requesting correction."""
        service = ApplicationService(db)

        # Create and submit application
        result = service.create_student_application(
            student_user=test_student_user,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
        )
        app_id = result["id"]

        service.submit_application(
            application_id=app_id,
            user=test_student_user,
            confirmation=True,
            declaration_accepted=True,
        )

        # Move to under verification
        service.mark_under_verification(
            application_id=app_id,
            admin_user=test_admin_user,
        )

        # Request correction
        result = service.request_correction(
            application_id=app_id,
            admin_user=test_admin_user,
            correction_notes="Please correct student name",
        )

        assert result["status"] == ApplicationStatus.CORRECTION_REQUIRED
        assert result["correction_notes"] == "Please correct student name"

    def test_admin_approve_application(
        self,
        db: Session,
        test_student_user: User,
        test_admin_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
        test_grade_level: GradeLevel,
        test_exam_fee: ExamFee,
    ):
        """Test admin approving application."""
        service = ApplicationService(db)

        # Create and submit application
        result = service.create_student_application(
            student_user=test_student_user,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
        )
        app_id = result["id"]

        service.submit_application(
            application_id=app_id,
            user=test_student_user,
            confirmation=True,
            declaration_accepted=True,
        )

        # Move to under verification
        service.mark_under_verification(
            application_id=app_id,
            admin_user=test_admin_user,
        )

        # Approve
        result = service.approve_application(
            application_id=app_id,
            admin_user=test_admin_user,
            admin_remarks="Application approved",
        )

        assert result["status"] == ApplicationStatus.APPROVED

    def test_admin_reject_application(
        self,
        db: Session,
        test_student_user: User,
        test_admin_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
        test_grade_level: GradeLevel,
        test_exam_fee: ExamFee,
    ):
        """Test admin rejecting application."""
        service = ApplicationService(db)

        # Create and submit application
        result = service.create_student_application(
            student_user=test_student_user,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
        )
        app_id = result["id"]

        service.submit_application(
            application_id=app_id,
            user=test_student_user,
            confirmation=True,
            declaration_accepted=True,
        )

        # Move to under verification
        service.mark_under_verification(
            application_id=app_id,
            admin_user=test_admin_user,
        )

        # Reject
        result = service.reject_application(
            application_id=app_id,
            admin_user=test_admin_user,
            rejection_reason="Incomplete documents",
        )

        assert result["status"] == ApplicationStatus.REJECTED
        assert result["rejection_reason"] == "Incomplete documents"


class TestApplicationRepository:
    """Tests for application repository."""

    def test_exists_active_duplicate(
        self,
        db: Session,
        test_student_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
        test_grade_level: GradeLevel,
        test_exam_fee: ExamFee,
    ):
        """Test checking for duplicate active applications."""
        repo = ApplicationRepository(db)

        # Create an application
        repo.create(
            application_number="MBT-BSP-2026-000001",
            student_id=test_student_user.student_profile.id,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
            fee_amount=Decimal("500.00"),
            status=ApplicationStatus.DRAFT,
        )
        repo.commit()

        # Check for duplicate
        exists = repo.exists_active_duplicate(
            student_id=test_student_user.student_profile.id,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
        )

        assert exists is True

    def test_get_by_application_number(
        self,
        db: Session,
        test_student_user: User,
        test_exam_session: ExamSession,
        test_subject: Subject,
        test_grade_level: GradeLevel,
        test_exam_fee: ExamFee,
    ):
        """Test getting application by number."""
        repo = ApplicationRepository(db)

        # Create an application
        app = repo.create(
            application_number="MBT-BSP-2026-000001",
            student_id=test_student_user.student_profile.id,
            exam_session_id=test_exam_session.id,
            subject_id=test_subject.id,
            grade_level_id=test_grade_level.id,
            fee_amount=Decimal("500.00"),
            status=ApplicationStatus.DRAFT,
        )
        repo.commit()

        # Retrieve by number
        retrieved = repo.get_by_application_number("MBT-BSP-2026-000001")

        assert retrieved is not None
        assert retrieved.id == app.id
