import re
from datetime import datetime
from typing import Any, Dict, List


class ValidationError(Exception):
    """Custom validation exception"""
    def __init__(self, message: str, errors: Dict[str, List[str]] = None):
        self.message = message
        self.errors = errors or {}
        super().__init__(self.message)


class Validator:
    """Utility class for input validation"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """Validate password strength"""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one number")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, " ".join(errors)

    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format"""
        if len(username) < 3 or len(username) > 20:
            return False
        return re.match(r'^[a-zA-Z0-9_-]+$', username) is not None

    @staticmethod
    def validate_future_date(date_str: str) -> bool:
        """Validate that date is in the future"""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return date > datetime.now()
        except ValueError:
            return False

    @staticmethod
    def validate_string_length(value: str, min_length: int = 1, max_length: int = 255) -> bool:
        """Validate string length"""
        return min_length <= len(value) <= max_length

    @staticmethod
    def validate_positive_number(value: float) -> bool:
        """Validate positive number"""
        try:
            num = float(value)
            return num > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_enum(value: str, allowed_values: List[str]) -> bool:
        """Validate value is in allowed list"""
        return value in allowed_values
