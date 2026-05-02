<template>
  <div class="roadmap-page">
    <header class="header">
      <div class="header-inner">
        <RouterLink to="/" class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 36 36" fill="none">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2" />
              <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor" />
              <path d="M18 13C15.5 15.5 15 19 18 23" stroke="white" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.55" />
            </svg>
          </div>
          <span class="logo-text">HealthyKids</span>
        </RouterLink>

        <nav class="nav">
          <RouterLink to="/parent-dashboard" class="nav-a">Parent dashboard</RouterLink>
          <RouterLink to="/parent-nutrition-tools" class="nav-a">Nutrition tools</RouterLink>
          <RouterLink to="/parent-entry" class="nav-a">Parent access</RouterLink>
          <RouterLink to="/young-person-dashboard" class="nav-a">Kids dashboard</RouterLink>
        </nav>

        <div class="nav-cta">
          <RouterLink to="/parent-nutrition-tools" class="nav-link">Nutrition tools</RouterLink>
          <RouterLink to="/parent-quiz" class="nav-link">Retake quiz</RouterLink>
          <RouterLink to="/parent-dashboard" class="nav-btn">
            Back to dashboard
            <svg width="12" height="12" viewBox="0 0 12 12">
              <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </RouterLink>
        </div>
      </div>
    </header>

    <main>
      <section class="hero">
        <div class="hero-bg">
          <span class="hero-orb orb-a"></span>
          <span class="hero-orb orb-b"></span>
          <span class="hero-orb orb-c"></span>
          <span class="hero-grid-lines"></span>
        </div>
        <div class="hero-wrap">
          <div class="hero-copy-col">
            <div class="section-eyebrow">User Story 4.1 + 4.2</div>
            <h1 class="hero-title">
              4-week roadmap and<br />
              <em>weekly habit progress.</em>
            </h1>
            <p class="hero-copy">
              A dedicated parent page for tracking {{ childName }}'s weekly progress, reviewing the
              personalised 4-week habit roadmap, and getting simple feedback that supports consistent
              behaviour change over time.
            </p>
            <div class="hero-tags">
              <span class="hero-tag">{{ focusLabel }} focus</span>
              <span class="hero-tag">{{ state.ageRange || 'Ages 5-12' }}</span>
              <span class="hero-tag">{{ state.supportStyle || 'Weekly family plan' }}</span>
            </div>
            <div class="roadmap-hero-actions">
              <RouterLink to="/parent-entry" class="hero-action-solid">Parent access</RouterLink>
              <RouterLink to="/parent-quiz" class="hero-action-ghost">Build or refresh plan</RouterLink>
            </div>

            <div class="hero-micro-stats">
              <div class="hero-micro-card">
                <span>Current momentum</span>
                <strong>{{ roadmapMomentumLabel }}</strong>
              </div>
              <div class="hero-micro-card">
                <span>Best day</span>
                <strong>{{ strongestDay.label }}</strong>
              </div>
              <div class="hero-micro-card">
                <span>Focus</span>
                <strong>{{ focusLabel }}</strong>
              </div>
            </div>
          </div>

          <div class="hero-visual-board">
            <div class="hero-ring-panel">
              <div class="hero-ring-shell" :style="roadmapRingStyle">
                <div class="hero-ring-core">
                  <span>Roadmap</span>
                  <strong>{{ roadmapCompletion }}%</strong>
                  <small>{{ completedRoadmapActions }}/{{ totalRoadmapActions }}</small>
                </div>
              </div>
              <div class="hero-selected-chip" :class="selectedRoadmapWeek.theme">
                {{ selectedRoadmapWeek.icon }} Week {{ selectedRoadmapWeek.week }}
              </div>
            </div>

            <div class="hero-side-stack">
              <article class="hero-kpi-card glass">
                <span>Current week</span>
                <strong>Week {{ currentWeek }}</strong>
                <p>{{ selectedRoadmapWeek.status }}</p>
              </article>
              <article class="hero-kpi-card glass">
                <span>Simple feedback</span>
                <strong>{{ selectedRoadmapWeek.feedbackCue }}</strong>
                <p>{{ selectedRoadmapWeek.feedbackNextStep }}</p>
              </article>
              <article class="hero-kpi-card dark spotlight">
                <span>Consistency gap</span>
                <strong>{{ weeklyConsistencyGap }}%</strong>
                <p>{{ weakestDay.fullLabel }} to {{ strongestDay.fullLabel }}</p>
              </article>
            </div>
          </div>
        </div>
      </section>

      <section v-if="hasPlanData" class="overview-section">
        <div class="section-wrap">
          <div class="overview-grid">
            <article class="overview-card accent">
              <span class="overview-label">Weeks started</span>
              <strong>{{ startedWeeksCount }}<small>/4</small></strong>
              <p>{{ completedWeeksCount }} weeks completed so far.</p>
            </article>
            <article class="overview-card">
              <span class="overview-label">Best day this week</span>
              <strong>{{ strongestDay.fullLabel }}</strong>
              <p>{{ strongestDay.value }}% completion on the strongest day.</p>
            </article>
            <article class="overview-card">
              <span class="overview-label">Consistency gap</span>
              <strong>{{ weeklyConsistencyGap }}<small>%</small></strong>
              <p>Difference between strongest and weakest day.</p>
            </article>
            <article class="overview-card dark">
              <span class="overview-label">Momentum</span>
              <strong>{{ roadmapMomentumLabel }}</strong>
              <p>{{ selectedRoadmapWeek.feedbackCue }} for Week {{ selectedRoadmapWeek.week }}.</p>
            </article>
          </div>

          <div class="visual-dashboard-grid">
            <article class="journey-panel">
              <div class="journey-head">
                <div>
                  <div class="journey-kicker">4-week journey</div>
                  <h3 class="journey-title">Tap any week to inspect progress</h3>
                </div>
                <div class="journey-total">{{ roadmapCompletion }}%</div>
              </div>
              <div class="journey-track-wrap">
                <button
                  v-for="week in fourWeekRoadmap"
                  :key="week.id"
                  class="journey-node"
                  :class="[week.statusKey, { active: week.id === activeRoadmapWeek }]"
                  @click="activeRoadmapWeek = week.id"
                >
                  <span class="journey-node-ring">{{ week.week }}</span>
                  <span class="journey-node-label">Week {{ week.week }}</span>
                  <span class="journey-node-pct">{{ week.progress }}%</span>
                </button>
              </div>
              <div class="journey-bars">
                <div v-for="week in fourWeekRoadmap" :key="week.id" class="journey-bar-col">
                  <div class="journey-bar-track">
                    <div class="journey-bar-fill" :class="'fill-' + week.statusKey" :style="{ height: week.progress + '%' }"></div>
                  </div>
                  <span>W{{ week.week }}</span>
                </div>
              </div>
            </article>

            <article class="heatmap-panel">
              <div class="journey-head">
                <div>
                  <div class="journey-kicker">This week's rhythm</div>
                  <h3 class="journey-title">Daily completion heatmap</h3>
                </div>
                <div class="journey-total">{{ weeklyAverage }}%</div>
              </div>
              <div class="heatmap-grid">
                <button
                  v-for="day in weeklyProgress"
                  :key="day.label"
                  class="heatmap-day"
                  :class="{ active: selectedDayLabel === day.label }"
                  @click="selectedDayLabel = day.label"
                >
                  <span class="heatmap-day-label">{{ day.label }}</span>
                  <span class="heatmap-day-box" :style="{ opacity: 0.22 + day.value / 130 }"></span>
                  <span class="heatmap-day-value">{{ day.value }}%</span>
                </button>
              </div>
              <div class="heatmap-foot">
                <span>Lowest: {{ weakestDay.fullLabel }} {{ weakestDay.value }}%</span>
                <span>Highest: {{ strongestDay.fullLabel }} {{ strongestDay.value }}%</span>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section v-if="!hasPlanData" class="empty-state-section">
        <div class="section-wrap">
          <div class="empty-state-card">
            <div>
              <div class="section-eyebrow">Plan setup</div>
              <h2 class="section-h2">No saved family plan yet.</h2>
              <p class="section-desc">
                This roadmap page is fully ready, but it works best once a parent profile and quiz-based
                habit plan have been created. Start the parent flow to generate a personalised 4-week
                roadmap for your child.
              </p>
            </div>
            <div class="empty-state-actions">
              <RouterLink to="/parent-entry" class="hero-action-solid">Go to parent access</RouterLink>
              <RouterLink to="/parent-quiz" class="hero-action-ghost">Start the onboarding quiz</RouterLink>
            </div>
          </div>
        </div>
      </section>

      <section class="roadmap-section">
        <div class="section-wrap">
          <div class="section-head-row">
            <div class="section-head-left">
              <div class="section-eyebrow">4-week habit roadmap · Acceptance Criteria 4.1.1</div>
              <h2 class="section-h2">
                One main focus,<br />
                <em>one action, one tip.</em>
              </h2>
              <p class="section-desc">
                Each week below clearly shows one main focus, one key action, and one support tip,
                while the progress feedback stays visible and easy for parents to follow.
              </p>
            </div>

            <div class="roadmap-score-block">
              <div class="rsb-ring" :style="roadmapRingStyle">
                <div class="rsb-ring-inner">
                  <div class="rsb-pct">{{ roadmapCompletion }}<span>%</span></div>
                  <div class="rsb-lbl">complete</div>
                </div>
              </div>
              <div class="rsb-meta">
                <div class="rsb-num">{{ completedRoadmapActions }}<span>/{{ totalRoadmapActions }}</span></div>
                <div class="rsb-desc">roadmap items completed</div>
                <div class="rsb-focus-chip">Focus: {{ focusLabel }}</div>
              </div>
            </div>
          </div>

          <div class="roadmap-weeks">
            <button
              v-for="week in fourWeekRoadmap"
              :key="week.id"
              class="rweek-card"
              :class="{
                active: week.id === activeRoadmapWeek,
                completed: week.statusKey === 'completed',
                'in-progress': week.statusKey === 'in-progress'
              }"
              @click="activeRoadmapWeek = week.id"
            >
              <div class="rweek-top">
                <span class="rweek-num">Week {{ week.week }}</span>
                <span class="rweek-status" :class="'rs-' + week.statusKey">{{ week.status }}</span>
              </div>
              <div class="rweek-icon" :class="week.theme">{{ week.icon }}</div>
              <h3 class="rweek-title">{{ week.focus }}</h3>
              <p class="rweek-summary">{{ week.summary }}</p>
              <div class="rweek-meta-block">
                <div class="rweek-meta-item">
                  <span class="rweek-meta-label">Action</span>
                  <p class="rweek-meta-text">{{ week.mainAction }}</p>
                </div>
                <div class="rweek-meta-item">
                  <span class="rweek-meta-label">Support tip</span>
                  <p class="rweek-meta-text">{{ week.supportTip }}</p>
                </div>
              </div>
              <div class="rweek-progress-wrap">
                <div class="rweek-track">
                  <div class="rweek-fill" :style="{ width: week.progress + '%' }"></div>
                </div>
                <span class="rweek-pct">{{ week.progress }}%</span>
              </div>
              <div class="rweek-done-count">{{ week.completed }}/{{ week.totalItems }} items</div>
            </button>
          </div>

          <div class="roadmap-detail">
            <div class="roadmap-detail-main">
              <div class="rdm-header">
                <div>
                  <div class="rdm-eyebrow">Selected · Week {{ selectedRoadmapWeek.week }}</div>
                  <h3 class="rdm-title">{{ selectedRoadmapWeek.title }}</h3>
                </div>
                <div class="rdm-week-badge" :class="selectedRoadmapWeek.theme">
                  {{ selectedRoadmapWeek.icon }} Week {{ selectedRoadmapWeek.week }}
                </div>
              </div>

              <div class="rdm-story-strip">
                <article class="rdm-story-card primary">
                  <span>Week story</span>
                  <strong>{{ selectedRoadmapWeek.summary }}</strong>
                  <p>{{ selectedRoadmapWeek.detail }}</p>
                </article>
                <article class="rdm-story-card">
                  <span>Strongest day</span>
                  <strong>{{ strongestDay.label }}</strong>
                  <p>{{ strongestDay.value }}% completion</p>
                </article>
                <article class="rdm-story-card">
                  <span>Feedback cue</span>
                  <strong>{{ selectedRoadmapWeek.feedbackCue }}</strong>
                  <p>{{ roadmapMomentumLabel }} momentum</p>
                </article>
              </div>

              <div class="mini-day-bars">
                <button
                  v-for="day in weeklyProgress"
                  :key="day.label"
                  class="mini-day-bar"
                  :class="{ active: selectedDayLabel === day.label }"
                  @click="selectedDayLabel = day.label"
                >
                  <span class="mini-day-bar-fill" :style="{ height: Math.max(day.value, 8) + '%' }"></span>
                  <span class="mini-day-bar-label">{{ day.label }}</span>
                </button>
              </div>

              <div class="rdm-visual-stats">
                <article class="rdm-visual-card">
                  <span>Week progress</span>
                  <strong>{{ selectedRoadmapWeek.progress }}%</strong>
                  <p>{{ selectedRoadmapWeek.status }}</p>
                </article>
                <article class="rdm-visual-card">
                  <span>Action completion</span>
                  <strong>{{ selectedWeekActionCompletion }}%</strong>
                  <p>{{ selectedRoadmapWeek.weeklyCompleted }}/{{ selectedRoadmapWeek.actions.length }} actions</p>
                </article>
                <article class="rdm-visual-card">
                  <span>Daily completion</span>
                  <strong>{{ selectedWeekDailyCompletion }}%</strong>
                  <p>{{ selectedRoadmapWeek.dailyCompleted }}/{{ selectedRoadmapWeek.dailyTotal }} schedule items</p>
                </article>
                <article class="rdm-visual-card accent">
                  <span>Open items</span>
                  <strong>{{ selectedWeekOpenItems }}</strong>
                  <p>Remaining this week</p>
                </article>
              </div>

              <div class="rdm-template-grid">
                <article class="rdm-template-card">
                  <span class="rdm-template-label">Main focus</span>
                  <h4 class="rdm-template-value">{{ selectedRoadmapWeek.focus }}</h4>
                </article>
                <article class="rdm-template-card">
                  <span class="rdm-template-label">Weekly action</span>
                  <p class="rdm-template-value body">{{ selectedRoadmapWeek.mainAction }}</p>
                </article>
                <article class="rdm-template-card">
                  <span class="rdm-template-label">Support tip</span>
                  <p class="rdm-template-value body">{{ selectedRoadmapWeek.supportTip }}</p>
                </article>
              </div>

              <div class="rdm-actions-head">
                <span>Core actions this week</span>
                <span class="rdm-actions-count">{{ selectedRoadmapWeek.weeklyCompleted }}/{{ selectedRoadmapWeek.actions.length }} done</span>
              </div>

              <div class="rdm-actions-list">
                <label
                  v-for="action in selectedRoadmapWeek.actions"
                  :key="action.id"
                  class="rdm-action"
                  :class="{ done: action.done }"
                >
                  <input type="checkbox" :checked="action.done" @change="toggleRoadmapAction(action.id)" />
                  <span class="rdm-check" :class="{ done: action.done }">
                    <svg v-if="action.done" width="10" height="10" viewBox="0 0 10 10">
                      <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </span>
                  <span class="rdm-action-text">{{ action.text }}</span>
                </label>
              </div>

              <div class="rdm-day-plan-block">
                <div class="rdm-day-plan-head">
                  <div>
                    <span>Daily schedule for Week {{ selectedRoadmapWeek.week }}</span>
                    <p>
                      Time-blocked support tailored to {{ childName }} and organised around {{ focusLabel.toLowerCase() }}
                      with clear daily progress.
                    </p>
                  </div>
                  <strong>{{ selectedRoadmapWeek.dailyCompleted }}/{{ selectedRoadmapWeek.dailyTotal }} done</strong>
                </div>

                <div class="day-chip-strip">
                  <button
                    v-for="day in weeklyProgress"
                    :key="day.label"
                    class="day-chip"
                    :class="{ active: selectedDayLabel === day.label }"
                    @click="selectedDayLabel = day.label"
                  >
                    <span>{{ day.label }}</span>
                    <strong>{{ day.value }}%</strong>
                  </button>
                </div>

                <div class="rdm-day-plan-grid">
                  <article
                    v-for="day in currentFirstRoadmapDailyPlan"
                    :key="day.day"
                    class="rdm-day-card"
                    :class="{ today: day.day === todayName }"
                  >
                    <div class="rdm-day-card-head">
                      <div>
                        <span class="rdm-day-name">{{ getShortDayName(day.day) }}</span>
                        <small v-if="day.day === todayName">Today</small>
                      </div>
                      <strong>{{ day.completed }}/{{ day.timeSlots.length }}</strong>
                    </div>

                    <div class="rdm-day-mini-track">
                      <div class="rdm-day-mini-fill" :style="{ width: day.progress + '%' }"></div>
                    </div>

                    <div class="rdm-day-schedule">
                      <div
                        v-for="slot in day.timeSlots"
                        :key="slot.id"
                        class="rdm-time-slot"
                        :class="['slot-' + slot.category, { done: slot.done }]"
                      >
                        <div class="slot-time-col">
                          <span class="slot-time">{{ slot.time }}</span>
                          <span class="slot-cat-dot"></span>
                        </div>
                        <label class="slot-action-col">
                          <input type="checkbox" :checked="slot.done" @change="toggleRoadmapDailyAction(slot.id)" />
                          <span class="slot-check" :class="{ done: slot.done }">
                            <svg v-if="slot.done" width="8" height="8" viewBox="0 0 8 8">
                              <path d="M1.5 4l2 2 3-3" stroke="white" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" />
                            </svg>
                          </span>
                          <div class="slot-text-wrap">
                            <span class="slot-text">{{ slot.text }}</span>
                            <span v-if="slot.tip" class="slot-tip">{{ slot.tip }}</span>
                          </div>
                        </label>
                      </div>
                    </div>
                  </article>
                </div>

                <div class="schedule-legend">
                  <div v-for="cat in scheduleCategories" :key="cat.key" class="legend-item" :class="'legend-' + cat.key">
                    <span class="legend-dot"></span>
                    <span>{{ cat.label }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="roadmap-feedback-panel">
              <div class="rfp-status-row">
                <div class="rfp-status-indicator" :class="'rfi-' + selectedRoadmapWeek.statusKey">
                  <svg v-if="selectedRoadmapWeek.statusKey === 'completed'" width="18" height="18" viewBox="0 0 18 18">
                    <path d="M3 9l4 4 8-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <svg v-else-if="selectedRoadmapWeek.statusKey === 'in-progress'" width="18" height="18" viewBox="0 0 18 18">
                    <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.5" />
                    <path d="M9 5v4l2.5 2.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                  </svg>
                  <svg v-else width="18" height="18" viewBox="0 0 18 18">
                    <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.5" />
                    <path d="M9 6v4M9 12v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                  </svg>
                </div>
                <div>
                  <div class="rfp-status-label">Weekly progress · Story 4.2</div>
                  <div class="rfp-status-text">{{ selectedRoadmapWeek.status }}</div>
                </div>
              </div>

              <div class="rfp-progress-donut">
                <svg width="88" height="88" viewBox="0 0 88 88">
                  <circle cx="44" cy="44" r="36" stroke="rgba(255,255,255,0.12)" stroke-width="8" fill="none" />
                  <circle
                    cx="44" cy="44" r="36"
                    :stroke="selectedRoadmapWeek.statusKey === 'completed' ? '#4ade80' : selectedRoadmapWeek.statusKey === 'in-progress' ? '#fbbf24' : '#64748b'"
                    stroke-width="8"
                    fill="none"
                    stroke-linecap="round"
                    :stroke-dasharray="`${(selectedRoadmapWeek.progress / 100) * 226} 226`"
                    transform="rotate(-90 44 44)"
                  />
                  <text x="44" y="49" text-anchor="middle" font-size="14" font-weight="700" fill="#ffffff">{{ selectedRoadmapWeek.progress }}%</text>
                </svg>
              </div>

              <div class="rfp-feedback-block">
                <div class="rfp-fb-title">{{ selectedRoadmapWeek.feedbackTitle }}</div>
                <p class="rfp-fb-body">{{ selectedRoadmapWeek.feedback }}</p>
              </div>

              <div class="rfp-signal-row">
                <div class="rfp-signal-card">
                  <span>Completed</span>
                  <strong>{{ selectedRoadmapWeek.completed }}</strong>
                </div>
                <div class="rfp-signal-card">
                  <span>Remaining</span>
                  <strong>{{ selectedWeekOpenItems }}</strong>
                </div>
                <div class="rfp-signal-card">
                  <span>Daily avg</span>
                  <strong>{{ weeklyAverage }}%</strong>
                </div>
              </div>

              <div class="rfp-guidance-grid">
                <div class="rfp-guidance-card">
                  <div class="rfp-guidance-label">Status update</div>
                  <div class="rfp-guidance-value">{{ selectedRoadmapWeek.status }}</div>
                  <p>{{ selectedRoadmapWeek.statusSummary }}</p>
                </div>
                <div class="rfp-guidance-card">
                  <div class="rfp-guidance-label">Simple feedback</div>
                  <div class="rfp-guidance-value">{{ selectedRoadmapWeek.feedbackCue }}</div>
                  <p>{{ selectedRoadmapWeek.feedbackNextStep }}</p>
                </div>
              </div>

              <div class="rfp-quiz-insights">
                <div class="rfp-qi-head">Plan tailored for</div>
                <div class="rfp-qi-chips">
                  <span v-for="tag in planTags" :key="tag" class="rfp-qi-chip">{{ tag }}</span>
                </div>
              </div>

              <div class="rfp-tip">
                <div class="rfp-tip-head">Parent tip</div>
                <p>{{ selectedRoadmapWeek.parentTip }}</p>
              </div>

              <div class="rfp-all-weeks">
                <div class="rfp-aw-head">All weeks at a glance</div>
                <div class="rfp-week-bars">
                  <div
                    v-for="week in fourWeekRoadmap"
                    :key="week.id"
                    class="rfp-wbar-col"
                    :class="{ current: week.id === activeRoadmapWeek }"
                  >
                    <div class="rfp-wbar-track">
                      <div class="rfp-wbar-fill" :class="'rfp-wfill-' + week.statusKey" :style="{ height: week.progress + '%' }"></div>
                    </div>
                    <div class="rfp-wbar-label">W{{ week.week }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="insights-section">
        <div class="section-wrap insights-grid">
          <div class="insight-dark-card">
            <div class="tcc-eyebrow">This week's focus</div>
            <h3 class="tcc-title">{{ weeklyNarrativeTitle }}</h3>
            <div class="narrative-chip-row">
              <span class="narrative-chip">{{ focusLabel }}</span>
              <span class="narrative-chip">{{ selectedRoadmapWeek.status }}</span>
              <span class="narrative-chip">{{ weeklyAverage }}% avg</span>
            </div>
            <p class="tcc-body">{{ weeklyNarrative }}</p>
            <div class="tcc-facts">
              <div class="tcc-fact">
                <div class="tcc-fact-label">Expected win</div>
                <div class="tcc-fact-val">{{ winNarrative }}</div>
              </div>
              <div class="tcc-fact">
                <div class="tcc-fact-label">Support style</div>
                <div class="tcc-fact-val">{{ state.supportStyle || 'Weekly family plan' }}</div>
              </div>
            </div>
            <div class="category-mix">
              <div v-for="cat in selectedWeekCategoryMix" :key="cat.key" class="mix-row">
                <div class="mix-row-top">
                  <span>{{ cat.label }}</span>
                  <strong>{{ cat.count }}</strong>
                </div>
                <div class="mix-row-track">
                  <div class="mix-row-fill" :class="'mix-' + cat.key" :style="{ width: cat.percent + '%' }"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="insight-light-card">
            <div class="twc-eyebrow">Risk to watch</div>
            <h3 class="twc-title">If this week stalls</h3>
            <div class="risk-pill-row">
              <span class="risk-pill">{{ weakestDay.fullLabel }}</span>
              <span class="risk-pill">{{ selectedWeekOpenItems }} open</span>
            </div>
            <p class="twc-body">{{ riskNarrative }}</p>
            <div class="risk-stats">
              <div class="risk-stat">
                <span>Weakest day</span>
                <strong>{{ weakestDay.label }}</strong>
              </div>
              <div class="risk-stat">
                <span>Open items</span>
                <strong>{{ selectedRoadmapWeek.totalItems - selectedRoadmapWeek.completed }}</strong>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="chart-section">
        <div class="section-wrap">
          <div class="chart-head-row">
            <div>
              <div class="section-eyebrow">Weekly progress</div>
              <h2 class="section-h2">
                7-day consistency<br />
                <em>for the selected week.</em>
              </h2>
            </div>
            <div class="chart-avg-block">
              <div class="cab-val">{{ weeklyAverage }}<span>%</span></div>
              <div class="cab-lbl">Weekly average</div>
            </div>
          </div>

          <div class="chart-card">
            <div class="chart-bars-wrap">
              <button
                v-for="day in weeklyProgress"
                :key="day.label"
                class="cbar-col"
                :class="{ active: selectedDayLabel === day.label }"
                @click="selectedDayLabel = day.label"
              >
                <div class="cbar-val">{{ day.value }}%</div>
                <div class="cbar-track">
                  <div class="cbar-fill" :style="{ height: day.value + '%' }"></div>
                </div>
                <div class="cbar-lbl">{{ day.label }}</div>
              </button>
            </div>

            <div class="chart-detail">
              <div class="cd-eyebrow">Selected day</div>
              <h3 class="cd-day">{{ selectedDay.fullLabel }}</h3>
              <div class="cd-score">{{ selectedDay.value }}<span>%</span></div>
              <p class="cd-meta">{{ selectedDay.completed }} of {{ selectedDay.total }} schedule items completed</p>
              <div class="cd-tasks">
                <div v-for="task in selectedDay.tasks" :key="task.id" class="cd-task" :class="{ done: task.done }">
                  <span class="cd-task-dot"></span>
                  <span>{{ task.text }}</span>
                </div>
                <p v-if="!selectedDay.tasks.length" class="cd-empty">No tasks for this day.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'

const { state, savePlan } = useFamilyPlanStore()

const TIME_ZONE = 'Australia/Melbourne'
const LOCALE = 'en-AU'
const DAY_LABEL_LENGTH = 3
const API_BASE_URL = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL

const orderedDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
const scheduleCategories = [
  { key: 'nutrition', label: 'Nutrition' },
  { key: 'movement', label: 'Movement' },
  { key: 'sleep', label: 'Sleep / Wind-down' },
  { key: 'routine', label: 'Routine' },
  { key: 'family', label: 'Family time' },
]

const activeRoadmapWeek = ref(1)
const selectedDayLabel = ref(getShortDayName(getTodayName()))

function getTodayName() {
  return new Date().toLocaleDateString(LOCALE, {
    weekday: 'long',
    timeZone: TIME_ZONE,
  })
}

function getShortDayName(dayName) {
  return dayName.slice(0, DAY_LABEL_LENGTH)
}

function getApproxAge(ageRange) {
  if (!ageRange) return 8
  const match = String(ageRange).match(/(\d+)\s*-\s*(\d+)/)
  if (!match) return 8
  const min = Number(match[1])
  const max = Number(match[2])
  if (Number.isNaN(min) || Number.isNaN(max)) return 8
  return Math.round((min + max) / 2)
}

const childName = computed(() => state.childName || 'Your child')
const todayName = computed(() => getTodayName())
const hasPlanData = computed(() =>
  Boolean(
    state.username ||
    state.childName ||
    state.ageRange ||
    (state.concerns && state.concerns.length) ||
    state.supportStyle
  )
)

const primaryConcern = computed(() => {
  const concerns = state.concerns || []
  if (concerns.includes('Sleep consistency') || concerns.includes('Bedtime feels inconsistent')) return 'sleep'
  if (concerns.includes('Nutrition') || concerns.includes('My child snacks too often')) return 'nutrition'
  if (concerns.includes('Physical activity') || concerns.includes('My child is not active enough')) return 'movement'
  if (concerns.includes('Routine battles') || concerns.includes('Our family routine feels hard to manage')) return 'routine'
  return 'balanced'
})

const focusLabel = computed(() => {
  const labels = { sleep: 'Sleep', nutrition: 'Nutrition', movement: 'Movement', routine: 'Routine', balanced: 'Balanced' }
  return labels[primaryConcern.value] || 'Balanced'
})

const planTags = computed(() => {
  const tags = []
  if (childName.value && childName.value !== 'Your child') tags.push(childName.value)
  if (state.ageRange) tags.push(state.ageRange)
  if (primaryConcern.value !== 'balanced') tags.push(focusLabel.value + ' focus')
  if (state.supportStyle) tags.push(state.supportStyle)
  return tags.slice(0, 4)
})

const weeklyNarrativeTitle = computed(() => {
  const c = state.concerns || []
  if (c.includes('Sleep consistency') || c.includes('Bedtime feels inconsistent')) return 'Sleep is the priority this week.'
  if (c.includes('Nutrition') || c.includes('My child snacks too often')) return 'Nutrition needs your attention.'
  if (c.includes('Physical activity') || c.includes('My child is not active enough')) return 'Movement matters most right now.'
  return 'Consistency drives everything.'
})

const weeklyNarrative = computed(() => {
  const name = childName.value
  const c = state.concerns || []
  if (c.includes('Sleep consistency') || c.includes('Bedtime feels inconsistent')) {
    return `${name} may struggle with energy and mood if sleep stays inconsistent. Prioritising bedtime structure can improve appetite, attention, and after-school behaviour.`
  }
  if (c.includes('Nutrition') || c.includes('My child snacks too often')) {
    return `${name} needs consistent fuel through the day. Better snack quality can stabilise energy, reduce irritability, and support healthy growth habits.`
  }
  return `${name}'s plan is focused on consistency. One repeated healthy action each day is the strongest predictor of long-term habit success.`
})

const riskNarrative = computed(() => {
  const c = state.concerns || []
  if (c.includes('Routine battles') || c.includes('Our family routine feels hard to manage')) {
    return 'Daily friction increases and healthy habits become harder to sustain.'
  }
  if (c.includes('Physical activity') || c.includes('My child is not active enough')) {
    return 'Lower movement can affect mood regulation and sleep quality.'
  }
  return 'Inconsistent habits reduce progress and make routines harder to maintain.'
})

const winNarrative = computed(() => {
  const c = state.concerns || []
  if (c.includes('Nutrition') || c.includes('My child snacks too often')) {
    return 'Higher energy and fewer snack-related conflicts after school.'
  }
  if (c.includes('Sleep consistency') || c.includes('Bedtime feels inconsistent')) {
    return 'Calmer evenings and more predictable morning routines.'
  }
  return 'Better consistency with less parent-child conflict across the day.'
})

function buildTimeSlots(focusKey, weekNumber, dayName, childNameVal, stateRef, baseId) {
  const name = childNameVal || 'your child'
  const age = getApproxAge(stateRef.ageRange)
  const isYoung = age <= 7
  const isWeekend = dayName === 'Saturday' || dayName === 'Sunday'
  const concerns = stateRef.concerns || []
  const hasScreenIssue = concerns.includes('Too much screen time') || concerns.includes('Screen time battles')
  const hasSleepIssue = concerns.includes('Sleep consistency') || concerns.includes('Bedtime feels inconsistent')
  const hasNutritionIssue = concerns.includes('Nutrition') || concerns.includes('My child snacks too often')
  const hasMovementIssue = concerns.includes('Physical activity') || concerns.includes('My child is not active enough')
  const hasRoutineIssue = concerns.includes('Routine battles') || concerns.includes('Our family routine feels hard to manage')

  const s = (time, category, categoryLabel, text, tip, id) => ({
    id: `${baseId}-${id}`,
    time,
    category,
    categoryLabel,
    text,
    tip: tip || null,
    done: Boolean((stateRef.roadmapProgress || {})[`${baseId}-${id}`]),
  })

  const templates = {
    nutrition: {
      1: {
        weekday: [
          s('7:00 am', 'nutrition', 'Nutrition', 'Offer one nutritious breakfast option - whole grain, fruit, or eggs', isYoung ? 'Make it fun: let them pick the fruit topping' : 'Keep prep under 5 minutes', 'breakfast'),
          s('8:00 am', 'routine', 'Routine', 'Pack one healthy item in the school lunchbox', 'A familiar item reduces lunchbox refusal', 'lunchpack'),
          s('3:30 pm', 'nutrition', 'Nutrition', 'Have a healthy snack ready before screens go on', hasNutritionIssue ? 'Snack before screens reduces binge eating later' : null, 'aftersnack'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Serve dinner together at the table where possible', 'Family meals reduce screen time naturally', 'dinner'),
          s(hasSleepIssue ? '7:30 pm' : '8:00 pm', 'sleep', 'Wind-down', 'Begin bedtime cue - dim lights and reduce noise', null, 'winddown'),
        ],
        weekend: [
          s('8:30 am', 'family', 'Family', 'Cook or prepare a simple breakfast together', isYoung ? 'Let them pour or mix - involvement = engagement' : null, 'breakfast'),
          s('10:30 am', 'movement', 'Movement', 'Do a 20-minute outdoor or active play session', null, 'movement'),
          s('12:30 pm', 'nutrition', 'Nutrition', 'Prepare a home-made lunch with one new ingredient', 'Trying one new food weekly builds variety', 'lunch'),
          s('3:00 pm', 'nutrition', 'Nutrition', 'Choose a healthy afternoon snack together', hasNutritionIssue ? 'Involve them in choice - reduces resistance' : null, 'snack'),
          s('6:30 pm', 'routine', 'Routine', 'Plan one healthy food goal for the coming week', null, 'plan'),
        ],
      },
      2: {
        weekday: [
          s('7:00 am', 'nutrition', 'Nutrition', 'Use the same breakfast each weekday - build the routine', 'Repetition creates automatic habit', 'breakfast'),
          s('8:00 am', 'routine', 'Routine', 'Use a consistent lunchbox packing cue - same time, same spot', null, 'lunchpack'),
          s('3:30 pm', 'nutrition', 'Nutrition', 'Offer water before the after-school snack', hasNutritionIssue ? 'Thirst is often mistaken for hunger - water first reduces overeating' : null, 'water'),
          s('5:00 pm', 'movement', 'Movement', 'Encourage 20 minutes of active play or bike ride', hasMovementIssue ? 'Schedule movement before homework - energy improves focus' : null, 'movement'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Include one vegetable in dinner tonight', null, 'dinner'),
          s(hasSleepIssue ? '7:30 pm' : '8:00 pm', 'sleep', 'Wind-down', 'Begin the same bedtime routine - books, bath, or quiet time', null, 'winddown'),
        ],
        weekend: [
          s('9:00 am', 'family', 'Family', 'Make a smoothie or fruit bowl together', null, 'breakfast'),
          s('11:00 am', 'movement', 'Movement', 'Family walk, scooter, or park visit', null, 'movement'),
          s('1:00 pm', 'nutrition', 'Nutrition', 'Try one new healthy lunch option as a family', null, 'lunch'),
          s('4:00 pm', 'routine', 'Routine', 'Review what food habits worked this week', null, 'review'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Maintain the same bedtime even on weekends', hasSleepIssue ? 'Weekend sleep drift makes Monday mornings harder' : null, 'bedtime'),
        ],
      },
      3: {
        weekday: [
          s('7:00 am', 'nutrition', 'Nutrition', `Let ${name} choose between two breakfast options`, 'Choice builds ownership', 'breakfast'),
          s('3:30 pm', 'nutrition', 'Nutrition', 'Put fruit or veggies out before the snack - first food seen = first food eaten', null, 'snack'),
          s('5:00 pm', 'movement', 'Movement', 'Active break before homework or screens', null, 'movement'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Involve them in one small dinner task - washing veg, setting table', null, 'dinner'),
          s('8:00 pm', 'sleep', 'Wind-down', 'Follow the same wind-down order without prompting', null, 'winddown'),
        ],
        weekend: [
          s('9:30 am', 'family', 'Family', 'Cook one full breakfast together - pancakes, eggs, or toast', isYoung ? 'Assign simple safe tasks: stirring, plating' : null, 'breakfast'),
          s('12:00 pm', 'nutrition', 'Nutrition', 'Try one meal with reduced processed options', null, 'lunch'),
          s('3:00 pm', 'movement', 'Movement', 'Active outdoor time as a family for at least 30 minutes', null, 'movement'),
          s('6:30 pm', 'routine', 'Routine', 'Note which food habit felt easiest this week', null, 'reflect'),
        ],
      },
      4: {
        weekday: [
          s('7:00 am', 'nutrition', 'Nutrition', 'Maintain the breakfast routine with no prompting needed', null, 'breakfast'),
          s('3:30 pm', 'nutrition', 'Nutrition', 'Healthy snack is the default - no alternative offered', null, 'snack'),
          s('5:30 pm', 'movement', 'Movement', 'Active time before dinner - make it non-negotiable', null, 'movement'),
          s('6:30 pm', 'nutrition', 'Nutrition', 'Serve one balanced dinner with protein, veg, and starch', null, 'dinner'),
          s('8:00 pm', 'sleep', 'Wind-down', 'Wind down at the same time without reminders', null, 'winddown'),
        ],
        weekend: [
          s('9:00 am', 'family', 'Family', 'Celebrate the strongest food habit from the 4 weeks', null, 'celebrate'),
          s('11:00 am', 'movement', 'Movement', 'Family physical activity - their choice', null, 'movement'),
          s('2:00 pm', 'nutrition', 'Nutrition', 'Plan next month\'s one food habit goal', null, 'plan'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Set bedtime for the school week ahead', null, 'bedtime'),
        ],
      },
    },
    sleep: {
      1: {
        weekday: [
          s('3:30 pm', 'movement', 'Movement', 'Encourage active play after school - physical tiredness aids sleep', null, 'movement'),
          s('5:30 pm', 'nutrition', 'Nutrition', 'Serve dinner at a consistent time each night', hasSleepIssue ? 'Late meals delay sleep onset' : null, 'dinner'),
          s('6:30 pm', 'routine', 'Routine', 'Reduce screen brightness and noise 90 minutes before bed', hasScreenIssue ? 'Blue light suppresses melatonin for up to 2 hours' : null, 'screens'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Begin wind-down: bath, pyjamas, or quiet reading', null, 'bath'),
          s('7:30 pm', 'sleep', 'Wind-down', `Say goodnight using one calm, consistent phrase with ${name}`, isYoung ? 'Predictable phrases signal safety to young children' : null, 'goodnight'),
        ],
        weekend: [
          s('8:00 am', 'sleep', 'Wind-down', 'Wake at the same time as school days - within 1 hour', hasSleepIssue ? 'Weekend sleep drift disrupts Monday school mornings significantly' : null, 'wake'),
          s('10:00 am', 'movement', 'Movement', 'Morning physical activity to build sleep pressure for tonight', null, 'movement'),
          s('7:00 pm', 'routine', 'Routine', 'Begin bedtime routine at the same time as weekdays', null, 'routine'),
          s('7:30 pm', 'sleep', 'Wind-down', 'Follow the same wind-down steps as school nights', null, 'winddown'),
        ],
      },
      2: {
        weekday: [
          s('5:30 pm', 'nutrition', 'Nutrition', 'Serve a light, early dinner - avoid heavy meals close to bed', null, 'dinner'),
          s('6:00 pm', 'movement', 'Movement', 'Last active play session of the day ends now', null, 'movement'),
          s('6:30 pm', 'routine', 'Routine', 'Use one visual bedtime countdown - clock, timer, or chart', isYoung ? 'Visual cues work better than verbal reminders for young children' : null, 'cue'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Screens off - swap to books, drawing, or calm music', hasScreenIssue ? 'No screens at least 60 min before target bedtime' : null, 'screens'),
          s('7:30 pm', 'sleep', 'Wind-down', 'Lights dim, same story or quiet routine - same order each night', null, 'story'),
          s('8:00 pm', 'sleep', 'Wind-down', `${name} in bed - aim for lights out by 8:00-8:30 pm`, null, 'sleep'),
        ],
        weekend: [
          s('8:30 am', 'sleep', 'Wind-down', 'Morning routine at the same time - no sleeping in past 1 hour', null, 'wake'),
          s('10:30 am', 'family', 'Family', 'Calm, low-stimulation family activity in the morning', null, 'family'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Begin weekend bedtime routine - same steps as weekdays', null, 'bedtime'),
        ],
      },
      3: {
        weekday: [
          s('5:00 pm', 'movement', 'Movement', 'Active outdoor play - use up energy before wind-down', null, 'movement'),
          s('6:30 pm', 'routine', 'Routine', 'Start bedtime cue without prompting - let it become expected', null, 'cue'),
          s('7:00 pm', 'sleep', 'Wind-down', `Let ${name} choose one part of the wind-down routine`, 'Choice reduces resistance dramatically', 'choice'),
          s('7:30 pm', 'sleep', 'Wind-down', 'Lights low, quiet voices, same sequence', null, 'quiet'),
          s('8:00 pm', 'sleep', 'Wind-down', 'Lights out - no re-entries unless genuinely needed', null, 'sleep'),
        ],
        weekend: [
          s('8:00 am', 'routine', 'Routine', 'Keep wake time consistent', null, 'wake'),
          s('2:00 pm', 'family', 'Family', 'Lower-stimulation afternoon activity - park, art, or reading', null, 'afternoon'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Bedtime routine starts - same time, same steps', null, 'bedtime'),
        ],
      },
      4: {
        weekday: [
          s('5:00 pm', 'movement', 'Movement', 'Physical activity in the afternoon - make it a daily anchor', null, 'movement'),
          s('6:30 pm', 'routine', 'Routine', `${name} initiates part of the bedtime routine independently`, null, 'independent'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Wind-down sequence runs smoothly with minimal prompting', null, 'winddown'),
          s('8:00 pm', 'sleep', 'Wind-down', 'Lights out at the consistent time', null, 'sleep'),
        ],
        weekend: [
          s('8:00 am', 'routine', 'Routine', 'Wake time within 1 hour of school schedule', null, 'wake'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Begin bedtime routine - celebrate the consistency built', null, 'bedtime'),
        ],
      },
    },
    movement: {
      1: {
        weekday: [
          s('7:30 am', 'movement', 'Movement', 'Walk or bike to school if possible - even part of the way', null, 'morning'),
          s('3:30 pm', 'movement', 'Movement', 'Active play for 15 minutes before snack or screens', hasMovementIssue ? 'Movement before screens is easier to enforce than after' : null, 'afterschool'),
          s('5:00 pm', 'routine', 'Routine', 'Set a simple daily movement goal - e.g. 3 laps of the yard', isYoung ? 'Make it a game - chase, tag, or obstacle course' : null, 'goal'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Serve dinner - protein helps muscle recovery from activity', null, 'dinner'),
          s('8:00 pm', 'sleep', 'Wind-down', 'Begin calm bedtime routine - active kids need clear transitions', null, 'winddown'),
        ],
        weekend: [
          s('9:30 am', 'movement', 'Movement', 'Family physical activity - park, beach, or backyard play', null, 'morning'),
          s('12:00 pm', 'nutrition', 'Nutrition', 'Fuel up with a balanced lunch after the morning activity', null, 'lunch'),
          s('3:00 pm', 'movement', 'Movement', 'Second active session - bike, scooter, or sports', null, 'afternoon'),
          s('6:00 pm', 'family', 'Family', 'Celebrate the day\'s active moments together', null, 'celebrate'),
        ],
      },
      2: {
        weekday: [
          s('3:30 pm', 'movement', 'Movement', 'After-school active break - 20 minutes before any screen time', hasScreenIssue ? 'Movement before screens builds the expectation: active first, then relax' : null, 'afterschool'),
          s('5:00 pm', 'movement', 'Movement', 'Attach one movement habit to homework time - stretch breaks every 20 min', null, 'homework'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Dinner together - discuss one active thing done today', null, 'dinner'),
          s('7:30 pm', 'routine', 'Routine', 'Track today\'s movement on a simple chart or sticker', isYoung ? 'Sticker charts work brilliantly for ages 5-8' : null, 'track'),
          s('8:00 pm', 'sleep', 'Wind-down', 'Calm wind-down - avoid vigorous activity within 90 min of bed', null, 'winddown'),
        ],
        weekend: [
          s('9:00 am', 'movement', 'Movement', 'Family walk or cycle - aim for 30+ minutes', null, 'morning'),
          s('11:30 am', 'nutrition', 'Nutrition', 'Healthy brunch after activity', null, 'brunch'),
          s('3:00 pm', 'movement', 'Movement', `${childName.value}'s choice of physical activity`, null, 'choice'),
          s('6:00 pm', 'family', 'Family', 'Reflect on the week\'s movement wins', null, 'reflect'),
        ],
      },
      3: {
        weekday: [
          s('7:30 am', 'movement', 'Movement', 'Morning stretch or short walk - sets an active tone for the day', null, 'morning'),
          s('3:30 pm', 'movement', 'Movement', `${name} chooses today's after-school active activity`, 'Choice increases follow-through significantly', 'choice'),
          s('5:30 pm', 'routine', 'Routine', 'Reduce sitting time - stand during homework or TV', null, 'sit'),
          s('8:00 pm', 'sleep', 'Wind-down', 'Calm wind-down after an active day', null, 'winddown'),
        ],
        weekend: [
          s('9:00 am', 'movement', 'Movement', 'Long active session - sport, hiking, or playground for 45+ min', null, 'morning'),
          s('1:00 pm', 'nutrition', 'Nutrition', 'Post-activity nourishing meal', null, 'lunch'),
          s('4:00 pm', 'family', 'Family', 'Shared activity - board game, dance, or casual sport', null, 'family'),
        ],
      },
      4: {
        weekday: [
          s('3:30 pm', 'movement', 'Movement', `${name} starts the after-school active session independently`, null, 'afterschool'),
          s('5:00 pm', 'routine', 'Routine', 'Movement habit runs without reminders', null, 'independent'),
          s('8:00 pm', 'sleep', 'Wind-down', 'Wind down smoothly after active day', null, 'winddown'),
        ],
        weekend: [
          s('9:00 am', 'movement', 'Movement', 'Celebrate 4 weeks of building movement habits - family activity of choice', null, 'celebrate'),
          s('12:00 pm', 'nutrition', 'Nutrition', 'Fuel the activity with a balanced meal', null, 'lunch'),
          s('3:00 pm', 'family', 'Family', 'Plan one movement goal for next month', null, 'plan'),
        ],
      },
    },
    routine: {
      1: {
        weekday: [
          s('7:00 am', 'routine', 'Routine', 'Use one consistent morning cue - alarm, song, or phrase', hasRoutineIssue ? 'One predictable cue reduces morning conflict significantly' : null, 'morning'),
          s('7:30 am', 'nutrition', 'Nutrition', 'Breakfast at the same time - consistency is the goal', null, 'breakfast'),
          s('3:30 pm', 'routine', 'Routine', 'After-school routine: snack -> play -> homework in order', null, 'afterschool'),
          s('5:30 pm', 'movement', 'Movement', 'Active time before dinner - built into the routine', null, 'movement'),
          s('7:00 pm', 'routine', 'Routine', 'Begin bedtime sequence at the same time', hasSleepIssue ? 'Consistent start time matters more than sleep time' : null, 'bedtime'),
        ],
        weekend: [
          s('8:30 am', 'routine', 'Routine', 'Morning routine similar to weekdays - anchor the habit', null, 'morning'),
          s('10:00 am', 'family', 'Family', 'One shared family activity that uses a routine cue', null, 'family'),
          s('6:30 pm', 'routine', 'Routine', 'Evening routine starts at the same time as school nights', null, 'evening'),
        ],
      },
      2: {
        weekday: [
          s('7:00 am', 'routine', 'Routine', 'Morning routine runs on the same order - no deviations', null, 'morning'),
          s('3:30 pm', 'routine', 'Routine', 'Use one visual or verbal cue to start the after-school routine', hasRoutineIssue ? 'Cues eliminate negotiation - they just signal what\'s next' : null, 'cue'),
          s('5:00 pm', 'movement', 'Movement', 'Active break as part of the routine - not optional', null, 'movement'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Dinner at the same time - sets the rhythm for the evening', null, 'dinner'),
          s('7:30 pm', 'routine', 'Routine', 'Bedtime routine starts with a predictable cue', null, 'bedtime'),
        ],
        weekend: [
          s('9:00 am', 'routine', 'Routine', 'Anchor the weekend to at least one weekday routine step', null, 'anchor'),
          s('11:00 am', 'movement', 'Movement', 'Active family time - use the movement habit', null, 'movement'),
          s('7:00 pm', 'routine', 'Routine', 'Weekend bedtime routine - same steps, maybe slightly later', null, 'bedtime'),
        ],
      },
      3: {
        weekday: [
          s('7:00 am', 'routine', 'Routine', `${name} follows the morning routine with minimal prompts`, 'Reduce reminders by one each week', 'morning'),
          s('3:30 pm', 'routine', 'Routine', `${name} helps choose how the after-school routine runs`, 'Offering choices increases buy-in', 'choice'),
          s('5:00 pm', 'movement', 'Movement', 'Movement is built into the routine - no separate reminder needed', null, 'movement'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Bedtime routine runs smoother - less friction', null, 'winddown'),
        ],
        weekend: [
          s('9:00 am', 'routine', 'Routine', 'Weekend morning routine - keep the anchor habit', null, 'morning'),
          s('3:00 pm', 'family', 'Family', 'Family reflection: what routine step felt easiest this week?', null, 'reflect'),
          s('7:00 pm', 'routine', 'Routine', 'Evening routine - aim for same time as school nights', null, 'evening'),
        ],
      },
      4: {
        weekday: [
          s('7:00 am', 'routine', 'Routine', 'Morning routine runs independently - minimal parent involvement', null, 'morning'),
          s('3:30 pm', 'routine', 'Routine', `${name} begins after-school routine without prompting`, null, 'afterschool'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Family dinner - celebrate the routine habit formed', null, 'dinner'),
          s('7:30 pm', 'sleep', 'Wind-down', 'Bedtime routine is automatic - everyone knows what\'s next', null, 'winddown'),
        ],
        weekend: [
          s('9:00 am', 'routine', 'Routine', 'Celebrate 4 weeks of routine building', null, 'celebrate'),
          s('2:00 pm', 'family', 'Family', 'Choose one routine to keep for next month', null, 'plan'),
        ],
      },
    },
    balanced: {
      1: {
        weekday: [
          s('7:00 am', 'nutrition', 'Nutrition', 'Start the day with one nutritious breakfast', null, 'breakfast'),
          s('3:30 pm', 'movement', 'Movement', 'After-school active play for 15 minutes', null, 'movement'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Family dinner - one vegetable included', null, 'dinner'),
          s('7:30 pm', 'sleep', 'Wind-down', 'Begin consistent bedtime routine', null, 'winddown'),
        ],
        weekend: [
          s('9:00 am', 'family', 'Family', 'Active family morning', null, 'morning'),
          s('12:00 pm', 'nutrition', 'Nutrition', 'Balanced home-cooked lunch together', null, 'lunch'),
          s('3:00 pm', 'movement', 'Movement', 'Afternoon activity of their choice', null, 'afternoon'),
          s('7:30 pm', 'sleep', 'Wind-down', 'Consistent bedtime routine', null, 'winddown'),
        ],
      },
      2: {
        weekday: [
          s('7:00 am', 'nutrition', 'Nutrition', 'Same breakfast routine - build the habit', null, 'breakfast'),
          s('3:30 pm', 'movement', 'Movement', 'After-school movement before screens', null, 'movement'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Dinner together - healthy and consistent', null, 'dinner'),
          s('7:30 pm', 'sleep', 'Wind-down', 'Wind-down - same sequence each night', null, 'winddown'),
        ],
        weekend: [
          s('9:30 am', 'family', 'Family', 'Active family activity outside', null, 'morning'),
          s('1:00 pm', 'nutrition', 'Nutrition', 'Healthy weekend lunch', null, 'lunch'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Consistent weekend bedtime', null, 'bedtime'),
        ],
      },
      3: {
        weekday: [
          s('7:00 am', 'nutrition', 'Nutrition', `${name} helps with one breakfast task`, null, 'breakfast'),
          s('3:30 pm', 'movement', 'Movement', `${name} chooses the after-school activity`, null, 'movement'),
          s('7:00 pm', 'sleep', 'Wind-down', 'Wind-down with reduced prompting', null, 'winddown'),
        ],
        weekend: [
          s('10:00 am', 'movement', 'Movement', '30-minute family activity', null, 'morning'),
          s('6:00 pm', 'nutrition', 'Nutrition', 'Balanced family dinner', null, 'dinner'),
          s('7:30 pm', 'sleep', 'Wind-down', 'Bedtime routine - smooth and calm', null, 'bedtime'),
        ],
      },
      4: {
        weekday: [
          s('7:00 am', 'nutrition', 'Nutrition', 'Breakfast habit is automatic', null, 'breakfast'),
          s('3:30 pm', 'movement', 'Movement', 'Movement habit runs without reminders', null, 'movement'),
          s('7:30 pm', 'sleep', 'Wind-down', 'Bedtime routine is self-directed', null, 'winddown'),
        ],
        weekend: [
          s('9:30 am', 'family', 'Family', 'Celebrate the 4-week journey', null, 'celebrate'),
          s('2:00 pm', 'routine', 'Routine', 'Set one habit goal for next month', null, 'plan'),
        ],
      },
    },
  }

  const focusTemplates = templates[focusKey] || templates.balanced
  const weekTemplates = focusTemplates[weekNumber] || focusTemplates[1]
  const slotSet = isWeekend ? weekTemplates.weekend : weekTemplates.weekday
  return slotSet || []
}

function getCategoryLabel(category) {
  const labels = {
    nutrition: 'Nutrition',
    movement: 'Movement',
    sleep: 'Wind-down',
    routine: 'Routine',
    family: 'Family',
  }
  return labels[category] || 'Routine'
}

function applyPlannerOverrides(slot) {
  const overrides = state.plannerOverrides || {}
  const edited = overrides[slot.id]

  if (!edited) return slot

  const category = edited.category || slot.category
  return {
    ...slot,
    time: edited.time || slot.time,
    text: edited.text || slot.text,
    tip: edited.tip ?? slot.tip,
    category,
    categoryLabel: getCategoryLabel(category),
  }
}

const roadmapFocus = computed(() => {
  const focusMap = {
    sleep: { w1: 'Create a calmer bedtime rhythm', w2: 'Reduce evening friction', w3: 'Strengthen wind-down habits', w4: 'Make sleep routines self-sustaining' },
    nutrition: { w1: 'Improve snack quality', w2: 'Build simple meal structure', w3: 'Increase healthy choices', w4: 'Make food routines consistent' },
    movement: { w1: 'Add short movement moments', w2: 'Build active after-school habits', w3: 'Reduce long sitting periods', w4: 'Make movement part of the routine' },
    routine: { w1: 'Create one predictable daily cue', w2: 'Reduce routine battles', w3: 'Build consistency around transitions', w4: 'Make family routines easier to repeat' },
    balanced: { w1: 'Start with one simple healthy habit', w2: 'Build consistency across the week', w3: 'Connect habits into a routine', w4: 'Maintain progress with less effort' },
  }
  return focusMap[primaryConcern.value] || focusMap.balanced
})

const roadmapProgressMap = computed(() => state.roadmapProgress || {})

const roadmapActionTemplates = computed(() => {
  const name = childName.value
  return [
    {
      id: 1,
      week: 1,
      title: roadmapFocus.value.w1,
      focus: roadmapFocus.value.w1,
      icon: '🌱',
      theme: 'week-theme-green',
      summary: 'Start small - the goal is to make one action feel easy to repeat.',
      detail: 'Week 1 focuses on starting gently. The goal is not perfection - it is to make one healthy routine feel possible without adding pressure.',
      mainAction: `Choose one daily habit to try with ${name}`,
      supportTip: 'Keep the habit tiny and easy so it feels achievable on busy days too.',
      actions: [`Choose one daily habit to try with ${name}`, 'Complete the habit at least three times this week', 'Celebrate one small win together'],
      parentTip: 'Keep the first week very small. A habit that feels easy is far more likely to continue than one that feels like a chore.',
    },
    {
      id: 2,
      week: 2,
      title: roadmapFocus.value.w2,
      focus: roadmapFocus.value.w2,
      icon: '🧩',
      theme: 'week-theme-amber',
      summary: 'Turn the first habit into something predictable and expected.',
      detail: 'Week 2 builds consistency. Families begin connecting the habit to a regular part of the day, making it feel automatic rather than intentional.',
      mainAction: 'Attach the habit to an existing family routine',
      supportTip: 'Use the same cue each day so your child knows what happens next.',
      actions: ['Attach the habit to an existing family routine', 'Use one visual or verbal cue to remind everyone', 'Track progress without applying pressure'],
      parentTip: 'Try linking the habit to something that already happens - after school, dinner, or bedtime. This is called habit stacking.',
    },
    {
      id: 3,
      week: 3,
      title: roadmapFocus.value.w3,
      focus: roadmapFocus.value.w3,
      icon: '✨',
      theme: 'week-theme-blue',
      summary: 'Strengthen the routine and reduce daily resistance.',
      detail: 'Week 3 makes the habit smoother. The aim is to reduce reminders, arguments, or pushback - and let your child take some ownership.',
      mainAction: `Let ${name} help choose how the habit is completed`,
      supportTip: 'Offer small choices so the routine feels shared instead of enforced.',
      actions: [`Let ${name} help choose how the habit is completed`, 'Repeat the habit on at least four days this week', 'Notice what makes the habit easier or harder'],
      parentTip: 'Children are more engaged when they feel involved. Offer simple choices rather than instructions - it shifts the dynamic significantly.',
    },
    {
      id: 4,
      week: 4,
      title: roadmapFocus.value.w4,
      focus: roadmapFocus.value.w4,
      icon: '🏁',
      theme: 'week-theme-violet',
      summary: 'Reflect, adjust, and make the habit sustainable beyond this plan.',
      detail: 'Week 4 helps families reflect, adapt, and decide what to continue. The goal is to identify one or two habits worth keeping long-term.',
      mainAction: 'Review what improved over the last four weeks',
      supportTip: 'Keep the parts that worked best and simplify anything that felt too hard.',
      actions: ['Review what improved over the last four weeks', 'Choose one habit to continue next month', `Set one gentle goal for ${name} for the next stage`],
      parentTip: 'The best habit is the one your family can keep doing. Keep what worked, simplify what felt too hard, and build from there.',
    },
  ]
})

const fourWeekRoadmap = computed(() =>
  roadmapActionTemplates.value.map((week) => {
    const actions = week.actions.map((text, index) => {
      const id = `week-${week.week}-action-${index + 1}`
      return { id, text, done: Boolean(roadmapProgressMap.value[id]) }
    })

    const dailyPlan = orderedDays.map((day) => {
      const baseId = `week-${week.week}-${day.toLowerCase()}`
      const timeSlots = buildTimeSlots(primaryConcern.value, week.week, day, childName.value, state, baseId)
      const slotsWithDoneState = timeSlots.map(slot => {
        const editedSlot = applyPlannerOverrides(slot)
        return { ...editedSlot, done: Boolean(roadmapProgressMap.value[slot.id]) }
      })

      const completed = slotsWithDoneState.filter(slot => slot.done).length
      const progress = slotsWithDoneState.length ? Math.round((completed / slotsWithDoneState.length) * 100) : 0

      return { day, timeSlots: slotsWithDoneState, completed, progress }
    })

    const weeklyCompleted = actions.filter(action => action.done).length
    const dailyCompleted = dailyPlan.reduce((sum, day) => sum + day.completed, 0)
    const dailyTotal = dailyPlan.reduce((sum, day) => sum + day.timeSlots.length, 0)
    const totalItems = actions.length + dailyTotal
    const completedItems = weeklyCompleted + dailyCompleted
    const progress = totalItems ? Math.round((completedItems / totalItems) * 100) : 0

    let status = 'Not started'
    let statusKey = 'not-started'
    if (progress > 0 && progress < 100) {
      status = 'In progress'
      statusKey = 'in-progress'
    }
    if (progress === 100) {
      status = 'Completed'
      statusKey = 'completed'
    }

    return {
      ...week,
      actions,
      dailyPlan,
      dailyCompleted,
      dailyTotal,
      weeklyCompleted,
      totalItems,
      completed: completedItems,
      progress,
      status,
      statusKey,
      feedbackTitle: progress === 100 ? 'Week complete - excellent work!' : progress > 0 ? 'Building momentum' : 'Ready to begin',
      feedback: progress === 100
        ? `${childName.value} has completed all actions for this week. This is a strong sign the routine is becoming easier to repeat.`
        : progress > 0
          ? 'Some progress is already happening. Continue with the easiest action first and build from there - every check matters.'
          : 'This week is ready to begin. Choose the single easiest action and try it just once today to get started.',
      statusSummary: progress === 100
        ? `All weekly roadmap items for Week ${week.week} are complete.`
        : progress > 0
          ? `${completedItems} of ${totalItems} weekly items are complete so far.`
          : `No items completed yet for Week ${week.week}.`,
      feedbackCue: progress === 100 ? 'Keep this habit going' : progress > 0 ? 'Stay consistent' : 'Start with one easy win',
      feedbackNextStep: progress === 100
        ? 'Repeat the strongest habit next week to help it become part of the family routine.'
        : progress > 0
          ? 'Keep supporting the same habit cue this week so progress feels predictable and manageable.'
          : 'Complete the main weekly action once today, then build from that small success.',
    }
  })
)

const selectedRoadmapWeek = computed(() =>
  fourWeekRoadmap.value.find(week => week.id === activeRoadmapWeek.value) || fourWeekRoadmap.value[0]
)

const currentFirstRoadmapDailyPlan = computed(() => {
  const plan = selectedRoadmapWeek.value?.dailyPlan || []
  const todayIndex = plan.findIndex(day => day.day === todayName.value)
  if (todayIndex === -1) return plan
  return [plan[todayIndex], ...plan.slice(0, todayIndex), ...plan.slice(todayIndex + 1)]
})

const totalRoadmapActions = computed(() => fourWeekRoadmap.value.reduce((sum, week) => sum + week.totalItems, 0))
const completedRoadmapActions = computed(() => fourWeekRoadmap.value.reduce((sum, week) => sum + week.completed, 0))
const roadmapCompletion = computed(() =>
  totalRoadmapActions.value ? Math.round((completedRoadmapActions.value / totalRoadmapActions.value) * 100) : 0
)
const roadmapRingStyle = computed(() => {
  const pct = roadmapCompletion.value
  const color = pct === 100 ? '#16a34a' : pct > 0 ? '#d97706' : '#e2e8f0'
  return { background: `conic-gradient(${color} ${pct}%, rgba(0,0,0,0.07) ${pct}%)` }
})

const currentWeek = computed(() =>
  fourWeekRoadmap.value.find(week => week.statusKey !== 'completed')?.week || 4
)

const weeklyProgress = computed(() =>
  selectedRoadmapWeek.value.dailyPlan.map((day) => ({
    label: day.day.slice(0, 3),
    fullLabel: day.day,
    value: day.progress,
    completed: day.completed,
    total: day.timeSlots.length,
    tasks: day.timeSlots.map(slot => ({
      id: slot.id,
      text: slot.text,
      done: slot.done,
    })),
  }))
)

const selectedDay = computed(() =>
  weeklyProgress.value.find(day => day.label === selectedDayLabel.value) ||
  weeklyProgress.value[0] ||
  { label: 'Mon', fullLabel: 'Monday', value: 0, completed: 0, total: 0, tasks: [] }
)

const weeklyAverage = computed(() => {
  const total = weeklyProgress.value.reduce((sum, day) => sum + day.value, 0)
  return weeklyProgress.value.length ? Math.round(total / weeklyProgress.value.length) : 0
})

const selectedWeekActionCompletion = computed(() =>
  selectedRoadmapWeek.value.actions.length
    ? Math.round((selectedRoadmapWeek.value.weeklyCompleted / selectedRoadmapWeek.value.actions.length) * 100)
    : 0
)

const selectedWeekDailyCompletion = computed(() =>
  selectedRoadmapWeek.value.dailyTotal
    ? Math.round((selectedRoadmapWeek.value.dailyCompleted / selectedRoadmapWeek.value.dailyTotal) * 100)
    : 0
)

const selectedWeekOpenItems = computed(() =>
  Math.max(0, selectedRoadmapWeek.value.totalItems - selectedRoadmapWeek.value.completed)
)

const startedWeeksCount = computed(() => fourWeekRoadmap.value.filter(week => week.progress > 0).length)
const completedWeeksCount = computed(() => fourWeekRoadmap.value.filter(week => week.statusKey === 'completed').length)

const strongestDay = computed(() =>
  weeklyProgress.value.reduce((best, day) => (day.value > best.value ? day : best), weeklyProgress.value[0] || {
    label: 'Mon',
    fullLabel: 'Monday',
    value: 0,
  })
)

const weakestDay = computed(() =>
  weeklyProgress.value.reduce((worst, day) => (day.value < worst.value ? day : worst), weeklyProgress.value[0] || {
    label: 'Mon',
    fullLabel: 'Monday',
    value: 0,
  })
)

const weeklyConsistencyGap = computed(() => Math.max(0, strongestDay.value.value - weakestDay.value.value))

const roadmapMomentumLabel = computed(() => {
  if (roadmapCompletion.value >= 80) return 'Strong'
  if (roadmapCompletion.value >= 40) return 'Growing'
  return 'Starting'
})

const selectedWeekCategoryMix = computed(() => {
  const totals = selectedRoadmapWeek.value.dailyPlan
    .flatMap(day => day.timeSlots)
    .reduce((acc, slot) => {
      acc[slot.category] = (acc[slot.category] || 0) + 1
      return acc
    }, {})

  const total = Object.values(totals).reduce((sum, value) => sum + value, 0) || 1

  return scheduleCategories.map(cat => ({
    key: cat.key,
    label: cat.label,
    count: totals[cat.key] || 0,
    percent: Math.round(((totals[cat.key] || 0) / total) * 100),
  }))
})

watch(currentWeek, (nextWeek, previousWeek) => {
  if (activeRoadmapWeek.value === previousWeek || !fourWeekRoadmap.value.some(week => week.id === activeRoadmapWeek.value)) {
    activeRoadmapWeek.value = nextWeek
  }
}, { immediate: true })

function saveAndPersist(updatedState) {
  savePlan(updatedState)
  persistDashboardUpdate(updatedState).catch(error => {
    console.error('Failed to sync roadmap update:', error)
  })
}

function toggleRoadmapAction(actionId) {
  const updated = { ...(state.roadmapProgress || {}), [actionId]: !state.roadmapProgress?.[actionId] }
  saveAndPersist({ ...state, roadmapProgress: updated })
}

function toggleRoadmapDailyAction(actionId) {
  const updated = { ...(state.roadmapProgress || {}), [actionId]: !state.roadmapProgress?.[actionId] }
  saveAndPersist({ ...state, roadmapProgress: updated })
}

async function persistDashboardUpdate(updatedState) {
  const username = updatedState.username || state.username
  if (!username) throw new Error('Missing username')
  if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')

  const response = await fetch(`${API_BASE_URL}/parent-profiles/${encodeURIComponent(username)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      dailyPlan: updatedState.dailyPlan ?? state.dailyPlan,
      progressItems: updatedState.progressItems ?? state.progressItems,
      roadmapProgress: updatedState.roadmapProgress ?? state.roadmapProgress ?? {},
      todaySchedule: updatedState.todaySchedule ?? state.todaySchedule ?? {},
      plannerOverrides: updatedState.plannerOverrides ?? state.plannerOverrides ?? {},
      streakDays: updatedState.streakDays ?? state.streakDays ?? 0,
      nextAction: updatedState.nextAction ?? state.nextAction,
      mission: updatedState.mission ?? state.mission,
    }),
  })

  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.error || `Dashboard update failed: ${response.status}`)
  return data
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400;1,9..144,500&display=swap');
@import url('https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&display=swap');

:global(:root) {
  --c-black:#0a0b0a; --c-900:#111312; --c-800:#1c1f1d; --c-700:#2d3230;
  --c-500:#52605a; --c-400:#7a8880; --c-300:#a8b5ae; --c-100:#e8ece9;
  --c-50:#f4f5f2; --c-white:#ffffff;
  --c-green:#16a34a; --c-green-mid:#22c55e; --c-green-soft:#f0fdf4; --c-green-pale:#dcfce7;
  --c-amber-soft:#fffbeb;
  --border:rgba(10,11,10,0.08); --border-mid:rgba(10,11,10,0.14);
  --shadow-xs:0 1px 4px rgba(0,0,0,0.06); --shadow-sm:0 2px 12px rgba(0,0,0,0.07);
  --shadow-md:0 8px 28px rgba(0,0,0,0.09); --shadow-lg:0 20px 56px rgba(0,0,0,0.12);
  --f-display:'Fraunces',Georgia,serif;
  --f-body:'General Sans','Helvetica Neue',ui-sans-serif,sans-serif;
  --f-mono:'JetBrains Mono',monospace;
  --section-v:clamp(72px,8vw,108px);
  --slot-nutrition:#16a34a; --slot-nutrition-bg:#f0fdf4; --slot-nutrition-border:rgba(22,163,74,0.2);
  --slot-movement:#2563eb; --slot-movement-bg:#eff6ff; --slot-movement-border:rgba(37,99,235,0.18);
  --slot-sleep:#7c3aed; --slot-sleep-bg:#f5f3ff; --slot-sleep-border:rgba(124,58,237,0.18);
  --slot-routine:#d97706; --slot-routine-bg:#fffbeb; --slot-routine-border:rgba(217,119,6,0.2);
  --slot-family:#db2777; --slot-family-bg:#fdf2f8; --slot-family-border:rgba(219,39,119,0.18);
}

:global(*, *::before, *::after){box-sizing:border-box}
:global(body){margin:0;font-family:var(--f-body),system-ui;background:var(--c-white);color:var(--c-black);-webkit-font-smoothing:antialiased;overflow-x:hidden}

.roadmap-page{min-height:100vh;background:
  radial-gradient(circle at top left, rgba(22,163,74,.10), transparent 24%),
  radial-gradient(circle at top right, rgba(37,99,235,.08), transparent 22%),
  linear-gradient(180deg,#fbfcfb 0%, #eef3ef 52%, #f7f8f6 100%)}
.header{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.92);border-bottom:1px solid var(--border);backdrop-filter:blur(18px)}
.header-inner,.section-wrap,.hero-wrap{max-width:1280px;margin:0 auto;padding:0 40px}
.header-inner{height:76px;display:flex;align-items:center;justify-content:space-between}
.logo{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--c-black)}
.logo-icon{width:28px;height:28px;color:var(--c-black)}
.logo-text{font-family:var(--f-display);font-size:1.22rem;color:var(--c-black);letter-spacing:-.03em}
.nav{display:flex;align-items:center;gap:2px}
.nav-a,.nav-link{height:36px;padding:0 12px;display:flex;align-items:center;font-size:.86rem;font-weight:500;color:var(--c-500);text-decoration:none;border-radius:8px;transition:all .18s}
.nav-a:hover,.nav-link:hover{color:var(--c-black);background:var(--c-50)}
.nav-cta{display:flex;align-items:center;gap:8px}
.nav-btn{height:38px;padding:0 16px;display:inline-flex;align-items:center;gap:7px;font-size:.86rem;font-weight:600;color:var(--c-white);background:var(--c-black);text-decoration:none;border-radius:10px;border:1px solid var(--c-900);transition:all .2s}
.nav-btn:hover{background:var(--c-800);transform:translateY(-1px)}

.hero{position:relative;padding:56px 0 0;overflow:hidden}
.hero-bg{position:absolute;inset:0;pointer-events:none}
.hero-orb{position:absolute;border-radius:50%;filter:blur(10px);opacity:.9}
.orb-a{width:240px;height:240px;top:40px;left:-40px;background:radial-gradient(circle,#dcfce7 0%, rgba(220,252,231,0) 70%)}
.orb-b{width:280px;height:280px;right:6%;top:10px;background:radial-gradient(circle,rgba(219,234,254,.95) 0%, rgba(219,234,254,0) 72%)}
.orb-c{width:220px;height:220px;right:32%;bottom:-20px;background:radial-gradient(circle,rgba(233,213,255,.9) 0%, rgba(233,213,255,0) 72%)}
.hero-grid-lines{position:absolute;inset:30px 40px auto 40px;height:280px;border-radius:28px;background-image:linear-gradient(rgba(10,11,10,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(10,11,10,.04) 1px,transparent 1px);background-size:30px 30px;mask-image:linear-gradient(180deg,rgba(0,0,0,.6),transparent)}
.hero-wrap{position:relative;display:grid;grid-template-columns:minmax(0,1.02fr) minmax(360px,.98fr);gap:28px;align-items:stretch}
.hero-copy-col{padding:14px 0}
.section-eyebrow{display:inline-flex;align-items:center;gap:8px;height:26px;padding:0 11px;border-radius:999px;border:1px solid var(--border-mid);font-size:.68rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--c-500);margin-bottom:18px}
.hero-title,.section-h2{margin:0;font-family:var(--f-display);font-weight:400;letter-spacing:-.03em;line-height:1.02}
.hero-title{font-size:clamp(2.5rem,4.3vw,4.4rem);margin-bottom:18px}
.section-h2{font-size:clamp(2rem,3.2vw,3rem);margin-bottom:14px}
em{font-style:italic;color:var(--c-green)}
.hero-copy,.section-desc{font-size:.98rem;line-height:1.75;color:var(--c-500);max-width:40rem}
.hero-tags{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.hero-tag{height:30px;padding:0 12px;border-radius:999px;background:var(--c-green-soft);border:1px solid rgba(22,163,74,.18);color:var(--c-green);font-size:.74rem;font-weight:700;display:inline-flex;align-items:center}
.roadmap-hero-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}
.hero-action-solid,.hero-action-ghost{height:44px;padding:0 18px;border-radius:12px;display:inline-flex;align-items:center;justify-content:center;text-decoration:none;font-size:.88rem;font-weight:600;transition:all .2s ease}
.hero-action-solid{background:var(--c-black);border:1px solid var(--c-900);color:var(--c-white)}
.hero-action-solid:hover{background:var(--c-800);transform:translateY(-1px)}
.hero-action-ghost{background:transparent;border:1px solid var(--border-mid);color:var(--c-500)}
.hero-action-ghost:hover{background:var(--c-50);color:var(--c-black)}
.hero-micro-stats{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}
.hero-micro-card{min-width:120px;padding:12px 14px;border-radius:16px;background:rgba(255,255,255,.66);border:1px solid rgba(255,255,255,.72);backdrop-filter:blur(14px);box-shadow:var(--shadow-xs)}
.hero-micro-card span{display:block;font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:6px}
.hero-micro-card strong{font-family:var(--f-display);font-size:1rem;font-weight:400;color:var(--c-black)}
.hero-visual-board{display:grid;grid-template-columns:1fr .88fr;gap:16px;align-items:stretch;padding:18px;border-radius:30px;background:rgba(255,255,255,.58);border:1px solid rgba(255,255,255,.8);backdrop-filter:blur(18px);box-shadow:0 18px 50px rgba(0,0,0,.08)}
.hero-ring-panel{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;padding:24px;border-radius:24px;background:linear-gradient(160deg,rgba(255,255,255,.92),rgba(240,253,244,.7))}
.hero-ring-shell{width:250px;height:250px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 18px rgba(255,255,255,.58),0 20px 42px rgba(22,163,74,.12)}
.hero-ring-core{width:168px;height:168px;border-radius:50%;background:rgba(255,255,255,.96);display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(0,0,0,.08)}
.hero-ring-core span{display:block;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:8px}
.hero-ring-core strong{font-family:var(--f-display);font-size:3rem;font-weight:400;color:var(--c-black);line-height:1}
.hero-ring-core small{margin-top:8px;font-family:var(--f-mono);font-size:.74rem;font-weight:700;color:var(--c-400)}
.hero-selected-chip{min-height:40px;padding:0 16px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;font-size:.84rem;font-weight:700;border:1px solid rgba(10,11,10,.08);box-shadow:var(--shadow-xs)}
.hero-side-stack{display:grid;gap:14px}
.hero-kpi-card{padding:22px;border:1px solid var(--border);border-radius:22px;box-shadow:var(--shadow-sm)}
.hero-kpi-card.glass{background:rgba(255,255,255,.76);backdrop-filter:blur(14px)}
.hero-kpi-card span{display:block;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:8px}
.hero-kpi-card strong{display:block;font-family:var(--f-display);font-size:1.7rem;font-weight:400;color:var(--c-black);line-height:1.05;margin-bottom:8px}
.hero-kpi-card p{margin:0;font-size:.82rem;color:var(--c-500);line-height:1.6}
.hero-kpi-card.dark{background:linear-gradient(180deg,#101311,#171b18);border-color:rgba(255,255,255,.06)}
.hero-kpi-card.spotlight{position:relative;overflow:hidden}
.hero-kpi-card.spotlight::after{content:"";position:absolute;inset:auto -20px -35px auto;width:120px;height:120px;background:radial-gradient(circle,rgba(74,222,128,.18),transparent 70%)}
.hero-kpi-card.dark strong,.hero-kpi-card.dark p{color:var(--c-white)}
.hero-kpi-card.dark span{color:rgba(255,255,255,.4)}

.overview-section,.empty-state-section,.roadmap-section,.insights-section,.chart-section{padding:var(--section-v) 0}
.overview-section{padding-top:34px;padding-bottom:16px}
.overview-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:18px}
.overview-card{padding:22px;border-radius:22px;background:rgba(255,255,255,.9);border:1px solid rgba(255,255,255,.76);box-shadow:0 14px 36px rgba(0,0,0,.06)}
.overview-card.accent{background:linear-gradient(145deg,#f0fdf4,#ffffff);border-color:rgba(22,163,74,.16)}
.overview-card.dark{background:linear-gradient(180deg,#101311,#171b18);border-color:rgba(255,255,255,.06)}
.overview-label{display:block;font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:8px}
.overview-card.dark .overview-label{color:rgba(255,255,255,.35)}
.overview-card strong{display:block;font-family:var(--f-display);font-size:1.8rem;font-weight:400;color:var(--c-black);line-height:1.05;margin-bottom:8px}
.overview-card strong small{font-size:.55em;color:var(--c-400)}
.overview-card p{margin:0;font-size:.82rem;color:var(--c-500);line-height:1.6}
.overview-card.dark strong,.overview-card.dark p{color:var(--c-white)}
.visual-dashboard-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:20px}
.journey-panel,.heatmap-panel{padding:24px;border-radius:26px;background:rgba(255,255,255,.92);border:1px solid rgba(255,255,255,.74);box-shadow:0 20px 44px rgba(0,0,0,.06)}
.journey-head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:18px}
.journey-kicker{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:6px}
.journey-title{margin:0;font-family:var(--f-display);font-size:1.25rem;font-weight:400;color:var(--c-black);letter-spacing:-.02em}
.journey-total{font-family:var(--f-display);font-size:2rem;font-weight:400;color:var(--c-black);line-height:1}
.journey-track-wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
.journey-node{padding:14px 10px;border-radius:18px;border:1px solid var(--border);background:var(--c-50);display:flex;flex-direction:column;align-items:center;gap:8px;cursor:pointer;transition:all .18s ease}
.journey-node.active{background:var(--c-white);border-color:rgba(22,163,74,.28);box-shadow:0 0 0 3px rgba(22,163,74,.08)}
.journey-node-ring{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--f-display);font-size:1rem;color:var(--c-black);background:var(--c-white);border:1px solid var(--border)}
.journey-node.completed .journey-node-ring{background:#f0fdf4;border-color:rgba(22,163,74,.16);color:var(--c-green)}
.journey-node.in-progress .journey-node-ring{background:#fffbeb;border-color:rgba(217,119,6,.16);color:#b45309}
.journey-node-label{font-size:.7rem;font-weight:700;color:var(--c-500);text-transform:uppercase;letter-spacing:.08em}
.journey-node-pct{font-family:var(--f-mono);font-size:.74rem;font-weight:700;color:var(--c-400)}
.journey-bars{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;align-items:end;height:90px}
.journey-bar-col{display:flex;flex-direction:column;align-items:center;gap:8px;height:100%}
.journey-bar-track{width:100%;flex:1;background:rgba(0,0,0,.06);border-radius:10px 10px 4px 4px;display:flex;align-items:flex-end;overflow:hidden}
.journey-bar-fill{width:100%;border-radius:10px 10px 4px 4px}
.fill-completed{background:linear-gradient(180deg,#4ade80,#16a34a)}
.fill-in-progress{background:linear-gradient(180deg,#fbbf24,#d97706)}
.fill-not-started{background:rgba(148,163,184,.35)}
.journey-bar-col span{font-family:var(--f-mono);font-size:.66rem;color:var(--c-400);font-weight:700}
.heatmap-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:10px}
.heatmap-day{border:none;background:transparent;padding:0;display:flex;flex-direction:column;align-items:center;gap:8px;cursor:pointer}
.heatmap-day-label{font-family:var(--f-mono);font-size:.64rem;font-weight:700;color:var(--c-400);text-transform:uppercase}
.heatmap-day-box{width:100%;height:72px;border-radius:16px;background:linear-gradient(180deg,#16a34a,#86efac)}
.heatmap-day.active .heatmap-day-box{box-shadow:0 0 0 3px rgba(22,163,74,.16)}
.heatmap-day-value{font-size:.74rem;font-weight:700;color:var(--c-500)}
.heatmap-foot{display:flex;justify-content:space-between;gap:12px;margin-top:16px;font-size:.78rem;color:var(--c-500)}
.empty-state-section{padding-top:28px;padding-bottom:0}
.empty-state-card{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:center;padding:28px 30px;border-radius:24px;background:linear-gradient(145deg,#f0fdf4,#ffffff);border:1px solid rgba(22,163,74,.16);box-shadow:var(--shadow-sm)}
.empty-state-actions{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:flex-end}
.insights-section{padding-top:0}
.section-head-row{display:grid;grid-template-columns:1fr auto;gap:48px;align-items:start;margin-bottom:40px}
.roadmap-score-block{display:flex;align-items:center;gap:20px;padding:24px 28px;background:var(--c-white);border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow-sm)}
.rsb-ring{width:90px;height:90px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.rsb-ring-inner{width:62px;height:62px;border-radius:50%;background:var(--c-white);display:flex;flex-direction:column;align-items:center;justify-content:center}
.rsb-pct{font-family:var(--f-display);font-size:1.3rem;color:var(--c-black);line-height:1}
.rsb-pct span{font-size:.7em}
.rsb-lbl{font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--c-400)}
.rsb-num{font-family:var(--f-display);font-size:2rem;color:var(--c-black);line-height:1;margin-bottom:2px}
.rsb-num span{font-size:.55em;color:var(--c-400)}
.rsb-desc{font-size:.76rem;color:var(--c-400);margin-bottom:10px}
.rsb-focus-chip{display:inline-flex;height:24px;padding:0 10px;border-radius:999px;background:var(--c-green-pale);color:var(--c-green);font-size:.68rem;font-weight:700;align-items:center;letter-spacing:.06em;text-transform:uppercase}

.roadmap-weeks{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px}
.rweek-card{text-align:left;padding:22px;border-radius:24px;background:rgba(255,255,255,.92);border:1px solid rgba(255,255,255,.74);box-shadow:0 18px 38px rgba(0,0,0,.05);cursor:pointer;transition:all .25s ease;position:relative;overflow:hidden}
.rweek-card::after{content:"";position:absolute;inset:auto -30px -34px auto;width:120px;height:120px;background:radial-gradient(circle,rgba(22,163,74,.10),transparent 72%);pointer-events:none}
.rweek-card:hover{transform:translateY(-6px) scale(1.01);box-shadow:0 22px 50px rgba(0,0,0,.08)}
.rweek-card.active{border-color:rgba(22,163,74,.22);box-shadow:0 0 0 4px rgba(22,163,74,.10),0 22px 50px rgba(0,0,0,.08)}
.rweek-card.completed{background:linear-gradient(145deg,#f0fdf4,var(--c-white))}
.rweek-card.in-progress{background:linear-gradient(145deg,#fffbeb,var(--c-white))}
.rweek-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.rweek-num{font-family:var(--f-mono);font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.rweek-status{height:22px;padding:0 9px;border-radius:999px;font-size:.64rem;font-weight:700;display:inline-flex;align-items:center}
.rs-not-started{background:var(--c-50);color:var(--c-400)}
.rs-in-progress{background:var(--c-amber-soft);color:#b45309}
.rs-completed{background:var(--c-green-pale);color:var(--c-green)}
.rweek-icon{width:48px;height:48px;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:1.35rem;margin-bottom:12px;box-shadow:var(--shadow-xs)}
.week-theme-green{background:linear-gradient(145deg,#f0fdf4,#dcfce7);color:var(--c-green)}
.week-theme-amber{background:linear-gradient(145deg,#fffbeb,#fde68a);color:#b45309}
.week-theme-blue{background:linear-gradient(145deg,#eff6ff,#dbeafe);color:#2563eb}
.week-theme-violet{background:linear-gradient(145deg,#f5f3ff,#e9d5ff);color:#7c3aed}
.rweek-title{font-family:var(--f-display);font-size:1.1rem;color:var(--c-black);letter-spacing:-.02em;line-height:1.2;margin:0 0 8px}
.rweek-summary{font-size:.82rem;color:var(--c-500);line-height:1.55;margin:0 0 16px}
.rweek-meta-block{display:flex;flex-direction:column;gap:10px;margin-bottom:16px}
.rweek-meta-item{padding:12px 13px;border-radius:14px;background:var(--c-50);border:1px solid var(--border)}
.rweek-meta-label{display:block;font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:5px}
.rweek-meta-text{font-size:.77rem;color:var(--c-700);line-height:1.5;margin:0}
.rweek-progress-wrap{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.rweek-track{flex:1;height:6px;border-radius:999px;background:rgba(0,0,0,.07);overflow:hidden}
.rweek-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#4ade80,#16a34a)}
.rweek-pct{font-family:var(--f-mono);font-size:.7rem;font-weight:700;color:var(--c-400)}
.rweek-done-count{font-size:.72rem;font-weight:600;color:var(--c-400)}

.roadmap-detail{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(320px,.65fr);gap:24px;align-items:stretch}
.roadmap-detail-main{padding:32px;background:rgba(255,255,255,.94);border-radius:28px;border:1px solid rgba(255,255,255,.76);box-shadow:0 20px 50px rgba(0,0,0,.06)}
.rdm-header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:16px}
.rdm-eyebrow{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-400);margin-bottom:6px}
.rdm-title{font-family:var(--f-display);font-size:1.6rem;color:var(--c-black);letter-spacing:-.02em;line-height:1.15;margin:0}
.rdm-week-badge{display:inline-flex;height:32px;padding:0 14px;border-radius:999px;border:1px solid var(--border-mid);font-size:.8rem;font-weight:700;align-items:center;white-space:nowrap}
.rdm-week-badge.week-theme-green{background:#f0fdf4;border-color:rgba(22,163,74,.16);color:var(--c-green)}
.rdm-week-badge.week-theme-amber{background:#fffbeb;border-color:rgba(217,119,6,.16);color:#b45309}
.rdm-week-badge.week-theme-blue{background:#eff6ff;border-color:rgba(37,99,235,.16);color:#2563eb}
.rdm-week-badge.week-theme-violet{background:#f5f3ff;border-color:rgba(124,58,237,.16);color:#7c3aed}
.rdm-story-strip{display:grid;grid-template-columns:1.25fr .8fr .8fr;gap:12px;margin:0 0 18px}
.rdm-story-card{padding:16px 18px;border-radius:20px;background:rgba(244,245,242,.9);border:1px solid rgba(10,11,10,.06)}
.rdm-story-card.primary{background:linear-gradient(145deg,#f0fdf4,#ffffff);border-color:rgba(22,163,74,.16)}
.rdm-story-card span{display:block;font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:8px}
.rdm-story-card strong{display:block;font-family:var(--f-display);font-size:1rem;font-weight:400;color:var(--c-black);line-height:1.2;margin-bottom:8px}
.rdm-story-card p{margin:0;font-size:.78rem;color:var(--c-500);line-height:1.5}
.mini-day-bars{display:grid;grid-template-columns:repeat(7,1fr);gap:10px;align-items:end;height:88px;margin:0 0 22px}
.mini-day-bar{border:none;background:transparent;padding:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:8px;cursor:pointer}
.mini-day-bar-fill{width:100%;border-radius:10px 10px 4px 4px;background:linear-gradient(180deg,#86efac,#16a34a);min-height:8px;transition:all .18s ease}
.mini-day-bar.active .mini-day-bar-fill{box-shadow:0 0 0 3px rgba(22,163,74,.16)}
.mini-day-bar-label{font-family:var(--f-mono);font-size:.64rem;font-weight:700;color:var(--c-400);text-transform:uppercase}
.rdm-visual-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:22px}
.rdm-visual-card{padding:18px;border-radius:20px;background:rgba(244,245,242,.92);border:1px solid rgba(10,11,10,.06)}
.rdm-visual-card.accent{background:linear-gradient(145deg,#f0fdf4,#ffffff);border-color:rgba(22,163,74,.16)}
.rdm-visual-card span{display:block;font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:8px}
.rdm-visual-card strong{display:block;font-family:var(--f-display);font-size:1.4rem;font-weight:400;color:var(--c-black);line-height:1.05;margin-bottom:8px}
.rdm-visual-card p{margin:0;font-size:.76rem;color:var(--c-500);line-height:1.45}
.rdm-template-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px}
.rdm-template-card{padding:18px;border-radius:20px;background:rgba(244,245,242,.92);border:1px solid rgba(10,11,10,.06)}
.rdm-template-label{display:block;font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:8px}
.rdm-template-value{margin:0;font-family:var(--f-display);font-size:1.02rem;color:var(--c-black);line-height:1.35}
.rdm-template-value.body{font-family:var(--f-body);font-size:.88rem;font-weight:600;color:var(--c-700)}
.rdm-actions-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.rdm-actions-head span{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.rdm-actions-count{background:var(--c-green-pale);color:var(--c-green);padding:3px 10px;border-radius:999px;font-size:.7rem}
.rdm-actions-list{display:flex;flex-direction:column;gap:10px}
.rdm-action{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:18px;background:rgba(244,245,242,.9);border:1px solid rgba(10,11,10,.06);cursor:pointer;transition:all .18s ease}
.rdm-action:hover{transform:translateY(-1px);box-shadow:var(--shadow-xs)}
.rdm-action.done{opacity:.65}
.rdm-action input{position:absolute;opacity:0;pointer-events:none}
.rdm-check{width:22px;height:22px;border-radius:50%;border:1.5px solid var(--c-100);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.rdm-check.done{background:var(--c-green);border-color:var(--c-green)}
.rdm-action-text{font-size:.88rem;font-weight:500;color:var(--c-700)}
.rdm-action.done .rdm-action-text{text-decoration:line-through;color:var(--c-400)}

.rdm-day-plan-block{margin-top:28px;padding-top:24px;border-top:1px solid var(--border)}
.rdm-day-plan-head{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:18px}
.rdm-day-plan-head span{display:block;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--c-green);margin-bottom:6px}
.rdm-day-plan-head p{font-size:.84rem;color:var(--c-500);line-height:1.6;margin:0}
.rdm-day-plan-head strong{min-height:30px;padding:0 12px;display:inline-flex;align-items:center;border-radius:999px;background:var(--c-green-pale);color:var(--c-green);font-size:.78rem;font-weight:800}
.day-chip-strip{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:16px}
.day-chip{min-width:88px;padding:10px 12px;border-radius:14px;border:1px solid var(--border);background:var(--c-white);display:flex;flex-direction:column;gap:4px;align-items:flex-start;cursor:pointer;transition:all .18s ease}
.day-chip.active{background:var(--c-green-soft);border-color:rgba(22,163,74,.2);box-shadow:0 0 0 3px rgba(22,163,74,.08)}
.day-chip span{font-family:var(--f-mono);font-size:.66rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--c-400)}
.day-chip strong{font-size:.86rem;font-weight:700;color:var(--c-black)}
.rdm-day-plan-grid{display:flex;gap:14px;overflow-x:auto;padding-bottom:12px;scroll-snap-type:x mandatory}
.rdm-day-card{min-width:250px;max-width:262px;flex:0 0 250px;scroll-snap-align:start;padding:16px;border-radius:22px;background:rgba(244,245,242,.92);border:1px solid rgba(10,11,10,.06);box-shadow:var(--shadow-xs)}
.rdm-day-card.today{border:1px solid rgba(22,163,74,.18);background:linear-gradient(160deg,#f0fdf4,#ffffff);box-shadow:0 0 0 4px rgba(22,163,74,.08),0 14px 30px rgba(22,163,74,.08)}
.rdm-day-card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:8px}
.rdm-day-name{display:block;font-family:var(--f-mono);font-size:.66rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.rdm-day-card-head small{display:inline-flex;margin-top:4px;padding:2px 6px;border-radius:999px;background:var(--c-green);color:white;font-size:.55rem;font-weight:800;text-transform:uppercase}
.rdm-day-card-head strong{font-size:.68rem;color:var(--c-400);font-weight:800}
.rdm-day-mini-track{height:5px;border-radius:999px;overflow:hidden;background:rgba(0,0,0,.07);margin-bottom:10px}
.rdm-day-mini-fill{height:100%;border-radius:inherit;background:linear-gradient(90deg,#4ade80,#16a34a)}
.rdm-day-schedule{display:grid;gap:6px}
.rdm-time-slot{display:flex;gap:7px;align-items:flex-start;padding:7px 8px;border-radius:10px;border:1px solid transparent}
.rdm-time-slot.slot-nutrition{background:var(--slot-nutrition-bg);border-color:var(--slot-nutrition-border)}
.rdm-time-slot.slot-movement{background:var(--slot-movement-bg);border-color:var(--slot-movement-border)}
.rdm-time-slot.slot-sleep{background:var(--slot-sleep-bg);border-color:var(--slot-sleep-border)}
.rdm-time-slot.slot-routine{background:var(--slot-routine-bg);border-color:var(--slot-routine-border)}
.rdm-time-slot.slot-family{background:var(--slot-family-bg);border-color:var(--slot-family-border)}
.rdm-time-slot.done{opacity:.55}
.slot-time-col{display:flex;flex-direction:column;align-items:center;gap:3px;flex-shrink:0;padding-top:2px}
.slot-time{font-family:var(--f-mono);font-size:.56rem;font-weight:700;color:var(--c-400);white-space:nowrap}
.slot-cat-dot{width:5px;height:5px;border-radius:50%;background:currentColor;opacity:.4}
.slot-action-col{display:flex;align-items:flex-start;gap:5px;cursor:pointer;flex:1}
.slot-action-col input{position:absolute;opacity:0;pointer-events:none}
.slot-check{width:12px;height:12px;margin-top:2px;border-radius:50%;border:1.5px solid rgba(0,0,0,.15);flex-shrink:0;display:flex;align-items:center;justify-content:center}
.slot-check.done{background:var(--c-green);border-color:var(--c-green)}
.slot-text-wrap{display:flex;flex-direction:column;gap:2px}
.slot-text{font-size:.76rem;line-height:1.45;color:var(--c-700);font-weight:600}
.rdm-time-slot.done .slot-text{text-decoration:line-through;color:var(--c-300)}
.slot-tip{font-size:.6rem;color:var(--c-400);line-height:1.3;font-style:italic}
.schedule-legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:16px;padding-top:14px;border-top:1px solid var(--border)}
.legend-item{display:flex;align-items:center;gap:6px;font-size:.7rem;font-weight:600;color:var(--c-500)}
.legend-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.legend-nutrition .legend-dot{background:var(--slot-nutrition)}
.legend-movement .legend-dot{background:var(--slot-movement)}
.legend-sleep .legend-dot{background:var(--slot-sleep)}
.legend-routine .legend-dot{background:var(--slot-routine)}
.legend-family .legend-dot{background:var(--slot-family)}

.roadmap-feedback-panel{padding:28px;background:linear-gradient(180deg,#101311,#171b18);border-radius:28px;border:1px solid rgba(255,255,255,.06);display:flex;flex-direction:column;gap:20px;box-shadow:0 20px 50px rgba(0,0,0,.12)}
.rfp-status-row{display:flex;align-items:center;gap:14px}
.rfp-status-indicator{width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center}
.rfi-completed{background:rgba(74,222,128,.15);color:#4ade80}
.rfi-in-progress{background:rgba(251,191,36,.12);color:#fbbf24}
.rfi-not-started{background:rgba(255,255,255,.07);color:rgba(255,255,255,.4)}
.rfp-status-label{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);margin-bottom:3px}
.rfp-status-text{font-size:.88rem;font-weight:600;color:rgba(255,255,255,.8)}
.rfp-progress-donut{display:flex;justify-content:center}
.rfp-fb-title{font-family:var(--f-display);font-size:1.1rem;color:var(--c-white);margin-bottom:8px}
.rfp-fb-body{font-size:.84rem;color:rgba(255,255,255,.58);line-height:1.65;margin:0}
.rfp-signal-row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.rfp-signal-card{padding:14px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}
.rfp-signal-card span{display:block;font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);margin-bottom:6px}
.rfp-signal-card strong{font-family:var(--f-display);font-size:1.1rem;font-weight:400;color:var(--c-white)}
.rfp-guidance-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.rfp-guidance-card{padding:16px;border-radius:16px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}
.rfp-guidance-label{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.4);margin-bottom:6px}
.rfp-guidance-value{font-family:var(--f-display);font-size:1rem;color:var(--c-white);margin-bottom:6px}
.rfp-guidance-card p{font-size:.8rem;line-height:1.55;color:rgba(255,255,255,.58);margin:0}
.rfp-quiz-insights,.rfp-tip{padding:16px 18px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}
.rfp-qi-head,.rfp-tip-head,.rfp-aw-head{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);margin-bottom:10px}
.rfp-qi-chips{display:flex;flex-wrap:wrap;gap:6px}
.rfp-qi-chip{height:22px;padding:0 9px;border-radius:999px;background:rgba(22,163,74,.18);border:1px solid rgba(22,163,74,.25);color:#4ade80;font-size:.68rem;font-weight:700;display:inline-flex;align-items:center}
.rfp-tip p{font-size:.82rem;color:rgba(255,255,255,.58);margin:0;line-height:1.65}
.rfp-all-weeks{border-top:1px solid rgba(255,255,255,.06);padding-top:18px}
.rfp-week-bars{display:flex;gap:12px;align-items:flex-end;height:60px}
.rfp-wbar-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end}
.rfp-wbar-col.current .rfp-wbar-track{box-shadow:0 0 0 2px rgba(255,255,255,.2)}
.rfp-wbar-track{width:100%;flex:1;background:rgba(255,255,255,.07);border-radius:6px 6px 0 0;overflow:hidden;display:flex;align-items:flex-end}
.rfp-wbar-fill{width:100%;border-radius:6px 6px 0 0}
.rfp-wfill-completed{background:#4ade80}
.rfp-wfill-in-progress{background:#fbbf24}
.rfp-wfill-not-started{background:rgba(255,255,255,.12)}
.rfp-wbar-label{font-family:var(--f-mono);font-size:.6rem;font-weight:700;color:rgba(255,255,255,.35)}

.insights-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.insight-dark-card{padding:24px;background:linear-gradient(180deg,#101311,#171b18);border-radius:28px;border:1px solid rgba(255,255,255,.06);box-shadow:0 20px 50px rgba(0,0,0,.12)}
.tcc-eyebrow,.twc-eyebrow{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px}
.tcc-eyebrow{color:rgba(255,255,255,.35)}
.tcc-title{font-family:var(--f-display);font-size:1.15rem;color:var(--c-white);margin:0 0 10px}
.narrative-chip-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.narrative-chip{height:26px;padding:0 10px;border-radius:999px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.08);display:inline-flex;align-items:center;font-size:.68rem;font-weight:700;color:rgba(255,255,255,.72)}
.tcc-body{font-size:.84rem;color:rgba(255,255,255,.55);line-height:1.65;margin:0 0 20px}
.tcc-facts{display:flex;flex-direction:column;gap:12px}
.tcc-fact{padding:12px 14px;border-radius:12px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.07)}
.tcc-fact-label{font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.3);margin-bottom:4px}
.tcc-fact-val{font-size:.82rem;font-weight:500;color:rgba(255,255,255,.68);line-height:1.4}
.category-mix{display:grid;gap:12px;margin-top:18px;padding-top:18px;border-top:1px solid rgba(255,255,255,.08)}
.mix-row-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;font-size:.78rem;color:rgba(255,255,255,.68)}
.mix-row-top strong{font-family:var(--f-mono);font-size:.72rem;color:rgba(255,255,255,.82)}
.mix-row-track{height:8px;border-radius:999px;background:rgba(255,255,255,.08);overflow:hidden}
.mix-row-fill{height:100%;border-radius:inherit}
.mix-nutrition{background:#4ade80}
.mix-movement{background:#60a5fa}
.mix-sleep{background:#c084fc}
.mix-routine{background:#fbbf24}
.mix-family{background:#f472b6}
.insight-light-card{padding:24px;background:rgba(255,255,255,.92);border-radius:28px;border:1px solid rgba(255,255,255,.76);box-shadow:0 20px 50px rgba(0,0,0,.06)}
.twc-eyebrow{color:var(--c-400)}
.twc-title{font-family:var(--f-display);font-size:1.1rem;color:var(--c-black);margin:0 0 10px}
.risk-pill-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.risk-pill{height:26px;padding:0 10px;border-radius:999px;background:var(--c-white);border:1px solid var(--border);display:inline-flex;align-items:center;font-size:.68rem;font-weight:700;color:var(--c-500)}
.twc-body{font-size:.84rem;color:var(--c-500);line-height:1.65;margin:0}
.risk-stats{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:18px}
.risk-stat{padding:14px;border-radius:14px;background:var(--c-white);border:1px solid var(--border)}
.risk-stat span{display:block;font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:6px}
.risk-stat strong{font-family:var(--f-display);font-size:1.1rem;font-weight:400;color:var(--c-black)}

.chart-head-row{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:32px;gap:32px}
.cab-val{font-family:var(--f-display);font-size:2.4rem;font-weight:300;color:var(--c-black);letter-spacing:-.04em;line-height:1}
.cab-val span{font-size:.5em;color:var(--c-400)}
.cab-lbl{font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-top:4px}
.chart-card{display:grid;grid-template-columns:1fr 280px;gap:24px;padding:30px;background:rgba(255,255,255,.92);border:1px solid rgba(255,255,255,.74);border-radius:28px;box-shadow:0 20px 50px rgba(0,0,0,.06)}
.chart-bars-wrap{display:grid;grid-template-columns:repeat(7,1fr);gap:10px;align-items:end;min-height:200px}
.cbar-col{display:flex;flex-direction:column;align-items:center;gap:6px;border:none;background:transparent;padding:0;cursor:pointer}
.cbar-col.active .cbar-track{box-shadow:0 0 0 2px rgba(22,163,74,.25)}
.cbar-val{font-family:var(--f-mono);font-size:.68rem;font-weight:700;color:var(--c-400)}
.cbar-col.active .cbar-val{color:var(--c-green)}
.cbar-track{width:100%;height:140px;border-radius:8px;background:rgba(0,0,0,.06);overflow:hidden;display:flex;align-items:flex-end}
.cbar-fill{width:100%;border-radius:8px;background:linear-gradient(180deg,#86efac,#16a34a)}
.cbar-lbl{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--c-300)}
.chart-detail{padding:22px;background:var(--c-50);border-radius:16px;border:1px solid var(--border)}
.cd-eyebrow{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-400);margin-bottom:6px}
.cd-day{font-family:var(--f-display);font-size:1.2rem;color:var(--c-black);margin:0 0 6px}
.cd-score{font-family:var(--f-display);font-size:2.4rem;font-weight:300;color:var(--c-green);letter-spacing:-.04em;line-height:1;margin-bottom:4px}
.cd-score span{font-size:.5em}
.cd-meta{font-size:.78rem;color:var(--c-400);margin-bottom:14px}
.cd-tasks{display:flex;flex-direction:column;gap:7px}
.cd-task{display:flex;align-items:flex-start;gap:8px;font-size:.8rem;color:var(--c-500)}
.cd-task-dot{width:6px;height:6px;border-radius:50%;background:var(--c-300);flex-shrink:0;margin-top:5px}
.cd-task.done{opacity:.5}
.cd-task.done .cd-task-dot{background:var(--c-green)}
.cd-empty{font-size:.8rem;color:var(--c-300);font-style:italic;margin:0}

@media(max-width:1100px){
  .hero-wrap,.overview-grid,.visual-dashboard-grid,.section-head-row,.roadmap-detail,.insights-grid,.chart-card{grid-template-columns:1fr}
  .hero-visual-board{grid-template-columns:1fr}
  .hero-ring-panel{padding:20px}
  .roadmap-weeks{grid-template-columns:repeat(2,1fr)}
  .rdm-story-strip,.rdm-visual-stats,.rdm-template-grid,.rfp-signal-row,.rfp-guidance-grid{grid-template-columns:1fr}
  .empty-state-card{grid-template-columns:1fr}
  .empty-state-actions{justify-content:flex-start}
}

@media(max-width:700px){
  .header-inner,.section-wrap,.hero-wrap{padding-left:24px;padding-right:24px}
  .nav,.nav-link{display:none}
  .hero{padding-top:34px}
  .hero-grid-lines{inset:24px 24px auto 24px;height:220px}
  .hero-micro-stats{display:grid;grid-template-columns:1fr;gap:10px}
  .hero-ring-shell{width:210px;height:210px}
  .hero-ring-core{width:142px;height:142px}
  .hero-ring-core strong{font-size:2.3rem}
  .roadmap-weeks{grid-template-columns:1fr}
  .journey-track-wrap,.journey-bars,.heatmap-grid,.risk-stats{grid-template-columns:repeat(2,1fr)}
  .roadmap-score-block{padding:22px;gap:16px;flex-direction:column;align-items:flex-start}
  .rdm-day-card{min-width:82vw;flex-basis:82vw;max-width:82vw}
  .chart-bars-wrap{gap:5px}
  .cbar-track{height:100px}
  .heatmap-foot{flex-direction:column}
}
</style>
