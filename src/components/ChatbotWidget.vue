<template>
  <div
    class="chatbot-wrapper"
    :class="{ dragging: isDragging }"
    :style="{
      left: `${position.x}px`,
      top: `${position.y}px`
    }"
  >
    <transition name="chat-slide">
      <section
        v-if="isOpen"
        class="chatbot-panel"
        :style="panelStyle"
      >
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

          <button class="close-btn" @click="isOpen = false" aria-label="Close chatbot">
            x
          </button>
        </header>

        <div ref="messagesContainer" class="chatbot-messages">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="['message-row', message.role]"
          >
            <div class="message-bubble">
              {{ message.text }}
            </div>
          </div>

          <div v-if="loading" class="message-row bot">
            <div class="message-bubble typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>

        <div class="suggestions" v-if="messages.length <= 1">
          <button @click="useSuggestion('My child refuses vegetables. What can I do?')">
            Refuses vegetables
          </button>
          <button @click="useSuggestion('How much screen time is okay?')">
            Screen time
          </button>
          <button @click="useSuggestion('How can I improve my childs sleep routine?')">
            Sleep routine
          </button>
        </div>

        <form class="chatbot-input-area" @submit.prevent="sendMessage">
          <input
            v-model="userMessage"
            type="text"
            placeholder="Ask Healthy Buddy..."
            :disabled="loading"
          />

          <button type="submit" :disabled="loading || !userMessage.trim()">
            <span>&#10148;</span>
          </button>
        </form>
      </section>
    </transition>

    <button
      class="chatbot-toggle"
      :class="{ active: isOpen, 'chatbot-toggle--kids': isKidsRoute && !isOpen }"
      @pointerdown="startDrag"
      @click="handleToggleClick"
      aria-label="Open HealthyKids assistant"
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

      <span v-else class="close-icon">×</span>
    </button>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from "vue";
import { useRoute } from "vue-router";
import healthyBuddyIcon from "@/assets/healthy-buddy-chatbot.png";
import KidsBuddyCharacter from "@/components/KidsBuddyCharacter.vue";

const route = useRoute();
const isKidsRoute = computed(() => {
  const p = route.path || "";
  return (
    p.startsWith("/kids") ||
    p.startsWith("/young-person") ||
    p === "/kids-dashboard"
  );
});

const isOpen = ref(false);
const userMessage = ref("");
const loading = ref(false);
const messagesContainer = ref(null);

const CHATBOT_API_BASE_URL = import.meta.env.VITE_CHATBOT_API;

const WIDGET_SIZE = 130;
const PANEL_WIDTH = 390;
const PANEL_HEIGHT = 570;
const SCREEN_PADDING = 16;
const PANEL_GAP = 12;
const DRAG_THRESHOLD = 6;

const messages = ref([
  {
    role: "bot",
    text: "Hi! I'm Healthy Buddy. Ask me a quick question about food, sleep, screen time or activity."
  }
]);

const position = ref({
  x: window.innerWidth - 155,
  y: window.innerHeight - 245
});

const isDragging = ref(false);
const didDrag = ref(false);
const dragStart = ref({ x: 0, y: 0 });
const dragOffset = ref({ x: 0, y: 0 });

const panelStyle = computed(() => {
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  const actualPanelWidth = Math.min(PANEL_WIDTH, viewportWidth - SCREEN_PADDING * 2);
  const actualPanelHeight = Math.min(PANEL_HEIGHT, viewportHeight - SCREEN_PADDING * 2);

  let left = 0;
  let top = 0;

  const iconCenterX = position.value.x + WIDGET_SIZE / 2;
  const iconCenterY = position.value.y + WIDGET_SIZE / 2;

  /*
    Horizontal placement:
    - If icon is on right half, open panel to the left
    - If icon is on left half, open panel to the right
  */
  if (iconCenterX > viewportWidth / 2) {
    left = -actualPanelWidth + WIDGET_SIZE;
  } else {
    left = 0;
  }

  /*
    Vertical placement:
    - If icon is on lower half, open panel above
    - If icon is on upper half, open panel below
  */
  if (iconCenterY > viewportHeight / 2) {
    top = -actualPanelHeight - PANEL_GAP;
  } else {
    top = WIDGET_SIZE + PANEL_GAP;
  }

  /*
    Clamp panel so it never leaves screen.
    Since panel is absolute inside wrapper, convert viewport clamping
    into wrapper-relative left/top.
  */
  const panelViewportLeft = position.value.x + left;
  const panelViewportTop = position.value.y + top;

  if (panelViewportLeft < SCREEN_PADDING) {
    left += SCREEN_PADDING - panelViewportLeft;
  }

  if (panelViewportLeft + actualPanelWidth > viewportWidth - SCREEN_PADDING) {
    left -= panelViewportLeft + actualPanelWidth - (viewportWidth - SCREEN_PADDING);
  }

  if (panelViewportTop < SCREEN_PADDING) {
    top += SCREEN_PADDING - panelViewportTop;
  }

  if (panelViewportTop + actualPanelHeight > viewportHeight - SCREEN_PADDING) {
    top -= panelViewportTop + actualPanelHeight - (viewportHeight - SCREEN_PADDING);
  }

  return {
    width: `${actualPanelWidth}px`,
    height: `${actualPanelHeight}px`,
    left: `${left}px`,
    top: `${top}px`
  };
});

