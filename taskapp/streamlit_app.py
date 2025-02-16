import streamlit as st
import requests
import jwt  # PyJWT for decoding the JWT token

# Base URL of your Django API
API_BASE = "http://127.0.0.1:8000/api"

def register(username, email, password):
    url = f"{API_BASE}/register/"
    payload = {"username": username, "email": email, "password": password}
    response = requests.post(url, json=payload)
    return response

def login(username, password):
    url = f"{API_BASE}/login/"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    return response

def get_apps(token):
    url = f"{API_BASE}/apps/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response

def add_app(token, name, points, description):
    url = f"{API_BASE}/apps/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"name": name, "points": points, "description": description}
    response = requests.post(url, headers=headers, json=payload)
    return response

def logout():
    # Clear authentication tokens and admin flag from session state
    st.session_state.pop("access_token", None)
    st.session_state.pop("refresh_token", None)
    st.session_state.pop("is_admin", None)
    st.success("Logged out successfully!")
    st.experimental_rerun()

def main():
    st.title("Django Evaluation App - Streamlit UI")
    
    # Sidebar menu for navigation
    menu = ["Register", "Login", "Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Register":
        st.subheader("Register")
        username = st.text_input("Username", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register"):
            res = register(username, email, password)
            if res.status_code == 201:
                st.success("Registration successful! Please log in.")
            else:
                st.error(f"Registration failed: {res.text}")

    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            res = login(username, password)
            if res.status_code == 200:
                token_data = res.json()
                st.session_state['access_token'] = token_data.get("access")
                st.session_state['refresh_token'] = token_data.get("refresh")

                # Print the raw JWT access token for debugging:
                st.write("Raw Access Token:", token_data.get("access"))

                # Decode the token to check for admin status
                try:
                    decoded = jwt.decode(token_data.get("access"), options={"verify_signature": False})
                    # Check if user is admin by is_staff or is_superuser flag in the token
                    st.session_state['is_admin'] = decoded.get("is_staff", False) or decoded.get("is_superuser", False)
                except Exception as e:
                    st.error(f"Error decoding token: {e}")
                    st.session_state['is_admin'] = False
                st.success("Login successful!")
            else:
                st.error(f"Login failed: {res.text}")
                
    elif choice == "Dashboard":
        st.subheader("Dashboard - Available Android Apps")
        
        # Layout: create three columns for positioning (left, center, right)
        col1, col2, col3 = st.columns([1, 8, 1])
        
        token = st.session_state.get("access_token")
        
        # Display logout button only if token exists
        if token:
            with col3:
                if st.button("Logout"):
                    logout()
        
        # Fetch and display apps only if user is logged in
        if token:
            res = get_apps(token)
            if res.status_code == 200:
                apps = res.json()
                if apps:
                    for app in apps:
                        st.markdown(f"**{app.get('name')}** - Points: {app.get('points')}")
                else:
                    st.info("No apps available.")
            else:
                st.error(f"Error fetching apps: {res.text}")
            
            # Check if the logged-in user is admin using the decoded flag
            if st.session_state.get("is_admin"):
                st.subheader("Admin Options: Add a New Application")
                admin_name = st.text_input("App Name", key="admin_app_name")
                admin_points = st.number_input("Points", value=0, step=1, key="admin_app_points")
                admin_desc = st.text_area("Description", key="admin_app_desc")
                if st.button("Add App"):
                    add_response = add_app(token, admin_name, admin_points, admin_desc)
                    if add_response.status_code == 201:
                        st.success("Application added successfully!")
                        st.experimental_rerun()
                    else:
                        st.error(f"Failed to add application: {add_response.text}")
            else:
                st.info("You are not an admin. Admin options are hidden.")
                
            # Display the is_admin flag for debugging purposes
            st.markdown(f"**is_admin:** {st.session_state.get('is_admin', False)}")
        else:
            st.warning("Please log in to view the dashboard.")

if __name__ == '__main__':
    main()
