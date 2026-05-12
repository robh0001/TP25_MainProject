<template>
  <section class="habit-lab" :class="{ 'habit-lab--dark': isDarkMode }">
    <div class="mission-tabs" role="tablist" aria-label="Habit mission tabs">
      <button
        v-for="mission in missions"
        :key="mission.id"
        type="button"
        class="mission-tab"
        :class="{ active: mission.id === activeMission }"
        @click="setMission(mission.id)"
      >
        {{ mission.title }}
      </button>
    </div>

    <div class="mission-summary">
      <div class="mission-summary-copy">
        <strong>{{ currentStage.title }}</strong>
        <button type="button" class="info-btn" @click="showInfo = true" aria-label="Show explorer game info">i</button>
      </div>
      <div class="summary-pill">
        <span>Set {{ currentProgress.stageIndex + 1 }} / {{ currentMission.stages.length }}</span>
        <strong>{{ completedCount }} / {{ currentStage.items.length }}</strong>
      </div>
    </div>

    <div class="progress-track" aria-hidden="true">
      <span class="progress-bar" :style="{ width: `${stageProgress}%` }"></span>
    </div>

    <div class="lab-shell">
      <aside class="ingredient-panel">
        <div class="panel-heading">
          <h4>{{ currentStage.title }} Cards</h4>
        </div>

        <div class="ingredient-grid">
          <button
            v-for="item in currentStage.items"
            :key="item.id"
            type="button"
            class="ingredient-btn"
            :class="{
              selected: isItemSelected(item.id),
              completed: isItemCompleted(item.id),
              burst: isUnlockBurstItem(item.id),
            }"
            :disabled="isItemDisabled(item.id)"
            @click="pickItem(item.id)"
          >
            <img class="ingredient-image" :src="item.image" :alt="item.label" />
            <div class="ingredient-copy">
              <span class="ingredient-icon" aria-hidden="true">{{ item.icon }}</span>
              <strong>{{ item.label }}</strong>
            </div>
            <span v-if="isItemCompleted(item.id)" class="state-badge">Done</span>
            <span v-else-if="isItemSelected(item.id)" class="state-badge">Picked</span>
          </button>
        </div>
      </aside>

      <section class="combine-panel" :class="{ unlocking: unlockBurst.active }">
        <div class="slots-header">
          <button type="button" class="clear-btn" @click="resetSelection">Clear cards</button>
        </div>

        <div class="slots">
          <button type="button" class="slot" :class="{ burst: firstSlotItem && isUnlockBurstItem(firstSlotItem.id) }" @click="clearSlot(0)">
            <template v-if="slotItem(0)">
              <img class="slot-image" :src="slotItem(0).image" :alt="slotItem(0).label" />
              <span>{{ slotItem(0).label }}</span>
            </template>
            <template v-else>Pick first card</template>
          </button>
          <span class="plus">+</span>
          <button type="button" class="slot" :class="{ burst: secondSlotItem && isUnlockBurstItem(secondSlotItem.id) }" @click="clearSlot(1)">
            <template v-if="slotItem(1)">
              <img class="slot-image" :src="slotItem(1).image" :alt="slotItem(1).label" />
              <span>{{ slotItem(1).label }}</span>
            </template>
            <template v-else>Pick second card</template>
          </button>
        </div>

        <button type="button" class="combine-btn" :disabled="!canCombine" @click="combineSlots">
          Make a healthy match
        </button>

        <div class="result-box" :class="{ success: lastResult.success, fail: !lastResult.success, celebrate: unlockBurst.active }">
          <strong>{{ lastResult.title }}</strong>
          <p>{{ lastResult.message }}</p>
        </div>

        <div class="preview-card" :class="{ celebrate: unlockBurst.active }">
          <div class="preview-image-wrap">
            <img class="preview-image" :src="previewCard.image" :alt="previewCard.title" />
          </div>
          <div class="preview-copy">
            <p class="preview-label">Bright explorer preview</p>
            <h5>{{ previewCard.title }}</h5>
            <p>{{ previewCard.description }}</p>
          </div>
        </div>

        <div class="video-shell">
          <div class="video-heading">
            <h5>Watch a bright idea</h5>
            <span>{{ previewCard.videoLabel }}</span>
          </div>
          <div class="video-frame">
            <iframe
              :src="previewCard.videoUrl"
              :title="previewCard.videoLabel"
              loading="lazy"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </section>

      <aside class="discoveries-panel">
        <h4>Discoveries</h4>
        <ul>
          <li v-for="discovery in discoveryList" :key="discovery.id" :class="{ newest: isLatestDiscovery(discovery.id) }">
            <strong>{{ discovery.result }}</strong>
            <span>{{ discovery.tip }}</span>
          </li>
          <li v-if="discoveryList.length === 0" class="empty">No discoveries yet. Try your first bright pair.</li>
        </ul>

        <div class="score">
          <span>Stars</span>
          <strong>{{ stars }}</strong>
        </div>
      </aside>
    </div>
    <div v-if="showInfo" class="info-modal-backdrop" @click.self="showInfo = false">
      <div class="info-modal">
        <div class="info-modal-head">
          <div>
            <p class="panel-kicker">How to play</p>
            <h4>Explorer Game</h4>
          </div>
          <button type="button" class="info-close" @click="showInfo = false" aria-label="Close info">×</button>
        </div>
        <ul class="info-list">
          <li>Pick two matching cards to build a healthy pair.</li>
          <li>Watch the result box and preview card to see what you unlocked.</li>
          <li>Finish each set to move to the next stage and earn more stars.</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, reactive, ref } from "vue"
