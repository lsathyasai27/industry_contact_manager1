
from io import TextIOWrapper
import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse

from .models import Contact, Tag, ContactNote, UserProfile
from .forms import ContactForm, ContactNoteForm, CSVImportForm


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')
    return render(request, 'contacts/register.html', {'form': form})


def login_view(request):
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        error = 'Invalid username or password'
    return render(request, 'contacts/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


def _sync_tags(contact, tag_string):
    tag_names = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
    tags = []
    for name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=name)
        tags.append(tag)
    contact.tags.set(tags)


@login_required
def dashboard(request):
    query = request.GET.get('q', '').strip()
    contacts = Contact.objects.filter(user=request.user)

    if query:
        contacts = contacts.filter(
            Q(name__icontains=query)
            | Q(company__icontains=query)
            | Q(job_title__icontains=query)
            | Q(email__icontains=query)
            | Q(address__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()

    favorites_count = contacts.filter(favorite=True).count()
    
    # Calculate new contacts this month
    from django.utils import timezone
    from datetime import timedelta
    this_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_this_month = contacts.filter(created_at__gte=this_month_start).count()
    
    paginator = Paginator(contacts.order_by('-created_at'), 6)
    page = request.GET.get('page')
    contacts_page = paginator.get_page(page)

    return render(request, 'contacts/dashboard.html', {
        'contacts': contacts_page,
        'total': Contact.objects.filter(user=request.user).count(),
        'favorites_count': favorites_count,
        'new_this_month': new_this_month,
        'query': query,
    })


@login_required
def add_contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        _sync_tags(contact, form.cleaned_data.get('tags', ''))
        messages.success(request, 'Contact added successfully')
        return redirect('dashboard')
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Add Contact'})


@login_required
def edit_contact(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)
    form = ContactForm(request.POST or None, instance=contact)
    if form.is_valid():
        contact = form.save()
        _sync_tags(contact, form.cleaned_data.get('tags', ''))
        messages.success(request, 'Contact updated successfully')
        return redirect('contact_detail', id=contact.id)
    return render(request, 'contacts/contact_form.html', {'form': form, 'title': 'Edit Contact'})


@login_required
def contact_detail(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)
    note_form = ContactNoteForm(request.POST or None)
    if request.method == 'POST' and note_form.is_valid():
        note = note_form.save(commit=False)
        note.contact = contact
        note.save()
        messages.success(request, 'Note added to contact')
        return redirect('contact_detail', id=id)
    return render(request, 'contacts/contact_detail.html', {
        'contact': contact,
        'note_form': note_form,
        'notes': contact.notes.all().order_by('-created_at'),
    })


@login_required
def toggle_favorite(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)
    contact.favorite = not contact.favorite
    contact.save()
    status = 'added to favorites' if contact.favorite else 'removed from favorites'
    messages.success(request, f'{contact.name} {status}')
    return redirect('dashboard')


@login_required
def delete_contact(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)
    contact.delete()
    messages.success(request, 'Contact deleted')
    return redirect('dashboard')


@login_required
def import_contacts(request):
    form = CSVImportForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            contact = Contact.objects.create(
                user=request.user,
                name=row.get('name', '').strip() or 'Unnamed',
                company=row.get('company', '').strip(),
                job_title=row.get('job_title', '').strip(),
                phone=row.get('phone', '').strip(),
                email=row.get('email', '').strip(),
                address=row.get('address', '').strip(),
                category=row.get('category', '').strip(),
                favorite=row.get('favorite', '').strip().lower() in ['true', '1', 'yes'],
            )
            birthday = row.get('birthday', '').strip()
            if birthday:
                try:
                    contact.birthday = birthday
                    contact.save()
                except ValueError:
                    pass
            _sync_tags(contact, row.get('tags', ''))
            count += 1
        messages.success(request, f'{count} contacts imported successfully')
        return redirect('dashboard')
    return render(request, 'contacts/import_contacts.html', {'form': form})


@login_required
def export_contacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['name', 'company', 'job_title', 'phone', 'email', 'address', 'birthday', 'category', 'favorite', 'tags'])
    for contact in Contact.objects.filter(user=request.user).order_by('name'):
        tags = ', '.join(contact.tags.values_list('name', flat=True))
        writer.writerow([
            contact.name,
            contact.company,
            contact.job_title,
            contact.phone,
            contact.email,
            contact.address,
            contact.birthday or '',
            contact.category,
            'yes' if contact.favorite else 'no',
            tags,
        ])
    return response


@login_required
def api_contacts(request):
    contacts = Contact.objects.filter(user=request.user).order_by('-created_at')
    data = [
        {
            'id': contact.id,
            'name': contact.name,
            'company': contact.company,
            'job_title': contact.job_title,
            'phone': contact.phone,
            'email': contact.email,
            'category': contact.category,
            'favorite': contact.favorite,
            'tags': list(contact.tags.values_list('name', flat=True)),
            'created_at': contact.created_at.isoformat(),
        }
        for contact in contacts
    ]
    return JsonResponse({'contacts': data})


@login_required
def api_contact_detail(request, id):
    contact = get_object_or_404(Contact, id=id, user=request.user)
    data = {
        'id': contact.id,
        'name': contact.name,
        'company': contact.company,
        'job_title': contact.job_title,
        'phone': contact.phone,
        'email': contact.email,
        'address': contact.address,
        'birthday': contact.birthday.isoformat() if contact.birthday else None,
        'category': contact.category,
        'favorite': contact.favorite,
        'tags': list(contact.tags.values_list('name', flat=True)),
        'notes': [{'id': note.id, 'note': note.note, 'created_at': note.created_at.isoformat()} for note in contact.notes.all().order_by('-created_at')],
    }
    return JsonResponse(data)


@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_contacts = Contact.objects.filter(user=request.user)
    
    total_contacts = user_contacts.count()
    favorite_contacts = user_contacts.filter(favorite=True).count()
    total_tags = Tag.objects.filter(contact__user=request.user).distinct().count()
    personal_contacts = user_contacts.filter(category='personal').count()
    professional_contacts = user_contacts.filter(category='professional').count()
    family_contacts = user_contacts.filter(category='family').count()
    other_contacts = user_contacts.filter(category__in=['vendor', 'other']).count()
    
    return render(request, 'contacts/profile.html', {
        'profile': user_profile,
        'total_contacts': total_contacts,
        'favorite_contacts': favorite_contacts,
        'total_tags': total_tags,
        'personal_contacts': personal_contacts,
        'professional_contacts': professional_contacts,
        'family_contacts': family_contacts,
        'other_contacts': other_contacts,
    })
