<!--
  ParentRoadmapPage.vue

  Creates the HealthyKids 4-week planner page.

  Purpose:
  - Separates the 4-week planner from the parent dashboard.
  - Keeps the website journey flow visible at the top.
  - Shows Step 04 as the current active step.
  - Allows parents to view weekly roadmap progress.
  - Allows only today's planner actions to be completed or edited.

  API requirement:
  - Requires VITE_PARENT_PROFILES_API_BASE_URL.
  - Uses GET /{familyCode} to load the saved profile.
  - Uses PUT /{familyCode} to save planner progress and planner edits.

  Accessibility:
  - Uses aria-labels, aria-live, role="status", role="alert", and role="progressbar".
  - Uses aria-pressed for selected weeks and selected days.
  - Uses aria-disabled for locked planner controls.
  - Uses data-hover-read-text for hover-to-read support.
-->

<template>
    <div class="dashboard-page">
      <!-- Decorative dashboard background -->
  
    <div class="dashboard-page-bg" aria-hidden="true">
      <img
        class="dashboard-page-bg__img"
        src="https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=2400&q=90"
        alt=""
        aria-hidden="true"
      />
      <div class="dashboard-page-bg__overlay"></div>
      <div class="dashboard-page-bg__grain"></div>
    </div>

      <!-- LOADING STATE -->
      <div
        v-if="isPageLoading"
        class="dashboard-state-screen"
        role="status"
        aria-live="polite"
        data-hover-read-text="Loading your four week family plan."
      >
        <div class="dashboard-state-spinner" aria-hidden="true"></div>
        <p class="dashboard-state-msg">Loading your 4-week family plan...</p>
      </div>
  
      <!-- ERROR STATE -->
      <div
        v-else-if="displayError"
        class="dashboard-state-screen"
        role="alert"
        aria-live="assertive"
        :data-hover-read-text="`Could not load your four week plan. ${displayError}`"
      >
        <p class="dashboard-state-error">Could not load your 4-week plan: {{ displayError }}</p>
  
        <button
          class="dashboard-nav-btn"
          type="button"
          data-hover-read-text="Retry loading your four week plan"
          @click="loadDashboard(familyCode)"
        >
          Retry
        </button>
      </div>
  
      <!-- EMPTY STATE -->
      <div
        v-else-if="!isPlanReady"
        class="dashboard-state-screen"
        role="status"
        aria-live="polite"
        data-hover-read-text="No family plan found yet. Complete the quiz to create your four week plan."
      >
        <p class="dashboard-state-msg">No family plan found yet.</p>
  
        <RouterLink
          to="/parent-quiz"
          class="dashboard-nav-btn"
          data-hover-read-text="Complete the parent quiz"
        >
          Complete quiz
        </RouterLink>
      </div>
  
      <!-- MAIN ROADMAP PAGE -->
      <main
        v-else
        id="main-content"
        class="dashboard-main"
        aria-labelledby="roadmap-page-title"
      >
        <!-- WEBSITE JOURNEY BAR -->
        <FamilyJourneyBar :current-step="4" />
  
        <!-- ROADMAP CARD -->
        <section
          class="dashboard-content-card dashboard-content-card--wide dashboard-planner-tab"
          aria-labelledby="roadmap-page-title"
          aria-describedby="roadmap-page-description"
        >
          <!-- PAGE HEADER -->
          <div class="dashboard-content-header">
            <div class="dashboard-content-header-text">
              <div
                class="dashboard-content-eyebrow"
                data-hover-read-text="Step 04. Four week family roadmap."
              >
                <span class="dashboard-eyebrow-dot" aria-hidden="true"></span>
                Step 04 · 4-week plan
              </div>
  
              <h1
                id="roadmap-page-title"
                class="dashboard-content-title"
                data-hover-read-text="Your four week family roadmap"
              >
                Your 4-week family roadmap
              </h1>
  
              <p
                id="roadmap-page-description"
                class="dashboard-content-subtitle"
                data-hover-read-text="Review weekly focus areas, complete today's planner actions, and adjust today's steps when needed."
              >
                Review weekly focus areas, complete today's planner actions, and adjust today's steps when needed.
              </p>
            </div>
  
            <div
              class="dashboard-today-progress-ring"
              role="progressbar"
              :aria-valuenow="selectedRoadmapWeek.progress"
              aria-valuemin="0"
              aria-valuemax="100"
              :aria-label="`Selected week progress is ${selectedRoadmapWeek.progress} percent`"
              :data-hover-read-text="`Selected week progress is ${selectedRoadmapWeek.progress} percent`"
            >
              <svg aria-hidden="true" viewBox="0 0 64 64" width="64" height="64">
                <circle
                  cx="32"
                  cy="32"
                  r="26"
                  fill="none"
                  stroke="rgba(22,48,43,0.08)"
                  stroke-width="5"
                />
                <circle
                  cx="32"
                  cy="32"
                  r="26"
                  fill="none"
                  stroke="#13806f"
                  stroke-width="5"
                  stroke-linecap="round"
                  stroke-dasharray="163.4"
                  :stroke-dashoffset="163.4 - (163.4 * selectedRoadmapWeek.progress / 100)"
                  transform="rotate(-90 32 32)"
                  style="transition: stroke-dashoffset 0.6s ease"
                />
              </svg>
  
              <div class="dashboard-ring-inner">
                <strong>{{ selectedRoadmapWeek.progress }}%</strong>
              </div>
            </div>
          </div>
  
          <!-- QUICK SUMMARY -->
          <div class="dashboard-daily-summary-row">
            <div class="dashboard-daily-summary-card">
              <span>Family code</span>
              <strong>{{ familyCode }}</strong>
            </div>
  
            <div class="dashboard-daily-summary-card">
              <span>Current week</span>
              <strong>Week {{ currentWeek }} of 4</strong>
            </div>
  
            <div class="dashboard-daily-summary-card">
              <span>Selected day</span>
              <strong>{{ selectedPlannerDayData.day || todayName }}</strong>
            </div>
          </div>
  
          <!-- SYNC ERROR -->
          <p
            v-if="dashboardSaveError"
            class="dashboard-form-error"
            role="alert"
            aria-live="assertive"
            :data-hover-read-text="dashboardSaveError"
          >
            {{ dashboardSaveError }}
          </p>
  
          <!-- PLANNER CONTENT -->
          <div class="dashboard-planner-layout">
            <!-- WEEK LIST -->
            <aside class="dashboard-week-list" aria-label="Four week roadmap list">
              <div class="dashboard-week-list-head">
                <span>Weeks</span>
                <strong>{{ currentWeek }}/4 active</strong>
              </div>
  
              <button
                v-for="week in fourWeekRoadmap"
                :key="week.id"
                type="button"
                class="dashboard-week-pill"
                :class="{ 'dashboard-week-pill--active': week.id === activeRoadmapWeek }"
                :aria-pressed="week.id === activeRoadmapWeek ? 'true' : 'false'"
                :aria-label="getWeekReadableText(week)"
                :data-hover-read-text="getWeekReadableText(week)"
                @click="activeRoadmapWeek = week.id"
              >
                <span class="dashboard-week-badge">W{{ week.week }}</span>
  
                <span class="dashboard-week-pill-copy">
                  <strong>{{ week.title || week.focus || `Week ${week.week}` }}</strong>
                  <span>{{ week.progress }}% complete</span>
                </span>
  
                <span class="dashboard-week-pill-chevron" aria-hidden="true">›</span>
              </button>
            </aside>
  
            <!-- WEEK DETAIL -->
            <article class="dashboard-week-detail" aria-label="Selected week details">
              <div class="dashboard-week-detail-head">
                <div>
                  <span class="dashboard-week-kicker">Selected week</span>
  
                  <h2 class="dashboard-week-title">
                    Week {{ selectedRoadmapWeek.week }} · {{ selectedRoadmapWeek.title }}
                  </h2>
  
                  <p class="dashboard-week-desc">
                    {{
                      selectedRoadmapWeek.summary ||
                      selectedRoadmapWeek.detail ||
                      selectedRoadmapWeek.parentTip ||
                      'Focus on a small number of repeatable family actions this week.'
                    }}
                  </p>
                </div>
  
                <!-- EDIT CONTROLS -->
                <div class="dashboard-week-actions">
                  <button
                    v-if="!isEditingPlanner"
                    type="button"
                    class="dashboard-btn-edit"
                    :disabled="!canModifySelectedPlannerDay"
                    :aria-disabled="!canModifySelectedPlannerDay ? 'true' : 'false'"
                    :data-hover-read-text="canModifySelectedPlannerDay ? 'Edit todays planner actions' : 'Editing locked. Only today’s actions can be updated.'"
                    @click="startEditingPlanner"
                  >
                    {{ canModifySelectedPlannerDay ? 'Edit today' : 'Locked' }}
                  </button>
  
                  <template v-else>
                    <button
                      type="button"
                      class="dashboard-btn-cancel"
                      data-hover-read-text="Cancel editing planner actions"
                      @click="cancelEditingPlanner"
                    >
                      Cancel
                    </button>
  
                    <button
                      type="button"
                      class="dashboard-btn-save"
                      data-hover-read-text="Save planner changes"
                      @click="saveEditedPlanner"
                    >
                      Save changes
                    </button>
                  </template>
                </div>
              </div>
  
              <!-- WEEK STATS -->
              <div class="dashboard-week-stats" aria-label="Selected week progress summary">
                <div
                  class="dashboard-stat-card"
                  :data-hover-read-text="`Week progress is ${selectedRoadmapWeek.progress} percent`"
                >
                  <span class="dashboard-stat-label">Week progress</span>
                  <strong class="dashboard-stat-value">{{ selectedRoadmapWeek.progress }}%</strong>
  
                  <div class="dashboard-stat-track">
                    <div
                      class="dashboard-stat-fill"
                      :style="{ width: selectedRoadmapWeek.progress + '%' }"
                    ></div>
                  </div>
                </div>
  
                <div
                  class="dashboard-stat-card"
                  :data-hover-read-text="`${selectedRoadmapWeek.completed} of ${selectedRoadmapWeek.totalItems} actions completed`"
                >
                  <span class="dashboard-stat-label">Completed</span>
                  <strong class="dashboard-stat-value">{{ selectedRoadmapWeek.completed }}</strong>
                  <p class="dashboard-stat-sub">of {{ selectedRoadmapWeek.totalItems }} actions</p>
                </div>
  
                <div
                  class="dashboard-stat-card"
                  :data-hover-read-text="`${selectedWeekOpenItems} actions remaining`"
                >
                  <span class="dashboard-stat-label">Remaining</span>
                  <strong class="dashboard-stat-value">{{ selectedWeekOpenItems }}</strong>
                  <p class="dashboard-stat-sub">small steps left</p>
                </div>
              </div>
  
              <!-- DAY PICKER -->
              <div class="dashboard-day-picker" aria-label="Select a day in the selected week">
                <button
                  v-for="day in currentFirstRoadmapDailyPlan"
                  :key="day.day"
                  type="button"
                  class="dashboard-day-btn"
                  :aria-pressed="selectedPlannerDayData.day === day.day ? 'true' : 'false'"
                  :aria-label="getDayReadableText(day)"
                  :data-hover-read-text="getDayReadableText(day)"
                  :class="{
                    'dashboard-day-btn--active': selectedPlannerDayData.day === day.day,
                    'dashboard-day-btn--today': activeRoadmapWeek === currentWeek && day.day === todayName
                  }"
                  @click="selectedPlannerDay = day.day"
                >
                  <span class="dashboard-day-short">{{ getShortDayName(day.day) }}</span>
  
                  <strong class="dashboard-day-pct">{{ day.progress }}%</strong>
  
                  <div class="dashboard-day-track">
                    <div
                      class="dashboard-day-fill"
                      :style="{ width: day.progress + '%' }"
                    ></div>
                  </div>
  
                  <span
                    v-if="activeRoadmapWeek === currentWeek && day.day === todayName"
                    class="dashboard-day-today-tag"
                  >
                    Today
                  </span>
                </button>
              </div>
  
              <!-- DAILY PLANNER PANEL -->
              <div class="dashboard-daily-panel">
                <div class="dashboard-daily-panel-head">
                  <div>
                    <span class="dashboard-week-kicker">Daily view</span>
  
                    <h3 class="dashboard-daily-title">
                      {{ selectedPlannerDayData.day || todayName }}
                    </h3>
  
                    <p class="dashboard-daily-sub">
                      {{ selectedPlannerDayData.completed || 0 }}
                      of
                      {{ selectedPlannerDayData.timeSlots?.length || 0 }}
                      actions completed
                    </p>
                  </div>
  
                  <div
                    class="dashboard-daily-score"
                    :data-hover-read-text="`${selectedPlannerDayData.progress || 0} percent complete for ${selectedPlannerDayData.day || todayName}`"
                  >
                    {{ selectedPlannerDayData.progress || 0 }}%
                  </div>
                </div>
  
                <div class="dashboard-daily-slots">
                  <div
                    v-for="slot in selectedPlannerDayData.timeSlots || []"
                    :key="slot.id"
                    class="dashboard-daily-slot"
                    :data-hover-read-text="getSlotReadableText(slot)"
                    :class="[
                      'dashboard-cat-' + slot.category,
                      {
                        'dashboard-daily-slot--done': slot.done,
                        'dashboard-daily-slot--editing': isEditingPlanner
                      }
                    ]"
                  >
                    <!-- READ-ONLY CHECKLIST MODE -->
                    <template v-if="!isEditingPlanner">
                      <span class="dashboard-slot-time">{{ slot.time }}</span>
  
                      <label
                        class="dashboard-slot-action"
                        :class="{ 'dashboard-slot-action--locked': !canModifySelectedPlannerDay }"
                      >
                        <input
                          type="checkbox"
                          :checked="slot.done"
                          :disabled="!canModifySelectedPlannerDay"
                          :aria-label="`${slot.done ? 'Mark incomplete' : 'Mark complete'}: ${slot.text}`"
                          :aria-disabled="!canModifySelectedPlannerDay ? 'true' : 'false'"
                          @change="toggleRoadmapDailyAction(slot.id)"
                        />
  
                        <span
                          class="dashboard-slot-checkbox"
                          :class="{ 'dashboard-slot-checkbox--checked': slot.done }"
                          aria-hidden="true"
                        >
                          <svg v-if="slot.done" width="8" height="8" viewBox="0 0 10 10">
                            <path
                              d="M2 5l2.5 2.5L8 3"
                              stroke="white"
                              stroke-width="1.7"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              fill="none"
                            />
                          </svg>
                        </span>
  
                        <div class="dashboard-slot-body">
                          <strong class="dashboard-slot-title">{{ slot.text }}</strong>
  
                          <span v-if="slot.tip || slot.detail" class="dashboard-slot-tip">
                            {{ slot.tip || slot.detail }}
                          </span>
  
                          <span v-if="!canModifySelectedPlannerDay" class="dashboard-slot-locked-note">
                            Only today's actions can be updated.
                          </span>
                        </div>
                      </label>
                    </template>
  
                    <!-- EDIT MODE -->
                    <template v-else-if="canModifySelectedPlannerDay">
                      <div class="dashboard-slot-edit">
                        <div class="dashboard-slot-edit-row">
                          <input
                            v-model="editablePlanner[slot.id].time"
                            class="dashboard-edit-input"
                            type="text"
                            placeholder="Time"
                            aria-label="Edit action time"
                            data-hover-read-text="Edit action time"
                          />
  
                          <select
                            v-model="editablePlanner[slot.id].category"
                            class="dashboard-edit-input"
                            aria-label="Edit action category"
                            data-hover-read-text="Edit action category"
                          >
                            <option value="nutrition">Nutrition</option>
                            <option value="movement">Movement</option>
                            <option value="sleep">Sleep</option>
                            <option value="routine">Routine</option>
                            <option value="family">Family</option>
                          </select>
                        </div>
  
                        <input
                          v-model="editablePlanner[slot.id].text"
                          class="dashboard-edit-input"
                          type="text"
                          placeholder="Habit action"
                          aria-label="Edit habit action"
                          data-hover-read-text="Edit habit action"
                        />
  
                        <input
                          v-model="editablePlanner[slot.id].tip"
                          class="dashboard-edit-input"
                          type="text"
                          placeholder="Parent tip optional"
                          aria-label="Edit parent tip optional"
                          data-hover-read-text="Edit parent tip optional"
                        />
                      </div>
                    </template>
  
                    <!-- LOCKED VIEW -->
                    <template v-else>
                      <span class="dashboard-slot-time">{{ slot.time }}</span>
  
                      <div class="dashboard-slot-action dashboard-slot-action--locked">
                        <span
                          class="dashboard-slot-checkbox"
                          :class="{ 'dashboard-slot-checkbox--checked': slot.done }"
                          aria-hidden="true"
                        >
                          <svg v-if="slot.done" width="8" height="8" viewBox="0 0 10 10">
                            <path
                              d="M2 5l2.5 2.5L8 3"
                              stroke="white"
                              stroke-width="1.7"
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              fill="none"
                            />
                          </svg>
                        </span>
  
                        <div class="dashboard-slot-body">
                          <strong class="dashboard-slot-title">{{ slot.text }}</strong>
  
                          <span v-if="slot.tip || slot.detail" class="dashboard-slot-tip">
                            {{ slot.tip || slot.detail }}
                          </span>
  
                          <span class="dashboard-slot-locked-note">
                            Only today's actions can be updated.
                          </span>
                        </div>
                      </div>
                    </template>
                  </div>
  
                  <p
                    v-if="!(selectedPlannerDayData.timeSlots || []).length"
                    class="dashboard-empty-state"
                  >
                    No actions scheduled for this day.
                  </p>
                </div>
              </div>
            </article>
          </div>
  
          <!-- NEXT STEP CARD -->
          <div class="dashboard-next-step-card dashboard-next-step-card--split">
            <RouterLink
              to="/parent-dashboard"
              class="dashboard-next-step-btn dashboard-next-step-btn--previous"
              aria-label="Go back to today's plan page"
              data-hover-read-text="Previous step. Go back to today's plan."
            >
              <span aria-hidden="true">←</span>
              Previous step
            </RouterLink>

            <div class="dashboard-next-step-copy">
              <span>Step 04 of 05</span>
              <strong>Continue to nutrition support</strong>
              <p>Use the nutrition page to explore healthy meal and recipe ideas for your family.</p>
            </div>

            <RouterLink
              to="/parent-nutrition-tools"
              class="dashboard-next-step-btn"
              aria-label="Go to nutrition support"
              data-hover-read-text="Go to nutrition support"
            >
              Open nutrition
              <span aria-hidden="true">→</span>
            </RouterLink>
          </div>
  
          <!-- SCROLL TOP -->
          <button
            v-if="showPlannerBackTop"
            type="button"
            class="dashboard-scroll-top-btn"
            data-hover-read-text="Back to top"
            aria-label="Back to top"
            @click="scrollToTop"
          >
            <svg aria-hidden="true" width="13" height="13" viewBox="0 0 14 14" fill="none">
              <path
                d="M7 12V2M3 6l4-4 4 4"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>
        </section>
  
        <!-- FOOTER -->
        <footer
          class="dashboard-inner-footer"
          aria-label="Website footer"
        >
          <div
            class="dashboard-inner-footer-left"
            aria-label="Supporting families across Australia"
            data-hover-read-text
          >
            <span class="dashboard-inner-footer-live-dot" aria-hidden="true"></span>
            Supporting families across Australia
          </div>
  
          <div
            class="dashboard-inner-footer-right"
            aria-label="UN Sustainable Development Goal 3, Good Health and Wellbeing. Developed by Team SYRBYX."
            data-hover-read-text
          >
            <span>UN SDG 3 · Good Health &amp; Wellbeing</span>
            <span class="dashboard-home-footer-divider" aria-hidden="true">·</span>
            <span>Developed by Team SYRBYX</span>
          </div>
        </footer>
      </main>
    </div>
  </template>
  
  <script setup>
  import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
  import { RouterLink, useRoute } from 'vue-router'
  import { useFamilyPlanStore } from '../stores/familyPlanStore'
  import { useDynamicPlan } from '../composables/useDynamicPlan'
  import FamilyJourneyBar from '../components/FamilyJourneyBar.vue'
  
  // Shared family plan store and dynamic plan helpers.
  const { state, savePlan } = useFamilyPlanStore()
  const {
    loading: planLoading,
    error: planError,
    fetchPlan,
    buildRoadmapWeeks,
  } = useDynamicPlan()
  
  // Date, locale, and API configuration.
  const TIME_ZONE = 'Australia/Melbourne'
  const LOCALE = 'en-AU'
  const DAY_LABEL_LENGTH = 3
  const DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  const API_BASE_URL = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL
  const route = useRoute()
  
  // Page state.

  const isProfileLoading = ref(false)
  const profileLoadError = ref('')
  const isScrolled = ref(false)
  const activeDashboardTab = ref('today')
  const activeRoadmapWeek = ref(1)
  const selectedPlannerDay = ref(getTodayName())
  const isEditingPlanner = ref(false)
  const editablePlanner = ref({})
  const isSavingDashboard = ref(false)
  const dashboardSaveError = ref('')
  const showPlannerBackTop = ref(false)

  // Returns today's weekday name using the configured timezone.
  function getTodayName() {
    return new Date().toLocaleDateString(LOCALE, {
      weekday: 'long',
      timeZone: TIME_ZONE,
    })
  }
  
  // Returns a shortened day label such as Mon, Tue, or Wed.
  function getShortDayName(dayName = '') {
    return dayName.slice(0, DAY_LABEL_LENGTH)
  }
  
  // Safely returns an object, or an empty object when the value is invalid.
  function safeObject(value) {
    if (!value || Array.isArray(value) || typeof value !== 'object') return {}
    return value
  }
  
  // Converts internal category keys into user-facing labels.
  function getCategoryLabel(category) {
    return {
      nutrition: 'Nutrition',
      movement: 'Movement',
      sleep: 'Wind-down',
      routine: 'Routine',
      family: 'Family',
    }[category] || 'Routine'
  }
  
  // Normalises API profile fields so both camelCase and snake_case responses work.
  function normalizeDashboardProfile(profile = {}) {
    const progressItems = safeObject(profile.progressItems || profile.progress_items)
  
    return {
      ...profile,
  
      username: profile.username || state.username || '',
      userName: profile.username || state.userName || '',
      user_name: profile.username || state.user_name || '',
  
      childName: profile.childName ?? profile.child_name ?? state.childName,
      child_name: profile.childName ?? profile.child_name ?? state.child_name,
  
      parentName: profile.parentName ?? profile.parent_name ?? state.parentName,
      parent_name: profile.parentName ?? profile.parent_name ?? state.parent_name,
  
      dailyPlan: profile.dailyPlan ?? profile.daily_plan ?? state.dailyPlan ?? {},
  
      progressItems,
  
      roadmapProgress: safeObject(
        profile.roadmapProgress ||
        profile.roadmap_progress ||
        progressItems.roadmapProgress ||
        state.roadmapProgress
      ),
  
      todaySchedule: safeObject(
        profile.todaySchedule ||
        profile.today_schedule ||
        progressItems.todaySchedule ||
        state.todaySchedule
      ),
  
      plannerOverrides: safeObject(
        profile.plannerOverrides ||
        profile.planner_overrides ||
        progressItems.plannerOverrides ||
        state.plannerOverrides
      ),
  
      streakDays: profile.streakDays ?? profile.streak_days ?? state.streakDays ?? 0,
      streak_days: profile.streakDays ?? profile.streak_days ?? state.streak_days ?? 0,
  
      nextAction: profile.nextAction ?? profile.next_action ?? state.nextAction,
      next_action: profile.nextAction ?? profile.next_action ?? state.next_action,
  
      mission: profile.mission ?? state.mission,
    }
  }
  
  // Current family code from route, store, or localStorage.
  const familyCode = computed(() =>
    String(
      route.query.username ||
      route.params.username ||
      state.username ||
      state.userName ||
      state.user_name ||
      localStorage.getItem('hk-parent-username') ||
      ''
    ).trim()
  )
  
  // Today's weekday name.
  const todayName = computed(() => getTodayName())
  
  // Loading and error display.
  const isPageLoading = computed(() => planLoading.value || isProfileLoading.value)
  const displayError = computed(() => profileLoadError.value || planError.value || '')
  
  // Loads the saved parent profile from the parent profiles API.
  async function fetchParentProfile(username) {
    if (!username) throw new Error('Missing username')
    if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')
  
    const response = await fetch(`${API_BASE_URL}/${encodeURIComponent(username)}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
  
    const data = await response.json().catch(() => ({}))
  
    if (!response.ok) {
      throw new Error(data.error || `Profile load failed: ${response.status}`)
    }
  
    return data
  }
  
  // Loads the roadmap and profile for the selected family code.
  async function loadDashboard(username) {
    const cleanUsername = String(username || '').trim()
  
    if (!cleanUsername) {
      profileLoadError.value = 'Missing family code.'
      return
    }
  
    profileLoadError.value = ''
    isProfileLoading.value = true
  
    try {
      localStorage.setItem('hk-parent-username', cleanUsername)
  
      savePlan({
        ...state,
        username: cleanUsername,
        userName: cleanUsername,
        user_name: cleanUsername,
      })
  
      await fetchPlan(cleanUsername)
  
      const profile = await fetchParentProfile(cleanUsername)
      const normalizedProfile = normalizeDashboardProfile(profile)
  
      savePlan({
        ...state,
        ...normalizedProfile,
      })
  
      activeRoadmapWeek.value = currentWeek.value
      selectedPlannerDay.value = todayName.value
    } catch (error) {
      profileLoadError.value = error.message || 'Dashboard load failed.'
      console.error('Roadmap load failed:', error)
    } finally {
      isProfileLoading.value = false
    }
  }
  
  // Applies saved planner edits to a generated slot without changing the original slot shape.
  function applyPlannerOverridesToSlot(slot) {
    const overrides = safeObject(state.plannerOverrides)
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
  
  // Builds the 4-week roadmap and calculates day-level progress.
  const fourWeekRoadmap = computed(() => {
    const roadmapProgress = safeObject(state.roadmapProgress)
  
    return buildRoadmapWeeks(roadmapProgress).map((week) => ({
      ...week,
  
      dailyPlan: (week.dailyPlan || []).map((day) => {
        const timeSlots = (day.timeSlots || []).map(applyPlannerOverridesToSlot)
        const completed = timeSlots.filter((slot) => slot.done).length
        const progress = timeSlots.length ? Math.round((completed / timeSlots.length) * 100) : 0
  
        return {
          ...day,
          timeSlots,
          completed,
          progress,
        }
      }),
    }))
  })
  
  // Checks whether the roadmap has been generated.
  const isPlanReady = computed(() => fourWeekRoadmap.value.length > 0)
  
  // Fallback week used before roadmap data is available.
  const emptyRoadmapWeek = {
    id: 1,
    week: 1,
    title: 'Loading...',
    summary: '',
    detail: '',
    parentTip: '',
    actions: [],
    dailyPlan: [],
    dailyCompleted: 0,
    dailyTotal: 0,
    weeklyCompleted: 0,
    totalItems: 0,
    completed: 0,
    progress: 0,
    status: 'Not started',
    statusKey: 'not-started',
  }
  
  // Currently selected roadmap week.
  const selectedRoadmapWeek = computed(() =>
    fourWeekRoadmap.value.find((week) => week.id === activeRoadmapWeek.value) ||
    fourWeekRoadmap.value[0] ||
    emptyRoadmapWeek
  )
  
  // Finds the first incomplete week and treats it as the active/current week.
  const currentWeek = computed(() => {
    const firstIncompleteWeek = fourWeekRoadmap.value.find((week) => week.progress < 100)
    return firstIncompleteWeek?.week || fourWeekRoadmap.value[0]?.week || 1
  })
  
  // Sorts the selected week's daily plan in Monday-to-Sunday order.
  const currentFirstRoadmapDailyPlan = computed(() => {
    const plan = selectedRoadmapWeek.value?.dailyPlan || []
  
    return [...plan].sort((a, b) => {
      const aIndex = DAY_ORDER.indexOf(a.day)
      const bIndex = DAY_ORDER.indexOf(b.day)
  
      return (aIndex === -1 ? 99 : aIndex) - (bIndex === -1 ? 99 : bIndex)
    })
  })
  
  // Gets the selected planner day, falling back to today, Monday, or the first available day.
  const selectedPlannerDayData = computed(() => {
    const plan = selectedRoadmapWeek.value?.dailyPlan || []
    const selectedDay = plan.find((day) => day.day === selectedPlannerDay.value)
    const monday = plan.find((day) => day.day === 'Monday')
  
    const today =
      activeRoadmapWeek.value === currentWeek.value
        ? plan.find((day) => day.day === todayName.value)
        : null
  
    return (
      selectedDay ||
      today ||
      monday ||
      plan[0] || {
        day: activeRoadmapWeek.value === currentWeek.value ? todayName.value : 'Monday',
        timeSlots: [],
        completed: 0,
        progress: 0,
      }
    )
  })
  
  // Number of unfinished actions in the selected week.
  const selectedWeekOpenItems = computed(() =>
    Math.max(
      0,
      (selectedRoadmapWeek.value?.totalItems || 0) - (selectedRoadmapWeek.value?.completed || 0)
    )
  )
  
  // Checks whether the selected planner day is today.
  const isSelectedPlannerDayToday = computed(() =>
    activeRoadmapWeek.value === currentWeek.value &&
    selectedPlannerDayData.value?.day === todayName.value
  )
  
  // Only today's planner actions can be edited or toggled.
  const canModifySelectedPlannerDay = computed(() => isSelectedPlannerDayToday.value)
  
  // Builds readable text for hover-to-read and assistive features.
  function getSlotReadableText(slot) {
    const status = slot.done ? 'Completed' : 'Not completed'
    const category = getCategoryLabel(slot.category)
    const detail = slot.detail || slot.tip || ''
  
    return `${status}. ${slot.time}. ${category}. ${slot.text}. ${detail}`
  }
  
  // Builds readable summary text for a roadmap week.
  function getWeekReadableText(week) {
    return `Week ${week.week}. ${week.title || week.focus || `Week ${week.week}`}. ${week.progress} percent complete.`
  }
  
  // Builds readable summary text for a roadmap day.
  function getDayReadableText(day) {
    const todayText =
      activeRoadmapWeek.value === currentWeek.value && day.day === todayName.value
        ? 'Today. '
        : ''
  
    return `${todayText}${day.day}. ${day.progress} percent complete.`
  }
  
  // Converts different slot ID formats into one canonical action ID.
  function getCanonicalActionId(slotOrId) {
    if (slotOrId === null || slotOrId === undefined) return ''
  
    if (typeof slotOrId === 'string' || typeof slotOrId === 'number') {
      return String(slotOrId).replace('today-schedule-', '')
    }
  
    return String(slotOrId.sourceSlotId || slotOrId.id || '').replace('today-schedule-', '')
  }
  
  // Combines progress, today schedule, and planner overrides into progressItems.
  function buildProgressItems(updatedState) {
    return {
      ...safeObject(updatedState.progressItems),
      roadmapProgress: safeObject(updatedState.roadmapProgress),
      todaySchedule: safeObject(updatedState.todaySchedule),
      plannerOverrides: safeObject(updatedState.plannerOverrides),
    }
  }
  
  // Toggles a roadmap action and persists the updated progress.
  function togglePlanAction(slotOrId) {
    const actionId = getCanonicalActionId(slotOrId)
  
    if (!actionId) return
  
    const currentRoadmapProgress = safeObject(state.roadmapProgress)
    const currentTodaySchedule = safeObject(state.todaySchedule)
    const nextDone = !currentRoadmapProgress[actionId]
  
    const updatedState = {
      ...state,
  
      roadmapProgress: {
        ...currentRoadmapProgress,
        [actionId]: nextDone,
      },
  
      todaySchedule: {
        ...currentTodaySchedule,
        [`today-schedule-${actionId}`]: nextDone,
      },
    }
  
    updatedState.progressItems = buildProgressItems(updatedState)
    saveAndPersist(updatedState)
  }
  
  // Toggles a roadmap action only when the selected planner day is today.
  function toggleRoadmapDailyAction(actionId) {
    if (!canModifySelectedPlannerDay.value) return
    togglePlanAction(actionId)
  }
  
  // Starts editing the selected planner day.
  function startEditingPlanner() {
    if (!canModifySelectedPlannerDay.value) return
  
    const editable = {}
  
    ;(selectedPlannerDayData.value.timeSlots || []).forEach((slot) => {
      editable[slot.id] = {
        time: slot.time,
        text: slot.text,
        tip: slot.tip || slot.detail || '',
        category: slot.category,
      }
    })
  
    editablePlanner.value = editable
    isEditingPlanner.value = true
  }
  
  // Cancels planner editing and clears temporary edits.
  function cancelEditingPlanner() {
    editablePlanner.value = {}
    isEditingPlanner.value = false
  }
  
  // Saves planner edits as overrides and persists them.
  function saveEditedPlanner() {
    const updatedState = {
      ...state,
  
      plannerOverrides: {
        ...safeObject(state.plannerOverrides),
        ...safeObject(editablePlanner.value),
      },
    }
  
    updatedState.progressItems = buildProgressItems(updatedState)
  
    saveAndPersist(updatedState)
  
    editablePlanner.value = {}
    isEditingPlanner.value = false
  }
  
  // Saves updates locally first, then syncs them to the backend.
  function saveAndPersist(updatedState) {
    dashboardSaveError.value = ''
    savePlan(updatedState)
  
    persistDashboardUpdate(updatedState).catch((error) => {
      dashboardSaveError.value = error.message || 'Roadmap sync failed.'
      console.error('Roadmap sync failed:', error)
    })
  }
  
  // Persists roadmap progress and planner updates to the parent profile API.
  async function persistDashboardUpdate(updatedState) {
    const username = updatedState.username || state.username || familyCode.value
  
    if (!username) throw new Error('Missing username')
    if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')
  
    const roadmapProgress = safeObject(updatedState.roadmapProgress)
    const todaySchedule = safeObject(updatedState.todaySchedule)
    const plannerOverrides = safeObject(updatedState.plannerOverrides)
  
    const progressItems = {
      ...safeObject(updatedState.progressItems),
      roadmapProgress,
      todaySchedule,
      plannerOverrides,
    }
  
    const payload = {
      dailyPlan: updatedState.dailyPlan ?? state.dailyPlan ?? {},
      progressItems,
      roadmapProgress,
      todaySchedule,
      plannerOverrides,
      streakDays: updatedState.streakDays ?? state.streakDays ?? 0,
      nextAction: updatedState.nextAction ?? state.nextAction,
      mission: updatedState.mission ?? state.mission,
    }
  
    isSavingDashboard.value = true
  
    try {
      const response = await fetch(`${API_BASE_URL}/${encodeURIComponent(username)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
  
      const data = await response.json().catch(() => ({}))
  
      if (!response.ok) {
        throw new Error(data.error || `Update failed: ${response.status}`)
      }
  
      const normalizedResponse = normalizeDashboardProfile({
        ...updatedState,
        ...data,
      })
  
      savePlan({
        ...state,
        ...normalizedResponse,
      })
  
      return data
    } finally {
      isSavingDashboard.value = false
    }
  }
  
  // Tracks page scroll for header styling and back-to-top visibility.
  function onScroll() {
    isScrolled.value = window.scrollY > 40
    showPlannerBackTop.value = window.scrollY > 120
  }
  
  // Smoothly scrolls the page to the top.
  function scrollToTop() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  }
  
  // Keeps the active roadmap week aligned with the current incomplete week.
  watch(
    currentWeek,
    (nextWeek, previousWeek) => {
      const weekStillExists = fourWeekRoadmap.value.some(
        (week) => week.id === activeRoadmapWeek.value
      )
  
      if (activeRoadmapWeek.value === previousWeek || !weekStillExists) {
        activeRoadmapWeek.value = nextWeek
      }
    },
    { immediate: true }
  )
  
  // Resets the selected planner day when the active roadmap week changes.
  watch(activeRoadmapWeek, (weekId) => {
    selectedPlannerDay.value = weekId === currentWeek.value ? todayName.value : 'Monday'
  })
  
  // Sets up scroll tracking and loads the roadmap.
  onMounted(() => {
    window.addEventListener('scroll', onScroll, { passive: true })
  
    const username = familyCode.value
  
    if (username) {
      loadDashboard(username)
    } else {
      profileLoadError.value = 'Missing family code.'
    }
  })
  
  // Cleans up scroll tracking when leaving the page.
  onUnmounted(() => {
    window.removeEventListener('scroll', onScroll)
  })
  </script>