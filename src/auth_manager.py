"""
Authentication Manager Module
Handles user registration, login, and admin management.
Supports both traditional email/password and Google SSO authentication.
"""

import json
import hashlib
import os
from datetime import datetime
from typing import Dict, List, Optional

# Google OAuth imports
try:
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_requests
    from google_auth_oauthlib.flow import Flow
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    print("[WARNING] Google auth libraries not available. SSO will be disabled.")

# Google OAuth Configuration (can be overridden via environment variables)
# Support for multiple OAuth clients (Printo and Canvera)
GOOGLE_CLIENT_ID_PRINTO = os.getenv("GOOGLE_OAUTH_CLIENT_ID_PRINTO", "675787155214-njto72teukrq4425erkf2voqtaojmps7.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET_PRINTO = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET_PRINTO", "")

GOOGLE_CLIENT_ID_CANVERA = os.getenv("GOOGLE_OAUTH_CLIENT_ID_CANVERA", "316876622534-8hthl3q8gm9v5p18nbmppqfdsrk62mt9.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET_CANVERA = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET_CANVERA", "")

# Legacy single client configuration (for backward compatibility)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", GOOGLE_CLIENT_ID_PRINTO)
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "")

GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "https://screening-hr.printo.in")
ALLOWED_EMAIL_DOMAINS = os.getenv("ALLOWED_EMAIL_DOMAINS", "printo.in,canvera.com")
ALLOWED_EMAIL_DOMAIN = os.getenv("ALLOWED_EMAIL_DOMAIN", "printo.in")  # Legacy

# OAuth clients configuration
OAUTH_CLIENTS = {
    "printo.in": {
        "client_id": GOOGLE_CLIENT_ID_PRINTO,
        "client_secret": GOOGLE_CLIENT_SECRET_PRINTO,
        "display_name": "Printo"
    },
    "canvera.com": {
        "client_id": GOOGLE_CLIENT_ID_CANVERA,
        "client_secret": GOOGLE_CLIENT_SECRET_CANVERA,
        "display_name": "Canvera"
    }
}


