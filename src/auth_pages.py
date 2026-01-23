"""
Authentication Pages Module
Provides login, registration, and user management pages for Streamlit
Supports both traditional email/password and Google SSO authentication
"""

import streamlit as st
from src.auth_manager import AuthManager
import streamlit.components.v1 as components


def get_google_signin_html(client_id: str) -> str:
    """
    Generate the HTML/JavaScript for Google Sign-In button.

    Args:
        client_id: Google OAuth Client ID

    Returns:
        HTML string with Google Sign-In button
    """
    return f"""
    <html>
    <head>
        <meta name="google-signin-client_id" content="{client_id}">
        <script src="https://accounts.google.com/gsi/client" async defer></script>
        <style>
            .g_id_signin {{
                display: flex;
                justify-content: center;
                margin: 20px 0;
            }}
            .google-btn-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                margin: 10px 0;
            }}
            .domain-notice {{
                font-size: 12px;
                color: #666;
                margin-top: 10px;
                text-align: center;
            }}
            .success-message {{
                color: #155724;
                background: #d4edda;
                padding: 10px 20px;
                border-radius: 5px;
                margin: 10px 0;
                text-align: center;
            }}
            .error-message {{
                color: #721c24;
                background: #f8d7da;
                padding: 10px 20px;
                border-radius: 5px;
                margin: 10px 0;
                text-align: center;
            }}
            .token-display {{
                background: #e9ecef;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                word-break: break-all;
                font-family: monospace;
                font-size: 10px;
                max-height: 100px;
                overflow-y: auto;
            }}
            .copy-btn {{
                background: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 10px;
            }}
            .copy-btn:hover {{
                background: #0056b3;
            }}
            .instruction {{
                font-size: 12px;
                color: #666;
                margin: 5px 0;
            }}
        </style>
    </head>
    <body>
        <div class="google-btn-container">
            <div id="g_id_onload"
                data-client_id="{client_id}"
                data-callback="handleCredentialResponse"
                data-auto_prompt="false">
            </div>
            <div class="g_id_signin"
                data-type="standard"
                data-size="large"
                data-theme="outline"
                data-text="sign_in_with"
                data-shape="rectangular"
                data-logo_alignment="left">
            </div>
            <div class="domain-notice">
                Only @printo.in email addresses are allowed
            </div>
        </div>

        <div id="result"></div>

        <script>
            function handleCredentialResponse(response) {{
                const token = response.credential;

                // Decode the JWT to get user info
                const payload = JSON.parse(atob(token.split('.')[1]));
                const email = payload.email;
                const name = payload.name || '';

                // Check domain before proceeding
                if (!email.endsWith('@printo.in')) {{
                    document.getElementById('result').innerHTML =
                        '<div class="error-message">Access denied. Only @printo.in emails are allowed.</div>';
                    return;
                }}

                // Show success and token for copying
                document.getElementById('result').innerHTML =
                    '<div class="success-message">✅ Verified: ' + email + '</div>' +
                    '<p class="instruction">Copy this token and paste it in the "Manual Google Sign-In" section below:</p>' +
                    '<div class="token-display" id="token-text">' + token + '</div>' +
                    '<button class="copy-btn" onclick="copyToken()">📋 Copy Token</button>' +
                    '<p class="instruction">After copying, expand "Manual Google Sign-In" below and paste the token.</p>';

                // Store in localStorage for persistence
                localStorage.setItem('google_sso_token', token);
                localStorage.setItem('google_sso_email', email);
                localStorage.setItem('google_sso_name', name);
            }}

            function copyToken() {{
                const tokenText = document.getElementById('token-text').innerText;
                navigator.clipboard.writeText(tokenText).then(function() {{
                    alert('Token copied! Now paste it in the "Manual Google Sign-In" section below.');
                }});
            }}

            // Check for stored token on load
            window.onload = function() {{
                const storedToken = localStorage.getItem('google_sso_token');
                if (storedToken) {{
                    const storedEmail = localStorage.getItem('google_sso_email') || '';
                    document.getElementById('result').innerHTML =
                        '<div class="success-message">Previous sign-in found: ' + storedEmail + '</div>' +
                        '<p class="instruction">Copy this token and paste it in the "Manual Google Sign-In" section below:</p>' +
                        '<div class="token-display" id="token-text">' + storedToken + '</div>' +
                        '<button class="copy-btn" onclick="copyToken()">📋 Copy Token</button>' +
                        '<button class="copy-btn" onclick="clearToken()" style="background: #dc3545; margin-left: 10px;">🗑️ Clear</button>';
                }}
            }}

            function clearToken() {{
                localStorage.removeItem('google_sso_token');
                localStorage.removeItem('google_sso_email');
                localStorage.removeItem('google_sso_name');
                document.getElementById('result').innerHTML = '';
            }}
        </script>
    </body>
    </html>
    """


