from django.urls import path
from . import views

app_name = 'cram'

urlpatterns = [
    path('', views.home, name='home'),
    path('decks/', views.deck_list, name='deck_list'),
    path('decks/create/', views.deck_create, name='deck_create'),
    path('decks/<int:deck_id>/', views.deck_detail, name='deck_detail'),
    path('decks/<int:deck_id>/edit/', views.deck_edit, name='deck_edit'),
    path('decks/<int:deck_id>/delete/', views.deck_delete, name='deck_delete'),
    path('decks/<int:deck_id>/cards/create/', views.card_create, name='card_create'),
    path('decks/<int:deck_id>/study/', views.study_deck, name='study_deck'),
    path('cards/<int:card_id>/edit/', views.card_edit, name='card_edit'),
    path('cards/<int:card_id>/delete/', views.card_delete, name='card_delete'),
    path('decks/<int:deck_id>/documents/', views.document_list, name='document_list'),
    path('decks/<int:deck_id>/documents/upload/', views.document_upload, name='document_upload'),
    path('documents/<int:document_id>/download/', views.document_download, name='document_download'),
    path('documents/<int:document_id>/delete/', views.document_delete, name='document_delete'),
    path('documents/<int:document_id>/generate-test/', views.generate_test, name='generate_test'),
    path('tests/<int:test_id>/', views.test_detail, name='test_detail'),
    path('tests/<int:test_id>/take/', views.take_test, name='take_test'),
    path('tests/<int:test_id>/results/', views.test_results, name='test_results'),
] 