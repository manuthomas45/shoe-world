# your_app/pipeline.py

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    if backend.name == 'google-oauth2':
        email = details.get('email')
        first_name = details.get('first_name')
        last_name = details.get('last_name')

        if not email:
            return

        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,  # Set is_active to True
            date_joined=timezone.now(),
        )
        user.set_unusable_password()  # Since the user is logging in via Google, they won't need a local password
        user.save()
        return {'is_new': True, 'user': user}
