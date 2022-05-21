<script setup>
import logo from "@/assets/logo-cropped.png";
import { ref } from "@vue/reactivity";
import Header from "@/components/Header.vue";
import { onMounted, onBeforeMount, onUnmounted, onBeforeUnmount } from "@vue/runtime-core";
import userStore from "@/stores/store.js";

const store = userStore();
var fetch_matches

onBeforeMount(() => {
    clearInterval(fetch_matches);
    let data = store.getCurrentMatches();
    fetch_matches = setInterval(() => {
        let data = store.getCurrentMatches();
    }, 60*1000)    
});

onBeforeUnmount(() => {
    clearInterval(fetch_matches);
});

console.log(store.current_matches);

</script>


<template>
    <main>
        <Header />
        <div class="container" v-if="store.current_matches">
            <router-link :to="{name: 'match_detail', params: {matchid: match.match_id} }" class="match--div px-3 py-2 block" :key="match.id" v-for="match in store.current_matches">
                <div class="match--details flex flex-column">
                    <span class="match--name">{{match.match_name}}</span>
                    <span>{{match.date}}</span>
                </div>
                <div class="match--ratios">
                    <div class="match-ratio text-center">
                        <span class="block my-1">Back</span>
                        <div class="ratio-values">
                            <span>{{match.gold.ratio_a}}</span>
                            <span>{{match.gold.ratio_b}}</span>
                        </div>
                    </div>
                    <div class="match-ratio text-center">
                        <span class="block my-1">Lay</span>
                        <div class="ratio-values">
                            <span>{{match.diamond.ratio_a}}</span>
                            <span>{{match.diamond.ratio_b}}</span>
                        </div>
                    </div>
                    <div class="match-ratio text-center">
                        <span class="block my-1">Toss</span>
                        <div class="ratio-values">
                            <span>{{match.tossbet_ratio.ratio_a}}</span>
                            <span>{{match.tossbet_ratio.ratio_b}}</span>
                        </div>
                    </div>
                    <!-- <div class="match-ratio text-center">
                        <span class="block my-1">Over</span>
                        <div class="ratio-values">
                            <span>{{match.gold.ratio_a}}</span>
                            <span>{{match.gold.ratio_b}}</span>
                        </div>
                    </div>
                    <div class="match-ratio text-center">
                        <span class="block my-1">Ball</span>
                        <div class="ratio-values">
                            <span>{{match.gold.ratio_a}}</span>
                            <span>{{match.gold.ratio_b}}</span>
                        </div>
                    </div>
                    <div class="match-ratio text-center">
                        <span class="block my-1">BookMaker</span>
                        <div class="ratio-values">
                            <span>{{match.gold.ratio_a}}</span>
                            <span>{{match.gold.ratio_b}}</span>
                        </div>
                    </div> -->
                </div>
            </router-link>
        </div>   
        <div class="my-3" v-else>
            <span class="p-2" > No live matches are running.</span>
        </div>
    </main>  
</template>


<style scoped>
a{
    text-decoration: none;
}
.container{
    background: #fafafa;
}
.match--ratios{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
}
@media (min-width: 900px) {
    .match--ratios{     
        grid-template-columns: repeat(6, 1fr);
    }    
}
.match-ratio > span {
    font-weight: 600;
}
.ratio-values {
    display: flex;
    flex-direction: row;
}
.ratio-values span{
    /* padding: 0.35rem 1.  75rem; */
    font-weight: 700;
    width: 50%;
}
.ratio-values span:nth-child(2n){    
    background: var(--lay-bg);
}
.ratio-values span:nth-child(2n+1){    
    background: var(--back-bg);
}
.match--div{
    border-bottom: 1px solid #d0d0d0;
}
.match--name{
    font-size: 1.1rem;
    font-weight: 600;
}
</style>