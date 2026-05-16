<template>
  <div class="page-shell">
    <RouterView v-slot="{ Component, route }">
      <Transition name="page-slide" mode="out-in">
        <component :is="Component" :key="route.fullPath" />
      </Transition>
    </RouterView>
  </div>
</template>


<style scoped>
:global(.page-slide-enter-active),
:global(.page-slide-leave-active) {
  transition: opacity 0.28s ease, transform 0.28s ease, filter 0.28s ease;
}

:global(.page-slide-enter-from),
:global(.page-slide-leave-to) {
  opacity: 0;
  transform: translateY(12px) scale(0.985);
  filter: blur(4px);
}

:global(.page-slide-enter-to),
:global(.page-slide-leave-from) {
  opacity: 1;
  transform: translateY(0) scale(1);
  filter: blur(0);
}
</style>
