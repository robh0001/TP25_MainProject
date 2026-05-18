<!--
  ChatbotWidget.vue

  Floating Healthy Buddy chatbot for the HealthyKids website.

  Main features:
  - Shows a draggable chatbot button.
  - Opens a chat panel within the screen bounds.
  - Changes character style on kids routes.
  - Saves the widget position in localStorage.
  - Shows starter suggestions for common questions.
  - Sends user messages to the chatbot API and displays replies.
  - Shows a typing indicator while waiting for a response.

  API requirement:
  - Requires VITE_CHATBOT_API.
  - Sends messages using POST /chat.
  - Shows a fallback message if the API URL is missing or the request fails.

  Accessibility:
  - Uses aria-labels and aria-live for chat controls and messages.
  - Uses native buttons and form input for keyboard access.
  - Hides decorative icons with aria-hidden="true".
-->

<template>
  <!-- Main draggable chatbot wrapper -->
  <div
    class="chatbot-wrapper"
    :class="{ dragging: isDragging }"
    :style="{
      left: `${position.x}px`,
      top: `${position.y}px`
    }"
  >
    <!-- Chat panel transition -->
    <transition name="chat-slide">
      <!-- Chatbot panel shown when the widget is open -->
      <section
        v-if="isOpen"
        class="chatbot-panel"
        :style="panelStyle"
        aria-label="Healthy Buddy chatbot panel"
      >
        <!-- Chatbot panel header -->
        <header class="chatbot-header">
          <div class="bot-avatar" :class="{ 'bot-avatar--kids': isKidsRoute }">
            <KidsBuddyCharacter v-if="isKidsRoute" size="sm" />

            <img
              v-else
              :src="healthyBuddyIcon"
              alt="Healthy Buddy chatbot"
              class="header-character-img"
            />
          </div>

          <div class="header-text">
            <h3>Healthy Buddy</h3>
            <p>Your friendly guide for food, sleep and activity</p>
          </div>

          <button
            type="button"
            class="close-btn"
            aria-label="Close chatbot"
            @click="isOpen = false"
          >
            x
          </button>
        </header>

        <!-- Chat message list -->
        <div
          ref="messagesContainer"
          class="chatbot-messages"
          aria-live="polite"
          aria-label="Chat messages"
        >
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="['message-row', message.role]"
          >
            <div class="message-bubble">
              {{ message.text }}
            </div>
          </div>

          <!-- Typing indicator shown while waiting for the API response -->
          <div v-if="loading" class="message-row bot" aria-label="Healthy Buddy is typing">
            <div class="message-bubble typing">
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
            </div>
          </div>
        </div>

        <!-- Starter suggestions shown only at the beginning of the chat -->
        <div
          v-if="messages.length <= 1"
          class="suggestions"
          aria-label="Suggested chatbot questions"
        >
          <button
            type="button"
            @click="useSuggestion('My child refuses vegetables. What can I do?')"
          >
            Refuses vegetables
          </button>

          <button
            type="button"
            @click="useSuggestion('How much screen time is okay?')"
          >
            Screen time
          </button>

          <button
            type="button"
            @click="useSuggestion('How can I improve my childs sleep routine?')"
          >
            Sleep routine
          </button>
        </div>

        <!-- User message input form -->
        <form class="chatbot-input-area" @submit.prevent="sendMessage">
          <input
            v-model="userMessage"
            type="text"
            placeholder="Ask Healthy Buddy..."
            aria-label="Type a message for Healthy Buddy"
            :disabled="loading"
          />

          <button
            type="submit"
            aria-label="Send message"
            :disabled="loading || !userMessage.trim()"
          >
            <span aria-hidden="true">&#10148;</span>
          </button>
        </form>
      </section>
    </transition>

    <!-- Floating chatbot toggle button -->
    <button
      type="button"
      class="chatbot-toggle"
      :class="{ active: isOpen, 'chatbot-toggle--kids': isKidsRoute && !isOpen }"
      aria-label="Open HealthyKids assistant"
      @pointerdown="startDrag"
      @click="handleToggleClick"
    >
      <template v-if="!isOpen">
        <KidsBuddyCharacter v-if="isKidsRoute" size="lg" />

        <img
          v-else
          :src="healthyBuddyIcon"
          alt="Healthy Buddy chatbot"
          class="floating-character-img"
          draggable="false"
        />
      </template>

      <span v-else class="close-icon" aria-hidden="true">x</span>
    </button>
  </div>
</template>

<script setup>
// Vue utilities
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'

// Vue Router
import { useRoute } from 'vue-router'

// Assets and components
import healthyBuddyIcon from '@/assets/healthy-buddy-chatbot.png'
import KidsBuddyCharacter from '@/components/KidsBuddyCharacter.vue'

