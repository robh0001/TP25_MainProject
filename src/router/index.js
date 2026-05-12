import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import ParentQuizPage from '../components/ParentQuizPage.vue'
import ParentDashboardPage from '../components/ParentDashboardPage.vue'
import ParentRoadmapPage from '../components/ParentRoadmapPage.vue'
import ParentNutritionToolsPage from '../components/ParentNutritionToolsPage.vue'
import KidsDashboardPage from '../components/KidsDashboardPage.vue'
import KidsGameZonePage from '../components/KidsGameZonePage.vue'
import KidsMealsPage from '../components/KidsMealsPage.vue'
import KidsStatsPage from '../components/KidsStatsPage.vue'
import KidsWinsPage from '../components/KidsWinsPage.vue'
import ParentEntry from '../components/ParentEntry.vue'
import { useFamilyPlanStore } from '../stores/familyPlanStore'

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
    meta: { requiresParentProfile: true },
  },
  {
    path: '/parent-roadmap',
    name: 'ParentRoadmap',
    component: ParentRoadmapPage,
    meta: { requiresParentProfile: true },
  },
  {
    path: '/parent-nutrition-tools',
    name: 'ParentNutritionTools',
    component: ParentNutritionToolsPage,
    meta: { requiresParentProfile: true },
  },
  {
    path: '/kids-dashboard',
    alias: '/young-person-dashboard',
    name: 'kids-dashboard',
    component: KidsDashboardPage,
  },
  {
    path: '/kids-games',
    alias: '/kids-game-zone',
    name: 'kids-game-zone',
    component: KidsGameZonePage,
  },
  {
    path: '/kids-meals',
    name: 'kids-meals',
    component: KidsMealsPage,
  },
  {
    path: '/kids-stats',
    name: 'kids-stats',
    component: KidsStatsPage,
  },
  {
    path: '/kids-wins',
    name: 'kids-wins',
    component: KidsWinsPage,
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

router.beforeEach((to) => {
  if (!to.meta.requiresParentProfile) {
    return true
  }

  const { state } = useFamilyPlanStore()

  const hasParentProfile =
    Boolean(state.username) &&
    (
      Boolean(state.childName) ||
      Boolean(state.child_name) ||
      Boolean(state.dailyPlan) ||
      Boolean(state.roadmapProgress)
    )

  if (hasParentProfile) {
    return true
  }

  return {
    path: '/parent-entry',
    query: {
      redirect: to.fullPath,
      reason: 'missing-parent-profile',
    },
  }
})

export default router