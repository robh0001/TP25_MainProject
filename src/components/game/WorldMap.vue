<template>
  <article class="adventure-panel world-map">
    <div class="world-map-title">
      <h3>Adventure World Map</h3>
      <p>Travel the route, beat levels, and unlock the next world like a real adventure game.</p>
    </div>

    <div class="adventure-route">
      <div
        v-for="world in worlds"
        :key="world.id"
        class="world-route-card"
        :class="{
          unlocked: unlockedWorldIds.includes(world.id),
          active: activeWorldId === world.id,
        }"
      >
        <div class="world-route-head">
          <div class="world-icon">{{ world.icon }}</div>
          <div>
            <strong>{{ world.name }}</strong>
            <small v-if="unlockedWorldIds.includes(world.id)">World unlocked</small>
            <small v-else>Unlock at trainer level {{ world.unlockLevel }}</small>
          </div>
          <span class="world-badge">{{ unlockedWorldIds.includes(world.id) ? 'OPEN' : 'LOCKED' }}</span>
        </div>

        <div class="level-path">
          <div
            v-for="(levelItem, idx) in world.levels"
            :key="`${world.id}-${levelItem.level}`"
            class="level-node"
            :class="{
              reached: unlockedWorldIds.includes(world.id) && levelItem.level <= worldProgressLevel(world),
              current: activeWorldId === world.id && levelItem.level === worldProgressLevel(world),
              locked: !unlockedWorldIds.includes(world.id),
            }"
          >
            <span class="node-dot">{{ idx + 1 }}</span>
            <small>Lv {{ levelItem.level }}</small>
          </div>
        </div>

        <p class="world-focus">
          Focus: <strong>{{ world.theme }}</strong>
        </p>
      </div>
    </div>
  </article>
</template>

<script setup>
const props = defineProps({
  worlds: {
    type: Array,
    default: () => [],
  },
  unlockedWorldIds: {
    type: Array,
    default: () => [],
  },
  activeWorldId: {
    type: String,
    default: '',
  },
  playerLevel: {
    type: Number,
    default: 1,
  },
})

function worldProgressLevel(world) {
  if (!props.unlockedWorldIds.includes(world.id)) return 0
  const maxLevel = world.levels[world.levels.length - 1]?.level ?? 1
  return Math.max(1, Math.min(maxLevel, props.playerLevel - world.unlockLevel + 1))
}
</script>
