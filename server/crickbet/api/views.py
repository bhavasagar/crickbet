from django.http import JsonResponse
from django.shortcuts import render
from django.conf import Settings, settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text, force_bytes

from rest_framework import exceptions, status, generics, authentication, permissions
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from .models import Account, BallToBallRatio, Bet, Match, OverToOverRatio, PageData, Score, TossBet, OverToOverBet, MatchBet, BookMakerBet, BallToBallBet, Recharge, UserProfile
from .serializers import AccountSerializer, BallToBallRatioSerializer, BookMakerSerializer, ForgotPasswordSerializer, LoginSerializer, OverToOverRatioSerializer, ResetPasswordSerializer, UserProfileSerializer, UserRegisterSerializer, UserUpdateSerializer, MatchSerializer, BallToBallBetSerializer, OverToOverBetSerializer, TossBetSerializer, BookMakerBetSerializer, MatchBetSerializer, RechargeSerializer, ScoreSerializer, PageDataSerializer
from . import paytm

class LoginView(GenericAPIView):
    """
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer  
    queryset = User.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ResetPasswordView(GenericAPIView):
    """
    """
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.none()

    def patch(self, request, uid, token, *args, **kwargs):        
        data = {"uid":uid, "token":token, 'password1': request.data.get('password1'), 'password2': request.data.get('password2')}
        serializer = self.serializer_class(data=data, context={'data': data})
        serializer.is_valid(raise_exception=True)       
        serializer.save()         

        return Response({"message": "Password is updated successfully"}, status=status.HTTP_200_OK)

class ForgotPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer
    queryset = User.objects.none()

    def post(self, request, *args, **kwargs):
        data = request.data 
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRegisterView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer
    queryset = User.objects.none()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EmailVerificationView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserUpdateSerializer
    queryset = User.objects.none()

    def get(self, request, uid, token, *args, **kwargs):
        if not (uid or token):
            raise exceptions.ValidationError(_("Invalid Verification URL. Please check the mail."))
        token = self.context.get('data')['token']
        uid = force_text(urlsafe_base64_decode(self.context.get('data')['uid']))

        try:
            user = User.objects.get(pk=uid)        
        except User.DoesNotExist:
            raise exceptions.NotFound(_("Email doesn't exist in database"))
        
        if not default_token_generator.check_token(user, token):
            raise exceptions.NotAcceptable(_('Invalid Token'))

        user.is_active = True
        user.save()
        
        return Response({"message": "Email successfully verified."})

class UserUpdateView(GenericAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer
    queryset = User.objects.none()

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class TossBetCreateAPI(CreateAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = TossBetSerializer
    queryset = TossBet.objects.all()    

class TossBetAPI(RetrieveDestroyAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = TossBetSerializer
    queryset = TossBet.objects.all()

class OverToOverBetCreateAPI(CreateAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = OverToOverBetSerializer
    queryset = OverToOverBet.objects.all()    

class OverToOverBetAPI(RetrieveDestroyAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = OverToOverBetSerializer
    queryset = OverToOverBet.objects.all()

class BallToBallBetCreateAPI(CreateAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = BallToBallBetSerializer
    queryset = BallToBallBet.objects.all()    

class BallToBallBetAPI(RetrieveDestroyAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = BallToBallBetSerializer
    queryset = BallToBallBet.objects.all()

class BookMakerBetCreateAPI(CreateAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = BookMakerBetSerializer
    queryset = BookMakerBet.objects.all()    

class BookMakerBetAPI(RetrieveDestroyAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = BookMakerBetSerializer
    queryset = BookMakerBet.objects.all()

class MatchBetCreateAPI(CreateAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = MatchBetSerializer
    queryset = MatchBet.objects.all()    

class MatchBetAPI(RetrieveDestroyAPIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = MatchBetSerializer
    queryset = MatchBet.objects.all()

def get_match_data(match):
    match_data = {}        
    serialized_match_data = MatchSerializer(match)
    match_data.update(serialized_match_data.data)
    scorea = Score.objects.filter(match=match, team=match.team_a)            
    scoreb = Score.objects.filter(match=match, team=match.team_b)   
    bookmakers = match.bookmaker_set
    match_data["bookmaker"] = BookMakerSerializer(bookmakers, many=True).data
    match_data["over_to_over_ratios"] = []
    match_data["ball2ball_ratios"] = []
    match_data['current_over'] = match.current_over
    scores_exist = False
    if scorea.exists():
        scores_exist = True
        serialized_score_a = ScoreSerializer(scorea.first())
        match_data[serialized_score_a.data["team"]] = serialized_score_a.data
        print(serialized_score_a.data)
    if scoreb.exists():
        scores_exist = True
        serialized_score_b = ScoreSerializer(scoreb.first())
        match_data[serialized_score_b.data["team"]] = serialized_score_b.data 
    if scores_exist:
        over2over_ratios = OverToOverRatio.objects.filter(match=match)         
        over2over_serializer = OverToOverRatioSerializer(over2over_ratios, many=True)
        ball2ball_ratios = BallToBallRatio.objects.filter(match=match)         
        ball2ball_serializer = BallToBallRatioSerializer(ball2ball_ratios, many=True)
        match_data["over_to_over_ratios"] = over2over_serializer.data
        match_data["ball2ball_ratios"] = ball2ball_serializer.data
    return match_data

class CurrentMatchesAPI(APIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]    
    permission_classes = (IsAuthenticated,)    

    def get(self, request):
        matches = Match.objects.filter(not_required=False)        
        data = []
        for match in matches:    
            match_data = get_match_data(match)
            data.append(match_data)     
        old_matchs = Match.objects.filter(not_required=True).order_by('-id')      
        for match in old_matchs[:2]:
            match_data = get_match_data(match)
            data.append(match_data)
        print(data)
        if data == []:
            return Response({"message": "There aren't any matches scheduled today."})
        return Response({"data": data}, status=status.HTTP_200_OK)                

class MatcheDetailAPI(APIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]    
    permission_classes = (IsAuthenticated,)    

    def get(self, request, *args, **kwargs):
        matches = Match.objects.filter(match_id=kwargs.get('match_id'))
        if not matches.exists():
            return Response({"message": "There is't any match with this ID."})              
        match_data = get_match_data(matches.first())        
        return Response({"data": match_data}, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_pending_balance(request):
    def sum_pending(bets, pending_amount):
        for bet in bets:
            pending_amount += bet.amount_invested        
        return pending_amount
    pending_amount = 0
    bets = MatchBet.objects.filter(user=request.user, paid=False)
    pending_amount = sum_pending(bets, pending_amount)
    bets = OverToOverBet.objects.filter(user=request.user, paid=False)
    pending_amount = sum_pending(bets, pending_amount)     
    bets = BallToBallBet.objects.filter(user=request.user, paid=False)
    pending_amount = sum_pending(bets, pending_amount)     
    bets = BookMakerBet.objects.filter(user=request.user, paid=False)
    pending_amount = sum_pending(bets, pending_amount)     
    bets = TossBet.objects.filter(user=request.user, paid=False)
    pending_amount = sum_pending(bets, pending_amount)     
    return Response({"username": request.user.username, "pending_amount": pending_amount}, status.HTTP_200_OK)    

class UserDetailsAPI(APIView):
    if settings.BROWSE:
        authentication_classes = [authentication.BasicAuthentication]    
    permission_classes = (IsAuthenticated,)  

    def get(self, request):
        print(request.user)
        user_profile = UserProfile.objects.get(user=request.user)
        account = Account.objects.get(user=request.user)
        data = {}
        user_profile_serializer = UserProfileSerializer(user_profile)                
        data.update(user_profile_serializer.data)
        account_serializer = AccountSerializer(account)        
        data.update(account_serializer.data)                
        return Response({"data": data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def page_details(request):
    page_details = PageData.objects.all().last()
    if not page_details:
        return Response({"data": {"heading": "IPL 2022", "scorll_text": "Lorem Ipsum text"}}, status=status.HTTP_200_OK)
    return Response({"data": PageDataSerializer(page_details).data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_payment(request):

    amount = request.data.get('amount')
    name = request.data.get('name')
    email = request.data.get('email')

    try: 
        user = User.objects.get(email=email)
    except:
        return Response({'error': "Email doesn't exsists in our database"}, status=status.HTTP_404_NOT_FOUND)
    
    recharge = Recharge.objects.create(product_name=name,amount=amount, user=user.email)

    # serializer = RechargeSerializer(recharge)
    param_dict = {
        'MID': settings.MERCHANTID,
        'ORDER_ID': str(recharge.id),
        'TXN_AMOUNT': str(amount),
        'CUST_ID': email,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,        
    }
    
    param_dict['CHECKSUMHASH'] = paytm.generate_checksum(param_dict,  settings.MERCHANTID)
    
    return Response({'param_dict': param_dict})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_payment(request):
    checksum = ""    
    form = request.POST

    response_dict = {}
    recharge = None 

    for i in form.keys():   
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':            
            checksum = form[i]

        if i == 'ORDERID':            
            recharge = recharge.objects.get(id=form[i])
    
    verify = paytm.verify_checksum(response_dict, settings.MERCHANTID, checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':            
            print('Recharge successful')            
            recharge.paid = True
            recharge.save()            
            return render(request, 'payment_success.html', {'response': response_dict})
        else:
            print('Recharge was not successful because' + response_dict['RESPMSG'])
            return render(request, 'payment_success.html', {'response': response_dict})        

# CrossRechargeAPI, NotificationsAPI
