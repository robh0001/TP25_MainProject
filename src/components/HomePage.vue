<template>
  <div class="page" ref="pageEl">

    <div class="noise-overlay" aria-hidden="true"></div>

    <header class="header" :class="{ scrolled: isScrolled }">
      <div class="header-inner">
        <RouterLink to="/" class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2"/>
              <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor"/>
              <path d="M18 13C15.5 15.5 15 19 18 23" stroke="white" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.55"/>
            </svg>
          </div>
          <span class="logo-text">HealthyKids</span>
        </RouterLink>

        <nav class="nav">
          <a href="#about">About</a>
          <a href="#focus">Approach</a>
          <a href="#how">How it works</a>
          <a href="#insights">Research</a>
        </nav>

        <div class="nav-cta">
          <RouterLink to="/parent-entry" class="nav-link">Parent portal</RouterLink>
          <RouterLink to="/young-person-dashboard" class="nav-btn">
            Kids dashboard
            <svg width="12" height="12" viewBox="0 0 12 12"><path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </RouterLink>
        </div>
      </div>
    </header>

    <main>
      <section class="hero">
        <div class="hero-bg">
          <div class="hero-blob hero-blob-1"></div>
          <div class="hero-blob hero-blob-2"></div>
          <div class="hero-blob hero-blob-3"></div>
          <div class="hero-lines" aria-hidden="true">
            <span v-for="n in 8" :key="n"></span>
          </div>
        </div>

        <div class="hero-wrap">
          <div class="hero-badge-row">
            <div class="live-badge">
              <span class="live-dot"></span>
              <span>Actively supporting 12,000+ families · Australia 2025</span>
            </div>
          </div>

          <div class="hero-headline">
            <h1>
              <span class="hl-row hl-serif">Healthier kids</span>
              <span class="hl-row hl-mixed">
                <span class="hl-thin">start with</span>
                <span class="hl-em"> better habits.</span>
              </span>
            </h1>
          </div>

          <div class="hero-sub-row">
            <p class="hero-desc">
              HealthyKids turns complex family health data into a clear,
              personalised weekly plan - covering nutrition, movement,
              sleep, and daily routine for children aged 5 - 12.
            </p>
            <div class="hero-actions">
              <RouterLink to="/parent-entry" class="btn-hero">
                Build your family plan
                <svg width="16" height="16" viewBox="0 0 16 16"><path d="M3 8h10M9 4.5l4 3.5-4 3.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </RouterLink>
              <RouterLink to="/parent-dashboard" class="btn-ghost-hero">View live demo</RouterLink>
            </div>
          </div>

          <div class="trust-strip">
            <div class="trust-item">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7l3 3L11.5 4" stroke="#22c55e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>Free · no account needed</span>
            </div>
            <div class="trust-sep"></div>
            <div class="trust-item">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7l3 3L11.5 4" stroke="#22c55e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>3-minute onboarding</span>
            </div>
            <div class="trust-sep"></div>
            <div class="trust-item">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7l3 3L11.5 4" stroke="#22c55e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>Evidence-based · Monash University</span>
            </div>
            <div class="trust-sep"></div>
            <div class="trust-item">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7l3 3L11.5 4" stroke="#22c55e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>94% see results in 2 weeks</span>
            </div>
          </div>
        </div>

        <div class="hero-product">
          <div class="product-frame">
            <div class="product-chrome">
              <div class="chrome-dots"><span></span><span></span><span></span></div>
              <div class="chrome-url">healthykids.app/dashboard</div>
              <div class="chrome-controls"><span></span><span></span></div>
            </div>
            <div class="product-screen">
              <div class="dash-sidebar">
                <div class="dash-logo-sm">HK</div>
                <div class="dash-nav-items">
                  <div class="dash-nav-item active">
                    <svg width="15" height="15" viewBox="0 0 16 16"><rect x="2" y="2" width="5" height="5" rx="1.2" fill="currentColor"/><rect x="9" y="2" width="5" height="5" rx="1.2" fill="currentColor"/><rect x="2" y="9" width="5" height="5" rx="1.2" fill="currentColor"/><rect x="9" y="9" width="5" height="5" rx="1.2" fill="currentColor"/></svg>
                  </div>
                  <div class="dash-nav-item">
                    <svg width="15" height="15" viewBox="0 0 16 16"><circle cx="8" cy="6" r="3" stroke="currentColor" stroke-width="1.3" fill="none"/><path d="M2 14c0-3 2.7-5 6-5s6 2 6 5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" fill="none"/></svg>
                  </div>
                  <div class="dash-nav-item">
                    <svg width="15" height="15" viewBox="0 0 16 16"><path d="M2 10l4-4 3 3 5-6" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
                  </div>
                  <div class="dash-nav-item">
                    <svg width="15" height="15" viewBox="0 0 16 16"><path d="M3 12V7l5-4 5 4v5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" fill="none"/><rect x="6" y="9" width="4" height="3" rx="0.5" stroke="currentColor" stroke-width="1.3" fill="none"/></svg>
                  </div>
                </div>
              </div>
              <div class="dash-main">
                <div class="dash-topbar">
                  <div class="dash-greeting">
                    <div class="dash-greeting-sub">Week 12 · May 2025</div>
                    <div class="dash-greeting-main">Good morning, Sarah </div>
                  </div>
                  <div class="dash-streak-badge">
                    <span class="streak-flame"></span>
                    <div>
                      <div class="streak-n">14</div>
                      <div class="streak-l">day streak</div>
                    </div>
                  </div>
                </div>

                <div class="dash-kpis">
                  <div class="dash-kpi dash-kpi-primary">
                    <div class="kpi-label">Family score</div>
                    <div class="kpi-val">82<span>/100</span></div>
                    <div class="kpi-delta up">↑ +6 this week</div>
                  </div>
                  <div class="dash-kpi">
                    <div class="kpi-label">Goals completed</div>
                    <div class="kpi-val">11<span>/14</span></div>
                    <div class="kpi-delta up">↑ 79%</div>
                  </div>
                  <div class="dash-kpi">
                    <div class="kpi-label">Nutrition</div>
                    <div class="kpi-val">88<span>%</span></div>
                    <div class="kpi-delta up">↑ On track</div>
                  </div>
                  <div class="dash-kpi">
                    <div class="kpi-label">Sleep avg.</div>
                    <div class="kpi-val">8.4<span>hrs</span></div>
                    <div class="kpi-delta neutral">→ Target: 9</div>
                  </div>
                </div>

                <div class="dash-row-2">
                  <div class="dash-chart-area">
                    <div class="chart-label">Progress · 7 days</div>
                    <div class="chart-bars">
                      <div v-for="(bar, i) in chartBars" :key="i" class="chart-bar-col">
                        <div class="chart-bar" :style="{ height: bar.h + '%' }" :class="{ today: bar.today }"></div>
                        <div class="chart-day">{{ bar.day }}</div>
                      </div>
                    </div>
                  </div>
                  <div class="dash-actions">
                    <div class="dash-actions-label">Today's actions</div>
                    <div v-for="action in dashActions" :key="action.text" class="dash-action-item" :class="{ done: action.done }">
                      <div class="action-check" :class="{ done: action.done }">
                        <svg v-if="action.done" width="10" height="10" viewBox="0 0 10 10"><path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
                      </div>
                      <span>{{ action.text }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="anno anno-1">
            <div class="anno-dot"></div>
            <div class="anno-card">
              <div class="anno-icon">📊</div>
              <div class="anno-content">
                <strong>Personalised weekly plan</strong>
                <span>Based on your quiz responses</span>
              </div>
            </div>
          </div>
          <div class="anno anno-2">
            <div class="anno-dot"></div>
            <div class="anno-card">
              <div class="anno-icon">⚡</div>
              <div class="anno-content">
                <strong>Real-time habit tracking</strong>
                <span>Log daily and watch progress build</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="proof-bar">
        <div class="proof-inner">
          <span class="proof-label">Trusted by parents across Australia · Aligned with</span>
          <div class="proof-logos">
            <div class="proof-logo">
              <svg width="20" height="20" viewBox="0 0 36 36"><circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.5" fill="none"/><text x="18" y="23" text-anchor="middle" font-size="11" font-weight="600" fill="currentColor">MU</text></svg>
              <span>Monash University</span>
            </div>
            <div class="proof-div"></div>
            <div class="proof-logo">
              <svg width="20" height="20" viewBox="0 0 22 22"><circle cx="11" cy="11" r="9" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M6 11a5 5 0 0 0 5 5 5 5 0 0 0 5-5" stroke="currentColor" stroke-width="1.4" fill="none"/><path d="M11 6v5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
              <span>UN SDG 3</span>
            </div>
            <div class="proof-div"></div>
            <div class="proof-logo">
              <svg width="20" height="20" viewBox="0 0 22 22"><path d="M4 11h14M4 7h10M4 15h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              <span>Evidence-based</span>
            </div>
            <div class="proof-div"></div>
            <div class="proof-logo">
              <svg width="20" height="20" viewBox="0 0 22 22"><path d="M11 3l2.2 6.6H20l-5.6 4 2.1 6.6L11 16.2l-5.5 4 2.1-6.6L2 9.6h6.8z" stroke="currentColor" stroke-width="1.3" fill="none"/></svg>
              <span>12,000+ families</span>
            </div>
          </div>
        </div>
      </section>

      <section id="about" class="value-section">
        <div class="value-wrap">
          <div class="value-left">
            <div class="section-eyebrow">The problem we solve</div>
            <h2 class="value-h2">Parents want to help.<br>The advice is <em>overwhelming.</em></h2>
          </div>
          <div class="value-right">
            <p class="value-lede">Most family health guidance is generic, conflicting, and unrealistic. HealthyKids cuts through that - turning your child's actual habits into a specific, achievable weekly plan.</p>
            <div class="value-cards">
              <div class="vcard">
                <div class="vcard-number">01</div>
                <div class="vcard-content">
                  <h3>Personalised to your child</h3>
                  <p>Quiz responses drive tailored recommendations - not generic checklists that feel impossible to follow.</p>
                </div>
              </div>
              <div class="vcard">
                <div class="vcard-number">02</div>
                <div class="vcard-content">
                  <h3>Built for busy parents</h3>
                  <p>3-minute onboarding, weekly focus, and a dashboard showing exactly what to do next - nothing more.</p>
                </div>
              </div>
              <div class="vcard">
                <div class="vcard-number">03</div>
                <div class="vcard-content">
                  <h3>Four pillars, one plan</h3>
                  <p>Nutrition, movement, sleep, and daily routine - scored, prioritised, and actioned together.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="value-fullbleed">
          <img src="https://images.unsplash.com/photo-1609220136736-443140cffec6?auto=format&fit=crop&w=2000&q=90" alt="Family cooking together" />
          <div class="fullbleed-overlay"></div>
          <div class="fullbleed-stats">
            <div class="fstat">
              <div class="fstat-n">94<span>%</span></div>
              <div class="fstat-l">of parents report clearer routines within 2 weeks</div>
            </div>
            <div class="fstat-sep"></div>
            <div class="fstat">
              <div class="fstat-n">12k<span>+</span></div>
              <div class="fstat-l">families onboarded across Australia</div>
            </div>
            <div class="fstat-sep"></div>
            <div class="fstat">
              <div class="fstat-n">4</div>
              <div class="fstat-l">health pillars in one personalised plan</div>
            </div>
            <div class="fstat-sep"></div>
            <div class="fstat">
              <div class="fstat-n">3<span>min</span></div>
              <div class="fstat-l">average onboarding - no account required</div>
            </div>
          </div>
        </div>
      </section>

      <section id="focus" class="pillars-section">
        <div class="pillars-wrap">
          <div class="pillars-head">
            <div class="section-eyebrow">Our approach</div>
            <h2>Four pillars.<br><em>One clear direction.</em></h2>
            <p>Every recommendation maps to one of four core areas. We surface whichever needs the most attention and give you one focused action at a time.</p>
          </div>
          <div class="pillars-grid">
            <div class="pillar-item" v-for="p in pillarsData" :key="p.key">
              <div class="pillar-img">
                <img :src="p.img" :alt="p.name" />
                <div class="pillar-img-cover"></div>
              </div>
              <div class="pillar-body">
                <div class="pillar-index">{{ p.idx }}</div>
                <div class="pillar-chip" :class="'pillar-chip-' + p.color">{{ p.name }}</div>
                <h3>{{ p.headline }}</h3>
                <p>{{ p.desc }}</p>
                <div class="pillar-tags">
                  <span v-for="t in p.tags" :key="t">{{ t }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="how" class="process-section">
        <div class="process-wrap">
          <div class="process-head">
            <div class="section-eyebrow">How it works</div>
            <h2>From quiz to results<br>in <em>three steps.</em></h2>
          </div>
          <div class="process-steps">
            <div class="process-step" v-for="(step, i) in processSteps" :key="i">
              <div class="pstep-media">
                <img :src="step.img" :alt="step.title" />
                <div class="pstep-num">{{ String(i+1).padStart(2,'0') }}</div>
              </div>
              <div class="pstep-body">
                <h3>{{ step.title }}</h3>
                <p>{{ step.body }}</p>
              </div>
            </div>
          </div>
          <div class="process-cta-nudge">
            <RouterLink to="/parent-entry" class="btn-process">Start your plan - it's free →</RouterLink>
            <span>No account · 3 minutes · Immediate results</span>
          </div>
        </div>
      </section>

      <section id="insights" class="research-section wellbeing-light-section ">
        <div class="research-wrap">
          <div class="research-head">
              <h2>Understanding where families may need support.</h2>
              <br>
              <p>
                HealthyKids uses simple wellbeing insights to help families focus on one
                area at a time - with gentle, practical support.
              </p>
            <div class="rtabs">
              <button v-for="tab in tabs" :key="tab.key" :class="['rtab', { active: activeInsight === tab.key }]" @click="activeInsight = tab.key">{{ tab.label }}</button>
            </div>
          </div>

          <div class="research-panel">
            <div v-if="loadingInsights" class="rpanel-loading"><div class="rspinner"></div></div>
            <div v-else-if="insightsError" class="rpanel-err">{{ insightsError }}</div>
            <template v-else-if="insights">

              <div v-show="activeInsight === 'body'" class="rpane">
                <div class="rpane-main children-grid-card">
                  <div class="children-grid-head">
                    <div>
                      <h3>Out of every 100 children</h3>
                      <p>
                        A simple view of children's growth patterns, shown in a way that is
                        easier for families to understand.
                      </p>
                    </div>

                    <div class="children-grid-badge">
                      {{ formattedHeadlinePct }} in healthy range
                    </div>
                  </div>

                  <div class="children-grid-wrap">
                    <div class="children-grid">
                      <div
                        v-for="child in childrenGrid"
                        :key="child.id"
                        class="child-square"
                        :class="'child-' + child.key"
                        :title="child.label"
                      ></div>
                    </div>

                    <div class="children-legend">
                      <div
                        v-for="item in friendlyBodySegments"
                        :key="item.key"
                        class="legend-item"
                      >
                        <span class="legend-dot" :class="'legend-' + item.key"></span>
                        <div>
                          <strong>{{ item.value }} children</strong>
                          <small>{{ item.friendlyLabel }}</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="rpane-notes">
                  <div class="rnote">
                    <div class="rnote-head">What this means</div>
                    <p>
                      Children's wellbeing is shaped by everyday routines, including meals,
                      movement, sleep, and family structure.
                    </p>
                  </div>

                  <div class="rnote">
                    <div class="rnote-head">How HealthyKids helps</div>
                    <p>
                      HealthyKids turns wellbeing insights into small, realistic actions that
                      families can try at home without pressure.
                    </p>
                  </div>
                </div>
              </div>

              <div v-show="activeInsight === 'sleep'" class="rpane">
                <div class="rpane-main simple-sleep-card">
                  <div class="simple-sleep-head">
                    <div>
                      <h3>Sleep routine snapshot</h3>
                      <p>
                        A simple view of children's sleep patterns across school nights and weekends.
                      </p>
                    </div>

                    <div class="simple-sleep-badge">
                      {{ sleepHeadlinePct }} reach target sleep
                    </div>
                  </div>

                  <div class="sleep-simple-grid">
                    <div class="sleep-big-card sleep-target-card">
                      <small>Target sleep</small>
                      <strong>{{ sleepHeadlinePct }}</strong>
                      <p>of children reach the target sleep range.</p>
                    </div>

                    <div class="sleep-big-card">
                      <small>Most common on weeknights</small>
                      <strong>{{ weeknightTopBand.friendlyLabel }}</strong>
                      <p>{{ weeknightTopBand.value }}% of children are in this range.</p>
                    </div>

                    <div class="sleep-big-card">
                      <small>Most common on weekends</small>
                      <strong>{{ weekendTopBand.friendlyLabel }}</strong>
                      <p>{{ weekendTopBand.value }}% of children are in this range.</p>
                    </div>
                  </div>

                  <div class="sleep-takeaway">
                    <div>
                      <strong>Parent takeaway</strong>
                      <p>{{ weekendShiftText }}</p>
                    </div>
                  </div>
                </div>

                <div class="rpane-notes">
                  <div class="rnote">
                    <div class="rnote-head">Why this matters</div>
                    <p>
                      Sleep routines can affect children's mood, energy, focus, and daily habits.
                    </p>
                  </div>

                  <div class="rnote">
                    <div class="rnote-head">How HealthyKids helps</div>
                    <p>
                      HealthyKids suggests small bedtime actions that families can try without pressure.
                    </p>
                  </div>
                </div>
              </div>

              <div v-show="activeInsight === 'activity'" class="rpane">
                <div class="rpane-main simple-activity-card">
                  <div class="simple-activity-head">
                    <div>
                      <h3>Daily movement snapshot</h3>
                      <p>
                        A simple view to help families understand inactive time and where
                        small movement breaks may help.
                      </p>
                    </div>

                    <div class="simple-activity-badge">
                      {{ activityHeadlinePct }} most common band
                    </div>
                  </div>

                  <div class="activity-focus-card">

                    <div class="activity-focus-content">
                      <small>Most common inactive time</small>
                      <strong>{{ activityTopBand.friendlyLabel }}</strong>
                      <p>
                        {{ activityTopBand.value }}% of children are in this range.
                      </p>
                    </div>
                  </div>

                  <div class="activity-parent-summary">
                    <div class="activity-summary-item">
                      <span>What this means</span>
                      <p>
                        Many children spend a large part of the day sitting during school,
                        homework, travel, and screen time.
                      </p>
                    </div>

                    <div class="activity-summary-item">
                      <span>What families can try</span>
                      <p>
                        Add 2-3 short movement breaks into the day, such as after school,
                        before dinner, or between screen sessions.
                      </p>
                    </div>
                  </div>
                </div>

                <div class="rpane-notes">
                  <div class="rnote">
                    <div class="rnote-head">Parent takeaway</div>
                    <p>
                      The goal is not intense exercise every day. Small active moments can
                      make daily routines healthier and easier to maintain.
                    </p>
                  </div>

                  <div class="rnote">
                    <div class="rnote-head">How HealthyKids helps</div>
                    <p>
                      HealthyKids suggests simple movement ideas that fit into normal family
                      routines.
                    </p>
                  </div>
                </div>
              </div>

            </template>
          </div>
        </div>
      </section>

      <section class="pathways-section">
        <div class="pathways-wrap">
          <div class="pathway" style="background:#f7f6f2">
            <div class="pathway-body">
              <div class="pathway-eyebrow">For parents</div>
              <h3>Build, manage and track your family's health plan.</h3>
              <p>Complete the quiz, get personalised recommendations, and use the dashboard to track habits across nutrition, movement, sleep, and routine.</p>
              <ul class="pathway-list">
                <li>3-minute personalised quiz</li>
                <li>Weekly prioritised action plan</li>
                <li>Progress tracking dashboard</li>
              </ul>
              <RouterLink to="/parent-entry" class="pathway-btn-dark">Go to parent portal →</RouterLink>
            </div>
          </div>
          <div class="pathway" style="background:#0d1f14">
            <div class="pathway-body pathway-body-dark">
              <div class="pathway-eyebrow pathway-eyebrow-green">For kids aged 5–12</div>
              <h3 style="color:#fff">A playful dashboard made just for children.</h3>
              <p style="color:rgba(255,255,255,0.5)">Missions, streaks, and habit goals in a fun, age-appropriate experience that connects directly to the parent plan.</p>
              <ul class="pathway-list pathway-list-dark">
                <li>Adventure missions & habit goals</li>
                <li>Visual progress & rewards</li>
                <li>Synced with parent dashboard</li>
              </ul>
              <RouterLink to="/young-person-dashboard" class="pathway-btn-green">Open Kids dashboard →</RouterLink>
            </div>
          </div>
        </div>
      </section>

      <section class="testimonials-section">
        <div class="testimonials-wrap">
          <div class="test-head">
            <div class="section-eyebrow">Parent stories</div>
            <h2>Real families.<br><em>Real results.</em></h2>
          </div>
          <div class="testimonials-layout">
            <div class="testimonials-col-a">
              <blockquote class="tq tq-lg">
                <div class="tq-stars">★★★★★</div>
                <p>"HealthyKids gave our family a clear way to manage after-school time. The actions were small enough to actually follow — and that made all the difference."</p>
                <footer>
                  <div class="tq-av" style="background:#dbeafe">SL</div>
                  <div><strong>Sarah L.</strong><span>Parent of a 7-year-old, Melbourne</span></div>
                </footer>
              </blockquote>
            </div>
            <div class="testimonials-col-b">
              <blockquote class="tq">
                <div class="tq-stars">★★★★★</div>
                <p>"Instead of generic advice, I got a dashboard telling me exactly what to do each day. Everything felt realistic for our busy family."</p>
                <footer>
                  <div class="tq-av" style="background:#f3e8ff">MJ</div>
                  <div><strong>Marcus J.</strong><span>Parent of a 9-year-old, Sydney</span></div>
                </footer>
              </blockquote>
              <blockquote class="tq">
                <div class="tq-stars">★★★★★</div>
                <p>"It focused on progress, not perfection. Improving our family's routines felt genuinely achievable for all of us."</p>
                <footer>
                  <div class="tq-av" style="background:#fce7f3">AT</div>
                  <div><strong>Anika T.</strong><span>Parent of an 11-year-old, Brisbane</span></div>
                </footer>
              </blockquote>
            </div>
          </div>
        </div>
      </section>

      <section class="final-cta">
        <div class="fcta-inner">
          <div class="fcta-bg">
            <img src="https://images.unsplash.com/photo-1484665042814-bf35cda4e7e5?auto=format&fit=crop&w=2000&q=85" alt="" aria-hidden="true" />
            <div class="fcta-overlay"></div>
          </div>
          <div class="fcta-content">
            <div class="section-eyebrow light">Ready to start?</div>
            <h2 class="fcta-h2">Build healthier routines<br>for your family - today.</h2>
            <p>Join 12,000+ Australian families already making progress. Free, no account required, results in 3 minutes.</p>
            <div class="fcta-btns">
              <RouterLink to="/parent-entry" class="fcta-btn-primary">Start your family plan →</RouterLink>
              <RouterLink to="/young-person-dashboard" class="fcta-btn-secondary">Open Kids portal</RouterLink>
            </div>
          </div>
        </div>
      </section>

    </main>

    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-col">
          <RouterLink to="/" class="logo">
            <div class="logo-icon"><svg viewBox="0 0 36 36" fill="none"><circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2"/><path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor"/></svg></div>
            <span class="logo-text">HealthyKids</span>
          </RouterLink>
          <p class="footer-tagline">A Monash University SDG 3 project<br>Team TP25 · 2025</p>
        </div>
        <div class="footer-col">
          <div class="footer-col-head">Product</div>
          <RouterLink to="/parent-entry">Parent portal</RouterLink>
          <RouterLink to="/young-person-dashboard">Kids dashboard</RouterLink>
          <RouterLink to="/parent-dashboard">Family dashboard</RouterLink>
        </div>
        <div class="footer-col">
          <div class="footer-col-head">Learn</div>
          <a href="#about">About</a>
          <a href="#focus">Approach</a>
          <a href="#how">How it works</a>
          <a href="#insights">Research</a>
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
import { RouterLink } from 'vue-router'
import { computed, onMounted, onUnmounted, ref } from 'vue'

const isScrolled = ref(false)
const activeInsight = ref('body')
const insights = ref(null)
const loadingInsights = ref(false)
const insightsError = ref('')

const tabs = [
  { key: 'body', label: 'Body balance' },
  { key: 'sleep', label: 'Sleep patterns' },
  { key: 'activity', label: 'Activity levels' },
]

const chartBars = [
  { h: 48, day: 'M' }, { h: 62, day: 'T' }, { h: 55, day: 'W' },
  { h: 70, day: 'T' }, { h: 74, day: 'F' }, { h: 80, day: 'S' }, { h: 88, day: 'S', today: true },
]

const dashActions = [
  { text: 'Screens off by 8:30pm', done: true },
  { text: 'Include a vegetable at dinner', done: true },
  { text: '30 min outdoor play after school', done: false },
  { text: 'Consistent wake time (7am)', done: false },
]

const pillarsData = [
  { key: 'nutrition', idx: '01', name: 'Nutrition', color: 'green', headline: 'Healthier meals, without the fight.', desc: "Practical meal and snack strategies that fit your family's schedule - not idealised plans that gather dust.", tags: ['Meal planning', 'Smart snacking', 'Hydration'], img: 'https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=900&q=85' },
  { key: 'movement', idx: '02', name: 'Movement', color: 'blue', headline: 'More active. Every single day.', desc: 'Build joyful, consistent movement habits into after-school time and weekends - without forcing it.', tags: ['Active play', 'Sport & games', 'Screen breaks'], img: 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&w=900&q=85' },
  { key: 'sleep', idx: '03', name: 'Sleep', color: 'indigo', headline: 'Calmer evenings. Deeper rest.', desc: "Wind-down routines and bedtime strategies tailored to your child's age and current patterns.", tags: ['Bedtime rituals', 'Wind-down', 'Screen limits'], img: 'https://images.unsplash.com/photo-1588072432836-e10032774350?auto=format&fit=crop&w=900&q=85' },
  { key: 'routine', idx: '04', name: 'Daily Routine', color: 'amber', headline: 'Structure that actually sticks.', desc: 'Build consistent habits around devices, homework, meals, and bedtime - reducing friction for the whole family.', tags: ['Device balance', 'After-school', 'Consistency'], img: 'https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&w=900&q=85' },
]

const processSteps = [
  {
    title: 'Complete the quiz',
    body: "Parents answer targeted questions about their child's current routines, habits, and primary concerns - in under 3 minutes.",
    img: 'https://images.pexels.com/photos/4145153/pexels-photo-4145153.jpeg?auto=compress&cs=tinysrgb&w=1200',
  },
  {
    title: 'Receive your plan',
    body: 'We analyse your responses against population health data to surface priority areas and generate a personalised weekly action plan.',
    img: 'https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=1200',
  },
  {
    title: 'Build lasting habits',
    body: 'Use the parent and kids dashboards to log habits, track progress, and adapt goals as your family improves over time.',
    img: 'https://images.pexels.com/photos/8613312/pexels-photo-8613312.jpeg?auto=compress&cs=tinysrgb&w=1200',
  },
]

const API_BASE_URL = import.meta.env.VITE_PARENT_DATA_INSIGHTS_API_BASE_URL || ''
const API_URL = API_BASE_URL ? `${API_BASE_URL}/test/data-insights` : '/test/data-insights'
console.log(API_BASE_URL)
async function fetchInsights() {
  loadingInsights.value = true
  insightsError.value = ''
  try {
    const res = await fetch(API_URL)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    insights.value = await res.json()
  } catch (err) {
    insightsError.value = err.message || 'Unable to load insights.'
  } finally {
    loadingInsights.value = false
  }
}

function onScroll() { isScrolled.value = window.scrollY > 40 }

onMounted(() => {
  fetchInsights()
  window.addEventListener('scroll', onScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})

const bodyRingStyle = computed(() => {
  const segs = insights.value?.bodyBalance?.segments
  if (!segs?.length) return { background: '#e5e7eb' }
  const uw = segs.find(s => s.key === 'underweight')?.value || 0
  const nm = segs.find(s => s.key === 'normal')?.value || 0
  const ow = segs.find(s => s.key === 'overweight')?.value || 0
  const ob = segs.find(s => s.key === 'obese')?.value || 0
  const a = uw, b = uw + nm, c = uw + nm + ow, d = uw + nm + ow + ob
  return { background: `conic-gradient(#93c5fd ${0}% ${a}%, #4ade80 ${a}% ${b}%, #fbbf24 ${b}% ${c}%, #f87171 ${c}% ${d}%, #e5e7eb ${d}% 100%)` }
})

const friendlyBodySegments = computed(() => {
  const segs = insights.value?.bodyBalance?.segments || []

  const labelMap = {
    underweight: 'Below healthy range',
    normal: 'Healthy range',
    overweight: 'Above healthy range',
    obese: 'Needs extra support',
  }

  return segs.map((seg) => ({
    ...seg,
    friendlyLabel: labelMap[seg.key] || seg.label,
    value: Math.round(Number(seg.value || 0)),
  }))
})

const childrenGrid = computed(() => {
  const segs = friendlyBodySegments.value

  if (!segs.length) return []

  let counts = segs.map((seg) => ({
    key: seg.key,
    label: seg.friendlyLabel,
    count: Math.round(Number(seg.value || 0)),
  }))

  const total = counts.reduce((sum, item) => sum + item.count, 0)
  const diff = 100 - total

  if (diff !== 0 && counts.length) {
    const largestIndex = counts.reduce((maxIndex, item, index, arr) => {
      return item.count > arr[maxIndex].count ? index : maxIndex
    }, 0)

    counts[largestIndex].count += diff
  }

  const squares = []
  let id = 1

  counts.forEach((item) => {
    for (let i = 0; i < item.count; i++) {
      squares.push({
        id,
        key: item.key,
        label: item.label,
      })
      id++
    }
  })

  return squares.slice(0, 100)
})

const formattedHeadlinePct = computed(() => {
  const pct = Number(insights.value?.bodyBalance?.headlinePct || 0)
  return `${Math.round(pct)}%`
})

const sleepHeadlinePct = computed(() => {
  const pct = Number(insights.value?.sleep?.headlinePct || 0)
  return `${Math.round(pct)}%`
})

function simplifySleepLabel(label = '') {
  const map = {
    'Less than 6 hours': 'Less than 6 hours',
    '6 to less than 7 hours': '6–7 hours',
    '7 to less than 8 hours': '7–8 hours',
    '8 to less than 9 hours': '8–9 hours',
    '9 to less than 10 hours': '9–10 hours',
    '10 hours or more': '10+ hours',
  }

  return map[label] || label
}

function mapSleepBands(items = []) {
  return items.map((item) => ({
    ...item,
    friendlyLabel: simplifySleepLabel(item.label),
    value: Number(item.value || 0),
  }))
}

const friendlySleepWeeknight = computed(() =>
  mapSleepBands(insights.value?.sleep?.weeknight || [])
)

const friendlySleepWeekend = computed(() =>
  mapSleepBands(insights.value?.sleep?.weekend || [])
)

function getTopBand(items = []) {
  if (!items.length) {
    return {
      friendlyLabel: '-',
      value: 0,
    }
  }

  return items.reduce((best, current) =>
    Number(current.value) > Number(best.value) ? current : best
  )
}

const weeknightTopBand = computed(() =>
  getTopBand(friendlySleepWeeknight.value)
)

const weekendTopBand = computed(() =>
  getTopBand(friendlySleepWeekend.value)
)

const weekendShiftText = computed(() => {
  const weeknight = weeknightTopBand.value?.friendlyLabel || '-'
  const weekend = weekendTopBand.value?.friendlyLabel || '-'

  if (weeknight === weekend) {
    return `The most common sleep range is ${weeknight} on both weeknights and weekends, which suggests a fairly consistent routine.`
  }

  return `The most common sleep range changes from ${weeknight} on weeknights to ${weekend} on weekends, which may suggest routines shift at the end of the week.`
})

const activityHeadlinePct = computed(() => {
  const pct = Number(insights.value?.activity?.headlinePct || 0)
  return `${Math.round(pct)}%`
})

function simplifyActivityLabel(label = '') {
  const map = {
    'Less than 9 hours': 'Less than 9 hours',
    '9 to less than 10 hours': '9–10 hours',
    '10 to less than 11 hours': '10–11 hours',
    '11 to less than 12 hours': '11–12 hours',
    '12 to less than 13 hours': '12–13 hours',
    '13 to less than 14 hours': '13–14 hours',
    '14 hours or more': '14+ hours',
  }

  return map[label] || label
}

const friendlyActivityBands = computed(() => {
  const bands = insights.value?.activity?.bands || []

  return bands.map((item) => ({
    ...item,
    value: Number(item.value || 0),
    friendlyLabel: simplifyActivityLabel(item.label),
  }))
})

const activityTopBand = computed(() => {
  const bands = friendlyActivityBands.value

  if (!bands.length) {
    return {
      label: '',
      friendlyLabel: '—',
      value: 0,
    }
  }

  return bands.reduce((best, current) =>
    Number(current.value) > Number(best.value) ? current : best
  )
})
</script>

<style scoped>
:global(:root) {
  --c-black: #0a0b0a;
  --c-900: #111312;
  --c-800: #1c1f1d;
  --c-700: #2d3230;
  --c-500: #52605a;
  --c-400: #7a8880;
  --c-300: #a8b5ae;
  --c-100: #e8ece9;
  --c-50: #f4f5f2;
  --c-white: #ffffff;

  --c-green: #16a34a;
  --c-green-mid: #22c55e;
  --c-green-soft: #f0fdf4;
  --c-green-pale: #dcfce7;

  --c-blue-soft: #eff6ff;
  --c-indigo-soft: #eef2ff;
  --c-amber-soft: #fffbeb;

  --border: rgba(10, 11, 10, 0.08);
  --border-mid: rgba(10, 11, 10, 0.14);

  --shadow-xs: 0 1px 4px rgba(0, 0, 0, 0.06);
  --shadow-sm: 0 2px 12px rgba(0, 0, 0, 0.07);
  --shadow-md: 0 8px 28px rgba(0, 0, 0, 0.09);
  --shadow-lg: 0 20px 56px rgba(0, 0, 0, 0.12);
  --shadow-xl: 0 40px 100px rgba(0, 0, 0, 0.16);

  --f-display: 'Fraunces', Georgia, serif;
  --f-body: 'General Sans', 'Helvetica Neue', ui-sans-serif, sans-serif;
  --f-mono: 'JetBrains Mono', monospace;

  --section-v: clamp(96px, 11vw, 140px);

  --r-sm: 8px;
  --r-md: 14px;
  --r-lg: 20px;
  --r-xl: 28px;
  --r-2xl: 40px;
}

/* GLOBAL */
:global(*, *::before, *::after) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  font-family: var(--f-body), system-ui;
  background: var(--c-white);
  color: var(--c-black);
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

.page {
  min-height: 100vh;
  overflow-x: clip;
  position: relative;
}

.noise-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.028;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 256px;
}

/* TYPOGRAPHY */
h1,
h2,
h3 {
  margin: 0;
  font-family: var(--f-display);
  font-weight: 400;
  letter-spacing: -0.03em;
  line-height: 1.02;
}

h1 {
  font-size: clamp(3rem, 6vw, 6.4rem);
}

h2 {
  font-size: clamp(2.2rem, 4vw, 4rem);
}

h3 {
  font-size: clamp(1.1rem, 1.6vw, 1.45rem);
  line-height: 1.25;
  font-weight: 500;
}

em {
  font-style: italic;
  color: var(--c-green);
}

p {
  font-family: var(--f-body);
  font-size: clamp(0.92rem, 1.05vw, 1.02rem);
  line-height: 1.78;
  color: var(--c-500);
  margin: 0 0 1em;
}

p:last-child {
  margin-bottom: 0;
}

.section-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 26px;
  padding: 0 11px;
  border-radius: 999px;
  border: 1px solid var(--border-mid);
  font-family: var(--f-body);
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--c-500);
  margin-bottom: 22px;
}

.section-eyebrow.light {
  border-color: rgba(255, 255, 255, 0.25);
  color: rgba(255, 255, 255, 0.6);
}

/* HEADER */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 500;
  transition: background 0.3s, border-color 0.3s, box-shadow 0.3s;
}

