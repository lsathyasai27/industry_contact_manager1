from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from contacts.models import Contact, Tag, UserProfile
from datetime import date

class Command(BaseCommand):
    help = 'Load sample contacts for demonstration'

    def handle(self, *args, **options):
        # Get or create the first superuser
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No users found. Create a user first.'))
            return

        # Create or get additional users
        users = {
            'user1': User.objects.get_or_create(username='user1', defaults={'email': 'user1@example.com'})[0],
            'user2': User.objects.get_or_create(username='user2', defaults={'email': 'user2@example.com'})[0],
        }
        
        # Ensure passwords are set
        if users['user1'].password.startswith('!'):
            users['user1'].set_password('password123')
            users['user1'].save()
        if users['user2'].password.startswith('!'):
            users['user2'].set_password('password123')
            users['user2'].save()
        
        # Create user profiles with roles
        for username, user_obj in users.items():
            profile, _ = UserProfile.objects.get_or_create(user=user_obj)
            if username == 'user1':
                profile.role = 'manager'
                profile.company = 'TCS'
                profile.job_title = 'Project Manager'
            else:
                profile.role = 'premium'
                profile.company = 'Infosys'
                profile.job_title = 'Team Lead'
            profile.save()

        # Sample contacts for main user
        sample_contacts_main = [
            {
                'name': 'Rajesh Kumar',
                'company': 'Tata Consultancy Services',
                'job_title': 'Senior Developer',
                'phone': '9876543210',
                'email': 'rajesh.kumar@tcs.com',
                'address': '123 Cyber City, Hyderabad, Telangana 500081',
                'birthday': date(1990, 5, 15),
                'category': 'professional',
                'favorite': True,
                'tags': ['developer', 'python', 'urgent'],
            },
            {
                'name': 'Priya Sharma',
                'company': 'Infosys Limited',
                'job_title': 'Brand Manager',
                'phone': '8765432109',
                'email': 'priya.sharma@infosys.com',
                'address': '456 MG Road, Bangalore, Karnataka 560001',
                'birthday': date(1992, 8, 22),
                'category': 'professional',
                'favorite': True,
                'tags': ['marketing', 'creative', 'partner'],
            },
            {
                'name': 'Amit Patel',
                'company': 'HDFC Bank',
                'job_title': 'CFO',
                'phone': '7654321098',
                'email': 'amit.patel@hdfc.com',
                'address': '789 Fort Complex, Mumbai, Maharashtra 400001',
                'birthday': date(1985, 3, 10),
                'category': 'professional',
                'favorite': False,
                'tags': ['finance', 'executive'],
            },
            {
                'name': 'Ananya Gupta',
                'company': 'Apollo Hospitals',
                'job_title': 'Project Manager',
                'phone': '6543210987',
                'email': 'ananya.gupta@apollo.com',
                'address': '321 Medical Plaza, Delhi, Delhi 110001',
                'birthday': date(1995, 11, 5),
                'category': 'professional',
                'favorite': True,
                'tags': ['healthcare', 'management'],
            },
            {
                'name': 'Vikram Singh',
                'company': 'Design Studios India',
                'job_title': 'UI/UX Designer',
                'phone': '5432109876',
                'email': 'vikram.singh@designstudios.com',
                'address': '654 Creative District, Pune, Maharashtra 411001',
                'birthday': date(1993, 7, 18),
                'category': 'professional',
                'favorite': False,
                'tags': ['design', 'ui', 'ux'],
            },
            {
                'name': 'Divya Nair',
                'company': 'Amazon India',
                'job_title': 'Sales Director',
                'phone': '4321098765',
                'email': 'divya.nair@amazon.com',
                'address': '987 Tech Park, Bangalore, Karnataka 560103',
                'birthday': date(1988, 2, 14),
                'category': 'professional',
                'favorite': True,
                'tags': ['sales', 'ecommerce'],
            },
            {
                'name': 'Rohit Verma',
                'company': 'Consulting Group',
                'job_title': 'Business Consultant',
                'phone': '3210987654',
                'email': 'rohit.verma@consulting.com',
                'address': '111 Business Hub, Gurugram, Haryana 122001',
                'birthday': date(1987, 9, 3),
                'category': 'professional',
                'favorite': False,
                'tags': ['consulting', 'business'],
            },
            {
                'name': 'Neha Deshmukh',
                'company': '---',
                'job_title': 'College Friend',
                'phone': '2109876543',
                'email': 'neha.d@email.com',
                'address': '222 Residential Complex, Pune, Maharashtra 411006',
                'birthday': date(1994, 4, 28),
                'category': 'personal',
                'favorite': True,
                'tags': ['college', 'close-friend'],
            },
            {
                'name': 'Suresh Reddy',
                'company': 'Acme India Suppliers',
                'job_title': 'Account Manager',
                'phone': '1098765432',
                'email': 'suresh.reddy@acme.com',
                'address': '333 Industrial Area, Chennai, Tamil Nadu 600096',
                'birthday': date(1991, 6, 11),
                'category': 'vendor',
                'favorite': False,
                'tags': ['vendor', 'supplier'],
            },
            {
                'name': 'Meera Chopra',
                'company': 'Digital Marketing Solutions',
                'job_title': 'Content Lead',
                'phone': '9123456789',
                'email': 'meera.chopra@digmark.com',
                'address': '444 Media Street, Jaipur, Rajasthan 302001',
                'birthday': date(1996, 12, 7),
                'category': 'professional',
                'favorite': True,
                'tags': ['content', 'marketing', 'social-media'],
            },
        ]

        # Sample contacts for user1
        sample_contacts_user1 = [
            {
                'name': 'Arjun Menon',
                'company': 'Wipro Technologies',
                'job_title': 'Senior Architect',
                'phone': '9876543211',
                'email': 'arjun.menon@wipro.com',
                'address': '150 Tech Tower, Bangalore, Karnataka 560001',
                'birthday': date(1988, 1, 20),
                'category': 'professional',
                'favorite': True,
                'tags': ['architecture', 'enterprise'],
            },
            {
                'name': 'Shreya Das',
                'company': 'Accenture India',
                'job_title': 'Solutions Manager',
                'phone': '8765432110',
                'email': 'shreya.das@accenture.com',
                'address': '200 IT Park, Noida, Uttar Pradesh 201301',
                'birthday': date(1993, 7, 15),
                'category': 'professional',
                'favorite': True,
                'tags': ['consulting', 'solutions'],
            },
            {
                'name': 'Karan Malhotra',
                'company': 'Google India',
                'job_title': 'Product Manager',
                'phone': '7654321099',
                'email': 'karan.malhotra@google.com',
                'address': '350 One Google Building, Hyderabad, Telangana 500081',
                'birthday': date(1991, 4, 10),
                'category': 'professional',
                'favorite': False,
                'tags': ['product', 'tech'],
            },
        ]

        # Sample contacts for user2
        sample_contacts_user2 = [
            {
                'name': 'Snehal Joshi',
                'company': 'Microsoft India',
                'job_title': 'Cloud Specialist',
                'phone': '6543210988',
                'email': 'snehal.joshi@microsoft.com',
                'address': '400 Azure Plaza, Pune, Maharashtra 411001',
                'birthday': date(1995, 9, 25),
                'category': 'professional',
                'favorite': True,
                'tags': ['cloud', 'azure'],
            },
            {
                'name': 'Nikhil Bhat',
                'company': 'IBM India',
                'job_title': 'Data Engineer',
                'phone': '5432109877',
                'email': 'nikhil.bhat@ibm.com',
                'address': '500 Tech Road, Mumbai, Maharashtra 400092',
                'birthday': date(1992, 3, 8),
                'category': 'professional',
                'favorite': True,
                'tags': ['data', 'bigdata'],
            },
        ]

        # Create tags
        tag_cache = {}
        all_tags = ['developer', 'python', 'urgent', 'marketing', 'creative', 'partner', 'finance', 'executive', 'healthcare', 'management', 'design', 'ui', 'ux', 'sales', 'ecommerce', 'consulting', 'business', 'college', 'close-friend', 'vendor', 'supplier', 'content', 'social-media', 'architecture', 'enterprise', 'solutions', 'product', 'tech', 'cloud', 'azure', 'data', 'bigdata']
        for tag_name in all_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_cache[tag_name] = tag

        # Create contacts for each user
        contact_sets = [
            (user, sample_contacts_main),
            (users['user1'], sample_contacts_user1),
            (users['user2'], sample_contacts_user2),
        ]

        for current_user, contacts_data in contact_sets:
            for contact_data in contacts_data:
                tags = contact_data.pop('tags')
                contact, created = Contact.objects.get_or_create(
                    user=current_user,
                    name=contact_data['name'],
                    defaults=contact_data
                )
                if created:
                    for tag_name in tags:
                        contact.tags.add(tag_cache[tag_name])
                    self.stdout.write(self.style.SUCCESS(f'Created contact for {current_user.username}: {contact.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Contact already exists for {current_user.username}: {contact.name}'))

        self.stdout.write(self.style.SUCCESS('Sample contacts loaded successfully!'))
