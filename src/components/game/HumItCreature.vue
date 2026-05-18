<template>
    <svg
      class="humit-creature"
      viewBox="0 0 200 200"
      xmlns="http://www.w3.org/2000/svg"
      :class="{
        'humit-creature--loud': volume > 0.12,
        'humit-creature--boost': boost,
        'humit-creature--near-win': nearWin,
        'humit-creature--spike': volSpike > 0.5,
      }"
      :style="creatureStyle"
      aria-hidden="true"
    >
      <defs>
        <radialGradient id="humit-body" cx="40%" cy="35%" r="65%">
          <stop offset="0%" :stop-color="lightColor" />
          <stop offset="55%" :stop-color="baseColor" />
          <stop offset="100%" :stop-color="deepColor" />
        </radialGradient>
        <radialGradient id="humit-glow" cx="50%" cy="45%" r="55%">
          <stop offset="0%" :stop-color="glowStop" stop-opacity="0.55" />
          <stop offset="70%" :stop-color="glowStop2" stop-opacity="0" />
        </radialGradient>
        <filter id="humit-soft" x="-25%" y="-25%" width="150%" height="150%">
          <feGaussianBlur stdDeviation="0.6" result="b" />
          <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
        <filter id="humit-bloom" x="-40%" y="-40%" width="180%" height="180%">
          <feGaussianBlur stdDeviation="2.5" result="blur" />
          <feColorMatrix
            in="blur"
            type="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.55 0"
            result="glow"
          />
          <feMerge><feMergeNode in="glow" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
      </defs>
  
      <!-- Outer voice halo -->
      <ellipse
        cx="100"
        cy="112"
        rx="72"
        ry="68"
        fill="url(#humit-glow)"
        class="humit-creature__halo"
        :style="{ opacity: 0.25 + volume * 0.65 }"
      />
  
      <!-- Shadow -->
      <ellipse cx="100" cy="178" rx="56" ry="10" fill="rgba(0,0,0,0.18)" />
  
      <!-- Antennae (pitch-reactive) -->
      <g class="humit-creature__antenna" :style="antennaStyle">
        <path
          d="M72 58 Q68 38 62 22"
          stroke="rgba(0,0,0,0.2)"
          stroke-width="5"
          fill="none"
          stroke-linecap="round"
        />
        <path d="M72 58 Q68 38 62 22" :stroke="deepColor" stroke-width="3" fill="none" stroke-linecap="round" />
        <circle cx="62" cy="20" r="7" :fill="lightColor" stroke="rgba(255,255,255,0.5)" stroke-width="1.5" />
        <path
          d="M128 58 Q132 38 138 22"
          stroke="rgba(0,0,0,0.2)"
          stroke-width="5"
          fill="none"
          stroke-linecap="round"
        />
        <path d="M128 58 Q132 38 138 22" :stroke="deepColor" stroke-width="3" fill="none" stroke-linecap="round" />
        <circle cx="138" cy="20" r="7" :fill="lightColor" stroke="rgba(255,255,255,0.5)" stroke-width="1.5" />
      </g>
  
      <!-- Limbs back -->
      <g v-if="limbs >= 4" class="humit-creature__limb humit-creature__limb--bl" :style="limbAnim">
        <path d="M78 130 Q62 155 58 172" stroke="rgba(0,0,0,0.25)" stroke-width="10" fill="none" stroke-linecap="round" />
        <path d="M78 130 Q62 155 58 172" :stroke="deepColor" stroke-width="7" fill="none" stroke-linecap="round" />
      </g>
      <g v-if="limbs >= 4" class="humit-creature__limb humit-creature__limb--br" :style="limbAnim">
        <path d="M122 130 Q138 155 142 172" stroke="rgba(0,0,0,0.25)" stroke-width="10" fill="none" stroke-linecap="round" />
        <path d="M122 130 Q138 155 142 172" :stroke="deepColor" stroke-width="7" fill="none" stroke-linecap="round" />
      </g>
  
      <!-- Body blob -->
      <path
        :filter="volume > 0.11 ? 'url(#humit-bloom)' : 'url(#humit-soft)'"
        :d="bodyPath"
        fill="url(#humit-body)"
        stroke="rgba(255,255,255,0.38)"
        stroke-width="2"
      />
  
      <!-- Cheek blush (volume) -->
      <ellipse cx="52" cy="108" rx="14" ry="10" :fill="blushColor" :opacity="0.12 + volume * 0.45" />
      <ellipse cx="148" cy="108" rx="14" ry="10" :fill="blushColor" :opacity="0.12 + volume * 0.45" />
  
      <!-- Face -->
      <g class="humit-creature__face">
        <ellipse cx="78" cy="95" rx="eyeRx" ry="eyeRy" fill="#1a1530" />
        <ellipse cx="122" cy="95" rx="eyeRx" ry="eyeRy" fill="#1a1530" />
        <ellipse cx="80" cy="92" rx="3" ry="2.5" fill="#fff" opacity="0.75" />
        <ellipse cx="124" cy="92" rx="3" ry="2.5" fill="#fff" opacity="0.75" />
        <!-- "Sing" mouth - opens with volume -->
        <ellipse
          cx="100"
          cy="122"
          :rx="6 + volume * 14"
          :ry="3 + volume * 18"
          fill="#3d2a52"
          opacity="0.88"
        />
        <path
          v-if="volume < 0.06"
          d="M82 118 Q100 132 118 118"
          stroke="#1a1530"
          stroke-width="4"
          fill="none"
          stroke-linecap="round"
        />
      </g>
  
      <!-- Wings -->
      <g v-if="boost" class="humit-creature__wing" opacity="0.9">
        <path class="humit-creature__wing-l" d="M46 98 Q12 78 8 52 Q28 72 52 88" :fill="lightColor" opacity="0.62" />
        <path class="humit-creature__wing-r" d="M154 98 Q188 78 192 52 Q172 72 148 88" :fill="lightColor" opacity="0.62" />
      </g>
  
      <!-- Limbs front -->
      <g v-if="limbs >= 3" class="humit-creature__limb humit-creature__limb--fl" :style="limbAnimRev">
        <path d="M70 116 Q52 132 46 152" :stroke="deepColor" stroke-width="7" fill="none" stroke-linecap="round" />
      </g>
      <g v-if="limbs >= 3" class="humit-creature__limb humit-creature__limb--fr" :style="limbAnimRev">
        <path d="M130 116 Q148 132 154 152" :stroke="deepColor" stroke-width="7" fill="none" stroke-linecap="round" />
      </g>
  
      <!-- Sparkle dots when humming loud / spiking -->
      <g v-if="volume > 0.08 || volSpike > 0.35" class="humit-creature__sparkles" fill="#fff" opacity="0.95">
        <circle cx="38" cy="72" r="2.5" />
        <circle cx="162" cy="68" r="2" />
        <circle cx="170" cy="112" r="2.5" />
        <circle cx="32" cy="118" r="2" />
      </g>
    </svg>
  </template>
  
  <script setup>
  import { computed } from "vue"
  
  const props = defineProps({
    hue: { type: Number, default: 168 },
    limbs: { type: Number, default: 4 },
    roundness: { type: Number, default: 0.45 },
    wobble: { type: Number, default: 0 },
    boost: { type: Boolean, default: false },
    /** 0-1 mic / demo volume for expression */
    volume: { type: Number, default: 0 },
    /** 0-1 normalized pitch */
    pitchNorm: { type: Number, default: 0.5 },
    /** Sudden volume climb - extra sparkle / jolt class */
    volSpike: { type: Number, default: 0 },
    /** Challenge almost locked - golden anticipation */
    nearWin: { type: Boolean, default: false },
  })
  
  function hsl(h, s, l) {
    return `hsl(${h % 360}, ${s}%, ${l}%)`
  }
  
  const baseColor = computed(() => hsl(props.hue, 72, 52))
  const lightColor = computed(() => hsl(props.hue + 12, 85, 72))
  const deepColor = computed(() => hsl(props.hue - 18, 68, 38))
  const blushColor = computed(() => hsl(props.hue + 28, 92, 72))
  
  const glowStop = computed(() => hsl(props.hue + 50, 95, 78))
  const glowStop2 = computed(() => hsl(props.hue, 70, 55))
  
  const eyeRx = computed(() => 8 - props.volume * 2.5)
  const eyeRy = computed(() => 10 - props.volume * 1.5)
  
  const bodyPath = computed(() => {
    const r = props.roundness
    const squish = 1 - r * 0.35
    const breath = props.volume * 6
    const cy = 108 + props.wobble * 14
    return `
      M 100 ${56 + squish * 8 + breath * 0.15}
      C ${156 + r * 22} ${62 + squish * 6} ${174 + breath * 0.2} ${cy - 8 - breath * 0.1} ${168 + breath * 0.25} ${cy + 26}
      C ${172} ${146} ${140} ${172 + breath * 0.1} 100 ${172}
      C ${60} ${172} ${28} ${146} ${32 - breath * 0.25} ${cy + 26}
      C ${26} ${cy - 8 - breath * 0.1} ${44 + r * -22} ${62 + squish * 6} 100 ${56 + squish * 8 + breath * 0.15}
      Z
    `
  })
  
  const antennaStyle = computed(() => {
    const tilt = (props.pitchNorm - 0.5) * 22 + props.volSpike * 14
    return {
      transformOrigin: "100px 70px",
      transform: `rotate(${tilt}deg)`,
      transition: "transform 0.08s ease-out",
    }
  })
  
  const creatureStyle = computed(() => ({
    transform: `rotate(${props.wobble * 20}deg) scale(${1 + props.wobble * 0.08 + props.volume * 0.04 + props.volSpike * 0.05})`,
    transition: "transform 0.1s ease-out",
  }))
  
  const limbAnim = computed(() => ({
    transformOrigin: "100px 130px",
    animation: `humit-limb ${2.2 - props.volume * 0.6}s ease-in-out infinite`,
  }))
  const limbAnimRev = computed(() => ({
    transformOrigin: "100px 130px",
    animation: `humit-limb-rev ${2.4 - props.volume * 0.7}s ease-in-out infinite`,
  }))
  </script>
  
  <style scoped>
  .humit-creature {
    width: min(260px, 58vw);
    height: auto;
    overflow: visible;
    filter: drop-shadow(0 14px 32px rgba(0, 0, 0, 0.24));
  }
  
  .humit-creature__halo {
    transition: opacity 0.14s ease-out;
  }
  
  .humit-creature--loud {
    filter: drop-shadow(0 14px 32px rgba(0, 0, 0, 0.24)) drop-shadow(0 0 22px rgba(255, 220, 140, 0.35));
  }
  
  .humit-creature--near-win {
    filter: drop-shadow(0 14px 32px rgba(0, 0, 0, 0.24)) drop-shadow(0 0 24px rgba(255, 200, 90, 0.48));
    animation: humit-near-win-pulse 0.95s ease-in-out infinite;
  }
  
  .humit-creature--spike .humit-creature__sparkles circle {
    animation-duration: 0.45s;
  }
  
  .humit-creature__sparkles circle {
    animation: humit-twinkle 1.1s ease-in-out infinite;
  }
  
  .humit-creature__sparkles circle:nth-child(2) {
    animation-delay: 0.2s;
  }
  .humit-creature__sparkles circle:nth-child(3) {
    animation-delay: 0.45s;
  }
  .humit-creature__sparkles circle:nth-child(4) {
    animation-delay: 0.65s;
  }
  
  .humit-creature__wing-l {
    animation: humit-wing-l 0.45s ease-in-out infinite;
    transform-origin: 52px 92px;
  }
  
  .humit-creature__wing-r {
    animation: humit-wing-r 0.45s ease-in-out infinite;
    transform-origin: 148px 92px;
  }
  
  @keyframes humit-near-win-pulse {
    0%,
    100% {
      filter: drop-shadow(0 14px 32px rgba(0, 0, 0, 0.24)) drop-shadow(0 0 18px rgba(255, 200, 90, 0.35));
    }
    50% {
      filter: drop-shadow(0 14px 32px rgba(0, 0, 0, 0.24)) drop-shadow(0 0 34px rgba(120, 240, 255, 0.42));
    }
  }
  
  @keyframes humit-twinkle {
    0%,
    100% {
      opacity: 0.35;
      transform: scale(0.8);
    }
    50% {
      opacity: 1;
      transform: scale(1.15);
    }
  }
  
  @keyframes humit-wing-l {
    0%,
    100% {
      transform: rotate(-4deg);
    }
    50% {
      transform: rotate(12deg);
    }
  }
  
  @keyframes humit-wing-r {
    0%,
    100% {
      transform: rotate(4deg);
    }
    50% {
      transform: rotate(-12deg);
    }
  }
  
  @keyframes humit-limb {
    0%,
    100% {
      transform: rotate(-4deg);
    }
    50% {
      transform: rotate(6deg);
    }
  }
  
  @keyframes humit-limb-rev {
    0%,
    100% {
      transform: rotate(5deg);
    }
    50% {
      transform: rotate(-5deg);
    }
  }
  </style>
  