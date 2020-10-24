from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Member(models.Model):
    REGULAR = "regular"
    ADMIN = "admin"
    MALE = "male"
    FEMALE = "female"
    MEMBER_TYPES = [
        (REGULAR, _("Regular Member")),
        (ADMIN, _("Admin Member")) 
    ]
    GENDER_TYPES = [
        (MALE, _("Male")),
        (FEMALE, _("Female"))
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    types =  models.CharField(
        max_length=8, 
        choices=MEMBER_TYPES, 
        default=REGULAR
    )
    birth_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    birth_place = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=8,
        choices=GENDER_TYPES
    )

class Post(models.Model):
    writer = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
