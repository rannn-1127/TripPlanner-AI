<template>
  <main class="about-page">
    <div class="about-container">

      <!-- ================= Hero ================= -->
      <section class="hero-section">

        <div class="hero-orb orb-one"></div>
        <div class="hero-orb orb-two"></div>

        <div class="hero-grid"></div>

        <div class="hero-content">

          <div class="hero-badge">
            <span class="badge-dot"></span>
            AI TRAVEL PLANNER
          </div>

          <h1>
            TripPlanner
            <span>-AI</span>
          </h1>

          <p class="hero-subtitle">
            让 AI 帮你规划每一次旅行
          </p>

          <p class="hero-description">
            基于 LangChain Agent、RAG 与 DeepSeek 构建的
            智能旅游行程规划系统，为旅行提供更加个性化、
            有依据的行程方案。
          </p>

          <div class="hero-actions">

            <button
              class="primary-button"
              @click="$router.push('/')"
            >
              <span>开始规划行程</span>
              <span class="button-arrow">→</span>
            </button>

            <button
              class="github-button"
              @click="openGithub"
            >
              <span class="github-symbol">★</span>
              <span>GitHub</span>
              <span class="button-arrow">↗</span>
            </button>

          </div>

        </div>

        <!-- Floating particles -->
        <div class="particle particle-one"></div>
        <div class="particle particle-two"></div>
        <div class="particle particle-three"></div>
        <div class="particle particle-four"></div>

      </section>


      <!-- ================= Stats ================= -->
      <section class="stats-section">

        <div
          v-for="stat in stats"
          :key="stat.label"
          class="stat-card"
        >
          <div class="stat-number">
            {{ stat.value }}
          </div>

          <div class="stat-label">
            {{ stat.label }}
          </div>
        </div>

      </section>


      <!-- ================= 项目介绍 ================= -->
      <section class="content-section reveal">

        <div class="section-heading">

          <div class="section-index">
            01
          </div>

          <div>
            <h2>项目介绍</h2>
            <p>让旅行规划从繁琐搜索变得更加简单</p>
          </div>

        </div>


        <div class="intro-card">

          <div class="intro-visual">

            <div class="visual-circle circle-one"></div>
            <div class="visual-circle circle-two"></div>

            <div class="visual-icon">
              🗺️
            </div>

          </div>


          <div class="intro-content">

            <div class="intro-label">
              ABOUT THE PROJECT
            </div>

            <h3>
              一个真正面向旅行场景的
              <span>AI Agent</span>
            </h3>

            <p>
              TripPlanner-AI 是一个基于大语言模型与 RAG
              技术构建的智能旅游行程规划系统。
            </p>

            <p>
              用户可以上传目的地旅游资料，并输入旅行天数、
              兴趣偏好以及行程节奏。系统通过知识库检索相关资料，
              再结合 DeepSeek 大模型生成个性化旅游行程。
            </p>

            <div class="intro-tags">
              <span>AI Agent</span>
              <span>RAG</span>
              <span>Semantic Search</span>
              <span>Personalized Planning</span>
            </div>

          </div>

        </div>

      </section>


      <!-- ================= 核心功能 ================= -->
      <section class="content-section reveal">

        <div class="section-heading">

          <div class="section-index">
            02
          </div>

          <div>
            <h2>核心功能</h2>
            <p>从资料管理到行程生成的一站式体验</p>
          </div>

        </div>


        <div class="feature-grid">

          <div
            v-for="(feature, index) in features"
            :key="feature.title"
            class="feature-card"
            :class="`feature-delay-${index}`"
          >

            <div class="feature-glow"></div>

            <div class="feature-top">

              <div class="feature-icon">
                {{ feature.icon }}
              </div>

              <span class="feature-number">
                0{{ index + 1 }}
              </span>

            </div>

            <h3>
              {{ feature.title }}
            </h3>

            <p>
              {{ feature.description }}
            </p>

            <div class="feature-line"></div>

          </div>

        </div>

      </section>


      <!-- ================= 技术栈 ================= -->
      <section class="content-section reveal">

        <div class="section-heading">

          <div class="section-index">
            03
          </div>

          <div>
            <h2>技术栈</h2>
            <p>项目核心技术与开发框架</p>
          </div>

        </div>


        <div class="tech-grid">

          <div
            v-for="group in techStack"
            :key="group.title"
            class="tech-card"
          >

            <div class="tech-header">

              <div class="tech-icon">
                {{ group.icon }}
              </div>

              <div>
                <span>TECHNOLOGY</span>
                <h3>
                  {{ group.title }}
                </h3>
              </div>

            </div>


            <div class="tech-tags">

              <span
                v-for="item in group.items"
                :key="item"
                class="tech-tag"
              >
                {{ item }}
              </span>

            </div>

          </div>

        </div>

      </section>


      <!-- ================= 系统流程 ================= -->
      <section class="content-section reveal">

        <div class="section-heading">

          <div class="section-index">
            04
          </div>

          <div>
            <h2>系统流程</h2>
            <p>从旅游资料到 AI 行程的完整流程</p>
          </div>

        </div>


        <div class="flow-wrapper">

          <div class="flow-line">
            <div class="flow-light"></div>
          </div>


          <div
            v-for="(step, index) in flowSteps"
            :key="step.title"
            class="flow-step"
          >

            <div class="flow-circle">
              <span>{{ step.icon }}</span>
            </div>

            <div class="flow-step-number">
              STEP {{ String(index + 1).padStart(2, "0") }}
            </div>

            <h3>
              {{ step.title }}
            </h3>

            <p>
              {{ step.description }}
            </p>

          </div>

        </div>

      </section>




      <!-- ================= GitHub ================= -->
      <section class="github-section reveal">

        <div class="github-background">
          <div class="github-glow"></div>
        </div>


        <div class="github-content">

          <div class="github-icon">
            ★
          </div>


          <div class="github-text">

            <div class="github-label">
              OPEN SOURCE
            </div>

            <h2>
              查看完整项目源码
            </h2>

            <p>
              欢迎访问 GitHub，了解项目实现细节，
              查看源码与项目文档。
            </p>

          </div>


          <button
            class="github-large-button"
            @click="openGithub"
          >
            <span>View on GitHub</span>
            <span>↗</span>
          </button>

        </div>

      </section>


      <!-- ================= Footer ================= -->
      <footer class="about-footer">

        <div class="footer-logo">
          ✦ TripPlanner-AI
        </div>

        <p>
          AI 驱动的智能旅游行程规划系统
        </p>

        <div class="footer-tech">
          Vue 3 · FastAPI · LangChain · RAG · DeepSeek
        </div>

      </footer>

    </div>
  </main>
