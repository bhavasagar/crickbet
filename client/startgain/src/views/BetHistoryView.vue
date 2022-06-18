<script setup>
import logo from "@/assets/logo.png";
import { onBeforeMount, onMounted, reactive, ref } from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ToastSeverity} from 'primevue/api';
import { useToast } from "primevue/usetoast";   

import formatDateTime from "@/helpers/FormatDateTime.js"
import useStore from "@/stores/store.js";
import Header from "@/components/Header.vue";
import Loader from "@/components/Loader.vue";

const store = useStore();

const toast = useToast();
const route = useRoute();
const router = useRouter();
const bet_history = ref ({});

onBeforeMount(async () => {
    const access_token = JSON.parse(localStorage.getItem("credentials") || '{}')?.access_token;
    const options = {
    method: "GET",
    headers: new Headers({"Authorization": `Bearer ${access_token}`})
    };            
    const resp = await fetch(`${store.server}/bet-history/  `, options);    
    const data = await resp.json();
    bet_history.value = data.data;
    console.log(bet_history, data)
})

</script>

<template>
    <main>
        <Loader v-if="!bet_history" />
        <Header />
        <div class="container">
            <div class="heading  px-1 py-3 text-center " style="background: #000;color: #fff;" >
                <h3 class="font-bold">Bet History</h3>
            </div>
            <div class="bet--history" v-if="bet_history.length > 0">
                <div class="history--row flex flex-row justify-content-between my-3 mx-2 shadow-3 " style=" position: relative;" :key="bet.id" v-for="bet in bet_history" >                    
                    <span class="flex flex-column my-1 px-1" style="width: 80%;" > 
                        <span class="flex flex-row py-2 " >
                            <span class="mx-2 font-semibold" > {{bet.id}} </span>
                            <span class="mx-1 dot  align-self-center" ></span>
                            <span class="mx-1 font-semibold"  > <span v-if="bet.type != 'match'" style="text-transform: uppercase;" > {{bet.type}} </span>  {{bet.invested_on}} </span>
                        </span>
                        <span class="px-2 py-1 flex flex-row align-items-baseline " >
                            <span class="mr-3" style="font-size: 0.8rem" > {{formatDateTime(bet.made_on)}} </span>
                            <span class="badge px-2 " > {{bet.type}} </span>
                            <span class="ml-3 align-self-center" v-if="bet.paid"  > <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="green"><g><rect fill="none" height="24" width="24"/></g><g><g><path d="M23,11.99l-2.44-2.79l0.34-3.69l-3.61-0.82L15.4,1.5L12,2.96L8.6,1.5L6.71,4.69L3.1,5.5L3.44,9.2L1,11.99l2.44,2.79 l-0.34,3.7l3.61,0.82L8.6,22.5l3.4-1.47l3.4,1.46l1.89-3.19l3.61-0.82l-0.34-3.69L23,11.99z M19.05,13.47l-0.56,0.65l0.08,0.85 l0.18,1.95l-1.9,0.43l-0.84,0.19l-0.44,0.74l-0.99,1.68l-1.78-0.77L12,18.85l-0.79,0.34l-1.78,0.77l-0.99-1.67l-0.44-0.74 l-0.84-0.19l-1.9-0.43l0.18-1.96l0.08-0.85l-0.56-0.65l-1.29-1.47l1.29-1.48l0.56-0.65L5.43,9.01L5.25,7.07l1.9-0.43l0.84-0.19 l0.44-0.74l0.99-1.68l1.78,0.77L12,5.14l0.79-0.34l1.78-0.77l0.99,1.68l0.44,0.74l0.84,0.19l1.9,0.43l-0.18,1.95l-0.08,0.85 l0.56,0.65l1.29,1.47L19.05,13.47z"/><polygon points="10.09,13.75 7.77,11.42 6.29,12.91 10.09,16.72 17.43,9.36 15.95,7.87"/></g></g></svg> </span>
                            <span class="ml-3 align-self-center" v-else  > <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#FCF55F"><g><rect fill="none" height="24" width="24"/></g><g><g><path d="M12,2C6.48,2,2,6.48,2,12c0,5.52,4.48,10,10,10s10-4.48,10-10C22,6.48,17.52,2,12,2z M12,20c-4.42,0-8-3.58-8-8 c0-4.42,3.58-8,8-8s8,3.58,8,8C20,16.42,16.42,20,12,20z"/><circle cx="7" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="17" cy="12" r="1.5"/></g></g></svg> </span>
                        </span>
                    </span>
                    <span class="px-1 flex flex-column justify-content-center align-items-center" :class="bet.result ? bet.result == 'W' ? 'green': 'red' : 'yellow' " style="width: 20%;" >
                        <span class="my-1 font-bold" style="color: #fff" v-if="bet.result == 'W'" > Rs. {{ parseFloat(bet.amount_invested)*parseFloat(bet.ratio_invested) }} </span>
                        <span class="my-1 font-bold" style="color: #fff" v-else > Rs. {{ bet.amount_invested }} </span>
                        <svg v-if="bet.result == 'L'" xmlns="http://www.w3.org/2000/svg"  enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#fff"><g><rect fill="none" height="24" width="24"/></g><g><g><rect height="12" width="4" x="19" y="3"/><path d="M1,11.6V16h8.31l-1.12,5.38L9.83,23L17,15.82V3H4.69L1,11.6z M15,5v9.99l-4.34,4.35l0.61-2.93l0.5-2.41H9.31H3v-1.99 L6.01,5H15z"/></g></g></svg>
                        <svg v-if="bet.result == 'W'" xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#fff"><g><rect fill="none" height="24" width="24" x="0" y="0"/></g><g><g><path d="M9,21h9c0.83,0,1.54-0.5,1.84-1.22l3.02-7.05C22.95,12.5,23,12.26,23,12v-2c0-1.1-0.9-2-2-2h-6.31l0.95-4.57l0.03-0.32 c0-0.41-0.17-0.79-0.44-1.06L14.17,1L7.58,7.59C7.22,7.95,7,8.45,7,9v10C7,20.1,7.9,21,9,21z M9,9l4.34-4.34L12,10h9v2l-3,7H9V9z M1,9h4v12H1V9z"/></g></g></svg>
                    </span>                                       
                </div>                
            </div>   
            <div class="p-3 m-1" v-else>
                Bet history is not available.
            </div>      
        </div>
    </main>
</template>


<style>
.badge{    
    background: rgb(79, 78, 78);
    color: #fff;
    border-radius: 3px;
}
.red{
    background: red;
}
.green {
    background: green;
}
.yellow {
    background: #FCF55F;
}
.dot{
    width: 0.35rem;
    height: 0.35rem;
    border-radius: 50%;
    background: #000;
}
</style>