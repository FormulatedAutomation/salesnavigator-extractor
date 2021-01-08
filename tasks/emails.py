import csv
import os

from pyhunter import PyHunter
from requests import HTTPError

CONFIDENCE_THRESHOLD = 70

def get_email(row):
    hunter = PyHunter(os.environ.get('HUNTER_API_KEY'))
    suggested_email = None
    confidence_score = None
    try:
        suggested_email, confidence_score = hunter.email_finder(company=row['employeecompany'], first_name=row['firstname'], last_name=row['lastname'])
    except HTTPError:
        pass
    if confidence_score is not None and confidence_score > CONFIDENCE_THRESHOLD:
        return suggested_email
    else:
        return None


def find_emails(csv_file):
    with open(csv_file, mode='r') as csvfile:
        leads = csv.DictReader(csvfile)
        with open('output/emails.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                ['email', 'firstname', 'lastname', 'jobtitle', 'employeecompany', 'country', 'appleidfa', 'googleaid'])
            for row in leads:
                email = row['email']
                if email == '' and row['lastname'].__len__() > 1:
                    found_email = get_email(row)
                    print(f"Looking for {found_email}")
                    try:
                        if found_email is not None:
                            print(found_email)
                            writer.writerow([
                                found_email,
                                row['firstname'],
                                row['lastname'],
                                row['jobtitle'],
                                row['employeecompany'],
                                row['country'],
                                '',
                                ''
                            ])
                    except TypeError:
                        pass
                else:
                    writer.writerow([
                        row['email'],
                        row['firstname'],
                        row['lastname'],
                        row['jobtitle'],
                        row['employeecompany'],
                        row['country'],
                        '',
                        ''
                    ])