"""Service for Razorpay operations."""
import hashlib
import hmac
import json
import logging
from typing import Any, Optional

import razorpay
from app.core.config import get_settings

logger = logging.getLogger(__name__)


class RazorpayService:
    """Service for Razorpay payment operations."""

    def __init__(self):
        """Initialize Razorpay client."""
        settings = get_settings()

        if not settings.razorpay_key_id or not settings.razorpay_key_secret:
            raise ValueError(
                "Razorpay keys not configured. Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET."
            )

        self.key_id = settings.razorpay_key_id
        self.key_secret = settings.razorpay_key_secret
        self.webhook_secret = settings.razorpay_webhook_secret

        self.client = razorpay.Client(auth=(self.key_id, self.key_secret))

    def create_order(
        self,
        amount_paise: int,
        receipt: str,
        notes: Optional[dict[str, str]] = None,
    ) -> dict[str, Any]:
        """Create a Razorpay order.

        Args:
            amount_paise: Amount in paise (1 rupee = 100 paise)
            receipt: Receipt identifier (must be unique)
            notes: Optional notes to attach to order

        Returns:
            Order response from Razorpay API
        """
        try:
            order_payload = {
                "amount": amount_paise,
                "currency": "INR",
                "receipt": receipt,
            }

            if notes:
                order_payload["notes"] = notes

            order = self.client.order.create(order_payload)
            logger.info(f"Razorpay order created: {order['id']}")
            return order

        except Exception as e:
            logger.error(f"Failed to create Razorpay order: {str(e)}")
            raise

    def verify_checkout_signature(
        self,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ) -> bool:
        """Verify Razorpay checkout signature.

        Args:
            razorpay_order_id: Order ID from Razorpay
            razorpay_payment_id: Payment ID from Razorpay
            razorpay_signature: Signature from Razorpay checkout

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Create the string to sign: order_id|payment_id
            data = f"{razorpay_order_id}|{razorpay_payment_id}"

            # Generate HMAC SHA256 signature
            generated_signature = hmac.new(
                self.key_secret.encode(),
                data.encode(),
                hashlib.sha256,
            ).hexdigest()

            # Compare signatures
            is_valid = generated_signature == razorpay_signature
            if is_valid:
                logger.info(f"Signature verified for payment {razorpay_payment_id}")
            else:
                logger.warning(
                    f"Signature mismatch for payment {razorpay_payment_id}"
                )

            return is_valid

        except Exception as e:
            logger.error(f"Error verifying signature: {str(e)}")
            return False

    def verify_webhook_signature(
        self,
        request_body: bytes,
        signature_header: str,
    ) -> bool:
        """Verify Razorpay webhook signature.

        Args:
            request_body: Raw request body from webhook
            signature_header: X-Razorpay-Signature header value

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            if not self.webhook_secret:
                logger.warning("Webhook secret not configured")
                return False

            # Generate HMAC SHA256 signature
            generated_signature = hmac.new(
                self.webhook_secret.encode(),
                request_body,
                hashlib.sha256,
            ).hexdigest()

            # Compare signatures
            is_valid = generated_signature == signature_header
            if is_valid:
                logger.info("Webhook signature verified")
            else:
                logger.warning("Webhook signature mismatch")

            return is_valid

        except Exception as e:
            logger.error(f"Error verifying webhook signature: {str(e)}")
            return False

    def fetch_payment(self, payment_id: str) -> dict[str, Any]:
        """Fetch payment details from Razorpay.

        Args:
            payment_id: Razorpay payment ID

        Returns:
            Payment details from Razorpay API
        """
        try:
            payment = self.client.payment.fetch(payment_id)
            return payment
        except Exception as e:
            logger.error(f"Failed to fetch payment {payment_id}: {str(e)}")
            raise

    def fetch_order(self, order_id: str) -> dict[str, Any]:
        """Fetch order details from Razorpay.

        Args:
            order_id: Razorpay order ID

        Returns:
            Order details from Razorpay API
        """
        try:
            order = self.client.order.fetch(order_id)
            return order
        except Exception as e:
            logger.error(f"Failed to fetch order {order_id}: {str(e)}")
            raise

    def parse_webhook_payload(self, request_body: bytes) -> dict[str, Any]:
        """Parse webhook payload.

        Args:
            request_body: Raw request body

        Returns:
            Parsed JSON payload
        """
        try:
            return json.loads(request_body)
        except Exception as e:
            logger.error(f"Failed to parse webhook payload: {str(e)}")
            raise
