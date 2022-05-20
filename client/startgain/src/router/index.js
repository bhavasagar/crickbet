import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import MatchesView from "../views/MatchesView.vue";
import MatchDetailView from "../views/MatchDetailView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import ForgotPasswordView from "../views/ForgotPasswordView.vue";
import ResetPasswordView from "../views/ResetPasswordView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: MatchesView,
    },
    {
      path: "/match/:matchid",
      name: "match_detail",
      component: MatchDetailView,
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

export default router;
