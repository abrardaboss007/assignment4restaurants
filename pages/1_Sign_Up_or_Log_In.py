import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate("pages/userauthentication-51220-36b0a62c489f.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Main app function
def app():
    st.title("Create Account or Sign In")

    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "useremail" not in st.session_state:
        st.session_state.useremail = ""

    # Logout function
    def logout():
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.useremail = ""

    # Logged-in view
    if st.session_state.logged_in:
        st.header("Account information")
        #st.header("Account Information")
        st.text(f"Username: {st.session_state.username}")
        st.text(f"Email: {st.session_state.useremail}")
        if st.button("Sign Out"):
            logout()
            st.success("You have been signed out. Please click another page and come back to Sign Up/Log In again")

    # Login/Signup view
    else:
        choice = st.selectbox("Login or Sign Up", ["Login", "Sign Up"])

        if choice == "Login":
            email_login = st.text_input("Email Address")
            password_login = st.text_input("Password", type="password")
            if st.button("Login"):
                try:
                    user = auth.get_user_by_email(email=email_login)
                    # Simulate password verification (use Firebase Client SDK in real apps)
                    if password_login:  # 
                        st.session_state.logged_in = True
                        st.session_state.username = user.uid
                        st.session_state.useremail = user.email
                        st.success(f"Welcome back, {user.email}! Please click another page and come back to see account info")
                    else:
                        st.error("Password is incorrect.")
                except firebase_admin.exceptions.FirebaseError:
                    st.error("Email not recognized.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        elif choice == "Sign Up":
            username = st.text_input("Username")
            email_signup = st.text_input("Email Address")
            password_signup_1 = st.text_input("Password", type="password")
            password_signup_2 = st.text_input("Confirm Password", type="password")
            if st.button("Create Account"):
                if password_signup_1 != password_signup_2:
                    if not email_signup or not username or not password_signup_1 or not password_signup_2:
                        st.error("Passwords do not match")
                        st.error("Please fill in all the fields")
                    else:
                        st.error("Passwords do not match")
                else:
                    try:
                        user = auth.create_user(
                            email=email_signup,
                            password=password_signup_1,
                            uid=username
                        )
                        st.success("Account created successfully! Please log in.")
                        st.balloons()
                    except firebase_admin.exceptions.FirebaseError:
                        st.error("Failed to create account. Please try again.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    app()
