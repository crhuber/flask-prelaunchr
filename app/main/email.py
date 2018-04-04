from flask import current_app, render_template
import boto3

def send_email(email, ref_code):
    ses = boto3.client(
        'ses',
        region_name=current_app.config['SES_REGION_NAME'],
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )
    subject = "Welcome"
    sender = current_app.config['SES_EMAIL_SOURCE']
    body_html = render_template('email/signup_email.html', ref_code=ref_code)
    response = ses.send_email(
                        Source=sender,
                        Destination={'ToAddresses': [email]},
                        Message={
                            'Subject': {'Data': subject},
                            'Body': {
                                'Html': {'Data': body_html},
                            }
                        }
                )
    print response['ResponseMetadata']