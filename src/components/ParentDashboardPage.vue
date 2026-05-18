<template>
  <div class="dashboard-page">
    <div class="dashboard-page-bg" aria-hidden="true">
      <div class="dashboard-bg-orb dashboard-bg-orb-1"></div>
      <div class="dashboard-bg-orb dashboard-bg-orb-2"></div>
      <div class="dashboard-bg-orb dashboard-bg-orb-3"></div>
      <div class="dashboard-grain"></div>
    </div>

    <!-- HEADER -->
    <header
      class="dashboard-header"
      :class="{ 'dashboard-header--scrolled': isScrolled }"
      aria-label="HealthyKids dashboard header"
    >
      <div class="dashboard-header-inner">
        <RouterLink
          to="/"
          class="dashboard-logo"
          aria-label="Go to HealthyKids home page"
          data-hover-read-text="Go to HealthyKids home page"
        >
          <div class="dashboard-logo-icon" aria-hidden="true">
            <svg viewBox="0 0 36 36" fill="none">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.5" />
              <path
                d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z"
                fill="currentColor"
              />
            </svg>
          </div>
          <span>HealthyKids</span>
        </RouterLink>

        <nav class="dashboard-nav" aria-label="Dashboard page navigation">
          <RouterLink to="/" class="dashboard-nav-a" data-hover-read-text="Go to home page">
            Home
          </RouterLink>

          <RouterLink
            to="/parent-dashboard"
            class="dashboard-nav-a"
            aria-current="page"
            data-hover-read-text="Current page. Dashboard."
          >
            Dashboard
          </RouterLink>

          <RouterLink
            to="/parent-nutrition-tools"
            class="dashboard-nav-a"
            data-hover-read-text="Go to nutrition page"
          >
            Nutrition
          </RouterLink>

          <RouterLink
            to="/statistics"
            class="dashboard-nav-a"
            data-hover-read-text="Go to statistics page"
          >
            Statistics
          </RouterLink>

          <RouterLink
            to="/young-person-dashboard"
            class="dashboard-nav-a"
            data-hover-read-text="Go to kids view"
          >
            Kids view
          </RouterLink>
        </nav>

        <div class="dashboard-nav-cta">
          <RouterLink
            to="/parent-quiz"
            class="dashboard-nav-link"
            data-hover-read-text="Retake the parent quiz"
          >
            Retake quiz
          </RouterLink>

          <RouterLink
            to="/parent-quiz"
            class="dashboard-nav-btn"
            data-hover-read-text="Create a new family plan"
          >
            <span style="color:white">New Plan</span>
            <svg aria-hidden="true" width="11" height="11" viewBox="0 0 12 12">
              <path
                d="M2 6h8M7 3l3 3-3 3"
                stroke="currentColor"
                stroke-width="1.4"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </RouterLink>
        </div>
      </div>
    </header>

    <!-- LOADING / ERROR STATES -->
    <div
      v-if="planLoading"
      class="dashboard-state-screen"
      role="status"
      aria-live="polite"
      data-hover-read-text="Loading your personalised family plan."
    >
      <div class="dashboard-state-spinner" aria-hidden="true"></div>
      <p class="dashboard-state-msg">Loading your personalised family plan...</p>
    </div>

    <div
      v-else-if="planError"
      class="dashboard-state-screen"
      role="alert"
      aria-live="assertive"
      :data-hover-read-text="`Could not load your family plan. ${planError}`"
    >
      <p class="dashboard-state-error">Could not load your family plan: {{ planError }}</p>
      <button
        class="dashboard-nav-btn"
        type="button"
        data-hover-read-text="Retry loading your family plan"
        @click="fetchPlan(state.username)"
      >
        Retry
      </button>
    </div>

    <div
      v-else-if="!isPlanReady"
      class="dashboard-state-screen"
      role="status"
      aria-live="polite"
      data-hover-read-text="No family plan found yet. Complete the quiz to create your plan."
    >
      <p class="dashboard-state-msg">No family plan found yet.</p>
      <RouterLink to="/parent-quiz" class="dashboard-nav-btn">Complete quiz</RouterLink>
    </div>

    <main
      v-else
      id="main-content"
      class="dashboard-main"
      aria-labelledby="dashboard-page-title"
    >
      <div class="dashboard-layout">
        <!-- SIDEBAR -->
        <aside class="dashboard-sidebar" aria-label="Dashboard sidebar">
          <div class="dashboard-sidebar-welcome">
            <p class="dashboard-sidebar-greeting">Welcome back,</p>
            <h1
              id="dashboard-page-title"
              class="dashboard-sidebar-name"
              :data-hover-read-text="`Welcome back, ${parentDisplayName}`"
            >
              {{ parentDisplayName }}
            </h1>
            <div class="dashboard-sidebar-accent"></div>
          </div>

          <div
            class="dashboard-sidebar-date-badge"
            :data-hover-read-text="`Today is ${selectedDateLabel}`"
          >
            <svg aria-hidden="true" width="13" height="13" viewBox="0 0 14 14" fill="none">
              <rect x="1" y="2" width="12" height="11" rx="2" stroke="currentColor" stroke-width="1.2"/>
              <path d="M1 5h12" stroke="currentColor" stroke-width="1.2"/>
              <circle cx="4.5" cy="8.5" r="1" fill="currentColor"/>
              <circle cx="7" cy="8.5" r="1" fill="currentColor"/>
            </svg>
            {{ selectedDateLabel }}
          </div>

          <nav class="dashboard-sidebar-nav" aria-label="Dashboard sections">
            <button
              v-for="tab in sidebarTabs"
              :key="tab.key"
              type="button"
              class="dashboard-sidebar-tab"
              :class="{ 'dashboard-sidebar-tab--active': activeDashboardTab === tab.key }"
              :aria-pressed="activeDashboardTab === tab.key ? 'true' : 'false'"
              :aria-label="`${tab.label}${activeDashboardTab === tab.key ? ', selected' : ''}`"
              :data-hover-read-text="`${tab.label}${activeDashboardTab === tab.key ? ', selected' : ''}`"
              @click="activeDashboardTab = tab.key"
            >
              <span class="dashboard-sidebar-tab-icon" aria-hidden="true" v-html="tab.icon"></span>
              <span class="dashboard-sidebar-tab-label">{{ tab.label }}</span>
              <span
                v-if="activeDashboardTab === tab.key"
                class="dashboard-sidebar-tab-pip"
                aria-hidden="true"
              ></span>
            </button>
          </nav>

          <div class="dashboard-sidebar-streak" v-if="streakDays > 0">
            <span class="dashboard-streak-flame">🔥</span>
            <div>
              <strong>{{ streakDays }}-day streak</strong>
              <small>Keep it going!</small>
            </div>
          </div>
        </aside>

        <!-- MAIN CONTENT -->
        <section
          class="dashboard-content-card"
          aria-labelledby="dashboard-section-title"
          aria-describedby="dashboard-section-description"
        >
          <!-- TAB HEADER -->
          <div class="dashboard-content-header">
            <div class="dashboard-content-header-text">
              <div
                class="dashboard-content-eyebrow"
                :data-hover-read-text="activeTabReadableTitle"
              >
                <span class="dashboard-eyebrow-dot" aria-hidden="true"></span>
                <template v-if="activeDashboardTab === 'today'">Daily view</template>
                <template v-else-if="activeDashboardTab === 'meal'">Nutrition</template>
                <template v-else-if="activeDashboardTab === 'activity'">Movement</template>
                <template v-else-if="activeDashboardTab === 'progress'">Roadmap</template>
                <template v-else>Account</template>
              </div>

              <h2
                id="dashboard-section-title"
                class="dashboard-content-title"
                :data-hover-read-text="activeTabReadableTitle"
              >
                <template v-if="activeDashboardTab === 'today'">Today's plan</template>
                <template v-else-if="activeDashboardTab === 'meal'">Meal plan</template>
                <template v-else-if="activeDashboardTab === 'activity'">Activity plan</template>
                <template v-else-if="activeDashboardTab === 'progress'">4-week planner</template>
                <template v-else>Settings</template>
              </h2>

              <p
                id="dashboard-section-description"
                class="dashboard-content-subtitle"
                :data-hover-read-text="activeTabReadableDescription"
              >
                <template v-if="activeDashboardTab === 'today'">Your child's personalised schedule for today.</template>
                <template v-else-if="activeDashboardTab === 'meal'">Nutrition-focused actions from today's family plan.</template>
                <template v-else-if="activeDashboardTab === 'activity'">Movement and activity actions for your family.</template>
                <template v-else-if="activeDashboardTab === 'progress'">Your family's 4-week roadmap progress.</template>
                <template v-else>Manage your dashboard and family plan.</template>
              </p>
            </div>

            <!-- TODAY PROGRESS RING -->
            <div
              v-if="activeDashboardTab === 'today'"
              class="dashboard-today-progress-ring"
              role="progressbar"
              :aria-valuenow="todayProgress"
              aria-valuemin="0"
              aria-valuemax="100"
              :aria-label="`Today's progress is ${todayProgress} percent`"
              :data-hover-read-text="`Today's progress is ${todayProgress} percent`"
            >
              <svg aria-hidden="true" viewBox="0 0 64 64" width="64" height="64">
                <circle cx="32" cy="32" r="26" fill="none" stroke="rgba(22,48,43,0.08)" stroke-width="5"/>
                <circle
                  cx="32" cy="32" r="26"
                  fill="none"
                  stroke="#13806f"
                  stroke-width="5"
                  stroke-linecap="round"
                  stroke-dasharray="163.4"
                  :stroke-dashoffset="163.4 - (163.4 * todayProgress / 100)"
                  transform="rotate(-90 32 32)"
                  style="transition: stroke-dashoffset 0.6s ease"
                />
              </svg>
              <div class="dashboard-ring-inner">
                <strong>{{ todayProgress }}%</strong>
              </div>
            </div>
          </div>
          
        
          <!-- TODAY TAB -->
          <div v-if="activeDashboardTab === 'today'" class="dashboard-slot-list">
            <!-- DAY AT A GLANCE TIMELINE -->
          <div
            class="dashboard-day-cycle-card"
            role="region"
            aria-label="Day at a glance timeline"
            :data-hover-read-text="`Day at a glance. ${completedTodayCount} complete and ${todayFullSchedule.length - completedTodayCount} remaining.`"
          >
            <div class="dashboard-day-cycle-header">
              <span class="dashboard-day-cycle-title">Day at a glance</span>
              <span class="dashboard-day-cycle-sub">
                {{ completedTodayCount }} complete · {{ todayFullSchedule.length - completedTodayCount }} remaining
              </span>
            </div>

            <div class="dashboard-day-cycle-track-wrap">
              <div class="dashboard-day-cycle-track">
                <!-- Time zones -->
                <div class="dashboard-day-cycle-zone dashboard-day-cycle-zone-morning" style="left: 0%; width: 18%;">
                  <span>Morning</span>
                </div>

                <div class="dashboard-day-cycle-zone dashboard-day-cycle-zone-afternoon" style="left: 18%; width: 40%;">
                  <span>Afternoon</span>
                </div>

                <div class="dashboard-day-cycle-zone dashboard-day-cycle-zone-evening" style="left: 58%; width: 27%;">
                  <span>Evening</span>
                </div>

                <div class="dashboard-day-cycle-zone dashboard-day-cycle-zone-night" style="left: 85%; width: 15%;">
                  <span>Night</span>
                </div>

                <!-- Current time progress -->
                <div
                  class="dashboard-day-cycle-progress"
                  :style="{ width: currentTimePercent + '%' }"
                  aria-hidden="true"
                ></div>

                <!-- Now marker -->
                <div
                  class="dashboard-day-cycle-now"
                  :style="{ left: currentTimePercent + '%' }"
                  aria-hidden="true"
                >
                  <div class="dashboard-day-cycle-now-line"></div>
                  <div class="dashboard-day-cycle-now-label">now</div>
                </div>

                <!-- Task nodes -->
                <button
                  v-for="slot in todayFullSchedule"
                  :key="slot.id"
                  type="button"
                  class="dashboard-day-cycle-node"
                  :class="[
                    'dashboard-day-cycle-node-' + slot.category,
                    {
                      'dashboard-day-cycle-node--done': slot.done,
                      'dashboard-day-cycle-node--upcoming': isUpcoming(slot)
                    }
                  ]"
                  :style="{ left: slotTimePercent(slot.time) + '%' }"
                  :aria-label="`${slot.time}. ${slot.text}. ${slot.done ? 'Completed' : 'Not completed'}`"
                  :data-hover-read-text="`${slot.time}. ${slot.text}. ${slot.done ? 'Completed' : 'Not completed'}`"
                  @click="toggleTodayScheduleSlot(slot)"
                >
                  <span class="dashboard-day-cycle-node-icon" aria-hidden="true">
                    <svg v-if="slot.done" width="10" height="10" viewBox="0 0 10 10">
                      <path
                        d="M2 5l2.5 2.5L8 3"
                        stroke="white"
                        stroke-width="1.7"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        fill="none"
                      />
                    </svg>
                    <span v-else>{{ catInitial(slot.category) }}</span>
                  </span>

                  <span class="dashboard-day-cycle-tooltip" aria-hidden="true">
                    <strong>{{ slot.time }}</strong>
                    <span>{{ slot.text }}</span>
                  </span>
                </button>
              </div>

              <div class="dashboard-day-cycle-time-labels" aria-hidden="true">
                <span>6 am</span>
                <span>9 am</span>
                <span>12 pm</span>
                <span>3 pm</span>
                <span>6 pm</span>
                <span>9 pm</span>
              </div>
            </div>

            <div class="dashboard-day-cycle-legend" aria-label="Timeline category legend">
              <div
                v-for="cat in scheduleCategories"
                :key="cat.key"
                class="dashboard-day-cycle-legend-item"
                :class="'dashboard-day-cycle-legend-' + cat.key"
              >
                <span aria-hidden="true"></span>
                {{ cat.label }}
              </div>
            </div>
          </div>
            <label
              v-for="slot in todayFullSchedule"
              :key="slot.id"
              class="dashboard-slot-row"
              :class="['dashboard-cat-' + slot.category, { 'dashboard-slot-row--done': slot.done }]"
              :data-hover-read-text="getSlotReadableText(slot)"
            >
              <div class="dashboard-slot-time-col">
                <span class="dashboard-slot-time">{{ slot.time }}</span>
                <span class="dashboard-slot-cat-badge">{{ getCategoryLabel(slot.category) }}</span>
              </div>

              <input
                type="checkbox"
                :checked="slot.done"
                :aria-label="`${slot.done ? 'Mark incomplete' : 'Mark complete'}: ${slot.text}`"
                @change="toggleTodayScheduleSlot(slot)"
              />

              <span
                class="dashboard-slot-checkbox"
                :class="{ 'dashboard-slot-checkbox--checked': slot.done }"
                aria-hidden="true"
              >
                <svg v-if="slot.done" width="10" height="10" viewBox="0 0 10 10">
                  <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                </svg>
              </span>

              <div class="dashboard-slot-body">
                <strong class="dashboard-slot-title">{{ slot.text }}</strong>
                <span v-if="slot.detail || slot.tip" class="dashboard-slot-tip">{{ slot.detail || slot.tip }}</span>
              </div>
            </label>

            <p v-if="!todayFullSchedule.length" class="dashboard-empty-state">
              No actions scheduled for today.
            </p>
          </div>

          <!-- MEAL TAB -->
          <div v-else-if="activeDashboardTab === 'meal'" class="dashboard-slot-list">
            <label
              v-for="slot in todayFullSchedule.filter(s => s.category === 'nutrition')"
              :key="slot.id"
              class="dashboard-slot-row dashboard-cat-nutrition"
              :class="{ 'dashboard-slot-row--done': slot.done }"
              :data-hover-read-text="getSlotReadableText(slot)"
            >
              <div class="dashboard-slot-time-col">
                <span class="dashboard-slot-time">{{ slot.time }}</span>
                <span class="dashboard-slot-cat-badge">Nutrition</span>
              </div>

              <input
                type="checkbox"
                :checked="slot.done"
                :aria-label="`${slot.done ? 'Mark incomplete' : 'Mark complete'}: ${slot.text}`"
                @change="toggleTodayScheduleSlot(slot)"
              />

              <span
                class="dashboard-slot-checkbox"
                :class="{ 'dashboard-slot-checkbox--checked': slot.done }"
                aria-hidden="true"
              >
                <svg v-if="slot.done" width="10" height="10" viewBox="0 0 10 10">
                  <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                </svg>
              </span>

              <div class="dashboard-slot-body">
                <strong class="dashboard-slot-title">{{ slot.text }}</strong>
                <span v-if="slot.detail || slot.tip" class="dashboard-slot-tip">{{ slot.detail || slot.tip }}</span>
              </div>
            </label>

            <p
              v-if="!todayFullSchedule.filter(s => s.category === 'nutrition').length"
              class="dashboard-empty-state"
            >
              No meal actions scheduled for today.
            </p>
          </div>

          <!-- ACTIVITY TAB -->
          <div v-else-if="activeDashboardTab === 'activity'" class="dashboard-slot-list">
            <label
              v-for="slot in todayFullSchedule.filter(s => s.category === 'movement')"
              :key="slot.id"
              class="dashboard-slot-row dashboard-cat-movement"
              :class="{ 'dashboard-slot-row--done': slot.done }"
              :data-hover-read-text="getSlotReadableText(slot)"
            >
              <div class="dashboard-slot-time-col">
                <span class="dashboard-slot-time">{{ slot.time }}</span>
                <span class="dashboard-slot-cat-badge">Movement</span>
              </div>

              <input
                type="checkbox"
                :checked="slot.done"
                :aria-label="`${slot.done ? 'Mark incomplete' : 'Mark complete'}: ${slot.text}`"
                @change="toggleTodayScheduleSlot(slot)"
              />

              <span
                class="dashboard-slot-checkbox"
                :class="{ 'dashboard-slot-checkbox--checked': slot.done }"
                aria-hidden="true"
              >
                <svg v-if="slot.done" width="10" height="10" viewBox="0 0 10 10">
                  <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                </svg>
              </span>

              <div class="dashboard-slot-body">
                <strong class="dashboard-slot-title">{{ slot.text }}</strong>
                <span v-if="slot.detail || slot.tip" class="dashboard-slot-tip">{{ slot.detail || slot.tip }}</span>
              </div>
            </label>

            <p
              v-if="!todayFullSchedule.filter(s => s.category === 'movement').length"
              class="dashboard-empty-state"
            >
              No activity actions scheduled for today.
            </p>
          </div>

          <!-- 4-WEEK PLANNER TAB -->
          <div v-else-if="activeDashboardTab === 'progress'" class="dashboard-planner-tab">
            <div class="dashboard-planner-layout">
              <!-- WEEK LIST -->
              <aside class="dashboard-week-list">
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
              <article class="dashboard-week-detail">
                <div class="dashboard-week-detail-head">
                  <div>
                    <span class="dashboard-week-kicker">Selected week</span>
                    <h3 class="dashboard-week-title">
                      Week {{ selectedRoadmapWeek.week }} · {{ selectedRoadmapWeek.title }}
                    </h3>
                    <p class="dashboard-week-desc">
                      {{ selectedRoadmapWeek.summary || selectedRoadmapWeek.detail || selectedRoadmapWeek.parentTip || 'Focus on a small number of repeatable family actions this week.' }}
                    </p>
                  </div>

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

                <!-- STATS ROW -->
                <div class="dashboard-week-stats" aria-label="Selected week progress summary">
                  <div
                    class="dashboard-stat-card"
                    :data-hover-read-text="`Week progress is ${selectedRoadmapWeek.progress} percent`"
                  >
                    <span class="dashboard-stat-label">Week progress</span>
                    <strong class="dashboard-stat-value">{{ selectedRoadmapWeek.progress }}%</strong>
                    <div class="dashboard-stat-track">
                      <div class="dashboard-stat-fill" :style="{ width: selectedRoadmapWeek.progress + '%' }"></div>
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
                <div class="dashboard-day-picker">
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
                      <div class="dashboard-day-fill" :style="{ width: day.progress + '%' }"></div>
                    </div>
                    <span
                      v-if="activeRoadmapWeek === currentWeek && day.day === todayName"
                      class="dashboard-day-today-tag"
                    >
                      Today
                    </span>
                  </button>
                </div>

                <!-- DAILY VIEW -->
                <div class="dashboard-daily-panel">
                  <div class="dashboard-daily-panel-head">
                    <div>
                      <span class="dashboard-week-kicker">Daily view</span>
                      <h4 class="dashboard-daily-title">{{ selectedPlannerDayData.day || todayName }}</h4>
                      <p class="dashboard-daily-sub">
                        {{ selectedPlannerDayData.completed || 0 }} of {{ selectedPlannerDayData.timeSlots?.length || 0 }} actions completed
                      </p>
                    </div>
                    <div class="dashboard-daily-score">{{ selectedPlannerDayData.progress || 0 }}%</div>
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
                              <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                            </svg>
                          </span>

                          <div class="dashboard-slot-body">
                            <strong class="dashboard-slot-title">{{ slot.text }}</strong>
                            <span v-if="slot.tip || slot.detail" class="dashboard-slot-tip">{{ slot.tip || slot.detail }}</span>
                            <span v-if="!canModifySelectedPlannerDay" class="dashboard-slot-locked-note">
                              Only today's actions can be updated.
                            </span>
                          </div>
                        </label>
                      </template>

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

                      <template v-else>
                        <span class="dashboard-slot-time">{{ slot.time }}</span>

                        <div class="dashboard-slot-action dashboard-slot-action--locked">
                          <span
                            class="dashboard-slot-checkbox"
                            :class="{ 'dashboard-slot-checkbox--checked': slot.done }"
                            aria-hidden="true"
                          >
                            <svg v-if="slot.done" width="8" height="8" viewBox="0 0 10 10">
                              <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                            </svg>
                          </span>

                          <div class="dashboard-slot-body">
                            <strong class="dashboard-slot-title">{{ slot.text }}</strong>
                            <span v-if="slot.tip || slot.detail" class="dashboard-slot-tip">{{ slot.tip || slot.detail }}</span>
                            <span class="dashboard-slot-locked-note">Only today's actions can be updated.</span>
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
          </div>

          <!-- SETTINGS TAB -->
          <div v-else class="dashboard-settings-tab">
            <div class="dashboard-settings-block">
              <h3 class="dashboard-settings-block-title">Family code</h3>
              <p
                class="dashboard-settings-block-value"
                :data-hover-read-text="`Family code: ${familyCode}`"
              >
                {{ familyCode }}
              </p>
            </div>

            <RouterLink
              to="/parent-quiz"
              class="dashboard-settings-btn"
              data-hover-read-text="Retake the parent quiz"
            >
              Retake quiz <span aria-hidden="true">→</span>
            </RouterLink>
          </div>

          <!-- SCROLL TOP -->
          <button
            v-if="activeDashboardTab === 'progress' && showPlannerBackTop"
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
      </div>

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

