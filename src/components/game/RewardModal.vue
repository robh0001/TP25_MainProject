<template>
  <Transition name="pop">
    <div v-if="reward" class="reward-overlay" @click.self="$emit('close')">
      <div class="reward-modal">
        <p class="panel-kicker">Quest complete!</p>
        <h3>🎉 {{ reward.title }}</h3>
        <p>{{ reward.message }}</p>
        <div class="reward-pills">
          <span>+{{ reward.xp }} XP</span>
          <span>+{{ reward.coins }} coins</span>
        </div>
        <button type="button" class="btn btn-coral" @click="$emit('close')">Continue adventure</button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  reward: {
    type: Object,
    default: null,
  },
})

defineEmits(['close'])
</script>
