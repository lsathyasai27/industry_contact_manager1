
from django import forms
from .models import Contact, ContactNote

class ContactForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class':'form-control glass-input',
            'placeholder':'Tags separated by commas',
        }),
        help_text='Add tags to categorize this contact.',
    )

    class Meta:
        model = Contact
        fields = [
            'name',
            'company',
            'job_title',
            'phone',
            'email',
            'birthday',
            'category',
            'favorite',
            'address',
        ]
        widgets = {
            'birthday': forms.DateInput(attrs={'type':'date', 'class':'form-control glass-input'}),
            'favorite': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'favorite':
                field.widget.attrs.update({'class': 'form-control glass-input'})
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join(self.instance.tags.values_list('name', flat=True))

class ContactNoteForm(forms.ModelForm):
    class Meta:
        model = ContactNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'form-control glass-input',
                'rows': 4,
                'placeholder': 'Add a note or history update for this contact',
            }),
        }

class CSVImportForm(forms.Form):
    file = forms.FileField(
        label='Upload CSV file',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control glass-input'}),
    )
