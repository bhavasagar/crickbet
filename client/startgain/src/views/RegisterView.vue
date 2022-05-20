<script setup>
import logo from "@/assets/logo.png";
import { onMounted, reactive, ref } from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ToastSeverity} from 'primevue/api';
import { useToast } from "primevue/usetoast";   

import { email, minLength, required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

import addToMessages from "@/helpers/AddToMessages.js"
import handleNotifications from "@/helpers/HandleNotifications.js"
import useStore from "@/stores/store.js";

const store = useStore();

const toast = useToast();
const route = useRoute();
const router = useRouter();

const userdata = reactive({
        username: '',
        email: '',
        password: '',
        checked: false
    });

const rules = {   
    username: {required,},
    email: { required, email },
    password: { required, minLengthValue: minLength(8) }
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
        body: new URLSearchParams({"username": userdata.username ,'email': userdata.email,'password': userdata.password}),
        redirect: 'follow'
    }       

    let response = await fetch(`${store.server}/register/`, options);    
    let result = await response.json();    
    console.log(result);
    if (!response.ok) {
        console.log('not ok')
        toast.add({severity: ToastSeverity.ERROR, summary: 'Registration Failed', detail: result.detail, life: 3000});
    }

    else if (response.ok) {        
        
        const message = {severity: ToastSeverity.SUCCESS, title: 'Registration Successfull', body: `Welcome, ${userdata.email}`}        
        addToMessages(message);                        

        const login = {state: 3}
        localStorage.setItem('login', JSON.stringify(login));
        router.push('/login')            
    }
} 


const handleSubmit = async (isFormValid) => {    
    submitted.value = true;
    console.log('Fill details')
    if (isFormValid) {            
        
        localStorage.setItem('email', userdata.email);                        

        await sendRequest()
        
    }
}

</script>

<template>  
    <section class="h-100">
        <!-- <Toast /> -->
        <div class="container">
            <div class="container">
                <div class="header">
                    <div class="logo">
                        <img :src="logo" alt="">
                    </div>
                </div>
                <div class="card">  
                    <form @submit.prevent="handleSubmit(!v$.$invalid)">
                        <div class="p-inputgroup">
                            <span class="p-inputgroup-addon">
                                <i class="pi pi-user"></i>
                            </span>
                            <InputText class="w-full" :class="{'p-invalid mb-0':v$.username.$invalid && submitted}" v-model="v$.username.$model" placeholder="Username" />
                        </div>               
                        <small v-if="(v$.username.$invalid && submitted) || v$.username.$pending.$response" class="p-error mb-3">{{v$.username.required.$message.replace('Value', 'Username')}}</small>
                        <div class="p-inputgroup mt-3">
                            <span class="p-inputgroup-addon">
                                <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24"><path d="M3.3 18.7V5.3H20.7V18.7ZM12 11.85 4 6.55V18H20V6.55ZM12 11 19.6 6H4.4ZM4 6.55V6V6.55V18Z"/></svg>
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
                        <span v-if="v$.password.$error && submitted">
                            <span id="password-error" v-for="(error, index) of v$.password.$errors" :key="index">
                            <small class="p-error">{{error.$message}}</small>
                            </span>
                        </span>
                        <small v-else-if="(v$.password.$invalid && submitted) || v$.password.$pending.$response" class="p-error">{{v$.password.required.$message.replace('Value', 'Password')}}</small>
                                   
                        <Button type="submit"  label="Register" class="p-button p-button-custom mt-5"  />    
                        <span class="text-create">Already have an account?<router-link :to="{ name: 'login'}">login</router-link></span>            
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
    .logo {
        width: 15rem;        
        margin: 0 auto;
    }
    .logo img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }
    section{
        background: rgb(30, 30, 30);
        width: 100vw;
        min-height: 100vh;
        height: 100%;
        display: flex;
        justify-content: center;
    }
    .container {
        min-width: 24rem;
        width: auto;
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