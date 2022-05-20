<script setup>
import { useRouter } from "vue-router";
import useStore from "@/stores/stores.js";

const router = useRouter();
const store = useStore();

const currentPath = () => window.location.pathname;
let credentials = localStorage.getItem('credentials')
if (credentials) {
    credentials = JSON.parse(credentials);        
    router.push({name: "login", query: { redirect: currentPath }})
}
</script>
<template>
</template>