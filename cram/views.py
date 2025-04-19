from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import FileResponse
from django.contrib.auth import logout
from .models import Deck, Flashcard, UserProgress, Document, Test, Question
from .forms import DeckForm, FlashcardForm, DocumentForm, TestGenerationForm
import google.generativeai as genai
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

def home(request):
    if request.user.is_authenticated:
        decks = Deck.objects.filter(user=request.user)
        public_decks = Deck.objects.filter(is_public=True).exclude(user=request.user)
    else:
        decks = []
        public_decks = Deck.objects.filter(is_public=True)
    
    return render(request, 'cram/home.html', {
        'decks': decks,
        'public_decks': public_decks
    })

@login_required
def deck_list(request):
    decks = Deck.objects.filter(user=request.user)
    return render(request, 'cram/deck_list.html', {'decks': decks})

@login_required
def deck_create(request):
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.user = request.user
            deck.save()
            messages.success(request, 'Deck created successfully!')
            return redirect('cram:deck_detail', deck_id=deck.id)
    else:
        form = DeckForm()
    return render(request, 'cram/deck_form.html', {'form': form})

@login_required
def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if deck.user != request.user and not deck.is_public:
        messages.error(request, 'You do not have permission to view this deck.')
        return redirect('cram:home')
    
    flashcards = deck.flashcards.all()
    return render(request, 'cram/deck_detail.html', {
        'deck': deck,
        'flashcards': flashcards
    })

@login_required
def deck_edit(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    if request.method == 'POST':
        form = DeckForm(request.POST, instance=deck)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deck updated successfully!')
            return redirect('cram:deck_detail', deck_id=deck.id)
    else:
        form = DeckForm(instance=deck)
    return render(request, 'cram/deck_form.html', {'form': form})

@login_required
def deck_delete(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    if request.method == 'POST':
        deck.delete()
        messages.success(request, 'Deck deleted successfully!')
        return redirect('cram:deck_list')
    return render(request, 'cram/deck_confirm_delete.html', {'deck': deck})

@login_required
def card_create(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.deck = deck
            card.save()
            messages.success(request, 'Card created successfully!')
            return redirect('cram:deck_detail', deck_id=deck.id)
    else:
        form = FlashcardForm()
    return render(request, 'cram/card_form.html', {'form': form, 'deck': deck})

@login_required
def study_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if deck.user != request.user and not deck.is_public:
        messages.error(request, 'You do not have permission to study this deck.')
        return redirect('cram:home')
    
    flashcards = list(deck.flashcards.all().values('front', 'back'))
    return render(request, 'cram/study_deck.html', {
        'deck': deck,
        'flashcards': flashcards
    })

@login_required
def card_edit(request, card_id):
    card = get_object_or_404(Flashcard, id=card_id)
    if card.deck.user != request.user:
        messages.error(request, 'You do not have permission to edit this card.')
        return redirect('cram:home')
    
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card updated successfully!')
            return redirect('cram:deck_detail', deck_id=card.deck.id)
    else:
        form = FlashcardForm(instance=card)
    return render(request, 'cram/card_form.html', {'form': form, 'deck': card.deck})

@login_required
def card_delete(request, card_id):
    card = get_object_or_404(Flashcard, id=card_id)
    if card.deck.user != request.user:
        messages.error(request, 'You do not have permission to delete this card.')
        return redirect('cram:home')
    
    if request.method == 'POST':
        deck_id = card.deck.id
        card.delete()
        messages.success(request, 'Card deleted successfully!')
        return redirect('cram:deck_detail', deck_id=deck_id)
    return render(request, 'cram/card_confirm_delete.html', {'card': card})

@login_required
def document_upload(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.deck = deck
            document.user = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('cram:deck_detail', deck_id=deck.id)
    else:
        form = DocumentForm()
    return render(request, 'cram/document_upload.html', {
        'form': form,
        'deck': deck
    })

@login_required
def document_delete(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if document.user != request.user:
        messages.error(request, 'You do not have permission to delete this document.')
        return redirect('cram:deck_detail', deck_id=document.deck.id)
    
    deck_id = document.deck.id
    document.delete()
    messages.success(request, 'Document deleted successfully!')
    return redirect('cram:deck_detail', deck_id=deck_id)

@login_required
def document_download(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    response = FileResponse(document.file)
    response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
    return response

def document_list(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    documents = Document.objects.filter(deck=deck)
    return render(request, 'cram/document_list.html', {
        'deck': deck,
        'documents': documents
    })

def generate_test(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    
    if request.method == 'POST':
        form = TestGenerationForm(request.POST)
        if form.is_valid():
            try:
                # Initialize Gemini
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-pro')
                
                # Read document content safely
                try:
                    with open(document.file.path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    messages.error(request, "Error reading document content. Please ensure the file is in UTF-8 format.")
                    return redirect('cram:document_list', deck_id=document.deck.id)
                except Exception as e:
                    messages.error(request, f"Error reading document: {str(e)}")
                    return redirect('cram:document_list', deck_id=document.deck.id)
                
                # Generate test using Gemini
                prompt = f"""
                Generate a test based on the following content. Create {form.cleaned_data['num_questions']} questions.
                Include these question types: {', '.join(form.cleaned_data['question_types'])}.
                Difficulty level: {form.cleaned_data['difficulty']}.
                
                For each question, provide:
                1. The question text
                2. The question type (MC, TF, or SA)
                3. The correct answer
                4. For multiple choice questions, provide 4 options
                
                Format the response as a JSON array of questions.
                
                Content:
                {content}
                """
                
                try:
                    response = model.generate_content(prompt)
                    questions_data = response.text
                except Exception as e:
                    messages.error(request, f"Error generating test: {str(e)}")
                    return redirect('cram:document_list', deck_id=document.deck.id)
                
                # Create test
                test = Test.objects.create(
                    deck=document.deck,
                    document=document,
                    title=form.cleaned_data['title']
                )
                
                # Parse questions_data and create Question objects
                try:
                    import json
                    questions = json.loads(questions_data)
                    for q in questions:
                        Question.objects.create(
                            test=test,
                            question_text=q['question_text'],
                            question_type=q['question_type'],
                            correct_answer=q['correct_answer'],
                            options=q.get('options', None)
                        )
                except json.JSONDecodeError:
                    messages.error(request, "Error parsing generated questions. Please try again.")
                    test.delete()  # Clean up the test if question creation fails
                    return redirect('cram:document_list', deck_id=document.deck.id)
                except Exception as e:
                    messages.error(request, f"Error creating questions: {str(e)}")
                    test.delete()  # Clean up the test if question creation fails
                    return redirect('cram:document_list', deck_id=document.deck.id)
                
                messages.success(request, "Test generated successfully!")
                return redirect('cram:test_detail', test_id=test.id)
                
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
                return redirect('cram:document_list', deck_id=document.deck.id)
    else:
        form = TestGenerationForm()
    
    return render(request, 'cram/generate_test.html', {
        'form': form,
        'document': document
    })

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'cram/test_detail.html', {
        'test': test
    })

def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    
    if request.method == 'POST':
        # Process answers and calculate score
        score = 0
        for question in test.questions.all():
            answer = request.POST.get(f'question_{question.id}')
            question.user_answer = answer
            question.is_correct = (answer.lower() == question.correct_answer.lower())
            question.save()
            
            if question.is_correct:
                score += 1
        
        test.score = score
        test.is_completed = True
        test.save()
        
        return redirect('test_results', test_id=test.id)
    
    return render(request, 'cram/take_test.html', {
        'test': test
    })

def test_results(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'cram/test_results.html', {
        'test': test
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
