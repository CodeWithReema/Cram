from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Deck(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']

class Flashcard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='flashcards')
    front = models.TextField()
    back = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.front[:50]}..."

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name='progress')
    last_reviewed = models.DateTimeField(default=timezone.now)
    next_review = models.DateTimeField(default=timezone.now)
    ease_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=0)
    repetitions = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.flashcard.front[:50]}..."

    class Meta:
        unique_together = ['user', 'flashcard']

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='documents')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Only allow specific file types
    file_extension_validator = FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx']
    )

    def __str__(self):
        return self.title

    def get_file_extension(self):
        return self.file.name.split('.')[-1].lower()

    def get_file_icon(self):
        extension = self.get_file_extension()
        icon_map = {
            'pdf': 'fa-file-pdf',
            'doc': 'fa-file-word',
            'docx': 'fa-file-word',
            'txt': 'fa-file-alt',
            'ppt': 'fa-file-powerpoint',
            'pptx': 'fa-file-powerpoint'
        }
        return icon_map.get(extension, 'fa-file')

class Test(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='tests')
    is_completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.deck.title}"

class Question(models.Model):
    QUESTION_TYPES = [
        ('MC', 'Multiple Choice'),
        ('TF', 'True/False'),
        ('SA', 'Short Answer'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    correct_answer = models.TextField()
    options = models.JSONField(null=True, blank=True)  # For multiple choice questions
    user_answer = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Question for {self.test.title}"
