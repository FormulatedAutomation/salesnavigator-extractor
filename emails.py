from RPA.Dialogs import Dialogs

from dotenv import load_dotenv

from tasks.emails import find_emails

if __name__ == "__main__":
    load_dotenv()
    d = Dialogs()
    d.create_form('questions')
    d.add_file_input(label='CSV File', name='csv_file', element_id='csv_file', filetypes='csv')
    response = d.request_response()
    csv_file = response['csv_file'][0]
    find_emails(csv_file)
