from django.core.management.base import BaseCommand
from campaigns.models import Campaign
from accounts.models import Account


class Command(BaseCommand):
    help = 'Seed the database with sample campaign data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of campaigns to create (default: 10)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force seeding even if campaigns already exist'
        )

    def handle(self, *args, **options):
        count = options['count']
        force = options['force']

        if not force and Campaign.objects.exists():
            self.stdout.write(
                self.style.WARNING('Campaigns already exist. Use --force to seed anyway.')
            )
            return

        # Check if accounts exist
        accounts = list(Account.objects.all())
        if not accounts:
            self.stdout.write(
                self.style.ERROR('No accounts found. Please run seed_accounts first.')
            )
            return

        # Simple campaign names
        campaign_names = [
            'Summer Campaign', 'Winter Sale', 'Spring Launch', 'Fall Promotion',
            'Holiday Special', 'New Product Launch', 'Customer Survey', 'Brand Awareness',
            'Lead Generation', 'Email Campaign', 'Social Media Push', 'Flash Sale',
            'Loyalty Program', 'Beta Testing', 'Product Demo', 'Trade Show',
            'Content Marketing', 'Referral Program', 'Customer Retention', 'Black Friday'
        ]

        created_count = 0
        for i in range(count):
            # Use predefined names or generate numbered ones
            if i < len(campaign_names):
                name = campaign_names[i]
            else:
                name = f'Campaign {i + 1}'

            # Check if campaign name already exists
            if Campaign.objects.filter(name=name).exists():
                name = f'{name} ({i + 1})'

            # Assign first account for simplicity, or cycle through accounts
            account = accounts[i % len(accounts)]

            Campaign.objects.create(
                name=name,
                account_uuid=account
            )
            created_count += 1
            self.stdout.write(f'Created campaign: {name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} campaigns')
        )