<script setup>
import { ref } from "vue"
import { marked } from "marked"

const destination = ref("")
const days = ref(3)
const interests = ref([])
const pace = ref("适中")

const result = ref("")
const loading = ref(false)
const status = ref([])
const tripId = ref(null)
const currentStep = ref("")

const interestOptions = [
  "历史文化",
  "自然风光",
  "美食",
  "购物",
  "夜景",
  "亲子"
]

async function createTrip() {
  if (!destination.value) {
    alert("请输入目的地")
    return
  }

  if (interests.value.length === 0) {
    alert("请选择至少一个兴趣偏好")
    return
  }

  result.value = ""
  tripId.value = null
  status.value = []
  currentStep.value = "正在分析旅行需求..."
  loading.value = true

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/trip/stream",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          destination: destination.value,
          days: days.value,
          interests: interests.value,
          pace: pace.value
        })
      }
    )

    if (!response.ok) {
      throw new Error("请求失败")
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    let buffer = ""

    while (true) {
      const { value, done } = await reader.read()

      if (done) {
        break
      }

      buffer += decoder.decode(value, { stream: true })

      buffer = buffer.replace(/\r\n/g, "\n")

      const events = buffer.split("\n\n")

      buffer = events.pop() || ""

      for (const event of events) {
        if (event.trim()) {
          handleEvent(event)
        }
      }
    }

    if (buffer.trim()) {
      handleEvent(buffer)
    }
  } catch (error) {
    console.error(error)
    currentStep.value = "行程生成失败"
    status.value.push("行程生成失败，请检查后端服务")
  } finally {
    loading.value = false
  }
}

function handleEvent(event) {
  const lines = event.split("\n")

  let eventType = ""
  const dataLines = []

  for (const line of lines) {
    if (line.startsWith("event:")) {
      eventType = line.substring(6).trim()
    }

    if (line.startsWith("data:")) {
      let value = line.substring(5)

      if (value.startsWith(" ")) {
        value = value.substring(1)
      }

      dataLines.push(value)
    }
  }

  const data = dataLines.join("\n")

  if (eventType === "thinking") {
    status.value.push(data)
    currentStep.value = data
    return
  }

  if (eventType === "trip_id") {
    tripId.value = Number(data)
    currentStep.value = "行程生成完成"
    return
  }

  if (eventType === "message") {
    result.value += data
    return
  }

  if (eventType === "done") {
    currentStep.value = "行程生成完成"
  }
}

