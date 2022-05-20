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
 
const isEmailAvailable = ref(false);
const label = ref('Reset Password');


const userdata = reactive({        
        password: '',
        confirmPassword: ''
    });

const passwordMinLength = 8    

const rules = computed(() => {   
    return {
        password: { required, minLengthValue: minLength(passwordMinLength) },
        confirmPassword: { required, sameAsRawValue: sameAs(userdata.password) }
    }
})
const v$ = useVuelidate(rules, userdata)

const submitted  = ref(false)    

const sendRequest = async () => { 
  
    let options = {
        method: 'PATCH',
        headers: new Headers({"Content-Type": "application/json"}), 
        body: JSON.stringify({password1: userdata.password, password2: userdata.confirmPassword, uid: route.params.uid, token: route.params.token}),
        redirect: 'follow'
    }       

    let response = await fetch(`${store.server}/reset-password/${route.params.uid}/${route.params.token}/`, options);    
    let result = await response.json();    
    
    if (!response.ok) {
        console.log('not ok')
        toast.add({severity: ToastSeverity.ERROR, summary: 'Password unchanged', detail: result.detail, life: 3000});
    }

    else if (response.ok) {        
        
        let message = {severity: ToastSeverity.SUCCESS, title: 'Password Updated', body: `Password changed successfully`}        
        addToMessages(message);                           

        router.push(route.query.redirect || {name: 'login'})            
    }

}

const handleSubmit = async (isFormValid) => {    
    submitted.value = true;

    if (isFormValid) {

        if (!userdata.password || !userdata.confirmPassword) {
            toast.add({severity: ToastSeverity.WARN, summary: 'Invalid data', detail:'Please fill all the details', life: 3000});
            return
        } 

        await sendRequest()
    }
}
</script>

<template>  
    <section class="h-100">        
        <div class="container">
            <div class="container">
                <div class="header">
                    <div class="logo">
                        <img :src="logo" alt="">
                    </div>
                </div>
                <div class="card">  
                    <form @submit.prevent="handleSubmit(!v$.$invalid)">                                          
                                                
                        <div class="mb-3" >
                            <label for="password1" class="block text-900 font-medium text-xl mb-2">Password</label>
                            <Password id="password1" v-model="v$.password.$model" placeholder="Type your New Password here.." :toggleMask="true" class="w-full" :class="{'p-invalid':v$.password.$invalid && submitted} " inputClass="w-full" inputStyle="padding:1rem"></Password>
                            <small v-if="(v$.password.$invalid && submitted) || v$.password.$pending.$response" class="p-error mb-3">{{v$.password.required.$message.replace('Value', 'Password')}}</small>
                        </div>

                        <div class="mb-3">
                            <label for="password1" class="block text-900 font-medium text-xl mb-2">Confirm Password</label>
                            <Password id="password1" v-model="v$.confirmPassword.$model" placeholder="Confirm your New Password here.." :toggleMask="true" class="w-full" :class="{'p-invalid':v$.confirmPassword.$invalid && submitted} " inputClass="w-full" inputStyle="padding:1rem"></Password>
                            <small v-if="(v$.confirmPassword.$invalid && submitted) || v$.confirmPassword.$pending.$response" class="p-error mb-3">{{v$.confirmPassword.required.$message.replace('Value', 'Confirm Password')}}</small>
                        </div>                        
                                   
                        <Button type="submit"  :label="label" class="p-button p-button-custom mt-5"  />                            
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
