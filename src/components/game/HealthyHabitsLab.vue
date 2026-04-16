<template>
    <section class="habit-lab">
      <header class="lab-header">
        <p class="lab-kicker">Discovery Lab</p>
        <h3>Mix two cards to unlock healthy habits</h3>
        <p>
          Tap two cards, combine them, and discover new actions just like a mini creation game.
        </p>
      </header>
  
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
  
      <div class="lab-shell">
        <aside class="ingredient-panel">
          <h4>{{ currentMission.title }} Cards</h4>
          <div class="ingredient-grid">
            <button
              v-for="item in currentMission.items"
              :key="item.id"
              type="button"
              class="ingredient-btn"
              @click="pickItem(item.id)"
              draggable="true"
              @dragstart="onDragStart($event, item.id)"
            >
              <span class="ingredient-illustration" aria-hidden="true">{{ item.icon }}</span>
              <span class="ingredient-label">{{ item.label }}</span>
            </button>
          </div>
        </aside>
  
        <div class="combine-panel">
          <div class="slots">
            <button
              type="button"
              class="slot"
              @click="clearSlot(0)"
              @dragover.prevent
              @drop="onSlotDrop($event, 0)"
              :draggable="Boolean(selected[0])"
              @dragstart="onSlotDragStart($event, 0)"
            >
              {{ slotLabel(0) }}
            </button>
            <span class="plus">+</span>
            <button
              type="button"
              class="slot"
              @click="clearSlot(1)"
              @dragover.prevent
              @drop="onSlotDrop($event, 1)"
              :draggable="Boolean(selected[1])"
              @dragstart="onSlotDragStart($event, 1)"
            >
              {{ slotLabel(1) }}
            </button>
          </div>
  
          <button type="button" class="combine-btn" :disabled="!canCombine" @click="combineSlots">
            Combine
          </button>
  
          <div class="result-box" :class="{ success: lastResult.success, fail: !lastResult.success }">
            <strong>{{ lastResult.title }}</strong>
            <p>{{ lastResult.message }}</p>
          </div>
        </div>
  
        <aside class="discoveries-panel">
          <h4>Discovered</h4>
          <ul>
            <li v-for="discovery in discoveryList" :key="discovery">{{ discovery }}</li>
            <li v-if="discoveryList.length === 0" class="empty">No discoveries yet.</li>
          </ul>
          <div class="score">
            <span>Stars</span>
            <strong>{{ stars }}</strong>
          </div>
        </aside>
      </div>
    </section>
  </template>
  
  <script setup>
  import { computed, reactive, ref } from "vue"
  
  const missions = [
    {
      id: "snack",
      title: "Snack Explorer",
      items: [
        { id: "apple", label: "Apple", icon: "🍎" },
        { id: "carrot", label: "Carrot", icon: "🥕" },
        { id: "yogurt", label: "Yogurt", icon: "🥣" },
        { id: "berries", label: "Berries", icon: "🫐" },
        { id: "nuts", label: "Nuts", icon: "🥜" },
      ],
      recipes: [
        {
          pair: ["apple", "yogurt"],
          result: "Crunch Cup",
          tip: "Awesome! Fruit + protein keeps your energy steady.",
        },
        {
          pair: ["carrot", "nuts"],
          result: "Rainbow Crunch Plate",
          tip: "Great mix. Color + crunch helps you feel full and strong.",
        },
        {
          pair: ["berries", "yogurt"],
          result: "Berry Power Bowl",
          tip: "Nice pick. This combo supports focus and growth.",
        },
        {
          pair: ["apple", "berries"],
          result: "Rainbow Fruit Mix",
          tip: "Great blend. Colorful fruit gives your body useful vitamins.",
        },
        {
          pair: ["apple", "carrot"],
          result: "Crunchy Duo",
          tip: "Nice crunch! A fresh combo that keeps snack time fun.",
        },
        {
          pair: ["apple", "nuts"],
          result: "Power Apple Bites",
          tip: "Excellent choice. Fiber plus healthy fats gives lasting energy.",
        },
        {
          pair: ["carrot", "yogurt"],
          result: "Veggie Dip Cup",
          tip: "Cool combo. Dips make veggies easier to enjoy.",
        },
        {
          pair: ["carrot", "berries"],
          result: "Color Blast Plate",
          tip: "Bright plate unlocked! Eating colors helps your body grow.",
        },
        {
          pair: ["yogurt", "nuts"],
          result: "Protein Crunch Bowl",
          tip: "Strong snack. Protein and crunch make a balanced bite.",
        },
        {
          pair: ["berries", "nuts"],
          result: "Trail Mix Twist",
          tip: "Great mission. Sweet + crunchy is a smart mini snack.",
        },
      ],
    },
    {
      id: "move",
      title: "Move and Groove",
      items: [
        { id: "jump", label: "Jump", icon: "🦘" },
        { id: "stretch", label: "Stretch", icon: "🤸" },
        { id: "dance", label: "Dance", icon: "💃" },
        { id: "balance", label: "Balance", icon: "🧘" },
        { id: "run", label: "Run", icon: "🏃" },
      ],
      recipes: [
        {
          pair: ["jump", "dance"],
          result: "Cardio Groove",
          tip: "Boom! Fast moves make your heart stronger.",
        },
        {
          pair: ["stretch", "balance"],
          result: "Calm Core Flow",
          tip: "Great control. Slow moves build balance and focus.",
        },
        {
          pair: ["run", "jump"],
          result: "Power Circuit",
          tip: "Awesome combo. You built a high-energy challenge.",
        },
        {
          pair: ["jump", "stretch"],
          result: "Jump and Reach",
          tip: "Great start. Big reaches help wake up your body.",
        },
        {
          pair: ["jump", "balance"],
          result: "Rocket Balance",
          tip: "Nice control! Quick jumps plus stillness build coordination.",
        },
        {
          pair: ["stretch", "dance"],
          result: "Flow Dance Warmup",
          tip: "Smooth move. Warm muscles help you move safely.",
        },
        {
          pair: ["stretch", "run"],
          result: "Runner Ready",
          tip: "Smart combo. Stretching before running protects your body.",
        },
        {
          pair: ["dance", "balance"],
          result: "Rhythm Balance",
          tip: "Amazing focus. Music and control are a strong team.",
        },
        {
          pair: ["dance", "run"],
          result: "Speed Groove",
          tip: "Energy boost unlocked! Fast feet and rhythm build stamina.",
        },
        {
          pair: ["balance", "run"],
          result: "Agility Quest",
          tip: "Nice challenge. Balance and running sharpen body control.",
        },
      ],
    },
    {
      id: "sleep",
      title: "Sleep Superpower",
      items: [
        { id: "tidy", label: "Tidy Toys", icon: "🧸" },
        { id: "brush", label: "Brush Teeth", icon: "🪥" },
        { id: "story", label: "Story Time", icon: "📖" },
        { id: "lights", label: "Dim Lights", icon: "🌙" },
        { id: "breath", label: "Slow Breaths", icon: "🫁" },
      ],
      recipes: [
        {
          pair: ["tidy", "brush"],
          result: "Ready for Bed",
          tip: "Nice start. A simple routine helps your brain wind down.",
        },
        {
          pair: ["story", "lights"],
          result: "Sleepy Mood",
          tip: "Perfect combo. Calm stories and low light help faster sleep.",
        },
        {
          pair: ["breath", "story"],
          result: "Dream Launch",
          tip: "Excellent! Calm breathing plus story makes bedtime smoother.",
        },
        {
          pair: ["tidy", "story"],
          result: "Calm Room Story",
          tip: "Great step. A tidy space helps your mind relax.",
        },
        {
          pair: ["tidy", "lights"],
          result: "Sleep Setup",
          tip: "Perfect prep. A calm room and dim light signal bedtime.",
        },
        {
          pair: ["tidy", "breath"],
          result: "Peaceful Start",
          tip: "Strong combo. Clean space and slow breaths lower stress.",
        },
        {
          pair: ["brush", "story"],
          result: "Cozy Routine",
          tip: "Nice flow. Consistent order makes bedtime easier each night.",
        },
        {
          pair: ["brush", "lights"],
          result: "Night Ready",
          tip: "Well done. Teeth done, lights low, body ready for rest.",
        },
        {
          pair: ["brush", "breath"],
          result: "Quiet Smile",
          tip: "Great calm-down combo before bed.",
        },
        {
          pair: ["lights", "breath"],
          result: "Moonlight Calm",
          tip: "Excellent! Soft light and breathing help faster sleep.",
        },
      ],
    },
  ]
  
  const activeMission = ref("snack")
  const selected = ref([null, null])
  const stars = ref(0)
  const discoveries = reactive({
    snack: new Set(),
    move: new Set(),
    sleep: new Set(),
  })
  const lastResult = reactive({
    success: true,
    title: "Pick two cards",
    message: "Try different pairs to unlock fun healthy discoveries.",
  })
  
  const currentMission = computed(() => missions.find(mission => mission.id === activeMission.value))
  const canCombine = computed(() => selected.value[0] && selected.value[1])
  const discoveryList = computed(() => Array.from(discoveries[activeMission.value]))
  
  function setMission(id) {
    activeMission.value = id
    selected.value = [null, null]
    lastResult.success = true
    lastResult.title = "Mission switched"
    lastResult.message = "Pick two cards to discover a new combo."
  }
  
  function pickItem(itemId) {
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
  
  function onDragStart(event, itemId) {
    event.dataTransfer.effectAllowed = "copyMove"
    event.dataTransfer.setData("text/plain", itemId)
  }
  
  function onSlotDragStart(event, index) {
    const itemId = selected.value[index]
    if (!itemId) return
    event.dataTransfer.effectAllowed = "move"
    event.dataTransfer.setData("text/plain", itemId)
  }
  
  function onSlotDrop(event, index) {
    const dragged = event.dataTransfer.getData("text/plain")
    if (!dragged) return
    const target = selected.value[index]
  
    if (!target) {
      selected.value[index] = dragged
      if (canCombine.value) combineSlots()
      return
    }
  
    if (target === dragged) return
    resolvePair(target, dragged)
  }
  
  function clearSlot(index) {
    selected.value[index] = null
  }
  
  function slotLabel(index) {
    const itemId = selected.value[index]
    if (!itemId) return "Pick card"
    const item = currentMission.value.items.find(entry => entry.id === itemId)
    return item ? item.label : "Pick card"
  }
  
  function combineSlots() {
    if (!canCombine.value) return
    const [first, second] = selected.value
    resolvePair(first, second)
  }
  
  function resolvePair(first, second) {
    const pair = [first, second].sort().join("+")
    const match = currentMission.value.recipes.find(recipe => recipe.pair.slice().sort().join("+") === pair)
    if (!match) {
      selected.value = [first, second]
      return
    }
  
    const seenBefore = discoveries[activeMission.value].has(match.result)
    discoveries[activeMission.value].add(match.result)
    if (!seenBefore) stars.value += 1
  
    lastResult.success = true
    lastResult.title = match.result
    lastResult.message = `${match.tip}${seenBefore ? " (Already discovered)" : " (+1 star)"}`
    selected.value = [null, null]
  }
  </script>
  
  <style scoped>
  .habit-lab {
    margin-top: 0;
    color: #1a2442;
  }
  
  .lab-header h3 {
    margin: 8px 0 0;
    font-size: 1.5rem;
  }
  
  .lab-header p {
    margin: 10px 0 0;
    color: #4a567b;
  }
  
  .lab-kicker {
    margin: 0;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 800;
    color: #4a5ad2;
  }
  
  .mission-tabs {
    display: flex;
    gap: 10px;
    margin-top: 18px;
    flex-wrap: wrap;
  }
  
  .mission-tab {
    border: 1px solid rgba(72, 91, 180, 0.26);
    background: #fff;
    color: #2a3f76;
    border-radius: 999px;
    min-height: 38px;
    padding: 0 12px;
    font-weight: 700;
    cursor: pointer;
  }
  
  .mission-tab.active {
    background: linear-gradient(135deg, #2e46dd 0%, #7a3df0 100%);
    color: #fff;
  }
  
  .lab-shell {
    margin-top: 14px;
    display: grid;
    grid-template-columns: 1fr 1fr 0.8fr;
    gap: 14px;
  }
  
  .ingredient-panel,
  .combine-panel,
  .discoveries-panel {
    border-radius: 20px;
    background: #fff;
    border: 1px solid rgba(68, 89, 160, 0.2);
    padding: 16px;
    box-shadow: 0 12px 24px rgba(21, 38, 86, 0.08);
  }
  
  .ingredient-panel h4,
  .discoveries-panel h4 {
    margin: 0 0 10px;
  }
  
  .ingredient-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }
  
  .ingredient-btn {
    border: 0;
    border-radius: 12px;
    min-height: 82px;
    font-weight: 700;
    cursor: pointer;
    background: #fff;
    color: #2f377d;
    display: grid;
    justify-items: center;
    align-content: center;
    gap: 6px;
    transition: transform 0.14s ease, box-shadow 0.14s ease;
    cursor: grab;
  }
  
  .ingredient-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(34, 48, 126, 0.18);
  }
  
  .ingredient-illustration {
    width: 34px;
    height: 34px;
    display: inline-grid;
    place-items: center;
    border-radius: 999px;
    background: linear-gradient(135deg, #f3f5ff 0%, #e6eaff 100%);
    font-size: 1.1rem;
  }
  
  .ingredient-label {
    font-size: 0.9rem;
  }
  
  .slots {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 8px;
  }
  
  .plus {
    font-size: 1.4rem;
    font-weight: 900;
  }
  
  .slot {
    border: 1px dashed rgba(62, 84, 152, 0.5);
    border-radius: 14px;
    min-height: 54px;
    background: #f2f5ff;
    color: #273661;
    font-weight: 700;
    cursor: grab;
  }
  
  .combine-btn {
    margin-top: 12px;
    width: 100%;
    min-height: 44px;
    border: 0;
    border-radius: 12px;
    font-weight: 800;
    cursor: pointer;
    color: #262a78;
    background: linear-gradient(135deg, #fff 0%, #dde2ff 100%);
  }
  
  .combine-btn:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
  
  .result-box {
    margin-top: 12px;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid rgba(68, 89, 160, 0.22);
  }
  
  .result-box.success {
    background: rgba(17, 132, 86, 0.14);
  }
  
  .result-box.fail {
    background: rgba(171, 54, 70, 0.14);
  }
  
  .result-box strong {
    display: block;
  }
  
  .result-box p {
    margin: 6px 0 0;
  }
  
  .discoveries-panel ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    gap: 8px;
  }
  
  .discoveries-panel li {
    border-radius: 10px;
    padding: 8px 10px;
    background: #f2f5ff;
  }
  
  .discoveries-panel .empty {
    color: #63709a;
  }
  
  .score {
    margin-top: 14px;
    border-radius: 14px;
    background: #15233f;
    padding: 10px 12px;
    display: grid;
    justify-items: center;
    color: #fff;
  }
  
  .score span {
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    opacity: 0.82;
  }
  
  .score strong {
    font-size: 1.45rem;
  }
  
  @media (max-width: 1080px) {
    .lab-shell {
      grid-template-columns: 1fr;
    }
  }
  </style>
  