import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/developer',
    name: 'Developer',
    component: () => import('@/views/Developer.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
