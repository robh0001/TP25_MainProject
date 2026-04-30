<template>
  <div class="dashboard-page">
    <div class="noise-overlay" aria-hidden="true"></div>

    <!-- HEADER -->
    <header class="header" :class="{ scrolled: isScrolled }">
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
          <RouterLink to="/" class="nav-a">Home</RouterLink>
          <RouterLink to="/parent-entry" class="nav-a">Parent access</RouterLink>
          <RouterLink to="/young-person-dashboard" class="nav-a">Kids dashboard</RouterLink>
        </nav>

        <div class="nav-cta">
          <RouterLink to="/parent-quiz" class="nav-link">Retake quiz</RouterLink>
          <RouterLink to="/parent-quiz" class="nav-btn">
            New plan
            <svg width="12" height="12" viewBox="0 0 12 12">
              <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </RouterLink>
        </div>
      </div>
    </header>

    <main>
      <section class="dash-hero">
        <div class="dash-hero-bg">
          <div class="hero-blob hb-1"></div>
          <div class="hero-blob hb-2"></div>
          <div class="hero-lines" aria-hidden="true">
            <span v-for="n in 8" :key="n"></span>
          </div>
        </div>

        <div class="dash-hero-inner">
          <div class="dash-hero-left">
            <div class="eyebrow-row">
              <div class="live-badge">
                <span class="live-dot"></span>
                Parent dashboard · Week {{ currentWeek }}
              </div>
            </div>

            <h1 class="dash-h1">
              <span class="dh-serif">Good {{ timeOfDay }},</span>
            </h1>

            <p class="dash-hero-desc">
              Here's your personalised habit plan. Track today's actions, follow the 4-week roadmap,
              and build lasting routines - one small step at a time.
            </p>

            <div class="hero-kpi-row">
              <div class="hkpi">
                <div class="hkpi-val">{{ streakDays }}</div>
                <div class="hkpi-lbl">Day streak</div>
              </div>
              <div class="hkpi-div"></div>
              <div class="hkpi">
                <div class="hkpi-val">{{ roadmapCompletion }}%</div>
                <div class="hkpi-lbl">Roadmap done</div>
              </div>
              <div class="hkpi-div"></div>
              <div class="hkpi">
                <div class="hkpi-val">{{ completedTodayCount }}/{{ todayTasks.length }}</div>
                <div class="hkpi-lbl">Today's tasks</div>
              </div>
              <div class="hkpi-div"></div>
              <div class="hkpi">
                <div class="hkpi-val">{{ weeklyAverage }}%</div>
                <div class="hkpi-lbl">Weekly avg.</div>
              </div>
            </div>
          </div>

          <div class="dash-hero-right">
            <div class="mission-card" :class="{ celebrate: showCelebration }">
              <div v-if="showCelebration" class="confetti-layer" aria-hidden="true">
                <span v-for="p in confettiPieces" :key="p.id" class="confetti-piece" :style="p.style"></span>
              </div>

              <div class="mission-top">
                <div class="mission-eyebrow">Daily mission</div>
                <div class="streak-chip"> {{ streakDays }}-day streak</div>
              </div>

              <h2 class="mission-title">{{ mission }}</h2>
              <p class="mission-desc">Keep momentum by completing one healthy action today.</p>

              <div class="mission-progress-wrap">
                <div class="mp-labels">
                  <span>Streak progress</span>
                  <span>{{ streakDays }}/7 days</span>
                </div>
                <div class="mp-track">
                  <div class="mp-fill" :style="{ width: streakProgress + '%' }"></div>
                </div>
              </div>

              <button class="mission-btn" @click="completeMission">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M3 8l3.5 3.5L13 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                Mark mission done
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 4-WEEK ROADMAP -->
      <section class="roadmap-section" id="roadmap">
        <div class="section-wrap">
          <div class="section-head-row">
            <div class="section-head-left">
              <div class="section-eyebrow">4-week habit roadmap · User Story 4.1</div>
              <h2 class="section-h2">
                Your personalised<br />
                <em>habit journey.</em>
              </h2>
              <p class="section-desc">
                A structured path for {{ childName }} built around
                {{ primaryConcern === 'balanced' ? 'balanced healthy habits' : primaryConcern + ' improvement' }}
                - broken into four manageable weeks with clear daily actions and feedback.
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
                <div class="rsb-desc">actions completed</div>
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
              <div class="rweek-icon">{{ week.icon }}</div>
              <h3 class="rweek-title">{{ week.title }}</h3>
              <p class="rweek-summary">{{ week.summary }}</p>
              <div class="rweek-progress-wrap">
                <div class="rweek-track">
                  <div class="rweek-fill" :style="{ width: week.progress + '%' }"></div>
                </div>
                <span class="rweek-pct">{{ week.progress }}%</span>
              </div>
              <div class="rweek-done-count">{{ week.completed }}/{{ week.totalItems }} actions</div>
            </button>
          </div>

          <div class="roadmap-detail">
            <div class="roadmap-detail-main">
              <div class="rdm-header">
                <div>
                  <div class="rdm-eyebrow">Selected · Week {{ selectedRoadmapWeek.week }}</div>
                  <h3 class="rdm-title">{{ selectedRoadmapWeek.title }}</h3>
                </div>
                <div class="rdm-header-actions">
                  <div class="rdm-week-badge">{{ selectedRoadmapWeek.icon }} Week {{ selectedRoadmapWeek.week }}</div>

                  <button
                    v-if="!isEditingPlanner"
                    class="planner-edit-btn"
                    type="button"
                    @click="startEditingPlanner"
                  >
                    Edit planner
                  </button>

                  <div v-else class="planner-edit-actions">
                    <button class="planner-cancel-btn" type="button" @click="cancelEditingPlanner">
                      Cancel
                    </button>
                    <button class="planner-save-btn" type="button" @click="saveEditedPlanner">
                      Save changes
                    </button>
                  </div>
                </div>
              </div>

              <p class="rdm-detail">{{ selectedRoadmapWeek.detail }}</p>

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

              <!-- DAILY PLAN INSIDE SELECTED WEEK -->
              <div class="rdm-day-plan-block">
                <div class="rdm-day-plan-head">
                  <div>
                    <span>Daily schedule for Week {{ selectedRoadmapWeek.week }}</span>
                    <p>Time-blocked actions tailored to {{ childName }}'s focus areas - {{ focusLabel.toLowerCase() }} first, every day.</p>
                  </div>
                  <strong>{{ selectedRoadmapWeek.dailyCompleted }}/{{ selectedRoadmapWeek.dailyTotal }} done</strong>
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
                      <strong>{{ day.completed }}/{{ day.actions.length }}</strong>
                    </div>

                    <div class="rdm-day-mini-track">
                      <div class="rdm-day-mini-fill" :style="{ width: day.progress + '%' }"></div>
                    </div>

                    <!-- TIME-BLOCKED SCHEDULE SLOTS -->
                    <div class="rdm-day-schedule">
                      <div
                        v-for="slot in day.timeSlots"
                        :key="slot.id"
                        class="rdm-time-slot"
                        :class="['slot-' + slot.category, { done: slot.done, editing: isEditingPlanner }]"
                      >
                        <template v-if="!isEditingPlanner">
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
                        </template>

                        <template v-else>
                          <div class="slot-edit-form">
                            <div class="slot-edit-row">
                              <input
                                v-model="editablePlanner[slot.id].time"
                                class="slot-edit-time"
                                type="text"
                                placeholder="Time"
                              />

                              <select
                                v-model="editablePlanner[slot.id].category"
                                class="slot-edit-category"
                              >
                                <option value="nutrition">Nutrition</option>
                                <option value="movement">Movement</option>
                                <option value="sleep">Sleep / Wind-down</option>
                                <option value="routine">Routine</option>
                                <option value="family">Family time</option>
                              </select>
                            </div>

                            <input
                              v-model="editablePlanner[slot.id].text"
                              class="slot-edit-text"
                              type="text"
                              placeholder="Habit action"
                            />

                            <input
                              v-model="editablePlanner[slot.id].tip"
                              class="slot-edit-tip"
                              type="text"
                              placeholder="Optional parent tip"
                            />
                          </div>
                        </template>
                      </div>
                    </div>

                    <!-- Legacy simple actions fallback -->
                    <div v-if="!day.timeSlots || !day.timeSlots.length" class="rdm-day-actions">
                      <label
                        v-for="action in day.actions"
                        :key="action.id"
                        class="rdm-day-action"
                        :class="{ done: action.done }"
                      >
                        <input type="checkbox" :checked="action.done" @change="toggleRoadmapDailyAction(action.id)" />
                        <span class="rdm-day-check"></span>
                        <span>{{ action.text }}</span>
                      </label>
                    </div>
                  </article>
                </div>

                <!-- SCHEDULE LEGEND -->
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
                  <circle cx="44" cy="44" r="36" stroke="rgba(0,0,0,0.06)" stroke-width="8" fill="none" />
                  <circle
                    cx="44" cy="44" r="36"
                    :stroke="selectedRoadmapWeek.statusKey === 'completed' ? '#16a34a' : selectedRoadmapWeek.statusKey === 'in-progress' ? '#d97706' : '#e2e8f0'"
                    stroke-width="8" fill="none" stroke-linecap="round"
                    :stroke-dasharray="`${(selectedRoadmapWeek.progress / 100) * 226} 226`"
                    transform="rotate(-90 44 44)"
                    style="transition: stroke-dasharray 0.6s ease"
                  />
                  <text x="44" y="49" text-anchor="middle" font-size="14" font-weight="700" fill="#0a0b0a">{{ selectedRoadmapWeek.progress }}%</text>
                </svg>
              </div>

              <div class="rfp-feedback-block">
                <div class="rfp-fb-title">{{ selectedRoadmapWeek.feedbackTitle }}</div>
                <p class="rfp-fb-body">{{ selectedRoadmapWeek.feedback }}</p>
              </div>

              <!-- QUIZ INSIGHTS PANEL -->
              <div class="rfp-quiz-insights">
                <div class="rfp-qi-head">Plan tailored for</div>
                <div class="rfp-qi-chips">
                  <span v-for="tag in planTags" :key="tag" class="rfp-qi-chip">{{ tag }}</span>
                </div>
              </div>

              <div class="rfp-tip">
                <div class="rfp-tip-head">
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <circle cx="7" cy="7" r="6" stroke="#16a34a" stroke-width="1.3" />
                    <path d="M7 4.5v3M7 9v.5" stroke="#16a34a" stroke-width="1.3" stroke-linecap="round" />
                  </svg>
                  Parent tip
                </div>
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

      <!-- TODAY'S PLAN -->
      <section class="today-section">
        <div class="section-wrap">
          <div class="section-head-row">
            <div class="section-head-left">
              <div class="section-eyebrow">Today's plan</div>
              <h2 class="section-h2">
                {{ todayName }}'s<br />
                <em>actions.</em>
              </h2>
              <p class="section-desc">
                {{ completedTodayCount }} of {{ todayTasks.length }} tasks completed today.
                Keep going - consistency beats perfection.
              </p>
            </div>

            <div class="today-score-block">
              <div class="tsb-pct">{{ todayProgress }}<span>%</span></div>
              <div class="tsb-lbl">Today's progress</div>
              <div class="tsb-track">
                <div class="tsb-fill" :style="{ width: todayProgress + '%' }"></div>
              </div>
            </div>
          </div>

          <!-- TODAY'S FULL TIME-BLOCKED SCHEDULE -->
          <div class="today-schedule-card">
            <div class="tsc-header">
              <div>
                <div class="tsc-day">{{ todayName }}</div>
                <div class="tsc-sub">{{ childName }}'s personalised schedule · {{ focusLabel }} focus</div>
              </div>
              <div class="tsc-pct-chip" :class="todayProgress === 100 ? 'chip-green' : 'chip-default'">{{ todayProgress }}%</div>
            </div>

            <div class="tsc-progress-bar">
              <div class="tsc-pb-fill" :style="{ width: todayProgress + '%' }"></div>
            </div>

            <div class="tsc-timeline">
              <div
                v-for="slot in todayFullSchedule"
                :key="slot.id"
                class="tsc-slot"
                :class="['tsc-' + slot.category, { done: slot.done }]"
              >
                <div class="tsc-time-col">
                  <span class="tsc-time">{{ slot.time }}</span>
                </div>
                <div class="tsc-slot-line">
                  <div class="tsc-dot" :class="{ done: slot.done }"></div>
                  <div class="tsc-line"></div>
                </div>
                <label class="tsc-content">
                  <input type="checkbox" :checked="slot.done" @change="toggleTodayScheduleSlot(slot.id)" />
                  <div class="tsc-card" :class="{ done: slot.done }">
                    <div class="tsc-card-row">
                      <span class="tsc-cat-badge" :class="'badge-' + slot.category">{{ slot.categoryLabel }}</span>
                      <span class="tsc-check" :class="{ done: slot.done }">
                        <svg v-if="slot.done" width="10" height="10" viewBox="0 0 10 10">
                          <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                      </span>
                    </div>
                    <span class="tsc-text">{{ slot.text }}</span>
                    <span v-if="slot.detail" class="tsc-detail">{{ slot.detail }}</span>
                  </div>
                </label>
              </div>

              <p v-if="!todayFullSchedule.length" class="tsc-empty">
                Complete the quiz to generate {{ todayName }}'s schedule.
              </p>
            </div>
          </div>

          <div class="today-context-row">
            <div class="today-context-card">
              <div class="tcc-eyebrow">This week's focus</div>
              <h3 class="tcc-title">{{ weeklyNarrativeTitle }}</h3>
              <p class="tcc-body">{{ weeklyNarrative }}</p>
              <div class="tcc-facts">
                <div class="tcc-fact">
                  <div class="tcc-fact-label">Main concern</div>
                  <div class="tcc-fact-val">{{ concernSummary }}</div>
                </div>
                <div class="tcc-fact">
                  <div class="tcc-fact-label">Habit focus</div>
                  <div class="tcc-fact-val">{{ habitSummary }}</div>
                </div>
                <div class="tcc-fact">
                  <div class="tcc-fact-label">Expected win</div>
                  <div class="tcc-fact-val">{{ winNarrative }}</div>
                </div>
              </div>
            </div>

            <div class="today-week-card">
              <div class="twc-eyebrow">Risk to watch</div>
              <h3 class="twc-title">If you skip this week</h3>
              <p class="twc-body">{{ riskNarrative }}</p>
              <div class="twc-support-style">
                <div class="tss-label">Best support style</div>
                <div class="tss-val">{{ state.supportStyle || 'Daily micro-actions' }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- PROGRESS TRACKER -->
      <section class="tracker-section">
        <div class="section-wrap tracker-grid">
          <div class="tracker-main-card">
            <div class="tmc-header">
              <div>
                <div class="section-eyebrow">Progress tracker</div>
                <h2 class="section-h2 tracker-title">
                  Track healthy<br />
                  <em>wins.</em>
                </h2>
              </div>
              <div class="tmc-pct-ring">
                <svg width="72" height="72" viewBox="0 0 72 72">
                  <circle cx="36" cy="36" r="28" stroke="rgba(0,0,0,0.07)" stroke-width="7" fill="none" />
                  <circle
                    cx="36" cy="36" r="28" stroke="#16a34a" stroke-width="7" fill="none"
                    stroke-linecap="round"
                    :stroke-dasharray="`${(progressCompletion / 100) * 176} 176`"
                    transform="rotate(-90 36 36)"
                    style="transition: stroke-dasharray 0.6s ease"
                  />
                  <text x="36" y="41" text-anchor="middle" font-size="13" font-weight="700" fill="#0a0b0a">{{ progressCompletion }}%</text>
                </svg>
              </div>
            </div>

            <div class="tmc-items">
              <label
                v-for="item in resolvedProgressItems"
                :key="item.id"
                class="tmc-item"
                :class="{ done: item.done }"
              >
                <input type="checkbox" :checked="item.done" @change="toggleProgressItem(item.id)" />
                <span class="tmc-check" :class="{ done: item.done }">
                  <svg v-if="item.done" width="10" height="10" viewBox="0 0 10 10">
                    <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
                <span class="tmc-item-text">{{ item.text }}</span>
              </label>
            </div>
          </div>

          <div class="tracker-custom-card">
            <div class="section-eyebrow">Add your own</div>
            <h3 class="tcc2-title">Custom habit item</h3>
            <p class="tcc2-desc">Track something specific to your family's routine.</p>
            <div class="tcc2-form">
              <input
                v-model="newProgressItem"
                type="text"
                placeholder="e.g. Packed fruit for school"
                class="tcc2-input"
                @keyup.enter="addProgressItem"
              />
              <button class="tcc2-btn" @click="addProgressItem">
                <svg width="14" height="14" viewBox="0 0 14 14">
                  <path d="M7 2v10M2 7h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                </svg>
                Add item
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- WEEKLY CHART -->
      <section class="chart-section">
        <div class="section-wrap">
          <div class="chart-head-row">
            <div>
              <div class="section-eyebrow">Weekly progress</div>
              <h2 class="section-h2 chart-section-title">
                7-day habit<br />
                <em>consistency.</em>
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
              <p class="cd-meta">{{ selectedDay.completed }} of {{ selectedDay.total }} tasks completed</p>
              <div class="cd-tasks">
                <div v-for="task in selectedDay.tasks" :key="task.id" class="cd-task" :class="{ done: task.done }">
                  <span class="cd-task-dot" :class="{ done: task.done }"></span>
                  <span>{{ task.text }}</span>
                </div>
                <p v-if="!selectedDay.tasks.length" class="cd-empty">No tasks for this day.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- WHY THIS MATTERS -->
      <section class="why-section">
        <div class="section-wrap why-inner">
          <div class="why-left">
            <div class="section-eyebrow light">Why this matters</div>
            <h2 class="why-h2">
              The science behind<br />
              <em>small habits.</em>
            </h2>
            <p class="why-copy">{{ weeklyNarrative }}</p>
            <div class="why-facts">
              <div class="why-fact">
                <div class="wf-label">Risk if skipped</div>
                <div class="wf-val">{{ riskNarrative }}</div>
              </div>
              <div class="why-fact">
                <div class="wf-label">Expected win</div>
                <div class="wf-val">{{ winNarrative }}</div>
              </div>
              <div class="why-fact">
                <div class="wf-label">Support style</div>
                <div class="wf-val">{{ state.supportStyle || 'Daily micro-actions' }}</div>
              </div>
            </div>
          </div>

          <div class="why-right">
            <div class="why-stat-grid">
              <div class="wsg-card">
                <div class="wsg-n">21</div>
                <div class="wsg-l">days to build early habit consistency</div>
              </div>
              <div class="wsg-card">
                <div class="wsg-n">3x</div>
                <div class="wsg-l">more effective with parent involvement</div>
              </div>
              <div class="wsg-card">
                <div class="wsg-n">4</div>
                <div class="wsg-l">weeks of structured small actions</div>
              </div>
              <div class="wsg-card">
                <div class="wsg-n">1</div>
                <div class="wsg-l">small action per day - all it takes</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-col">
          <RouterLink to="/" class="logo footer-logo">
            <div class="logo-icon footer-logo-icon">
              <svg viewBox="0 0 36 36" fill="none">
                <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2" />
                <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor" />
              </svg>
            </div>
            <span class="logo-text">HealthyKids</span>
          </RouterLink>
          <p class="footer-blurb">A Monash University SDG 3 project<br />Team TP25 · 2025</p>
        </div>
        <div class="footer-col">
          <div class="footer-col-head">Navigate</div>
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/parent-entry">Parent access</RouterLink>
          <RouterLink to="/parent-quiz">Retake quiz</RouterLink>
          <RouterLink to="/young-person-dashboard">Kids dashboard</RouterLink>
        </div>
        <div class="footer-col">
          <div class="footer-col-head">Legal</div>
          <a href="#">Privacy policy</a>
          <a href="#">Terms of use</a>
          <a href="#">Contact us</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2025 HealthyKids · Monash University · Good Health &amp; Wellbeing (UN SDG 3) · All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'

const { state, savePlan } = useFamilyPlanStore()

const TIME_ZONE = 'Australia/Melbourne'
const LOCALE = 'en-AU'
const DAY_LABEL_LENGTH = 3
const API_BASE_URL = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL

function getTodayName() {
  return new Date().toLocaleDateString(LOCALE, {
    weekday: 'long',
    timeZone: TIME_ZONE,
  })
}

function getShortDayName(dayName) {
  return dayName.slice(0, DAY_LABEL_LENGTH)
}

const isScrolled = ref(false)
const showCelebration = ref(false)
const newProgressItem = ref('')
const selectedDayLabel = ref(getShortDayName(getTodayName()))
const activeRoadmapWeek = ref(1)
const isEditingPlanner = ref(false)
const editablePlanner = ref({})

const orderedDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

const scheduleCategories = [
  { key: 'nutrition', label: 'Nutrition' },
  { key: 'movement', label: 'Movement' },
  { key: 'sleep', label: 'Sleep / Wind-down' },
  { key: 'routine', label: 'Routine' },
  { key: 'family', label: 'Family time' },
]

const defaultDailyPlan = {
  Monday: [
    { id: 101, text: 'Prepare one healthy after-school snack', done: false },
    { id: 102, text: 'Encourage 15 minutes of movement', done: false },
  ],
  Tuesday: [
    { id: 201, text: 'Do one screen-free activity together', done: false },
    { id: 202, text: 'Keep a calm bedtime cue', done: false },
  ],
  Wednesday: [
    { id: 301, text: 'Repeat the after-school snack routine', done: false },
    { id: 302, text: 'Offer water before snacks', done: false },
  ],
  Thursday: [
    { id: 401, text: 'Encourage active play before screens', done: false },
    { id: 402, text: 'Use one predictable routine cue', done: false },
  ],
  Friday: [
    { id: 501, text: 'Celebrate one healthy win from the week', done: false },
    { id: 502, text: 'Choose one easy family meal together', done: false },
  ],
  Saturday: [
    { id: 601, text: 'Do one family movement activity', done: false },
    { id: 602, text: 'Keep one healthy snack visible', done: false },
  ],
  Sunday: [
    { id: 701, text: 'Review the week and reset for Monday', done: false },
    { id: 702, text: 'Plan one routine goal for next week', done: false },
  ],
}

const defaultProgressItems = [
  { id: 1, text: 'Healthy snack prepared', done: false, custom: false },
  { id: 2, text: 'Active play completed', done: false, custom: false },
  { id: 3, text: 'Bedtime routine followed', done: false, custom: false },
  { id: 4, text: 'Screen-free family time completed', done: false, custom: false },
]


const childName = computed(() => state.childName || 'Your child')
const mission = computed(() => state.mission || 'Complete one healthy habit win together today.')
const streakDays = computed(() => state.streakDays || 0)
const streakProgress = computed(() => Math.min((streakDays.value / 7) * 100, 100))

const timeOfDay = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 17) return 'afternoon'
  return 'evening'
})

