
from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('personal', 'Personal'),
    ('professional', 'Professional'),
    ('family', 'Family'),
    ('vendor', 'Vendor'),
    ('other', 'Other'),
]

ROLE_CHOICES = [
    ('user', 'Standard User'),
    ('manager', 'Manager'),
    ('admin', 'Administrator'),
    ('premium', 'Premium User'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=120, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    company = models.CharField(max_length=120, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, blank=True)
    favorite = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company})" if self.company else self.name

class ContactNote(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.contact.name} @ {self.created_at:%Y-%m-%d}"
