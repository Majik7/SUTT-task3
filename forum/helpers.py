from django.core.mail import send_mail
from django.conf import settings
import threading

def send_reply_notification(post, reply):
    def start_mail():
        try:
            subject = f"New reply on your post: {post.title}"
            message = f"Hi {post.author.first_name},\n\n{reply.author} just replied to your post:\n\n'{reply.content[:100]}...'\n"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [post.author.email]

            # print(f"{post.title}")
            
            send_mail(subject, message, from_email, recipient_list)
            print("SUCCESS YIPPEEE")

        except Exception as e:
            print(f"Email Exception - {e}")

    threading.Thread(target=start_mail).start()