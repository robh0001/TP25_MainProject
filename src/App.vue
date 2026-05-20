<template>
  <div class="page-shell">
    <MainNavBar v-if="showMainNavBar" />

    <RouterView v-slot="{ Component, route }">
      <Transition name="page-slide" mode="out-in">
        <component :is="Component" :key="route.fullPath" />
      </Transition>
    </RouterView>

    <AccessibilityToolsPanel />
    <ChatbotWidget />
  </div>
</template>


<style scoped>
:global(.page-slide-enter-active),
:global(.page-slide-leave-active) {
  transition: opacity 0.16s ease, transform 0.16s ease;
}

:global(.page-slide-enter-from),
:global(.page-slide-leave-to) {
  opacity: 0;
  transform: translateY(4px);
}

:global(.page-slide-enter-to),
:global(.page-slide-leave-from) {
  opacity: 1;
  transform: translateY(0);
}
</style>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import AccessibilityToolsPanel from './components/AccessibilityToolsPanel.vue'
import ChatbotWidget from '@/components/ChatbotWidget.vue'
import MainNavBar from './components/MainNavBar.vue'

const route = useRoute()

const routesWithoutMainNav = [
  '/kids-dashboard',
  '/kids-game-zone'
]

const showMainNavBar = computed(() => {
  return !routesWithoutMainNav.includes(route.path)
})
</script>

<style scoped>
:global(.page-slide-enter-active),
:global(.page-slide-leave-active) {
  transition: opacity 0.16s ease, transform 0.16s ease;
}

:global(.page-slide-enter-from),
:global(.page-slide-leave-to) {
  opacity: 0;
  transform: translateY(4px);
}

:global(.page-slide-enter-to),
:global(.page-slide-leave-from) {
  opacity: 1;
  transform: translateY(0);
}
</style>