<template>
  <header class="kids-topbar">
    <RouterLink to="/kids-dashboard" class="brand-link">HealthyKids</RouterLink>

    <div class="page-chip">{{ pageLabel }}</div>

    <div class="topbar-right">
      <div class="topbar-links">
        <RouterLink to="/kids-dashboard" class="topbar-link">Home</RouterLink>
        <RouterLink to="/kids-games" class="topbar-link">Game zone</RouterLink>
        <RouterLink
          to="/parent-dashboard"
          class="topbar-link topbar-link--parent"
          aria-label="Leave kids area — open parent home"
        >
          <span class="parent-link-icon" aria-hidden="true" v-html="iconParentDoor"></span>
          <span class="parent-link-text">Parents</span>
        </RouterLink>
      </div>

      <button
        type="button"
        class="theme-toggle-btn"
        :aria-pressed="isDarkMode"
        @click="$emit('toggle-theme')"
      >
        <span class="theme-svg" aria-hidden="true" v-html="isDarkMode ? iconSun : iconMoon"></span>
        <span class="theme-label">{{ isDarkMode ? "Light" : "Dark" }}</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router"

defineProps({
  pageLabel: {
    type: String,
    required: true,
  },
  isDarkMode: {
    type: Boolean,
    default: false,
  },
})

defineEmits(["toggle-theme"])

const iconMoon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>`
const iconSun = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2.2M12 19.8V22M4.9 4.9l1.5 1.5M17.6 17.6l1.5 1.5M2 12h2.2M19.8 12H22M4.9 19.1l1.5-1.5M17.6 6.4l1.5-1.5"/></svg>`
const iconParentDoor = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M13 21h8v-9h-8z"/><path d="M3 21V4a1 1 0 0 1 1-1h7l5 5v13"/><circle cx="16.5" cy="13.5" r="1" fill="currentColor"/></svg>`
</script>

<style scoped>
.kids-topbar {
  margin: 0 auto 14px;
  padding: 6px 0 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.brand-link,
.topbar-link {
  text-decoration: none;
}

.brand-link {
  font-family: "Baloo 2", cursive;
  font-size: 1.12rem;
  font-weight: 800;
  color: var(--kids-ink, #18192b);
}

.page-chip {
  min-height: 32px;
  padding: 0 13px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--kids-top-chip-bg, rgba(255, 255, 255, 0.82));
  border: 1px solid var(--kids-top-chip-edge, rgba(255, 255, 255, 0.88));
  box-shadow: 0 10px 28px rgba(24, 25, 43, 0.07);
  color: var(--kids-top-chip-text, var(--kids-muted, #445066));
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.topbar-links {
  display: flex;
  align-items: center;
  gap: 7px;
}

.topbar-link {
  min-height: 34px;
  padding: 0 11px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  background: var(--kids-top-link-bg, rgba(255, 255, 255, 0.78));
  border: 1px solid var(--kids-top-link-edge, rgba(238, 239, 245, 0.95));
  box-shadow: 0 10px 28px rgba(24, 25, 43, 0.06);
  color: var(--kids-top-link-text, var(--kids-soft, #4b5577));
  font-size: 0.76rem;
  font-weight: 700;
  transition: transform 0.18s ease, color 0.18s ease, box-shadow 0.18s ease;
}

.topbar-link:hover {
  transform: translateY(-1px);
  color: var(--kids-ink, #18192b);
  box-shadow: 0 12px 34px rgba(24, 25, 43, 0.1);
}

.topbar-link--parent {
  gap: 5px;
  padding-left: 9px;
  padding-right: 11px;
}

.parent-link-icon {
  width: 15px;
  height: 15px;
  display: inline-flex;
  flex-shrink: 0;
}

.parent-link-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.theme-toggle-btn {
  min-height: 34px;
  padding: 0 11px;
  border-radius: 999px;
  border: 1px solid var(--kids-theme-btn-edge, rgba(238, 239, 245, 1));
  background: linear-gradient(
    145deg,
    var(--kids-theme-btn-a, rgba(255, 255, 255, 0.95)),
    var(--kids-theme-btn-b, rgba(246, 245, 255, 0.92))
  );
  color: var(--kids-soft, #4b5577);
  font-size: 0.73rem;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  box-shadow: 0 10px 28px rgba(24, 25, 43, 0.07);
  transition: transform 0.18s ease, filter 0.18s ease;
}

.theme-toggle-btn:hover {
  transform: translateY(-1px);
  filter: brightness(1.03);
}

.theme-svg {
  width: 16px;
  height: 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.theme-svg :deep(svg) {
  width: 100%;
  height: 100%;
}

.theme-label {
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

@media (max-width: 740px) {
  .kids-topbar {
    flex-wrap: wrap;
    justify-content: center;
    text-align: center;
  }

  .brand-link {
    width: 100%;
    font-size: 1.05rem;
  }

  .topbar-right {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
  }

  .topbar-link {
    font-size: 0.71rem;
  }

  .theme-label {
    display: none;
  }

  .parent-link-text {
    display: none;
  }

  .topbar-link--parent {
    padding: 0 10px;
  }
}
</style>
