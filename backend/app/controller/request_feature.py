from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class EmailSchema(BaseModel):
    email: EmailStr = "himanshujar870@gmail.com"  # Receiver's email (default value)
    subject: str = "AI-sandbox feedback"  # Default subject
    message: str  # Required field

def send_email(email: str, subject: str, message: str):
    
    sender_email = os.getenv('SENDER_EMAIL')  
    sender_password = os.getenv('GMAIL_APP_KEY')  
    smtp_server = os.getenv('SMTP_SERVER')  
    smtp_port = os.getenv('SMTP_PORT') 
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email  # Receiver's email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        logger.info(f"Email sent to {email} with subject '{subject}'")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/send-email/")
# async def send_email_endpoint(email_data: EmailSchema):
#     logger.info(f"Received request to send email to {email_data.email}")
#     send_email(email_data.email, email_data.subject, email_data.message)
#     return {"message": "Email has been sent successfully"}

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)