const { state, savePlan } = useFamilyPlanStore()
const { loading: planLoading, error: planError, fetchPlan, buildRoadmapWeeks } = useDynamicPlan()

const TIME_ZONE = 'Australia/Melbourne'
const LOCALE = 'en-AU'
const DAY_LABEL_LENGTH = 3
const DAY_ORDER = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
const API_BASE_URL = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL
const route = useRoute()

const isScrolled = ref(false)
const activeRoadmapWeek = ref(1)
const selectedPlannerDay = ref(getTodayName())
const isEditingPlanner = ref(false)
const editablePlanner = ref({})
const isSavingDashboard = ref(false)
const dashboardSaveError = ref('')
const activeDashboardTab = ref('today')
const showPlannerBackTop = ref(false)

const scheduleCategories = [
  { key: 'nutrition', label: 'Nutrition' },
  { key: 'movement', label: 'Movement' },
  { key: 'sleep', label: 'Sleep / Wind-down' },
  { key: 'routine', label: 'Routine' },
  { key: 'family', label: 'Family time' },
]

const sidebarTabs = [
  {
    key: 'today',
    label: "Today's plan",
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="1" y="2" width="14" height="13" rx="2" stroke="currentColor" stroke-width="1.3"/><path d="M1 6h14" stroke="currentColor" stroke-width="1.3"/><circle cx="5" cy="10" r="1" fill="currentColor"/><circle cx="8" cy="10" r="1" fill="currentColor"/></svg>`
  },
  {
    key: 'meal',
    label: 'Meal plan',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 2a5 5 0 100 10A5 5 0 008 2z" stroke="currentColor" stroke-width="1.3"/><path d="M8 5v3l2 1" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>`
  },
  {
    key: 'activity',
    label: 'Activity plan',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M2 10l3-5 3 3 2-4 4 6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>`
  },
  {
    key: 'progress',
    label: '4-week planner',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><rect x="1" y="1" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.3"/><rect x="9" y="1" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.3"/><rect x="1" y="9" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.3"/><rect x="9" y="9" width="6" height="6" rx="1.5" stroke="currentColor" stroke-width="1.3"/></svg>`
  },
  {
    key: 'settings',
    label: 'Settings',
    icon: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="2.5" stroke="currentColor" stroke-width="1.3"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3.05 3.05l1.41 1.41M11.54 11.54l1.41 1.41M3.05 12.95l1.41-1.41M11.54 4.46l1.41-1.41" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>`
  },
]

