<template>
    <div class="kbuddy" :class="[size]" aria-hidden="true">
      <svg viewBox="0 0 240 260" class="kbuddy-svg" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="kbBody" cx="36%" cy="30%" r="80%">
            <stop offset="0%" stop-color="#ffd2c9" />
            <stop offset="44%" stop-color="#ff6f72" />
            <stop offset="100%" stop-color="#b8243f" />
          </radialGradient>
          <radialGradient id="kbCheek" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#ff8aa0" stop-opacity="0.95" />
            <stop offset="100%" stop-color="#ff8aa0" stop-opacity="0" />
          </radialGradient>
          <linearGradient id="kbLeaf" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#7be08a" />
            <stop offset="100%" stop-color="#2fb255" />
          </linearGradient>
          <radialGradient id="kbHighlight" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#fff" stop-opacity="0.95" />
            <stop offset="100%" stop-color="#fff" stop-opacity="0" />
          </radialGradient>
          <radialGradient id="kbBoot" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#3a3aff" />
            <stop offset="100%" stop-color="#1a1052" />
          </radialGradient>
  
          <clipPath id="kbEyeClipLeft">
            <ellipse cx="92" cy="128" rx="13" ry="14" />
          </clipPath>
          <clipPath id="kbEyeClipRight">
            <ellipse cx="148" cy="128" rx="13" ry="14" />
          </clipPath>
          <clipPath id="kbMouthClip">
            <path d="M88 158 Q120 198 152 158 Q152 178 120 184 Q88 178 88 158 Z" />
          </clipPath>
        </defs>
  
        <g class="kbuddy-shadow">
          <ellipse cx="120" cy="240" rx="64" ry="9" fill="#000" opacity="0.18" />
        </g>
  
        <g class="kbuddy-character">
          <g class="kbuddy-leg kbuddy-leg-left">
            <rect x="86" y="200" width="14" height="22" rx="6" fill="#b8243f" />
            <ellipse cx="92" cy="226" rx="14" ry="9" fill="url(#kbBoot)" />
          </g>
          <g class="kbuddy-leg kbuddy-leg-right">
            <rect x="140" y="200" width="14" height="22" rx="6" fill="#b8243f" />
            <ellipse cx="148" cy="226" rx="14" ry="9" fill="url(#kbBoot)" />
          </g>
  
          <g class="kbuddy-body">
            <g class="kbuddy-stem">
              <path d="M119 38 Q123 18 142 14" stroke="#5e3b1f" stroke-width="7" stroke-linecap="round" fill="none" />
              <path
                class="kbuddy-leaf"
                d="M140 14 Q172 0 182 24 Q170 34 150 30 Q146 24 140 14 Z"
                fill="url(#kbLeaf)"
              />
              <path d="M150 18 Q160 22 168 26" stroke="#1f7a3a" stroke-width="1.5" fill="none" opacity="0.7" />
            </g>
  
            <ellipse class="kbuddy-belly" cx="120" cy="136" rx="86" ry="80" fill="url(#kbBody)" />
            <ellipse cx="86" cy="92" rx="26" ry="14" fill="url(#kbHighlight)" opacity="0.7" />
  
            <g class="kbuddy-cheeks">
              <circle cx="78" cy="158" r="13" fill="url(#kbCheek)" />
              <circle cx="162" cy="158" r="13" fill="url(#kbCheek)" />
            </g>
  
            <g class="kbuddy-brows">
              <path class="brow brow-left"  d="M76 108 Q92 100 104 106" stroke="#3a0d18" stroke-width="4" fill="none" stroke-linecap="round" />
              <path class="brow brow-right" d="M136 106 Q148 100 164 108" stroke="#3a0d18" stroke-width="4" fill="none" stroke-linecap="round" />
            </g>
  
            <g class="kbuddy-eye kbuddy-eye-left">
              <ellipse cx="92" cy="128" rx="13" ry="14" fill="#fff" />
              <g clip-path="url(#kbEyeClipLeft)">
                <g class="kbuddy-pupil-wrap">
                  <circle class="kbuddy-pupil" cx="92" cy="130" r="7" fill="#1a1024" />
                  <circle cx="94" cy="127" r="2.2" fill="#fff" />
                </g>
              </g>
            </g>
  
            <g class="kbuddy-eye kbuddy-eye-right">
              <ellipse cx="148" cy="128" rx="13" ry="14" fill="#fff" />
              <g clip-path="url(#kbEyeClipRight)">
                <g class="kbuddy-pupil-wrap">
                  <circle class="kbuddy-pupil" cx="148" cy="130" r="7" fill="#1a1024" />
                  <circle cx="150" cy="127" r="2.2" fill="#fff" />
                </g>
              </g>
            </g>
  
            <g class="kbuddy-mouth">
              <path
                class="kbuddy-mouth-shape"
                d="M88 158 Q120 198 152 158 Q152 178 120 184 Q88 178 88 158 Z"
                fill="#3a0d18"
              />
              <g clip-path="url(#kbMouthClip)">
                <path class="kbuddy-teeth" d="M104 156 L116 156 L116 168 L104 168 Z" fill="#fff" opacity="0.92" />
                <path
                  class="kbuddy-tongue"
                  d="M108 172 Q120 188 132 172 Q132 184 120 186 Q108 184 108 172 Z"
                  fill="#ff6a8a"
                />
              </g>
            </g>
  
            <g class="kbuddy-arm kbuddy-arm-left">
              <path d="M44 158 Q22 158 14 184" stroke="#b8243f" stroke-width="12" stroke-linecap="round" fill="none" />
              <circle cx="12" cy="186" r="11" fill="#ff6f72" />
              <circle cx="12" cy="186" r="3.6" fill="#3a0d18" opacity="0.55" />
            </g>
            <g class="kbuddy-arm kbuddy-arm-right">
              <path d="M196 158 Q218 152 226 128" stroke="#b8243f" stroke-width="12" stroke-linecap="round" fill="none" />
              <circle cx="228" cy="126" r="11" fill="#ff6f72" />
              <circle cx="228" cy="126" r="3.6" fill="#3a0d18" opacity="0.55" />
            </g>
          </g>
  
          <g class="kbuddy-heart" aria-hidden="true">
            <text x="34" y="80" font-size="20">&#10084;&#65039;</text>
          </g>

            <g class="kbuddy-sparkles" aria-hidden="true">
            <text x="20" y="60" class="kbuddy-sparkle s1">&#10024;</text>
            <text x="200" y="50" class="kbuddy-sparkle s2">&#11088;</text>
            <text x="208" y="208" class="kbuddy-sparkle s3">&#128171;</text>
            <text x="24" y="208" class="kbuddy-sparkle s4">&#127775;</text>
            </g>
        </g>
      </svg>
    </div>
  </template>
  
  <script setup>
  defineProps({
    size: {
      type: String,
      default: "md",
    },
  })
  </script>  