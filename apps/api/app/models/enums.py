from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    GUARDIAN = "guardian"
    INSTITUTION = "institution"
    ADMIN = "admin"
    EXAMINER = "examiner"
    SUPER_ADMIN = "super_admin"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class InstitutionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class ExamSessionStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
    RESULT_PUBLISHED = "result_published"
    ARCHIVED = "archived"


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PAYMENT_PENDING = "payment_pending"
    PAID = "paid"
    UNDER_VERIFICATION = "under_verification"
    CORRECTION_REQUIRED = "correction_required"
    APPROVED = "approved"
    REJECTED = "rejected"
    CENTRE_ALLOCATED = "centre_allocated"
    ADMIT_CARD_GENERATED = "admit_card_generated"
    EXAM_COMPLETED = "exam_completed"
    MARKS_ENTERED = "marks_entered"
    RESULT_PUBLISHED = "result_published"
    CERTIFICATE_ISSUED = "certificate_issued"
    CERTIFICATE_REVOKED = "certificate_revoked"


class PaymentStatus(str, Enum):
    INITIATED = "initiated"
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentProvider(str, Enum):
    RAZORPAY = "razorpay"
    MANUAL = "manual"
    OFFLINE = "offline"


class DocumentType(str, Enum):
    STUDENT_PHOTO = "student_photo"
    SIGNATURE = "signature"
    IDENTITY_PROOF = "identity_proof"
    PREVIOUS_CERTIFICATE = "previous_certificate"
    PAYMENT_RECEIPT = "payment_receipt"
    ADMIT_CARD = "admit_card"
    CERTIFICATE = "certificate"
    SCANNED_FORM = "scanned_form"
    OTHER = "other"


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    VERIFIED = "verified"
    REJECTED = "rejected"
    GENERATED = "generated"
    REVOKED = "revoked"


class CentreStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FULL = "full"
    SUSPENDED = "suspended"


class ResultStatus(str, Enum):
    DRAFT = "draft"
    MARKS_ENTERED = "marks_entered"
    PUBLISHED = "published"
    WITHHELD = "withheld"
    REVISED = "revised"


class CertificateStatus(str, Enum):
    PENDING = "pending"
    GENERATED = "generated"
    ISSUED = "issued"
    REVOKED = "revoked"


class SupportStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    IN_APP = "in_app"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class AIReviewStatus(str, Enum):
    PENDING_REVIEW = "pending_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IGNORED = "ignored"
    FLAGGED = "flagged"


class AIJobType(str, Enum):
    OCR_FORM_EXTRACTION = "ocr_form_extraction"
    DUPLICATE_DETECTION = "duplicate_detection"
    SPELLING_SUGGESTION = "spelling_suggestion"
    CENTRE_RECOMMENDATION = "centre_recommendation"
    ANOMALY_DETECTION = "anomaly_detection"
    RESULT_ANALYTICS = "result_analytics"
    ADMIN_ASSISTANT_QUERY = "admin_assistant_query"


class AIJobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
