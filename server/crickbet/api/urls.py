from django.urls import path    
from .views import CurrentMatchesAPI, LoginView, ResetPasswordView, ForgotPasswordView, UserRegisterView, UserUpdateView, EmailVerificationView, TossBetAPI, TossBetCreateAPI, MatchBetAPI, MatchBetCreateAPI, OverToOverBetAPI, OverToOverBetCreateAPI, BallToBallBetCreateAPI, BookMakerBetCreateAPI, BallToBallBetAPI, BookMakerBetAPI, start_payment, handle_payment, UserDetailsAPI, MatcheDetailAPI, get_user_pending_balance, page_details

bet_api = []

BET_VIEWS = [TossBetAPI, MatchBetAPI, OverToOverBetAPI, BallToBallBetAPI, BookMakerBetAPI]
BET_CREATE_VIEWS = [ TossBetCreateAPI, MatchBetCreateAPI, OverToOverBetCreateAPI, BallToBallBetCreateAPI, BookMakerBetCreateAPI]

for createview,view in zip(BET_CREATE_VIEWS, BET_VIEWS):    
    bet_api.append(path(f'{view.__name__[:-3].lower()}/', createview.as_view(), name=f'{view.__name__[:-3].lower()}_create'))
    bet_api.append(path(f'{view.__name__[:-3].lower()}/<int:pk>/', view.as_view(), name=f'{view.__name__[:-3].lower()}_retrive_delete'))

urlpatterns = [
    # API endpoints related to user.
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('update-user/', UserUpdateView.as_view(), name='update'),
    path('verify-email/<uid>/<token>/', EmailVerificationView.as_view(), name='email_verification'),
    path('user-details/', UserDetailsAPI.as_view(), name='user_details'),    
    
    path('page-details/', page_details, name='page_details'),    

    # API endpoints related to matches
    path('current-matches/', CurrentMatchesAPI.as_view(), name='current_matches'),    
    path('match/<int:match_id>/', MatcheDetailAPI.as_view(), name='match_detail'),    

    # API endpoints related to payments
    path('recharge/', start_payment, name="start_payment"),
    path('handle-recharge/', handle_payment, name="handle_payment"),
    # path('pending-balance/', get_user_pending_balance, name="pending_balance"),
] + bet_api

