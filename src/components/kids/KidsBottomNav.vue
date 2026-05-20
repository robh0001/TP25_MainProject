<template>
  <nav class="kids-bottom-nav" aria-label="Kids dashboard navigation">
    <RouterLink
      v-for="item in items"
      :key="item.id"
      :to="item.to"
      class="kids-bottom-link"
      :class="{ active: isActive(item) }"
      @click="onItemClick(item, $event)"
    >
      <span class="kids-bottom-icon" v-html="item.icon"></span>
      <span class="kids-bottom-label">{{ item.label }}</span>
      <span v-if="item.badge" class="kids-bottom-dot"></span>
    </RouterLink>
  </nav>
</template>

<script setup>
import { RouterLink, useRoute } from "vue-router"
import { useGameLaunch } from "../../composables/useGameLaunch.js"

const route = useRoute()
const { startGameLaunch } = useGameLaunch()

const items = [
  {
    id: "home",
    label: "Home",
    to: "/kids-dashboard",
    match: ["/kids-dashboard", "/young-person-dashboard"],
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
  },
  {
    id: "games",
    label: "Games",
    to: "/kids-games",
    match: ["/kids-games", "/kids-game-zone"],
    badge: true,
    launchKey: "games",
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M12 12h.01"/><path d="M7 10v4"/><path d="M5 12h4"/><path d="M17 11h.01"/><path d="M19 13h.01"/></svg>`,
  },
]

function isActive(item) {
  return item.match.includes(route.path)
}

function onItemClick(item, event) {
  if (item.launchKey && !isActive(item)) {
    event.preventDefault()
    startGameLaunch(item.launchKey)
  }
}
</script>

<style scoped>
.kids-bottom-nav {
  position: fixed;
  left: 50%;
  bottom: max(12px, env(safe-area-inset-bottom, 0px));
  z-index: 40;
  width: min(480px, calc(100vw - 16px));
  transform: translateX(-50%);
  padding: 6px 7px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 4px;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(28, 30, 54, 0.98), rgba(22, 24, 45, 0.98));
  border: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 0 14px 40px rgba(11, 13, 28, 0.3);
  backdrop-filter: blur(18px);
}

.kids-bottom-link {
  position: relative;
  min-height: 48px;
  padding: 4px 4px;
  border-radius: 13px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: rgba(227, 229, 249, 0.5);
  text-decoration: none;
  transition: transform 0.22s ease, background 0.22s ease, color 0.22s ease, box-shadow 0.22s ease;
}

.kids-bottom-link:hover {
  transform: translateY(-2px);
  color: rgba(255, 255, 255, 0.9);
}

.kids-bottom-link.active {
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.kids-bottom-icon {
  width: 20px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.kids-bottom-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.kids-bottom-label {
  font-size: 0.54rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.kids-bottom-dot {
  position: absolute;
  top: 10px;
  right: calc(50% - 26px);
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #ff6b8b;
  box-shadow: 0 0 8px rgba(255, 107, 139, 0.8);
}

@media (max-width: 700px) {
  .kids-bottom-nav {
    bottom: max(8px, env(safe-area-inset-bottom, 0px));
    width: calc(100vw - 12px);
    padding: 6px 6px;
    gap: 3px;
    border-radius: 18px;
  }

  .kids-bottom-link {
    min-height: 44px;
    border-radius: 11px;
    gap: 3px;
  }

  .kids-bottom-icon {
    width: 18px;
    height: 18px;
  }

  .kids-bottom-label {
    font-size: 0.48rem;
  }

  .kids-bottom-dot {
    top: 8px;
    right: calc(50% - 22px);
  }
}
</style>
