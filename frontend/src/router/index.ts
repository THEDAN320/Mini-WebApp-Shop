import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../modules/main/pages/MainPage.vue')
    }
    // {
    //   path: '/cart',
    //   name: 'cart',
    //   component: CartView
    // }
  ]
})

export default router
