from RPA.Dialogs import Dialogs

from tasks.salesnavigator import extract_leads
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    d = Dialogs()
    d.create_form('questions')
    d.add_text_input(label='Saved Search URL', name='saved_search_url')
    response = d.request_response()
    saved_search_url = response['saved_search_url']
    extract_leads(saved_search_url)
