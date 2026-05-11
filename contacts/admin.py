
from django.contrib import admin
from .models import Contact, Tag, ContactNote, UserProfile

class ContactNoteInline(admin.TabularInline):
    model = ContactNote
    extra = 0

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'company', 'job_title', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'company', 'job_title')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'phone', 'email', 'favorite', 'created_at')
    list_filter = ('favorite', 'category')
    search_fields = ('name', 'email', 'company', 'job_title')
    inlines = [ContactNoteInline]

admin.site.register(Tag)
admin.site.register(ContactNote)