.header.scrolled {
  background: rgba(255, 255, 255, 0.92);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: var(--shadow-xs);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
  height: 76px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  color: var(--c-black);
}

.logo-icon {
  width: 28px;
  height: 28px;
  color: var(--c-black);
}

.logo-text {
  font-family: var(--f-display);
  font-size: 1.25rem;
  font-weight: 400;
  letter-spacing: -0.03em;
  color: var(--c-black);
}

.nav {
  display: flex;
  align-items: center;
  gap: 2px;
}

.nav a,
.nav-link {
  height: 36px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  font-family: var(--f-body);
  font-size: 0.86rem;
  font-weight: 500;
  color: var(--c-500);
  text-decoration: none;
  border-radius: 8px;
  transition: color 0.18s, background 0.18s;
}

.nav-link {
  padding: 0 14px;
}

.nav a:hover,
.nav-link:hover {
  color: var(--c-black);
  background: var(--c-50);
}

.nav-cta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-btn {
  height: 38px;
  padding: 0 16px;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-family: var(--f-body);
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--c-white);
  background: var(--c-black);
  text-decoration: none;
  border-radius: 10px;
  border: 1px solid var(--c-900);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.06) inset;
  transition: all 0.2s;
}

.nav-btn:hover {
  background: var(--c-800);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.24);
}