import { injectKidsTheme } from "../../composables/useKidsTheme.js"
import { createExplorerMissions } from "../../data/explorerMissionData"

const { isDarkMode } = injectKidsTheme()

const missions = createExplorerMissions()

const activeMission = ref("snack")
const showInfo = ref(false)
const selected = ref([null, null])
const stars = ref(0)
const unlockBurst = reactive({
  active: false,
  itemIds: [],
  recipe: null,
  latestDiscoveryId: null,
})
const lastResult = reactive({
  success: true,
  title: "Pick two cards",
  message: "Choose two matching cards to unlock the healthy habit and complete the set.",
})

let unlockBurstTimer = null

const progress = reactive(
  Object.fromEntries(
    missions.map(mission => [
      mission.id,
      {
        stageIndex: 0,
        completedItemIds: [],
        discoveries: [],
      },
    ])
  )
)

const currentMission = computed(() => missions.find(mission => mission.id === activeMission.value))
const currentProgress = computed(() => progress[activeMission.value])
const currentStage = computed(() => currentMission.value.stages[currentProgress.value.stageIndex])
const canCombine = computed(() => Boolean(selected.value[0] && selected.value[1]))
const discoveryList = computed(() => currentProgress.value.discoveries)
const firstSlotItem = computed(() => slotItem(0))
const secondSlotItem = computed(() => slotItem(1))
const completedCount = computed(() =>
  currentStage.value.items.filter(item => currentProgress.value.completedItemIds.includes(item.id)).length
)
const stageProgress = computed(() =>
  Math.round((completedCount.value / currentStage.value.items.length) * 100)
)

const selectedItems = computed(() =>
  selected.value
    .map(itemId => currentStage.value.items.find(item => item.id === itemId))
    .filter(Boolean)
)

const selectedMatch = computed(() => {
  if (!canCombine.value) return null
  const pairKey = selected.value.slice().sort().join("+")
  return currentStage.value.recipes.find(recipe => recipe.pair.slice().sort().join("+") === pairKey) ?? null
})

const previewCard = computed(() => {
  if (unlockBurst.recipe) {
    return {
      image: unlockBurst.recipe.image,
      title: unlockBurst.recipe.result,
      description: unlockBurst.recipe.tip,
      videoUrl: unlockBurst.recipe.videoUrl,
      videoLabel: `${unlockBurst.recipe.result} video ideas`,
    }
  }

  if (selectedMatch.value) {
    return {
      image: selectedMatch.value.image,
      title: selectedMatch.value.result,
      description: selectedMatch.value.tip,
      videoUrl: selectedMatch.value.videoUrl,
      videoLabel: `${selectedMatch.value.result} video ideas`,
    }
  }

  if (selectedItems.value.length === 2) {
    return {
      image: selectedItems.value[1].image,
      title: "Almost there",
      description: "Try unlocking this pair. If it is a healthy match, those cards will complete and the set will move forward.",
      videoUrl: selectedItems.value[1].videoUrl,
      videoLabel: `${selectedItems.value[1].label} video ideas`,
    }
  }

  if (selectedItems.value.length === 1) {
    return {
      image: selectedItems.value[0].image,
      title: selectedItems.value[0].label,
      description: selectedItems.value[0].shortTip,
      videoUrl: selectedItems.value[0].videoUrl,
      videoLabel: `${selectedItems.value[0].label} video ideas`,
    }
  }

  return {
    image: currentStage.value.heroImage,
    title: currentStage.value.title,
    description: currentStage.value.description,
    videoUrl: currentStage.value.videoUrl,
    videoLabel: `${currentStage.value.title} video ideas`,
  }
})

