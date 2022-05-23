import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import MatchesView from "../views/MatchesView.vue";
import MatchDetailView from "../views/MatchDetailView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import ForgotPasswordView from "../views/ForgotPasswordView.vue";
import ResetPasswordView from "../views/ResetPasswordView.vue";
import ComingSoonView from "../views/ComingSoonView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: MatchesView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/match/:matchid",
      name: "match_detail",
      component: MatchDetailView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/forgot-password",
      name: "forgot_password",
      component: ForgotPasswordView,
    },
    {
      path: "/reset-password/:uid/:token",
      name: "reset_password",
      component: ResetPasswordView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/new",
      name: "new",
      component: ComingSoonView,
    },
    // {
    //   path: "/about",
    //   name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import("../views/AboutView.vue"),
    // },
  ],
});


router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    console.log("In router")
    let login_state = localStorage.getItem('login')
    if (!login_state) {
      login_state = 'login_required';
    }
    else {
      login_state = JSON.parse(login_state).state;
    }
    if (login_state == 'login_required' || login_state == 0) {
      next({ name: 'login' })
    } else {
      next() 
    }
  } else {
    next() 
  }
})

export default router;
