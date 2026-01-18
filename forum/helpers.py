from django.core.mail import send_mail
from django.conf import settings
import threading
import logging
logger = logging.getLogger(__name__)

def send_reply_notification(post, reply):
    logger.error(f"About to send email to {post.author.email}")
    try:
        subject = f"New reply on your post: {post.title}"
        recipient = post.author.email

        if not recipient:
            return

        send_mail(
            subject, 
            reply.content,
            settings.EMAIL_HOST_USER, 
            [recipient], 
            fail_silently=False
        )
        logger.error("Email sent successfully")
    except Exception as e:
        logger.error(f"Email failed: {e}")