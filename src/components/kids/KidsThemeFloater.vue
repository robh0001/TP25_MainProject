<template>
    <button
      type="button"
      class="kids-theme-floater"
      :class="{ 'is-dark': isDarkMode }"
      :aria-pressed="isDarkMode"
      aria-label="Toggle light or dark mode"
      @click="$emit('toggle-theme')"
    >
      <span class="floater-glow" aria-hidden="true"></span>
      <span class="floater-track" aria-hidden="true">
        <span class="thumb">
          <svg
            v-if="isDarkMode"
            class="thumb-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.2"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
          </svg>
          <svg
            v-else
            class="thumb-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.2"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="4" />
            <path d="M12 2v2.4M12 19.6V22M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M2 12h2.4M19.6 12H22M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6" />
          </svg>
        </span>
        <span class="cloud cloud-a" aria-hidden="true"></span>
        <span class="cloud cloud-b" aria-hidden="true"></span>
        <span class="star star-a" aria-hidden="true"></span>
        <span class="star star-b" aria-hidden="true"></span>
        <span class="star star-c" aria-hidden="true"></span>
      </span>
      <span class="floater-label">{{ isDarkMode ? "Night" : "Day" }}</span>
    </button>
  </template>
  
  <script setup>
  defineProps({
    isDarkMode: {
      type: Boolean,
      default: false,
    },
  })
  
  defineEmits(["toggle-theme"])
  </script>
  
  <style scoped>
  .kids-theme-floater {
    position: fixed;
    top: max(18px, env(safe-area-inset-top, 0px));
    right: max(18px, env(safe-area-inset-right, 0px));
    z-index: 60;
    padding: 6px 14px 6px 6px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border: none;
    border-radius: 999px;
    cursor: pointer;
    font-family: "Baloo 2", "DM Sans", sans-serif;
    font-weight: 800;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #103a2b;
    background: linear-gradient(135deg, #ffe7a8, #ffd060 60%, #6bd1ff);
    box-shadow: 0 14px 32px rgba(255, 176, 32, 0.32);
    transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s ease, filter 0.25s ease;
  }
  
  .kids-theme-floater:hover {
    transform: translateY(-2px) scale(1.04);
    filter: brightness(1.04);
    box-shadow: 0 18px 38px rgba(255, 176, 32, 0.4);
  }
  
  .kids-theme-floater.is-dark {
    color: #e9eaff;
    background: linear-gradient(135deg, #1c1f4d, #2c1d5f 55%, #6c4bff);
    box-shadow: 0 14px 32px rgba(76, 60, 180, 0.45);
  }
  
  .kids-theme-floater.is-dark:hover {
    box-shadow: 0 18px 38px rgba(108, 75, 255, 0.5);
  }
  
  .floater-glow {
    position: absolute;
    inset: -6px;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 50%, rgba(255, 213, 96, 0.55), transparent 60%);
    filter: blur(8px);
    z-index: -1;
    animation: floaterGlow 3.4s ease-in-out infinite alternate;
  }
  
  .kids-theme-floater.is-dark .floater-glow {
    background: radial-gradient(circle at 70% 50%, rgba(108, 75, 255, 0.55), transparent 60%);
  }
  
  @keyframes floaterGlow {
    from { opacity: 0.65; transform: scale(1); }
    to   { opacity: 1;    transform: scale(1.06); }
  }
  
  .floater-track {
    position: relative;
    width: 52px;
    height: 28px;
    border-radius: 999px;
    background: linear-gradient(135deg, #8fd9ff, #c9efff);
    box-shadow: inset 0 2px 6px rgba(20, 50, 100, 0.18);
    overflow: hidden;
    transition: background 0.4s ease;
  }
  
  .kids-theme-floater.is-dark .floater-track {
    background: linear-gradient(135deg, #0d1240, #2b1e6e);
  }
  
  .thumb {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: radial-gradient(circle at 30% 30%, #fff7d0, #ffcd5c);
    color: #c66c00;
    box-shadow: 0 0 12px rgba(255, 196, 80, 0.7), inset 0 0 0 1px rgba(255, 255, 255, 0.5);
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.4s ease, color 0.4s ease, box-shadow 0.4s ease;
    animation: thumbWobble 2.8s ease-in-out infinite;
  }
  
  .kids-theme-floater.is-dark .thumb {
    transform: translateX(24px);
    background: radial-gradient(circle at 30% 30%, #e0e5ff, #9eaaff 60%, #6c4bff);
    color: #fff;
    box-shadow: 0 0 14px rgba(108, 75, 255, 0.7), inset 0 0 0 1px rgba(255, 255, 255, 0.18);
  }
  
  @keyframes thumbWobble {
    0%, 100% { rotate: -4deg; }
    50%      { rotate: 6deg; }
  }
  
  .thumb-icon {
    width: 14px;
    height: 14px;
  }
  
  .cloud {
    position: absolute;
    background: rgba(255, 255, 255, 0.92);
    border-radius: 999px;
    opacity: 1;
    transition: opacity 0.4s ease;
    animation: cloudDrift 8s ease-in-out infinite;
  }
  
  .cloud-a {
    width: 14px;
    height: 8px;
    top: 6px;
    right: 6px;
  }
  
  .cloud-b {
    width: 10px;
    height: 6px;
    top: 14px;
    right: 14px;
    animation-delay: 1.4s;
  }
  
  .kids-theme-floater.is-dark .cloud {
    opacity: 0;
  }
  
  @keyframes cloudDrift {
    0%, 100% { transform: translateX(0); }
    50%      { transform: translateX(-6px); }
  }
  
  .star {
    position: absolute;
    background: #ffffff;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    opacity: 0;
    filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.85));
  }
  
  .star-a { top: 6px;  left: 10px; }
  .star-b { top: 16px; left: 18px; width: 2px; height: 2px; }
  .star-c { top: 8px;  left: 22px; }
  
  .kids-theme-floater.is-dark .star {
    opacity: 1;
    animation: starTwinkle 2.4s ease-in-out infinite;
  }
  
  .kids-theme-floater.is-dark .star-b { animation-delay: 0.6s; }
  .kids-theme-floater.is-dark .star-c { animation-delay: 1.2s; }
  
  @keyframes starTwinkle {
    0%, 100% { opacity: 0.35; transform: scale(0.7); }
    50%      { opacity: 1;    transform: scale(1.4); }
  }
  
  .floater-label {
    line-height: 1;
  }
  
  @media (max-width: 640px) {
    .kids-theme-floater {
      padding: 5px 12px 5px 5px;
      font-size: 0.7rem;
    }
    .floater-track {
      width: 46px;
      height: 24px;
    }
    .thumb {
      width: 20px;
      height: 20px;
    }
    .kids-theme-floater.is-dark .thumb {
      transform: translateX(22px);
    }
  }
  </style>
  