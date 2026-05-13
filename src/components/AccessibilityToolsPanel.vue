<template>
    <div class="hk-a11y-widget">
      <button
        v-if="!isOpen"
        type="button"
        class="hk-a11y-fab"
        aria-label="Open accessibility tools panel"
        @click="isOpen = true"
      >
        <span class="hk-a11y-fab-icon" aria-hidden="true">Aa</span>
      </button>
  
      <section
        v-else
        id="hk-accessibility-panel"
        class="hk-a11y-panel"
        aria-label="Accessibility tools"
      >
        <div class="hk-a11y-panel-top">
          <div>
            <p class="hk-a11y-panel-kicker">Accessibility</p>
            <h2 class="hk-a11y-panel-title">Text size</h2>
          </div>
  
          <button
            type="button"
            class="hk-a11y-close-btn"
            aria-label="Close accessibility tools panel"
            @click="isOpen = false"
          >
            ×
          </button>
        </div>
  
        <div class="hk-a11y-zoom-value-row">
          <span class="hk-a11y-zoom-label">Current size</span>
          <span class="hk-a11y-zoom-value" aria-label="Current text size">
            {{ zoomPercent }}%
          </span>
        </div>
  
        <div class="hk-a11y-zoom-controls" aria-label="Text resizing controls">
          <button
            type="button"
            class="hk-a11y-zoom-btn"
            aria-label="Zoom out text size"
            @click="handleZoomOut"
          >
            <span class="hk-a11y-zoom-icon" aria-hidden="true">-</span>
            <span>Zoom out</span>
          </button>
  
          <button
            type="button"
            class="hk-a11y-zoom-btn hk-a11y-reset-btn"
            aria-label="Reset text size to default"
            @click="handleReset"
          >
            <span class="hk-a11y-zoom-icon" aria-hidden="true">&#x21BA;</span>
            <span>Reset</span>
          </button>
  
          <button
            type="button"
            class="hk-a11y-zoom-btn"
            aria-label="Zoom in text size"
            @click="handleZoomIn"
          >
            <span class="hk-a11y-zoom-icon" aria-hidden="true">+</span>
            <span>Zoom in</span>
          </button>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue'
  
  const isOpen = ref(false)
  const zoomLevel = ref(0)
  
  const zoomPercent = computed(() => 100 + zoomLevel.value * 10)
  
  function handleZoomIn() {
    if (zoomLevel.value >= 3) return
    zoomLevel.value += 1
  }
  
  function handleZoomOut() {
    if (zoomLevel.value <= -2) return
    zoomLevel.value -= 1
  }
  
  function handleReset() {
    zoomLevel.value = 0
  }
  </script>