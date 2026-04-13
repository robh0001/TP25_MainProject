<template>
    <section id="how-it-works" class="how-section split-bg section-gap">
      <div class="container">
        <div class="section-heading center narrow">
          <h2>How It Works</h2>
          <p>Three simple steps to transform your family’s wellness journey</p>
        </div>
  
        <div class="steps-grid">
          <article class="step-card" v-for="step in steps" :key="step.title">
            <h4>{{ step.title }}</h4>
            <p>{{ step.description }}</p>
          </article>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  const steps = [
    {
      title: 'Choose a Challenge',
      description: 'Select from pre-made challenges or create your own custom family goal.',
    },
    {
      title: 'Complete Together',
      description: 'Work as a family unit. Everyone participates, no one gets singled out.',
    },
    {
      title: 'Earn Rewards',
      description: 'Celebrate success with meaningful, non-food rewards your family chooses together.',
    },
  ]
  </script>