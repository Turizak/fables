from django.core.management.base import BaseCommand
from django.core.management import call_command
from accounts.models import Account
from campaigns.models import Campaign


class Command(BaseCommand):
    help = 'Seed the database with all sample data (accounts and campaigns)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--accounts',
            type=int,
            default=10,
            help='Number of accounts to create (default: 10)'
        )
        parser.add_argument(
            '--campaigns',
            type=int,
            default=20,
            help='Number of campaigns to create (default: 20)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force seeding even if data already exists'
        )

    def handle(self, *args, **options):
        accounts_count = options['accounts']
        campaigns_count = options['campaigns']
        force = options['force']

        # Check current state of database
        current_accounts = Account.objects.count()
        current_campaigns = Campaign.objects.count()
        
        accounts_exist = current_accounts > 0
        campaigns_exist = current_campaigns > 0

        self.stdout.write(f'Current state: {current_accounts} accounts, {current_campaigns} campaigns')

        # Determine what needs to be seeded
        need_accounts = not accounts_exist or force
        need_campaigns = not campaigns_exist or force

        if not force and accounts_exist and campaigns_exist:
            self.stdout.write(
                self.style.WARNING(
                    'Database already contains both accounts and campaigns. Use --force to seed anyway.'
                )
            )
            return

        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Seed accounts if needed
        if need_accounts:
            self.stdout.write('Seeding accounts...')
            call_command('seed_accounts', count=accounts_count, force=force)
        else:
            self.stdout.write(f'Accounts already exist ({current_accounts} found), skipping account seeding')

        # Seed campaigns if needed (and accounts exist)
        if need_campaigns:
            # Check again in case we just created accounts
            if Account.objects.exists():
                self.stdout.write('Seeding campaigns...')
                call_command('seed_campaigns', count=campaigns_count, force=force)
            else:
                self.stdout.write(self.style.ERROR('No accounts found, cannot create campaigns'))
        else:
            self.stdout.write(f'Campaigns already exist ({current_campaigns} found), skipping campaign seeding')

        # Final summary
        final_accounts = Account.objects.count()
        final_campaigns = Campaign.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeding completed successfully!\n'
                f'Total accounts: {final_accounts}\n'
                f'Total campaigns: {final_campaigns}'
            )
        )