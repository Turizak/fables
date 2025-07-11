import random
from django.core.management.base import BaseCommand
from accounts.models import Account


class Command(BaseCommand):
    help = 'Seed the database with sample account data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of accounts to create (default: 10)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force seeding even if accounts already exist'
        )

    def handle(self, *args, **options):
        count = options['count']
        force = options['force']

        if not force and Account.objects.exists():
            self.stdout.write(
                self.style.WARNING('Accounts already exist. Use --force to seed anyway.')
            )
            return

        # Sample usernames for seeding
        sample_usernames = [
            'alice_smith', 'bob_jones', 'charlie_brown', 'diana_prince',
            'ethan_hunt', 'fiona_green', 'george_martin', 'hannah_davis',
            'ian_fleming', 'julia_roberts', 'kevin_hart', 'luna_lovegood',
            'mike_tyson', 'nina_simone', 'oscar_wilde', 'penny_lane',
            'quinn_fabray', 'rachel_green', 'steve_jobs', 'tina_turner',
            'ursula_burns', 'victor_hugo', 'wanda_maximoff', 'xavier_woods',
            'yasmin_bleeth', 'zoe_saldana', 'admin_user', 'test_user',
            'demo_user', 'sample_user'
        ]

        created_count = 0
        for i in range(count):
            # Use sample usernames or generate numbered ones if we exceed the list
            if i < len(sample_usernames):
                username = sample_usernames[i]
            else:
                username = f'user_{i + 1}'

            # Check if username already exists to avoid duplicates
            if not Account.objects.filter(username=username).exists():
                Account.objects.create(username=username)
                created_count += 1
                self.stdout.write(f'Created account: {username}')
            else:
                self.stdout.write(f'Account {username} already exists, skipping')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} accounts')
        )