const todayName = computed(() => getTodayName())

const resolvedDailyPlan = computed(() => {
  const base = state.dailyPlan && Object.keys(state.dailyPlan).length
    ? state.dailyPlan
    : defaultDailyPlan
  return orderedDays.reduce((acc, day) => {
    acc[day] = base[day] || []
    return acc
  }, {})
})

const resolvedProgressItems = computed(() =>
  state.progressItems?.length ? state.progressItems : defaultProgressItems
)

const todayTasks = computed(() => resolvedDailyPlan.value[todayName.value] || [])
const completedTodayCount = computed(() => todayTasks.value.filter(t => t.done).length)
const todayProgress = computed(() =>
  todayTasks.value.length
    ? Math.round((completedTodayCount.value / todayTasks.value.length) * 100)
    : 0
)

const progressCompletion = computed(() => {
  const items = resolvedProgressItems.value
  return items.length
    ? Math.round((items.filter(i => i.done).length / items.length) * 100)
    : 0
})


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
  const name = childName.value
  if (name && name !== 'Your child') tags.push(name)
  if (primaryConcern.value !== 'balanced') tags.push(focusLabel.value + ' focus')
  const age = state.childAge
  if (age) tags.push('Age ' + age)
  const habits = state.habits || []
  if (habits.includes('Regular bedtime') || habits.includes('Consistent sleep')) tags.push('Sleep habits')
  if (habits.includes('Healthy snacking') || habits.includes('Balanced meals')) tags.push('Nutrition habits')
  const style = state.supportStyle
  if (style) tags.push(style)
  if (!tags.length) tags.push('Personalised plan')
  return tags.slice(0, 5)
})

