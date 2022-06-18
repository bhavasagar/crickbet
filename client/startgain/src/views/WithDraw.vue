<script setup>
import logo from "@/assets/logo.png";
import { onBeforeMount, onMounted, reactive, ref } from 'vue';
import {useRoute, useRouter} from 'vue-router';
import {ToastSeverity} from 'primevue/api';
import { useToast } from "primevue/usetoast";   

import { email, required } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

import addToMessages from "@/helpers/AddToMessages.js"
import handleNotifications from "@/helpers/HandleNotifications.js"
import useStore from "@/stores/store.js";
import Header from "@/components/Header.vue";

const store = useStore();

const toast = useToast();
const route = useRoute();
const router = useRouter();



const proof = ref(null);
const userdata = reactive({
        amount: '',        
        upi_id: ''
    });

const rules = {   
    amount: { required },    
    upi_id: { required },    
};

const v$ = useVuelidate(rules, userdata)

const submitted  = ref(false);

onMounted(() => {
    handleNotifications(toast);        
});

onBeforeMount(() => {
    if (!store.user) {
        store.getUserDetails();
    }
});

const sendRequest = async () => {    
    if (store.user.balance >= userdata.amount) {

        let  formdata = new FormData();
        formdata.append("user", store.user.id);
        formdata.append('amount', userdata.amount);
        formdata.append('upi_id', userdata.upi_id);        

        const options = {
            method: 'POST',
            headers: new Headers({"Authorization": `Bearer ${ JSON.parse(localStorage.getItem('credentials')).access_token }`}),
            body: formdata,
            redirect: 'follow'
            }       

        const response = await fetch(`${store.server}/withdraw/`, options);    
        const result = await response.json();    
        console.log(result);
        if (!response.ok) {
            console.log('not ok');
            toast.add({severity: ToastSeverity.ERROR, summary: 'Request Failed', detail: result.detail, life: 3000});
        }

        else if (response.ok) {                                
            toast.add({severity: ToastSeverity.SUCCESS, summary: 'Withdraw Request is submitted', detail:'Please wait until we process your money.', life: 3000});
            store.getUserDetails();
            router.push({name: 'home'});            
        }
    }
} 

const handleSubmit = async (isFormValid) => {    
    submitted.value = true;
    console.log('Fill details')
    if (isFormValid) {                            

        await sendRequest()
        return
    }
    toast.add({severity: ToastSeverity.ERROR, summary: 'Withdraw failed', detail:'Invalid details', life: 3000});
}

</script>

<template>
    <main>
        <Toast />        
        <Header />
        <section class="h-100">
            <div class="container">
                <div class="container">                    
                    <div class="card">  
                        <form @submit.prevent="handleSubmit(!v$.$invalid)">
                            <div class="p-inputgroup my-1">
                                <span class="p-inputgroup-addon">
                                    <i class="pi pi-database"></i>
                                </span>
                                <InputText class="w-full " :class="{'p-invalid mb-0':v$.amount.$invalid && submitted}" v-model="v$.amount.$model" placeholder="Amount" />
                            </div>                    
                            <span v-if="v$.amount.$error && submitted">
                                <span id="email-error" v-for="(error, index) of v$.amount.$errors" :key="index">
                                <small class="p-error">{{error.$message}}</small>
                                </span>
                            </span>
                            <small v-else-if="(v$.amount.$invalid && submitted) || v$.amount.$pending.$response" class="p-error">{{v$.amount.required.$message.replace('Value', 'amount')}}</small>
                            
                            <div class="p-inputgroup my-1">
                                <span class="p-inputgroup-addon">
                                    <i class="pi pi-at"></i>
                                </span>
                                <InputText class="w-full " :class="{'p-invalid mb-0':v$.upi_id.$invalid && submitted}" v-model="v$.upi_id.$model" placeholder="UPI ID or Paytm Number" />
                            </div>                    
                            <span v-if="v$.upi_id.$error && submitted">
                                <span id="email-error" v-for="(error, index) of v$.upi_id.$errors" :key="index">
                                <small class="p-error">{{error.$message}}</small>
                                </span>
                            </span>
                            <small v-else-if="(v$.upi_id.$invalid && submitted) || v$.upi_id.$pending.$response" class="p-error">{{v$.upi_id.required.$message.replace('Value', 'upi_id')}}</small>

                                                        
                            
                            <Button type="submit"  label="Withdraw" class="p-button p-button-custom mt-2"  />                                
                        </form>                  
                    </div>
                </div>
            </div>
        </section>  
    </main>
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
