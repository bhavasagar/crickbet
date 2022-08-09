<script setup>
import Header from "@/components/Header.vue";
import backgroundImage from "@/assets/ground.jpg"
import { onMounted, onBeforeMount, onUnmounted, ref, reactive, onBeforeUnmount } from "@vue/runtime-core";
import userStore from "@/stores/store.js";
import { useRoute } from "vue-router";
import {ToastSeverity} from 'primevue/api';
import { useToast } from "primevue/usetoast"; 
import Loader from "@/components/Loader.vue";

import formatDateTime from "@/helpers/FormatDateTime";
import Toast from "primevue/toast";

const toast = useToast();
const route = useRoute();
const store = userStore();
const placebet = ref(false);
var fetch_matches;
const bet_details = reactive({
    invested_on: null,
    bet_amount: 500,
    ratio_invested: 1,
    type: null,
    over_num: null,
    ball_num: null,
    bookmaker_id: null,
    blocked: false,
    min: 50
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

    switch(type){
        case "toss":
        case "bookmaker":
        case "over":
            bet_details.min = 100
            break         
        case "match":
            bet_details.min = 200
            break                       
        case "ball":
            bet_details.min = 50        
    }

    console.log(ratio_invested)
}

const handleBetSubmission = async () => {
    console.log(bet_details)
    if (store.user.balance < bet_details.bet_amount){
        toast.add({severity: ToastSeverity.WARN, summary: "Insufficient Balance", detail: "Please recharge to place bet."})
        return;
    }
    if (bet_details.type=='toss') {
        if (store.match.tossbet_ratio.blocked) return;
        if (bet_details.bet_amount < 100) return;        
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
        const data = await store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
            toast.add({severity: ToastSeverity.SUCCESS, summary: `Bet Placed with amount ${bet_details.bet_amount}`, detail: `Invested on ${bet_details.invested_on}`, life: 3000});
            store.getUserDetails();
        }
    }
    if (store.user.balance < bet_details.bet_amount){
        toast.add({severity: ToastSeverity.WARN, summary: "Insufficient Balance", detail: "Please recharge to place bet."})
        return;
    }
    else if (bet_details.type=='match') {
        if (store.match.gold.blocked || store.match.diamond.blocked) return;
        if (bet_details.bet_amount < 200) return;        
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
        const data = await store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
            toast.add({severity: ToastSeverity.SUCCESS, summary: `Bet Placed with amount ${bet_details.bet_amount}`, detail: `Invested on ${bet_details.invested_on}`, life: 3000});
            store.getUserDetails();
        }
        if (store.user.balance < bet_details.bet_amount){
        toast.add({severity: ToastSeverity.WARN, summary: "Insufficient Balance", detail: "Please recharge to place bet."})
        return;
    }
    }
    else if (bet_details.type=='over') {
        if (bet_details.bet_amount < 100) return;        
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
        const data = await store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
            toast.add({severity: ToastSeverity.SUCCESS, summary: `Bet Placed with amount ${bet_details.bet_amount}`, detail: `Invested on ${bet_details.invested_on}`, life: 3000});
            store.getUserDetails();
        }
    }    
    else if (bet_details.type=='ball') {
        if (bet_details.bet_amount < 50)  return;
        if (store.user.balance < bet_details.bet_amount){
            toast.add({severity: ToastSeverity.WARN, summary: "Insufficient Balance", detail: "Please recharge to place bet."})
            eturn;
        }
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
        const data = await store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
            toast.add({severity: ToastSeverity.SUCCESS, summary: `Bet Placed with amount ${bet_details.bet_amount}`, detail: `Invested on ${bet_details.invested_on}`, life: 3000});
            store.getUserDetails();
        }
        if (store.user.balance < bet_details.bet_amount){
        toast.add({severity: ToastSeverity.WARN, summary: "Insufficient Balance", detail: "Please recharge to place bet."})
        return;
    }
    }
    else if (bet_details.type=='bookmaker') {
        if (bet_details.bet_amount < 100) return;        
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
        const data = await store.request(url, options)
        console.log(data)
        if (data.id) {
            console.log("success");
            toast.add({severity: ToastSeverity.SUCCESS, summary: `Bet Placed with amount ${bet_details.bet_amount}`, detail: `Invested on ${bet_details.invested_on}`, life: 3000});
            store.getUserDetails();
        }
    }
    bet_details.bet_amount = null;
    placebet.value = false;
}

