<template>
  <div class="container">
      <div class="p-3 ml-3">
          Logout
      </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";



const router = useRouter();

router.push({name: "home"})

localStorage.clear();

</script>

<style>

</style>