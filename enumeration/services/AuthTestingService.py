from io import StringIO
import json
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

    @staticmethod
    def verify_username_strength(username):
        pattern = r"^[a-zA-Z0-9_]{3,20}$"
        regex = re.compile(pattern)

        if regex.match(username):
            return True
        else:
            return False

    @staticmethod
    def get_nested_token(json_data: str, keys_as_string: str):
        # exaample of keys_as_string: "user.info.auth"
        keys = keys_as_string.split(".")
        data = json.loads(json_data)
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data.get("token", None)

    @staticmethod
    def get_token_by_login(
        website_url,username: str, password: str, auth_uri: str, token_path: str
    ):
        # exaample of token_path_in_response: "user.info.auth"
        
        login_data = {
            'username': username,
            'password': password
        }
        # Make a request to obtain the token
        url = urljoin(website_url, auth_uri)
        response = requests.post(url=url, json=login_data)
        response_data = response.json()
       
        token = AuthTestingService.get_nested_token(
            json.dumps(response_data), token_path)
        
        if token:
            return token
        else:
            raise Exception("Failed to obtain access token")


    @staticmethod
    def verify_access_to_one_ressource(
        website_url, role_username ,role_password, auth_uri, token_path,http_method, http_response_code_for_access_allowed, http_response_code_for_access_denied
    ):
        """
        Verify if the user can access to the ressources
        """
        # Get the token
        try:
            token = AuthTestingService.get_token_by_login(username=role_username, password=role_password, website_url=website_url, auth_uri=auth_uri, token_path=token_path)
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.request(method=http_method, url=website_url, headers=headers)

            if response.status_code == http_response_code_for_access_allowed:
                return True
            elif response.status_code == http_response_code_for_access_denied:
                return False
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def check_role_authorization(
        website_url, services, all_roles, auth_uri, token_path
    ):
        """
        Check if the roles are authorized to access the services
        """
        ans=[]
        # Check if the roles are authorized to access the services
        for service in services:
            # i should pass them as an argument
            http_method = service["http_method"]
            http_response_code_for_access_allowed = service["http_response_code_for_access_allowed"]
            http_response_code_for_access_denied = service["http_response_code_for_access_denied"]
            
            
            for role in all_roles:
                has_access = AuthTestingService.verify_access_to_one_ressource(
                    website_url=website_url,
                    role_username=role["username"],
                    role_password=role["password"],
                    auth_uri=auth_uri,
                    token_path = token_path,
                    http_method=http_method,
                    http_response_code_for_access_allowed=http_response_code_for_access_allowed,
                    http_response_code_for_access_denied=http_response_code_for_access_denied
                )
                if has_access and role not in service["roles_allowed"]:
                    # The role is not authorized to access the service
                    ans.append(f"{role} is not authorized to access {service.name}")
                elif not has_access and role in service["roles_allowed"]:
                    # The role is authorized to access the service
                    ans.append(f"{role} is authorized to access {service.name} but it has no access")
        return ans
