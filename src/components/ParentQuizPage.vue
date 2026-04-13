<template>
    <main class="page-main container section-gap">
      <section class="form-hero parent-quiz-hero">
        <p class="eyebrow">Parent onboarding</p>
        <h1>Let’s find your family’s best starting point</h1>
        <p class="hero-subtext narrow-copy">
          Answer a few quick questions so HealthySteps can tailor realistic recommendations for your child and your routine.
        </p>
      </section>
  
      <section class="form-card">
        <div class="form-grid">
          <div class="form-group">
            <label>Child age range</label>
            <select>
              <option>5–7 years</option>
              <option>8–10 years</option>
              <option>11–12 years</option>
            </select>
          </div>
  
          <div class="form-group">
            <label>Primary concern</label>
            <select>
              <option>Nutrition</option>
              <option>Physical activity</option>
              <option>Sleep</option>
              <option>Routine consistency</option>
            </select>
          </div>
  
          <div class="form-group full-row">
            <label>Biggest daily struggle</label>
            <textarea rows="4" placeholder="For example: after-school snacking, too much screen time, refusing vegetables..."></textarea>
          </div>
  
          <div class="form-group">
            <label>How confident do you feel making changes?</label>
            <select>
              <option>Very confident</option>
              <option>Somewhat confident</option>
              <option>Not very confident</option>
            </select>
          </div>
  
          <div class="form-group">
            <label>Preferred support style</label>
            <select>
              <option>Gentle weekly suggestions</option>
              <option>Step-by-step daily actions</option>
              <option>Visual dashboard summaries</option>
            </select>
          </div>
        </div>
  
        <div class="form-actions">
          <RouterLink to="/parent-dashboard" class="btn btn-coral link-btn">See My Starting Plan</RouterLink>
        </div>
      </section>
    </main>
  </template>
  
  <script setup>
  import { RouterLink } from 'vue-router'
  </script>