function setMission(id) {
  activeMission.value = id
  clearUnlockBurst()
  resetSelection()
  lastResult.success = true
  lastResult.title = "Mission switched"
  lastResult.message = "Choose two bright matching cards. Completed cards stay calm so kids can see their progress."
}

function slotItem(index) {
  const itemId = selected.value[index]
  return currentStage.value.items.find(item => item.id === itemId) ?? null
}

function isItemSelected(itemId) {
  return selected.value.includes(itemId)
}

function isItemCompleted(itemId) {
  return currentProgress.value.completedItemIds.includes(itemId)
}

function isItemDisabled(itemId) {
  return isItemSelected(itemId) || isItemCompleted(itemId)
}

function pickItem(itemId) {
  if (isItemDisabled(itemId)) return

  if (!selected.value[0]) {
    selected.value[0] = itemId
    return
  }

  if (!selected.value[1]) {
    selected.value[1] = itemId
    return
  }

  selected.value = [itemId, null]
}

function clearSlot(index) {
  selected.value[index] = null
}

function resetSelection() {
  selected.value = [null, null]
}

function clearUnlockBurst() {
  clearTimeout(unlockBurstTimer)
  unlockBurst.active = false
  unlockBurst.itemIds = []
  unlockBurst.recipe = null
  unlockBurst.latestDiscoveryId = null
}

function startUnlockBurst(match, itemIds) {
  clearTimeout(unlockBurstTimer)
  unlockBurst.active = true
  unlockBurst.itemIds = [...itemIds]
  unlockBurst.recipe = match
  unlockBurst.latestDiscoveryId = match.id
  unlockBurstTimer = setTimeout(() => {
    clearUnlockBurst()
  }, 900)
}

function isUnlockBurstItem(itemId) {
  return unlockBurst.active && unlockBurst.itemIds.includes(itemId)
}

function isLatestDiscovery(discoveryId) {
  return unlockBurst.latestDiscoveryId === discoveryId
}

function combineSlots() {
  if (!canCombine.value) return
  const [first, second] = selected.value
  resolvePair(first, second)
}

function resolvePair(first, second) {
  const pairKey = [first, second].sort().join("+")
  const match = currentStage.value.recipes.find(recipe => recipe.pair.slice().sort().join("+") === pairKey)

  if (!match) {
    lastResult.success = false
    lastResult.title = "Try a different match"
    lastResult.message = "That pair does not belong together in this set yet. Pick a different combination."
    return
  }

  const alreadyFound = currentProgress.value.discoveries.some(discovery => discovery.id === match.id)

  if (!alreadyFound) {
    currentProgress.value.discoveries.push(match)
    currentProgress.value.completedItemIds.push(first, second)
    stars.value += 2
    startUnlockBurst(match, [first, second])
  }

  const currentStageItemIds = currentStage.value.items.map(item => item.id)
  const completedAll = currentStageItemIds.every(itemId =>
    currentProgress.value.completedItemIds.includes(itemId)
  )

  if (completedAll && currentProgress.value.stageIndex < currentMission.value.stages.length - 1) {
    currentProgress.value.stageIndex += 1
    currentProgress.value.completedItemIds = currentProgress.value.completedItemIds.filter(itemId =>
      !currentStageItemIds.includes(itemId)
    )
    lastResult.success = true
    lastResult.title = `${match.result} unlocked the next set`
    lastResult.message =
      `${match.tip} Nice work: all cards in that set are finished, so a new set just appeared.`
  } else if (completedAll) {
    lastResult.success = true
    lastResult.title = `${match.result} finished the mission`
    lastResult.message =
      `${match.tip} Amazing job. Every set in this mission is complete, so the whole explorer challenge is done.`
  } else {
    lastResult.success = true
    lastResult.title = match.result
    lastResult.message = `${match.tip} Those cards are now greyed out because they are completed.`
  }

  if (alreadyFound) {
    clearUnlockBurst()
  }

  setTimeout(() => {
    resetSelection()
  }, alreadyFound ? 0 : 420)
}
</script>