/* HERO */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--c-white);
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.hero-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
}

.hero-blob-1 {
  width: 700px;
  height: 700px;
  top: -200px;
  right: -150px;
  background: radial-gradient(circle, rgba(22, 163, 74, 0.09) 0%, transparent 70%);
}

.hero-blob-2 {
  width: 500px;
  height: 500px;
  bottom: 100px;
  left: -100px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.06) 0%, transparent 70%);
}

.hero-blob-3 {
  width: 400px;
  height: 400px;
  top: 40%;
  left: 35%;
  background: radial-gradient(circle, rgba(22, 163, 74, 0.05) 0%, transparent 70%);
}

.hero-lines {
  position: absolute;
  inset: 0;
  display: grid;
  grid-template-columns: repeat(8, 1fr);
}

.hero-lines span {
  border-right: 1px solid rgba(10, 11, 10, 0.04);
}

.hero-wrap {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: 160px 40px 0;
}

.hero-badge-row {
  margin-bottom: 36px;
}

.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: var(--c-green-soft);
  border: 1px solid rgba(22, 163, 74, 0.2);
  font-family: var(--f-body);
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--c-green);
  letter-spacing: 0.02em;
}

.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--c-green-mid);
  animation: live-pulse 2.4s ease-in-out infinite;
}

