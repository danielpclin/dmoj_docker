import csv
import io

import tqdm as tqdm
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string

from judge.models import Language, Profile, Organization


class Command(BaseCommand):
    help = 'Used to generate exam users'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', default=250, type=int, help='users count to create')
        parser.add_argument('--prefix', '-p', default='TEAM', help='prefix of the accounts')
        parser.add_argument('--email', '-e', default=None, help='email address to send the credentials to')
        parser.add_argument('--organization', '-o', default=None, type=int, help='organization id')
        parser.add_argument('--clear_orgs', '--clear_organizations', '-c', action='store_true', default=False,
                            help='if specified, clears the organizations of the user')

    def handle(self, *args, **options):
        if options['count'] <= 0:
            raise CommandError('Count must be a positive int.')
        f = io.StringIO()
        writer = csv.writer(f)
        credentials = []
        for i in range(1, options['count'] + 1):
            username = f"{options['prefix']}{i:0{len(str(options['count']))}}"
            password = get_random_string(8)
            credentials.append((username, password))
        writer.writerows(credentials)

        organization = None
        if options['organization'] is not None:
            try:
                organization = Organization.objects.get(pk=options['organization'])
                print(f"Using organization: {organization.name}")
            except Organization.DoesNotExist:
                print(f"Organization id {options['organization']} does not exist, skipping.")
        if options['email'] is not None:
            email_message = EmailMultiAlternatives(
                f"Generated accounts for exam, {options['count']} accounts with prefix {options['prefix']}, "
                f"Organization id {options['organization']}, clear_orgs {options['clear_orgs']}",
                f.getvalue(), settings.SITE_ADMIN_EMAIL, [options['email']])
            email_message.send()
            print("Email sent.")
        else:
            print(f.getvalue())
        f.close()

        print("Saving password to database...")

        for username, password in tqdm.tqdm(credentials):
            usr, created = User.objects.update_or_create(username=username, defaults={
                "password": make_password(password),
                "email": "",
                "is_active": True,
                "is_superuser": False,
                "is_staff": False
            })

            if created:
                profile = Profile(user=usr)
                profile.language = Language.objects.get(key=settings.DEFAULT_USER_LANGUAGE)
                profile.save()
            else:
                usr.refresh_from_db()
                profile = usr.profile

            if options['clear_orgs']:
                profile.organizations.clear()

            if organization is not None:
                profile.organizations.add(organization)