<style scoped>
.habit-lab {
  --coral: #FF6058;
  --sky: #3B9EFF;
  --mint: #2CC97A;
  --amber: #FFB020;
  --violet: #9B72FF;
  --rose: #FF7EB3;
  margin-top: 0;
  color: #1a2442;
  font-family: "DM Sans", sans-serif;
}

.mission-tabs {
  display: flex;
  gap: 10px;
  margin-top: 6px;
  flex-wrap: wrap;
  padding: 10px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(240, 245, 255, 0.78));
  border: 1px solid rgba(88, 108, 196, 0.14);
  box-shadow: 0 16px 28px rgba(33, 52, 106, 0.08);
}

.mission-tab {
  border: 1.5px solid rgba(72, 91, 180, 0.14);
  background: linear-gradient(135deg, rgba(245, 248, 255, 0.98), rgba(239, 245, 255, 0.94));
  color: #38558d;
  border-radius: 999px;
  min-height: 48px;
  padding: 0 18px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 10px 18px rgba(37, 54, 108, 0.08);
  transition:
    transform 0.16s ease,
    box-shadow 0.16s ease,
    border-color 0.16s ease,
    background 0.16s ease;
}

.mission-tab:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 22px rgba(37, 54, 108, 0.12);
}

.mission-tab.active {
  background: linear-gradient(135deg, #ff7f62 0%, #ffb365 100%);
  color: #fff;
  border-color: transparent;
  box-shadow: 0 16px 28px rgba(255, 96, 88, 0.24);
  animation: labPulse 3.6s ease-in-out infinite;
}

.mission-summary {
  margin-top: 18px;
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 12px;
  padding: 18px;
  border-radius: 24px;
  background:
    radial-gradient(circle at 10% 18%, rgba(255, 176, 32, 0.14), transparent 24%),
    radial-gradient(circle at 88% 16%, rgba(59, 158, 255, 0.08), transparent 18%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.97), rgba(239, 246, 255, 0.92));
  border: 1px solid rgba(86, 102, 193, 0.14);
  box-shadow: 0 18px 30px rgba(33, 52, 106, 0.08);
  animation: panelFloat 5.4s ease-in-out infinite;
}

.mission-summary-copy {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mission-summary strong {
  display: block;
  font-size: 1.05rem;
  color: #21345d;
  font-family: "Baloo 2", cursive;
}

.summary-pill {
  min-width: 170px;
  padding: 10px 14px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(239, 247, 255, 0.98), rgba(233, 241, 255, 0.95));
  border: 1.5px solid rgba(72, 91, 180, 0.12);
  display: grid;
  gap: 6px;
  box-shadow: 0 10px 18px rgba(33, 52, 106, 0.08);
}

.summary-pill span {
  color: #5d6c92;
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.progress-track {
  margin-top: 12px;
  height: 12px;
  border-radius: 999px;
  background: rgba(87, 102, 195, 0.12);
  overflow: hidden;
}

.progress-bar {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(135deg, var(--sky) 0%, var(--violet) 100%);
  transition: width 0.2s ease;
  background-size: 200% 100%;
  animation: labProgressGlow 2.8s linear infinite;
}

.lab-shell {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 1.1fr 1.2fr 0.85fr;
  gap: 14px;
}

.ingredient-panel,
.combine-panel,
.discoveries-panel {
  border-radius: 24px;
  background:
    radial-gradient(circle at 100% 0%, rgba(59, 158, 255, 0.16), transparent 24%),
    radial-gradient(circle at 10% 20%, rgba(255, 176, 32, 0.12), transparent 20%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(246, 244, 255, 0.94));
  border: 1px solid rgba(86, 109, 184, 0.14);
  padding: 18px;
  box-shadow: 0 18px 30px rgba(33, 52, 106, 0.1);
  position: relative;
  overflow: hidden;
}

.panel-heading h4,
.discoveries-panel h4 {
  margin: 0;
  font-family: "Baloo 2", cursive;
  color: #1f325b;
}

.ingredient-grid {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.ingredient-btn {
  position: relative;
  border: 1px solid rgba(78, 97, 175, 0.1);
  border-radius: 22px;
  padding: 10px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(243, 246, 255, 0.92));
  color: #24305d;
  display: grid;
  gap: 10px;
  text-align: left;
  cursor: pointer;
  transition: transform 0.14s ease, box-shadow 0.14s ease, filter 0.14s ease;
}

.ingredient-btn:nth-child(3n + 1) {
  background: linear-gradient(180deg, rgba(255, 246, 249, 0.98), rgba(255, 238, 245, 0.92));
}

.ingredient-btn:nth-child(3n + 2) {
  background: linear-gradient(180deg, rgba(241, 249, 255, 0.98), rgba(234, 244, 255, 0.92));
}

.ingredient-btn:nth-child(3n + 3) {
  background: linear-gradient(180deg, rgba(243, 255, 247, 0.98), rgba(236, 250, 244, 0.92));
}

.ingredient-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(36, 51, 118, 0.14);
  animation: cardWiggle 0.32s ease;
}