@keyframes live-pulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.45);
  }

  50% {
    box-shadow: 0 0 0 4px rgba(34, 197, 94, 0);
  }
}

.hero-headline {
  margin-bottom: 40px;
}

.hero-headline h1 {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.hl-row {
  display: block;
}

.hl-serif {
  font-family: var(--f-display);
  font-weight: 300;
  font-size: clamp(3.4rem, 7vw, 8rem);
  color: var(--c-black);
  letter-spacing: -0.04em;
  line-height: 0.94;
}

.hl-mixed {
  display: flex;
  align-items: baseline;
  gap: 0.22em;
  line-height: 1;
  margin-top: 4px;
}

.hl-thin {
  font-family: var(--f-body);
  font-size: clamp(1.5rem, 3.2vw, 3.6rem);
  font-weight: 300;
  color: var(--c-300);
  letter-spacing: -0.03em;
}

.hl-em {
  font-family: var(--f-display);
  font-style: italic;
  font-size: clamp(2.6rem, 5.5vw, 6.2rem);
  font-weight: 400;
  color: var(--c-green);
  letter-spacing: -0.04em;
  line-height: 1;
}

.hero-sub-row {
  display: flex;
  align-items: flex-start;
  gap: 60px;
  margin-bottom: 44px;
}

.hero-desc {
  max-width: 28rem;
  font-size: clamp(0.96rem, 1.1vw, 1.08rem);
  color: var(--c-500);
  flex-shrink: 0;
  line-height: 1.72;
  margin: 0;
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 4px;
  flex-shrink: 0;
}

.btn-hero,
.btn-ghost-hero {
  height: 52px;
  display: inline-flex;
  align-items: center;
  font-family: var(--f-body);
  font-size: 0.94rem;
  text-decoration: none;
  border-radius: 12px;
  white-space: nowrap;
  transition: all 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.btn-hero {
  padding: 0 26px;
  gap: 9px;
  font-weight: 600;
  color: var(--c-white);
  background: var(--c-black);
  border: 1px solid var(--c-900);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.22),
    0 0 0 1px rgba(255, 255, 255, 0.06) inset;
}

.btn-hero:hover {
  background: var(--c-800);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
}

.btn-ghost-hero {
  padding: 0 22px;
  font-weight: 500;
  color: var(--c-500);
  background: transparent;
  border: 1px solid var(--border-mid);
}

.btn-ghost-hero:hover {
  color: var(--c-black);
  background: var(--c-50);
}

.trust-strip {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-bottom: 60px;
  flex-wrap: wrap;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 7px;
  font-family: var(--f-body);
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--c-400);
}

