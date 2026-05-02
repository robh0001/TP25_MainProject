<template>
  <div
    class="kids-route-shell"
    :class="{ 'kids-route-shell--dark': isDarkMode }"
  >
    <div class="kids-route-shell-bg" aria-hidden="true" />
    <div class="kids-route-shell-inner">
      <KidsPageTopbar
        :page-label="pageLabel"
        :is-dark-mode="isDarkMode"
        @toggle-theme="toggleDarkMode"
      />
      <slot />
      <KidsBottomNav />
    </div>
  </div>
</template>

<script setup>
import KidsPageTopbar from "./kids/KidsPageTopbar.vue"
import KidsBottomNav from "./kids/KidsBottomNav.vue"
import { provideKidsTheme } from "../composables/useKidsTheme.js"

defineProps({
  pageLabel: {
    type: String,
    required: true,
  },
})

const { isDarkMode, toggleDarkMode } = provideKidsTheme()
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap");

/* Match dashboard home tokens for light + dark (KidsDashboardPage). */
.kids-route-shell {
  --kids-bg: #f4f5fb;
  --kids-ink: #18192b;
  --kids-muted: #445066;
  --kids-soft: #5a6278;
  --kids-surface: rgba(255, 255, 255, 0.92);
  --kids-border: rgba(255, 255, 255, 0.78);
  --kids-card-shadow: 0 18px 44px rgba(24, 25, 43, 0.08);

  --kids-top-chip-bg: rgba(255, 255, 255, 0.82);
  --kids-top-chip-edge: rgba(255, 255, 255, 0.88);
  --kids-top-chip-text: var(--kids-muted);

  --kids-top-link-bg: rgba(255, 255, 255, 0.78);
  --kids-top-link-edge: rgba(238, 239, 245, 0.95);
  --kids-top-link-text: var(--kids-soft);

  --kids-theme-btn-a: rgba(255, 255, 255, 0.95);
  --kids-theme-btn-b: rgba(246, 245, 255, 0.92);
  --kids-theme-btn-edge: rgba(238, 239, 245, 1);
}

.kids-route-shell--dark {
  --kids-bg: #090e1f;
  --kids-ink: #f2f7ff;
  --kids-muted: rgba(224, 232, 255, 0.92);
  --kids-soft: rgba(198, 208, 240, 0.88);
  --kids-surface: rgba(18, 22, 43, 0.94);
  --kids-border: rgba(143, 154, 227, 0.26);
  --kids-card-shadow: 0 18px 50px rgba(3, 7, 23, 0.55);

  --kids-top-chip-bg: rgba(255, 255, 255, 0.1);
  --kids-top-chip-edge: rgba(255, 255, 255, 0.14);
  --kids-top-chip-text: rgba(226, 234, 255, 0.95);

  --kids-top-link-bg: rgba(255, 255, 255, 0.07);
  --kids-top-link-edge: rgba(255, 255, 255, 0.14);
  --kids-top-link-text: rgba(224, 232, 255, 0.9);

  --kids-theme-btn-a: rgba(255, 255, 255, 0.1);
  --kids-theme-btn-b: rgba(255, 255, 255, 0.05);
  --kids-theme-btn-edge: rgba(255, 255, 255, 0.16);
}

.kids-route-shell {
  position: relative;
  min-height: 100vh;
  font-family: "DM Sans", sans-serif;
  color: var(--kids-ink);
  background: var(--kids-bg);
  overflow-x: hidden;
  padding-bottom: 88px;
}

.kids-route-shell-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.kids-route-shell:not(.kids-route-shell--dark) .kids-route-shell-bg {
  background-image:
    radial-gradient(circle at 20% 18%, rgba(59, 158, 255, 0.09) 0%, transparent 50%),
    radial-gradient(circle at 82% 22%, rgba(155, 114, 255, 0.08) 0%, transparent 48%),
    radial-gradient(circle at 52% 96%, rgba(44, 201, 122, 0.06) 0%, transparent 42%);
}

.kids-route-shell--dark .kids-route-shell-bg {
  background-image:
    radial-gradient(circle at 18% 16%, rgba(59, 158, 255, 0.16) 0%, transparent 45%),
    radial-gradient(circle at 84% 20%, rgba(155, 114, 255, 0.14) 0%, transparent 40%),
    radial-gradient(circle at 48% 100%, rgba(255, 126, 179, 0.1) 0%, transparent 38%);
}

.kids-route-shell-inner {
  position: relative;
  z-index: 1;
  width: min(1120px, 100%);
  margin: 0 auto;
  padding: 14px min(22px, 4vw) 0;
}
</style>
