from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from .models import UserInformation
from django.contrib import messages
import subprocess

# Create your views here.

def index(request):
    return render(request, 'index.html')

def language(request):
    return render(request, 'language.html')

def setquestion(request):
    return render(request, 'setquestion.html')

def level(request):
    return render(request, 'level.html')

def feedback(request):
    script_output = request.COOKIES.get('script_output', 'No script output found')
    editor_content = request.COOKIES.get('editor_content', 'No code found')
    
    context = {
        'script_output': script_output,
        'editor_content': editor_content,
    }
    
    return render(request, 'feedback.html', context)

def answer(request):
    selected_language = request.GET.get('language', 'default_language')
    selected_questions = request.GET.get('questions', 'default_questions')
    selected_level = request.GET.get('level', 'default_level')

    script_path = 'scripts/index.py'  # Path to your Python script
    try:
        # Execute the script with arguments
        result = subprocess.run(
            ['python', script_path, selected_language, selected_questions, selected_level],
            capture_output=True, text=True
        )
        output = result.stdout
    except Exception as e:
        output = f'Error running script: {e}'
    return render(request, 'answer.html', {'script_output': output})

def login(request):
    if request.method == 'POST':
        # Retrieve username and password from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user_info = authenticate(request, username=username, password=password)
        
        if user_info is not None:
            # Log the user in and redirect to the index page
            auth_login(request, user_info)
            messages.success(request, 'Account login successfully')
            return redirect('index.html')
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password')
    
    # Render the login page for GET requests or failed POST requests
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if UserInformation.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif UserInformation.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            UserInformation.objects.create(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('login')
    return render(request, 'login.html')