function getTodayName() {
  return new Date().toLocaleDateString(LOCALE, { weekday: 'long', timeZone: TIME_ZONE })
}

function getShortDayName(dayName = '') {
  return dayName.slice(0, DAY_LABEL_LENGTH)
}

function safeObject(value) {
  if (!value || Array.isArray(value) || typeof value !== 'object') return {}
  return value
}

function getCategoryLabel(category) {
  return { nutrition: 'Nutrition', movement: 'Movement', sleep: 'Wind-down', routine: 'Routine', family: 'Family' }[category] || 'Routine'
}

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
    roadmapProgress: safeObject(profile.roadmapProgress || profile.roadmap_progress || progressItems.roadmapProgress || state.roadmapProgress),
    todaySchedule: safeObject(profile.todaySchedule || profile.today_schedule || progressItems.todaySchedule || state.todaySchedule),
    plannerOverrides: safeObject(profile.plannerOverrides || profile.planner_overrides || progressItems.plannerOverrides || state.plannerOverrides),
    streakDays: profile.streakDays ?? profile.streak_days ?? state.streakDays ?? 0,
    streak_days: profile.streakDays ?? profile.streak_days ?? state.streak_days ?? 0,
    nextAction: profile.nextAction ?? profile.next_action ?? state.nextAction,
    next_action: profile.nextAction ?? profile.next_action ?? state.next_action,
    mission: profile.mission ?? state.mission,
  }
}

