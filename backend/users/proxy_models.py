from users.models import User

class ManualQuoteUser(User):

    class Meta:
        proxy=True