.ingredient-btn.burst {
  animation: unlockPop 0.72s ease;
  box-shadow: 0 0 0 3px rgba(120, 99, 255, 0.14), 0 18px 34px rgba(88, 84, 220, 0.22);
}

.ingredient-btn.selected,
.ingredient-btn.completed,
.ingredient-btn:disabled {
  filter: grayscale(1);
  opacity: 0.62;
  cursor: not-allowed;
}

.ingredient-btn.completed {
  opacity: 0.56;
}

.ingredient-image {
  width: 100%;
  aspect-ratio: 1.12;
  object-fit: cover;
  border-radius: 14px;
  background: #eef2ff;
}

.ingredient-copy {
  display: grid;
  gap: 4px;
}

.ingredient-copy strong {
  font-size: 1rem;
}

.ingredient-icon {
  font-size: 1.8rem;
}

.state-badge {
  position: absolute;
  right: 12px;
  top: 12px;
  border-radius: 999px;
  background: rgba(20, 31, 69, 0.8);
  color: #fff;
  font-size: 0.82rem;
  font-weight: 800;
  padding: 5px 9px;
}

.slots-header {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.clear-btn {
  min-height: 40px;
  border: 1.5px solid rgba(89, 108, 197, 0.16);
  border-radius: 999px;
  padding: 0 14px;
  background: linear-gradient(135deg, rgba(243, 241, 255, 0.98), rgba(232, 243, 255, 0.95));
  color: #5c58d5;
  font-weight: 800;
  cursor: pointer;
}

.slots {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 8px;
  margin-top: 14px;
}

.plus {
  font-size: 1.4rem;
  font-weight: 900;
  color: #4253c8;
}

.slot {
  min-height: 94px;
  border: 1px dashed rgba(62, 84, 152, 0.45);
  border-radius: 18px;
  background: linear-gradient(180deg, #f2f5ff, #fbf2ff);
  color: #273661;
  font-weight: 700;
  display: grid;
  justify-items: center;
  align-content: center;
  gap: 8px;
  cursor: pointer;
  padding: 10px;
  text-align: center;
}

.slot.burst {
  animation: unlockPulse 0.72s ease;
  border-color: rgba(97, 92, 243, 0.55);
  background: linear-gradient(180deg, rgba(243, 242, 255, 0.96), rgba(230, 240, 255, 0.94));
  box-shadow: 0 16px 30px rgba(93, 89, 230, 0.18);
}

.slot-image {
  width: 72px;
  height: 56px;
  object-fit: cover;
  border-radius: 12px;
}

.combine-btn {
  margin-top: 14px;
  width: 100%;
  min-height: 46px;
  border: 0;
  border-radius: 14px;
  font-weight: 800;
  cursor: pointer;
  color: #fff;
  background: linear-gradient(135deg, #ff7f62 0%, #ffb365 100%);
  transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
  font-family: "Baloo 2", cursive;
  animation: labPulse 3.8s ease-in-out infinite;
}

.combine-panel.unlocking .combine-btn {
  transform: translateY(-1px) scale(1.01);
  box-shadow: 0 18px 30px rgba(92, 76, 226, 0.3);
}

.combine-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.result-box {
  margin-top: 14px;
  border-radius: 16px;
  padding: 14px;
  border: 1px solid rgba(68, 89, 160, 0.22);
}

.result-box.success {
  background: linear-gradient(135deg, rgba(17, 132, 86, 0.16), rgba(216, 255, 235, 0.72));
}

.result-box.fail {
  background: linear-gradient(135deg, rgba(171, 54, 70, 0.14), rgba(255, 232, 238, 0.72));
}

.result-box strong {
  display: block;
}

.result-box p {
  margin: 6px 0 0;
  line-height: 1.55;
}

.result-box.celebrate,
.preview-card.celebrate {
  animation: unlockPulse 0.82s ease;
}

.preview-card {
  margin-top: 14px;
  border-radius: 22px;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(249, 250, 255, 0.98), rgba(241, 245, 255, 0.92));
  border: 1px solid rgba(68, 89, 160, 0.12);
  box-shadow: 0 12px 24px rgba(33, 52, 106, 0.08);
  animation: panelFloat 5s ease-in-out infinite;
}

.preview-image-wrap {
  padding: 12px 12px 0;
}

.preview-image {
  width: 100%;
  border-radius: 16px;
  object-fit: cover;
}

.preview-copy {
  padding: 14px;
}

.preview-label {
  margin: 0;
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--violet);
  font-weight: 800;
}

.preview-copy h5,
.video-heading h5 {
  margin: 8px 0 0;
  font-size: 1rem;
  font-family: "Baloo 2", cursive;
}

.preview-copy p:last-child,
.video-heading span {
  margin: 8px 0 0;
  color: #5f6d92;
  line-height: 1.55;
}

.video-shell {
  margin-top: 14px;
  border-radius: 22px;
  border: 1px solid rgba(68, 89, 160, 0.12);
  padding: 14px;
  background: linear-gradient(180deg, rgba(251, 251, 255, 0.96), rgba(243, 246, 255, 0.92));
  box-shadow: 0 12px 24px rgba(33, 52, 106, 0.08);
}

.video-frame {
  margin-top: 12px;
  border-radius: 16px;
  overflow: hidden;
  aspect-ratio: 16 / 9;
  background: #101631;
}

.video-frame iframe {
  width: 100%;
  height: 100%;
  border: 0;
}

.discoveries-panel ul {
  list-style: none;
  margin: 12px 0 0;
  padding: 0;
  display: grid;
  gap: 10px;
}

.discoveries-panel li {
  border-radius: 18px;
  padding: 10px 12px;
  background: linear-gradient(180deg, rgba(242, 245, 255, 0.96), rgba(247, 249, 255, 0.92));
  display: grid;
  gap: 4px;
}

.discoveries-panel li.newest {
  animation: unlockPop 0.78s ease;
  border: 1px solid rgba(103, 101, 239, 0.24);
  box-shadow: 0 14px 28px rgba(93, 89, 230, 0.14);
}

.discoveries-panel li span {
  color: #5a688d;
  line-height: 1.5;
}

.discoveries-panel .empty {
  color: #63709a;
}

.score {
  margin-top: 14px;
  border-radius: 14px;
  background: linear-gradient(135deg, #7f7cff, #6bb2ff, #65d4a4);
  padding: 10px 12px;
  display: grid;
  justify-items: center;
  color: #fff;
  animation: panelFloat 4.8s ease-in-out infinite;
  box-shadow: 0 18px 30px rgba(91, 109, 255, 0.24);
}

.score span {
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.82;
}

.score strong {
  font-size: 1.5rem;
  font-family: "Baloo 2", cursive;
}

.info-btn,
.info-close {
  width: 48px;
  height: 48px;
  border-radius: 999px;
  border: 1.5px solid rgba(107, 45, 255, 0.18);
  background: linear-gradient(135deg, rgba(243, 240, 255, 0.98), rgba(232, 242, 255, 0.96));
  color: #5d57d8;
  font-weight: 900;
  font-size: 1.3rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 10px 18px rgba(33, 52, 106, 0.08);
  flex: 0 0 auto;
  animation: labPulse 3.2s ease-in-out infinite;
}

.panel-kicker {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.76rem;
  color: var(--violet);
  font-weight: 900;
}

.info-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 20;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(24, 25, 43, 0.28);
  backdrop-filter: blur(10px);
}

.info-modal {
  width: min(520px, 100%);
  border-radius: 26px;
  padding: 20px;
  background:
    radial-gradient(circle at 100% 0%, rgba(155, 114, 255, 0.18), transparent 30%),
    radial-gradient(circle at 0% 100%, rgba(255, 176, 32, 0.18), transparent 26%),
    rgba(255, 255, 255, 0.98);
  border: 1.5px solid rgba(86, 109, 184, 0.14);
  box-shadow: 0 18px 30px rgba(33, 52, 106, 0.16);
  animation: panelFloat 5.1s ease-in-out infinite;
}

.info-modal-head {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 12px;
}

.info-modal h4 {
  margin: 8px 0 0;
  font-size: 1.3rem;
  font-family: "Baloo 2", cursive;
  color: #1f325b;
}

.info-list {
  margin: 14px 0 0;
  padding-left: 18px;
  color: #556586;
  display: grid;
  gap: 10px;
  line-height: 1.6;
}

.info-list li::marker {
  color: var(--coral);
}

@keyframes labPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.04); }
}

