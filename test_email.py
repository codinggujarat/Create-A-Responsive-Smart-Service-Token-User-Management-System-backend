import os
from flask import Flask
from flask_mail import Mail, Message

# Test email configuration
def test_email():
    app = Flask(__name__)
    
    # Configure mail settings
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@servicetoken.com')
    
    print("Mail Configuration:")
    print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
    print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
    print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
    print(f"MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")
    
    # Check if credentials are set
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("WARNING: MAIL_USERNAME or MAIL_PASSWORD not set. Email sending will fail.")
        return
    
    mail = Mail(app)
    
    try:
        with app.app_context():
            msg = Message(
                subject="Test Email",
                recipients=["test@example.com"],
                body="This is a test email."
            )
            mail.send(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    test_email()