</template>


<script setup>

const githubUrl =
  "https://github.com/rannn-1127/TripPlanner-AI"

const authorGithubUrl =
  "https://github.com/rannn-1127"


const stats = [

  {
    value: "6+",
    label: "核心功能"
  },

  {
    value: "4",
    label: "AI / RAG 技术模块"
  },

  {
    value: "4",
    label: "系统核心流程"
  },

  {
    value: "3",
    label: "行程导出格式"
  }

]


const features = [

  {
    icon: "🤖",
    title: "AI 智能规划",
    description:
      "根据旅行天数、兴趣偏好和行程节奏，自动生成个性化旅游行程。"
  },

  {
    icon: "📚",
    title: "旅游知识库",
    description:
      "支持 PDF、Word、TXT 等资料上传，构建目的地专属知识库。"
  },

  {
    icon: "🔍",
    title: "语义检索",
    description:
      "使用向量检索召回与问题相关的旅游资料，为 Agent 提供可靠上下文。"
  },

  {
    icon: "⚡",
    title: "Rerank",
    description:
      "使用 BGE Reranker 对召回结果进行二次排序，提高检索结果相关性。"
  },

  {
    icon: "📖",
    title: "资料引用",
    description:
      "景点与路线信息关联资料来源和页码，减少缺乏依据的信息生成。"
  },

  {
    icon: "📥",
    title: "多格式导出",
    description:
      "支持 Markdown、Word、Excel 多种格式，方便保存和使用旅游攻略。"
  }

]


