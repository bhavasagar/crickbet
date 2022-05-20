<script setup>
import logo from "@/assets/logo.png";
import { computed, onMounted, reactive, ref } from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ToastSeverity} from 'primevue/api';
import { useToast } from "primevue/usetoast";   
import addToMessages from "@/helpers/addToMessages.js"
import { email, minLength, required, sameAs } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import useStore from "@/stores/store.js";

const store = useStore()

const toast = useToast();
const route = useRoute();
const router = useRouter();

const userdata = reactive({
        email: '',       
    });

const checkEmail = () => {
    if (localStorage.getItem('email')) {     
        userdata.email = localStorage.getItem('email');
        return
    }    
    return 
}

onMounted(() => {
    checkEmail()
})

const rules = computed(() => {   
    return {
        email: {required, email}
    }
})
const v$ = useVuelidate(rules, userdata)

const submitted  = ref(false)    

const sendRequest = async () => { 

    console.log("loh")
    
    let options = {
        method: 'POST',
        headers: new Headers({"Content-Type": "application/json"}),        
        body: JSON.stringify({email: userdata.email}),
        redirect: 'follow'
    }       

    let response = await fetch(`${store.server}/forgot-password/`, options);    
    let result = await response.json();    

    console.log(result);

    if (!response.ok) {
        console.log('not ok')
        toast.add({severity: ToastSeverity.ERROR, summary: 'Password unchanged', detail: result.detail, life: 3000});
    }

    else if (response.ok) {        
        
        let message = {severity: ToastSeverity.SUCCESS, title: 'Password Reset Link', body: `Reset link is sent to your email`}        
        addToMessages(message);                           

        router.push(route.query.redirect || {name: 'login'})            
    }
}

const handleSubmit = async (isFormValid) => {    
    submitted.value = true;
    console.log(isFormValid, userdata.email)

    if (isFormValid) {
                
        if (userdata.email) {
            localStorage.setItem('email', userdata.email)                                    
        }       

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
                        <div class="p-inputgroup mt-3" >
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
                                   
                        <Button type="submit"  label="Send Reset Password Link" class="p-button p-button-custom mt-5"  />                            
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
        max-width: 24rem;
        min-width: 23rem;
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
