from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.forms import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta

from .helpers import get_ball_num

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    userphoto = models.ImageField(upload_to='images/', null=True,blank=True)
    phone_number = models.CharField(default=False, max_length=30)

    def __str__(self):
        return self.user.username
    
    @property
    def tokens(self):
        tokens = RefreshToken.for_user(self.user)
        return {            
            'refresh_token': str(tokens),
            'access_token': str(tokens.access_token)
        }

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    bonus_amount = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} - Rs.{self.total_balance}"
    
    @property
    def total_balance(self):
        return self.bonus_amount + self.balance

class Ratio(models.Model):
    ratio_a = models.FloatField(default=2)
    ratio_b = models.FloatField(default=2)    
    blocked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.id}-{self.ratio_a}:{self.ratio_b}/{self.blocked}"

class Match(models.Model):
    match_name = models.CharField(max_length=300)
    team_a = models.CharField(max_length=300)
    team_b = models.CharField(max_length=300)
    batting_team = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=300)
    match_type = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateTimeField()
    match_winning_team = models.CharField(max_length=300, null=True, blank=True)
    toss_winning_team = models.CharField(max_length=300, null=True, blank=True)
    gold = models.ForeignKey(Ratio, on_delete=models.CASCADE, related_name='gold_ratio', null=True, blank=True)
    diamond = models.ForeignKey(Ratio, on_delete=models.CASCADE, related_name='diamond_ratio', null=True, blank=True)    
    tossbet_ratio = models.ForeignKey(Ratio, on_delete=models.CASCADE, related_name='toss_ratio', null=True, blank=True)            
    match_id = models.CharField(max_length=300) 
    team_a_image = models.URLField()         
    team_b_image = models.URLField()  
    ongoing = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    not_required = models.BooleanField(default=False)    
 
    def __str__(self) -> str:
        return f"{self.match_name}"

    # def save(self, *args, **kwargs):
    #     if self.status == 'completed':
    #         self.gold.blocked = True
    #         self.gold.save()
    #         self.diamond.blocked = True
    #         self.diamond.save()
    #     return super().save(*args, **kwargs)

    @property
    def current_over(self):                
        score = Score.objects.filter(match=self).order_by('-updated_at').first()
        if score:
            return score.overs
        return None
    
    @property
    def current_ball(self):                
        score = Score.objects.filter(match=self).order_by('-updated_at').first()
        if score:
            return get_ball_num(score.overs)
        return None
    
    @property
    def batting_team(self):                
        score = Score.objects.filter(match=self).order_by('-updated_at').first()
        if score:
            return score.team
        return None

import random

