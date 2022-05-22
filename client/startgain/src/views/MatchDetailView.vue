<script setup>
import Header from "@/components/Header.vue";
import backgroundImage from "@/assets/ground.jpg"
import { onMounted, onBeforeMount, onUnmounted, ref, reactive, onBeforeUnmount } from "@vue/runtime-core";
import userStore from "@/stores/store.js";
import { useRoute } from "vue-router";

const route = useRoute();
var fetch_matches
const store = userStore();
const placebet = ref(false);
const bet_details = reactive({
    invested_on: null,
    bet_amount: 500,
    ratio_invested: 1,
    type: null,
    over_num: null,
    ball_num: null,
    bookmaker_id: null
})

onBeforeMount(() => {
    clearInterval(fetch_matches);
    fetch_matches = setInterval(() => {
        store.getMatchDetail(route.params.matchid);
    }, 6*1000);    
});

onBeforeUnmount(() => {
    clearInterval(fetch_matches);
});

const handleClick = (invested_on, ratio_invested, type, over_num=null, ball_num=null, bookmaker_id=null) => {
    console.log(invested_on, ratio_invested, type, over_num, ball_num, bookmaker_id)
    bet_details.invested_on = invested_on;
    bet_details.ratio_invested = ratio_invested;
    bet_details.type = type;
    bet_details.over_num = over_num;
    bet_details.ball_num = ball_num;
    bet_details.bookmaker_id = bookmaker_id;
    placebet.value = true;
    console.log(ratio_invested)
}

const handleBetSubmission = () => {
    console.log(bet_details)
    if (bet_details.type=='toss') {
        const access_token = JSON.parse(localStorage.getItem("credentials")).access_token;
        console.log(access_token);
        const url = `${store.server}/tossbet/`;
        const options = {
            method: "POST",
            headers: new Headers({"Content-Type": "application/json", 'Authorization': `Bearer ${access_token}`}),
            body: JSON.stringify({
                                "user": store.user.id,
                                "match": store.match.id,
                                "amount_invested": bet_details.bet_amount,
                                "invested_on": bet_details.invested_on,
                                "ratio_invested": 2
                                })
        }
        const data = store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
        }
    }
    else if (bet_details.type=='match') {
        const access_token = JSON.parse(localStorage.getItem("credentials")).access_token;
        console.log(access_token);
        const url = `${store.server}/matchbet/`;
        const options = {
            method: "POST",
            headers: new Headers({"Content-Type": "application/json", 'Authorization': `Bearer ${access_token}`}),
            body: JSON.stringify({
                                "user": store.user.id,
                                "match": store.match.id,
                                "amount_invested": bet_details.bet_amount,
                                "invested_on": bet_details.invested_on,
                                "ratio_invested": bet_details.ratio_invested
                                })
        }
        const data = store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
        }
    }
    else if (bet_details.type=='over') {
        const access_token = JSON.parse(localStorage.getItem("credentials")).access_token;
        console.log(access_token);
        const url = `${store.server}/overtooverbet/`;
        const options = {
            method: "POST",
            headers: new Headers({"Content-Type": "application/json", 'Authorization': `Bearer ${access_token}`}),
            body: JSON.stringify({
                                "user": store.user.id,
                                "match": store.match.id,
                                "amount_invested": bet_details.bet_amount,
                                "invested_on": bet_details.invested_on,
                                "ratio_invested": bet_details.ratio_invested,
                                "over_num": bet_details.over_num,
                                "team": store.match.batting_team
                                })
        }
        const data = store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
        }
    }    
    else if (bet_details.type=='ball') {
        const access_token = JSON.parse(localStorage.getItem("credentials")).access_token;
        console.log(access_token);
        const url = `${store.server}/balltoballbet/`;
        const options = {
            method: "POST",
            headers: new Headers({"Content-Type": "application/json", 'Authorization': `Bearer ${access_token}`}),
            body: JSON.stringify({
                                "user": store.user.id,
                                "match": store.match.id,
                                "amount_invested": bet_details.bet_amount,
                                "invested_on": bet_details.invested_on,
                                "ratio_invested": bet_details.ratio_invested,
                                "ball_num": bet_details.ball_num,
                                "team": store.match.batting_team
                                })
        }
        const data = store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
        }
    }
    else if (bet_details.type=='bookmaker') {
        const access_token = JSON.parse(localStorage.getItem("credentials")).access_token;
        console.log(access_token);
        const url = `${store.server}/bookmakerbet/`;
        const options = {
            method: "POST",
            headers: new Headers({"Content-Type": "application/json", 'Authorization': `Bearer ${access_token}`}),
            body: JSON.stringify({
                                "user": store.user.id,
                                "match": store.match.id,
                                "amount_invested": bet_details.bet_amount,
                                "invested_on": bet_details.invested_on,
                                "ratio_invested": bet_details.ratio_invested,  
                                "bookmaker_id": bet_details.bookmaker_id                              
                                })
        }
        const data = store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
        }
    }
    placebet.value = false;
}

