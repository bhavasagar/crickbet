<script setup>
import logo from "@/assets/logo.png";
import { onBeforeMount, onMounted, reactive, ref } from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ToastSeverity} from 'primevue/api';
import { useToast } from "primevue/usetoast";   

import { email, required, url } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';

import formatDateTime from "@/helpers/FormatDateTime.js"
import useStore from "@/stores/store.js";
import Header from "@/components/Header.vue";
import Loader from "@/components/Loader.vue";

const store = useStore();

const toast = useToast();
const route = useRoute();
const router = useRouter();
const wallet_history = ref ({});

onBeforeMount(async () => {    
    const access_token = JSON.parse(localStorage.getItem("credentials") || '{}')?.access_token;
    const options = {
    method: "GET",
    headers: new Headers({"Authorization": `Bearer ${access_token}`})
    };            
    const resp = await fetch(`${store.server}/wallet-history/`, options);    
    const data = await resp.json();
    wallet_history.value = data.data;
    console.log(wallet_history, data);
})

</script>

<template>
    <main>
        <Loader v-if="!wallet_history" />
        <Header />
        <div class="container">
            <div class="heading  px-1 py-3 text-center " style="background: #000;color: #fff;" >
                <h3 class="font-bold">Wallet History</h3>
            </div>
            <div class="bet--history" v-if="wallet_history.length > 0" >
                <div class="history--row flex flex-row justify-content-between my-3 mx-2 shadow-3 " style=" position: relative;" :key="trans.id" v-for="trans in wallet_history" >                    
                    <span class="flex flex-column my-1 px-1" style="width: 80%;" > 
                        <span class="flex flex-row py-2 " >
                            <span class="mx-2 font-semibold" > {{trans.id}} </span>
                            <span class="mx-1 dot  align-self-center" ></span>
                            <span class="mx-1 font-semibold " v-if="trans.type == 'R'"  > Recharge </span>
                            <span class="mx-1 font-semibold " v-else  > WithDraw </span>
                        </span>
                        <span class="px-2 py-1 flex flex-row align-items-baseline " >
                            <span class="mr-3" style="font-size: 0.75rem" > {{formatDateTime(trans.made_on)}} </span>
                            <span class="badge px-2" > {{trans.mode}} </span>
                            <span class="ml-3 align-self-center" v-if="trans.paid"  > <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="green"><g><rect fill="none" height="24" width="24"/></g><g><g><path d="M23,11.99l-2.44-2.79l0.34-3.69l-3.61-0.82L15.4,1.5L12,2.96L8.6,1.5L6.71,4.69L3.1,5.5L3.44,9.2L1,11.99l2.44,2.79 l-0.34,3.7l3.61,0.82L8.6,22.5l3.4-1.47l3.4,1.46l1.89-3.19l3.61-0.82l-0.34-3.69L23,11.99z M19.05,13.47l-0.56,0.65l0.08,0.85 l0.18,1.95l-1.9,0.43l-0.84,0.19l-0.44,0.74l-0.99,1.68l-1.78-0.77L12,18.85l-0.79,0.34l-1.78,0.77l-0.99-1.67l-0.44-0.74 l-0.84-0.19l-1.9-0.43l0.18-1.96l0.08-0.85l-0.56-0.65l-1.29-1.47l1.29-1.48l0.56-0.65L5.43,9.01L5.25,7.07l1.9-0.43l0.84-0.19 l0.44-0.74l0.99-1.68l1.78,0.77L12,5.14l0.79-0.34l1.78-0.77l0.99,1.68l0.44,0.74l0.84,0.19l1.9,0.43l-0.18,1.95l-0.08,0.85 l0.56,0.65l1.29,1.47L19.05,13.47z"/><polygon points="10.09,13.75 7.77,11.42 6.29,12.91 10.09,16.72 17.43,9.36 15.95,7.87"/></g></g></svg> </span>
                            <span class="ml-3 align-self-center" v-else  > <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="yellow"><g><rect fill="none" height="24" width="24"/></g><g><g><path d="M12,2C6.48,2,2,6.48,2,12c0,5.52,4.48,10,10,10s10-4.48,10-10C22,6.48,17.52,2,12,2z M12,20c-4.42,0-8-3.58-8-8 c0-4.42,3.58-8,8-8s8,3.58,8,8C20,16.42,16.42,20,12,20z"/><circle cx="7" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="17" cy="12" r="1.5"/></g></g></svg> </span>
                        </span>
                    </span>
                    <span class="px-1 flex flex-column justify-content-center align-items-center" :class="trans.type == 'R' ? 'green': 'red'" style="width: 20%;" >
                        <span class="my-1 font-bold" style="color: #fff" > {{trans.amount}} </span>
                        <svg v-if="trans.type == 'R'"  xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24px" viewBox="0 0 24 24" width="24px" fill="#fff"><g><path d="M0,0h24v24H0V0z" fill="none"/></g><g><g><path d="M11,8v3H8v2h3v3h2v-3h3v-2h-3V8H11z M13,2.05v3.03c3.39,0.49,6,3.39,6,6.92c0,0.9-0.18,1.75-0.48,2.54l2.6,1.53 C21.68,14.83,22,13.45,22,12C22,6.82,18.05,2.55,13,2.05z M12,19c-3.87,0-7-3.13-7-7c0-3.53,2.61-6.43,6-6.92V2.05 C5.94,2.55,2,6.81,2,12c0,5.52,4.47,10,9.99,10c3.31,0,6.24-1.61,8.06-4.09l-2.6-1.53C16.17,17.98,14.21,19,12,19z"/></g></g></svg>                        
                        <svg v-else xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#fff"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M7 11v2h10v-2H7zm5-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg>
                    </span>                                       
                </div>                
            </div>   
            <div class="p-3 m-3" v-else>
                No records found.
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
.dot{
    width: 0.35rem;
    height: 0.35rem;
    border-radius: 50%;
    background: #000;
}
</style>