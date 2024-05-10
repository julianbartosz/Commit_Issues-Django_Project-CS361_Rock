from django.core.management.base import BaseCommand
import requests
import time
from django.db import transaction
from user_management.models import User


def determine_role(user_data):
    title = user_data.get('title', '').lower()
    affiliation = user_data.get('affiliation', '').lower()

    if 'department chair' in title:
        return 'Supervisor'
    elif 'professor' in title or 'lecturer' in title:
        return 'Instructor'
    elif 'teaching assistant' in title or 'ta' in affiliation:
        return 'TA'
    else:
        return 'Student'


class Command(BaseCommand):
    help = 'Fetches user data from UWM directory'

    def handle(self, *args, **options):
        base_url = "https://apps.uwm.edu/directory/api/v1/people/all/"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://uwm.edu/',
            'Origin': 'https://uwm.edu',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'
        }

        page = 1
        while True:
            try:
                response = requests.get(f"{base_url}{page}", headers=headers)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error fetching page {page}: {e}")
                break

            data = response.json()
            users = data['data']['data']

            try:
                with transaction.atomic():
                    for user in users:
                        firstname = user['firstname']
                        lastname = user['lastname']
                        middlename = user.get('middlename', '')
                        email = user['email']
                        campusphone = user.get('campusphone', 'Not Available')
                        mail_drop = user.get('mail_drop', 'Not Available')
                        role = determine_role(user)
                        emplid = user['emplid']
                        epantherid = user['epantherid']
                        classification = user.get('classification', 'Not Available')
                        school = user.get('school', 'Not Available')
                        year_in_school = user.get('yearinschool', 'Not Available')
                        building_name = user.get('building_name', 'Not Available')
                        room_number = user.get('room_number', 'Not Available')
                        udds = user.get('udds', 'Not Available')
                        appointing_department = user.get('appointing_department', 'Not Available')

                        User.objects.update_or_create(
                            email=email,
                            defaults={
                                'first_name': firstname,
                                'last_name': lastname,
                                'middle_name': middlename,
                                'email': email,
                                'campus_phone': campusphone,
                                'mail_drop': mail_drop,
                                'emplid': emplid,
                                'epantherid': epantherid,
                                'role': role,
                                'title': user.get('title', 'Not Available'),
                                'classification': classification,
                                'affiliation': user.get('affiliation', 'Not Available'),
                                'school': school,
                                'year_in_school': year_in_school,
                                'building_name': building_name,
                                'room_number': room_number,
                                'udds': udds,
                                'appointing_department': appointing_department,
                            }
                        )
                    print(f"Processed page {page} with {len(users)} users")
            except Exception as e:
                print(f"Error processing data for page {page}: {e}")
                break

            page += 1
            if page > data['data']['last_page']:
                break

            time.sleep(4)

        print("User data fetching completed.")