async function exportTrip(format) {
  if (!tripId.value) {
    alert("暂无可导出的行程")
    return
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/export/trip/${tripId.value}?format=${format}`,
      {
        method: "POST"
      }
    )

    if (!response.ok) {
      throw new Error("导出失败")
    }

    const blob = await response.blob()

    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")

    link.href = url
    link.download = getFileName(format)

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    URL.revokeObjectURL(url)
  } catch (error) {
    console.error(error)
    alert("攻略导出失败")
  }
}

function getFileName(format) {
  const baseName = `${destination.value}${days.value}天旅游攻略`

  if (format === "md") {
    return `${baseName}.md`
  }

  if (format === "word") {
    return `${baseName}.docx`
  }

  return `${baseName}.xlsx`
}

function renderMarkdown(content) {
  return marked(content)
}
</script>

<template>
  <main class="container">

    <!-- 左侧：旅行需求 -->
    <section class="panel form-panel">

      <div class="panel-title">
        <div>
          <h2>规划你的旅行</h2>
          <p>告诉 AI 你的旅行偏好</p>
        </div>

        <span class="title-icon">🧭</span>
      </div>

      <div class="form-item">
        <label>目的地</label>

        <div class="input-wrapper">
          <span class="input-icon">📍</span>

          <input
            v-model="destination"
            type="text"
            placeholder="例如：上海、北京、杭州"
          />
        </div>
      </div>

      <div class="form-item">
        <label>游玩天数</label>

        <div class="days-input">
          <button
            type="button"
            :disabled="days <= 1"
            @click="days--"
          >
            −
          </button>

          <span>{{ days }}</span>

          <button
            type="button"
            :disabled="days >= 30"
            @click="days++"
          >
            +
          </button>

          <em>天</em>
        </div>
      </div>

      <div class="form-item">
        <label>兴趣偏好</label>

        <div class="options">
          <label
            v-for="item in interestOptions"
            :key="item"
            class="interest-option"
            :class="{ active: interests.includes(item) }"
          >
            <input
              v-model="interests"
              type="checkbox"
              :value="item"
            />

            <span>{{ item }}</span>
          </label>
        </div>
      </div>

      <div class="form-item">
        <label>行程节奏</label>

        <div class="pace-options">

          <button
            type="button"
            :class="{ active: pace === '紧凑' }"
            @click="pace = '紧凑'"
          >
            <strong>⚡</strong>
            <span>紧凑</span>
          </button>

          <button
            type="button"
            :class="{ active: pace === '适中' }"
            @click="pace = '适中'"
          >
            <strong>☀</strong>
            <span>适中</span>
          </button>

          <button
            type="button"
            :class="{ active: pace === '休闲' }"
            @click="pace = '休闲'"
          >
            <strong>🌿</strong>
            <span>休闲</span>
          </button>

        </div>
      </div>

      <button
        class="submit-button"
        :class="{ loading: loading }"
        :disabled="loading"
        @click="createTrip"
      >
        <span v-if="loading" class="button-loading">
          <span class="button-spinner"></span>
          正在规划你的旅程...
        </span>

        <span v-else>
          ✈ 开始规划行程
        </span>
      </button>

      <div class="form-tip">
        <span>💡</span>

        <span>
          AI 将结合本地旅游资料，为你生成有依据的专属行程
        </span>
      </div>

    </section>


    <!-- 右侧：AI 行程 -->
    <section class="panel result-panel">

      <div class="result-header">

        <div>
          <h2>AI 行程攻略</h2>

          <p v-if="result">
            基于你的偏好生成的专属旅游方案
          </p>

          <p v-else>
            你的专属旅行计划将在这里生成
          </p>
        </div>

        <div class="result-actions">

          <span
            v-if="loading"
            class="loading"
          >
            <span class="loading-dot"></span>
            正在生成
          </span>

          <template v-if="result && !loading">

            <button
              class="export-button"
              @click="exportTrip('md')"
            >
              <span>↓</span>
              Markdown
            </button>

            <button
              class="export-button"
              @click="exportTrip('word')"
            >
              <span>↓</span>
              Word
            </button>

            <button
              class="export-button"
              @click="exportTrip('excel')"
            >
              <span>↓</span>
              Excel
            </button>

          </template>

        </div>

      </div>


      <!-- AI 执行过程 -->
      <div
        v-if="status.length"
        class="status-box"
        :class="{ processing: loading }"
      >

        <div class="status-header">

          <div class="status-title">
            <span class="status-title-icon">✦</span>
            <span>AI 执行过程</span>
          </div>

          <span
            class="status-state"
            :class="{ finished: !loading }"
          >
            {{ loading ? "处理中" : "已完成" }}
          </span>

        </div>

        <div class="status-list">

          <div
            v-for="(item, index) in status"
            :key="index"
            class="status-item"
            :class="{
              active: loading && item === currentStep,
              completed: !loading || item !== currentStep
            }"
          >

            <span
              class="status-icon"
              :class="{
                current: loading && item === currentStep,
                finished: !loading || item !== currentStep
              }"
            >
              <span
                v-if="loading && item === currentStep"
              >
                ●
              </span>

              <span v-else>
                ✓
              </span>
            </span>

            <span class="status-text">
              {{ item }}
            </span>

            <span
              v-if="loading && item === currentStep"
              class="status-running"
            >
              处理中
            </span>

          </div>

        </div>

      </div>


      <!-- 空状态 -->
      <div
        v-if="!result && !loading"
        class="empty"
      >

        <div class="empty-illustration">
          <div class="plane">✈</div>
        </div>

        <h3>开始你的旅行规划</h3>

        <p>填写左侧旅行需求</p>
        <p>AI 将为你生成专属旅游行程</p>

        <div class="empty-tags">
          <span>📚 RAG 知识库</span>
          <span>🤖 AI Agent</span>
          <span>📖 来源引用</span>
        </div>

      </div>


      <!-- Markdown 结果 -->
      <div
        v-if="result"
        class="markdown-body"
      >
        <div
          class="markdown-content"
          v-html="renderMarkdown(result)"
        ></div>
      </div>


      <!-- 生成中 -->
      <div
        v-if="loading && !result"
        class="generating"
      >

        <div class="generating-orbit">
          <div class="orbit-ring"></div>
          <div class="generating-icon">✦</div>
        </div>

        <p>AI 正在为你规划行程...</p>

        <span>
          {{ currentStep || "正在检索旅游资料并生成方案" }}
        </span>

      </div>

    </section>

  </main>
</template>


<style>
* {
  box-sizing: border-box;
}


body {
  margin: 0;
  font-family:
    Inter,
    "Microsoft YaHei",
    Arial,
    sans-serif;
  background: #f5f7fb;
  color: #1f2937;
}

button,
input,
select {
  font: inherit;
}

button {
  -webkit-tap-highlight-color: transparent;
}

.container {
  width: min(1400px, 92%);
  margin: 30px auto 50px;
  display: grid;
  grid-template-columns: 370px 1fr;
  gap: 24px;
  align-items: start;
  animation: pageFadeIn 0.45s ease-out;
}

.panel {
  background: white;
  border: 1px solid #e9ecf2;
  border-radius: 16px;
  box-shadow: 0 5px 25px rgba(31, 41, 55, 0.045);
  transition:
    box-shadow 0.25s ease,
    transform 0.25s ease;
}

.form-panel {
  padding: 28px;
}

.form-panel:hover {
  box-shadow: 0 10px 30px rgba(31, 41, 55, 0.07);
}

.panel-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.panel-title h2,
.result-header h2 {
  margin: 0;
  font-size: 19px;
  letter-spacing: -0.3px;
}

.panel-title p,
.result-header p {
  margin: 6px 0 0;
  color: #9aa2b1;
  font-size: 13px;
}

.title-icon {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fffbeb;
  border-radius: 10px;
  font-size: 19px;
  transition:
    transform 0.3s ease,
    background 0.3s ease;
}

.form-panel:hover .title-icon {
  transform: rotate(-8deg) scale(1.05);
  background: #fef3c7;
}

.form-item {
  margin-top: 25px;
}

.form-item > label {
  display: block;
  margin-bottom: 9px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 13px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 15px;
  transition: transform 0.2s ease;
}

.input-wrapper:focus-within .input-icon {
  transform: translateY(-50%) scale(1.12);
}

input[type="text"] {
  width: 100%;
  height: 44px;
  padding: 0 12px 0 39px;
  border: 1px solid #dfe3ea;
  border-radius: 9px;
  outline: none;
  background: #fafbfc;
  transition:
    border-color 0.2s,
    background 0.2s,
    box-shadow 0.2s;
}

input[type="text"]:focus {
  border-color: #f59e0b;
  background: white;
  box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.10);
}

input::placeholder {
  color: #b3bac6;
}

.days-input {
  height: 44px;
  display: flex;
  align-items: center;
  border: 1px solid #dfe3ea;
  border-radius: 9px;
  background: #fafbfc;
  overflow: hidden;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}

.days-input:focus-within {
  border-color: #f59e0b;
  box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.10);
}

.days-input button {
  width: 44px;
  height: 100%;
  border: none;
  background: transparent;
  color: #d97706;
  font-size: 21px;
  cursor: pointer;
  transition:
    background 0.2s,
    transform 0.15s;
}

.days-input button:hover:not(:disabled) {
  background: #fef3c7;
}

.days-input button:active:not(:disabled) {
  transform: scale(0.88);
}

.days-input button:disabled {
  color: #cdd1d9;
  cursor: not-allowed;
}

.days-input span {
  flex: 1;
  text-align: center;
  font-weight: 600;
  color: #374151;
}

.days-input em {
  padding-right: 14px;
  color: #9ca3af;
  font-size: 13px;
  font-style: normal;
}

.options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 9px;
}

.interest-option {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e3e6eb;
  border-radius: 8px;
  background: #fafbfc;
  color: #6b7280;
  font-size: 13px;
  cursor: pointer;
  transition:
    transform 0.18s ease,
    border-color 0.18s ease,
    background 0.18s ease,
    color 0.18s ease;
}

.interest-option:hover {
  transform: translateY(-1px);
  border-color: #f59e0b;
  color: #d97706;
}

.interest-option.active {
  border-color: #f59e0b;
  background: #fff7e6;
  color: #b45309;
  font-weight: 600;
  box-shadow: 0 3px 10px rgba(217, 119, 6, 0.10);
}

.interest-option input {
  display: none;
}

.pace-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.pace-options button {
  height: 64px;
  border: 1px solid #e3e6eb;
  border-radius: 9px;
  background: #fafbfc;
  color: #6b7280;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  transition:
    transform 0.18s ease,
    border-color 0.18s ease,
    background 0.18s ease,
    color 0.18s ease;
}

.pace-options button strong {
  font-size: 16px;
  font-weight: normal;
  transition: transform 0.2s ease;
}

.pace-options button:hover {
  transform: translateY(-2px);
  border-color: #f59e0b;
}

.pace-options button:hover strong {
  transform: scale(1.15);
}

.pace-options button.active {
  border-color: #f59e0b;
  background: #fff7e6;
  color: #b45309;
  box-shadow: 0 3px 10px rgba(217, 119, 6, 0.10);
}

.submit-button {
  width: 100%;
  height: 46px;
  margin-top: 28px;
  border: none;
  border-radius: 9px;
  background: linear-gradient(135deg, #d97706, #b45309);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(180, 83, 9, 0.20);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 11px 24px rgba(180, 83, 9, 0.28);
}

.submit-button:active:not(:disabled) {
  transform: translateY(0) scale(0.98);
}

.submit-button.loading {
  cursor: wait;
}

.submit-button:disabled {
  opacity: 0.72;
}

.button-loading {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.button-spinner {
  width: 13px;
  height: 13px;
  border: 2px solid rgba(255, 255, 255, 0.35);
  border-top-color: white;
  border-radius: 50%;
  animation: rotate 0.8s linear infinite;
}

.form-tip {
  margin-top: 14px;
  padding: 10px 12px;
  display: flex;
  gap: 8px;
  align-items: flex-start;
  border-radius: 8px;
  background: #f8f9fc;
  color: #9aa2b1;
  font-size: 11px;
  line-height: 18px;
  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.form-tip:hover {
  background: #f4f5fa;
  transform: translateY(-1px);
}

.result-panel {
  min-height: 680px;
  padding: 28px 32px 36px;
  overflow: hidden;
}

.result-header {
  min-height: 48px;
  padding-bottom: 17px;
  border-bottom: 1px solid #edf0f3;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

.result-actions {
  display: flex;
  align-items: center;
  gap: 7px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.loading {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-right: 5px;
  color: #d97706;
  font-size: 12px;
}

.loading-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #d97706;
  animation: pulse 1.2s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.35;
    transform: scale(0.85);
  }

  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

.export-button {
  height: 32px;
  padding: 0 10px;
  display: flex;
  align-items: center;
  gap: 5px;
  border: 1px solid #e0e3e8;
  border-radius: 7px;
  background: white;
  color: #5f6673;
  cursor: pointer;
  font-size: 11px;
  transition:
    transform 0.18s ease,
    border-color 0.18s ease,
    color 0.18s ease,
    background 0.18s ease;
}

.export-button:hover {
  transform: translateY(-1px);
  border-color: #fbbf24;
  color: #b45309;
  background: #fffdf8;
}

.export-button:active {
  transform: scale(0.96);
}


/* ================================
   AI 执行状态
================================ */

.status-box {
  position: relative;
  margin-top: 20px;
  padding: 15px 17px;
  border: 1px solid #e8eaf5;
  border-radius: 11px;
  background: linear-gradient(
    135deg,
    #fffdf8,
    #f8f9fc
  );
  overflow: hidden;
  animation: statusEnter 0.3s ease-out;
}

.status-box.processing::after {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  width: 35%;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    #f59e0b,
    transparent
  );
  animation: statusLoading 1.5s linear infinite;
}

@keyframes statusLoading {
  from {
    transform: translateX(-150%);
  }

  to {
    transform: translateX(400%);
  }
}

@keyframes statusEnter {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.status-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 9px;
  border-bottom: 1px solid #eceef5;
}

.status-title {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #4b5563;
  font-size: 12px;
  font-weight: 600;
}

.status-title-icon {
  color: #d97706;
  animation: sparkle 1.5s ease-in-out infinite;
}

@keyframes sparkle {
  0%,
  100% {
    opacity: 0.45;
    transform: scale(0.9);
  }

  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

.status-state {
  padding: 3px 8px;
  border-radius: 10px;
  background: #fef3c7;
  color: #d97706;
  font-size: 10px;
}

.status-state.finished {
  background: #f0fdf4;
  color: #16a34a;
}

.status-list {
  padding-top: 8px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 9px;
  min-height: 29px;
  color: #7b8493;
  font-size: 12px;
  transition:
    color 0.25s ease,
    transform 0.25s ease;
}

.status-item.active {
  color: #b45309;
  font-weight: 500;
}

.status-item.completed {
  color: #6b7280;
}

.status-icon {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 9px;
  transition: all 0.25s ease;
}

.status-icon.finished {
  background: #dcfce7;
  color: #16a34a;
}

.status-icon.current {
  background: #fde68a;
  color: #d97706;
  animation: statusPulse 1s ease-in-out infinite;
}

.status-text {
  flex: 1;
}

.status-running {
  color: #f59e0b;
  font-size: 10px;
  animation: pulse 1.2s ease-in-out infinite;
}

@keyframes statusPulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }

  50% {
    opacity: 0.4;
    transform: scale(0.88);
  }
}


/* ================================
   空状态
================================ */

.empty {
  min-height: 520px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  text-align: center;
  animation: emptyFadeIn 0.5s ease-out;
}

@keyframes emptyFadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.empty-illustration {
  width: 92px;
  height: 92px;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #fff7e6;
  transition:
    transform 0.3s ease,
    background 0.3s ease;
}

.empty:hover .empty-illustration {
  background: #fcdc9a;
}

.plane {
  color: #d97706;
  font-size: 40px;
  animation: planeFloat 3s ease-in-out infinite;
}

@keyframes planeFloat {
  0%,
  100% {
    transform: translate(0, 0) rotate(-10deg);
  }

  50% {
    transform: translate(5px, -5px) rotate(-6deg);
  }
}

.empty h3 {
  margin: 0 0 9px;
  color: #4b5563;
  font-size: 17px;
}

.empty p {
  margin: 3px 0;
  font-size: 13px;
}

.empty-tags {
  display: flex;
  gap: 7px;
  margin-top: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.empty-tags span {
  padding: 5px 9px;
  border-radius: 15px;
  background: #f7f8fa;
  color: #9ca3af;
  font-size: 10px;
  transition:
    transform 0.2s ease,
    background 0.2s ease,
    color 0.2s ease;
}

.empty-tags span:hover {
  transform: translateY(-2px);
  background: #fef3c7;
  color: #d97706;
}


/* ================================
   AI 生成中
================================ */

.generating {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  animation: generatingFadeIn 0.35s ease-out;
}

@keyframes generatingFadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.generating-orbit {
  position: relative;
  width: 70px;
  height: 70px;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.orbit-ring {
  position: absolute;
  width: 58px;
  height: 58px;
  border: 1px solid rgba(217, 119, 6, 0.22);
  border-top-color: #d97706;
  border-radius: 50%;
  animation: rotate 1.6s linear infinite;
}

.generating-icon {
  position: relative;
  z-index: 2;
  color: #d97706;
  font-size: 30px;
  animation: starFloat 1.8s ease-in-out infinite;
}

@keyframes starFloat {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }

  50% {
    transform: translateY(-4px) scale(1.05);
  }
}

.generating p {
  margin: 0 0 6px;
  color: #6b7280;
  font-size: 14px;
}

.generating span {
  max-width: 420px;
  text-align: center;
  font-size: 12px;
  color: #9ca3af;
}


/* ================================
   Markdown
================================ */

.markdown-body {
  padding: 26px 8px 10px;
  color: #374151;
  line-height: 1.85;
  font-size: 14px;
  animation: resultEnter 0.4s ease-out;
}

.markdown-content {
  animation: resultContentEnter 0.45s ease-out;
}

@keyframes resultEnter {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes resultContentEnter {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.markdown-body h1 {
  margin: 0 0 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f0f1f5;
  color: #1f2937;
  font-size: 26px;
  line-height: 1.4;
}

.markdown-body h2 {
  margin-top: 30px;
  margin-bottom: 13px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
  color: #374151;
  font-size: 19px;
}

.markdown-body h3 {
  margin-top: 21px;
  margin-bottom: 8px;
  color: #4b5563;
}


/* ================================
   通用交互
================================ */

button:not(:disabled) {
  -webkit-tap-highlight-color: transparent;
}

button:not(:disabled):active {
  transform: scale(0.97);
}


/* ================================
   页面响应式
================================ */

@media (max-width: 1000px) {
  .container {
    grid-template-columns: 1fr;
  }

  .form-panel {
    width: 100%;
  }

  .result-panel {
    min-height: 600px;
  }
}

@media (max-width: 600px) {
  .container {
    width: 94%;
    margin-top: 18px;
    gap: 16px;
  }

  .form-panel,
  .result-panel {
    padding: 20px;
    border-radius: 13px;
  }

  .result-header {
    flex-direction: column;
  }

  .result-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .markdown-body h1 {
    font-size: 22px;
  }

  .markdown-body h2 {
    font-size: 17px;
  }

  .empty {
    min-height: 400px;
  }
}


/* ================================
   减少动画偏好
================================ */

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}


@keyframes pageFadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>