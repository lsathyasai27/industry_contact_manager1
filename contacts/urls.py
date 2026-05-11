
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_contact, name='add'),
    path('edit/<int:id>/', views.edit_contact, name='edit'),
    path('delete/<int:id>/', views.delete_contact, name='delete'),
    path('contact/<int:id>/', views.contact_detail, name='contact_detail'),
    path('toggle-favorite/<int:id>/', views.toggle_favorite, name='toggle_favorite'),
    path('import/', views.import_contacts, name='import_contacts'),
    path('export/', views.export_contacts, name='export_contacts'),
    path('api/contacts/', views.api_contacts, name='api_contacts'),
    path('api/contacts/<int:id>/', views.api_contact_detail, name='api_contact_detail'),
    path('profile/', views.profile, name='profile'),
]