.trust-sep {
  width: 1px;
  height: 14px;
  background: var(--c-100);
}

/* PRODUCT PREVIEW */
.hero-product {
  position: relative;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
}

.product-frame {
  position: relative;
  border-radius: 16px 16px 0 0;
  border: 1px solid var(--border-mid);
  border-bottom: none;
  overflow: hidden;
  box-shadow: 0 -4px 40px rgba(0, 0, 0, 0.06),
    0 -40px 100px rgba(0, 0, 0, 0.04);
  background: var(--c-50);
}

.product-chrome {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 20px;
  background: var(--c-50);
  border-bottom: 1px solid var(--border);
}

.chrome-dots,
.chrome-controls {
  display: flex;
  gap: 6px;
}

.chrome-dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--c-100);
}

.chrome-url {
  flex: 1;
  height: 26px;
  display: flex;
  align-items: center;
  padding: 0 12px;
  border-radius: 6px;
  background: var(--c-white);
  border: 1px solid var(--border);
  font-family: var(--f-mono);
  font-size: 0.72rem;
  color: var(--c-400);
}

.chrome-controls span {
  width: 24px;
  height: 24px;
  border-radius: 5px;
  background: var(--c-100);
}

.product-screen {
  display: flex;
  height: 480px;
}

.dash-sidebar {
  width: 56px;
  background: var(--c-white);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
  gap: 6px;
  flex-shrink: 0;
}

.dash-logo-sm {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--c-black);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--f-display);
  font-size: 0.7rem;
  font-weight: 500;
  color: var(--c-white);
  margin-bottom: 16px;
}

.dash-nav-items {
  display: flex;
  flex-direction: column;
  gap: 2px;
  width: 100%;
  padding: 0 8px;
}

.dash-nav-item {
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-300);
  cursor: pointer;
  transition: all 0.15s;
}

.dash-nav-item.active {
  background: var(--c-50);
  color: var(--c-black);
}

.dash-main {
  flex: 1;
  padding: 24px 28px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: var(--c-white);
}

.dash-topbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.dash-greeting-sub,
.kpi-label,
.chart-label,
.dash-actions-label {
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--c-400);
}

.dash-greeting-sub {
  margin-bottom: 4px;
}

.dash-greeting-main {
  font-family: var(--f-display);
  font-size: 1.3rem;
  font-weight: 400;
  color: var(--c-black);
  letter-spacing: -0.02em;
}

.dash-streak-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 12px;
  background: var(--c-green-soft);
  border: 1px solid rgba(22, 163, 74, 0.15);
}

.streak-flame {
  font-size: 1.1rem;
}

.streak-n {
  font-family: var(--f-display);
  font-size: 1.3rem;
  font-weight: 400;
  color: var(--c-green);
  line-height: 1;
}

.streak-l {
  font-size: 0.62rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--c-green);
}

