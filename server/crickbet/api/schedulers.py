from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from requests import request
from datetime import datetime, timedelta
from django.db.models import Q

from .helpers import last_or_create, get_ball_num



scheduler = BackgroundScheduler()

class FetchMatchesList:
    
    def __init__(self) -> None:
        self.api_key = settings.API_KEY
        self.odds_api_key = settings.ODDS_API_KEY
        self.start_date = datetime.now().strftime("%Y-%m-%d") # "2022-05-15" # 
        end_date = datetime.now() + timedelta(days=3)
        self.end_date = end_date.strftime("%Y-%m-%d") # "2022-05-16" #
        self.teams = None
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        self.current_matchs_url = f'https://cricket.sportmonks.com/api/v2.0/fixtures?api_token={self.api_key}&include=scoreboards&filter[starts_between]={self.start_date},{self.end_date}'
        self.odds_matchs_url = f'https://apiv2.api-cricket.com/cricket/?method=get_events&APIkey={self.odds_api_key}&date_start={self.start_date}&date_stop={self.end_date}'
        self.odds_url = f'https://apiv2.api-cricket.com/cricket/?method=get_odds&APIkey={self.odds_api_key}&date_start={self.start_date}&date_stop={self.end_date}'
        self.teams_url = f'https://cricket.sportmonks.com/api/v2.0/teams?api_token={self.api_key}'
        self.ball2ballscore_url = f"https://cricket.sportmonks.com/api/v2.0/fixtures?api_token={self.api_key}&include=balls,&filter[starts_between]={self.start_date},{self.end_date}"

    def _request(self, method, url, headers=None, payload=None):
        if not headers:
            headers = self.headers
        if not payload:
            resp = request(method=method, url=url, headers=headers)    
        json_resp = resp.json()
        # print(json_resp)
        data = json_resp.get('data') or json_resp.get('result')
        return data

    def set_teams(self):
        print("called set Teams")
        teams = self._request("GET", self.teams_url)                 
        self.teams = {team['id']: team for team in teams}

    def _distribute_user_amount(self, bet):
        acc = bet.user.account 
        acc.balance  = float(acc.balance) + float(bet.amount_invested)*float(bet.ratio_invested)
        acc.save() 
    
    def _pass_bets(self, bets, actual_outcome, bookmakers=None):
        for bet in bets:
            print("passing bet ", bet.id)
            bet.result = 'L'
            if bookmakers:
                invested_bookmaker = bookmakers.get(pk=bet.bookmaker_id)
                actual_outcome = invested_bookmaker.answer
            if str(bet.invested_on) == str(actual_outcome):
                bet.result = 'W'
                self._distribute_user_amount(bet)  
            bet.actual_result = actual_outcome             
            bet.paid = True
            bet.save()   

    def _create_match_from_data(self, match):
        from .models import Ratio, Match, OverToOverRatio, BallToBallRatio
        gold = Ratio.objects.create()
        diamond = Ratio.objects.create()
        toss_bet_ratio = Ratio.objects.create()
        team1 = self.teams[match["localteam_id"]]["name"]
        team2 = self.teams[match["visitorteam_id"]]["name"]
        match_name = f"{team1} vs {team2}"
        db_match = Match.objects.create(match_name=match_name, team_a=team1, team_b=team2,
                status=match['status'], date=datetime.strptime(match['starting_at'], "%Y-%m-%dT%H:%M:%S.000000Z"), gold=gold, tossbet_ratio = toss_bet_ratio, 
                diamond=diamond, match_id=match['id'], team_a_image=self.teams[match["localteam_id"]]["image_path"], 
                team_b_image=self.teams[match["visitorteam_id"]]["image_path"])                
        return db_match

    def _set_score(self, score, db_match, team, item_no):
        from .models import Score        
        score_c, _ = last_or_create(Score, match=db_match, team=team)         
        score_c.runs = score[item_no]['total']
        score_c.wickets = score[item_no]['wickets']
        score_c.overs = score[item_no]['overs'] 
        score_c.save()      

    def _save_score(self, db_match, score):
        from .models import OverToOverBet, BallToBallBet, BallToBallRatio, OverToOverRatio, Ratio
        print(score[1])    
        batting_team = self.teams[score[1]["team_id"]]["name"]
        batting_team_id = score[1]["team_id"]
        item_num = 1
        updated_at_1 = datetime.strptime(score[1]['updated_at'], "%Y-%m-%dT%H:%M:%S.000000Z")
        updated_at_2 = datetime.strptime(score[-1]['updated_at'], "%Y-%m-%dT%H:%M:%S.000000Z")
        if updated_at_1 < updated_at_2:
            batting_team = self.teams[score[-1]["team_id"]]["name"]
            batting_team_id = score[-1]["team_id"]
            item_num = -1
        print(batting_team)
        over_num = int(score[item_num]['overs'])               
        if over_num >= 0:
            if not OverToOverRatio.objects.filter(match=db_match, team=batting_team, over_num=over_num+2).exists() and ((over_num+1 < 20) and ('T20' in db_match.match_type) ):
                print("creating o2o bets")
                ratio = Ratio.objects.create(ratio_a=1.2, ratio_b=1.2)
                OverToOverRatio.objects.create(match=db_match, ratio=ratio, team=batting_team, over_num=over_num+2)
            over_previous_bets = OverToOverBet.objects.filter(match=db_match, over_num__lte=over_num, paid=False)
            all_b2b_data = self._request("GET",self.ball2ballscore_url)            
            # Filter current match b2b data           
            b2b_data = list(filter(lambda item: int(item["id"]) == int(db_match.match_id), all_b2b_data))
            print(len(all_b2b_data), db_match.match_id)
            if b2b_data:                
                b2b_data = b2b_data[0]["balls"]          
                # Filter batting team scores
                team_data = list(filter(lambda item: int(item['team_id']) == int(batting_team_id), b2b_data))
                # Filter previous over scores
                def get_over_score(ds_over_num):
                    data = list(filter(lambda item: int(item['ball']) == ds_over_num, team_data))            
                    return sum([int(item['score']['runs']) for item in data])                            

                def get_ball_score(ball_num):
                    data = list(filter(lambda item: get_ball_num(item['ball']) == ball_num, team_data))            
                    return data[-1]['score']['runs']
        
                for bet in over_previous_bets:                    
                    o2o_ratio = OverToOverRatio.objects.get(match=db_match, over_num=bet.over_num)  
                    expected_runs = o2o_ratio.expected_runs
                    actual_score = "YES"                    
                    if int(get_ball_score(bet.ball_num)) < expected_runs:
                        actual_score = "NO"
                    self._pass_bets([bet], actual_score)
                
                ball_num = get_ball_num(score[item_num]['overs'])                
                ball_previous_bets = BallToBallBet.objects.filter(match=db_match, ball_num__lte=ball_num, paid=False)
                for bet in ball_previous_bets:
                    b2b_ratio = BallToBallRatio.objects.get(match=db_match, ball_num=score[item_num]['overs'])
                    expected_runs = b2b_ratio.expected_runs
                    actual_score = "YES"                    
                    if int(get_ball_score(bet.ball_num)) < expected_runs:
                        actual_score = "NO"
                    self._pass_bets([bet], actual_score)                

        self._set_score(score, db_match, batting_team, item_no = item_num)     

    def _set_odd_ratio(self, ratio, odds):
        odds = list(odds.values())
        ratio.ratio_a = odds[0]
        ratio.ratio_b = odds[0]
        if  len(odds) > 0:
            ratio.ratio_b = odds[1]
        ratio.save()

    def _set_ratios(self, db_match):
        print("**Checking Ratios**")
        matches = self._request("GET", self.odds_matchs_url)        
        for match in matches:
            # print(match.get('event_home_team'), db_match.team_a)
            if db_match.team_a.lower() in match.get('event_home_team').lower() and db_match.team_b.lower() in match.get('event_away_team').lower():
                print(match.get('event_key'))     
                url = f"https://apiv2.api-cricket.com/cricket/?method=get_odds&APIkey={self.odds_api_key}&event_key={match.get('event_key')}"   
                odds = self._request('GET', url)
                if odds:
                    odds = odds.get(match.get('event_key'))
                    self._set_odd_ratio(db_match.gold, odds.get("Home/Away").get('Home'))
                    self._set_odd_ratio(db_match.diamond, odds.get("Home/Away").get('Away'))
                    toss_bet = db_match.tossbet_ratio
                    toss_bet.ratio_a = list(odds.get("To Win the Toss").get('Home').values())[0]
                    toss_bet.ratio_b = list(odds.get("To Win the Toss").get('Away').values())[0]
                    toss_bet.save()

                    # gold = db_match.gold
                    # gold.ratio_a = odds.get("Home/Away").get('Home').values()[0]
                    # gold.ratio_b = odds.get("Home/Away").get('Home').values()[0]
                    # if  len(odds.get("Home/Away").get('Home').values()) > 0:
                    #     gold.ratio_b = odds.get("Home/Away").get('Home').values()[1]
                    
                    # gold.ratio_a = odds.get("Home/Away").get('Home').values()[0]
                    # gold.ratio_b = odds.get("Home/Away").get('Home').values()[0]
                    # if  len(odds.get("Home/Away").get('Home').values()) > 0:
                    #     gold.ratio_b = odds.get("Home/Away").get('Home').values()[1]                    
                    print(odds.get("Home/Away"))
                    return
        return 

    def fetch_current_matches(self):                
        data = self._request("GET", self.current_matchs_url)        
        print("Fetched...")  
        self.validate_data(data)       

    def blockratio(self, ratio):
        ratio.blocked = True 
        ratio.save()  

    def validate_data(self, data):
        from .models import Match, MatchBet, BookMaker, BookMakerBet, TossBet
        # load teams if not available
        if not self.teams:
            self.set_teams()
        # check for not required and completed matches to reduce api calls
        for match in data:                                    
            db_match = Match.objects.filter(match_id=match['id'])
            if not db_match.exists():
                db_match = self._create_match_from_data(match)
            else:
                db_match = db_match.first()
            try:
                self._set_ratios(db_match)
            except:
                print("Error")

            # Blocking not required matches.
            if db_match.not_required:
                continue            

            match_type = match.get('type')
            if match_type:
                db_match.match_type = match_type
            
            toss_winner = match.get('toss_won_team_id')            
            if toss_winner:
                toss_winner = self.teams[toss_winner]["name"]
                db_match.toss_winning_team = toss_winner
                self.blockratio(db_match.tossbet_ratio)
                try:
                    # Toss bets
                    toss_bets = TossBet.objects.filter(match=db_match, paid=False)
                    self._pass_bets(toss_bets, toss_winner)
                except:
                    print('Pass 1')

                if match.get('scoreboards'):
                    db_match.ongoing = True
                    score = match.get('scoreboards')
                    self._save_score(db_match, score)
                                      
            match_winner = match.get('winner_team_id')
            if match_winner:
                match_winner = self.teams[match.get('winner_team_id')]['name']
                db_match.match_winning_team = match_winner 
                db_match.ongoing = False                        
                db_match.completed = True        
                self.blockratio(db_match.gold)
                self.blockratio(db_match.diamond)                
                # Match Bets
                bets = MatchBet.objects.filter(match=db_match, paid=False)
                self._pass_bets(bets, match_winner)                
                # BookMaker bets
                bets = BookMakerBet.objects.filter(match=db_match, paid=False)
                bookmakers = BookMaker.objects.filter(match=db_match)
                if bookmakers.exists():
                    self._pass_bets(bets, '', bookmakers)

                #  After distributing the money to all bets.
                db_match.not_required = True
            if match.get('status'):
                db_match.status = match['status']
            db_match.save()                                  



matches_fetcher = FetchMatchesList()

def get_live_matches():    
    matches_fetcher.fetch_current_matches()
    scheduler.add_job(matches_fetcher.fetch_current_matches, 'interval', minutes=1, id='current_matches_fetcher', replace_existing=True)
    scheduler.start()
    # pass    
     