const techStack = [

  {
    icon: "🎨",
    title: "Frontend",
    items: [
      "Vue 3",
      "Vite",
      "Vue Router",
      "JavaScript"
    ]
  },

  {
    icon: "⚙️",
    title: "Backend",
    items: [
      "Python",
      "FastAPI",
      "SSE",
      "Pydantic"
    ]
  },

  {
    icon: "🧠",
    title: "AI / Agent",
    items: [
      "LangChain",
      "Agent",
      "DeepSeek",
      "LLM"
    ]
  },

  {
    icon: "🔎",
    title: "RAG",
    items: [
      "ChromaDB",
      "BGE Embedding",
      "BGE Reranker",
      "Vector Search"
    ]
  }

]


const flowSteps = [

  {
    icon: "📄",
    title: "上传资料",
    description:
      "上传目的地旅游资料"
  },

  {
    icon: "🧩",
    title: "构建知识库",
    description:
      "文档分片、向量化并建立索引"
  },

  {
    icon: "🔍",
    title: "检索资料",
    description:
      "召回并重新排序相关内容"
  },

  {
    icon: "🤖",
    title: "生成行程",
    description:
      "结合用户偏好生成旅游攻略"
  }

]


function openGithub() {

  window.open(
    githubUrl,
    "_blank",
    "noopener,noreferrer"
  )

}


function openAuthorGithub() {

  window.open(
    authorGithubUrl,
    "_blank",
    "noopener,noreferrer"
  )

}

</script>


<style>

/* =====================================================
   Page
===================================================== */

.about-page {

  min-height: calc(100vh - 64px);

  padding: 42px 24px 70px;

  overflow: hidden;

}


.about-container {

  width: min(1160px, 100%);

  margin: 0 auto;

}


/* =====================================================
   Hero
===================================================== */

.hero-section {

  position: relative;

  min-height: 510px;

  display: flex;

  align-items: center;

  justify-content: center;

  overflow: hidden;

  border: 1px solid #e7e9f0;

  border-radius: 30px;

  background:
    radial-gradient(
      circle at 50% 35%,
      rgba(99, 102, 241, 0.14),
      transparent 35%
    ),
    linear-gradient(
      135deg,
      #ffffff 0%,
      #f8f9ff 100%
    );

  box-shadow:
    0 25px 70px rgba(31, 41, 55, 0.07);

  animation: heroEnter 0.8s ease both;

}


.hero-content {

  position: relative;

  z-index: 3;

  width: min(760px, 90%);

  text-align: center;

}


.hero-badge {

  display: inline-flex;

  align-items: center;

  gap: 8px;

  padding: 7px 14px;

  border: 1px solid #e1e3ff;

  border-radius: 999px;

  background: rgba(255, 255, 255, 0.8);

  color: #6366f1;

  font-size: 11px;

  font-weight: 700;

  letter-spacing: 1.6px;

}


.badge-dot {

  width: 6px;

  height: 6px;

  border-radius: 50%;

  background: #6366f1;

  box-shadow:
    0 0 0 4px rgba(99, 102, 241, 0.1);

  animation:
    pulseDot 1.8s ease-in-out infinite;

}


.hero-section h1 {

  margin: 22px 0 0;

  color: #20242c;

  font-size: clamp(48px, 7vw, 76px);

  line-height: 1;

  letter-spacing: -4px;

}


.hero-section h1 span {

  color: #6366f1;

}


.hero-subtitle {

  margin: 22px 0 0;

  color: #3c414b;

  font-size: 22px;

  font-weight: 600;

}


.hero-description {

  max-width: 690px;

  margin: 18px auto 0;

  color: #7b8190;

  font-size: 14px;

  line-height: 1.9;

}


.hero-actions {

  display: flex;

  justify-content: center;

  gap: 12px;

  margin-top: 32px;

}


