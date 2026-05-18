<!--
  AccessibilityTools.vue

  Floating accessibility widget for HealthyKids.

  Main features:
  - Opens and closes an accessibility tools panel.
  - Lets users increase, decrease, or reset global text size.
  - Shows the current text zoom percentage.
  - Provides a Hover to Read toggle for reading page text aloud.
  - Shows active and reading status banners.
  - Allows users to stop speech output.

  Accessibility:
  - Uses aria-labels, aria-live, role="switch", and aria-checked.
  - Uses native buttons for keyboard access.
  - Hides decorative icons with aria-hidden="true".
  - Uses data-hover-read-ignore="true" so the widget is not read aloud.

  Related composables:
  - useTextResize
  - useHoverToRead
  - useSpeechSynthesis
  - useHoverSpeechReader
-->

<template>
  <!-- Main accessibility widget wrapper -->
  <div class="hk-a11y-widget" data-hover-read-ignore="true">
    <!-- Floating button shown when the panel is closed -->
    <button
      v-if="!isOpen"
      type="button"
      class="hk-a11y-fab"
      :class="{ 'hk-a11y-fab--active': isHoverToReadEnabled || isSpeaking }"
      aria-label="Open accessibility tools panel"
      title="Accessibility tools"
      @click="isOpen = true"
    >
      <span class="hk-a11y-fab-icon" aria-hidden="true">
        <svg
          class="hk-a11y-svg"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="1.4"
          />
          <circle
            cx="12"
            cy="6.7"
            r="1.8"
            fill="currentColor"
          />
          <path
            d="M7.5 10.2C9 11 10.5 11.3 12 11.3C13.5 11.3 15 11 16.5 10.2"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
          />
          <path
            d="M12 11.2V16.5"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
          />
          <path
            d="M9.4 18.5L12 16L14.6 18.5"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <path
            d="M9.1 11.4L7.5 15"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
          />
          <path
            d="M14.9 11.4L16.5 15"
            stroke="currentColor"
            stroke-width="1.7"
            stroke-linecap="round"
          />
        </svg>
      </span>

      <!-- Small indicator when any reading feature is active -->
      <span
        v-if="isHoverToReadEnabled || isSpeaking"
        class="hk-a11y-fab-active-dot"
        aria-hidden="true"
      ></span>
    </button>

    <!-- Accessibility tools panel -->
    <section
      v-else
      id="hk-accessibility-panel"
      class="hk-a11y-panel"
      aria-label="Accessibility tools"
    >
      <div class="hk-a11y-panel-top">
        <div>
          <p class="hk-a11y-panel-kicker">Accessibility</p>
          <h2 class="hk-a11y-panel-title">Tools</h2>
        </div>

        <button
          type="button"
          class="hk-a11y-close-btn"
          aria-label="Close accessibility tools panel"
          @click="isOpen = false"
        >
          x
        </button>
      </div>

      <!-- Text resizing section -->
      <div class="hk-a11y-section">
        <h3 class="hk-a11y-section-title">Text size</h3>

        <div class="hk-a11y-zoom-value-row">
          <span class="hk-a11y-zoom-label">Current size</span>

          <span
            class="hk-a11y-zoom-value"
            :aria-label="`Current text size is ${zoomPercent} percent`"
          >
            {{ zoomPercent }}%
          </span>
        </div>

        <div
          class="hk-a11y-zoom-controls"
          role="group"
          aria-label="Text resizing controls"
        >
          <button
            type="button"
            class="hk-a11y-zoom-btn"
            aria-label="Zoom out text size"
            :disabled="!canZoomOut"
            @click="handleZoomOut"
          >
            <span class="hk-a11y-zoom-icon" aria-hidden="true">-</span>
            <span>Zoom out</span>
          </button>

          <button
            type="button"
            class="hk-a11y-zoom-btn hk-a11y-reset-btn"
            aria-label="Reset text size to default"
            :disabled="!canReset"
            @click="handleReset"
          >
            <span class="hk-a11y-zoom-icon" aria-hidden="true">&#x21BA;</span>
            <span>Reset</span>
          </button>

          <button
            type="button"
            class="hk-a11y-zoom-btn"
            aria-label="Zoom in text size"
            :disabled="!canZoomIn"
            @click="handleZoomIn"
          >
            <span class="hk-a11y-zoom-icon" aria-hidden="true">+</span>
            <span>Zoom in</span>
          </button>
        </div>
      </div>

      <!-- Hover-to-read section -->
      <div
        class="hk-a11y-hover-read"
        :class="{ 'hk-a11y-hover-read--active': isHoverToReadEnabled }"
      >
        <div class="hk-a11y-hover-read-copy">
          <div class="hk-a11y-hover-read-heading-row">
            <h3>Hover to Read</h3>

            <span
              v-if="isHoverToReadEnabled"
              class="hk-a11y-active-pill"
              aria-label="Hover to Read is active"
            >
              Active
            </span>
          </div>

          <p>
            Turn this on, then hover over page text to make it easier to read.
          </p>
        </div>

        <button
          type="button"
          class="hk-a11y-toggle-switch"
          :class="{ 'hk-a11y-toggle-switch--on': isHoverToReadEnabled }"
          role="switch"
          :aria-checked="isHoverToReadEnabled"
          :aria-label="hoverToReadAriaLabel"
          @click="toggleHoverToRead"
        >
          <span class="hk-a11y-toggle-status" aria-hidden="true">
            {{ isHoverToReadEnabled ? 'ON' : 'OFF' }}
          </span>

          <span class="hk-a11y-toggle-thumb" aria-hidden="true"></span>
        </button>
      </div>
    </section>

    <!-- Status banner shown when hover-to-read is active -->
    <div
      v-if="isHoverToReadEnabled"
      class="hk-a11y-hover-read-banner"
      role="status"
      aria-live="polite"
      data-hover-read-ignore="true"
    >
      <span class="hk-a11y-hover-read-banner-icon" aria-hidden="true">Aa</span>
      <span>Hover to Read is active</span>
    </div>

    <!-- Status banner shown while speech is active -->
    <div
      v-if="isSpeaking"
      class="hk-a11y-speaking-banner"
      role="status"
      aria-live="polite"
      data-hover-read-ignore="true"
    >
      <span class="hk-a11y-hover-read-banner-icon" aria-hidden="true">🔊</span>
      <span>Reading aloud</span>

      <button
        type="button"
        class="hk-a11y-speaking-stop"
        aria-label="Stop reading aloud"
        data-hover-read-ignore="true"
        @mousedown.stop.prevent
        @click.stop.prevent="handleStopSpeech"
      >
        Stop
      </button>
    </div>
  </div>