onMounted(() => {
  const savedPosition = localStorage.getItem("healthyBuddyPosition");

  if (savedPosition) {
    try {
      const parsed = JSON.parse(savedPosition);
      position.value = keepInsideScreen(parsed.x, parsed.y);
    } catch {
      position.value = keepInsideScreen(position.value.x, position.value.y);
    }
  } else {
    position.value = keepInsideScreen(position.value.x, position.value.y);
  }

  window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
  window.removeEventListener("resize", handleResize);
  removeDragListeners();
});

function handleResize() {
  position.value = keepInsideScreen(position.value.x, position.value.y);
  savePosition();
}

function keepInsideScreen(x, y) {
  const maxX = window.innerWidth - WIDGET_SIZE - SCREEN_PADDING;
  const maxY = window.innerHeight - WIDGET_SIZE - SCREEN_PADDING;

  return {
    x: Math.min(Math.max(SCREEN_PADDING, x), Math.max(SCREEN_PADDING, maxX)),
    y: Math.min(Math.max(SCREEN_PADDING, y), Math.max(SCREEN_PADDING, maxY))
  };
}

function savePosition() {
  localStorage.setItem("healthyBuddyPosition", JSON.stringify(position.value));
}

function startDrag(event) {
  if (event.button !== undefined && event.button !== 0) return;

  const pointerX = event.clientX;
  const pointerY = event.clientY;

  isDragging.value = true;
  didDrag.value = false;

  dragStart.value = {
    x: pointerX,
    y: pointerY
  };

  dragOffset.value = {
    x: pointerX - position.value.x,
    y: pointerY - position.value.y
  };

  window.addEventListener("pointermove", onDrag);
  window.addEventListener("pointerup", stopDrag);
  window.addEventListener("pointercancel", stopDrag);
}

function onDrag(event) {
  if (!isDragging.value) return;

  const moveX = Math.abs(event.clientX - dragStart.value.x);
  const moveY = Math.abs(event.clientY - dragStart.value.y);

  if (moveX > DRAG_THRESHOLD || moveY > DRAG_THRESHOLD) {
    didDrag.value = true;
  }

  position.value = keepInsideScreen(
    event.clientX - dragOffset.value.x,
    event.clientY - dragOffset.value.y
  );
}

function stopDrag() {
  if (!isDragging.value) return;

  isDragging.value = false;
  savePosition();
  removeDragListeners();

  setTimeout(() => {
    didDrag.value = false;
  }, 80);
}

function removeDragListeners() {
  window.removeEventListener("pointermove", onDrag);
  window.removeEventListener("pointerup", stopDrag);
  window.removeEventListener("pointercancel", stopDrag);
}

function handleToggleClick() {
  if (didDrag.value) return;
  isOpen.value = !isOpen.value;
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
}

function useSuggestion(text) {
  userMessage.value = text;
  sendMessage();
}

async function sendMessage() {
  const message = userMessage.value.trim();
  if (!message || loading.value) return;

  messages.value.push({
    role: "user",
    text: message
  });

  userMessage.value = "";
  loading.value = true;
  scrollToBottom();

  try {
    if (!CHATBOT_API_BASE_URL) {
      throw new Error("Missing VITE_CHATBOT_API environment variable");
    }

    const response = await fetch(`${CHATBOT_API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message
      })
    });

    if (!response.ok) {
      throw new Error(`Chatbot API failed with status ${response.status}`);
    }

    const data = await response.json();

    messages.value.push({
      role: "bot",
      text: data.reply || "Sorry, I could not find a helpful answer for that."
    });
  } catch (error) {
    console.error("Chatbot error:", error);

    messages.value.push({
      role: "bot",
      text: "Sorry, I'm having trouble connecting right now. Please try again in a moment."
    });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
}
</script>