async function fetchParentProfile(username) {
  if (!username) throw new Error('Missing username')
  if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')
  const response = await fetch(`${API_BASE_URL}/${encodeURIComponent(username)}`, { method: 'GET', headers: { 'Content-Type': 'application/json' } })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.error || `Profile load failed: ${response.status}`)
  return data
}

async function loadDashboard(username) {
  if (!username) return
  localStorage.setItem('hk-parent-username', username)
  savePlan({ ...state, username, userName: username, user_name: username })
  await fetchPlan(username)
  const profile = await fetchParentProfile(username)
  const normalizedProfile = normalizeDashboardProfile(profile)
  savePlan({ ...state, ...normalizedProfile })
  activeRoadmapWeek.value = currentWeek.value
  selectedPlannerDay.value = todayName.value
}

function applyPlannerOverridesToSlot(slot) {
  const overrides = safeObject(state.plannerOverrides)
  const edited = overrides[slot.id]
  if (!edited) return slot
  const category = edited.category || slot.category
  return { ...slot, time: edited.time || slot.time, text: edited.text || slot.text, tip: edited.tip ?? slot.tip, category, categoryLabel: getCategoryLabel(category) }
}

const childName = computed(() => state.childName || state.child_name || 'Your child')
const streakDays = computed(() => state.streakDays || state.streak_days || 0)
const todayName = computed(() => getTodayName())