.primary-button,
.github-button {

  display: inline-flex;

  align-items: center;

  gap: 10px;

  border-radius: 12px;

  padding: 12px 20px;

  font-size: 13px;

  font-weight: 600;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;

}


.primary-button {

  border: none;

  background: #6366f1;

  color: #ffffff;

  box-shadow:
    0 8px 20px rgba(99, 102, 241, 0.2);

}


.primary-button:hover {

  transform: translateY(-3px);

  box-shadow:
    0 12px 28px rgba(99, 102, 241, 0.3);

}


.github-button {

  border: 1px solid #dedfe5;

  background: #ffffff;

  color: #30343d;

}


.github-button:hover {

  transform: translateY(-3px);

  background: #f7f7f9;

  box-shadow:
    0 10px 24px rgba(31, 41, 55, 0.08);

}


.github-symbol {

  font-size: 15px;

}


.button-arrow {

  transition:
    transform 0.2s ease;

}


.primary-button:hover .button-arrow,
.github-button:hover .button-arrow {

  transform:
    translate(2px, -2px);

}


/* =====================================================
   Hero Grid
===================================================== */

.hero-grid {

  position: absolute;

  inset: 0;

  opacity: 0.45;

  background-image:
    linear-gradient(
      rgba(99, 102, 241, 0.04) 1px,
      transparent 1px
    ),
    linear-gradient(
      90deg,
      rgba(99, 102, 241, 0.04) 1px,
      transparent 1px
    );

  background-size: 42px 42px;

  mask-image:
    linear-gradient(
      to bottom,
      black,
      transparent 80%
    );

}


/* =====================================================
   Hero Orbs
===================================================== */

.hero-orb {

  position: absolute;

  border-radius: 50%;

  filter: blur(2px);

  pointer-events: none;

}


.orb-one {

  width: 240px;

  height: 240px;

  top: -110px;

  left: -70px;

  background:
    radial-gradient(
      circle,
      rgba(99, 102, 241, 0.12),
      transparent 70%
    );

  animation:
    orbFloat 8s ease-in-out infinite;

}


.orb-two {

  width: 320px;

  height: 320px;

  right: -120px;

  bottom: -170px;

  background:
    radial-gradient(
      circle,
      rgba(59, 130, 246, 0.1),
      transparent 70%
    );

  animation:
    orbFloat 10s ease-in-out infinite reverse;

}


/* =====================================================
   Particles
===================================================== */

.particle {

  position: absolute;

  width: 5px;

  height: 5px;

  border-radius: 50%;

  background: #8b8ff7;

  opacity: 0.5;

  box-shadow:
    0 0 12px rgba(99, 102, 241, 0.5);

  animation:
    particleFloat 5s ease-in-out infinite;

}


.particle-one {

  top: 24%;

  left: 14%;

}


.particle-two {

  top: 65%;

  left: 23%;

  animation-delay: 1s;

}


.particle-three {

  top: 30%;

  right: 16%;

  animation-delay: 2s;

}


.particle-four {

  top: 70%;

  right: 22%;

  animation-delay: 3s;

}


/* =====================================================
   Stats
===================================================== */

.stats-section {

  display: grid;

  grid-template-columns:
    repeat(4, 1fr);

  gap: 14px;

  margin: 18px 0 74px;

}


.stat-card {

  padding: 25px 20px;

  text-align: center;

  border: 1px solid #e8eaf0;

  border-radius: 16px;

  background: #ffffff;

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;

}


.stat-card:hover {

  transform:
    translateY(-5px);

  box-shadow:
    0 14px 30px
    rgba(31, 41, 55, 0.07);

}


.stat-number {

  color: #6366f1;

  font-size: 27px;

  font-weight: 750;

}


.stat-label {

  margin-top: 5px;

  color: #9298a5;

  font-size: 12px;

}


/* =====================================================
   Sections
===================================================== */

.content-section {

  margin-bottom: 76px;

}


.section-heading {

  display: flex;

  gap: 15px;

  margin-bottom: 26px;

}


