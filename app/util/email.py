from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app import sg


def add_contact_to_list(form_data):
    """
    Add contact to SendGrid list to trigger automation
    """
    try:
        # Add contact with list assignment in one step
        data = {
            "contacts": [
                {
                    "email": form_data.get('email'),
                    "first_name": form_data.get('firstName'),
                    "last_name": form_data.get('lastName'),
                    "phone": form_data.get('phone', ''),
                }
            ],
            "list_ids": ["20e7967c-eecf-4ef9-8716-9d871c494bb7"]  # Notice this is list_ids, not list_id
        }

        response = sg.client.marketing.contacts.put(request_body=data)
        
        if response.status_code >= 200 and response.status_code < 300:
            current_app.logger.info(f'Contact added to list successfully: {form_data.get("email")}')
            return True
        else:
            raise Exception(f"Failed to add contact to list: {response.status_code}")

    except Exception as e:
        current_app.logger.error(f'Failed to add contact to list: {str(e)}')
        return False

def send_contact_form_email(form_data):
    """
    Process new contact form submission
    """
    try:
        if sg is None:
            raise Exception("SendGrid client not initialized")

        # First, add to list to trigger automation
        if not add_contact_to_list(form_data):
            raise Exception("Failed to add contact to list")

        # Then send notification email to you
        notification = Mail(
            from_email=Email(
                'kira@kirajiaevents.com',
                'Kira Jia Weddings'
            ),
            to_emails='kira@kirajiaevents.com',
            subject=f'New Wedding Inquiry from {form_data.get("firstName")} {form_data.get("lastName")}',
            plain_text_content=Content(
                'text/plain',
                f"""
                New Wedding Inquiry

                Name: {form_data.get('firstName', '')} {form_data.get('lastName', '')}
                Email: {form_data.get('email', '')}
                Phone: {form_data.get('phone', 'Not provided')}
                Wedding Date: {form_data.get('weddingDate', 'Not specified')}
                
                Vision:
                {form_data.get('vision', '')}
                
                To respond, simply reply to {form_data.get('email', '')}
                """
            )
        )

        # Send notification to you
        response = sg.send(notification)
        return response.status_code >= 200 and response.status_code < 300

    except Exception as e:
        current_app.logger.error(f'Failed to process contact form: {str(e)}')
        return False