const concernSummary = computed(() =>
  state.concerns?.length ? state.concerns.join(', ') : 'Nutrition, activity, sleep, and routine'
)

const habitSummary = computed(() =>
  state.habits?.length ? state.habits.join(', ') : 'Balanced meals and bedtime consistency'
)

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
  if (c.includes('Sleep consistency') || c.includes('Bedtime feels inconsistent'))
    return `${name} may struggle with energy and mood if sleep stays inconsistent. Prioritising bedtime structure can improve appetite, attention, and after-school behaviour.`
  if (c.includes('Nutrition') || c.includes('My child snacks too often'))
    return `${name} needs consistent fuel through the day. Better snack quality can stabilise energy, reduce irritability, and support healthy growth habits.`
  return `${name}'s plan is focused on consistency. One repeated healthy action each day is the strongest predictor of long-term habit success.`
})

const riskNarrative = computed(() => {
  const c = state.concerns || []
  if (c.includes('Routine battles') || c.includes('Our family routine feels hard to manage'))
    return 'Daily friction increases and healthy habits become harder to sustain.'
  if (c.includes('Physical activity') || c.includes('My child is not active enough'))
    return 'Lower movement can affect mood regulation and sleep quality.'
  return 'Inconsistent habits reduce progress and make routines harder to maintain.'
})

const winNarrative = computed(() => {
  const c = state.concerns || []
  if (c.includes('Nutrition') || c.includes('My child snacks too often'))
    return 'Higher energy and fewer snack-related conflicts after school.'
  if (c.includes('Sleep consistency') || c.includes('Bedtime feels inconsistent'))
    return 'Calmer evenings and more predictable morning routines.'
  return 'Better consistency with less parent-child conflict across the day.'
})

function buildTimeSlots(focusKey, weekNumber, dayName, childNameVal, stateRef, baseId) {
  const name = childNameVal || 'your child'
  const age = stateRef.childAge || 8
  const isYoung = age <= 7
  const isWeekend = dayName === 'Saturday' || dayName === 'Sunday'
  const concerns = stateRef.concerns || []
  const hasScreenIssue = concerns.includes('Too much screen time') || concerns.includes('Screen time battles')
  const hasSleepIssue = concerns.includes('Sleep consistency') || concerns.includes('Bedtime feels inconsistent')
  const hasNutritionIssue = concerns.includes('Nutrition') || concerns.includes('My child snacks too often')
  const hasMovementIssue = concerns.includes('Physical activity') || concerns.includes('My child is not active enough')
  const hasRoutineIssue = concerns.includes('Routine battles') || concerns.includes('Our family routine feels hard to manage')

  // Slot factory
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


const todayFullSchedule = computed(() => {
  const today = todayName.value
  const weekNum = currentWeek.value
  const baseId = `week-${weekNum}-${today.toLowerCase()}`

  const slots = buildTimeSlots(
    primaryConcern.value,
    weekNum,
    today,
    childName.value,
    state,
    baseId
  )

  return slots.map(slot => {
    const editedSlot = applyPlannerOverrides(slot)
    return {
      ...editedSlot,
      id: `today-schedule-${slot.id}`,
      done: Boolean((state.todaySchedule || {})[`today-schedule-${slot.id}`]),
    }
  })
})

function toggleTodayScheduleSlot(slotId) {
  const updated = {
    ...(state.todaySchedule || {}),
    [slotId]: !(state.todaySchedule || {})[slotId],
  }
  const updatedState = { ...state, todaySchedule: updated }
  saveAndPersist(updatedState)
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
      id: 1, week: 1,
      title: roadmapFocus.value.w1,
      summary: 'Start small - the goal is to make one action feel easy to repeat.',
      detail: 'Week 1 focuses on starting gently. The goal is not perfection - it is to make one healthy routine feel possible without adding pressure.',
      actions: [`Choose one daily habit to try with ${name}`, 'Complete the habit at least three times this week', 'Celebrate one small win together'],
      parentTip: 'Keep the first week very small. A habit that feels easy is far more likely to continue than one that feels like a chore.',
    },
    {
      id: 2, week: 2,
      title: roadmapFocus.value.w2,
      summary: 'Turn the first habit into something predictable and expected.',
      detail: 'Week 2 builds consistency. Families begin connecting the habit to a regular part of the day, making it feel automatic rather than intentional.',
      actions: ['Attach the habit to an existing family routine', 'Use one visual or verbal cue to remind everyone', 'Track progress without applying pressure'],
      parentTip: 'Try linking the habit to something that already happens - after school, dinner, or bedtime. This is called habit stacking.',
    },
    {
      id: 3, week: 3,
      title: roadmapFocus.value.w3,
      summary: 'Strengthen the routine and reduce daily resistance.',
      detail: 'Week 3 makes the habit smoother. The aim is to reduce reminders, arguments, or pushback - and let your child take some ownership.',
      actions: [`Let ${name} help choose how the habit is completed`, 'Repeat the habit on at least four days this week', 'Notice what makes the habit easier or harder'],
      parentTip: 'Children are more engaged when they feel involved. Offer simple choices rather than instructions - it shifts the dynamic significantly.',
    },
    {
      id: 4, week: 4,
      title: roadmapFocus.value.w4,
      summary: 'Reflect, adjust, and make the habit sustainable beyond this plan.',
      detail: 'Week 4 helps families reflect, adapt, and decide what to continue. The goal is to identify one or two habits worth keeping long-term.',
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
      const timeSlots = buildTimeSlots(
        primaryConcern.value,
        week.week,
        day,
        childName.value,
        state,
        baseId
      )

      const slotsWithDoneState = timeSlots.map(slot => {
        const editedSlot = applyPlannerOverrides(slot)

        return {
          ...editedSlot,
          done: Boolean(roadmapProgressMap.value[slot.id]),
        }
      })

      const legacyActions = slotsWithDoneState.map((slot, i) => ({
        id: `${baseId}-legacy-${i}`,
        text: slot.text,
        done: slot.done,
      }))

      const completed = slotsWithDoneState.filter(s => s.done).length
      const progress = slotsWithDoneState.length
        ? Math.round((completed / slotsWithDoneState.length) * 100)
        : 0

      return { day, actions: legacyActions, timeSlots: slotsWithDoneState, completed, progress }
    })

    const weeklyCompleted = actions.filter(a => a.done).length
    const dailyCompleted = dailyPlan.reduce((sum, d) => sum + d.completed, 0)
    const dailyTotal = dailyPlan.reduce((sum, d) => sum + d.timeSlots.length, 0)
    const totalItems = actions.length + dailyTotal
    const completedItems = weeklyCompleted + dailyCompleted
    const progress = totalItems ? Math.round((completedItems / totalItems) * 100) : 0

    let status = 'Not started'
    let statusKey = 'not-started'
    if (progress > 0 && progress < 100) { status = 'In progress'; statusKey = 'in-progress' }
    if (progress === 100) { status = 'Completed'; statusKey = 'completed' }

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
    }
  })
)

