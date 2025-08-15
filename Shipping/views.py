from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
import imaplib
import email
from django.http import HttpResponse
from email.header import decode_header
from .models import EmailModel  
from imap_tools import MailBox
import imapclient
from django.utils import timezone
from email.utils import parsedate_to_datetime
from imapclient import IMAPClient
# Create your views here.

def send_email(request):
    if request.method == 'GET':
        data = request.GET
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Define the recipient email address(es) as a list
        recipient_list = ['hayahamada10311@gmail.com']  

        # Send an email using Django's send_mail function
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'acroifcn@across-mena.com',
            recipient_list, 
            fail_silently=False,
        )

        send_mail(
            'نشكركم على التواصل معنا سيتم التواصل معكم من قبل الفريق المختص',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'acroifcn@across-mena.com',
            [email],  # Use the sender's email as the recipient
            fail_silently=False,
        )

        return JsonResponse({'message': 'Email sent successfully'})
    
    return JsonResponse({'message': 'Invalid request method'}, status=405)


 
def fetch_emails(request):
    # Replace with your email server details
    imap_server = 'across-mena.com'
    email_address = 'test@across-mena.com'
    email_password = ',^-hHb*.s@1(' 

   
    try:
        with IMAPClient(imap_server, ssl=False) as client:
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

        response_text = "Emails fetched and saved successfully."
        return HttpResponse(response_text)

    except Exception as e:
        response_text = f"An error occurred: {str(e)}"
        return HttpResponse(response_text, status=500)
