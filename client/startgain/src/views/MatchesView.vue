<script setup>
import logo from "@/assets/logo-cropped.png";
import { ref } from "@vue/reactivity";
import Header from "@/components/Header.vue";
import { onMounted, onBeforeMount, onUnmounted, onBeforeUnmount } from "@vue/runtime-core";
import userStore from "@/stores/store.js";
import { useRouter } from "vue-router";
import Loader from "@/components/Loader.vue";
import formatDateTime from "@/helpers/FormatDateTime";

const store = userStore();
const router = useRouter();
var fetch_matches

onBeforeMount(async () => {
    clearInterval(fetch_matches);
    await store.getCurrentMatches();
    fetch_matches = setInterval(() => {
        store.getCurrentMatches();
    }, 60*1000);
    const stored = localStorage.getItem("credentials");    
    if (!stored) {
        router.push({"name": 'Login'});
    }    
});

onBeforeUnmount(() => {
    clearInterval(fetch_matches);
    store.match = null;
});

class Game{
    constructor(name, img, link) {
        this.name = name;
        this.img = img;
        this.link= link;
    }
    getImgUrl() {
        return this.img;
    }
}

const other_games = [
    new Game("CASINO","/images/casino.jpeg",'/new'),
    new Game("COLOR TRADE","/images/colortrade.png",'/'),
    new Game("ANDHAR BAHAR","/images/andar_bahar.jpeg",'/new'),
    new Game("DRAGON TIGER","/images/dragon_tiger.jpg",'/new'),                                                     
]

console.log(store.current_matches);

</script>


<template>
    <main>
        <Loader v-if="store.current_matches ? store.meta.loading = false : store.meta.loading = true" />        
        <Header />
        <div class="container" v-if="store.current_matches">
            <router-link :to="{name: 'match_detail', params: {matchid: match.match_id} }" class="match--div px-3 py-2 block" :key="match.id" v-for="match in store.current_matches">
                <div class="match--details flex flex-column">
                    <span class="flex flex-row justify-content-between " ><span class="match--name">{{match.match_name}}</span> <span class="dot green-dot"  :class="match.not_required && 'red-dot'" >  </span> </span>
                    <span>{{formatDateTime(match.date)}}</span>
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

        <div class="other-games container ">
            <h2 class="p-2 ml-2" >Other Games</h2>
            <div class="p-2 m-2 other-games--div">
                <a class="game-info block" :href="game.link" style="position: relative; width: fit-content;"  :key="game.name" v-for="game in other_games" >
                    <div class="img--div" >
                        <img :src="game.getImgUrl()" style="height: 8.5rem; width: 8.5rem;" :alt="game.name">
                    </div>
                    <div class="img-detail--div py-1" style="position: absolute;bottom: 0.25rem;width: 100%;text-align: center;margin: 0 auto;background: #000;color: #fff;font-weight: bold;font-size: 1rem;">
                        <span style="font-weight: 600" >{{game.name}}</span>
                    </div>
                </a>
            </div>
        </div>
    </main>  
</template>


<style scoped>
.other-games--div{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 1rem;
}
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
    .other-games--div{
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        grid-gap: 1rem;
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
    width: 89%;
}
.dot{
    width: 0.75rem;
    height: 0.75rem;
    background: #000;
    position: absolute;
    right: 1rem;
    top: 1rem;
    border-radius: 100%;
}
.green-dot{
    background: #008000;
}
.red-dot{
    background: #D2042D;
}
</style>