const selectedRoadmapWeek = computed(() =>
  fourWeekRoadmap.value.find(w => w.id === activeRoadmapWeek.value) || fourWeekRoadmap.value[0]
)

const currentFirstRoadmapDailyPlan = computed(() => {
  const plan = selectedRoadmapWeek.value?.dailyPlan || []
  const todayIndex = plan.findIndex(day => day.day === todayName.value)
  if (todayIndex === -1) return plan
  return [
    plan[todayIndex],
    ...plan.slice(0, todayIndex),
    ...plan.slice(todayIndex + 1),
  ]
})

const totalRoadmapActions = computed(() => fourWeekRoadmap.value.reduce((s, w) => s + w.totalItems, 0))
const completedRoadmapActions = computed(() => fourWeekRoadmap.value.reduce((s, w) => s + w.completed, 0))
const roadmapCompletion = computed(() =>
  totalRoadmapActions.value ? Math.round((completedRoadmapActions.value / totalRoadmapActions.value) * 100) : 0
)

const roadmapRingStyle = computed(() => {
  const pct = roadmapCompletion.value
  const color = pct === 100 ? '#16a34a' : pct > 0 ? '#d97706' : '#e2e8f0'
  return { background: `conic-gradient(${color} ${pct}%, rgba(0,0,0,0.07) ${pct}%)` }
})

const currentWeek = computed(() => {
  const total = fourWeekRoadmap.value.reduce((s, w) => s + w.progress, 0)
  if (total === 0) return 1
  const avg = total / 4
  if (avg >= 75) return 4
  if (avg >= 50) return 3
  if (avg >= 25) return 2
  return 1
})

const weeklyProgress = computed(() =>
  orderedDays.map((day) => {
    const tasks = resolvedDailyPlan.value[day] || []
    const completed = tasks.filter(t => t.done).length
    return {
      label: day.slice(0, 3),
      fullLabel: day,
      value: tasks.length ? Math.round((completed / tasks.length) * 100) : 0,
      completed,
      total: tasks.length,
      tasks,
    }
  })
)

const selectedDay = computed(() =>
  weeklyProgress.value.find(d => d.label === selectedDayLabel.value) ||
  weeklyProgress.value[0] ||
  { label: 'Mon', fullLabel: 'Monday', value: 0, completed: 0, total: 0, tasks: [] }
)

const weeklyAverage = computed(() => {
  const total = weeklyProgress.value.reduce((s, d) => s + d.value, 0)
  return Math.round(total / weeklyProgress.value.length)
})

const confettiPieces = computed(() =>
  Array.from({ length: 16 }, (_, i) => ({
    id: i,
    style: { left: `${4 + i * 6}%`, animationDelay: `${i * 0.04}s`, transform: `rotate(${i * 22}deg)` },
  }))
)

function saveAndPersist(updatedState) {
  savePlan(updatedState)
  persistDashboardUpdate(updatedState).catch(error => {
    console.error('Failed to sync dashboard update:', error)
  })
}


function startEditingPlanner() {
  const editable = {}

  selectedRoadmapWeek.value.dailyPlan.forEach(day => {
    day.timeSlots.forEach(slot => {
      editable[slot.id] = {
        time: slot.time,
        text: slot.text,
        tip: slot.tip || '',
        category: slot.category,
      }
    })
  })

  editablePlanner.value = editable
  isEditingPlanner.value = true
}

function cancelEditingPlanner() {
  editablePlanner.value = {}
  isEditingPlanner.value = false
}

function saveEditedPlanner() {
  const currentOverrides = state.plannerOverrides || {}

  const updatedOverrides = {
    ...currentOverrides,
    ...editablePlanner.value,
  }

  const updatedState = {
    ...state,
    plannerOverrides: updatedOverrides,
  }

  saveAndPersist(updatedState)
  editablePlanner.value = {}
  isEditingPlanner.value = false
}


function toggleProgressItem(itemId) {
  const updated = resolvedProgressItems.value.map(item =>
    item.id === itemId ? { ...item, done: !item.done } : item
  )
  const updatedState = { ...state, progressItems: updated }
  saveAndPersist(updatedState)
}

function toggleRoadmapAction(actionId) {
  const updated = { ...(state.roadmapProgress || {}), [actionId]: !state.roadmapProgress?.[actionId] }
  const updatedState = { ...state, roadmapProgress: updated }
  saveAndPersist(updatedState)
}

function toggleRoadmapDailyAction(actionId) {
  const updated = { ...(state.roadmapProgress || {}), [actionId]: !state.roadmapProgress?.[actionId] }
  const updatedState = { ...state, roadmapProgress: updated }
  saveAndPersist(updatedState)
}

function addProgressItem() {
  const value = newProgressItem.value.trim()
  if (!value) return
  const newItem = { id: Date.now(), text: value, done: false, custom: true }
  const updatedState = { ...state, progressItems: [...resolvedProgressItems.value, newItem] }
  saveAndPersist(updatedState)
  newProgressItem.value = ''
}

function completeMission() {
  const updatedState = { ...state, streakDays: (state.streakDays || 0) + 1 }
  saveAndPersist(updatedState)
  showCelebration.value = true
  setTimeout(() => { showCelebration.value = false }, 2000)
}

async function persistDashboardUpdate(updatedState) {
  const username = updatedState.username || state.username
  if (!username) throw new Error('Missing username')
  if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')

  const response = await fetch(
    `${API_BASE_URL}/parent-profiles/${encodeURIComponent(username)}`,
    {
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
    }
  )
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.error || `Dashboard update failed: ${response.status}`)
  return data
}

function onScroll() { isScrolled.value = window.scrollY > 40 }

onMounted(() => {
  selectedDayLabel.value = getShortDayName(todayName.value)
  window.addEventListener('scroll', onScroll, { passive: true })
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
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
  --r-md:14px; --r-lg:20px; --r-xl:28px;
  --section-v:clamp(80px,9vw,120px);
  /* Schedule slot category colors */
  --slot-nutrition: #16a34a;
  --slot-nutrition-bg: #f0fdf4;
  --slot-nutrition-border: rgba(22,163,74,0.2);
  --slot-movement: #2563eb;
  --slot-movement-bg: #eff6ff;
  --slot-movement-border: rgba(37,99,235,0.18);
  --slot-sleep: #7c3aed;
  --slot-sleep-bg: #f5f3ff;
  --slot-sleep-border: rgba(124,58,237,0.18);
  --slot-routine: #d97706;
  --slot-routine-bg: #fffbeb;
  --slot-routine-border: rgba(217,119,6,0.2);
  --slot-family: #db2777;
  --slot-family-bg: #fdf2f8;
  --slot-family-border: rgba(219,39,119,0.18);
}

@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400;1,9..144,500&display=swap');
@import url('https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600&display=swap');

:global(*,*::before,*::after){box-sizing:border-box}
:global(body){margin:0;font-family:var(--f-body),system-ui;background:var(--c-white);color:var(--c-black);-webkit-font-smoothing:antialiased;overflow-x:hidden}

.dashboard-page{min-height:100vh;overflow-x:clip;position:relative}
.noise-overlay{position:fixed;inset:0;pointer-events:none;z-index:9999;opacity:.025;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:256px}

/* TYPOGRAPHY */
h1,h2,h3{margin:0;font-family:var(--f-display);font-weight:400;letter-spacing:-0.03em;line-height:1.02}
em{font-style:italic;color:var(--c-green)}
p{font-family:var(--f-body);font-size:clamp(.9rem,1vw,1rem);line-height:1.75;color:var(--c-500);margin:0 0 1em}
p:last-child{margin-bottom:0}

.section-eyebrow{display:inline-flex;align-items:center;gap:8px;height:26px;padding:0 11px;border-radius:999px;border:1px solid var(--border-mid);font-family:var(--f-body);font-size:.68rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--c-500);margin-bottom:18px}
.section-eyebrow.light{border-color:rgba(255,255,255,.25);color:rgba(255,255,255,.55)}
.section-wrap{max-width:1280px;margin:0 auto;padding:0 40px}
.section-h2{font-size:clamp(2rem,3.5vw,3.2rem);margin-bottom:14px}
.section-desc{max-width:32rem;font-size:clamp(.9rem,1vw,.98rem)}

