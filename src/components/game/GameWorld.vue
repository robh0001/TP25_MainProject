<template>
  <main class="adventure-shell game-mode">
    <section class="game-hud-top">
      <div class="hud-left">
        <div class="hud-pill">🧭 Adventure Mode</div>
        <div class="hud-pill">🌍 {{ currentWorldName }}</div>
      </div>
      <div class="hud-right">
        <div class="hero-chip">⭐ Lv {{ store.level }}</div>
        <div class="hero-chip">💎 {{ store.coins }}</div>
        <div class="hero-chip">⚡ {{ store.xp }}</div>
      </div>
    </section>

    <section
      ref="mapStageRef"
      class="game-map-stage"
      @pointerdown="startPointerDrag"
      @pointermove="onPointerDrag"
      @pointerup="stopPointerDrag"
      @pointercancel="stopPointerDrag"
      @pointerleave="stopPointerDrag"
    >
      <div class="map-layer" :style="{ transform: `translate(${mapOffset.x}px, ${mapOffset.y}px)` }">
        <div class="map-radar"></div>
        <button type="button" class="poi-node one" @click="openEncounter('forest')">🌳</button>
        <button type="button" class="poi-node two" @click="openEncounter('ocean')">🌊</button>
        <button type="button" class="poi-node three" @click="openEncounter('space')">🚀</button>
        <button type="button" class="poi-node four" @click="openEncounter('mountain')">⛰️</button>
      </div>
      <div class="player-marker" :style="{ left: `${playerPos.x}%`, top: `${playerPos.y}%` }">🧒</div>
      <div class="pet-marker" :style="{ left: `${playerPos.x + 7}%`, top: `${playerPos.y + 10}%` }">🦊</div>
      <div class="scan-ring"></div>
    </section>

    <section class="game-hud-bottom">
      <div class="hud-card hud-card-wide">
        <ProgressBar label="Trainer level progress" :value="store.levelProgress" />
      </div>
      <div class="hud-card">
        <StreakTracker :streak="store.streak" :milestone="store.streakMilestone" />
      </div>
      <div class="hud-card">
        <button class="radar-btn" type="button" @click="triggerScanEvent">📡 Scan Quests</button>
      </div>
    </section>

    <section class="movement-pad">
      <button type="button" @click="movePlayer(0, -6)">⬆️</button>
      <div>
        <button type="button" @click="movePlayer(-6, 0)">⬅️</button>
        <button type="button" @click="movePlayer(6, 0)">➡️</button>
      </div>
      <button type="button" @click="movePlayer(0, 6)">⬇️</button>
    </section>

    <section class="game-tabs">
      <button :class="{ active: activePanel === 'map' }" @click="activePanel = 'map'">Map</button>
      <button :class="{ active: activePanel === 'quests' }" @click="activePanel = 'quests'">Quests</button>
      <button :class="{ active: activePanel === 'pet' }" @click="activePanel = 'pet'">Pet</button>
      <button :class="{ active: activePanel === 'shop' }" @click="activePanel = 'shop'">Shop</button>
    </section>

    <section class="adventure-grid game-panels">
      <WorldMap
        v-if="activePanel === 'map'"
        :worlds="store.worlds"
        :active-world-id="store.activeWorldId"
        :unlocked-world-ids="store.unlockedWorldIds"
        :player-level="store.level"
      />
      <QuestBoard
        v-if="activePanel === 'quests'"
        :quests="store.dailyQuests"
        :completed-quest-ids="store.completedQuestIds"
        @complete-quest="completeQuest"
      />
      <Pet
        v-if="activePanel === 'pet' || activePanel === 'shop'"
        :streak="store.streak"
        :completed-quest-count="store.completedQuestIds.length"
        :active-skin="store.activePetSkin"
        @buy-skin="handleBuySkin"
      />
    </section>

    <Transition name="pop">
      <article v-if="encounterCard" class="encounter-card">
        <p class="panel-kicker">Wild habit appeared!</p>
        <h3>{{ encounterCard.title }}</h3>
        <p>{{ encounterCard.message }}</p>
        <button class="btn btn-primary" type="button" @click="encounterCard = null">Catch this quest</button>
      </article>
    </Transition>

    <RewardModal :reward="store.rewardFlash" @close="store.closeRewardFlash" />
  </main>