.section-index {

  padding-top: 5px;

  color: #6366f1;

  font-size: 11px;

  font-weight: 700;

  letter-spacing: 1px;

}


.section-heading h2 {

  margin: 0;

  color: #242830;

  font-size: 27px;

}


.section-heading p {

  margin: 6px 0 0;

  color: #979ca8;

  font-size: 13px;

}


/* =====================================================
   Intro
===================================================== */

.intro-card {

  position: relative;

  display: flex;

  align-items: center;

  gap: 42px;

  overflow: hidden;

  padding: 38px;

  border: 1px solid #e8eaf0;

  border-radius: 20px;

  background: #ffffff;

  box-shadow:
    0 10px 35px
    rgba(31, 41, 55, 0.04);

  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;

}


.intro-card:hover {

  transform:
    translateY(-4px);

  box-shadow:
    0 18px 42px
    rgba(31, 41, 55, 0.07);

}


.intro-visual {

  position: relative;

  flex: 0 0 210px;

  height: 210px;

  display: flex;

  align-items: center;

  justify-content: center;

}


.visual-circle {

  position: absolute;

  border-radius: 50%;

  border:
    1px solid
    rgba(99, 102, 241, 0.15);

  animation:
    circlePulse 4s ease-in-out infinite;

}


.circle-one {

  width: 180px;

  height: 180px;

}


.circle-two {

  width: 125px;

  height: 125px;

  animation-delay: 0.6s;

}


.visual-icon {

  position: relative;

  z-index: 2;

  width: 76px;

  height: 76px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 22px;

  background: #f0f1ff;

  font-size: 38px;

  box-shadow:
    0 12px 30px
    rgba(99, 102, 241, 0.12);

  animation:
    iconFloat 3.5s ease-in-out infinite;

}


.intro-content {

  flex: 1;

}


.intro-label,
.github-label,
.author-label {

  color: #6366f1;

  font-size: 10px;

  font-weight: 700;

  letter-spacing: 1.5px;

}


.intro-content h3 {

  margin: 9px 0 14px;

  color: #292d36;

  font-size: 23px;

}


.intro-content h3 span {

  color: #6366f1;

}


.intro-content p {

  margin: 0 0 10px;

  color: #7e8491;

  font-size: 13px;

  line-height: 1.9;

}


.intro-tags,
.author-tags {

  display: flex;

  flex-wrap: wrap;

  gap: 7px;

  margin-top: 18px;

}


.intro-tags span,
.author-tags span {

  padding: 6px 9px;

  border-radius: 7px;

  background: #f5f6ff;

  color: #676d7a;

  font-size: 10px;

}


/* =====================================================
   Feature
===================================================== */

.feature-grid {

  display: grid;

  grid-template-columns:
    repeat(3, 1fr);

  gap: 14px;

}


.feature-card {

  position: relative;

  overflow: hidden;

  min-height: 185px;

  padding: 24px;

  border: 1px solid #e8eaf0;

  border-radius: 17px;

  background: #ffffff;

  transition:
    transform 0.25s ease,
    border-color 0.25s ease,
    box-shadow 0.25s ease;

  animation:
    cardEnter 0.6s ease both;

}


/* 依次出现 */

.feature-delay-0 {

  animation-delay: 0s;

}


.feature-delay-1 {

  animation-delay: 0.06s;

}


.feature-delay-2 {

  animation-delay: 0.12s;

}


.feature-delay-3 {

  animation-delay: 0.18s;

}


.feature-delay-4 {

  animation-delay: 0.24s;

}


.feature-delay-5 {

  animation-delay: 0.30s;

}


.feature-card:hover {

  transform:
    translateY(-7px);

  border-color:
    #d8dbff;

  box-shadow:
    0 18px 38px
    rgba(31, 41, 55, 0.08);

}


.feature-glow {

  position: absolute;

  width: 130px;

  height: 130px;

  top: -70px;

  right: -70px;

  border-radius: 50%;

  background:
    radial-gradient(
      circle,
      rgba(99, 102, 241, 0.12),
      transparent 70%
    );

  opacity: 0;

  transition:
    opacity 0.3s ease;

}


