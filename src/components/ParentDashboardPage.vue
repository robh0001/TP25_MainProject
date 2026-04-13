<template>
    <main class="page-main container section-gap">
      <section class="dashboard-hero coral-soft">
        <div>
          <p class="eyebrow">Parent dashboard</p>
          <h1>Today’s family snapshot</h1>
          <p class="hero-subtext narrow-copy">
            A calm overview of what matters most today across meals, movement, sleep, and daily routine.
          </p>
        </div>
        <RouterLink to="/parent-quiz" class="btn btn-coral link-btn">Retake Quiz</RouterLink>
      </section>
  
      <section class="dashboard-grid">
        <article class="dashboard-card">
          <h3>Nutrition</h3>
          <p>Afternoon snacking is your biggest opportunity today.</p>
          <div class="metric-pill coral-pill">2 quick swap ideas ready</div>
        </article>
  
        <article class="dashboard-card">
          <h3>Physical Activity</h3>
          <p>Your child is most likely to engage after school for 15–20 minutes.</p>
          <div class="metric-pill mint-pill">Low-pressure option suggested</div>
        </article>
  
        <article class="dashboard-card">
          <h3>Sleep</h3>
          <p>Energy may be lower today based on last night’s bedtime pattern.</p>
          <div class="metric-pill sky-pill">Bedtime reset plan available</div>
        </article>
  
        <article class="dashboard-card">
          <h3>Routine</h3>
          <p>Focus on one change only this week to avoid overwhelm.</p>
          <div class="metric-pill lilac-pill">Weekly goal: snack reset</div>
        </article>
      </section>
  
      <section class="form-card action-card">
        <h2>Your next best action</h2>
        <p>
          Replace one afternoon processed snack with fruit and yogurt three times this week. Keep it visible and ready before school pickup.
        </p>
      </section>
    </main>
  </template>
  
  <script setup>
  </script>