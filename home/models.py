from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserInformation(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    institute = models.CharField(max_length=50, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    # Use this method to set a hashed password
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    # Use this method to check the password
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Answer(models.Model):
    user = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    set_of_questions = models.IntegerField()
    level = models.CharField(max_length=50)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"Answer {self.id} by {self.user.username}"

class Feedback(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.id} for Answer {self.answer.id}"
