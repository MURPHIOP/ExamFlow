from app.models import Base  # noqa: F401

# Import all models so SQLAlchemy metadata is fully registered for Alembic.
from app.models import (  # noqa: F401
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

target_metadata = Base.metadata
