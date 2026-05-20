<!-- MainNav.vue -->
<template>
    <nav class="main-nav">
      <div class="main-nav-inner">
        <RouterLink to="/" class="main-nav-logo">
          <div class="main-nav-logo-icon">
            <svg viewBox="0 0 36 36" fill="none">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.5" />
              <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor" />
            </svg>
          </div>
          <span class="main-nav-logo-text">HealthyKids</span>
        </RouterLink>
  
        <div class="main-nav-links">
          <RouterLink to="/" class="main-nav-link" exact-active-class="active">Home</RouterLink>
          <RouterLink to="/parent-entry" class="main-nav-link" active-class="active">Dashboard</RouterLink>
          <RouterLink to="/parent-nutrition-tools" class="main-nav-link" active-class="active">Nutrition</RouterLink>
          <RouterLink to="/statistics" class="main-nav-link" active-class="active">Statistics</RouterLink>
          <RouterLink to="/kids-dashboard" class="main-nav-link" active-class="active">Kids view</RouterLink>
        </div>
  
        <div class="main-nav-actions">
          <RouterLink to="/parent-quiz" class="main-nav-link">Retake quiz</RouterLink>
          <RouterLink to="/parent-entry" class="main-nav-btn">
            <span>New Plan</span>
            <svg width="11" height="11" viewBox="0 0 12 12">
              <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </RouterLink>
        </div>
      </div>
    </nav>
  </template>
  