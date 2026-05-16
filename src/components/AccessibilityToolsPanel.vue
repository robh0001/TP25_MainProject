<template>
    <div class="hk-a11y-widget" data-hover-read-ignore="true">
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

        <span
          v-if="isHoverToReadEnabled || isSpeaking"
          class="hk-a11y-fab-active-dot"
          aria-hidden="true"
        ></span>
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
          <h2 class="hk-a11y-panel-title">Tools</h2>
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

      <div class="hk-a11y-section">
        <h3 class="hk-a11y-section-title">Text size</h3>

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
          :aria-label="
            isHoverToReadEnabled
              ? 'Turn off Hover to Read'
              : 'Turn on Hover to Read'
          "
          @click="toggleHoverToRead"
          @keydown.enter.prevent="toggleHoverToRead"
          @keydown.space.prevent="toggleHoverToRead"
        >
          <span class="hk-a11y-toggle-status" aria-hidden="true">
            {{ isHoverToReadEnabled ? 'ON' : 'OFF' }}
          </span>
          <span class="hk-a11y-toggle-thumb"></span>
        </button>
      </div>
    </section>

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
import { ref } from 'vue'
import { useTextResize } from '../composables/useTextResize'
import { useHoverToRead } from '../composables/useHoverToRead'
import { useSpeechSynthesis } from '../composables/useSpeechSynthesis'
import { useHoverSpeechReader } from '../composables/useHoverSpeechReader'

useHoverSpeechReader()

const isOpen = ref(false)


const {
  zoomPercent,
  canZoomIn,
  canZoomOut,
  canReset,
  zoomIn,
  zoomOut,
  resetZoom,
} = useTextResize()


const {
  isHoverToReadEnabled,
  toggleHoverToRead,
} = useHoverToRead()

const {
  isSupported,
  isSpeaking,
  stopSpeech,
} = useSpeechSynthesis()

function handleZoomIn() {
  zoomIn()
}

function handleZoomOut() {
  zoomOut()
}

function handleReset() {
  resetZoom()
}

function handleStopSpeech() {
  stopSpeech()

  if (typeof window !== 'undefined' && window.speechSynthesis) {
    window.speechSynthesis.cancel()
  }
}

</script>