from django.core.mail import send_mail
from django.conf import settings

def send_reply_notification(post, reply):
    subject = f"New reply on your post: {post.title}"
    message = f"Hi {post.author.first_name},\n\n{reply.author} just replied to your post:\n\n'{reply.content[:100]}...'\n"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [post.author.email]

    print(f"{post.title}")
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)