class AuthManager:
    """
    Manages user authentication and authorization.
    Uses a JSON file for storing user data.
    """

    def __init__(self, users_file: str = "credentials/users.json"):
        """
        Initialize the Authentication Manager.

        Args:
            users_file: Path to the JSON file storing user data
        """
        self.users_file = users_file
        self._ensure_users_file()

    def _ensure_users_file(self):
        """Create users file with default admin if it doesn't exist."""
        if not os.path.exists(self.users_file):
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)

            # Create default admin user
            default_admin = {
                "users": {
                    "admin": {
                        "email": "admin@printo.in",
                        "password_hash": self._hash_password("admin123"),
                        "role": "admin",
                        "is_active": True,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "last_login": None
                    }
                }
            }

            with open(self.users_file, 'w') as f:
                json.dump(default_admin, f, indent=2)

            print(f"[OK] Created users file with default admin")
            print(f"[INFO] Default credentials: admin@printo.in / admin123")

    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def _load_users(self) -> Dict:
        """Load users from JSON file."""
        with open(self.users_file, 'r') as f:
            return json.load(f)

    def _save_users(self, users_data: Dict):
        """Save users to JSON file."""
        with open(self.users_file, 'w') as f:
            json.dump(users_data, f, indent=2)

    def register_user(self, email: str, password: str, role: str = "user") -> tuple[bool, str]:
        """
        Register a new user.

        Args:
            email: User's email address
            password: User's password
            role: User role (user or admin)

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            users_data = self._load_users()

            # Check if email already exists
            if email in users_data["users"]:
                return False, "Email already registered"

            # Validate email format
            if "@" not in email or "." not in email:
                return False, "Invalid email format"

            # Validate password
            if len(password) < 6:
                return False, "Password must be at least 6 characters"

            # Create new user
            users_data["users"][email] = {
                "email": email,
                "password_hash": self._hash_password(password),
                "role": role,
                "is_active": True,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_login": None
            }

            self._save_users(users_data)
            return True, "Registration successful! Please wait for admin approval."

        except Exception as e:
            return False, f"Registration failed: {str(e)}"

    def login_user(self, email: str, password: str) -> tuple[bool, str, Optional[Dict]]:
        """
        Authenticate a user.

        Args:
            email: User's email
            password: User's password

        Returns:
            Tuple of (success: bool, message: str, user_data: dict or None)
        """
        try:
            users_data = self._load_users()

            # Check if user exists
            if email not in users_data["users"]:
                return False, "Invalid email or password", None

            user = users_data["users"][email]

            # Check if account is active
            if not user.get("is_active", False):
                return False, "Account is deactivated. Contact admin.", None

            # Verify password
            if user["password_hash"] != self._hash_password(password):
                return False, "Invalid email or password", None

            # Update last login
            user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._save_users(users_data)

            return True, "Login successful!", user

        except Exception as e:
            return False, f"Login failed: {str(e)}", None

    def get_all_users(self) -> List[Dict]:
        """
        Get all users (admin only).

        Returns:
            List of user dictionaries
        """
        try:
            users_data = self._load_users()
            users_list = []

            for email, user_info in users_data["users"].items():
                users_list.append({
                    "email": email,
                    "name": user_info.get("name", ""),
                    "role": user_info.get("role", "user"),
                    "is_active": user_info.get("is_active", True),
                    "auth_method": user_info.get("auth_method", "password"),
                    "created_at": user_info.get("created_at", "N/A"),
                    "last_login": user_info.get("last_login", "Never")
                })

            return users_list

        except Exception as e:
            print(f"[ERROR] Failed to get users: {str(e)}")
            return []

    def deactivate_user(self, email: str) -> tuple[bool, str]:
        """
        Deactivate a user account (admin only).

        Args:
            email: Email of user to deactivate

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            users_data = self._load_users()

            if email not in users_data["users"]:
                return False, "User not found"

            # Don't allow deactivating the main admin
            if email == "admin@printo.in":
                return False, "Cannot deactivate main admin account"

            users_data["users"][email]["is_active"] = False
            self._save_users(users_data)

            return True, f"User {email} has been deactivated"

        except Exception as e:
            return False, f"Deactivation failed: {str(e)}"

    def activate_user(self, email: str) -> tuple[bool, str]:
        """
        Activate a user account (admin only).

        Args:
            email: Email of user to activate

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            users_data = self._load_users()

            if email not in users_data["users"]:
                return False, "User not found"

            users_data["users"][email]["is_active"] = True
            self._save_users(users_data)

            return True, f"User {email} has been activated"

        except Exception as e:
            return False, f"Activation failed: {str(e)}"

    def delete_user(self, email: str) -> tuple[bool, str]:
        """
        Delete a user account (admin only).

        Args:
            email: Email of user to delete

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            users_data = self._load_users()

            if email not in users_data["users"]:
                return False, "User not found"

            # Don't allow deleting the main admin
            if email == "admin@printo.in":
                return False, "Cannot delete main admin account"

            del users_data["users"][email]
            self._save_users(users_data)

            return True, f"User {email} has been deleted"

        except Exception as e:
            return False, f"Deletion failed: {str(e)}"

    def change_password(self, email: str, old_password: str, new_password: str) -> tuple[bool, str]:
        """
        Change user password.

        Args:
            email: User's email
            old_password: Current password
            new_password: New password

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            users_data = self._load_users()

            if email not in users_data["users"]:
                return False, "User not found"

            user = users_data["users"][email]

            # Verify old password
            if user["password_hash"] != self._hash_password(old_password):
                return False, "Current password is incorrect"

            # Validate new password
            if len(new_password) < 6:
                return False, "New password must be at least 6 characters"

            # Update password
            user["password_hash"] = self._hash_password(new_password)
            self._save_users(users_data)

            return True, "Password changed successfully"

        except Exception as e:
            return False, f"Password change failed: {str(e)}"

    def reset_user_password(self, email: str, new_password: str) -> tuple[bool, str]:
        """
        Reset user password (admin only - for when users forget their password).

        Args:
            email: User's email
            new_password: New password to set

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            users_data = self._load_users()

            if email not in users_data["users"]:
                return False, "User not found"

            # Validate new password
            if len(new_password) < 6:
                return False, "Password must be at least 6 characters"

            # Update password without requiring old password
            users_data["users"][email]["password_hash"] = self._hash_password(new_password)
            self._save_users(users_data)

            return True, f"Password reset successfully for {email}"

        except Exception as e:
            return False, f"Password reset failed: {str(e)}"

    # ============================================================
    # GOOGLE SSO AUTHENTICATION METHODS
    # ============================================================

    def verify_google_token(self, token: str) -> tuple[bool, str, Optional[Dict]]:
        """
        Verify a Google ID token and extract user information.

        Args:
            token: Google ID token from frontend

        Returns:
            Tuple of (success: bool, message: str, user_info: dict or None)
        """
        if not GOOGLE_AUTH_AVAILABLE:
            return False, "Google authentication is not available", None

        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                GOOGLE_CLIENT_ID
            )

            # Verify the token is from our client
            if idinfo['aud'] != GOOGLE_CLIENT_ID:
                return False, "Invalid token audience", None

            # Extract user info
            email = idinfo.get('email', '')
            name = idinfo.get('name', '')
            picture = idinfo.get('picture', '')

            # Verify email domain restriction
            allowed_domains = ALLOWED_EMAIL_DOMAINS.split(',')
            email_domain = email.split('@')[1] if '@' in email else ''
            if email_domain not in allowed_domains:
                domains_list = ', '.join([f"@{d}" for d in allowed_domains])
                return False, f"Access denied. Only {domains_list} email addresses are allowed.", None

            user_info = {
                'email': email,
                'name': name,
                'picture': picture,
                'google_id': idinfo.get('sub', '')
            }

            return True, "Token verified successfully", user_info

        except ValueError as e:
            return False, f"Invalid token: {str(e)}", None
        except Exception as e:
            return False, f"Token verification failed: {str(e)}", None

    def login_with_google(self, token: str) -> tuple[bool, str, Optional[Dict]]:
        """
        Login or register a user using Google SSO.

        Args:
            token: Google ID token

        Returns:
            Tuple of (success: bool, message: str, user_data: dict or None)
        """
        # Verify the Google token
        success, message, google_user = self.verify_google_token(token)

        if not success:
            return False, message, None

        email = google_user['email']

        try:
            users_data = self._load_users()

            # Check if user exists
            if email in users_data["users"]:
                user = users_data["users"][email]

                # Check if account is active
                if not user.get("is_active", False):
                    return False, "Account is deactivated. Contact admin.", None

                # Update user info from Google (name, picture) and last login
                user["name"] = google_user.get('name', user.get('name', ''))
                user["picture"] = google_user.get('picture', '')
                user["google_id"] = google_user.get('google_id', '')
                user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user["auth_method"] = "google_sso"

                self._save_users(users_data)

                return True, f"Welcome back, {user.get('name', email)}!", user

            else:
                # Auto-register new Google SSO user
                new_user = {
                    "email": email,
                    "name": google_user.get('name', ''),
                    "picture": google_user.get('picture', ''),
                    "google_id": google_user.get('google_id', ''),
                    "password_hash": None,  # No password for SSO users
                    "role": "user",  # Default role for SSO users
                    "is_active": True,
                    "auth_method": "google_sso",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                users_data["users"][email] = new_user
                self._save_users(users_data)

                return True, f"Welcome, {new_user.get('name', email)}! Your account has been created.", new_user

        except Exception as e:
            return False, f"Google login failed: {str(e)}", None

    def get_google_auth_url(self, domain: str = "printo.in") -> Optional[str]:
        """
        Build the Google OAuth authorization URL for redirect-based flow.
        Returns None if client secret is not configured.

        Args:
            domain: Email domain (printo.in or canvera.com)
        """
        if not GOOGLE_AUTH_AVAILABLE:
            return None

        # Get OAuth client config for the domain
        oauth_config = OAUTH_CLIENTS.get(domain)
        if not oauth_config or not oauth_config["client_secret"]:
            return None

        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": oauth_config["client_id"],
                    "client_secret": oauth_config["client_secret"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=[
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
                "openid"
            ],
            redirect_uri=GOOGLE_REDIRECT_URI,
        )
        # Add domain as state parameter to track which OAuth client was used
        auth_url, state = flow.authorization_url(
            prompt="select_account",
            state=f"domain:{domain}"
        )
        return auth_url

    def get_available_oauth_clients(self) -> list:
        """
        Get list of available OAuth clients (domains that have credentials configured).

        Returns:
            List of tuples (domain, display_name)
        """
        available = []
        for domain, config in OAUTH_CLIENTS.items():
            if config["client_secret"]:
                available.append((domain, config["display_name"]))
        return available

    def exchange_google_code(self, code: str, state: str = "") -> tuple[bool, str, Optional[Dict]]:
        """
        Exchange an authorization code for user info, then login/register.

        Args:
            code: Authorization code from OAuth callback
            state: State parameter containing domain info

        Returns:
            Tuple of (success, message, user_data)
        """
        if not GOOGLE_AUTH_AVAILABLE:
            return False, "Google OAuth is not configured", None

        # Extract domain from state parameter if available
        domain = None
        if state and state.startswith("domain:"):
            domain = state.split(":", 1)[1]

        # Try each OAuth client until one works (in case state is missing)
        oauth_configs_to_try = []
        if domain and domain in OAUTH_CLIENTS:
            oauth_configs_to_try.append((domain, OAUTH_CLIENTS[domain]))
        else:
            # Try all configured clients
            oauth_configs_to_try = [(d, c) for d, c in OAUTH_CLIENTS.items() if c["client_secret"]]

        last_error = "No OAuth clients configured"

        for domain, oauth_config in oauth_configs_to_try:
            try:
                flow = Flow.from_client_config(
                    {
                        "web": {
                            "client_id": oauth_config["client_id"],
                            "client_secret": oauth_config["client_secret"],
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                        }
                    },
                    scopes=[
                        "https://www.googleapis.com/auth/userinfo.profile",
                        "https://www.googleapis.com/auth/userinfo.email",
                        "openid"
                    ],
                    redirect_uri=GOOGLE_REDIRECT_URI,
                )
                flow.fetch_token(code=code)
                credentials = flow.credentials

                # Verify the ID token
                idinfo = id_token.verify_oauth2_token(
                    credentials.id_token,
                    google_requests.Request(),
                    oauth_config["client_id"],
                )

                email = idinfo.get("email", "")
                name = idinfo.get("name", "")
                picture = idinfo.get("picture", "")

                # Verify email domain matches
                if not email.endswith(f"@{domain}"):
                    continue  # Try next OAuth client

                # Successfully authenticated with this OAuth client
                break

            except Exception as e:
                last_error = str(e)
                continue  # Try next OAuth client
        else:
            # No OAuth client worked
            return False, f"Google login failed: {last_error}", None

        # Successfully authenticated - now handle user login/registration
        try:
            users_data = self._load_users()

            if email in users_data["users"]:
                user = users_data["users"][email]
                if not user.get("is_active", False):
                    return False, "Account is deactivated. Contact admin.", None
                user["name"] = name or user.get("name", "")
                user["picture"] = picture
                user["google_id"] = idinfo.get("sub", "")
                user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user["auth_method"] = "google_sso"
                self._save_users(users_data)
                return True, f"Welcome back, {user.get('name', email)}!", user
            else:
                new_user = {
                    "email": email,
                    "name": name,
                    "picture": picture,
                    "google_id": idinfo.get("sub", ""),
                    "password_hash": None,
                    "role": "user",
                    "is_active": True,
                    "auth_method": "google_sso",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                users_data["users"][email] = new_user
                self._save_users(users_data)
                return True, f"Welcome, {name or email}! Your account has been created.", new_user

        except Exception as e:
            return False, f"Failed to create/update user: {str(e)}", None

    def is_google_auth_available(self) -> bool:
        """Check if Google authentication is available."""
        return GOOGLE_AUTH_AVAILABLE

    def get_google_client_id(self) -> str:
        """Get the Google OAuth Client ID."""
        return GOOGLE_CLIENT_ID

    def get_allowed_domain(self) -> str:
        """Get the allowed email domain for SSO (legacy - returns first domain)."""
        return ALLOWED_EMAIL_DOMAINS.split(',')[0]

    def get_allowed_domains(self) -> list:
        """Get all allowed email domains for SSO."""
        return [d.strip() for d in ALLOWED_EMAIL_DOMAINS.split(',')]


# Example usage
if __name__ == "__main__":
    auth = AuthManager()

    # Test registration
    success, msg = auth.register_user("test@printo.in", "test123")
    print(f"Registration: {msg}")

    # Test login
    success, msg, user = auth.login_user("admin@printo.in", "admin123")
    print(f"Login: {msg}")
    if user:
        print(f"User role: {user['role']}")