// Gives access to the current route so the widget can change on kids pages.
const route = useRoute()

// Detects whether the current page is a kids or young-person route.
const isKidsRoute = computed(() => {
  const p = route.path || ''

  return (
    p.startsWith('/kids') ||
    p.startsWith('/young-person') ||
    p === '/kids-dashboard'
  )
})

// Controls whether the chatbot panel is open.
const isOpen = ref(false)

// Stores the user's current input text.
const userMessage = ref('')

// Tracks whether the chatbot is waiting for an API response.
const loading = ref(false)

// Reference to the messages container for automatic scrolling.
const messagesContainer = ref(null)

// Backend API base URL from the Vite environment variables.
const CHATBOT_API_BASE_URL = import.meta.env.VITE_CHATBOT_API

// Widget and panel layout constants.
const WIDGET_SIZE = 130
const PANEL_WIDTH = 390
const PANEL_HEIGHT = 570
const SCREEN_PADDING = 16
const PANEL_GAP = 12
const DRAG_THRESHOLD = 6
const NAV_OFFSET_TOP = 96

// Initial chatbot conversation.
const messages = ref([
  {
    role: 'bot',
    text: "Hi! I'm Healthy Buddy. Ask me a quick question about food, sleep, screen time or activity."
  }
])

// Initial floating widget position.
const position = ref({
  x: window.innerWidth - WIDGET_SIZE - 24,
  y: NAV_OFFSET_TOP
})

// Dragging state.
const isDragging = ref(false)
const didDrag = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const dragOffset = ref({ x: 0, y: 0 })

// Calculates the chatbot panel position so it opens within the screen.
const panelStyle = computed(() => {
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight

  const actualPanelWidth = Math.min(
    PANEL_WIDTH,
    viewportWidth - SCREEN_PADDING * 2
  )

  const actualPanelHeight = Math.min(
    PANEL_HEIGHT,
    viewportHeight - SCREEN_PADDING * 2
  )

  let left = 0
  let top = 0

  const iconCenterX = position.value.x + WIDGET_SIZE / 2
  const iconCenterY = position.value.y + WIDGET_SIZE / 2

  /*
    Horizontal placement:
    - If the icon is on the right half, open the panel to the left.
    - If the icon is on the left half, open the panel to the right.
  */
  if (iconCenterX > viewportWidth / 2) {
    left = -actualPanelWidth + WIDGET_SIZE
  } else {
    left = 0
  }

  /*
    Vertical placement:
    - If the icon is on the lower half, open the panel above.
    - If the icon is on the upper half, open the panel below.
  */
  if (iconCenterY > viewportHeight / 2) {
    top = -actualPanelHeight - PANEL_GAP
  } else {
    top = WIDGET_SIZE + PANEL_GAP
  }

  /*
    Clamp the panel so it never leaves the screen.
    The panel is absolutely positioned inside the wrapper, so viewport clamping
    is converted into wrapper-relative left and top values.
  */
  const panelViewportLeft = position.value.x + left
  const panelViewportTop = position.value.y + top

  if (panelViewportLeft < SCREEN_PADDING) {
    left += SCREEN_PADDING - panelViewportLeft
  }

  if (panelViewportLeft + actualPanelWidth > viewportWidth - SCREEN_PADDING) {
    left -= panelViewportLeft + actualPanelWidth - (viewportWidth - SCREEN_PADDING)
  }

  if (panelViewportTop < SCREEN_PADDING) {
    top += SCREEN_PADDING - panelViewportTop
  }

  if (panelViewportTop + actualPanelHeight > viewportHeight - SCREEN_PADDING) {
    top -= panelViewportTop + actualPanelHeight - (viewportHeight - SCREEN_PADDING)
  }

  return {
    width: `${actualPanelWidth}px`,
    height: `${actualPanelHeight}px`,
    left: `${left}px`,
    top: `${top}px`
  }
})

// Restores the saved widget position and registers resize handling when mounted.
onMounted(() => {
  const savedPosition = localStorage.getItem('healthyBuddyPosition')

  if (savedPosition) {
    try {
      const parsed = JSON.parse(savedPosition)
      position.value = keepInsideScreen(parsed.x, parsed.y)
    } catch {
      position.value = keepInsideScreen(position.value.x, position.value.y)
    }
  } else {
    position.value = keepInsideScreen(position.value.x, position.value.y)
  }

  window.addEventListener('resize', handleResize)
})

// Removes global event listeners when the component is destroyed.
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  removeDragListeners()
})

/**
 * Keeps the chatbot widget inside the screen whenever the browser is resized.
 * Also saves the corrected position to localStorage.
 */
function handleResize() {
  position.value = keepInsideScreen(position.value.x, position.value.y)
  savePosition()
}