class RatioModel(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    ratio = models.ForeignKey(Ratio, on_delete=models.CASCADE)
    expected_runs = models.IntegerField(default='')
    expected_wickets = models.IntegerField(default=0)
    team = models.CharField(default='', max_length=50)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if self.expected_runs == '':
            self.expected_runs = str(random.randint(7,9))
        return super().save(*args, **kwargs)

class OverToOverRatio(RatioModel):
    over_num = models.FloatField()

    def __str__(self) -> str:
        return f"{self.match.match_name} - {self.over_num}"

class BallToBallRatio(RatioModel):
    ball_num = models.FloatField()

    def __str__(self) -> str:
        return f"{self.match.match_name} - {self.ball_num}"
    
    @property
    def integral_ball_num(self):        
        return get_ball_num(self.ball_num)

class Score(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(default='', max_length=100)
    day = models.IntegerField(default=1)
    runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    overs = models.FloatField(default=0)     
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.match.match_name} - {self.team}"   
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

class OverToOverScore(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.CharField(default='', max_length=100)
    over_num = models.IntegerField(default=-1)
    runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.match.match_name} - {self.over_num}"

class BallToBallScore(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    innings_no = models.IntegerField(default=0)
    ball_no = models.IntegerField(default=1)
    runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.match.match_name} - {self.ball_no}"  

    @property
    def is_dot(self):
        if self.runs == 0 and self.wickets == 0:
            return True
        return False

class BookMaker(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    question = models.CharField(max_length=300, default="Who wins this Match?")
    answer = models.CharField(max_length=300, default="Yes")
    otheroption = models.CharField(max_length=300, default="No")
    ratio = models.ForeignKey(Ratio, on_delete=models.CASCADE)
    blocked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.match.match_name} - {self.question[:10]}..."

RESULT_CATEGORY_CHOICES = (
    ('W', 'Win'),
    ('L', 'Lose'),
)

class Bet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.SET_NULL, blank=True, null=True)
    amount_invested = models.FloatField(default=0)
    invested_on = models.CharField(max_length=50)    
    result = models.CharField(choices=RESULT_CATEGORY_CHOICES, max_length=5, null=True, blank=True)    
    paid = models.BooleanField(default=False)
    paid_on = models.DateTimeField(blank=True, null=True)
    made_on = models.DateTimeField(auto_now_add=True)  
    deducted = models.BooleanField(default=False)
    actual_result = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True        

    def save(self, *args, **kwargs):
        if not self.deducted:            
            account = self.user.account
            balance = account.balance
            if balance < self.amount_invested:
                raise ValidationError(_("Insufficient Balance"))
            account.balance = float(account.balance) - float(self.amount_invested)
            account.save()
            self.deducted = True

        if self.paid and ((self.paid_on == None) or (not self.paid_on)):
            self.paid_on = datetime.now()
        return super().save(*args, **kwargs)

class MatchBet(Bet):
    ratio_invested = models.FloatField()

    def __str__(self) -> str:
        return f"{self.user.username} - MatchBet - Rs.{self.amount_invested}"        

class OverToOverBet(Bet):    
    over_num = models.FloatField() 
    team = models.CharField(max_length=50)
    ratio_invested = models.FloatField()

    def __str__(self) -> str:
        return f"{self.user.username} - OverBet - Rs.{self.amount_invested}"      

class BallToBallBet(Bet):    
    ball_num = models.FloatField() 
    team = models.CharField(max_length=50)
    ratio_invested = models.FloatField()

    def __str__(self) -> str:
        return f"{self.user.username} - Ball2Ball - Rs.{self.amount_invested}"      
    
    def save(self, *args, **kwargs):
        self.ball_num = get_ball_num(self.ball_num)
        return super().save(*args, **kwargs)

class BookMakerBet(Bet):
    bookmaker_id = models.CharField(max_length=10)
    ratio_invested = models.FloatField()

    def __str__(self) -> str:
        return f"{self.user.username} - BookMakerBet - Rs.{self.amount_invested}"  

class TossBet(Bet):    
    ratio_invested = models.FloatField()
    
    def __str__(self) -> str:
        return f"{self.user.username} - TossBet - Rs.{self.amount_invested}"  

class WithDrawRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.CharField(default=False, max_length=15)
    upi_id = models.CharField(default=False, max_length=35)
    paid = models.BooleanField(default=False)  
    made_on = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'{self.amount} - {self.upi_id}'


class Recharge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField()
    mode = models.CharField(max_length=10)
    made_on = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Recharge - {self.user.username} - Rs.{self.amount}"

class PageData(models.Model):
    heading = models.CharField(max_length=100)
    scroll_text = models.CharField(max_length=500)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)        
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)
        account = Account.objects.create(user=instance)

@receiver(post_save, sender=OverToOverRatio)        
def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        for ball_num in range(int(instance.over_num)*10+1, int(instance.over_num)*10 + 7):
            ball_num = float(ball_num/10)   
            ratio = Ratio.objects.create(ratio_a=10,ratio_b=13)
            if not BallToBallRatio.objects.filter(match=instance.match, ball_num=ball_num).exists():
                BallToBallRatio.objects.create(match=instance.match, ratio=ratio, ball_num=ball_num, team=instance.team, expected_runs = str(random.randint(0,5)))
        