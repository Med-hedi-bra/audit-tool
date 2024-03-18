from io import StringIO
import re
from urllib.parse import urljoin
import requests
from django.middleware.csrf import get_token


class AuthTestingService:

    @staticmethod
    def verify_password_strength(password):
        """
        Verify if the password is strong enough
        """

        # Count characters
        lowercase_count = 0
        uppercase_count = 0
        digit_count = 0
        special_char_count = 0

        for char in password:
            if char.islower():
                lowercase_count += 1
            elif char.isupper():
                uppercase_count += 1
            elif char.isdigit():
                digit_count += 1
            elif not char.isalnum() and not char.isspace():
                special_char_count += 1

        # Verify strength
        results = {
            "Minimum 8 characters": "Verified" if len(password) >= 8 else "Unverified",
            "Minimum 2 lowercase letters": (
                "Verified" if lowercase_count >= 2 else "Unverified"
            ),
            "Minimum 2 uppercase letters": (
                "Verified" if uppercase_count >= 2 else "Unverified"
            ),
            "Minimum 2 digits": "Verified" if digit_count >= 2 else "Unverified",
            "Minimum 2 special characters": (
                "Verified" if special_char_count >= 2 else "Unverified"
            ),
        }

        return results


            