</template>

<script setup>
// Vue utilities
import { computed, ref } from 'vue'

// Accessibility composables
import { useTextResize } from '../composables/useTextResize'
import { useHoverToRead } from '../composables/useHoverToRead'
import { useSpeechSynthesis } from '../composables/useSpeechSynthesis'
import { useHoverSpeechReader } from '../composables/useHoverSpeechReader'

// Enables hover speech reading behaviour globally for supported page elements.
useHoverSpeechReader()

// Controls whether the floating accessibility panel is open or closed.
const isOpen = ref(false)

// Text resizing state and actions.
const {
  zoomPercent,
  canZoomIn,
  canZoomOut,
  canReset,
  zoomIn,
  zoomOut,
  resetZoom,
} = useTextResize()

// Hover-to-read state and action.
const {
  isHoverToReadEnabled,
  toggleHoverToRead,
} = useHoverToRead()

// Speech synthesis state and action.
const {
  isSpeaking,
  stopSpeech,
} = useSpeechSynthesis()

// Builds the accessible label for the hover-to-read switch based on its current state.
const hoverToReadAriaLabel = computed(() => (
  isHoverToReadEnabled.value
    ? 'Turn off Hover to Read'
    : 'Turn on Hover to Read'
))

/**
 * Increases the global text size using the text resize composable.
 */
function handleZoomIn() {
  zoomIn()
}

/**
 * Decreases the global text size using the text resize composable.
 */
function handleZoomOut() {
  zoomOut()
}

/**
 * Resets the global text size back to the default value.
 */
function handleReset() {
  resetZoom()
}

/**
 * Stops the current speech output and clears any queued browser speech.
 */
function handleStopSpeech() {
  stopSpeech()

  // Safety fallback to immediately cancel any browser speech queue.
  if (typeof window !== 'undefined' && window.speechSynthesis) {
    window.speechSynthesis.cancel()
  }
}
</script>