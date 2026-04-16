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
    path: '/parent-entry',
    name: 'ParentEntry',
    component: ParentEntry,
  },
  {
    path: '/parent-quiz',
    name: 'ParentQuiz',
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
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0, left: 0 }
  },
})

export default router