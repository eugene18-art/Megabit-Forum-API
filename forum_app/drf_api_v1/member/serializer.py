import re
from django.core.exceptions import ValidationError
from rest_framework import serializers
from forum_app.models import Member
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class CreateMemberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", max_length=150)
    last_name = serializers.CharField(source="user.last_name", max_length=150)
    email = serializers.CharField(source="user.email", max_length=75)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
            'types', 
            'birth_date', 
            'birth_place', 
            'gender'
    ]

    def validate_confirm_password(self, value):
        data = self.get_initial()
        password = data.get("password")
        confirm_password = value
        if (confirm_password != password):
            raise ValidationError(_("Your password didn't match."))
        # if not (re.match(r"(?=.*\d.*)(?=.*[A-Z].*)(?=.*[a-z].*)(?=.*[`~!@#$%^&*()\-_=+{}\[\]|\\:;'\"<>?,./].*).{8,}", password)):
        #     raise ValidationError("Password must contains at least 1 symbol, 1 capital character, 1 non capital character, and must have minimum 8 length.")
        return value

    def validate_email(self, value):
        request = self.context.get('request')
        rfc5322 = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        if not (re.match(rfc5322, value)):
            raise ValidationError(_("Email is not valid."))
        new_email_exists = User.objects.filter(email=value).exists()
        if (request.method == "PUT"):
            username = self.context.get('username')
            current_email = User.objects.get(username=username).email
            if (current_email != value) and new_email_exists:
                raise ValidationError(_("Someone already use this email. Is this your email?."))
            return value
        if new_email_exists:
            raise ValidationError(_("User with this email already exists."))
        return value

class ReadMemberSerializer(serializers.ModelSerializer):
    first_name= serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'email',
            'types', 
            'birth_date', 
            'birth_place', 
            'gender'
    ]

    def get_first_name(self, obj):
        return obj.user.first_name
    def get_last_name(self, obj):
        return obj.user.last_name
    def get_email(self, obj):
        return obj.user.email

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(max_length=75, required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
        ]
    def validate(self, data):
        email = data.get("email", None)
        username = data.get("username", None)
        password = data["password"]

        if (not email) and (not username):
            raise ValidationError({"email":_("Please provide either email or username!"), "username":_("Please provide either email or username!")})
        if email:
            rfc5322 = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
            if not (re.match(rfc5322, email)):
                raise ValidationError({"email":_("Email is not valid.")})
        return data

def generate_username(first_name,last_name):
    val = "{0}{1}".format(first_name,last_name).lower().replace(" ", "")
    if User.objects.filter(username=val).count() == 0:
        return val
    qs = User.objects.filter(username__regex=rf"^{val}\d+").order_by("-username")
    counters = [int(re.search(r"\d+$", str(x)).group(0)) for x in qs]
    if len(counters) == 0:
        return f"{val}{0}"
    counters.sort()
    max_counter = counters.pop()
    max_counter+=1
    val = f"{val}{max_counter}"
    return val