@keyframes panelFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

@keyframes cardWiggle {
  0%, 100% { transform: translateY(-2px) rotate(0deg); }
  35% { transform: translateY(-3px) rotate(-1deg); }
  70% { transform: translateY(-3px) rotate(1deg); }
}

@keyframes labProgressGlow {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

.ingredient-panel::after,
.combine-panel::after,
.discoveries-panel::after {
  content: "";
  position: absolute;
  inset: auto -20% -30% auto;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  pointer-events: none;
  background: radial-gradient(circle, rgba(155, 114, 255, 0.16), rgba(155, 114, 255, 0));
  animation: panelFloat 6.2s ease-in-out infinite reverse;
}

/* Dark theme — matches kid route shell */
.habit-lab--dark {
  color: rgba(226, 234, 255, 0.95);
}

.habit-lab--dark .mission-tabs {
  background: linear-gradient(135deg, rgba(22, 28, 52, 0.92), rgba(14, 18, 40, 0.9));
  border-color: rgba(143, 154, 227, 0.22);
}

.habit-lab--dark .mission-tab:not(.active) {
  border-color: rgba(143, 154, 227, 0.2);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
  color: rgba(226, 234, 255, 0.92);
  box-shadow: 0 8px 18px rgba(3, 7, 23, 0.35);
}

.habit-lab--dark .mission-summary {
  background:
    radial-gradient(circle at 10% 18%, rgba(255, 176, 32, 0.1), transparent 24%),
    linear-gradient(135deg, rgba(22, 28, 52, 0.95), rgba(14, 18, 42, 0.92));
  border-color: rgba(143, 154, 227, 0.22);
}

.habit-lab--dark .mission-summary strong {
  color: #f2f7ff;
}

.habit-lab--dark .summary-pill {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
  border-color: rgba(143, 154, 227, 0.22);
}

.habit-lab--dark .summary-pill span {
  color: rgba(198, 208, 240, 0.88);
}

.habit-lab--dark .summary-pill strong {
  color: #f2f7ff;
}

.habit-lab--dark .progress-track {
  background: rgba(255, 255, 255, 0.12);
}

.habit-lab--dark .ingredient-panel,
.habit-lab--dark .combine-panel,
.habit-lab--dark .discoveries-panel {
  background:
    radial-gradient(circle at 100% 0%, rgba(59, 158, 255, 0.12), transparent 24%),
    linear-gradient(180deg, rgba(18, 22, 43, 0.95), rgba(12, 16, 34, 0.94));
  border-color: rgba(143, 154, 227, 0.22);
}

.habit-lab--dark .panel-heading h4,
.habit-lab--dark .discoveries-panel h4 {
  color: #f2f7ff;
}

.habit-lab--dark .ingredient-btn:not(.completed):not(:disabled),
.habit-lab--dark .ingredient-btn:hover:not(:disabled) {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
  border-color: rgba(143, 154, 227, 0.18);
  color: rgba(226, 234, 255, 0.95);
}

.habit-lab--dark .ingredient-btn:nth-child(3n + 1),
.habit-lab--dark .ingredient-btn:nth-child(3n + 2),
.habit-lab--dark .ingredient-btn:nth-child(3n + 3) {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.03));
}

