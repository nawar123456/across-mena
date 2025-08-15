import imapclient
import email
from django.utils.dateparse import parsedate_to_datetime
from your_django_project.your_app.models import EmailModel  # Replace with your actual project and app names

# Replace with your email server details
imap_server = 'across-mena.com'
email_address = 'test@across-mena.com'
email_password = ',^-hHb*.s@1(' 

def fetch_and_save_emails():
    try:
        with imapclient.IMAPClient(imap_server, ssl=False) as client:
            client.login(email_address, email_password)

            # Select the mailbox you want to fetch emails from (e.g., INBOX)
            client.select_folder('INBOX.Sent')

            # Search for emails and fetch them
            messages = client.search(['ALL'])

            # Process the emails here
            for msg_id, data in client.fetch(messages, ['BODY[]']).items():
                msg = email.message_from_bytes(data[b'BODY[]'])

                # Extract relevant data from the email message
                subject = msg.get('Subject', 'No Subject')
                sender = msg.get('From', 'No Sender')
                date_str = msg.get('Date', None)
                date = parsedate_to_datetime(date_str) if date_str else None
                body = ''
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()

                # Check if the email already exists in the database
                existing_email = EmailModel.objects.filter(
                    subject=subject,
                    sender=sender,
                    date=date,
                ).first()

                if not existing_email:
                    # Create a new instance of EmailModel and save it
                    email_instance = EmailModel(
                        subject=subject,
                        sender=sender,
                        date=date,
                        body=body
                    )
                    email_instance.save()

        print("Emails fetched and saved successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    fetch_and_save_emails()
