from django.core.mail import send_mail
from django.conf import settings
import random

# Manually configure Django settings
settings.configure(
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    EMAIL_HOST='smtp.gmail.com',  # Replace with your actual SMTP host
    EMAIL_PORT=587,  # Replace with your SMTP port
    EMAIL_USE_TLS=True,
    EMAIL_HOST_USER="lolov853@gmail.com", 
    EMAIL_HOST_PASSWORD="vzhi iyva oapd jjfu"
)

# Sending email
email = "anushervon4j@gmail.com"
send_mail(
    "Your Verification Code",
    f"Your verification code is {random.randint(10, 100)}.",
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)