/* HEADER */
.header{position:fixed;top:0;left:0;right:0;z-index:500;transition:background .3s,border-color .3s,box-shadow .3s}
.header.scrolled{background:rgba(255,255,255,.92);border-bottom:1px solid var(--border);backdrop-filter:blur(20px);box-shadow:var(--shadow-xs)}
.header-inner{display:flex;align-items:center;justify-content:space-between;max-width:1280px;margin:0 auto;padding:0 40px;height:76px}
.logo{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--c-black)}
.logo-icon{width:28px;height:28px;color:var(--c-black)}
.logo-text{font-family:var(--f-display);font-size:1.22rem;font-weight:400;letter-spacing:-.03em;color:var(--c-black)}
.nav{display:flex;align-items:center;gap:2px}
.nav-a{height:36px;padding:0 12px;display:flex;align-items:center;font-family:var(--f-body);font-size:.86rem;font-weight:500;color:var(--c-500);text-decoration:none;border-radius:8px;transition:color .18s,background .18s}
.nav-a:hover{color:var(--c-black);background:var(--c-50)}
.nav-cta{display:flex;align-items:center;gap:8px}
.nav-link{height:36px;padding:0 14px;display:flex;align-items:center;font-family:var(--f-body);font-size:.86rem;font-weight:500;color:var(--c-500);text-decoration:none;border-radius:8px;transition:all .18s}
.nav-link:hover{color:var(--c-black);background:var(--c-50)}
.nav-btn{height:38px;padding:0 16px;display:inline-flex;align-items:center;gap:7px;font-family:var(--f-body);font-size:.86rem;font-weight:600;color:var(--c-white);background:var(--c-black);text-decoration:none;border-radius:10px;border:1px solid var(--c-900);box-shadow:0 1px 3px rgba(0,0,0,.2),0 0 0 1px rgba(255,255,255,.06) inset;transition:all .2s}
.nav-btn:hover{background:var(--c-800);transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.24)}

.dash-hero{position:relative;padding:120px 0 0;overflow:hidden;background:var(--c-white)}
.dash-hero-bg{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.hero-blob{position:absolute;border-radius:50%;filter:blur(90px)}
.hb-1{width:700px;height:700px;top:-200px;right:-100px;background:radial-gradient(circle,rgba(22,163,74,.08) 0%,transparent 70%)}
.hb-2{width:500px;height:500px;bottom:0;left:-100px;background:radial-gradient(circle,rgba(59,130,246,.05) 0%,transparent 70%)}
.hero-lines{position:absolute;inset:0;display:grid;grid-template-columns:repeat(8,1fr)}
.hero-lines span{border-right:1px solid rgba(10,11,10,.03)}
.dash-hero-inner{max-width:1280px;margin:0 auto;padding:0 40px 0;display:grid;grid-template-columns:1fr 420px;gap:60px;align-items:center;position:relative;z-index:2}
.eyebrow-row{margin-bottom:28px}
.live-badge{display:inline-flex;align-items:center;gap:8px;height:30px;padding:0 12px;border-radius:999px;background:var(--c-green-soft);border:1px solid rgba(22,163,74,.2);font-family:var(--f-body);font-size:.72rem;font-weight:600;color:var(--c-green)}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--c-green-mid);animation:live-pulse 2.4s ease-in-out infinite}
@keyframes live-pulse{0%,100%{box-shadow:0 0 0 0 rgba(34,197,94,.45)}50%{box-shadow:0 0 0 4px rgba(34,197,94,0)}}
.dash-h1{display:flex;flex-direction:column;margin-bottom:20px}
.dh-serif{font-family:var(--f-display);font-weight:300;font-size:clamp(2.4rem,5vw,5.6rem);color:var(--c-black);letter-spacing:-.04em;line-height:.96}
.dh-name{font-family:var(--f-display);font-style:italic;font-size:clamp(2rem,4.2vw,4.8rem);font-weight:400;color:var(--c-green);letter-spacing:-.04em;line-height:1}
.dash-hero-desc{max-width:28rem;font-size:clamp(.94rem,1.05vw,1.02rem);color:var(--c-500);margin-bottom:36px}
.hero-kpi-row{display:flex;align-items:center;gap:0;padding:20px 24px;background:var(--c-white);border:1px solid var(--border);border-radius:16px;box-shadow:var(--shadow-sm)}
.hkpi{flex:1;text-align:center}
.hkpi-val{font-family:var(--f-display);font-size:1.8rem;font-weight:400;color:var(--c-black);letter-spacing:-.03em;line-height:1}
.hkpi-lbl{font-family:var(--f-body);font-size:.68rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--c-400);margin-top:4px}
.hkpi-div{width:1px;height:40px;background:var(--border);flex-shrink:0}

/* Mission card */
.mission-card{position:relative;overflow:hidden;padding:28px;border-radius:24px;background:linear-gradient(145deg,#f0fdf4,#dcfce7);border:1.5px solid rgba(22,163,74,.2);box-shadow:var(--shadow-md)}
.mission-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.mission-eyebrow{font-family:var(--f-body);font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-green)}
.streak-chip{display:inline-flex;align-items:center;gap:5px;height:26px;padding:0 10px;border-radius:999px;background:rgba(22,163,74,.12);border:1px solid rgba(22,163,74,.2);font-size:.72rem;font-weight:700;color:var(--c-green)}
.mission-title{font-family:var(--f-display);font-size:1.5rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;line-height:1.2;margin-bottom:10px}
.mission-desc{font-size:.86rem;color:var(--c-500);margin-bottom:18px}
.mission-progress-wrap{margin-bottom:20px}
.mp-labels{display:flex;justify-content:space-between;font-size:.74rem;font-weight:600;color:var(--c-500);margin-bottom:8px}
.mp-track{height:8px;border-radius:999px;background:rgba(22,163,74,.15);overflow:hidden}
.mp-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .5s ease}
.mission-btn{display:inline-flex;align-items:center;gap:8px;height:48px;padding:0 22px;border-radius:12px;border:none;background:var(--c-black);color:var(--c-white);font-family:var(--f-body);font-size:.9rem;font-weight:600;cursor:pointer;transition:all .2s;width:100%;justify-content:center}
.mission-btn:hover{background:var(--c-800);transform:translateY(-1px);box-shadow:0 6px 20px rgba(0,0,0,.2)}
.confetti-layer{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.confetti-piece{position:absolute;top:-14px;width:10px;height:18px;border-radius:4px;background:linear-gradient(180deg,#86efac 0%,#facc15 100%);animation:confettiFall 1.4s ease forwards}
@keyframes confettiFall{0%{opacity:0;transform:translateY(0) rotate(0deg)}10%{opacity:1}100%{opacity:0;transform:translateY(260px) rotate(240deg)}}


.roadmap-section{padding:var(--section-v) 0;background:var(--c-50);border-top:1px solid var(--border)}
.section-head-row{display:grid;grid-template-columns:1fr auto;gap:48px;align-items:start;margin-bottom:48px}
.roadmap-score-block{display:flex;align-items:center;gap:20px;padding:24px 28px;background:var(--c-white);border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow-sm);flex-shrink:0}
.rsb-ring{width:90px;height:90px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 4px 16px rgba(0,0,0,.1)}
.rsb-ring-inner{width:62px;height:62px;border-radius:50%;background:var(--c-white);display:flex;flex-direction:column;align-items:center;justify-content:center}
.rsb-pct{font-family:var(--f-display);font-size:1.3rem;font-weight:400;color:var(--c-black);line-height:1}
.rsb-pct span{font-size:.7em}
.rsb-lbl{font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--c-400)}
.rsb-num{font-family:var(--f-display);font-size:2rem;font-weight:400;color:var(--c-black);letter-spacing:-.03em;line-height:1;margin-bottom:2px}
.rsb-num span{font-size:.55em;color:var(--c-400)}
.rsb-desc{font-size:.76rem;font-weight:500;color:var(--c-400);margin-bottom:10px}
.rsb-focus-chip{display:inline-flex;height:24px;padding:0 10px;border-radius:999px;background:var(--c-green-pale);color:var(--c-green);font-size:.68rem;font-weight:700;align-items:center;letter-spacing:.06em;text-transform:uppercase}
.roadmap-weeks{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px}
.rweek-card{text-align:left;padding:22px;border-radius:20px;background:var(--c-white);border:1.5px solid var(--border);box-shadow:var(--shadow-xs);cursor:pointer;transition:all .25s ease;display:flex;flex-direction:column;gap:0}
.rweek-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-md);border-color:var(--border-mid)}
.rweek-card.active{border-color:rgba(22,163,74,.35);box-shadow:0 0 0 3px rgba(22,163,74,.08),var(--shadow-md)}
.rweek-card.completed{border-color:rgba(22,163,74,.25);background:linear-gradient(145deg,#f0fdf4,var(--c-white))}
.rweek-card.in-progress{border-color:rgba(217,119,6,.25)}
.rweek-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.rweek-num{font-family:var(--f-mono);font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.rweek-status{height:22px;padding:0 9px;border-radius:999px;font-size:.64rem;font-weight:700;display:inline-flex;align-items:center}
.rs-not-started{background:var(--c-50);color:var(--c-400)}
.rs-in-progress{background:var(--c-amber-soft);color:#b45309}
.rs-completed{background:var(--c-green-pale);color:var(--c-green)}
.rweek-icon{font-size:1.6rem;margin-bottom:12px}
.rweek-title{font-family:var(--f-display);font-size:1.1rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;line-height:1.2;margin-bottom:8px}
.rweek-summary{font-size:.82rem;color:var(--c-500);line-height:1.55;margin-bottom:16px;flex:1}
.rweek-progress-wrap{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.rweek-track{flex:1;height:6px;border-radius:999px;background:rgba(0,0,0,.07);overflow:hidden}
.rweek-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .4s ease}
.rweek-pct{font-family:var(--f-mono);font-size:.7rem;font-weight:700;color:var(--c-400);min-width:28px;text-align:right}
.rweek-done-count{font-size:.72rem;font-weight:600;color:var(--c-400)}
.roadmap-detail{display:grid;grid-template-columns:1.1fr .9fr;gap:20px}
.roadmap-detail-main{padding:32px;background:var(--c-white);border-radius:20px;border:1px solid var(--border);box-shadow:var(--shadow-sm)}
.rdm-header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:16px}
.rdm-eyebrow{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-400);margin-bottom:6px}
.rdm-title{font-family:var(--f-display);font-size:1.6rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;line-height:1.15}
.rdm-week-badge{display:inline-flex;height:32px;padding:0 14px;border-radius:999px;background:var(--c-50);border:1px solid var(--border-mid);font-size:.8rem;font-weight:700;color:var(--c-500);align-items:center;white-space:nowrap}
.rdm-header-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:flex-end}
.planner-edit-btn,.planner-save-btn,.planner-cancel-btn{height:34px;padding:0 13px;border-radius:999px;font-family:var(--f-body);font-size:.76rem;font-weight:700;cursor:pointer;transition:all .18s ease}
.planner-edit-btn{border:1px solid rgba(22,163,74,.25);background:var(--c-green-pale);color:var(--c-green)}
.planner-edit-btn:hover{background:var(--c-green);color:white;transform:translateY(-1px)}
.planner-edit-actions{display:flex;gap:8px;align-items:center}
.planner-cancel-btn{border:1px solid var(--border-mid);background:var(--c-white);color:var(--c-500)}
.planner-cancel-btn:hover{background:var(--c-50);color:var(--c-black)}
.planner-save-btn{border:1px solid var(--c-black);background:var(--c-black);color:white}
.planner-save-btn:hover{background:var(--c-800);transform:translateY(-1px)}
.rdm-detail{font-size:.9rem;color:var(--c-500);line-height:1.7;margin-bottom:24px}
.rdm-actions-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.rdm-actions-head span{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.rdm-actions-count{background:var(--c-green-pale);color:var(--c-green);padding:3px 10px;border-radius:999px;font-size:.7rem}
.rdm-actions-list{display:flex;flex-direction:column;gap:10px}
.rdm-action{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:14px;background:var(--c-50);border:1px solid var(--border);cursor:pointer;transition:all .18s}
.rdm-action:hover{background:var(--c-white);border-color:var(--border-mid);box-shadow:var(--shadow-xs)}
.rdm-action.done{opacity:.65}
.rdm-action input{position:absolute;opacity:0;pointer-events:none}
.rdm-check{width:22px;height:22px;border-radius:50%;border:1.5px solid var(--c-100);display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all .2s}
.rdm-check.done{background:var(--c-green);border-color:var(--c-green)}
.rdm-action-text{font-family:var(--f-body);font-size:.88rem;font-weight:500;color:var(--c-700)}
.rdm-action.done .rdm-action-text{text-decoration:line-through;color:var(--c-400)}

/* DAILY PLAN INSIDE ROADMAP */
.rdm-day-plan-block{margin-top:28px;padding-top:24px;border-top:1px solid var(--border)}
.rdm-day-plan-head{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:18px}
.rdm-day-plan-head span{display:block;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--c-green);margin-bottom:6px}
.rdm-day-plan-head p{font-size:.84rem;color:var(--c-500);line-height:1.6;margin:0}
.rdm-day-plan-head strong{flex-shrink:0;min-height:30px;padding:0 12px;display:inline-flex;align-items:center;border-radius:999px;background:var(--c-green-pale);color:var(--c-green);font-size:.78rem;font-weight:800}
.rdm-day-plan-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:10px}

