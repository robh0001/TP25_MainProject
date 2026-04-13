<template>
    <main>
      <section class="hero split-bg">
        <div class="container">
          <div class="hero-grid">
            <div class="hero-text">
              <p class="eyebrow">Nurturing healthy kids, one tiny win at a time.</p>
              <h1>
                Practical support for<br />
                <span>parents and children.</span>
              </h1>
              <p class="hero-subtext">
                HealthySteps helps families with children aged 5-12 build better nutrition, movement,
                sleep, and routine habits with step-by-step guidance.
              </p>
            </div>
  
            <div class="hero-choices">
              <article class="choice-card parent-card">
                <div class="choice-icon coral">👨‍👩‍👧</div>
                <h3>I'm a parent</h3>
                <p>
                  Navigate family health with warmth and realism. Get practical tools that fit real
                  family life—no judgment, just support.
                </p>
                <ul>
                  <li>Family overview dashboard</li>
                  <li>Daily snapshot cards with personalised tips</li>
                  <li>Gentle alerts when you're overloading changes</li>
                </ul>
                <RouterLink to="/parent-quiz" class="btn btn-coral full link-btn">
                  Start as a Parent
                </RouterLink>
                <RouterLink to="/parent-dashboard" class="btn btn-outline-neutral full link-btn">
                  View Parent Dashboard
                </RouterLink>
              </article>
  
              <article class="choice-card teen-card">
                <div class="choice-icon blue">🚀</div>
                <h3>I'm a child</h3>
                <p>
                  Your journey, your pace. Complete fun daily missions, earn badges, and build healthy
                  habits with support from home.
                </p>
                <ul>
                  <li>Earn XP and badges for trying</li>
                  <li>Fun mission board with rewards</li>
                  <li>Progress that celebrates effort</li>
                </ul>
                <RouterLink to="/young-person-dashboard" class="btn btn-blue full link-btn">
                  Start as a Child
                </RouterLink>
              </article>
            </div>
          </div>
        </div>
      </section>

      <section class="container journey-strip">
        <div class="journey-pill">Home</div>
        <div class="journey-arrow">→</div>
        <div class="journey-pill">Choose Parent or Child</div>
        <div class="journey-arrow">→</div>
        <div class="journey-pill">Parent Quiz</div>
        <div class="journey-arrow">→</div>
        <div class="journey-pill">Personalized Dashboard</div>
      </section>
  
      <section class="container stats-banner">
        <div class="stats-icon">❤</div>
        <div>
          <h3>You're not alone</h3>
          <p>
            <strong>1 in 4 Australian children</strong> carry excess weight. This isn't about
            blame—it's about supporting families with practical, evidence-based tools that work in
            real life.
          </p>
          <div class="stats-links">
            <a href="#">Raising Children Network</a>
            <a href="#">Heart Foundation</a>
          </div>
        </div>
      </section>
  
      <section id="resources" class="tools-section container section-gap">
        <SectionTitle
          title="Start right now. No sign-up needed."
          description="Every core tool works instantly. Create an account later to save progress and unlock your dashboard."
        />
  
        <div class="tool-grid three">
          <ToolCard
            v-for="tool in tools"
            :key="tool.title"
            :icon="tool.icon"
            :title="tool.title"
            :description="tool.description"
            :link-text="tool.linkText"
            :icon-class="tool.className"
          />
        </div>
      </section>
  
      <section class="tip-section split-bg-alt section-gap">
        <div class="container">
          <SectionTitle
            badge="Updated every Monday"
            badge-class="yellow"
            title="This week's parent tip"
            description="Real advice from Australian families like yours"
          />
  
          <article class="tip-card">
            <div class="tip-header">
              <div class="avatar">S</div>
              <div>
                <h4>Sarah from Melbourne</h4>
                <p>Parent of two, ages 8 &amp; 11</p>
              </div>
            </div>
  
            <blockquote>
              “Instead of banning screens before dinner, we started a 10-minute dance party rule.
              The kids pick the songs, we all move around like idiots, and somehow they're less
              grumpy about eating veggies afterwards. It's chaotic but it works!”
            </blockquote>
  
            <div class="tip-footer">
              <span>❤ 247 families liked this</span>
              <span>💬 32</span>
              <button class="btn btn-coral">Share your tip</button>
            </div>
          </article>
        </div>
      </section>
  
      <section id="parent-child-paths" class="container section-gap">
        <SectionTitle
          title="Get your personalized starting point"
          description="60-second quiz. No sign-up. Instant action plan tailored to your family."
        />
  
        <div class="quiz-grid">
          <article class="quiz-card parent-quiz">
            <h3>Parent Quiz</h3>
            <ul>
              <li>Your child's age &amp; stage</li>
              <li>Top three health concerns</li>
              <li>Biggest daily struggle</li>
              <li>What you've already tried</li>
            </ul>
            <RouterLink to="/parent-quiz" class="btn btn-coral full link-btn">
              Start Parent Quiz
            </RouterLink>
          </article>
  
          <article class="quiz-card teen-quiz">
            <h3>Child Missions</h3>
            <ul>
              <li>Fun missions for energy and movement</li>
              <li>Badges for trying new healthy habits</li>
              <li>Simple wins children can complete daily</li>
              <li>Colorful progress moments</li>
            </ul>
            <RouterLink to="/young-person-dashboard" class="btn btn-blue full link-btn">
              Open Child Dashboard
            </RouterLink>
          </article>
        </div>
  
        <div class="quiz-output">
          <p>Quiz output example:</p>
          <div class="output-pill">
            “Your biggest win this week could be here’s your first action card—replacing afternoon
            chips with fruit &amp; yogurt.”
          </div>
        </div>
      </section>
  
      <section class="container section-gap">
        <SectionTitle
          title="Two experiences, one goal"
          description="Different language, different tools—both designed to support healthy habits at your own pace."
        />
  
        <div class="experience-grid two-columns">
          <article class="experience-card coral-panel">
            <div class="panel-header">
              <h3>❤ Parent Pulse</h3>
              <p>Warm, realistic, zero judgment. Small steps for real family life.</p>
            </div>
            <div class="snapshot-card">
              <strong>Daily Snapshot Card</strong>
              <p>
                “Your child’s energy might be low today based on last night’s sleep log—there are 2
                quick after-school snack swaps.”
              </p>
            </div>
            <div class="panel-placeholder"></div>
          </article>
  
          <article class="experience-card blue-panel">
            <div class="panel-header">
              <h3>⚡ Teen Track</h3>
              <p>Private, motivating, and built around progress—not perfection.</p>
            </div>
            <div class="teen-progress">
              <div class="xp-ring">+120 XP</div>
              <div>
                <strong>Current streak</strong>
                <p>3 days of breakfast before school</p>
              </div>
            </div>
            <div class="badge-row">
              <span class="tiny-badge">Tried a new fruit</span>
              <span class="tiny-badge">Hydration streak</span>
              <span class="tiny-badge">Walked after school</span>
            </div>
          </article>
        </div>
      </section>
  
      <section id="how-it-works" class="how-section split-bg section-gap">
        <div class="container">
          <SectionTitle
            title="How It Works"
            description="Three simple steps to transform your family’s wellness journey"
          />
  
          <div class="steps-grid">
            <StepCard
              v-for="step in steps"
              :key="step.title"
              :title="step.title"
              :description="step.description"
            />
          </div>
        </div>
      </section>
  
      <section class="container section-gap">
        <div class="cta-banner">
          <h2>Ready to Start Your Family Journey?</h2>
          <p>
            Join thousands of families building healthier habits together with our conflict-free
            approach.
          </p>
          <div class="cta-actions">
            <RouterLink to="/parent-dashboard" class="btn btn-light link-btn">
              Open Parent Dashboard
            </RouterLink>
            <RouterLink to="/parent-quiz" class="btn btn-light link-btn">
              Get Started Free
            </RouterLink>
            <a href="#" class="btn btn-outline-light link-btn">Watch Demo</a>
          </div>
        </div>
      </section>
    </main>
  </template>

  <script setup>
  import { RouterLink } from 'vue-router'
  import SectionTitle from '../components/SectionTitle.vue'
  import ToolCard from '../components/ToolCard.vue'
  import StepCard from '../components/StepCard.vue'
  
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