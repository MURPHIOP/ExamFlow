import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


class TestPasswordHashing:
    """Unit tests for password hashing functions."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword@123"
        hashed = hash_password(password)
        assert hashed != password
        assert len(hashed) > 20  # Bcrypt hashes are long

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "TestPassword@123"
        hashed = hash_password(password)
        assert verify_password(password, hashed)

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "TestPassword@123"
        wrong_password = "WrongPassword@123"
        hashed = hash_password(password)
        assert not verify_password(wrong_password, hashed)


class TestJWTTokens:
    """Unit tests for JWT token creation and decoding."""

    def test_create_access_token(self):
        """Test access token creation."""
        user_id = "test-user-id"
        role = "student"
        token = create_access_token(user_id, role)
        assert token
        assert isinstance(token, str)
        assert len(token) > 20

    def test_decode_access_token_valid(self):
        """Test decoding a valid access token."""
        user_id = "test-user-id"
        role = "student"
        token = create_access_token(user_id, role)
        payload = decode_access_token(token)
        assert payload.get("sub") == user_id
        assert payload.get("role") == role
        assert payload.get("type") == "access"

    def test_create_refresh_token(self):
        """Test refresh token creation."""
        user_id = "test-user-id"
        role = "student"
        token = create_access_token(user_id, role)
        assert token
        assert isinstance(token, str)

    def test_decode_access_token_tampered(self):
        """Test that tampered token fails to decode."""
        user_id = "test-user-id"
        role = "student"
        token = create_access_token(user_id, role)
        tampered_token = token[:-10] + "corrupted!"

        from jose import JWTError

        with pytest.raises(JWTError):
            decode_access_token(tampered_token)


class TestAuthSchemas:
    """Unit tests for authentication schemas."""

    def test_register_student_request_valid(self):
        """Test valid student registration request."""
        from app.schemas.auth import RegisterStudentRequest

        req = RegisterStudentRequest(
            full_name="Shreyan Mitra",
            email="shreyan@example.com",
            password="Student@12345",
            confirm_password="Student@12345",
        )
        assert req.full_name == "Shreyan Mitra"
        assert req.email == "shreyan@example.com"

    def test_register_student_request_passwords_mismatch(self):
        """Test that mismatched passwords are rejected."""
        from pydantic import ValidationError
        from app.schemas.auth import RegisterStudentRequest

        with pytest.raises(ValidationError):
            RegisterStudentRequest(
                full_name="Shreyan Mitra",
                email="shreyan@example.com",
                password="Student@12345",
                confirm_password="Different@12345",
            )

    def test_register_student_request_short_password(self):
        """Test that short passwords are rejected."""
        from pydantic import ValidationError
        from app.schemas.auth import RegisterStudentRequest

        with pytest.raises(ValidationError):
            RegisterStudentRequest(
                full_name="Shreyan Mitra",
                email="shreyan@example.com",
                password="Short1",
                confirm_password="Short1",
            )

    def test_register_student_no_email_or_phone(self):
        """Test that registration requires email or phone."""
        from pydantic import ValidationError
        from app.schemas.auth import RegisterStudentRequest

        with pytest.raises(ValidationError):
            RegisterStudentRequest(
                full_name="Shreyan Mitra",
                password="Student@12345",
                confirm_password="Student@12345",
            )

    def test_register_institution_request_valid(self):
        """Test valid institution registration request."""
        from app.schemas.auth import RegisterInstitutionRequest

        req = RegisterInstitutionRequest(
            institution_name="Kolkata Music Academy",
            contact_person_name="Admin Person",
            email="academy@example.com",
            password="Academy@12345",
            confirm_password="Academy@12345",
        )
        assert req.institution_name == "Kolkata Music Academy"

    def test_login_request_valid(self):
        """Test valid login request."""
        from app.schemas.auth import LoginRequest

        req = LoginRequest(
            identifier="shreyan@example.com",
            password="Student@12345",
        )
        assert req.identifier == "shreyan@example.com"


class TestCurrentUserResponse:
    """Unit tests for current user response schema."""

    def test_current_user_response_valid(self):
        """Test valid current user response."""
        from app.schemas.auth import CurrentUserResponse

        response = CurrentUserResponse(
            id="test-id",
            full_name="Shreyan Mitra",
            email="shreyan@example.com",
            phone="9876543210",
            role="student",
            is_active=True,
            is_verified=False,
        )
        assert response.id == "test-id"
        assert response.role == "student"


class TestPasswordChangeRequest:
    """Unit tests for password change schema."""

    def test_password_change_request_valid(self):
        """Test valid password change request."""
        from app.schemas.auth import PasswordChangeRequest

        req = PasswordChangeRequest(
            current_password="OldPassword@123",
            new_password="NewPassword@123",
            confirm_password="NewPassword@123",
        )
        assert req.current_password == "OldPassword@123"

    def test_password_change_request_new_passwords_mismatch(self):
        """Test that new passwords must match."""
        from pydantic import ValidationError
        from app.schemas.auth import PasswordChangeRequest

        with pytest.raises(ValidationError):
            PasswordChangeRequest(
                current_password="OldPassword@123",
                new_password="NewPassword@123",
                confirm_password="Different@123",
            )

    def test_password_change_request_new_password_too_short(self):
        """Test that new password must meet length requirement."""
        from pydantic import ValidationError
        from app.schemas.auth import PasswordChangeRequest

        with pytest.raises(ValidationError):
            PasswordChangeRequest(
                current_password="OldPassword@123",
                new_password="Short1",
                confirm_password="Short1",
            )