const fourWeekRoadmap = computed(() => {
  const roadmapProgress = safeObject(state.roadmapProgress)
  return buildRoadmapWeeks(roadmapProgress).map(week => ({
    ...week,
    dailyPlan: (week.dailyPlan || []).map(day => {
      const timeSlots = (day.timeSlots || []).map(applyPlannerOverridesToSlot)
      const completed = timeSlots.filter(slot => slot.done).length
      const progress = timeSlots.length ? Math.round((completed / timeSlots.length) * 100) : 0
      return { ...day, timeSlots, completed, progress }
    }),
  }))
})
function slotTimePercent(timeStr) {
  if (!timeStr) return 0

  const str = String(timeStr).toLowerCase().trim()
  let h = 0
  let m = 0

  const match = str.match(/^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$/i)

  if (match) {
    h = parseInt(match[1], 10) || 0
    m = parseInt(match[2] || '0', 10) || 0

    const period = match[3]

    if (period === 'pm' && h !== 12) h += 12
    if (period === 'am' && h === 12) h = 0
  } else {
    return 0
  }

  const totalMins = h * 60 + m
  const startMins = 6 * 60
  const endMins = 21 * 60

  return Math.min(
    100,
    Math.max(0, ((totalMins - startMins) / (endMins - startMins)) * 100)
  )
}

