import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import store from "@/store";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    meta: {
      layout: "main",
    },
    component: () => import("@/modules/main/pages/MainPage.vue"),
  },
  {
    path: "/admin",
    name: "admin",
    component: () => import("@/modules/admin/pages/adminPanel.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
