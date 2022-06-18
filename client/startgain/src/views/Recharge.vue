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
        image: null
    });

const rules = {   
    amount: { required },    
};

onBeforeMount(() => {
    if (!store.user) {
        store.getUserDetails();
    }
});

const v$ = useVuelidate(rules, userdata)

const submitted  = ref(false);
const upi = ref(null);

onMounted(() => {
    handleNotifications(toast);        
});

onBeforeMount(async () => {
    const access_token = JSON.parse(localStorage.getItem("credentials") || '{}')?.access_token;
    const options = {
        method: "GET",
        headers: new Headers({"Authorization": `Bearer ${access_token}`})
    };            
    const resp = await fetch(`${store.server}/upi/`, options);    
    const data = await resp.json();
    upi.value = data.data;
})

const sendRequest = async () => {
    // console.log(proof.files, proof.files[0]);
    if (userdata.image) {

        let  formdata = new FormData();
        formdata.append("user", store.user.id);
        formdata.append('amount', userdata.amount);
        formdata.append('proof', userdata.image);
        formdata.append( "mode", "manual");

        const options = {
            method: 'POST',
            headers: new Headers({"Authorization": `Bearer ${ JSON.parse(localStorage.getItem('credentials')).access_token }`}),
            body: formdata,
            redirect: 'follow'
            }       

        const response = await fetch(`${store.server}/recharge_api/`, options);    
        const result = await response.json();    
        console.log(result);
        if (!response.ok) {
            console.log('not ok');
            toast.add({severity: ToastSeverity.ERROR, summary: 'Request Failed', detail: result.detail, life: 3000});
        }

        else if (response.ok) {                                
            toast.add({severity: ToastSeverity.SUCCESS, summary: 'Recharge Request is submitted', detail:'Please wait until we process.', life: 3000});
            router.push({name: 'home'});
        }
    }
} 

const copy = () => {        
    navigator.clipboard.writeText(upi.value.upi_id);
}

const handleProof = event => {
    console.log(event.target, event.target.files);
    userdata.image = event.target.files[0];
}

const handleSubmit = async (isFormValid) => {    
    submitted.value = true;
    console.log('Fill details')
    if (isFormValid) {            
        
        localStorage.setItem('email', userdata.email);                                

        await sendRequest()
        return
    }
    toast.add({severity: ToastSeverity.ERROR, summary: 'Recharge failed', detail:'Invalid details', life: 3000});
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
                            <div class="p-inputgroup mb-4" @click="copy">
                                <InputText class="w-full " v-model="upi.upi_id"  disabled />
                                <span class="p-inputgroup-addon" >
                                    <i class="pi pi-copy"></i>
                                </span>
                            </div> 

                            <div class="p-inputgroup my-2">
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

                           
                            <div class="file--input my-3 flex justify-content-center card-container blue-container border-dashed border-black-500 p-3  surface-overlay ">
                                <label for="proof" class=" font-semibold border " > Proof of Payment </label>
                                <input class="form-control" type="file" id="proof" name="proof" @change="handleProof">
                            </div>
                            
                            <Button type="submit"  label="Recharge" class="p-button p-button-custom mt-2"  />                                                            
                        </form>                                          
                    </div>
                </div>
                <div class="img--details" style="width: 10rem; margin: 2rem auto;">
                    <img :src="store.server + '/../..' + upi.qr_code" style="width: 100%; height: 100%" alt="">
                </div>
            </div>
        </section>  
    </main>
</template>

<style scoped>
input[type="file"]{
    display: none;
}
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