.dash-kpis {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.dash-kpi {
  padding: 14px 16px;
  border-radius: 12px;
  background: var(--c-50);
  border: 1px solid var(--border);
}

.dash-kpi-primary {
  background: var(--c-black);
  border-color: var(--c-black);
}

.dash-kpi-primary .kpi-label {
  color: rgba(255, 255, 255, 0.5);
}

.kpi-val {
  font-family: var(--f-display);
  font-size: 1.6rem;
  font-weight: 400;
  color: var(--c-black);
  line-height: 1;
  letter-spacing: -0.02em;
}

.kpi-val span {
  font-size: 0.9rem;
  color: var(--c-400);
  font-family: var(--f-body);
}

.dash-kpi-primary .kpi-val {
  color: var(--c-white);
}

.dash-kpi-primary .kpi-val span {
  color: rgba(255, 255, 255, 0.45);
}

.kpi-delta {
  font-size: 0.7rem;
  font-weight: 600;
  margin-top: 4px;
}

.kpi-delta.up {
  color: var(--c-green);
}

.kpi-delta.neutral {
  color: var(--c-400);
}

.dash-row-2 {
  display: grid;
  grid-template-columns: 1fr 240px;
  gap: 16px;
  flex: 1;
}

.dash-chart-area,
.dash-actions {
  background: var(--c-50);
  border-radius: 12px;
  border: 1px solid var(--border);
  padding: 16px;
}

.dash-chart-area {
  display: flex;
  flex-direction: column;
}

.chart-label,
.dash-actions-label {
  margin-bottom: 12px;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  flex: 1;
}

.chart-bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  height: 100%;
  justify-content: flex-end;
}

.chart-bar {
  width: 100%;
  border-radius: 5px 5px 0 0;
  background: var(--c-100);
  transition: background 0.3s;
  min-height: 6px;
}

.chart-bar.today {
  background: var(--c-black);
}

.chart-day {
  font-size: 0.62rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--c-300);
}

.dash-action-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--c-700);
}

.dash-action-item:last-child {
  border-bottom: none;
}

.dash-action-item.done {
  color: var(--c-300);
}

.action-check {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1.5px solid var(--c-100);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.action-check.done {
  background: var(--c-green);
  border-color: var(--c-green);
}

/* ANNOTATION CARDS */
.anno {
  position: absolute;
  display: flex;
  align-items: center;
  z-index: 3;
}

.anno-1 {
  bottom: 60px;
  left: -20px;
  animation: anno-float-1 5s ease-in-out infinite;
}

.anno-2 {
  top: 80px;
  right: 20px;
  animation: anno-float-2 5s ease-in-out infinite 2.5s;
}

@keyframes anno-float-1 {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-10px);
  }
}

@keyframes anno-float-2 {
  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-8px);
  }
}

.anno-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--c-green-mid);
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.25);
  flex-shrink: 0;
  margin-right: -1px;
  z-index: 1;
}

.anno-card {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-radius: 12px;
  background: var(--c-white);
  border: 1px solid var(--border-mid);
  box-shadow: var(--shadow-md);
}

.anno-icon {
  font-size: 1.1rem;
}

.anno-content strong {
  display: block;
  font-family: var(--f-body);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--c-black);
}

.anno-content span {
  font-size: 0.7rem;
  color: var(--c-400);
}

/* PROOF BAR */
.proof-bar {
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  padding: 22px 0;
  background: var(--c-white);
}

.proof-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
  display: flex;
  align-items: center;
  gap: 32px;
  flex-wrap: wrap;
}

.proof-label {
  font-family: var(--f-body);
  font-size: 0.76rem;
  font-weight: 500;
  color: var(--c-300);
  white-space: nowrap;
}

.proof-logos {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.proof-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--c-400);
  transition: color 0.2s;
}

.proof-logo:hover {
  color: var(--c-700);
}

.proof-logo span {
  font-family: var(--f-body);
  font-size: 0.84rem;
  font-weight: 600;
  color: inherit;
}

.proof-div {
  width: 1px;
  height: 20px;
  background: var(--c-100);
}

/* VALUE */
.value-section {
  padding: var(--section-v) 0 0;
  background: var(--c-white);
}

.value-wrap {
  max-width: 1280px;
  margin: 0 auto clamp(64px, 8vw, 100px);
  padding: 0 40px;
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: clamp(48px, 6vw, 100px);
  align-items: start;
}

.value-h2 {
  max-width: 10ch;
  margin-bottom: 0;
}

.value-lede {
  font-size: clamp(1rem, 1.2vw, 1.14rem);
  color: var(--c-700);
  margin-bottom: 36px;
  max-width: 32rem;
  line-height: 1.7;
}

.value-cards {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.vcard {
  display: flex;
  gap: 24px;
  padding: 24px 0;
  border-bottom: 1px solid var(--border);
  transition: all 0.2s;
}

.vcard:first-child {
  border-top: 1px solid var(--border);
}

.vcard:hover {
  background: var(--c-50);
  margin: 0 -20px;
  padding-left: 20px;
  padding-right: 20px;
  border-radius: 12px;
  border-color: transparent;
}

.vcard-number {
  font-family: var(--f-mono);
  font-size: 0.68rem;
  font-weight: 500;
  color: var(--c-300);
  letter-spacing: 0.06em;
  padding-top: 3px;
  flex-shrink: 0;
  width: 28px;
}

.vcard-content h3 {
  font-size: 1rem;
  font-weight: 600;
  font-family: var(--f-body);
  color: var(--c-black);
  margin-bottom: 6px;
  letter-spacing: -0.01em;
}

.vcard-content p {
  font-size: 0.88rem;
  margin: 0;
}

.value-fullbleed {
  position: relative;
  height: clamp(300px, 35vw, 480px);
  overflow: hidden;
}

.value-fullbleed img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 30%;
}

.fullbleed-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(10, 11, 10, 0.72) 0%, rgba(10, 11, 10, 0.42) 100%);
}

.fullbleed-stats {
  position: absolute;
  inset: 0;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
  display: flex;
  align-items: center;
  left: 0;
  right: 0;
}

.fstat {
  flex: 1;
  padding: 0 32px;
}

.fstat:first-child {
  padding-left: 0;
}

.fstat-n {
  font-family: var(--f-display);
  font-size: clamp(2.5rem, 4.5vw, 4.8rem);
  font-weight: 300;
  color: var(--c-white);
  line-height: 1;
  letter-spacing: -0.04em;
  margin-bottom: 8px;
}

.fstat-n span {
  font-size: 0.5em;
  vertical-align: super;
}

.fstat-l {
  font-family: var(--f-body);
  font-size: 0.82rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.55);
  line-height: 1.45;
  max-width: 130px;
}

.fstat-sep {
  width: 1px;
  height: 60px;
  background: rgba(255, 255, 255, 0.14);
  flex-shrink: 0;
}

/* PILLARS */
.pillars-section {
  padding: var(--section-v) 0;
  background: var(--c-50);
  border-top: 1px solid var(--border);
}

.pillars-wrap {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
}

.pillars-head {
  max-width: 48rem;
  margin-bottom: 60px;
}

.pillars-head h2 {
  margin-bottom: 16px;
}

.pillars-head p {
  font-size: 1.02rem;
  max-width: 34rem;
}

.pillars-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.pillar-item {
  border-radius: var(--r-xl);
  overflow: hidden;
  background: var(--c-white);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s;
}

.pillar-item:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-lg);
  border-color: var(--border-mid);
}

.pillar-img {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.pillar-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
  filter: brightness(0.88);
}

.pillar-item:hover .pillar-img img {
  transform: scale(1.05);
}

.pillar-img-cover {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, transparent 40%, rgba(255, 255, 255, 0.15));
}

.pillar-body {
  padding: 22px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.pillar-index {
  font-family: var(--f-mono);
  font-size: 0.62rem;
  font-weight: 500;
  color: var(--c-300);
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}

.pillar-chip {
  display: inline-flex;
  height: 22px;
  padding: 0 9px;
  border-radius: 999px;
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  align-items: center;
  margin-bottom: 14px;
  align-self: flex-start;
}

.pillar-chip-green {
  background: var(--c-green-pale);
  color: var(--c-green);
}

.pillar-chip-blue {
  background: var(--c-blue-soft);
  color: #1d4ed8;
}

.pillar-chip-indigo {
  background: var(--c-indigo-soft);
  color: #4338ca;
}

.pillar-chip-amber {
  background: var(--c-amber-soft);
  color: #b45309;
}

.pillar-body h3 {
  margin-bottom: 10px;
  font-size: 1.08rem;
  font-weight: 500;
}

.pillar-body p {
  font-size: 0.86rem;
  flex: 1;
  margin-bottom: 16px;
}

.pillar-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: auto;
}

.pillar-tags span {
  font-size: 0.68rem;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 999px;
  background: var(--c-50);
  border: 1px solid var(--border);
  color: var(--c-500);
}

/* PROCESS */
.process-section {
  padding: var(--section-v) 0;
  background: var(--c-white);
  border-top: 1px solid var(--border);
}

.process-wrap {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
}