/* Day card in roadmap */
.rdm-day-card{padding:14px;border-radius:16px;background:var(--c-50);border:1px solid var(--border);transition:.18s ease}
.rdm-day-card:hover{background:var(--c-white);box-shadow:var(--shadow-xs)}
.rdm-day-card.today{border-color:rgba(22,163,74,.35);background:linear-gradient(160deg,#f0fdf4,var(--c-white))}
.rdm-day-card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:8px}
.rdm-day-name{display:block;font-family:var(--f-mono);font-size:.66rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.rdm-day-card-head small{display:inline-flex;margin-top:4px;padding:2px 6px;border-radius:999px;background:var(--c-green);color:white;font-size:.55rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em}
.rdm-day-card-head strong{font-size:.68rem;color:var(--c-400);font-weight:800}
.rdm-day-mini-track{height:5px;border-radius:999px;overflow:hidden;background:rgba(0,0,0,.07);margin-bottom:10px}
.rdm-day-mini-fill{height:100%;border-radius:inherit;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .3s ease}

/* TIME SLOTS in roadmap day cards */
.rdm-day-schedule{display:grid;gap:6px}
.rdm-time-slot{display:flex;gap:7px;align-items:flex-start;padding:7px 8px;border-radius:10px;border:1px solid transparent;transition:all .15s}
.rdm-time-slot.slot-nutrition{background:var(--slot-nutrition-bg);border-color:var(--slot-nutrition-border)}
.rdm-time-slot.slot-movement{background:var(--slot-movement-bg);border-color:var(--slot-movement-border)}
.rdm-time-slot.slot-sleep{background:var(--slot-sleep-bg);border-color:var(--slot-sleep-border)}
.rdm-time-slot.slot-routine{background:var(--slot-routine-bg);border-color:var(--slot-routine-border)}
.rdm-time-slot.slot-family{background:var(--slot-family-bg);border-color:var(--slot-family-border)}
.rdm-time-slot.done{opacity:.5}
.rdm-time-slot.editing{padding:10px;background:var(--c-white);border-color:rgba(22,163,74,.22);box-shadow:var(--shadow-xs)}
.slot-edit-form{width:100%;display:grid;gap:8px}
.slot-edit-row{display:grid;grid-template-columns:90px 1fr;gap:8px}
.slot-edit-time,.slot-edit-category,.slot-edit-text,.slot-edit-tip{width:100%;min-height:34px;border-radius:9px;border:1px solid var(--border-mid);background:var(--c-white);padding:0 10px;font-family:var(--f-body);font-size:.72rem;color:var(--c-700);outline:none}
.slot-edit-text,.slot-edit-tip{min-height:36px}
.slot-edit-time:focus,.slot-edit-category:focus,.slot-edit-text:focus,.slot-edit-tip:focus{border-color:var(--c-green);box-shadow:0 0 0 3px rgba(22,163,74,.1)}
.slot-time-col{display:flex;flex-direction:column;align-items:center;gap:3px;flex-shrink:0;padding-top:2px}
.slot-time{font-family:var(--f-mono);font-size:.56rem;font-weight:700;color:var(--c-400);white-space:nowrap}
.slot-cat-dot{width:5px;height:5px;border-radius:50%;background:currentColor;opacity:.4}
.slot-action-col{display:flex;align-items:flex-start;gap:5px;cursor:pointer;flex:1}
.slot-action-col input{position:absolute;opacity:0;pointer-events:none}
.slot-check{width:12px;height:12px;margin-top:2px;border-radius:50%;border:1.5px solid rgba(0,0,0,.15);flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:all .15s}
.slot-check.done{background:var(--c-green);border-color:var(--c-green)}
.slot-text-wrap{display:flex;flex-direction:column;gap:2px}
.slot-text{font-size:.68rem;line-height:1.4;color:var(--c-700);font-weight:500}
.rdm-time-slot.done .slot-text{text-decoration:line-through;color:var(--c-300)}
.slot-tip{font-size:.6rem;color:var(--c-400);line-height:1.3;font-style:italic}

/* Legacy day actions fallback */
.rdm-day-actions{display:grid;gap:7px}
.rdm-day-action{position:relative;display:flex;align-items:flex-start;gap:7px;cursor:pointer}
.rdm-day-action input{position:absolute;opacity:0;pointer-events:none}
.rdm-day-check{width:13px;height:13px;margin-top:3px;border-radius:50%;border:1.5px solid var(--c-100);flex-shrink:0}
.rdm-day-action.done .rdm-day-check{background:var(--c-green);border-color:var(--c-green)}
.rdm-day-action span:last-child{font-size:.72rem;line-height:1.4;color:var(--c-500)}
.rdm-day-action.done span:last-child{color:var(--c-300);text-decoration:line-through}

/* SCHEDULE LEGEND */
.schedule-legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:16px;padding-top:14px;border-top:1px solid var(--border)}
.legend-item{display:flex;align-items:center;gap:6px;font-size:.7rem;font-weight:600;color:var(--c-500)}
.legend-nutrition .legend-dot{background:var(--slot-nutrition)}
.legend-movement .legend-dot{background:var(--slot-movement)}
.legend-sleep .legend-dot{background:var(--slot-sleep)}
.legend-routine .legend-dot{background:var(--slot-routine)}
.legend-family .legend-dot{background:var(--slot-family)}
.legend-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}

