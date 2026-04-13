<template>
    <section id="resources" class="tools-section container section-gap">
      <div class="section-heading center">
        <h2>Start right now. No sign-up needed.</h2>
        <p>
          Every core tool works instantly. Create an account later to save progress and unlock
          your dashboard.
        </p>
      </div>
  
      <div class="tool-grid three">
        <article class="mini-tool" v-for="tool in tools" :key="tool.title">
          <div class="tool-icon" :class="tool.className">{{ tool.icon }}</div>
          <h4>{{ tool.title }}</h4>
          <p>{{ tool.description }}</p>
          <a href="#">{{ tool.linkText }}</a>
        </article>
      </div>
    </section>
  </template>
  
  <script setup>
  const tools = [
    {
      icon: '🍽️',
      title: 'Meal Builder',
      description: 'Mix and match healthy Aussie meals your family will actually eat.',
      linkText: 'Try now',
      className: 'lilac',
    },
    {
      icon: '🏃',
      title: 'Activity Finder',
      description: 'Discover fun ways to move that don’t feel like exercise.',
      linkText: 'Explore',
      className: 'mint',
    },
    {
      icon: '🌙',
      title: 'Sleep Tracker',
      description: 'See how sleep connects to energy and mood.',
      linkText: 'Start tracking',
      className: 'sky',
    },
  ]
  </script>