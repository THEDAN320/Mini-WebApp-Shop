import { createRouter, createWebHistory } from 'vue-router'
import AdminPanel from '../modules/admin/pages/adminPanel.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../modules/main/pages/MainPage.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminPanel
    }
  ]
})

export default router
