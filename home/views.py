from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserInformation, Answer
from django.contrib import messages
from .openai_service import evaluate_with_gemini, generate_new_answer
import subprocess

def index(request):
    return render(request, 'index.html')

def language(request):
    return render(request, 'language.html')

def setquestion(request):
    return render(request, 'setquestion.html')

def level(request):
    return render(request, 'level.html')

def logout(request):
    request.session.flush()  # Clear the session
    messages.success(request, 'Logged out successfully')
    return redirect('index')  # Redirect to index page after logout 

def feedback(request, answer_id):
    try:
        answer_instance = Answer.objects.get(id=answer_id)
    except Answer.DoesNotExist:
        return HttpResponse("Answer not found", status=404)

    question = answer_instance.question
    original_answer = answer_instance.answer

    # Retrieve API key from settings
    api_key = settings.GEMINI_API_KEY

    # Call Gemini API and get feedback
    is_correct, feedback_message = evaluate_with_gemini(question, original_answer, api_key)

    if not is_correct:
        # Generate a new answer using Gemini API with the API key
        new_answer = generate_new_answer(question, api_key)
    else:
        new_answer = None

    context = {
        'question': question,
        'original_answer': original_answer,
        'new_answer': new_answer,
        'feedback': feedback_message
    }

    return render(request, 'feedback.html', context)


def answer(request):
    selected_language = request.GET.get('language', 'default_language')
    selected_questions = request.GET.get('questions', '0')
    selected_level = request.GET.get('level', 'default_level')

    # Convert selected_questions to integer
    try:
        selected_questions = int(selected_questions)
    except ValueError:
        selected_questions = 0  # Provide a default value if conversion fails

    script_path = 'scripts/index.py'  # Path to your Python script
    try:
        # Execute the script with arguments
        result = subprocess.run(
            ['python', script_path, selected_language, str(selected_questions), selected_level],
            capture_output=True, text=True
        )
        output = result.stdout
    except Exception as e:
        output = f'Error running script: {e}'

    if request.method == 'POST':
        editor_content = request.POST.get('answer')
        question_content = request.POST.get('question')

        # Retrieve the logged-in user's username from the session
        username = request.session.get('username')
        if username:
            user = UserInformation.objects.get(username=username)
        else:
            messages.error(request, 'You must be logged in to submit an answer.')
            return redirect('login')

        # Save data to the Answer table
        answer_instance = Answer.objects.create(
            user= user,
            language=request.POST.get('language', selected_language),
            set_of_questions=request.POST.get('questions', selected_questions),
            level=request.POST.get('level', selected_level),
            question=question_content,
            answer=editor_content
        )
        return redirect('feedback', answer_id=answer_instance.id)

    context = {
        'selected_language': selected_language,
        'selected_questions': selected_questions,
        'selected_level': selected_level,
        'script_output': output,
    }

    return render(request, 'answer.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user_info = UserInformation.objects.get(username=username)
            if user_info.check_password(password):
                # Store user details in the session
                request.session['user_id'] = user_info.id
                request.session['username'] = user_info.username
                messages.success(request, 'Logged in successfully')
                return redirect('index')  # Redirect to the index page after login
            else:
                messages.error(request, 'Invalid username or password')
        except UserInformation.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        institute = request.POST.get('institute')
        
        if UserInformation.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif UserInformation.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            # Create a new user and hash the password
            user = UserInformation(username=username, email=email)
            user.set_password(password) #Hash the password
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    
    return render(request, 'signup.html')