.habit-lab--dark .ingredient-image {
  background: rgba(255, 255, 255, 0.06);
}

.habit-lab--dark .ingredient-copy strong {
  color: rgba(226, 234, 255, 0.95);
}

.habit-lab--dark .clear-btn {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border-color: rgba(143, 154, 227, 0.28);
  color: #c7d2fe;
}

.habit-lab--dark .plus {
  color: #a5b4fc;
}

.habit-lab--dark .slot {
  border-color: rgba(143, 154, 227, 0.28);
  background: rgba(255, 255, 255, 0.05);
  border-style: solid;
  color: rgba(226, 234, 255, 0.88);
}

.habit-lab--dark .slot.burst {
  background: linear-gradient(180deg, rgba(99, 102, 241, 0.25), rgba(22, 28, 52, 0.92));
}

.habit-lab--dark .discoveries-panel li,
.habit-lab--dark .discoveries-panel .empty {
  color: rgba(210, 220, 255, 0.88);
}

.habit-lab--dark .discoveries-panel li strong {
  color: #f2f7ff;
}

.habit-lab--dark .score {
  border-color: rgba(143, 154, 227, 0.22);
  background: rgba(255, 255, 255, 0.06);
}

.habit-lab--dark .info-btn,
.habit-lab--dark .info-close {
  border-color: rgba(143, 154, 227, 0.35);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.05));
  color: #e0e7ff;
}