def show_login_page():
    """Display the login page with both traditional and Google SSO options"""
    st.markdown('<div class="main-header">🔐 Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Please login to access the Hiring Automation Tool</div>', unsafe_allow_html=True)

    # Initialize auth manager
    auth = AuthManager()

    # Check for Google token in query params (callback from Google Sign-In)
    query_params = st.query_params
    if 'google_token' in query_params:
        google_token = query_params.get('google_token')
        if google_token:
            success, message, user_data = auth.login_with_google(google_token)
            if success:
                st.session_state.authenticated = True
                st.session_state.user_email = user_data['email']
                st.session_state.user_role = user_data.get('role', 'user')
                st.session_state.user_name = user_data.get('name', '')
                st.session_state.auth_method = 'google_sso'
                # Clear query params
                st.query_params.clear()
                st.success(f"✅ {message}")
                st.rerun()
            else:
                st.error(f"❌ {message}")
                st.query_params.clear()

    # ============================================================
    # GOOGLE SSO LOGIN SECTION
    # ============================================================
    if auth.is_google_auth_available():
        st.markdown("### Sign in with Google")
        st.info(f"🔐 Only **@{auth.get_allowed_domain()}** email addresses are allowed")

        # Check if we have a Google token in session state
        if 'google_token_input' not in st.session_state:
            st.session_state.google_token_input = ""

        # Display Google Sign-In button
        google_html = get_google_signin_html(auth.get_google_client_id())
        components.html(google_html, height=200)

        # Hidden input to receive Google token
        st.markdown("---")

        # Manual token input for Google SSO (as fallback)
        with st.expander("🔧 Manual Google Sign-In (if button doesn't work)"):
            st.markdown("""
            If the Google Sign-In button above doesn't work:
            1. Go to [Google OAuth Playground](https://developers.google.com/oauthplayground/)
            2. Or paste the ID token directly below
            """)
            google_token = st.text_input(
                "Google ID Token",
                type="password",
                key="google_token_manual",
                placeholder="Paste your Google ID token here"
            )

            if st.button("🔑 Sign in with Token", key="google_token_submit"):
                if google_token:
                    success, message, user_data = auth.login_with_google(google_token)

                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_email = user_data['email']
                        st.session_state.user_role = user_data.get('role', 'user')
                        st.session_state.user_name = user_data.get('name', '')
                        st.session_state.auth_method = 'google_sso'
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Please enter a Google ID token")

        st.markdown("---")
        st.markdown("### Or sign in with email/password")
    else:
        st.warning("⚠️ Google SSO is not available. Please use email/password login.")

    # ============================================================
    # TRADITIONAL EMAIL/PASSWORD LOGIN
    # ============================================================
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your.email@printo.in")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("🔑 Login", type="primary")

        if submit:
            if not email or not password:
                st.error("❌ Please enter both email and password")
            else:
                success, message, user_data = auth.login_user(email, password)

                if success:
                    # Store user info in session state
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_role = user_data['role']
                    st.session_state.user_name = user_data.get('name', email.split('@')[0])
                    st.session_state.auth_method = 'password'
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

    st.markdown("---")

    # Register link
    st.markdown("### Don't have an account?")
    if st.button("📝 Register New Account"):
        st.session_state.show_register = True
        st.rerun()

    # Default credentials info
    with st.expander("ℹ️ Default Admin Credentials"):
        st.info("""
        **Default Admin Account:**
        - Email: `admin@printo.in`
        - Password: `admin123`

        ⚠️ Please change the password after first login!
        """)


