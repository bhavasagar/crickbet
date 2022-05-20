<script setup>
import logo from "@/assets/logo-cropped.png";
import { ref } from "@vue/reactivity";
import useStore from "@/stores/store.js";

const store = useStore();

const usermenu = ref(null)
const openMenu = event => {
    console.log("Test");
    usermenu.value.toggle(event);
}

const items = [
				{
					label: 'Home',
					icon: 'pi pi-home',
					command: () => {
						this.$toast.add({severity:'success', summary:'Updated', detail:'Data Updated', life: 3000});
					}
				},
				{
					label: 'Delete',
					icon: 'pi pi-times',
					command: () => {
						this.$toast.add({ severity: 'warn', summary: 'Delete', detail: 'Data Deleted', life: 3000});
					}
				},
				{
					label: 'Change Password',
					icon: 'pi pi-external-link',
					url: 'https://vuejs.org/'
				},
				{
                    label: 'History',
                    icon: 'pi pi-upload',
                    to: '/fileupload'
                }
			]
</script>
<template>
    <span>
        <div class="header flex flex-row justify-content-between align-content-center align-items-center p-1">
            <router-link :to="{name: 'home'}" class="logo--div">
                <img :src="logo" alt="">
            </router-link>
            <div class="user-details p-3 flex flex-column align-items-end ">
                <div id="balance" style="float: right;" class="flex flex-row align-items-center">                       
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#FFFFFF"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M21 7.28V5c0-1.1-.9-2-2-2H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2v-2.28c.59-.35 1-.98 1-1.72V9c0-.74-.41-1.37-1-1.72zM20 9v6h-7V9h7zM5 19V5h14v2h-6c-1.1 0-2 .9-2 2v6c0 1.1.9 2 2 2h6v2H5z"/><circle cx="16" cy="12" r="1.5"/></svg>
                    <span class="ml-2">Bal: {store.user.balance}</span>
                </div>                
                <div id="username" style="text-align: right; width: max-content" >
                    <span class="mr-2">Exp: 0 </span>
                    <span style="cursor: pointer;"  @click="openMenu" >Username123 <span class="pi pi-angle-down"></span></span>
                    <Menu ref="usermenu" :popup="true" :model="items" />  
                </div>
            </div>
        </div>
        <div class="scroll--div">
            <div class="scroll-text">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Aut error maiores veritatis amet suscipit, tenetur repellat? Necessitatibus facilis veritatis autem quam ipsa? Ad architecto cumque esse quis placeat suscipit tenetur.
            </div>
        </div>    
        <div class="highlight">
            IPL 2022
        </div>
        <div class="menu--div ">
            <div class="menu--item">
                <router-link to="/">
                    Cricket
                </router-link>
            </div>
            <div class="menu--item">
                <router-link to="https://colortrade.startgain.in/play/">
                    Color-Trade
                </router-link>
            </div>
            <div class="menu--item">
                <router-link to="/">
                    Casino
                </router-link>
            </div>
            <div class="menu--item">
                <router-link to="/">
                    Cards
                </router-link>
            </div>
        </div>        
    </span>
</template>

<style scoped>
.menu--div{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    text-align: center;
    padding: 0.5rem 0;
    background: var(--dark-shade-2);
}
.menu--item{
    font-size: 0.85rem;
    border-right: 1px solid #dcdcdc;
    color: #fff;
}
.menu--item:last-child{
    border-right: none;
}
.menu--item a{
    text-decoration: none;
    font-weight: 700;
}
.highlight {
    font-size: 0.95rem;
    font-weight: 600;
    background: var(--dark-shade-1);
    color: #fff;
    padding: 0.25rem;
    margin: 0 auto;
    display: block;
    text-align: center;
}

.logo--div {
    width: 10rem;            
    /* margin: 0 auto; */
}
.logo--div img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
.header {
    background: var(--dark-shade-2);
    color: #fff;
    font-size: 1rem;
}
.user-details {
    float: right;
}
.scroll--div{
    width: 100vw;
    overflow: hidden;
    background: var(--dark-shade-2);
    color: #fff;
    padding: 0.25rem 0;
}
.scroll-text{
    display: inline-block;
    white-space: nowrap;
    animation: scrollText 15s infinite linear;
}
.scroll-text:hover {
  animation-play-state: paused;
}

@keyframes scrollText {
  
  from {
    transform: translateX(50%);
  }
  to {
    transform: translateX(-100%);
  }
}
</style>