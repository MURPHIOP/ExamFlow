"""Service for managing application status transitions."""
from __future__ import annotations

from typing import Optional

from app.models.enums import ApplicationStatus
from app.core.response import api_response


class ApplicationStatusService:
    """Service for controlling application status transitions."""

    # Define allowed transitions
    ALLOWED_TRANSITIONS = {
        ApplicationStatus.DRAFT: [
            ApplicationStatus.SUBMITTED,
        ],
        ApplicationStatus.SUBMITTED: [
            ApplicationStatus.PAYMENT_PENDING,
            ApplicationStatus.UNDER_VERIFICATION,  # For zero-fee or manual mode
        ],
        ApplicationStatus.PAYMENT_PENDING: [
            ApplicationStatus.UNDER_VERIFICATION,  # Only by admin with manual mode
            ApplicationStatus.PAID,  # When payment is processed
        ],
        ApplicationStatus.UNDER_VERIFICATION: [
            ApplicationStatus.CORRECTION_REQUIRED,
            ApplicationStatus.APPROVED,
            ApplicationStatus.REJECTED,
        ],
        ApplicationStatus.CORRECTION_REQUIRED: [
            ApplicationStatus.SUBMITTED,
            ApplicationStatus.REJECTED,  # Admin can reject without resubmission
        ],
        ApplicationStatus.APPROVED: [
            ApplicationStatus.CENTRE_ALLOCATED,
            ApplicationStatus.CORRECTION_REQUIRED,  # Only by super admin
            # Rejection of approved should generally be blocked
        ],
        ApplicationStatus.REJECTED: [],
        ApplicationStatus.PAID: [
            ApplicationStatus.UNDER_VERIFICATION,
        ],
        ApplicationStatus.CENTRE_ALLOCATED: [
            ApplicationStatus.ADMIT_CARD_GENERATED,
        ],
        ApplicationStatus.ADMIT_CARD_GENERATED: [
            ApplicationStatus.EXAM_COMPLETED,
        ],
        ApplicationStatus.EXAM_COMPLETED: [
            ApplicationStatus.MARKS_ENTERED,
        ],
        ApplicationStatus.MARKS_ENTERED: [
            ApplicationStatus.RESULT_PUBLISHED,
        ],
        ApplicationStatus.RESULT_PUBLISHED: [
            ApplicationStatus.CERTIFICATE_ISSUED,
        ],
        ApplicationStatus.CERTIFICATE_ISSUED: [
            ApplicationStatus.CERTIFICATE_REVOKED,
        ],
        ApplicationStatus.CERTIFICATE_REVOKED: [],
    }

    @staticmethod
    def can_transition(
        current_status: ApplicationStatus,
        new_status: ApplicationStatus,
    ) -> tuple[bool, Optional[str]]:
        """
        Check if transition is allowed.

        Returns:
            (can_transition, error_message)
        """
        if current_status == new_status:
            return False, f"Application is already in {current_status} status"

        if current_status not in ApplicationStatusService.ALLOWED_TRANSITIONS:
            return False, f"No transitions defined for status {current_status}"

        allowed_statuses = ApplicationStatusService.ALLOWED_TRANSITIONS[current_status]

        if new_status not in allowed_statuses:
            return False, f"Cannot transition from {current_status} to {new_status}. Allowed transitions: {allowed_statuses}"

        return True, None

    @staticmethod
    def validate_transition(
        current_status: ApplicationStatus,
        new_status: ApplicationStatus,
    ) -> None:
        """
        Validate and raise exception if transition is not allowed.

        Raises:
            ValueError: If transition is not allowed
        """
        can_transition, error_message = ApplicationStatusService.can_transition(
            current_status,
            new_status,
        )

        if not can_transition:
            raise ValueError(error_message)

    @staticmethod
    def get_allowed_transitions(current_status: ApplicationStatus) -> list[ApplicationStatus]:
        """Get list of allowed status transitions from current status."""
        return ApplicationStatusService.ALLOWED_TRANSITIONS.get(current_status, [])