</template>

<script setup>
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useAdventureStore } from '../../stores/adventureStore'
import ProgressBar from './ProgressBar.vue'
import WorldMap from './WorldMap.vue'
import QuestBoard from './QuestBoard.vue'
import RewardModal from './RewardModal.vue'
import StreakTracker from './StreakTracker.vue'
import Pet from './Pet.vue'

const store = useAdventureStore()
const currentWorldName = computed(
  () => store.worlds.find((world) => world.id === store.activeWorldId)?.name ?? 'Forest World'
)
const activePanel = ref('map')
const playerPos = reactive({ x: 45, y: 42 })
const mapOffset = reactive({ x: 0, y: 0 })
const dragging = reactive({ active: false, pointerId: null, startX: 0, startY: 0 })
const mapStageRef = ref(null)
const encounterCard = ref(null)

onMounted(() => {
  store.loadFromStorage()
  store.resetDailyQuestsIfNeeded()
  window.addEventListener('keydown', onKeyMove)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeyMove)
})

function playRewardSound() {
  if (typeof window === 'undefined') return
  const ctx = new window.AudioContext()
  const oscillator = ctx.createOscillator()
  const gain = ctx.createGain()

  oscillator.type = 'triangle'
  oscillator.frequency.value = 680
  gain.gain.value = 0.04

  oscillator.connect(gain)
  gain.connect(ctx.destination)
  oscillator.start()
  oscillator.stop(ctx.currentTime + 0.12)
}

function completeQuest(questId) {
  store.completeQuest(questId)
  playRewardSound()
}

function handleBuySkin(skin) {
  store.buyPetSkin(skin.id, skin.cost)
}

function movePlayer(dx, dy) {
  playerPos.x = Math.max(8, Math.min(86, playerPos.x + dx))
  playerPos.y = Math.max(10, Math.min(82, playerPos.y + dy))
}

function onKeyMove(event) {
  if (event.key === 'ArrowUp') movePlayer(0, -4)
  if (event.key === 'ArrowDown') movePlayer(0, 4)
  if (event.key === 'ArrowLeft') movePlayer(-4, 0)
  if (event.key === 'ArrowRight') movePlayer(4, 0)
}

function startPointerDrag(event) {
  if (event.pointerType === 'mouse' && event.button !== 0) return
  dragging.active = true
  dragging.pointerId = event.pointerId
  dragging.startX = event.clientX - mapOffset.x
  dragging.startY = event.clientY - mapOffset.y
  mapStageRef.value?.setPointerCapture?.(event.pointerId)
}

function onPointerDrag(event) {
  if (!dragging.active || dragging.pointerId !== event.pointerId) return
  mapOffset.x = Math.max(-60, Math.min(60, event.clientX - dragging.startX))
  mapOffset.y = Math.max(-40, Math.min(40, event.clientY - dragging.startY))
}

function stopPointerDrag(event) {
  if (dragging.pointerId !== null && event?.pointerId === dragging.pointerId) {
    mapStageRef.value?.releasePointerCapture?.(dragging.pointerId)
  }
  dragging.active = false
  dragging.pointerId = null
}

function openEncounter(worldId) {
  const messages = {
    forest: 'Berry Blitz challenge nearby. Complete one nutrition quest for bonus coins.',
    ocean: 'Sleep Wave alert. Finish bedtime quest before 9 PM for extra XP.',
    space: 'Rocket Run spotted. Try 20 active minutes to catch the reward.',
    mountain: 'Peak Streak mission found. Keep your streak alive for milestone loot.',
  }
  encounterCard.value = {
    title: `Encounter in ${worldId[0].toUpperCase()}${worldId.slice(1)} World`,
    message: messages[worldId],
  }
}

function triggerScanEvent() {
  const worldIds = ['forest', 'ocean', 'space', 'mountain']
  openEncounter(worldIds[Math.floor(Math.random() * worldIds.length)])
}
</script>
