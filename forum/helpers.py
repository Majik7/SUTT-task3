from django.core.mail import send_mail
from django.conf import settings
import threading

def send_reply_notification(post, reply):
    print("DEBUG: send_reply_notification function TRIGGERED")
    try:
        subject = f"New reply on your post: {post.title}"
        recipient = post.author.email
        print(f"DEBUG: Attempting to send to {recipient}")

        if not recipient:
            print("DEBUG: ABORTING - Recipient email is empty!")
            return

        send_mail(
            subject, 
            "Test message content", 
            settings.EMAIL_HOST_USER, 
            [recipient], 
            fail_silently=False
        )
        print("DEBUG: send_mail command EXECUTED")
    except Exception as e:
        print(f"DEBUG: Email Exception - {e}")