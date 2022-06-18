<script setup>
import logo from "@/assets/logo.png";
import { onMounted, reactive, ref } from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ToastSeverity} from 'primevue/api';
import { useToast } from "primevue/usetoast";   

import { email, required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

import addToMessages from "@/helpers/AddToMessages.js"
import handleNotifications from "@/helpers/HandleNotifications.js"
import useStore from "@/stores/store.js";

const store = useStore();

const toast = useToast();
const route = useRoute();
const router = useRouter();

const userdata = reactive({
        email: '',
        password: '',
        checked: false
    });

const rules = {   
    email: { required },
    password: { required }
};

const v$ = useVuelidate(rules, userdata)

const submitted  = ref(false);


const updateEmail = () => {
    let email = localStorage.getItem('email')
    if (email) {
        userdata.email = email;
    }    
}

const checkLogin = () => {
    console.log('check Login')
    let login = JSON.parse(localStorage.getItem('login'));
    if (login) { 
        (login.state === 1) && router.push({name: 'home'})            
    }
}

onMounted(() => {
    handleNotifications(toast);
    updateEmail();
    checkLogin();
});

const sendRequest = async () => {
    let options = {
        method: 'POST',
        headers: new Headers({"Content-Type": "application/x-www-form-urlencoded"}),
        body: new URLSearchParams({'email': userdata.email,'password': userdata.password}),
        redirect: 'follow'
    }       

    let response = await fetch(`${store.server}/login/`, options);    
    let result = await response.json();    
    console.log(result);
    if (!response.ok) {
        console.log('not ok')
        toast.add({severity: ToastSeverity.ERROR, summary: 'Login Failed', detail: result.detail, life: 3000});
    }

    else if (response.ok && result.access_token) {        
        
        // let message = {severity: ToastSeverity.SUCCESS, title: 'Login Successfull', body: `Welcome back, ${userdata.email}`}        
        // addToMessages(message);        
        
        let credentials = {access_token: result.access_token, refresh_token: result.refresh_token, email: userdata.email}        
        localStorage.setItem('credentials', JSON.stringify(credentials))

        let login = {state: 1}
        localStorage.setItem('login', JSON.stringify(login));

        toast.add({severity: ToastSeverity.SUCCESS, summary: 'Login Successfull', detail:'Welcome back', life: 3000});

        router.push(route.query.redirect || '/')            
    }
} 

const handleSubmit = async (isFormValid) => {    
    submitted.value = true;
    console.log('Fill details')
    if (isFormValid) {            
        
        localStorage.setItem('email', userdata.email);                                

        await sendRequest()
        return
    }
    toast.add({severity: ToastSeverity.ERROR, summary: 'Login failed', detail:'Invalid details', life: 3000});
}

</script>

<template>  
    <section class="h-100">
        <div class="container">
            <div class="container">
                <div class="header flex-row">
                    <div class="logo--div">
                        <img :src="logo" alt="">
                    </div>
                </div>
                <div class="card">  
                    <form @submit.prevent="handleSubmit(!v$.$invalid)">
                        <div class="p-inputgroup">
                            <span class="p-inputgroup-addon">
                                <i class="pi pi-user"></i>
                            </span>
                            <InputText class="w-full " :class="{'p-invalid mb-0':v$.email.$invalid && submitted}" v-model="v$.email.$model" placeholder="Email" />
                        </div>                    
                        <span v-if="v$.email.$error && submitted">
                            <span id="email-error" v-for="(error, index) of v$.email.$errors" :key="index">
                            <small class="p-error">{{error.$message}}</small>
                            </span>
                        </span>
                        <small v-else-if="(v$.email.$invalid && submitted) || v$.email.$pending.$response" class="p-error">{{v$.email.required.$message.replace('Value', 'Email')}}</small>
                        <div class="p-inputgroup mt-3">
                            <span class="p-inputgroup-addon">
                                <i class="pi pi-key"></i>
                            </span>
                            <InputText class="w-full " type="password" placeholder="Password" v-model="v$.password.$model" :class="{'p-invalid':v$.password.$invalid && submitted}" :toggleMask="true" />
                        </div>    
                        <small v-if="(v$.password.$invalid && submitted) || v$.password.$pending.$response" class="p-error mb-3">{{v$.password.required.$message.replace('Value', 'Password')}}</small>
                        <span class="text-forgot mt-3"><a href="https://colortrade.startgain.in/accounts/password/reset/">Forgot Password</a></span>            
                        <Button type="submit"  label="Login" class="p-button p-button-custom mt-2"  />    
                        <span class="text-create">Don't you have an account? <a href="https://colortrade.startgain.in/accounts/signup/">create one</a></span>            
                    </form>                  
                </div>
            </div>
        </div>
	</section>  
</template>

<style scoped>
a, a:visited {
    color: inherit;        
}    
.text-create{
    text-align: center;
    margin: 0.5rem auto;
    width: 100%;
    display: block;
}
.text-forgot {
    float: right;
}
.logo--div {
    width: 15rem;        
    margin: 0 auto;
}
.logo--div img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
section{
    background: rgb(30, 30, 30);
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
}
.container {
    width: calc(100vw - 2rem);
    max-width: 28rem;
    margin: 3rem auto;      
}
.card{
    width: 100%;
    background: #fff;
    padding: 3rem 0.7rem;
    border-radius: 3px;
}    
/* .p-inputgroup {
    margin-bottom: 1rem;
} */    
</style>

<style>
.p-button-custom {
    background: rgb(21, 21, 21)  !important;    
    width: 99% !important;
    margin: 0.5rem auto !important;
    border-radius: 5px !important;
    font-size: 1.1rem !important;
    border: 1px solid rgb(50, 50, 50) !important;
}
.p-button-custom:enabled:active, .p-button-custom:enabled:hover {
    background: rgb(21, 21, 21) !important;  
    color: #ffffff !important;
    border-color: rgb(50, 50, 50) !important;  
}
.p-button:focus {
    box-shadow: 0 0 0 0.2rem rgba(208, 207, 207, 0.5) !important;
}
</style>