const nowTick = ref(Date.now())
let nowTimer = null

const currentTimePercent = computed(() => {
  nowTick.value

  const now = new Date()
  const totalMins = now.getHours() * 60 + now.getMinutes()
  const startMins = 6 * 60
  const endMins = 21 * 60

  return Math.min(
    100,
    Math.max(0, ((totalMins - startMins) / (endMins - startMins)) * 100)
  )
})

function isUpcoming(slot) {
  return !slot.done && slotTimePercent(slot.time) >= currentTimePercent.value - 4
}

function catInitial(category) {
  return {
    nutrition: 'N',
    movement: 'M',
    sleep: 'S',
    routine: 'R',
    family: 'F',
  }[category] || '·'
}


const isPlanReady = computed(() => fourWeekRoadmap.value.length > 0)

const emptyRoadmapWeek = { id: 1, week: 1, title: 'Loading...', summary: '', detail: '', parentTip: '', actions: [], dailyPlan: [], dailyCompleted: 0, dailyTotal: 0, weeklyCompleted: 0, totalItems: 0, completed: 0, progress: 0, status: 'Not started', statusKey: 'not-started' }

const selectedRoadmapWeek = computed(() =>
  fourWeekRoadmap.value.find(week => week.id === activeRoadmapWeek.value) || fourWeekRoadmap.value[0] || emptyRoadmapWeek
)

