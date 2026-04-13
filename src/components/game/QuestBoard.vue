<template>
  <article class="adventure-panel quest-board">
    <div class="quest-header">
      <h3>Daily Quest Board</h3>
      <p>Quests reset daily. Complete all to boost your streak.</p>
    </div>

    <div class="quest-list">
      <QuestCard
        v-for="quest in quests"
        :key="quest.id"
        :quest="quest"
        :completed="completedQuestIds.includes(quest.id)"
        @complete="$emit('completeQuest', $event)"
      />
    </div>
  </article>
</template>

<script setup>
import QuestCard from './QuestCard.vue'

defineProps({
  quests: {
    type: Array,
    default: () => [],
  },
  completedQuestIds: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['completeQuest'])
</script>
