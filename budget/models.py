from django.db import models
from django.utils import timezone   
from django.contrib.auth.models import User

# Create your models here.
class Budget(models.Model):
    ACCOUNT_CHOICES = [
        ("CS", "CASH"),
        ("CD", "CARD"),
        ("SV", "SAVINGS"),
    ]
    CATEGORY_CHOICES =[
        ("FM", "FAMILY"),
        ("BL", "BILLS"),
        ("HM", "HOME")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.CharField(max_length=2, choices=ACCOUNT_CHOICES)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.account} --> {self.category} by {self.user.username}"
    
    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def get_account_display(self):
        return dict(self.ACCOUNT_CHOICES).get(self.account, self.account)