const currentWeek = computed(() => {
  const firstIncompleteWeek = fourWeekRoadmap.value.find(week => week.progress < 100)
  return firstIncompleteWeek?.week || fourWeekRoadmap.value[0]?.week || 1
})

const currentFirstRoadmapDailyPlan = computed(() => {
  const plan = selectedRoadmapWeek.value?.dailyPlan || []
  return [...plan].sort((a, b) => {
    const aIndex = DAY_ORDER.indexOf(a.day)
    const bIndex = DAY_ORDER.indexOf(b.day)
    return (aIndex === -1 ? 99 : aIndex) - (bIndex === -1 ? 99 : bIndex)
  })
})

const selectedPlannerDayData = computed(() => {
  const plan = selectedRoadmapWeek.value?.dailyPlan || []
  const selectedDay = plan.find(day => day.day === selectedPlannerDay.value)
  const monday = plan.find(day => day.day === 'Monday')
  const today = activeRoadmapWeek.value === currentWeek.value ? plan.find(day => day.day === todayName.value) : null
  return selectedDay || today || monday || plan[0] || { day: activeRoadmapWeek.value === currentWeek.value ? todayName.value : 'Monday', timeSlots: [], completed: 0, progress: 0 }
})

const selectedWeekOpenItems = computed(() => Math.max(0, (selectedRoadmapWeek.value?.totalItems || 0) - (selectedRoadmapWeek.value?.completed || 0)))

const isSelectedPlannerDayToday = computed(() =>
  activeRoadmapWeek.value === currentWeek.value && selectedPlannerDayData.value?.day === todayName.value
)

const canModifySelectedPlannerDay = computed(() => isSelectedPlannerDayToday.value)

const todayFullSchedule = computed(() => {
  const week = fourWeekRoadmap.value.find(item => item.week === currentWeek.value)
  const today = week?.dailyPlan?.find(day => day.day === todayName.value)
  return today?.timeSlots || []
})

const completedTodayCount = computed(() => todayFullSchedule.value.filter(slot => slot.done).length)

const todayProgress = computed(() =>
  todayFullSchedule.value.length ? Math.round((completedTodayCount.value / todayFullSchedule.value.length) * 100) : 0
)
const activeTabReadableTitle = computed(() => {
  if (activeDashboardTab.value === 'today') return "Today's plan"
  if (activeDashboardTab.value === 'meal') return 'Meal plan'
  if (activeDashboardTab.value === 'activity') return 'Activity plan'
  if (activeDashboardTab.value === 'progress') return '4-week planner'
  return 'Settings'
})

const activeTabReadableDescription = computed(() => {
  if (activeDashboardTab.value === 'today') return "Your child's personalised schedule for today."
  if (activeDashboardTab.value === 'meal') return "Nutrition-focused actions from today's family plan."
  if (activeDashboardTab.value === 'activity') return 'Movement and activity actions for your family.'
  if (activeDashboardTab.value === 'progress') return "Your family's 4-week roadmap progress."
  return 'Manage your dashboard and family plan.'
})

function getSlotReadableText(slot) {
  const status = slot.done ? 'Completed' : 'Not completed'
  const category = getCategoryLabel(slot.category)
  const detail = slot.detail || slot.tip || ''

  return `${status}. ${slot.time}. ${category}. ${slot.text}. ${detail}`
}

function getWeekReadableText(week) {
  return `Week ${week.week}. ${week.title || week.focus || `Week ${week.week}`}. ${week.progress} percent complete.`
}

function getDayReadableText(day) {
  const todayText =
    activeRoadmapWeek.value === currentWeek.value && day.day === todayName.value
      ? 'Today. '
      : ''

  return `${todayText}${day.day}. ${day.progress} percent complete.`
}

function getCanonicalActionId(slotOrId) {
  if (slotOrId === null || slotOrId === undefined) return ''
  if (typeof slotOrId === 'string' || typeof slotOrId === 'number') return String(slotOrId).replace('today-schedule-', '')
  return String(slotOrId.sourceSlotId || slotOrId.id || '').replace('today-schedule-', '')
}

function buildProgressItems(updatedState) {
  return { ...(safeObject(updatedState.progressItems) || {}), roadmapProgress: safeObject(updatedState.roadmapProgress), todaySchedule: safeObject(updatedState.todaySchedule), plannerOverrides: safeObject(updatedState.plannerOverrides) }
}