.feature-card:hover .feature-glow {

  opacity: 1;

}


.feature-top {

  display: flex;

  justify-content: space-between;

  align-items: center;

}


.feature-icon {

  width: 45px;

  height: 45px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 12px;

  background: #f3f4ff;

  font-size: 21px;

  transition:
    transform 0.25s ease;

}


.feature-card:hover .feature-icon {

  transform:
    scale(1.1)
    rotate(-4deg);

}


.feature-number {

  color: #d3d6de;

  font-size: 10px;

  font-weight: 700;

  letter-spacing: 1px;

}


.feature-card h3 {

  margin: 18px 0 8px;

  color: #2b3039;

  font-size: 16px;

}


.feature-card p {

  margin: 0;

  color: #8a909c;

  font-size: 12px;

  line-height: 1.7;

}


.feature-line {

  position: absolute;

  left: 24px;

  bottom: 18px;

  width: 0;

  height: 2px;

  border-radius: 99px;

  background: #6366f1;

  transition:
    width 0.3s ease;

}


.feature-card:hover .feature-line {

  width: 35px;

}


/* =====================================================
   Tech
===================================================== */

.tech-grid {

  display: grid;

  grid-template-columns:
    repeat(2, 1fr);

  gap: 14px;

}


.tech-card {

  padding: 25px;

  border: 1px solid #e8eaf0;

  border-radius: 17px;

  background: #ffffff;

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;

}


.tech-card:hover {

  transform:
    translateY(-5px);

  box-shadow:
    0 14px 30px
    rgba(31, 41, 55, 0.07);

}


.tech-header {

  display: flex;

  align-items: center;

  gap: 13px;

  margin-bottom: 20px;

}


.tech-icon {

  width: 43px;

  height: 43px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 11px;

  background: #f4f5ff;

  font-size: 20px;

}


.tech-header span {

  color: #a1a6b0;

  font-size: 9px;

  font-weight: 700;

  letter-spacing: 1px;

}


.tech-header h3 {

  margin: 3px 0 0;

  color: #2c3039;

  font-size: 15px;

}


.tech-tags {

  display: flex;

  flex-wrap: wrap;

  gap: 8px;

}


.tech-tag {

  padding: 7px 10px;

  border: 1px solid #eceef3;

  border-radius: 7px;

  color: #6e7480;

  background: #fafbfc;

  font-size: 11px;

  transition:
    color 0.2s ease,
    border-color 0.2s ease,
    background 0.2s ease;

}


.tech-tag:hover {

  border-color:
    #d8dbff;

  background:
    #f4f5ff;

  color:
    #6366f1;

}


/* =====================================================
   Flow
===================================================== */

.flow-wrapper {

  position: relative;

  display: grid;

  grid-template-columns:
    repeat(4, 1fr);

  padding: 34px 15px 10px;

  border: 1px solid #e8eaf0;

  border-radius: 20px;

  background: #ffffff;

}


.flow-line {

  position: absolute;

  top: 56px;

  left: 13%;

  width: 74%;

  height: 2px;

  overflow: hidden;

  background: #e9eaf0;

}


.flow-light {

  width: 25%;

  height: 100%;

  background:
    linear-gradient(
      90deg,
      transparent,
      #6366f1,
      transparent
    );

  animation:
    flowMove 2.6s linear infinite;

}


.flow-step {

  position: relative;

  z-index: 2;

  text-align: center;

}


.flow-circle {

  width: 46px;

  height: 46px;

  display: flex;

  align-items: center;

  justify-content: center;

  margin: 0 auto;

  border: 4px solid #ffffff;

  border-radius: 50%;

  background: #f0f1ff;

  box-shadow:
    0 0 0 1px #dfe1f9;

  font-size: 18px;

  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;

}


.flow-step:hover .flow-circle {

  transform:
    scale(1.15);

  box-shadow:
    0 0 0 5px
    rgba(99, 102, 241, 0.08);

}