def show_register_page():
    """Display the registration page"""
    st.markdown('<div class="main-header">📝 Register</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create a new account</div>', unsafe_allow_html=True)

    # Initialize auth manager
    auth = AuthManager()

    # Show SSO recommendation
    if auth.is_google_auth_available():
        st.info(f"""
        💡 **Recommended:** Use Google Sign-In for easier access!

        If you have a **@{auth.get_allowed_domain()}** email, you can sign in directly with Google
        without creating a password.
        """)

        if st.button("🔙 Back to Login (Use Google Sign-In)"):
            st.session_state.show_register = False
            st.rerun()

        st.markdown("---")
        st.markdown("### Or create a password-based account")

    # Registration form
    with st.form("register_form"):
        email = st.text_input("Email", placeholder="your.email@printo.in")
        password = st.text_input("Password", type="password", help="Minimum 6 characters")
        password_confirm = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button("📝 Register", type="primary")

        if submit:
            if not email or not password or not password_confirm:
                st.error("❌ Please fill all fields")
            elif password != password_confirm:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                success, message = auth.register_user(email, password, role="user")

                if success:
                    st.success(f"✅ {message}")
                    st.info("👉 You can now login with your credentials")
                    st.balloons()

                    # Auto-switch to login page after 2 seconds
                    import time
                    time.sleep(2)
                    st.session_state.show_register = False
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

    st.markdown("---")

    # Back to login
    if st.button("🔙 Back to Login"):
        st.session_state.show_register = False
        st.rerun()


def show_admin_users_page():
    """Display admin user management page"""
    st.markdown('<div class="main-header">👥 User Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Manage user accounts and permissions</div>', unsafe_allow_html=True)

    # Check if user is admin
    if st.session_state.get('user_role') != 'admin':
        st.error("❌ Access denied. Admin privileges required.")
        return

    # Initialize auth manager
    auth = AuthManager()

    # Get all users
    users = auth.get_all_users()

    if not users:
        st.info("ℹ️ No users found")
        return

    st.success(f"✅ {len(users)} user(s) registered")

    # Display users in a table
    for idx, user in enumerate(users):
        status_icon = "✅" if user['is_active'] else "❌"
        role_badge = "🔑 Admin" if user['role'] == 'admin' else "👤 User"
        auth_badge = "🔐 SSO" if user.get('auth_method') == 'google_sso' else "🔑 Password"

        with st.expander(f"{status_icon} {user['email']} - {role_badge} {auth_badge}", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Email:** {user['email']}")
                st.markdown(f"**Name:** {user.get('name', 'N/A')}")
                st.markdown(f"**Role:** {user['role']}")
                st.markdown(f"**Auth Method:** {user.get('auth_method', 'password')}")
                st.markdown(f"**Status:** {'Active' if user['is_active'] else 'Inactive'}")
                st.markdown(f"**Created:** {user['created_at']}")
                st.markdown(f"**Last Login:** {user['last_login']}")

            with col2:
                # Action buttons
                st.markdown("### Actions")

                # Reset password (only for password-based users)
                if user.get('auth_method') != 'google_sso':
                    with st.form(key=f"reset_password_form_{idx}"):
                        st.markdown("**🔑 Reset Password**")
                        new_password = st.text_input("New Password", type="password", key=f"new_pwd_{idx}")
                        reset_submit = st.form_submit_button("Reset Password")

                        if reset_submit:
                            if not new_password:
                                st.error("Please enter a new password")
                            elif len(new_password) < 6:
                                st.error("Password must be at least 6 characters")
                            else:
                                success, message = auth.reset_user_password(user['email'], new_password)
                                if success:
                                    st.success(message)
                                    st.info(f"New password: {new_password}")
                                    st.rerun()
                                else:
                                    st.error(message)
                else:
                    st.info("🔐 SSO user - no password to reset")

                st.markdown("---")

                # Toggle active status
                if user['is_active']:
                    if st.button("🔴 Deactivate", key=f"deactivate_{idx}"):
                        success, message = auth.deactivate_user(user['email'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    if st.button("🟢 Activate", key=f"activate_{idx}"):
                        success, message = auth.activate_user(user['email'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

                # Delete user
                if user['email'] != "admin@printo.in":  # Protect main admin
                    if st.button("🗑️ Delete", key=f"delete_{idx}"):
                        success, message = auth.delete_user(user['email'])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)


def show_user_profile():
    """Show user profile in sidebar"""
    if st.session_state.get('authenticated'):
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 User Profile")

        auth_method = st.session_state.get('auth_method', 'password')
        auth_icon = "🔐" if auth_method == 'google_sso' else "🔑"

        st.sidebar.info(f"""
**Email:** {st.session_state.get('user_email', 'Unknown')}
**Name:** {st.session_state.get('user_name', 'N/A')}
**Role:** {st.session_state.get('user_role', 'user').title()}
**Auth:** {auth_icon} {'Google SSO' if auth_method == 'google_sso' else 'Password'}
        """)

        if st.sidebar.button("🚪 Logout"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