/* Feedback panel */
.roadmap-feedback-panel{padding:28px;background:var(--c-900);border-radius:20px;border:1px solid rgba(255,255,255,.06);display:flex;flex-direction:column;gap:20px}
.rfp-status-row{display:flex;align-items:center;gap:14px}
.rfp-status-indicator{width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.rfi-completed{background:rgba(74,222,128,.15);color:#4ade80}
.rfi-in-progress{background:rgba(251,191,36,.12);color:#fbbf24}
.rfi-not-started{background:rgba(255,255,255,.07);color:rgba(255,255,255,.4)}
.rfp-status-label{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);margin-bottom:3px}
.rfp-status-text{font-family:var(--f-body);font-size:.88rem;font-weight:600;color:rgba(255,255,255,.8)}
.rfp-progress-donut{display:flex;justify-content:center}
.rfp-feedback-block{}
.rfp-fb-title{font-family:var(--f-display);font-size:1.1rem;font-weight:500;color:var(--c-white);margin-bottom:8px;letter-spacing:-.02em}
.rfp-fb-body{font-size:.84rem;color:rgba(255,255,255,.5);line-height:1.65;margin:0}

/* Quiz insights */
.rfp-quiz-insights{padding:16px 18px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}
.rfp-qi-head{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.3);margin-bottom:10px}
.rfp-qi-chips{display:flex;flex-wrap:wrap;gap:6px}
.rfp-qi-chip{height:22px;padding:0 9px;border-radius:999px;background:rgba(22,163,74,.18);border:1px solid rgba(22,163,74,.25);color:#4ade80;font-size:.68rem;font-weight:700;display:inline-flex;align-items:center}

.rfp-tip{padding:16px 18px;border-radius:14px;background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.18)}
.rfp-tip-head{display:flex;align-items:center;gap:6px;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#4ade80;margin-bottom:8px}
.rfp-tip p{font-size:.82rem;color:rgba(255,255,255,.55);margin:0;line-height:1.65}
.rfp-all-weeks{border-top:1px solid rgba(255,255,255,.06);padding-top:18px}
.rfp-aw-head{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);margin-bottom:14px}
.rfp-week-bars{display:flex;gap:12px;align-items:flex-end;height:60px}
.rfp-wbar-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end}
.rfp-wbar-col.current .rfp-wbar-track{box-shadow:0 0 0 2px rgba(255,255,255,.2)}
.rfp-wbar-track{width:100%;flex:1;background:rgba(255,255,255,.07);border-radius:6px 6px 0 0;overflow:hidden;display:flex;align-items:flex-end}
.rfp-wbar-fill{width:100%;border-radius:6px 6px 0 0;transition:height .5s ease}
.rfp-wfill-completed{background:#4ade80}
.rfp-wfill-in-progress{background:#fbbf24}
.rfp-wfill-not-started{background:rgba(255,255,255,.12)}
.rfp-wbar-label{font-family:var(--f-mono);font-size:.6rem;font-weight:700;color:rgba(255,255,255,.35)}

.today-section{padding:var(--section-v) 0;background:var(--c-white);border-top:1px solid var(--border)}
.today-score-block{text-align:center;padding:24px 32px;background:var(--c-50);border:1px solid var(--border);border-radius:20px;min-width:180px;flex-shrink:0}
.tsb-pct{font-family:var(--f-display);font-size:3rem;font-weight:300;color:var(--c-black);letter-spacing:-.04em;line-height:1}
.tsb-pct span{font-size:.4em;color:var(--c-400)}
.tsb-lbl{font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin:6px 0 14px}
.tsb-track{height:8px;border-radius:999px;background:rgba(0,0,0,.07);overflow:hidden}
.tsb-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .5s ease}

/* TODAY FULL SCHEDULE CARD */
.today-schedule-card{background:var(--c-white);border:1px solid var(--border);border-radius:24px;box-shadow:var(--shadow-md);overflow:hidden;margin-top:32px;margin-bottom:24px}
.tsc-header{display:flex;justify-content:space-between;align-items:flex-start;padding:24px 28px 16px;background:var(--c-50);border-bottom:1px solid var(--border)}
.tsc-day{font-family:var(--f-display);font-size:1.6rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em}
.tsc-sub{font-size:.76rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--c-400);margin-top:4px}
.tsc-pct-chip{height:32px;padding:0 14px;border-radius:999px;font-size:.86rem;font-weight:700;display:inline-flex;align-items:center}
.chip-green{background:var(--c-green-pale);color:var(--c-green)}
.chip-default{background:var(--c-50);border:1px solid var(--border-mid);color:var(--c-500)}
.tsc-progress-bar{height:5px;background:rgba(0,0,0,.06);overflow:hidden}
.tsc-pb-fill{height:100%;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .5s ease}

/* TIMELINE */
.tsc-timeline{padding:16px 24px 24px;display:grid;gap:0}
.tsc-slot{display:grid;grid-template-columns:56px 24px 1fr;gap:0 12px;align-items:stretch;min-height:72px;position:relative}
.tsc-slot:last-child .tsc-line{display:none}
.tsc-time-col{display:flex;align-items:flex-start;padding-top:16px;justify-content:flex-end}
.tsc-time{font-family:var(--f-mono);font-size:.68rem;font-weight:700;color:var(--c-400);white-space:nowrap}
.tsc-slot-line{display:flex;flex-direction:column;align-items:center;padding-top:16px}
.tsc-dot{width:12px;height:12px;border-radius:50%;border:2px solid var(--c-100);background:var(--c-white);flex-shrink:0;transition:all .2s;z-index:1}
.tsc-dot.done{background:var(--c-green);border-color:var(--c-green)}
.tsc-line{flex:1;width:2px;background:var(--border);margin-top:4px}

/* Slot category colors on dot */
.tsc-nutrition .tsc-dot{border-color:rgba(22,163,74,.4)}
.tsc-nutrition .tsc-dot.done{background:var(--slot-nutrition);border-color:var(--slot-nutrition)}
.tsc-movement .tsc-dot{border-color:rgba(37,99,235,.3)}
.tsc-movement .tsc-dot.done{background:var(--slot-movement);border-color:var(--slot-movement)}
.tsc-sleep .tsc-dot{border-color:rgba(124,58,237,.3)}
.tsc-sleep .tsc-dot.done{background:var(--slot-sleep);border-color:var(--slot-sleep)}
.tsc-routine .tsc-dot{border-color:rgba(217,119,6,.3)}
.tsc-routine .tsc-dot.done{background:var(--slot-routine);border-color:var(--slot-routine)}
.tsc-family .tsc-dot{border-color:rgba(219,39,119,.3)}
.tsc-family .tsc-dot.done{background:var(--slot-family);border-color:var(--slot-family)}

.tsc-content{display:flex;align-items:flex-start;padding:10px 0 14px;cursor:pointer}
.tsc-content input{position:absolute;opacity:0;pointer-events:none}
.tsc-card{flex:1;padding:12px 16px;border-radius:14px;background:var(--c-50);border:1px solid var(--border);transition:all .18s}
.tsc-card:hover{background:var(--c-white);box-shadow:var(--shadow-xs);border-color:var(--border-mid)}
.tsc-card.done{opacity:.55}
.tsc-card-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.tsc-cat-badge{height:20px;padding:0 8px;border-radius:999px;font-size:.62rem;font-weight:700;display:inline-flex;align-items:center;letter-spacing:.06em;text-transform:uppercase}
.badge-nutrition{background:var(--slot-nutrition-bg);color:var(--slot-nutrition);border:1px solid var(--slot-nutrition-border)}
.badge-movement{background:var(--slot-movement-bg);color:var(--slot-movement);border:1px solid var(--slot-movement-border)}
.badge-sleep{background:var(--slot-sleep-bg);color:var(--slot-sleep);border:1px solid var(--slot-sleep-border)}
.badge-routine{background:var(--slot-routine-bg);color:var(--slot-routine);border:1px solid var(--slot-routine-border)}
.badge-family{background:var(--slot-family-bg);color:var(--slot-family);border:1px solid var(--slot-family-border)}
.tsc-check{width:20px;height:20px;border-radius:50%;border:1.5px solid var(--c-100);display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all .2s}
.tsc-check.done{background:var(--c-green);border-color:var(--c-green)}
.tsc-text{display:block;font-size:.9rem;font-weight:500;color:var(--c-700);line-height:1.4}
.tsc-card.done .tsc-text{text-decoration:line-through;color:var(--c-400)}
.tsc-detail{display:block;margin-top:5px;font-size:.78rem;color:var(--c-400);line-height:1.5;font-style:italic}
.tsc-empty{font-size:.9rem;color:var(--c-400);font-style:italic;padding:24px 0;text-align:center;margin:0}

/* Today context row */
.today-context-row{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.today-context-card{padding:24px;background:var(--c-900);border-radius:20px;border:1px solid rgba(255,255,255,.06)}
.tcc-eyebrow{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:rgba(255,255,255,.35);margin-bottom:8px}
.tcc-title{font-family:var(--f-display);font-size:1.15rem;font-weight:500;color:var(--c-white);letter-spacing:-.02em;margin-bottom:10px;line-height:1.2}
.tcc-body{font-size:.84rem;color:rgba(255,255,255,.5);line-height:1.65;margin-bottom:20px}
.tcc-facts{display:flex;flex-direction:column;gap:12px}
.tcc-fact{padding:12px 14px;border-radius:12px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.07)}
.tcc-fact-label{font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.3);margin-bottom:4px}
.tcc-fact-val{font-size:.82rem;font-weight:500;color:rgba(255,255,255,.65);line-height:1.4}
.today-week-card{padding:24px;background:var(--c-50);border-radius:20px;border:1px solid var(--border)}
.twc-eyebrow{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-400);margin-bottom:8px}
.twc-title{font-family:var(--f-display);font-size:1.1rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;margin-bottom:10px;line-height:1.2}
.twc-body{font-size:.84rem;color:var(--c-500);line-height:1.65;margin-bottom:20px}
.tss-label{font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:6px}
.tss-val{font-family:var(--f-display);font-size:1.1rem;font-weight:400;color:var(--c-black);letter-spacing:-.01em}

