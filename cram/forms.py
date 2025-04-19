from django import forms
from .models import Deck, Flashcard, Document, Question

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['title', 'description', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['front', 'back']
        widgets = {
            'front': forms.Textarea(attrs={'rows': 3}),
            'back': forms.Textarea(attrs={'rows': 3}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }

class TestGenerationForm(forms.Form):
    title = forms.CharField(max_length=200, required=True)
    num_questions = forms.IntegerField(
        min_value=5,
        max_value=20,
        initial=10,
        help_text="Number of questions to generate (5-20)"
    )
    question_types = forms.MultipleChoiceField(
        choices=Question.QUESTION_TYPES,
        widget=forms.CheckboxSelectMultiple,
        initial=['MC', 'TF', 'SA'],
        help_text="Select question types to include"
    )
    difficulty = forms.ChoiceField(
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard')
        ],
        initial='medium',
        help_text="Select difficulty level"
    ) 