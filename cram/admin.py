from django.contrib import admin
from .models import Deck, Flashcard, UserProgress

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('front', 'deck', 'created_at')
    list_filter = ('deck', 'created_at')
    search_fields = ('front', 'back')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'flashcard', 'last_reviewed', 'next_review')
    list_filter = ('user', 'last_reviewed')
    search_fields = ('user__username', 'flashcard__front')
