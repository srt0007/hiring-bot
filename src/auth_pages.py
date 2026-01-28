"""
Authentication Pages Module
Provides login, registration, and user management pages for Streamlit
Supports both traditional email/password and Google SSO authentication
Modern SaaS-style UI/UX
"""

import streamlit as st
from src.auth_manager import AuthManager


def apply_auth_styles():
    """Apply modern SaaS-style CSS for authentication pages"""
    st.markdown("""
    <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Modern auth container */
        .auth-container {
            max-width: 440px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 1px 3px rgba(0, 0, 0, 0.06);
        }

        /* Logo/Brand area */
        .auth-logo {
            text-align: center;
            margin-bottom: 2rem;
        }

        .auth-logo h1 {
            font-size: 1.75rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 0.5rem;
        }

        .auth-logo p {
            font-size: 0.95rem;
            color: #6b7280;
            margin: 0;
        }

        /* SSO Buttons */
        .sso-button {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 0.75rem 1rem;
            margin-bottom: 0.75rem;
            border: 1.5px solid #e5e7eb;
            border-radius: 8px;
            background: white;
            color: #374151;
            font-size: 0.95rem;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
        }

        .sso-button:hover {
            background: #f9fafb;
            border-color: #d1d5db;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .sso-icon {
            margin-right: 0.75rem;
            font-size: 1.25rem;
        }

        /* Divider */
        .auth-divider {
            display: flex;
            align-items: center;
            text-align: center;
            margin: 1.5rem 0;
        }

        .auth-divider::before,
        .auth-divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid #e5e7eb;
        }

        .auth-divider span {
            padding: 0 1rem;
            color: #6b7280;
            font-size: 0.875rem;
            font-weight: 500;
        }

        /* Info banner */
        .auth-info {
            padding: 0.875rem 1rem;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }

        .auth-info p {
            margin: 0;
            color: #1e40af;
            font-size: 0.875rem;
            line-height: 1.5;
        }

        /* Form styling */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1.5px solid #e5e7eb;
            padding: 0.625rem 0.875rem;
            font-size: 0.95rem;
        }

        .stTextInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        /* Primary button */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }

        /* Secondary link button */
        .auth-secondary {
            text-align: center;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e5e7eb;
        }

        .auth-secondary p {
            color: #6b7280;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }

        .auth-secondary a {
            color: #3b82f6;
            font-weight: 600;
            text-decoration: none;
        }

        .auth-secondary a:hover {
            color: #2563eb;
            text-decoration: underline;
        }

        /* Success/Error messages */
        .stSuccess, .stError {
            border-radius: 8px;
            padding: 0.875rem 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)


def show_login_page():
    """Display modern SaaS-style login page"""
    apply_auth_styles()

    # Initialize auth manager
    auth = AuthManager()

    # ============================================================
    # HANDLE GOOGLE OAUTH CALLBACK
    # ============================================================
    try:
        query_params = st.query_params
        auth_code = query_params.get("code", None)
        state = query_params.get("state", "")

        if auth_code and not st.session_state.get('oauth_processed', False):
            st.session_state.oauth_processed = True

            with st.spinner("Signing in with Google..."):
                success, message, user_data = auth.exchange_google_code(auth_code, state)

            try:
                st.query_params.clear()
            except Exception as e:
                print(f"[WARNING] Could not clear query params: {e}")

            if success:
                st.session_state.authenticated = True
                st.session_state.user_email = user_data['email']
                st.session_state.user_role = user_data.get('role', 'user')
                st.session_state.user_name = user_data.get('name', '')
                st.session_state.auth_method = 'google_sso'
                st.success(f"✅ {message}")
                st.session_state.oauth_processed = False
                st.rerun()
            else:
                st.error(f"❌ {message}")
                st.session_state.oauth_processed = False
                try:
                    st.query_params.clear()
                except:
                    pass

    except Exception as e:
        print(f"[ERROR] OAuth callback handling failed: {e}")
        st.error(f"❌ OAuth callback error: {str(e)}")

    # ============================================================
    # LOGIN PAGE LAYOUT
    # ============================================================

    # Center column for auth card
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Logo/Brand
        st.markdown("""
        <div class="auth-logo">
            <h1>📋 Hiring Automation</h1>
            <p>Sign in to continue to your account</p>
        </div>
        """, unsafe_allow_html=True)

        # Get available OAuth clients
        if auth.is_google_auth_available():
            available_clients = auth.get_available_oauth_clients()

            if available_clients:
                # Info banner
                allowed_domains = auth.get_allowed_domains()
                domains_text = " & ".join([f"@{d}" for d in allowed_domains])

                st.markdown(f"""
                <div class="auth-info">
                    <p><strong>🔐 Authorized Access</strong><br>
                    Only {domains_text} emails are allowed</p>
                </div>
                """, unsafe_allow_html=True)

                # SSO Buttons
                for domain, display_name in available_clients:
                    google_url = auth.get_google_auth_url(domain)
                    st.markdown(f"""
                    <a href="{google_url}" class="sso-button">
                        <span class="sso-icon">🔑</span>
                        <span>Continue with Google ({display_name})</span>
                    </a>
                    """, unsafe_allow_html=True)

                # Divider
                st.markdown("""
                <div class="auth-divider">
                    <span>OR</span>
                </div>
                """, unsafe_allow_html=True)

        # Email/Password Login Form
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="login_email"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )

            submit = st.form_submit_button("Sign in", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("❌ Please enter both email and password")
                else:
                    success, message, user_data = auth.login_user(email, password)

                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_role = user_data['role']
                        st.session_state.user_name = user_data.get('name', email.split('@')[0])
                        st.session_state.auth_method = 'password'
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

        # Register link
        st.markdown("""
        <div class="auth-secondary">
            <p>Don't have an account?</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Create an account", use_container_width=True, type="secondary"):
            st.session_state.show_register = True
            st.rerun()


def show_register_page():
    """Display modern SaaS-style registration page"""
    apply_auth_styles()

    # Initialize auth manager
    auth = AuthManager()

    # Center column for auth card
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Logo/Brand
        st.markdown("""
        <div class="auth-logo">
            <h1>📋 Hiring Automation</h1>
            <p>Create your account</p>
        </div>
        """, unsafe_allow_html=True)

        # SSO Recommendation
        if auth.is_google_auth_available():
            available_clients = auth.get_available_oauth_clients()

            if available_clients:
                allowed_domains = auth.get_allowed_domains()
                domains_text = " or ".join([f"@{d}" for d in allowed_domains])

                st.markdown(f"""
                <div class="auth-info">
                    <p><strong>💡 Recommended</strong><br>
                    If you have a {domains_text} email, use Google Sign-In for instant access</p>
                </div>
                """, unsafe_allow_html=True)

                # Back to login button
                if st.button("← Back to Sign In", use_container_width=True, type="secondary"):
                    st.session_state.show_register = False
                    st.rerun()

                # Divider
                st.markdown("""
                <div class="auth-divider">
                    <span>OR REGISTER WITH EMAIL</span>
                </div>
                """, unsafe_allow_html=True)

        # Registration Form
        with st.form("register_form", clear_on_submit=False):
            email = st.text_input(
                "Email address",
                placeholder="you@example.com",
                key="register_email"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="At least 6 characters",
                key="register_password"
            )
            password_confirm = st.text_input(
                "Confirm password",
                type="password",
                placeholder="Re-enter your password",
                key="register_password_confirm"
            )

            submit = st.form_submit_button("Create account", use_container_width=True)

            if submit:
                if not email or not password or not password_confirm:
                    st.error("❌ Please fill in all fields")
                elif password != password_confirm:
                    st.error("❌ Passwords do not match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    success, message = auth.register_user(email, password, role="user")

                    if success:
                        st.success(f"✅ {message}")
                        st.info("You can now sign in with your credentials")
                        st.balloons()

                        import time
                        time.sleep(2)
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

        # Sign in link
        st.markdown("""
        <div class="auth-secondary">
            <p>Already have an account?</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Sign in instead", use_container_width=True, type="secondary"):
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
