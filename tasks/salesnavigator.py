import csv

from RPA.Robocloud.Secrets import Secrets
from playwright import sync_playwright

next_button_selector = '.search-results__pagination-next-button'
disabled_next_button_selector = '.search-results__pagination-next-button:disabled'
sales_navigator_login_url = 'https://www.linkedin.com/uas/login?fromSignIn=true&trk=navigator&session_redirect=/sales2/loginRedirect.html'


def scrape_page(page):
    data = []
    people = page.querySelectorAll('section#results .search-results__result-item')
    for person in people:
        try:
            name = person.querySelectorAll('.result-lockup__name')[0].innerText()
            try:
                split_name = name.split(' ')
                first_name = split_name[0]
                last_name = split_name[1]
            except IndexError:
                first_name = name
                last_name = ''
            profile_url = person.querySelectorAll('.result-lockup__name a')[0].getAttribute('href')
            company = person.querySelectorAll('.result-lockup__position-company')[0].innerText()
            company_link = person.querySelectorAll('.result-lockup__position-company a')[0].getAttribute('href')
            data.append({
                'first_name': first_name,
                'last_name': last_name,
                'profile_url': profile_url,
                'company': company,
                'link': company_link,
                'location': '',
                'urn': ''
            })
        except IndexError:
            pass
    return data


def has_next_button(page):
    return page.querySelectorAll(next_button_selector).__len__() > 0 and \
           page.querySelectorAll(disabled_next_button_selector).__len__() == 0


def process_json(json_data):
    data = []
    for person in json_data['elements']:
        try:
            company = person['currentPositions'][0]
        except (KeyError, IndexError):
            company = {'companyName': None}

        try:
            urn = company['companyUrnResolutionResult']
        except KeyError:
            urn = {'location': None, 'entityUrn': None}

        try:
            location = urn['location']
        except KeyError:
            location = None

        data.append({
            'first_name': person['firstName'],
            'last_name': person['lastName'],
            'company': company['companyName'],
            'job_title': company['title'],
            'location': location
        })
    return data


def login(page):
    page.goto(sales_navigator_login_url)
    page.waitForLoadState('load')
    secrets = Secrets()
    USER_NAME = secrets.get_secret("credentials")["LINKEDIN_EMAIL"]
    PASSWORD = secrets.get_secret("credentials")["LINKEDIN_PASSWORD"]
    page.fill('input#username', USER_NAME)
    page.fill('input#password', PASSWORD)
    page.click('button[type=submit]')


def crawl_page(page, generated_data):
    page.click('.search-results__pagination-next-button')
    new_response = page.waitForResponse('**people**')
    json_response = new_response.json()
    new_data = process_json(json_response)
    appended_data = generated_data + new_data
    print(f"Appending {new_data.__len__()} leads, {appended_data.__len__()} total")
    return appended_data


def output_csv(generated_data):
    with open('output/search_results.csv', mode='w') as writer:
        employee_writer = csv.writer(writer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(
            ['email', 'firstname', 'lastname', 'jobtitle', 'employeecompany', 'country', 'appleidfa', 'googleaid'])
        for row in generated_data:
            employee_writer.writerow([
                '',
                row['first_name'],
                row['last_name'],
                row['job_title'],
                row['company'],
                row['location'],
                '',
                ''
            ])


def extract_leads(search_url):
    with sync_playwright() as p:
        generated_data = []
        browser = p.webkit.launch(headless=False)
        context = browser.newContext()
        page = context.newPage()
        login(page)
        page.goto(search_url)
        page.click('.search-results__pagination-next-button')
        page.waitForResponse('**people**')
        page.click('.search-results__pagination-previous-button')
        first_response = page.waitForResponse('**people**')
        json_response = first_response.json()
        generated_data = generated_data + process_json(json_response)
        while has_next_button(page):
            generated_data = crawl_page(page, generated_data)
        output_csv(generated_data)
