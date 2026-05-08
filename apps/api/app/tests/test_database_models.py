from app.models import (
    AIJob,
    AIReviewItem,
    AdmitCard,
    Application,
    AuditLog,
    CentreAllocation,
    Certificate,
    Document,
    ExamCentre,
    ExamFee,
    ExamSession,
    GradeLevel,
    Institution,
    MarksEntry,
    Notification,
    Payment,
    Result,
    StudentProfile,
    Subject,
    SupportRequest,
    User,
)
from app.models.base import Base
from app.models.enums import (
    AIJobStatus,
    AIJobType,
    AIReviewStatus,
    ApplicationStatus,
    CentreStatus,
    CertificateStatus,
    DocumentStatus,
    DocumentType,
    ExamSessionStatus,
    Gender,
    InstitutionStatus,
    NotificationChannel,
    NotificationStatus,
    PaymentProvider,
    PaymentStatus,
    ResultStatus,
    SupportStatus,
    UserRole,
)


def test_models_import_successfully():
    assert User.__tablename__ == "users"
    assert Application.__tablename__ == "applications"
    assert Payment.__tablename__ == "payments"
    assert AIReviewItem.__tablename__ == "ai_review_items"


def test_metadata_contains_expected_tables():
    expected_tables = {
        "users",
        "student_profiles",
        "institutions",
        "exam_sessions",
        "subjects",
        "grade_levels",
        "exam_fees",
        "exam_centres",
        "applications",
        "payments",
        "documents",
        "centre_allocations",
        "admit_cards",
        "marks_entries",
        "results",
        "certificates",
        "support_requests",
        "notifications",
        "audit_logs",
        "ai_jobs",
        "ai_review_items",
    }

    assert expected_tables.issubset(set(Base.metadata.tables.keys()))


def test_required_enum_values_exist():
    assert UserRole.SUPER_ADMIN.value == "super_admin"
    assert Gender.PREFER_NOT_TO_SAY.value == "prefer_not_to_say"
    assert InstitutionStatus.PENDING.value == "pending"
    assert ExamSessionStatus.RESULT_PUBLISHED.value == "result_published"
    assert ApplicationStatus.CERTIFICATE_ISSUED.value == "certificate_issued"
    assert PaymentStatus.SUCCESS.value == "success"
    assert PaymentProvider.RAZORPAY.value == "razorpay"
    assert DocumentType.ADMIT_CARD.value == "admit_card"
    assert DocumentStatus.GENERATED.value == "generated"
    assert CentreStatus.ACTIVE.value == "active"
    assert ResultStatus.PUBLISHED.value == "published"
    assert CertificateStatus.ISSUED.value == "issued"
    assert SupportStatus.IN_PROGRESS.value == "in_progress"
    assert NotificationChannel.IN_APP.value == "in_app"
    assert NotificationStatus.FAILED.value == "failed"
    assert AIReviewStatus.PENDING_REVIEW.value == "pending_review"
    assert AIJobType.ADMIN_ASSISTANT_QUERY.value == "admin_assistant_query"
    assert AIJobStatus.COMPLETED.value == "completed"


def test_relationship_mappers_configure_without_crash():
    table_names = sorted(Base.metadata.tables.keys())
    assert "applications" in table_names
    assert "users" in table_names
    assert "results" in table_names
