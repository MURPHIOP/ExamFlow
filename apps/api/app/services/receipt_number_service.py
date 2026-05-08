"""Service for generating unique receipt numbers."""
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment

logger = logging.getLogger(__name__)


class ReceiptNumberService:
    """Service for generating unique receipt numbers."""

    MAX_RETRIES = 10
    FORMAT = "MBT-RCPT-{year}-{sequence:06d}"

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def generate_receipt_number(self, year: Optional[int] = None) -> str:
        """Generate a unique receipt number.

        Args:
            year: Year for receipt number (defaults to current year)

        Returns:
            Unique receipt number in format MBT-RCPT-{YEAR}-{XXXXXX}

        Raises:
            RuntimeError: If unable to generate unique number after MAX_RETRIES
        """
        if year is None:
            year = datetime.utcnow().year

        for attempt in range(self.MAX_RETRIES):
            # Count existing numbers for this year
            stmt = select(Payment).where(
                Payment.receipt_number.like(f"MBT-RCPT-{year}-%")
            )
            existing = self.db.scalars(stmt).all()
            sequence = len(existing) + 1

            # Generate receipt number
            receipt_number = self.FORMAT.format(year=year, sequence=sequence)

            # Check if it already exists (safety check)
            stmt = select(Payment).where(Payment.receipt_number == receipt_number)
            if not self.db.scalar(stmt):
                logger.info(f"Generated receipt number: {receipt_number}")
                return receipt_number

            # If exists, try next sequence
            logger.debug(f"Receipt number exists, retrying... (attempt {attempt + 1})")

        raise RuntimeError(
            f"Failed to generate unique receipt number after {self.MAX_RETRIES} attempts"
        )