.habit-lab--dark .info-modal-backdrop {
  background: rgba(3, 7, 23, 0.62);
}

.habit-lab--dark .info-modal {
  background: rgba(18, 22, 43, 0.97);
  border-color: rgba(143, 154, 227, 0.22);
}

.habit-lab--dark .info-modal h4,
.habit-lab--dark .panel-kicker {
  color: rgba(226, 234, 255, 0.95);
}

.habit-lab--dark .info-list {
  color: rgba(210, 220, 255, 0.88);
}

.habit-lab--dark .combine-btn:not(:disabled) {
  border-color: rgba(143, 154, 227, 0.25);
}

.habit-lab--dark .result-box {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(143, 154, 227, 0.2);
}

.habit-lab--dark .result-box.success {
  background: rgba(44, 201, 122, 0.12);
}

.habit-lab--dark .result-box.fail {
  background: rgba(255, 126, 179, 0.1);
}

.habit-lab--dark .result-box strong {
  color: #f2f7ff;
}

.habit-lab--dark .result-box p {
  color: rgba(210, 220, 255, 0.9);
}

.habit-lab--dark .preview-card {
  background: rgba(14, 18, 40, 0.88);
  border-color: rgba(143, 154, 227, 0.2);
}

.habit-lab--dark .preview-label,
.habit-lab--dark .preview-copy p,
.habit-lab--dark .preview-copy h5 {
  color: rgba(226, 234, 255, 0.95);
}

.habit-lab--dark .video-shell {
  background: rgba(12, 16, 34, 0.9);
  border-color: rgba(143, 154, 227, 0.2);
}

.habit-lab--dark .video-heading h5,
.habit-lab--dark .video-heading span {
  color: rgba(226, 234, 255, 0.92);
}

.habit-lab--dark .video-frame {
  border-color: rgba(143, 154, 227, 0.25);
}

.habit-lab--dark .score span {
  color: rgba(198, 208, 240, 0.88);
}

.habit-lab--dark .score strong {
  color: #f2f7ff;
}

@keyframes unlockPulse {
  0% {
    transform: scale(0.98);
    box-shadow: 0 0 0 rgba(99, 91, 239, 0);
  }
  45% {
    transform: scale(1.02);
    box-shadow: 0 0 0 10px rgba(123, 101, 255, 0.08);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0 rgba(99, 91, 239, 0);
  }
}

@keyframes unlockPop {
  0% {
    transform: scale(0.94) translateY(6px);
    opacity: 0.72;
  }
  50% {
    transform: scale(1.03) translateY(-2px);
    opacity: 1;
  }
  100% {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

@media (max-width: 1180px) {
  .lab-shell {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 780px) {
  .mission-summary,
  .slots-header {
    grid-template-columns: 1fr;
    display: grid;
  }

  .summary-pill {
    min-width: 0;
  }

  .ingredient-grid {
    grid-template-columns: 1fr;
  }

  .slots {
    grid-template-columns: 1fr;
  }

  .plus {
    justify-self: center;
  }
}
</style>
  