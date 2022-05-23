from django.contrib import admin
from .models import UserProfile, Match, Score, MatchBet, Account, BookMaker, BallToBallScore, OverToOverBet, OverToOverScore, TossBet, Ratio, BookMakerBet, BallToBallBet, BallToBallRatio, OverToOverRatio

models = [UserProfile, Score, MatchBet, Account, BookMaker, BallToBallScore, OverToOverBet, OverToOverScore, TossBet, Ratio, Match, BookMakerBet, BallToBallBet, BallToBallRatio, OverToOverRatio]

for i in models:
    admin.site.register(i)


# class MyAdminSite(admin.AdminSite):
#     site_header = 'CrickBet Admin Page'

# admin_site = MyAdminSite(name='Crickbet')

# admin.site_header = 'CrickBet Admin Page'
admin.autodiscover()
admin.site.enable_nav_sidebar = False


# admin.site.register(UserProfile)
# admin.site.register(Match)
# admin.site.register(MatchBet)
# admin.site.register(Score)
# admin.site.register(Account)
# admin.site.register(Account)
# admin.site.register(Account)