</script>

<template>
    <main>
        <Header />
        <div class="container" v-if="store.match" >
            <div class="match--header p-2">
                <span class="font-semibold text-base">{{store.match.match_name}}</span>
                <span style="text-align: right;" class="block">
                    {{store.match.date}}
                </span>
            </div>
            <div class="match-score-header p-3" style="font: size 0.95rem;background-position: center;" :style="{ backgroundImage: `url(${backgroundImage})` }">
                <div class="score--header" style="font-size: 0.9rem">                    
                    <span class="m-2 font-bold">{{store.match.status}}</span>
                </div>
                <div class="scorebord flex flex-row justify-content-between m-2">   
                    <div class="font-bold flex flex-row">
                        <span class="team--name font-bold">
                            {{store.match.team_a}}
                        </span>
                    </div>
                    <div class="team-score font-bold" >
                        <span class="font-bold" v-if="store.match[store.match.team_a]">
                            {{store.match[store.match.team_a].runs}}-{{store.match[store.match.team_a].wickets}} ({{store.match[store.match.team_a].overs}})
                        </span>
                        <span class="font-bold" v-else>
                            N/A
                        </span>
                    </div>
                </div>
                <div class="scorebord flex flex-row justify-content-between m-2">
                    <div class="flex flex-row">
                        <span class="team--name font-bold">
                            {{store.match.team_b}}
                        </span>
                    </div>
                    <div class="team-score font-bold">
                        <span class="font-bold" v-if="store.match[store.match.team_b]">
                            {{store.match[store.match.team_b].runs}}-{{store.match[store.match.team_b].wickets}} ({{store.match[store.match.team_b].overs}})
                        </span>
                        <span class="font-bold" v-else>
                            N/A
                        </span>
                    </div>
                </div>
                <div class="toss-winner flex flex-row justify-content-start ml-2 font-bold">
                    <span class="font-bold" >Toss Winner</span> <span class="mx-2">-</span> <span class="font-bold" > {{ store.match.toss_winning_team }}</span>
                </div>
            </div>
            
            <Dialog class="p-dialog" header="INVEST" :key="header" v-model:visible="placebet" >
                <div class="bet--details flex flex-row justify-content-between p-2 mx-1 my-3 ">
                    <span class="team--name">{{bet_details.invested_on}}</span>
                    <span class="ratio--bet">{{bet_details.ratio_invested}}</span>
                </div>                
                <form @submit.prevent="handleBetSubmission" class="amount flex flex-row justify-content-between p-2 mx-1 my-3 align-content-center" >
                    <InputNumber style="height: 2.6rem" v-model="bet_details.bet_amount" />
                    <Button type="submit"  label="Submit" class="p-button p-button-custom ml-2"  />    
                </form>                
            </Dialog>

            <div class="contianer--bets my-3" v-if="store.match">

                <div class="match--bet flex flex-column lg:my-0 md:my-0 my-2 md:mx-2 lg:mx-2" id="tossbet" v-if="!store.match.toss_winning_team" >
                    <div class="title--bet py-1 px-3 flex flex-row align-items-center justify-content-between">
                        <span>TOSS BET</span>
                        <span class="pi pi-info-circle mr-0 "></span>
                    </div>
                    <div class="details--bet">
                        <div class="flex flex-row">
                            <div class="min-max--bet span-2-col" style="width: 70%">
                                <span class="mr-2">Min: 500</span>
                                <span>Max: 500000</span>
                            </div>                        
                            <div class="ratio--bet back-bet" style="width: 30%" >
                                RATIO
                            </div>
                            
                        </div>
                        
                        <div class="flex flex-row" >
                            <div class="team--name py-2 px-1 span-2-col align-self-center" style="width: 70%" >
                                <span>
                                    {{store.match.team_a}}
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" style="width: 30%" @click="handleClick(store.match.team_a, store.match.tossbet_ratio.ratio_a, 'toss')" >
                                {{store.match.tossbet_ratio.ratio_a}}
                            </div>
                            
                        </div>

                        <div class="flex flex-row">
                            <div class="team--name span-2-col py-2 px-1 align-self-center" style="width: 70%" >
                                <span>
                                    {{store.match.team_b}}
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" style="width: 30%" @click="handleClick(store.match.team_b, store.match.tossbet_ratio.ratio_b, 'toss')" >
                                {{store.match.tossbet_ratio.ratio_b}}
                            </div>
                            
                        </div>

                    </div>
                </div>

                <div class="match--bet flex flex-column lg:my-0 md:my-0 sm:my-2 md:mx-2 lg:mx-2" id="match">
                    <div class="title--bet py-1 px-3 flex flex-row align-items-center justify-content-between">
                        <span>MATCH ODDS</span>
                        <span class="pi pi-info-circle mr-0 "></span>
                    </div>
                    <div class="details--bet">
                        <div class="flex flex-row">
                            <div class="min-max--bet span-2-col">
                                <span class="mr-2">Min: 500</span>
                                <span>Max: 500000</span>
                            </div>                        
                            <div class="ratio--bet back-bet">
                                BACK
                            </div>
                            <div class="ratio--bet lay-bet">
                                LAY
                            </div>
                        </div>
                        
                        <div class="flex flex-row">
                            <div class="team--name py-2 px-1 span-2-col align-self-center">
                                <span>
                                    {{store.match.team_a}}
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" @click="handleClick(store.match.team_a, store.match.gold.ratio_a, 'match')">
                                {{store.match.gold.ratio_a}}
                            </div>
                            <div class="ratio-bet--value py-2 lay-bet align-self-strech" @click="handleClick(store.match.team_b, store.match.gold.ratio_b, 'match')">
                                {{store.match.gold.ratio_b}}
                            </div>
                        </div>

                        <div class="flex flex-row">
                            <div class="team--name span-2-col py-2 px-1 align-self-center">
                                <span>
                                    {{store.match.team_b}}
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" @click="handleClick(store.match.team_a, store.match.diamond.ratio_a, 'match')">
                                {{store.match.diamond.ratio_a}}
                            </div>
                            <div class="ratio-bet--value py-2 lay-bet align-self-strech" @click="handleClick(store.match.team_b, store.match.diamond.ratio_b, 'match')">
                                {{store.match.diamond.ratio_b}}
                            </div>
                        </div>

                    </div>
                </div>
                
                <div class="match--bet flex flex-column lg:my-0 md:my-0 my-2 md:mx-2 lg:mx-2" id="bookmaker" v-if="store.match.bookmaker.length > 0" >
                    <div class="title--bet py-1 px-3 flex flex-row align-items-center justify-content-between">
                        <span>BOOKMAKER</span>
                        <span class="pi pi-info-circle mr-0 "></span>
                    </div>
                    <div class="details--bet">
                        <div class="flex flex-row">
                            <div class="min-max--bet span-2-col">
                                <span class="mr-2">Min: 500</span>
                                <span>Max: 500000</span>
                            </div>                        
                            <div class="ratio--bet back-bet">
                                YES
                            </div>
                            <div class="ratio--bet lay-bet">
                                NO  
                            </div>
                        </div>
                        
                        <div class="flex flex-row">
                            <div class="team--name py-2 px-1 span-2-col align-self-center">
                                <span>
                                    Score in last over will be greater than 12?
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" @click="handleClick('replace it by qusestion', 'store.match.tossbet_ratio.ratio_a', 'bookmaker')">
                                1.2
                            </div>
                            <div class="ratio-bet--value py-2 lay-bet align-self-strech">
                                1.4
                            </div>
                        </div>

                        <div class="flex flex-row">
                            <div class="team--name span-2-col py-2 px-1 align-self-center">
                                <span>
                                    Wide ball in next over?
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 back-bet align-self-strech">
                                2.2
                            </div>
                            <div class="ratio-bet--value py-2 lay-bet align-self-strech">
                                2.1
                            </div>
                        </div>

                    </div>
                </div>                           
                
                
                <div class="match--bet flex flex-column lg:my-0 md:my-0 my-2 md:mx-2 lg:mx-2" id="over" v-if="store.match.over_to_over_ratios.length > 0" >
                    <div class="title--bet py-1 px-3 flex flex-row align-items-center justify-content-between">
                        <span>OVER TO OVER</span>
                        <span class="pi pi-info-circle mr-0 "></span>
                    </div>
                    <div class="details--bet">
                        <div class="flex flex-row">
                            <div class="min-max--bet span-2-col">
                                <span class="mr-2">Min: 500</span>
                                <span>Max: 500000</span>
                            </div>                        
                            <div class="ratio--bet back-bet">
                                YES
                            </div>
                            <div class="ratio--bet lay-bet">
                                NO  
                            </div>
                        </div>
                        
                        <span v-for="over in store.match.over_to_over_ratios" :key="over.id" >
                            <div class="flex flex-row" v-if=" parseFloat(store.match.current_over)+1 < parseFloat(over.over_num)" >
                                <div class="team--name py-2 px-1 span-2-col align-self-center flex flex-column">
                                    <span>
                                        Over {{over.over_num}}
                                    </span>
                                    <span style="padding: 0; margin: 0; font-size: 0.8rem; font-weight: 400">
                                        runs greater than {{over.expected_runs}}
                                        <!-- {{expected_runs}} -->
                                    </span>
                                </div>
                                <div class="ratio-bet--value py-2 back-bet align-self-strech" @click="handleClick('YES', over.ratio.ratio_a, 'over', over_num=over.over_num)" >
                                    {{over.ratio.ratio_a}}
                                </div>
                                <div class="ratio-bet--value py-2 lay-bet align-self-strech" @click="handleClick('NO', over.ratio.ratio_b, 'over', over_num=over.over_num)" >
                                    {{over.ratio.ratio_b}}
                                </div>
                            </div>                    
                        </span>
                    </div>
                </div>      

                <div class="match--bet flex flex-column lg:my-0 md:my-0 my-2 md:mx-2 lg:mx-2" id="ball" v-if="store.match.ball2ball_ratios.length > 0">
                    <div class="title--bet py-1 px-3 flex flex-row align-items-center justify-content-between">
                        <span>BALL TO BALL</span>
                        <span class="pi pi-info-circle mr-0 "></span>
                    </div>
                    <div class="details--bet">
                        <div class="flex flex-row">
                            <div class="min-max--bet span-2-col">
                                <span class="mr-2">Min: 500</span>
                                <span>Max: 500000</span>
                            </div>                        
                            <div class="ratio--bet back-bet">
                                YES
                            </div>
                            <div class="ratio--bet lay-bet">
                                NO  
                            </div>
                        </div>
                        <span v-for="ball_ratio in store.match.ball2ball_ratios" :key="ball_ratio.id">
                            <div class="flex flex-row" v-if=" parseFloat(store.match.current_over)+1 < parseFloat(ball_ratio.ball_num)" >
                                <div class="team--name py-2 px-1 span-2-col align-self-center flex flex-column">
                                    <span>
                                        Ball {{ball_ratio.ball_num}}
                                    </span>
                                    <span style="padding: 0; margin: 0; font-size: 0.8rem; font-weight: 400">
                                        runs greater than {{ball_ratio.expected_runs}}
                                    </span>
                                </div>
                                <div class="ratio-bet--value py-2 back-bet align-self-strech" @click="handleClick('YES', ball_ratio.ratio.ratio_a, 'ball', null, ball_ratio.ball_num)" >
                                    {{ball_ratio.ratio.ratio_a}}
                                </div>
                                <div class="ratio-bet--value py-2 lay-bet align-self-strech" @click="handleClick('NO', ball_ratio.ratio.ratio_b, 'ball', null, ball_ratio.ball_num)" >
                                    {{ball_ratio.ratio.ratio_b}}
                                </div>
                            </div>
                        </span>                    
                    </div>
                </div>                                                       
            </div>            
        </div>
    </main>  