.flow-step-number {

  margin-top: 14px;

  color: #a1a6b0;

  font-size: 9px;

  font-weight: 700;

  letter-spacing: 1px;

}


.flow-step h3 {

  margin: 6px 0;

  color: #2d313a;

  font-size: 14px;

}


.flow-step p {

  max-width: 140px;

  margin: 0 auto;

  color: #9298a5;

  font-size: 11px;

  line-height: 1.6;

}


/* =====================================================
   Author
===================================================== */

.author-card {

  position: relative;

  display: flex;

  align-items: center;

  gap: 22px;

  overflow: hidden;

  padding: 30px;

  border: 1px solid #e5e7ee;

  border-radius: 20px;

  background:
    linear-gradient(
      135deg,
      #ffffff,
      #f8f9ff
    );

  box-shadow:
    0 12px 35px
    rgba(31, 41, 55, 0.05);

}


.author-background {

  position: absolute;

  width: 280px;

  height: 280px;

  right: -80px;

  top: -130px;

  border-radius: 50%;

  background:
    radial-gradient(
      circle,
      rgba(99, 102, 241, 0.1),
      transparent 70%
    );

  animation:
    orbFloat 7s ease-in-out infinite;

}


.author-avatar {

  position: relative;

  z-index: 2;

  flex: 0 0 72px;

  width: 72px;

  height: 72px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 20px;

  background:
    linear-gradient(
      135deg,
      #6366f1,
      #818cf8
    );

  color: #ffffff;

  font-size: 29px;

  font-weight: 700;

  box-shadow:
    0 12px 25px
    rgba(99, 102, 241, 0.25);

  animation:
    avatarFloat 3.5s ease-in-out infinite;

}


.author-info {

  position: relative;

  z-index: 2;

  flex: 1;

}


.author-info h2 {

  margin: 5px 0;

  color: #282c34;

  font-size: 23px;

}


.author-info p {

  margin: 0;

  color: #858b98;

  font-size: 12px;

}


.author-button {

  position: relative;

  z-index: 2;

  display: flex;

  align-items: center;

  gap: 8px;

  flex-shrink: 0;

  border: none;

  border-radius: 10px;

  padding: 11px 16px;

  background: #20242c;

  color: #ffffff;

  font-size: 12px;

  font-weight: 600;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;

}


.author-button:hover {

  transform:
    translateY(-2px);

  box-shadow:
    0 10px 22px
    rgba(32, 36, 44, 0.18);

}


/* =====================================================
   GitHub
===================================================== */

.github-section {

  position: relative;

  overflow: hidden;

  margin-bottom: 60px;

  border-radius: 22px;

  background: #20242c;

  box-shadow:
    0 20px 45px
    rgba(32, 36, 44, 0.14);

}


.github-background {

  position: absolute;

  inset: 0;

  overflow: hidden;

}


.github-glow {

  position: absolute;

  width: 400px;

  height: 400px;

  right: -120px;

  top: -240px;

  border-radius: 50%;

  background:
    radial-gradient(
      circle,
      rgba(99, 102, 241, 0.32),
      transparent 70%
    );

  animation:
    orbFloat 8s ease-in-out infinite;

}


.github-content {

  position: relative;

  z-index: 2;

  display: flex;

  align-items: center;

  gap: 20px;

  padding: 38px;

}


.github-icon {

  width: 58px;

  height: 58px;

  display: flex;

  align-items: center;

  justify-content: center;

  flex-shrink: 0;

  border-radius: 15px;

  background:
    rgba(255, 255, 255, 0.1);

  color: #ffffff;

  font-size: 25px;

}


.github-text {

  flex: 1;

}


.github-label {

  color: #9298ff;

}


.github-text h2 {

  margin: 5px 0;

  color: #ffffff;

  font-size: 22px;

}


.github-text p {

  margin: 0;

  color: #aeb4c1;

  font-size: 12px;

}


.github-large-button {

  display: flex;

  align-items: center;

  gap: 9px;

  flex-shrink: 0;

  border: none;

  border-radius: 10px;

  padding: 12px 18px;

  background: #ffffff;

  color: #20242c;

  font-size: 12px;

  font-weight: 650;

  cursor: pointer;

  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;

}