function togglePlanAction(slotOrId) {
  const actionId = getCanonicalActionId(slotOrId)
  if (!actionId) return
  const currentRoadmapProgress = safeObject(state.roadmapProgress)
  const currentTodaySchedule = safeObject(state.todaySchedule)
  const nextDone = !currentRoadmapProgress[actionId]
  const updatedState = { ...state, roadmapProgress: { ...currentRoadmapProgress, [actionId]: nextDone }, todaySchedule: { ...currentTodaySchedule, [`today-schedule-${actionId}`]: nextDone } }
  updatedState.progressItems = buildProgressItems(updatedState)
  saveAndPersist(updatedState)
}

function toggleTodayScheduleSlot(slot) { togglePlanAction(slot) }
function toggleRoadmapDailyAction(actionId) { if (!canModifySelectedPlannerDay.value) return; togglePlanAction(actionId) }

function startEditingPlanner() {
  if (!canModifySelectedPlannerDay.value) return
  const editable = {}
  ;(selectedPlannerDayData.value.timeSlots || []).forEach(slot => {
    editable[slot.id] = { time: slot.time, text: slot.text, tip: slot.tip || slot.detail || '', category: slot.category }
  })
  editablePlanner.value = editable
  isEditingPlanner.value = true
}

function cancelEditingPlanner() { editablePlanner.value = {}; isEditingPlanner.value = false }

function saveEditedPlanner() {
  const updatedState = { ...state, plannerOverrides: { ...safeObject(state.plannerOverrides), ...safeObject(editablePlanner.value) } }
  updatedState.progressItems = buildProgressItems(updatedState)
  saveAndPersist(updatedState)
  editablePlanner.value = {}
  isEditingPlanner.value = false
}

function saveAndPersist(updatedState) {
  dashboardSaveError.value = ''
  savePlan(updatedState)
  persistDashboardUpdate(updatedState).catch(error => { dashboardSaveError.value = error.message || 'Dashboard sync failed'; console.error('Sync failed:', error) })
}

async function persistDashboardUpdate(updatedState) {
  const username = updatedState.username || state.username
  if (!username) throw new Error('Missing username')
  if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')
  const roadmapProgress = safeObject(updatedState.roadmapProgress)
  const todaySchedule = safeObject(updatedState.todaySchedule)
  const plannerOverrides = safeObject(updatedState.plannerOverrides)
  const progressItems = { ...safeObject(updatedState.progressItems), roadmapProgress, todaySchedule, plannerOverrides }
  const payload = { dailyPlan: updatedState.dailyPlan ?? state.dailyPlan ?? {}, progressItems, roadmapProgress, todaySchedule, plannerOverrides, streakDays: updatedState.streakDays ?? state.streakDays ?? 0, nextAction: updatedState.nextAction ?? state.nextAction, mission: updatedState.mission ?? state.mission }
  isSavingDashboard.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/${encodeURIComponent(username)}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    const data = await response.json().catch(() => ({}))
    if (!response.ok) throw new Error(data.error || `Update failed: ${response.status}`)
    const normalizedResponse = normalizeDashboardProfile({ ...updatedState, ...data })
    savePlan({ ...state, ...normalizedResponse })
    return data
  } finally { isSavingDashboard.value = false }
}

function onScroll() {
  const hasScrolled = window.scrollY > 120

  isScrolled.value = window.scrollY > 40
  showPlannerBackTop.value = activeDashboardTab.value === 'progress' && hasScrolled
}

const familyCode = computed(() =>
  state.username ||
  state.userName ||
  state.user_name ||
  localStorage.getItem('hk-parent-username') ||
  'Family'
)

const parentDisplayName = computed(() => familyCode.value)

const selectedDateLabel = computed(() =>
  new Date().toLocaleDateString(LOCALE, { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric', timeZone: TIME_ZONE })
)

function scrollToTop() { window.scrollTo({ top: 0, behavior: 'smooth' }) }

watch(currentWeek, (nextWeek, previousWeek) => {
  if (activeRoadmapWeek.value === previousWeek || !fourWeekRoadmap.value.some(week => week.id === activeRoadmapWeek.value)) {
    activeRoadmapWeek.value = nextWeek
  }
}, { immediate: true })

watch(activeRoadmapWeek, weekId => { selectedPlannerDay.value = weekId === currentWeek.value ? todayName.value : 'Monday' })

watch(activeDashboardTab, tab => {
  showPlannerBackTop.value = tab === 'progress' && window.scrollY > 120
})

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  const routeUsername = route.query.username || route.params.username || ''
  const savedUsername = state.username || state.userName || state.user_name || localStorage.getItem('hk-parent-username') || ''
  const username = String(routeUsername || savedUsername).trim()
  if (username) loadDashboard(username).catch(error => console.error('Dashboard load failed:', error))
  nowTimer = window.setInterval(() => {
  nowTick.value = Date.now()
}, 60_000)
})

onUnmounted(() => { window.removeEventListener('scroll', onScroll) 
if (nowTimer) window.clearInterval(nowTimer)
})
</script>