</template>

<style scoped>
.contianer--bets{
    display: grid;   
    grid-template-columns: repeat(1, 1fr);
}
@media (min-width:900px) {
    .contianer--bets{     
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
        grid-template-areas: 
                            "match over ball"
                            "bookmaker over ball";
    }    
    #match{
        grid-area: match;
    }
    #over{
        grid-area: over;
    }
    #ball{
        grid-area: ball;
    }
    #bookmaker{
        grid-area: bookmaker;
    }
}
.container{
    background: #fbfbfb;
}
.title--bet{
    background: #424242;
    color: #fff;
}
.details--bet{
    /* display: grid;
    grid-template-columns: repeat(5, 1fr); */
    /* grid-template-rows: 0.8fr 2fr 2fr;   */
    background: #eae9e9; 
    width: 100%;
}
.details--bet *{
    font-weight: 700;   
}
.back-bet{
    background: var(--back-bg);
}
.lay-bet{
    background: var(--lay-bg);
}
.details--bet > div {
    border-right: 0.1px solid #929292;    
    border-bottom: 0.1px solid #929292;    
    padding-left: 0.25rem;    
}
/* .team--name{
    padding-top: 0.5rem;
} */
.span-2-col {
    /* grid-column: 1/4; */
    /* flex-grow: 3; */
    width: 60%;
}
.ratio--bet, .ratio-bet--value{
    text-align: center;
    /* flex-grow: 2;    */
    width: 20%;
}
.match--header{
    background: var(--dark-shade-1);
    color: #fff;
}
.match-score-header{
    color: #fff;
}
</style>

<style>
.p-dialog-mask{
    width: 100vw !important;
    height: 100vh !important;
    align-items: unset !important;
    background: rgba(0, 0, 0, 0.3);
}
.p-dialog-header{
    background: #424242 !important;
    padding: 0.25rem 1rem !important;
    color: #fff !important;
}
.p-dialog{
    margin: 0.25rem !important;  
    box-shadow: none !important;  
    width: 95% !important;
}
.p-button-custom {
    background: rgb(21, 21, 21);    
    width: 99%;
    margin: 0.5rem auto;
    border-radius: 5px;
    font-size: 1.1rem;
    border: 1px solid rgb(50, 50, 50);
}
.p-button-custom:enabled:active, .p-button-custom:enabled:hover {
    background: rgb(21, 21, 21);  
    color: #ffffff;
    border-color: rgb(50, 50, 50);  
}
.p-button:focus {
    box-shadow: 0 0 0 0.2rem rgba(208, 207, 207, 0.5) !important;
}
</style>