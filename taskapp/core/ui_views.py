from django.shortcuts import render, redirect
from django.contrib import messages
import requests

# Helper function to build full URL for API endpoints
def get_api_url(request, endpoint):
    return request.build_absolute_uri(endpoint)

# Registration UI view
def ui_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # Build API URL (assuming /api/register/ is your endpoint)
        api_url = get_api_url(request, '/api/register/')
        data = {"username": username, "email": email, "password": password}
        response = requests.post(api_url, json=data)
        if response.status_code == 201:
            messages.success(request, "Registration successful. Please log in.")
            return redirect("ui_login")
        else:
            messages.error(request, "Registration failed: " + response.text)
    return render(request, "registration.html")

# Login UI view
def ui_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        api_url = get_api_url(request, '/api/login/')
        data = {"username": username, "password": password}
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            token_data = response.json()
            # Save tokens in session
            request.session['access_token'] = token_data.get("access")
            request.session['refresh_token'] = token_data.get("refresh")
            return redirect("dashboard")
        else:
            messages.error(request, "Login failed: " + response.text)
    return render(request, "login.html")

# Dashboard view (example: display list of Android apps)
def dashboard(request):
    access_token = request.session.get("access_token")
    if not access_token:
        messages.info(request, "Please log in first.")
        return redirect("ui_login")
    headers = {"Authorization": f"Bearer {access_token}"}
    api_url = get_api_url(request, '/api/apps/')
    response = requests.get(api_url, headers=headers)
    apps = response.json() if response.status_code == 200 else []
    return render(request, "dashboard.html", {"apps": apps})