.tracker-section{padding:var(--section-v) 0;background:var(--c-white);border-top:1px solid var(--border)}
.tracker-grid{display:grid;grid-template-columns:1.4fr .6fr;gap:20px}
.tracker-main-card{padding:32px;background:var(--c-white);border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow-sm)}
.tmc-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:24px}
.tmc-items{display:flex;flex-direction:column;gap:8px}
.tmc-item{display:flex;align-items:center;gap:12px;padding:13px 16px;border-radius:12px;background:var(--c-50);border:1px solid var(--border);cursor:pointer;transition:all .18s}
.tmc-item:hover{background:var(--c-white);box-shadow:var(--shadow-xs);border-color:var(--border-mid)}
.tmc-item.done{opacity:.6}
.tmc-item input{position:absolute;opacity:0;pointer-events:none}
.tmc-check{width:20px;height:20px;border-radius:50%;border:1.5px solid var(--c-100);display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all .2s}
.tmc-check.done{background:var(--c-green);border-color:var(--c-green)}
.tmc-item-text{font-size:.88rem;font-weight:500;color:var(--c-700)}
.tmc-item.done .tmc-item-text{text-decoration:line-through;color:var(--c-400)}
.tracker-custom-card{padding:28px;background:var(--c-50);border:1px solid var(--border);border-radius:20px;display:flex;flex-direction:column}
.tcc2-title{font-family:var(--f-display);font-size:1.3rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;margin-bottom:8px}
.tcc2-desc{font-size:.84rem;color:var(--c-500);margin-bottom:20px}
.tcc2-form{display:flex;flex-direction:column;gap:10px;margin-top:auto}
.tcc2-input{width:100%;height:48px;border-radius:12px;border:1.5px solid var(--border-mid);padding:0 16px;font-family:var(--f-body);font-size:.88rem;background:var(--c-white);outline:none;transition:border-color .2s}
.tcc2-input:focus{border-color:var(--c-green);box-shadow:0 0 0 3px rgba(22,163,74,.12)}
.tcc2-btn{height:48px;border-radius:12px;border:none;background:var(--c-black);color:var(--c-white);font-family:var(--f-body);font-size:.88rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;gap:7px;transition:all .2s}
.tcc2-btn:hover{background:var(--c-800);transform:translateY(-1px);box-shadow:var(--shadow-md)}

.chart-section{padding:var(--section-v) 0;background:var(--c-50);border-top:1px solid var(--border)}
.chart-head-row{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:32px;gap:32px}
.cab-val{font-family:var(--f-display);font-size:2.4rem;font-weight:300;color:var(--c-black);letter-spacing:-.04em;line-height:1}
.cab-val span{font-size:.5em;color:var(--c-400)}
.cab-lbl{font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-top:4px}
.chart-card{display:grid;grid-template-columns:1fr 280px;gap:24px;padding:28px;background:var(--c-white);border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow-sm)}
.chart-bars-wrap{display:grid;grid-template-columns:repeat(7,1fr);gap:10px;align-items:end;min-height:200px}
.cbar-col{display:flex;flex-direction:column;align-items:center;gap:6px;border:none;background:transparent;padding:0;cursor:pointer;transition:transform .18s}
.cbar-col:hover{transform:translateY(-3px)}
.cbar-col.active .cbar-track{box-shadow:0 0 0 2px rgba(22,163,74,.25)}
.cbar-val{font-family:var(--f-mono);font-size:.68rem;font-weight:700;color:var(--c-400)}
.cbar-col.active .cbar-val{color:var(--c-green)}
.cbar-track{width:100%;height:140px;border-radius:8px;background:rgba(0,0,0,.06);overflow:hidden;display:flex;align-items:flex-end}
.cbar-fill{width:100%;border-radius:8px;background:linear-gradient(180deg,#86efac,#16a34a);transition:height .4s ease}
.cbar-lbl{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--c-300)}
.chart-detail{padding:22px;background:var(--c-50);border-radius:16px;border:1px solid var(--border)}
.cd-eyebrow{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-400);margin-bottom:6px}
.cd-day{font-family:var(--f-display);font-size:1.2rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;margin-bottom:6px}
.cd-score{font-family:var(--f-display);font-size:2.4rem;font-weight:300;color:var(--c-green);letter-spacing:-.04em;line-height:1;margin-bottom:4px}
.cd-score span{font-size:.5em;color:var(--c-green)}
.cd-meta{font-size:.78rem;color:var(--c-400);margin-bottom:14px}
.cd-tasks{display:flex;flex-direction:column;gap:7px}
.cd-task{display:flex;align-items:flex-start;gap:8px;font-size:.8rem;color:var(--c-500)}
.cd-task-dot{width:6px;height:6px;border-radius:50%;background:var(--c-300);flex-shrink:0;margin-top:5px}
.cd-task.done{opacity:.5}
.cd-task.done .cd-task-dot{background:var(--c-green)}
.cd-empty{font-size:.8rem;color:var(--c-300);font-style:italic;margin:0}
.chart-section-title{font-size:clamp(1.8rem,3vw,2.8rem)}
.tracker-title{font-size:clamp(1.8rem,3vw,2.6rem)}


.why-section{padding:var(--section-v) 0;background:var(--c-900);border-top:1px solid rgba(255,255,255,.04)}
.why-inner{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center}
.why-h2{color:var(--c-white);margin-bottom:20px;font-size:clamp(2rem,3.8vw,3.6rem)}
.why-copy{color:rgba(255,255,255,.55);margin-bottom:32px;max-width:28rem}
.why-facts{display:flex;flex-direction:column;gap:14px}
.why-fact{padding:16px 18px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.07)}
.wf-label{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);margin-bottom:5px}
.wf-val{font-size:.86rem;font-weight:500;color:rgba(255,255,255,.65);line-height:1.5}
.why-stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.wsg-card{padding:28px 24px;border-radius:18px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);transition:all .25s}
.wsg-card:hover{background:rgba(255,255,255,.07);transform:translateY(-3px)}
.wsg-n{font-family:var(--f-display);font-size:clamp(2.2rem,3.5vw,3.2rem);font-weight:300;color:var(--c-white);letter-spacing:-.04em;line-height:1;margin-bottom:10px}
.wsg-l{font-size:.82rem;color:rgba(255,255,255,.45);line-height:1.5}


.footer{background:var(--c-black);padding:56px 0 0}
.footer-inner{max-width:1280px;margin:0 auto;padding:0 40px 44px;display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:48px;border-bottom:1px solid rgba(255,255,255,.07)}
.footer-col{display:flex;flex-direction:column;gap:10px}
.footer-col-head{font-family:var(--f-body);font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:rgba(255,255,255,.35);margin-bottom:4px}
.footer-col a{font-family:var(--f-body);font-size:.86rem;font-weight:500;color:rgba(255,255,255,.5);text-decoration:none;transition:color .18s}
.footer-col a:hover{color:rgba(255,255,255,.9)}
.footer-bottom{max-width:1280px;margin:0 auto;padding:18px 40px}
.footer-bottom p{font-size:.76rem;color:rgba(255,255,255,.2);margin:0}
.footer-logo{color:rgba(255,255,255,.88);margin-bottom:12px}
.footer-logo-icon{color:rgba(255,255,255,.8)}
.footer-blurb{font-size:.8rem;color:rgba(255,255,255,.3);line-height:1.6;margin:0}


@media(max-width:1100px){
  .roadmap-weeks{grid-template-columns:repeat(2,1fr)}
  .roadmap-detail{grid-template-columns:1fr}
  .section-head-row{grid-template-columns:1fr}
  .rdm-day-plan-grid{grid-template-columns:repeat(2,1fr)}
  .today-context-row{grid-template-columns:1fr}
  .why-inner{grid-template-columns:1fr}
  .footer-inner{grid-template-columns:1fr 1fr}
}
@media(max-width:900px){
  .dash-hero-inner{grid-template-columns:1fr}
  .tracker-grid{grid-template-columns:1fr}
  .chart-card{grid-template-columns:1fr}
  .why-stat-grid{grid-template-columns:1fr 1fr}
  .section-wrap,.header-inner,.dash-hero-inner{padding-left:24px;padding-right:24px}
  .tsc-slot{grid-template-columns:48px 20px 1fr}
}
@media(max-width:700px){
  .nav,.nav-link{display:none}
  .hero-kpi-row{flex-wrap:wrap}
  .hkpi{flex:0 0 50%}
  .hkpi-div{display:none}
  .roadmap-weeks{grid-template-columns:1fr}
  .rdm-day-plan-grid{grid-template-columns:1fr}
  .rdm-day-plan-head{flex-direction:column}
  .chart-bars-wrap{grid-template-columns:repeat(7,1fr);gap:5px}
  .cbar-track{height:100px}
  .why-stat-grid{grid-template-columns:1fr}
  .footer-inner{grid-template-columns:1fr}
  h2{font-size:clamp(1.9rem,7vw,2.6rem)}
  .tsc-slot{grid-template-columns:40px 18px 1fr;gap:0 8px}
  .tsc-time{font-size:.6rem}
}


.rdm-day-plan-grid {
  display: flex;
  gap: 14px;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 12px;
  scroll-snap-type: x mandatory;
  align-items: stretch;
}

.rdm-day-plan-grid::-webkit-scrollbar {
  height: 8px;
}

.rdm-day-plan-grid::-webkit-scrollbar-track {
  background: rgba(0,0,0,.05);
  border-radius: 999px;
}

.rdm-day-plan-grid::-webkit-scrollbar-thumb {
  background: rgba(22,163,74,.35);
  border-radius: 999px;
}

.rdm-day-plan-grid::-webkit-scrollbar-thumb:hover {
  background: rgba(22,163,74,.55);
}

.rdm-day-card {
  min-width: 230px;
  max-width: 250px;
  flex: 0 0 230px;
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
}

.rdm-day-card.today {
  border: 2px solid rgba(22,163,74,.42);
  background: linear-gradient(160deg,#f0fdf4,#ffffff);
  box-shadow: 0 10px 28px rgba(22,163,74,.12);
}

.rdm-day-card.today .rdm-day-name {
  color: var(--c-green);
}

.rdm-day-schedule {
  flex: 1;
}

.roadmap-detail {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(320px, .65fr);
  gap: 24px;
  align-items: stretch;
}

.roadmap-detail-main,
.roadmap-feedback-panel {
  min-width: 0;
  height: 100%;
}

.roadmap-feedback-panel {
  align-self: stretch;
}

.slot-text {
  font-size: .76rem;
  line-height: 1.45;
  color: var(--c-700);
  font-weight: 600;
}

.slot-time {
  font-family: var(--f-mono);
  font-size: .62rem;
  font-weight: 700;
  color: var(--c-400);
  white-space: nowrap;
}

@media(max-width:1100px){
  .roadmap-detail{grid-template-columns:1fr}
  .rdm-day-card{min-width:240px;flex-basis:240px}
}

@media(max-width:700px){
  .rdm-day-card{min-width:82vw;flex-basis:82vw;max-width:82vw}
}
</style>