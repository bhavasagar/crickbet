from rest_framework import serializers, exceptions
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.encoding import force_text, force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import Account, BallToBallRatio, BookMaker, Match, OverToOverRatio, UserProfile, Score, MatchBet, TossBet, OverToOverBet, BookMakerBet, BallToBallBet, Recharge


class LoginSerializer(serializers.ModelSerializer):
    """
    Fields: 
    `email`, `password` [Write Only]
    `access_token`, `refresh_token` [Read Only]

    Model: User
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)   

    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token']    
    
    def validate(self, attrs):
        """
        This method validates and sends the tokens with `email` and `password`
        """
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        # print(email, password)
        if not (email and password):
            raise exceptions.ValidationError(_('Must Include Password and Email'))
        try:
            user = User.objects.get(email=email)        
        except User.DoesNotExist:
            raise exceptions.NotFound(_("Email doesn't exist in database"))
        if not user:
            raise exceptions.ValidationError(_('Invalid Credetials'))
        IsCorrectPassword = user.check_password(password)
        if not user.is_active:
            raise exceptions.ValidationError(_('Your account is in active, please contact customer support.'))
        if not IsCorrectPassword:
            raise exceptions.ValidationError(_('Wrong Password.'))
        # print(user)
        userprofile = UserProfile.objects.get(user__username=user)
        tokens = userprofile.tokens       
        return {
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token']
            }   

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')
        if not email:
            raise exceptions.ValidationError(_("Email is required."))
        try:
            user = User.objects.get(email=email)        
        except User.DoesNotExist:
            raise exceptions.NotFound(_("Email doesn't exist in database"))
                
        reset_password_link = settings.UI_WEBSITE_URL + urlsafe_base64_encode(force_bytes(user.id)) + '/' + default_token_generator.make_token(user) 
        print(reset_password_link, user)
        sub = 'CrickBet Password Rest Link'
        message = f"""
        Hello {user.username}, 
        Here is your reset password link, {reset_password_link} !
        """  
        print(message, settings.EMAIL_HOST_USER)      
        try: 
            send_mail(sub, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])
        except:
            raise exceptions.ErrorDetail(_("Unable to send Email, Please contact customer support."))

        return {
            "message": "Reset password link is sent to your email."
        }


class ResetPasswordSerializer(serializers.Serializer):    
    password1 = serializers.CharField(max_length=60, min_length=8, required=True, write_only=True)
    password2 = serializers.CharField(max_length=60, min_length=8, required=True, write_only=True)
    uid = serializers.CharField(max_length=60, min_length=1, required=True, write_only=True)
    token = serializers.CharField(max_length=100, min_length=8, required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['password1', 'password2', 'uid', 'token']

    def validate(self, attrs, *args, **kwargs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if not (password1 and password2):
            raise AssertionError('Please fill the Password and Confirm Password.')
        
        if password1 != password2:
            raise AssertionError('Password and Confirm Password are not same')
                
        print(attrs, self.context.get('data'))
        token = self.context.get('data')['token']
        uid = force_text(urlsafe_base64_decode(self.context.get('data')['uid']))

        try:
            user = User.objects.get(pk=uid)        
        except User.DoesNotExist:
            raise exceptions.NotFound(_("Email doesn't exist in database"))
        
        if not default_token_generator.check_token(user, token):
            raise exceptions.NotAcceptable(_('Invalid Token'))
        

        self.user = user
        self.password = password1

        return attrs

    def create(self, validated_data):
        self.user.set_password(self.password)
        self.user.save()
        print('Password saved', self.password) 
        return {
            "message": "password saved"
        }


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=60, min_length=8, required=True, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not (username and password and email):
            raise exceptions.ValidationError(_("Please fill all the fields"))

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():       
            raise exceptions.NotAcceptable(_("User already exists"))

        return attrs


    def send_verification_email(self, user):
        email_verification_link = "http://localhost:8000" + reverse('email_verification', kwargs={'uid': urlsafe_base64_encode(force_bytes(user.id)), 'token': default_token_generator.make_token(user)})
        sub = 'CrickBet Email Verification Link'
        message = f"""
        Hello {user.username}, 
        Here is your Email verification link, {email_verification_link} !
        """  
        print(message, settings.EMAIL_HOST_USER)      
        try: 
            send_mail(sub, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])
        except:
            raise exceptions.ErrorDetail(_("Unable to send Email, Please contact customer support."))

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(**validated_data)
        self.send_verification_email(user)
        return user
    
class UserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)    
    password = serializers.CharField(min_length=8, max_length=60, required=False, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not (username or password or email):
            raise exceptions.ValidationError(_("Please fill any one the field."))        

        return attrs
    
    def create(self, validated_data):
        user = self.context.get('request').user        
        print(validated_data)
        if validated_data.get('email'):
            user.email = validated_data.get('email')
        if validated_data.get('username'):
            user.username = validated_data.get('username')
        if validated_data.get('password'):
            user.set_password(validated_data.get('password'))
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        depth = 2

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"        

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"
        depth = 1

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = "__all__"

class OverToOverRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverToOverRatio
        fields = "__all__"

class BallToBallRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallToBallRatio
        fields = "__all__"

class MatchBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchBet
        fields = "__all__"

class BallToBallBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallToBallBet
        fields = "__all__"

class TossBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TossBet
        fields = "__all__"

class OverToOverBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverToOverBet
        fields = "__all__"

class BookMakerBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMakerBet
        fields = "__all__"

class BookMakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMaker
        fields = "__all__"

class RechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recharge
        fields = "__all__"