.process-head {
  margin-bottom: 56px;
  max-width: 26rem;
}

.process-head h2 {
  margin-bottom: 0;
}

.process-steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  margin-bottom: 52px;
}

.pstep-media {
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  aspect-ratio: 16 / 10;
  margin-bottom: 24px;
  border: 1px solid var(--border);
}

.pstep-media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.82);
  transition: transform 0.4s ease;
}

.process-step:hover .pstep-media img {
  transform: scale(1.04);
}

.pstep-num {
  position: absolute;
  top: 14px;
  left: 14px;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--f-mono);
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--c-black);
  backdrop-filter: blur(4px);
}

.pstep-body h3 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  font-weight: 500;
}

.pstep-body p {
  font-size: 0.9rem;
}

.process-cta-nudge {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-top: 8px;
  border-top: 1px solid var(--border);
}

.btn-process {
  height: 48px;
  padding: 0 24px;
  display: inline-flex;
  align-items: center;
  font-family: var(--f-body);
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--c-white);
  background: var(--c-black);
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-process:hover {
  background: var(--c-800);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.process-cta-nudge span {
  font-family: var(--f-body);
  font-size: 0.82rem;
  color: var(--c-400);
}

/* INSIGHTS / WELLBEING */
.research-section {
  padding: var(--section-v) 0;
  background:
    radial-gradient(circle at top right, rgba(67, 169, 119, 0.08), transparent 28rem),
    radial-gradient(circle at bottom left, rgba(255, 231, 168, 0.05), transparent 24rem),
    #111715;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
}

.research-wrap {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 80px;
  align-items: start;
}

.research-head h2 {
  color: var(--c-white);
  margin-bottom: 16px;
}

.research-head p {
  color: rgba(255, 255, 255, 0.72);
  margin-bottom: 36px;
}

.rtabs {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rtab {
  height: 46px;
  padding: 0 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.09);
  background: transparent;
  font-family: var(--f-body);
  font-size: 0.88rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.45);
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
}

.rtab:hover {
  border-color: rgba(255, 255, 255, 0.18);
  color: rgba(255, 255, 255, 0.75);
  background: rgba(255, 255, 255, 0.04);
}

.rtab.active {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: var(--c-white);
  font-weight: 800;
}

.rpanel-loading {
  display: flex;
  justify-content: center;
  padding: 60px;
}

.rspinner {
  width: 28px;
  height: 28px;
  border: 2px solid rgba(255, 255, 255, 0.12);
  border-top-color: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.rpanel-err {
  color: #f87171;
  font-size: 0.88rem;
}

.rpane {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.rpane-main {
  padding: 32px;
  border-radius: 30px;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.18);
}

.rpane-heading,
.children-grid-head,
.simple-sleep-head,
.simple-activity-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 28px;
}

.rpane-heading h3,
.children-grid-head h3,
.simple-sleep-head h3,
.simple-activity-head h3 {
  color: var(--c-white);
  font-size: 1.35rem;
  margin-bottom: 10px;
}

.children-grid-head p,
.simple-sleep-head p,
.simple-activity-head p {
  color: rgba(255, 255, 255, 0.64);
  font-size: 0.95rem;
  line-height: 1.65;
  margin: 0;
  max-width: 560px;
}

.rpane-badge,
.children-grid-badge,
.simple-sleep-badge,
.simple-activity-badge {
  display: inline-flex;
  align-items: center;
  min-height: 36px;
  padding: 0 16px;
  border-radius: 999px;
  font-size: 0.84rem;
  font-weight: 900;
  white-space: nowrap;
}

.children-grid-badge,
.rpane-badge {
  background: rgba(34, 197, 94, 0.16);
  border: 1px solid rgba(34, 197, 94, 0.28);
  color: #6ee7a3;
}

.simple-sleep-badge,
.rpane-badge-b {
  background: rgba(99, 102, 241, 0.18);
  border: 1px solid rgba(99, 102, 241, 0.28);
  color: #c7d2fe;
}

.simple-activity-badge,
.rpane-badge-c {
  background: rgba(251, 191, 36, 0.16);
  border: 1px solid rgba(251, 191, 36, 0.28);
  color: #facc15;
}

.rpane-notes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.rnote {
  padding: 20px 22px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.09);
}

.rnote-head {
  font-family: var(--f-body);
  font-size: 0.72rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: rgba(255, 255, 255, 0.82);
  margin-bottom: 8px;
}

.rnote p {
  color: rgba(255, 255, 255, 0.62);
  font-size: 0.88rem;
  line-height: 1.65;
  margin: 0;
}

/* BODY BALANCE CHART */
.children-grid-wrap {
  display: grid;
  grid-template-columns: 1fr 220px;
  gap: 28px;
  align-items: start;
}

.children-grid {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 8px;
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.09);
}

.child-square {
  aspect-ratio: 1;
  min-width: 0;
  border-radius: 10px;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.08);
}

.child-underweight,
.legend-underweight {
  background: #93c5fd;
}

.child-normal,
.legend-normal {
  background: #4ade80;
}

.child-overweight,
.legend-overweight {
  background: #fbbf24;
}

.child-obese,
.legend-obese {
  background: #fb7185;
}

.children-legend {
  display: grid;
  gap: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.09);
}

.legend-dot {
  width: 16px;
  height: 16px;
  border-radius: 5px;
  flex-shrink: 0;
}

.legend-item strong {
  display: block;
  color: rgba(255, 255, 255, 0.92);
  font-size: 0.92rem;
  margin-bottom: 3px;
}

.legend-item small {
  display: block;
  color: rgba(255, 255, 255, 0.58);
  font-size: 0.78rem;
  line-height: 1.35;
}

/* SLEEP SNAPSHOT */
.sleep-simple-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 18px;
}

.sleep-big-card {
  min-height: 190px;
  padding: 24px;
  border-radius: 24px;
  background: #ffffff;
  border: 1px solid rgba(20, 53, 40, 0.08);
  box-shadow: 0 12px 28px rgba(20, 53, 40, 0.06);
}

.sleep-target-card {
  background: linear-gradient(145deg, #eef2ff, #ffffff);
}

.sleep-card-icon {
  width: 42px;
  height: 42px;
  border-radius: 16px;
  background: #f0fdf4;
  display: grid;
  place-items: center;
  font-size: 1.25rem;
  margin-bottom: 18px;
}

.sleep-big-card small,
.activity-focus-content small {
  display: block;
  font-size: 0.74rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}

.sleep-big-card small {
  color: #6b7c73;
}

.sleep-big-card strong {
  display: block;
  color: #143528;
  font-family: var(--f-display);
  font-size: 2rem;
  line-height: 1.05;
  margin-bottom: 10px;
}

.sleep-big-card p {
  color: #66766e;
  font-size: 0.9rem;
  line-height: 1.55;
  margin: 0;
}

.sleep-takeaway {
  padding: 20px 22px;
  border-radius: 22px;
  background: #f6fbf7;
  border: 1px solid rgba(20, 53, 40, 0.08);
}

.sleep-takeaway strong {
  display: block;
  color: #15803d;
  font-size: 0.78rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 8px;
}

.sleep-takeaway p {
  color: #52665c;
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.65;
}

/* ACTIVITY SNAPSHOT */
.activity-focus-card {
  display: flex;
  align-items: center;
  gap: 22px;
  padding: 30px;
  border-radius: 28px;
  background: linear-gradient(145deg, #fff7ed, #ffffff);
  border: 1px solid rgba(245, 158, 11, 0.18);
  box-shadow: 0 14px 34px rgba(20, 53, 40, 0.07);
  margin-bottom: 18px;
}

.activity-focus-icon {
  width: 72px;
  height: 72px;
  border-radius: 24px;
  display: grid;
  place-items: center;
  background: #fef3c7;
  font-size: 2rem;
  flex-shrink: 0;
}

.activity-focus-content small {
  color: #b45309;
}

.activity-focus-content strong {
  display: block;
  color: #143528;
  font-family: var(--f-display);
  font-size: clamp(2.2rem, 4vw, 3.4rem);
  line-height: 1;
  margin-bottom: 10px;
}

.activity-focus-content p {
  color: #66766e;
  font-size: 1rem;
  margin: 0;
}

.activity-parent-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.activity-summary-item {
  padding: 22px;
  border-radius: 22px;
  background: #f6fbf7;
  border: 1px solid rgba(20, 53, 40, 0.08);
}

.activity-summary-item span {
  display: block;
  color: #15803d;
  font-size: 0.72rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 8px;
}

.activity-summary-item p {
  color: #52665c;
  font-size: 0.92rem;
  line-height: 1.65;
  margin: 0;
}

/* PATHWAYS */
.pathways-wrap {
  display: grid;
  grid-template-columns: 1fr 1fr;
}


.pathway {
  display: flex;
  flex-direction: column;
  min-height: 390px;
}

.pathway-img-col {
  height: 220px;
  flex: none;
  overflow: hidden;
}


.pathway:hover .pathway-img-col img {
  transform: scale(1.04);
}

.pathway-body {
  padding: 44px 48px;
}

.pathway-eyebrow {
  display: inline-flex;
  height: 26px;
  padding: 0 11px;
  border-radius: 999px;
  font-family: var(--f-body);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  align-items: center;
  margin-bottom: 18px;
  border: 1px solid var(--border-mid);
  color: var(--c-500);
  background: transparent;
}

.pathway-eyebrow-green {
  border-color: rgba(34, 197, 94, 0.35);
  color: #22c55e;
  background: rgba(34, 197, 94, 0.08);
}

.pathway-body h3 {
  margin-bottom: 14px;
  font-size: clamp(1.3rem, 2vw, 1.8rem);
}

.pathway-body p {
  margin-bottom: 24px;
}

.pathway-body-dark h3 {
  color: var(--c-white);
}

.pathway-body-dark p {
  color: rgba(255, 255, 255, 0.5);
}

.pathway-list {
  list-style: none;
  padding: 0;
  margin: 0 0 28px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.pathway-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--f-body);
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--c-500);
}