.github-large-button:hover {

  transform:
    translateY(-3px);

  box-shadow:
    0 10px 25px
    rgba(0, 0, 0, 0.2);

}


/* =====================================================
   Footer
===================================================== */

.about-footer {

  text-align: center;

  color: #a0a5b1;

  font-size: 11px;

}


.footer-logo {

  margin-bottom: 8px;

  color: #6366f1;

  font-size: 14px;

  font-weight: 700;

}


.about-footer p {

  margin: 4px 0;

}


.footer-tech {

  margin-top: 10px;

  color: #b3b7c0;

  font-size: 10px;

}


/* =====================================================
   Animations
===================================================== */

@keyframes heroEnter {

  from {

    opacity: 0;

    transform:
      translateY(15px);

  }

  to {

    opacity: 1;

    transform:
      translateY(0);

  }

}


@keyframes cardEnter {

  from {

    opacity: 0;

    transform:
      translateY(12px);

  }

  to {

    opacity: 1;

    transform:
      translateY(0);

  }

}


@keyframes pulseDot {

  0%,
  100% {

    box-shadow:
      0 0 0 4px
      rgba(99, 102, 241, 0.08);

  }

  50% {

    box-shadow:
      0 0 0 7px
      rgba(99, 102, 241, 0.03);

  }

}


@keyframes orbFloat {

  0%,
  100% {

    transform:
      translate(0, 0);

  }

  50% {

    transform:
      translate(15px, 12px);

  }

}


@keyframes particleFloat {

  0%,
  100% {

    transform:
      translateY(0);

    opacity: 0.3;

  }

  50% {

    transform:
      translateY(-18px);

    opacity: 0.8;

  }

}


@keyframes iconFloat {

  0%,
  100% {

    transform:
      translateY(0);

  }

  50% {

    transform:
      translateY(-7px);

  }

}


@keyframes avatarFloat {

  0%,
  100% {

    transform:
      translateY(0);

  }

  50% {

    transform:
      translateY(-5px);

  }

}


@keyframes circlePulse {

  0%,
  100% {

    transform:
      scale(1);

    opacity: 0.6;

  }

  50% {

    transform:
      scale(1.05);

    opacity: 1;

  }

}


@keyframes flowMove {

  from {

    transform:
      translateX(-100%);

  }

  to {

    transform:
      translateX(400%);

  }

}


/* =====================================================
   Responsive
===================================================== */

@media (max-width: 900px) {

  .feature-grid {

    grid-template-columns:
      repeat(2, 1fr);

  }

  .stats-section {

    grid-template-columns:
      repeat(2, 1fr);

  }

  .flow-wrapper {

    grid-template-columns:
      repeat(2, 1fr);

    gap: 30px;

  }

  .flow-line {

    display: none;

  }

}


@media (max-width: 700px) {

  .about-page {

    padding:
      24px 16px 50px;

  }

  .hero-section {

    min-height: 480px;

    border-radius: 22px;

  }

  .hero-section h1 {

    font-size: 48px;

    letter-spacing: -2px;

  }

  .hero-subtitle {

    font-size: 18px;

  }

  .hero-actions {

    flex-direction: column;

  }

  .hero-actions button {

    width: 100%;

    justify-content: center;

  }

  .intro-card {

    flex-direction: column;

    padding: 25px;

  }

  .intro-visual {

    flex-basis: 170px;

    width: 100%;

  }

  .feature-grid,
  .tech-grid {

    grid-template-columns: 1fr;

  }

  .flow-wrapper {

    grid-template-columns: 1fr;

  }

  .author-card {

    flex-direction: column;

    align-items: flex-start;

  }

  .author-button {

    width: 100%;

    justify-content: center;

  }

  .github-content {

    align-items: flex-start;

    flex-direction: column;

    padding: 28px;

  }

  .github-large-button {

    width: 100%;

    justify-content: center;

  }

}

</style>
