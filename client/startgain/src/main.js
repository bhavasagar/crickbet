import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import PrimeVue from 'primevue/config';
import Toast from 'primevue/toast';
import Button from 'primevue/button';
import ToastService from 'primevue/toastservice';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Checkbox from 'primevue/checkbox';
import InlineMessage from 'primevue/inlinemessage';
import Menu from 'primevue/menu';
import Dialog from 'primevue/dialog';
import InputNumber from 'primevue/inputnumber';

import "primevue/resources/themes/saga-blue/theme.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";
import "primeflex/primeflex.css";


const app = createApp(App);

app.use(createPinia());
app.use(PrimeVue, {ripple: true});
app.use(router);
app.use(ToastService);


app.component('Menu', Menu);
app.component('Button', Button);
app.component('Toast', Toast);
app.component('InputText', InputText);
app.component('Password', Password);
app.component('Checkbox', Checkbox);
app.component('InlineMessage', InlineMessage);
app.component('Dialog', Dialog);
app.component('InputNumber', InputNumber);

app.mount("#app");
