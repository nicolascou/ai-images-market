from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.is_active) + str(user.pk) + str(timestamp)
        )

email_verification_token = EmailVerificationTokenGenerator()

# Custom validators
def validate_name(name, spa, field):
    if not name:
        raise ValidationError('Please, enter your %s'%spa, params={'bad_field': field},)
    elif len(name) < 2:
        raise ValidationError('Your %s must have a minimum of 2 characters'%spa, params={'bad_field': field})

def validate_password(password, spa, field):
    if not password:
        raise ValidationError('Please, enter a %s'%spa, params={'bad_field': field},)
    elif len(password) < 8:
        raise ValidationError('Your %s must have a minimum of 8 characters'%spa, params={'bad_field': field},)
    elif not password.isalnum():
        raise ValidationError('Your %s must have at least one letter and one number'%spa, params={'bad_field': field},)
        