const getRandomUserCount = () => {
    return Number((Math.random() + 1.23)%1.46).toFixed(2) + 'k'
}

</script>

<template>
    <main>        
        <Loader v-if="store.match ? store.meta.loading = false : store.meta.loading = true" />        
        <Header />
        <div class="container" v-if="store.match" >
            <div class="match--header p-2">
                <span class="font-semibold text-base">{{store.match.match_name}}</span>
                <span style="text-align: right;" class="block">
                    {{formatDateTime(store.match.date)}}
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
                <span class="flex flex-row justify-content-evenly">
                    <div class="toss-winner flex flex-row justify-content-start ml-2 font-bold" v-if="store.match.toss_winning_team">
                        <span class="font-bold" >Toss Winner</span> <span class="mx-2">-</span> <span class="font-bold" v-if="store.match.toss_winning_team"> {{ store.match.toss_winning_team }} </span><span class="font-bold" v-else> N/A </span>
                    </div>
                    <div class="toss-winner flex flex-row justify-content-start ml-2 font-bold" v-if="store.match.match_winning_team">
                        <span class="font-bold" >Match Winner</span> <span class="mx-2">-</span> <span class="font-bold"  v-if="store.match.match_winning_team" > {{ store.match.match_winning_team }} </span><span class="font-bold" v-else> N/A </span>
                    </div>
                </span>
            </div>
            
            <Dialog class="p-dialog" header="INVEST" :key="header" v-model:visible="placebet"  >
                <div class="bet--details flex flex-row justify-content-between mx-1 my-3 "  >
                    <span class="font-bold">{{bet_details.invested_on}}</span> 
                    <span class="font-bold mr-3" >{{bet_details.ratio_invested}}</span>
                </div>                
                <form @submit.prevent="handleBetSubmission" class="amount flex flex-row justify-content-between mx-1 my-3 align-items-center" >
                    <InputNumber style="height: 100%;" class="mx-1 p-inputtext-sm" :min="bet_details.min" v-model="bet_details.bet_amount" />
                    <Button type="submit"  label="OK" style="height: 2rem; font-size: 1rem !important;width: fit-content !important; border-radius: 1.5px !important;" class="p-button p-button-custom ml-2"  />    
                    <span class="font-bold text-green-400 align-self-center mr-1 text-xl" > {{ bet_details.bet_amount*bet_details.ratio_invested }} </span>
                </form>    
                <div class="buttons-grid ">
                    <Button  label="50" style="border-radius: 1.5px !important;margin: 0 !important;" class="p-button p-button-custom py-1 px-1" @click="bet_details.bet_amount = 50"  />    
                    <Button  label="100" style="border-radius: 1.5px !important;margin: 0 !important;" class="p-button p-button-custom py-1 px-1" @click="bet_details.bet_amount = 100"  />    
                    <Button  label="1000" style="border-radius: 1.5px !important;margin: 0 !important;" class="p-button p-button-custom py-1 px-1" @click="bet_details.bet_amount = 1000"  />    

                    <Button  label="500" style="border-radius: 1.5px !important;margin: 0 !important;" class="p-button p-button-custom py-1 px-1" @click="bet_details.bet_amount = 500"  />    
                    <Button  label="300" style="border-radius: 1.5px !important;margin: 0 !important;" class="p-button p-button-custom py-1 px-1" @click="bet_details.bet_amount = 300"  />    
                    <Button  label="2000" style="border-radius: 1.5px !important;margin: 0 !important;" class="p-button p-button-custom py-1 px-1" @click="bet_details.bet_amount = 2000"  />    

                    <Button  label="5000" style="border-radius: 1.5px !important;margin: 0 !important;" class="p-button p-button-custom py-1 px-1" @click="bet_details.bet_amount = 5000"  />    
                    <Button  label="900" style="border-radius: 1.5px !important;margin: 0 !important;" class="p-button p-button-custom py-1 px-1" @click="bet_details.bet_amount = 900"  />    
                    <Button  label="3000" style="border-radius: 1.5px !important;margin: 0 !important;" class="p-button p-button-custom py-1 px-1" @click="bet_details.bet_amount = 3000"  />    

                </div>            
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
                                <span class="mr-2">Min: 100</span>
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
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" :class="store.match.tossbet_ratio.blocked && 'blocked'" style="width: 30%" @click="!store.match.tossbet_ratio.blocked && handleClick(store.match.team_a, store.match.tossbet_ratio.ratio_a, 'toss')" >                                
                                <span class="flex flex-column">
                                    <span>{{store.match.tossbet_ratio.ratio_a}}</span>
                                    <span class="user--count">{{ getRandomUserCount() }}</span>
                                </span>
                            </div>
                            
                        </div>

                        <div class="flex flex-row">
                            <div class="team--name span-2-col py-2 px-1 align-self-center" style="width: 70%" >
                                <span>
                                    {{store.match.team_b}}
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" :class="store.match.tossbet_ratio.blocked && 'blocked'" style="width: 30%" @click="!store.match.tossbet_ratio.blocked && handleClick(store.match.team_b, store.match.tossbet_ratio.ratio_b, 'toss')" >                                
                                <span class="flex flex-column">
                                    <span>{{store.match.tossbet_ratio.ratio_b}}</span>
                                    <span class="user--count">{{ getRandomUserCount() }}</span>
                                </span>
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
                                <span class="mr-2">Min: 200</span>
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
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" :class="store.match.gold.blocked && 'blocked'" @click="!store.match.gold.blocked && handleClick(store.match.team_a, store.match.gold.ratio_a, 'match')">
                                <span class="flex flex-column">
                                    <span>{{store.match.gold.ratio_a}}</span>
                                    <span class="user--count">{{ getRandomUserCount() }}</span>
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 lay-bet align-self-strech" :class="store.match.gold.blocked && 'blocked'" @click="!store.match.gold.blocked && handleClick(store.match.team_a, store.match.gold.ratio_b, 'match')">
                                <span class="flex flex-column">
                                    <span>{{store.match.gold.ratio_b}}</span>
                                    <span class="user--count">{{ getRandomUserCount() }}</span>
                                </span>
                            </div>
                        </div>

                        <div class="flex flex-row">
                            <div class="team--name span-2-col py-2 px-1 align-self-center">
                                <span>
                                    {{store.match.team_b}}
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" :class="store.match.diamond.blocked && 'blocked'" @click="!store.match.diamond.blocked && handleClick(store.match.team_b, store.match.diamond.ratio_a, 'match')">                                
                                 <span class="flex flex-column">
                                    <span>{{store.match.diamond.ratio_a}}</span>
                                    <span class="user--count">{{ getRandomUserCount() }}</span>
                                </span>
                                
                            </div>
                            <div class="ratio-bet--value py-2 lay-bet align-self-strech" :class="store.match.diamond.blocked && 'blocked'" @click="!store.match.diamond.blocked && handleClick(store.match.team_b, store.match.diamond.ratio_b, 'match')">                                
                                 <span class="flex flex-column">
                                    <span>{{store.match.diamond.ratio_b}}</span>
                                    <span class="user--count">{{ getRandomUserCount() }}</span>
                                </span>
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
                                <span class="mr-2">Min: 100</span>
                                <span>Max: 500000</span>
                            </div>                        
                            <div class="ratio--bet back-bet">
                                YES
                            </div>
                            <div class="ratio--bet lay-bet">
                                NO  
                            </div>
                        </div>
                        
                        <div class="flex flex-row" v-for="bookmaker in store.match.bookmaker" :key="bookmaker.id" >
                            <div class="team--name py-2 px-1 span-2-col align-self-center">
                                <span>
                                    {{bookmaker.question}}
                                </span>
                            </div>
                            <div class="ratio-bet--value py-2 back-bet align-self-strech" :class="bookmaker.ratio.blocked && 'blocked'" @click="handleClick(bookmaker.question, bookmaker.ratio.ratio_a, 'bookmaker', null, null, bookmaker.id)">
                                {{bookmaker.ratio.ratio_a}}
                            </div>
                            <div class="ratio-bet--value py-2 lay-bet align-self-strech" :class="bookmaker.ratio.blocked && 'blocked'" @click="handleClick(bookmaker.question, bookmaker.ratio.ratio_b, 'bookmaker', null, null, bookmaker.id)">
                                {{bookmaker.ratio.ratio_b}}
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
                            <div class="min-max--bet " style="flex: 4">
                                <span class="mr-2">Min: 100</span>
                                <span>Max: 500000</span>
                            </div>                        
                            <div class="ratio--bet back-bet" style="flex: 6">
                                Runs
                            </div>
                            <!-- <div class="ratio--bet lay-bet">
                                NO  
                            </div> -->
                        </div>
                        
                        <span v-for="over in store.match.over_to_over_ratios.filter(item => item.team == store.match.batting_team)" :key="over.id" >
                            <div class="flex flex-row" v-if="parseFloat(store.match.current_over)-1 < parseFloat(over.over_num)" >
                                <div class="team--name py-2 px-1 align-self-center flex flex-column" style="flex: 4">
                                    <span>
                                        Over {{ parseFloat(over.over_num) + 1 }}
                                    </span>
                                    <!-- <span style="padding: 0; margin: 0; font-size: 0.8rem; font-weight: 400">
                                        runs greater than {{over.expected_runs}}                                        
                                    </span> -->
                                </div>
                                <!-- <div class="ratio-bet--value py-2 back-bet align-self-strech" :class="(over.ratio.blocked || parseFloat(store.match.current_over)+1 >= parseFloat(over.over_num)) ? 'blocked' : ''" @click="!(over.ratio.blocked || parseFloat(store.match.current_over)+1 >= parseFloat(over.over_num)) ? handleClick('YES', over.ratio.ratio_a, 'over', over_num=over.over_num) : () => {}" >
                                    {{over.ratio.ratio_a}}
                                </div>
                                <div class="ratio-bet--value py-2 lay-bet align-self-strech" :class="(over.ratio.blocked || parseFloat(store.match.current_over)+1 >= parseFloat(over.over_num)) ? 'blocked' : ''" @click="!over.ratio.blocked && handleClick('NO', over.ratio.ratio_b, 'over', over_num=over.over_num)" >
                                    {{over.ratio.ratio_b}}
                                </div> -->
                                <div :class="(over.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(over.over_num)) ? 'suspended' : '' " class="flex flex-row" style="flex: 6">
                                    <!-- <span  class="flex flex-row" style="width: 100%; heigh: 100%"> -->
                                        <div class="ratio-bet--value py-2 back-bet align-self-strech" @click=" !(over.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(over.over_num)) ? handleClick(0, over.ratio.ratio_a, 'over', over_num=over.over_num) : () => {} " >
                                            0
                                        </div>
                                        <div class="ratio-bet--value py-2 lay-bet align-self-strech" @click="!(over.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(over.over_num)) ? handleClick(1, over.ratio.ratio_a, 'over', over_num=over.over_num) : () => {} " >
                                            1
                                        </div>
                                        <div class="ratio-bet--value py-2 back-bet align-self-strech" @click=" !(over.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(over.over_num)) ? handleClick(2, over.ratio.ratio_a, 'over', over_num=over.over_num) : () => {} " >
                                            2
                                        </div>
                                        <div class="ratio-bet--value py-2 lay-bet align-self-strech" @click="!(over.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(over.over_num)) ? handleClick(4, over.ratio.ratio_a, 'over', over_num=over.over_num) : () => {} " >
                                            4
                                        </div>
                                        <div class="ratio-bet--value py-2 back-bet align-self-strech" @click=" !(over.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(over.over_num)) ? handleClick(6, over.ratio.ratio_a, 'over', over_num=over.over_num) : () => {} " >
                                            6
                                        </div>
                                    <!-- </span> -->
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
                            <div class="min-max--bet px-1" style="flex: 4">
                                <span class="mr-2">Min: 50</span>
                                <span>Max: 500000</span>
                            </div>                        
                            <div class="ratio--bet back-bet" style="flex: 6">
                                Runs
                            </div>
                        </div>
                        <span v-for="ball_ratio in store.match.ball2ball_ratios.filter(item => item.team == store.match.batting_team)" :key="ball_ratio.id">
                            <div class="flex flex-row border-300 border-bottom-1" v-if=" parseFloat(store.match.current_over)+1 < parseFloat(ball_ratio.ball_num)" >
                                <div class="team--name py-2 px-1 align-self-center flex flex-column" style="flex: 4">
                                    <span>
                                        Ball {{parseFloat(ball_ratio.ball_num)+1}}
                                    </span>
                                    <!-- <span style="padding: 0; margin: 0; font-size: 0.8rem; font-weight: 400">
                                        runs greater than {{ball_ratio.expected_runs}}
                                    </span> -->
                                </div>

                                <div :class="(ball_ratio.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(ball_ratio.ball_num)) ? 'suspended' : '' " class="flex flex-row" style="flex: 6">
                                    <!-- <span  class="" style="width: 100%; heigh: 100%"> -->
                                        <div class="ratio-bet--value py-2 back-bet align-self-strech" @click=" !(ball_ratio.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(ball_ratio.ball_num)) ? handleClick(0, ball_ratio.ratio.ratio_a, 'ball', null, ball_ratio.ball_num) : () => {} " >
                                            0
                                        </div>
                                        <div class="ratio-bet--value py-2 lay-bet align-self-strech" @click="!(ball_ratio.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(ball_ratio.ball_num)) ? handleClick(1, ball_ratio.ratio.ratio_a, 'ball', null, ball_ratio.ball_num) : () => {} " >
                                            1
                                        </div>
                                        <div class="ratio-bet--value py-2 back-bet align-self-strech" @click=" !(ball_ratio.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(ball_ratio.ball_num)) ? handleClick(2, ball_ratio.ratio.ratio_a, 'ball', null, ball_ratio.ball_num) : () => {} " >
                                            2
                                        </div>
                                        <div class="ratio-bet--value py-2 lay-bet align-self-strech" @click="!(ball_ratio.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(ball_ratio.ball_num)) ? handleClick(4, ball_ratio.ratio.ratio_a, 'ball', null, ball_ratio.ball_num) : () => {} " >
                                            4
                                        </div>
                                        <div class="ratio-bet--value py-2 back-bet align-self-strech" @click=" !(ball_ratio.ratio.blocked || parseInt(store.match.current_over)+1 >= parseInt(ball_ratio.ball_num)) ? handleClick(6, ball_ratio.ratio.ratio_a, 'ball', null, ball_ratio.ball_num) : () => {} " >
                                            6
                                        </div>
                                    <!-- </span> -->
                                </div>
                            </div>
                        </span>                    
                    </div>
                </div>                                                       
            </div>            
        </div>

        <div style="margin-bottom: 5rem"></div>
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
    height: 100%;
    align-self: center;
    justify-content: center;
}
.match--header{
    background: var(--dark-shade-1);
    color: #fff;
}
.match-score-header{
    color: #fff;
}
.p-button > span{
    font-weight: 600;
}
</style>
<style >
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
.p-dialog-content {
    background: #eee !important;
    padding: 0.25rem !important;
}
.p-button-custom {
    background: rgb(21, 21, 21);    
    width: auto !important;
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
.blocked{
    position: relative;
    background: rgba(0,0,0,0.5) !important;
    justify-content: center;
    display: flex;
    align-items: center;
    z-index: 200;
    font-weight: bold;
    cursor: not-allowed;
}
.blocked::before {
    content: "BLOCKED";
    color: tomato;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 201;
    padding-top: 0.75rem;
    font-size: 1.05rem;
    border-right: 1px solid rgba(255,255,255, 0.2);
    font-weight: bold;
}
.buttons-grid{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 1fr);
    grid-gap: 0.5rem;
}
.user--count {
    font-size: 0.72rem;
    /* color: #929292 */
    opacity: 0.75;
    /* line-height: 1px; */
}

.suspended {
    position: relative;
    display: none;
    width: 100%;
    background: rgba(0, 0, 0, 0.5) !important;
    z-index: 100;    
    border-bottom: 0.1px solid #aaa;   
    font-weight: 500;
    font-size: 1rem;
    letter-spacing: 1.5px; 
    cursor: not-allowed;
}

.suspended::after {    
    position: absolute;
    content: "SUSPENDED";   
    color: tomato;background: rgba(0, 0, 0, 0.5);
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-content: center;
    align-self: center;
    font-weight: bold;
    line-height: 2rem;
}

.suspended:nth-child(n)::not(before) {
    opacity: 0;
}

</style>