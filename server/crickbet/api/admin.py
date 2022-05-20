from django.contrib import admin
from .models import UserProfile, Match, Score, MatchBet, Account, BookMaker, BallToBallScore, OverToOverBet, OverToOverScore, TossBet, Ratio, BookMakerBet, BallToBallBet, BallToBallRatio, OverToOverRatio

models = [UserProfile, Score, MatchBet, Account, BookMaker, BallToBallScore, OverToOverBet, OverToOverScore, TossBet, Ratio, Match, BookMakerBet, BallToBallBet, BallToBallRatio, OverToOverRatio]

for i in models:
    admin.site.register(i)


# admin.site.register(UserProfile)
# admin.site.register(Match)
# admin.site.register(MatchBet)
# admin.site.register(Score)
# admin.site.register(Account)
# admin.site.register(Account)
# admin.site.register(Account)
