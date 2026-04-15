import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import ParentQuizPage from '../components/ParentQuizPage.vue'
import ParentDashboardPage from '../components/ParentDashboardPage.vue'
import YoungPersonDashboardPage from '../components/YoungPersonDashboardPage.vue'
import ParentEntry from '../components/ParentEntry.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
  },
  {
    path: '/parent-quiz',
    name: 'parent-quiz',
    component: ParentQuizPage,
  },
  {
    path: '/parent-dashboard',
    name: 'ParentDashboard',
    component: ParentDashboardPage,
  },
  {
    path: '/young-person-dashboard',
    name: 'young-person-dashboard',
    component: YoungPersonDashboardPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router