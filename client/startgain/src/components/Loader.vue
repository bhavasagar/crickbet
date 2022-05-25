<template>
  <div class="loader--div" v-if="store.meta.loading" >
        <div class="loader">       
        </div>
    </div>
</template>

<script setup>
import useStore from "@/stores/store.js";
import { onBeforeMount } from "@vue/runtime-core";

const store = useStore();

onBeforeMount(() => {
    store.meta.loading = true;
    console.log('loading');
})

</script>

<style scoped>

.loader--div{
  width: 100vw;
  height: 100vh;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  z-index: 100001;
}
.loader{
  width: 5rem;
  height: 5rem;
  border: 0.5rem solid #868686;
  border-top-color: #000;
  animation: rotate 1s cubic-bezier(0.165, 0.84, 0.44, 1) 500ms infinite;
  border-radius: 50%;
}
@keyframes rotate {
  0% {
      transform: rotateZ(0deg);
  }
  100% {
      transform: rotateZ(360deg);
  }
}   
</style>