import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

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
  {
    path: "/admin/users",
    name: "users",
    component: () => import("@/modules/admin/pages/usersPanel.vue"),
  },
  {
    path: "/admin/orders",
    name: "orders",
    component: () => import("@/modules/admin/pages/ordersPanel.vue"),
  },
  {
    path: "/catalog",
    name: "catalog",
    component: () => import("@/modules/catalog/pages/CatalogPage.vue"),
    meta: {
      title: "Каталог",
      layout: "default",
    },
  },
  {
    path: "/cart",
    name: "cart",
    component: () => import("@/modules/cart/pages/CartPage.vue"),
  },
  {
    path: "/orders",
    name: "order-history",
    component: () => import("@/modules/orders/pages/OrderHistoryPage.vue"),
    meta: {
      title: "История заказов",
      layout: "default",
    },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
