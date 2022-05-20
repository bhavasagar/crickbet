<script setup>
import { RouterLink, RouterView } from "vue-router";
import handleNotifications from "@/helpers/HandleNotifications.js"
import { onMounted } from "@vue/runtime-core";

import { useToast } from "primevue/usetoast";   

const toast = useToast();

onMounted(() => {
    handleNotifications(toast);   
});
</script>

<template> 
  <span>
    <Toast style="width: var(--toast-width)" />
    <RouterView />
  </span> 
</template>

<style>
@import "@/assets/base.css";

@media (max-width: 500px) {
  :root { 
    --toast-width: 85vw; 
  }
}
#app {  
  margin: 0 auto;  
  font-weight: normal;
}



</style>