.pathway-list li::before {
  content: '';
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--c-300);
  flex-shrink: 0;
}

.pathway-list-dark li {
  color: rgba(255, 255, 255, 0.45);
}

.pathway-list-dark li::before {
  background: rgba(255, 255, 255, 0.2);
}

.pathway-btn-dark,
.pathway-btn-green {
  display: inline-flex;
  align-items: center;
  height: 48px;
  padding: 0 22px;
  border-radius: 10px;
  font-family: var(--f-body);
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.pathway-btn-dark {
  background: var(--c-black);
  color: var(--c-white);
}

.pathway-btn-dark:hover {
  background: var(--c-800);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.pathway-btn-green {
  background: var(--c-green);
  color: var(--c-white);
}

.pathway-btn-green:hover {
  background: #15803d;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(22, 163, 74, 0.35);
}

/* TESTIMONIALS */
.testimonials-section {
  padding: var(--section-v) 0;
  background: var(--c-50);
  border-top: 1px solid var(--border);
}

.testimonials-wrap {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
}

.test-head {
  margin-bottom: 52px;
  max-width: 20rem;
}

.testimonials-layout {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 20px;
}

.testimonials-col-a,
.testimonials-col-b {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tq {
  margin: 0;
  padding: 30px;
  border-radius: var(--r-xl);
  background: var(--c-white);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: box-shadow 0.25s, transform 0.25s;
}

.tq:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
}

.tq-lg {
  flex: 1;
  background: linear-gradient(145deg, #f0fdf4, #dcfce7);
  border-color: rgba(22, 163, 74, 0.14);
}

.tq-stars {
  font-size: 0.8rem;
  color: #f59e0b;
  letter-spacing: 2px;
}

.tq p {
  font-family: var(--f-display);
  font-style: italic;
  font-size: clamp(0.98rem, 1.2vw, 1.15rem);
  color: var(--c-black);
  line-height: 1.62;
  flex: 1;
  margin: 0;
}

.tq footer {
  display: flex;
  align-items: center;
  gap: 12px;
  border-top: 1px solid var(--border);
  padding-top: 16px;
  margin-top: auto;
}

.tq-av {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--f-body);
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--c-700);
  flex-shrink: 0;
}

.tq footer strong {
  display: block;
  font-family: var(--f-body);
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--c-black);
}

.tq footer span {
  font-size: 0.76rem;
  color: var(--c-400);
}

/* FINAL CTA */
.final-cta {
  position: relative;
  overflow: hidden;
}

.fcta-inner {
  position: relative;
  min-height: clamp(400px, 45vw, 560px);
  display: flex;
  align-items: center;
}

.fcta-bg {
  position: absolute;
  inset: 0;
}

.fcta-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 40%;
}

.fcta-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(10, 11, 10, 0.88), rgba(10, 11, 10, 0.72) 60%, rgba(4, 60, 30, 0.65));
}

.fcta-content {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 80px 40px;
  width: 100%;
}

.fcta-h2 {
  color: var(--c-white);
  margin-bottom: 20px;
  max-width: 16ch;
}

.fcta-content p {
  color: rgba(255, 255, 255, 0.55);
  font-size: 1rem;
  margin-bottom: 36px;
  max-width: 30rem;
}

.fcta-btns {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.fcta-btn-primary,
.fcta-btn-secondary {
  display: inline-flex;
  align-items: center;
  height: 52px;
  padding: 0 28px;
  border-radius: 12px;
  font-family: var(--f-body);
  font-size: 0.94rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.22s;
}

.fcta-btn-primary {
  background: var(--c-white);
  color: var(--c-black);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.fcta-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.fcta-btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(8px);
}

.fcta-btn-secondary:hover {
  background: rgba(255, 255, 255, 0.18);
  color: var(--c-white);
  transform: translateY(-2px);
}

/* FOOTER */
.footer {
  background: var(--c-black);
  padding: 60px 0 0;
}

.footer-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px 48px;
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr 1fr;
  gap: 48px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.footer .logo {
  color: var(--c-white);
  margin-bottom: 14px;
  display: flex;
}

.footer .logo-icon {
  color: rgba(255, 255, 255, 0.8);
}

.footer-tagline {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.3);
  line-height: 1.6;
  margin: 0;
}

.footer-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-col-head {
  font-family: var(--f-body);
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: rgba(255, 255, 255, 0.35);
  margin-bottom: 4px;
}

.footer-col a {
  font-family: var(--f-body);
  font-size: 0.86rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  transition: color 0.18s;
}

.footer-col a:hover {
  color: rgba(255, 255, 255, 0.9);
}

.footer-bottom {
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px 40px;
}

.footer-bottom p {
  font-size: 0.76rem;
  color: rgba(255, 255, 255, 0.2);
  margin: 0;
}

/* RESPONSIVE */
@media (max-width: 1100px) {
  .pillars-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .research-wrap {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .rtabs {
    flex-direction: row;
  }

  .rtab {
    flex: 1;
  }

  .fullbleed-stats {
    flex-wrap: wrap;
    padding: 20px 40px;
  }

  .fstat {
    flex: 0 0 50%;
    padding: 16px 0;
  }

  .fstat-sep {
    display: none;
  }

  .footer-inner {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 1000px) {
  .sleep-simple-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .hero-sub-row {
    flex-direction: column;
    gap: 28px;
  }

  .value-wrap {
    grid-template-columns: 1fr;
  }

  .pathways-wrap {
    grid-template-columns: 1fr;
  }

  .process-steps {
    grid-template-columns: 1fr;
  }

  .testimonials-layout {
    grid-template-columns: 1fr;
  }

  .children-grid-head,
  .simple-sleep-head,
  .simple-activity-head {
    flex-direction: column;
  }

  .children-grid-wrap,
  .rpane-notes,
  .activity-parent-summary {
    grid-template-columns: 1fr;
  }

  .activity-focus-card {
    align-items: flex-start;
    flex-direction: column;
  }

  .children-grid-badge,
  .simple-sleep-badge,
  .simple-activity-badge,
  .rpane-badge {
    white-space: normal;
  }

  .proof-inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-inner,
  .hero-wrap,
  .hero-product,
  .value-wrap,
  .pillars-wrap,
  .process-wrap,
  .testimonials-wrap,
  .fcta-content,
  .research-wrap {
    padding-left: 24px;
    padding-right: 24px;
  }

  .fullbleed-stats {
    padding: 20px 24px;
  }

  .footer-inner,
  .footer-bottom {
    padding-left: 24px;
    padding-right: 24px;
  }

  .fcta-content {
    padding: 60px 24px;
  }
}

@media (max-width: 700px) {
  .nav,
  .nav-link {
    display: none;
  }

  .trust-strip {
    flex-wrap: wrap;
    gap: 10px;
  }

  .trust-sep {
    display: none;
  }

  .pillars-grid {
    grid-template-columns: 1fr;
  }

  .dash-kpis {
    grid-template-columns: 1fr 1fr;
  }

  .dash-row-2 {
    grid-template-columns: 1fr;
  }

  .product-screen {
    height: auto;
  }

  .footer-inner {
    grid-template-columns: 1fr;
  }

  .fstat {
    flex: 0 0 100%;
  }

  h2 {
    font-size: clamp(2rem, 8vw, 2.8rem);
  }

  .hl-serif {
    font-size: clamp(2.8rem, 11vw, 4rem);
  }

  .hl-em {
    font-size: clamp(2rem, 9vw, 3rem);
  }

  .hl-thin {
    font-size: clamp(1.1rem, 5vw, 1.8rem);
  }

  .hero-actions {
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
  }

  .btn-hero,
  .btn-ghost-hero {
    width: 100%;
    justify-content: center;
  }

  .proof-logos {
    flex-wrap: wrap;
    gap: 16px;
  }

  .pathway-body {
    padding: 28px 24px;
  }

  .anno {
    display: none;
  }
}

@media (max-width: 600px) {
  .children-grid {
    gap: 5px;
    padding: 14px;
  }

  .child-square {
    border-radius: 6px;
  }
}
</style>