/**
 * Receives a proposed x/y position and returns a safe position that keeps the
 * floating widget inside the visible browser window.
 *
 * @param {number} x - Proposed horizontal position in pixels.
 * @param {number} y - Proposed vertical position in pixels.
 * @returns {{ x: number, y: number }} Safe widget position.
 */
function keepInsideScreen(x, y) {
  const maxX = window.innerWidth - WIDGET_SIZE - SCREEN_PADDING
  const maxY = window.innerHeight - WIDGET_SIZE - SCREEN_PADDING

  return {
    x: Math.min(Math.max(SCREEN_PADDING, x), Math.max(SCREEN_PADDING, maxX)),
    y: Math.min(Math.max(SCREEN_PADDING, y), Math.max(SCREEN_PADDING, maxY))
  }
}

/**
 * Saves the current chatbot widget position in localStorage so the user's
 * preferred position remains after a page refresh.
 */
function savePosition() {
  localStorage.setItem('healthyBuddyPosition', JSON.stringify(position.value))
}

/**
 * Starts dragging the chatbot widget when the user presses the primary pointer
 * button. It records the initial pointer position and registers global drag
 * listeners.
 *
 * @param {PointerEvent} event - Pointer down event from the floating button.
 */
function startDrag(event) {
  if (event.button !== undefined && event.button !== 0) return

  const pointerX = event.clientX
  const pointerY = event.clientY

  isDragging.value = true
  didDrag.value = false

  dragStart.value = {
    x: pointerX,
    y: pointerY
  }

  dragOffset.value = {
    x: pointerX - position.value.x,
    y: pointerY - position.value.y
  }

  window.addEventListener('pointermove', onDrag)
  window.addEventListener('pointerup', stopDrag)
  window.addEventListener('pointercancel', stopDrag)
}

/**
 * Updates the chatbot widget position while the user is dragging it.
 * If the movement passes the drag threshold, it marks the action as a drag
 * instead of a normal click.
 *
 * @param {PointerEvent} event - Pointer move event from the browser window.
 */
function onDrag(event) {
  if (!isDragging.value) return

  const moveX = Math.abs(event.clientX - dragStart.value.x)
  const moveY = Math.abs(event.clientY - dragStart.value.y)

  if (moveX > DRAG_THRESHOLD || moveY > DRAG_THRESHOLD) {
    didDrag.value = true
  }

  position.value = keepInsideScreen(
    event.clientX - dragOffset.value.x,
    event.clientY - dragOffset.value.y
  )
}

/**
 * Stops the current drag action, saves the final widget position, removes
 * global drag listeners, and briefly preserves didDrag to prevent accidental
 * panel toggling.
 */
function stopDrag() {
  if (!isDragging.value) return

  isDragging.value = false
  savePosition()
  removeDragListeners()

  setTimeout(() => {
    didDrag.value = false
  }, 80)
}

/**
 * Removes all global pointer listeners used during dragging.
 * This prevents duplicate listeners and avoids memory leaks.
 */
function removeDragListeners() {
  window.removeEventListener('pointermove', onDrag)
  window.removeEventListener('pointerup', stopDrag)
  window.removeEventListener('pointercancel', stopDrag)
}

/**
 * Opens or closes the chatbot panel when the floating button is clicked.
 * If the user just dragged the widget, the click is ignored.
 */
function handleToggleClick() {
  if (didDrag.value) return

  isOpen.value = !isOpen.value
}

/**
 * Scrolls the chat message container to the latest message after Vue updates
 * the DOM.
 */
function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

/**
 * Places a suggested question into the input and sends it immediately.
 *
 * @param {string} text - Suggested chatbot message text.
 */
function useSuggestion(text) {
  userMessage.value = text
  sendMessage()
}

/**
 * Sends the user's message to the chatbot API and appends the bot response to
 * the chat. If the API URL is missing or the request fails, a friendly fallback
 * message is shown instead.
 */
async function sendMessage() {
  const message = userMessage.value.trim()

  if (!message || loading.value) return

  messages.value.push({
    role: 'user',
    text: message
  })

  userMessage.value = ''
  loading.value = true
  scrollToBottom()

  try {
    if (!CHATBOT_API_BASE_URL) {
      throw new Error('Missing VITE_CHATBOT_API environment variable')
    }

    const response = await fetch(`${CHATBOT_API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message
      })
    })

    if (!response.ok) {
      throw new Error(`Chatbot API failed with status ${response.status}`)
    }

    const data = await response.json()

    messages.value.push({
      role: 'bot',
      text: data.reply || 'Sorry, I could not find a helpful answer for that.'
    })
  } catch (error) {
    console.error('Chatbot error:', error)

    messages.value.push({
      role: 'bot',
      text: "Sorry, I'm having trouble connecting right now. Please try again in a moment."
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}
</script>