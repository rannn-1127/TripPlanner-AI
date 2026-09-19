<script setup>
import { ref, computed, onMounted } from "vue"
import { marked } from "marked"

const API_BASE = "http://127.0.0.1:8000"

/* =========================
   页面
========================= */

const currentPage = ref("home")

function switchPage(page) {
  currentPage.value = page

  if (page === "history") {
    loadHistory()
  }

  if (page === "knowledge") {
    loadKnowledgeFiles()
  }
}

/* =========================
   行程规划
========================= */

const destination = ref("")
const days = ref(3)
const interests = ref([])
const pace = ref("适中")

const result = ref("")
const loading = ref(false)
const status = ref([])
const tripId = ref(null)

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
  loading.value = true

  try {
    const response = await fetch(
      `${API_BASE}/trip/stream`,
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
    return
  }

  if (eventType === "trip_id") {
    tripId.value = Number(data)
    return
  }

  if (eventType === "message") {
    result.value += data
    return
  }

  if (eventType === "done") {
    return
  }
}

/* =========================
   导出
========================= */

async function exportTrip(format) {
  if (!tripId.value) {
    alert("暂无可导出的行程")
    return
  }

  try {
    const response = await fetch(
      `${API_BASE}/export/trip/${tripId.value}?format=${format}`,
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
  const baseName =
    `${selectedTrip.value?.destination || destination.value}` +
    `${selectedTrip.value?.days || days.value}天旅游攻略`

  if (format === "md") {
    return `${baseName}.md`
  }

  if (format === "word") {
    return `${baseName}.docx`
  }

  return `${baseName}.xlsx`
}

function renderMarkdown(content) {
  return marked(content || "")
}

/* =========================
   历史记录
========================= */

const historyList = ref([])
const historyLoading = ref(false)
const historyError = ref("")
const selectedTrip = ref(null)

async function loadHistory() {
  historyLoading.value = true
  historyError.value = ""

  try {
    const response = await fetch(`${API_BASE}/history`)

    if (!response.ok) {
      throw new Error("历史记录获取失败")
    }

    const data = await response.json()

    historyList.value = data.trips || []
  } catch (error) {
    console.error(error)
    historyError.value = "历史记录加载失败，请检查后端服务"
  } finally {
    historyLoading.value = false
  }
}

async function viewHistory(trip) {
  try {
    const response = await fetch(
      `${API_BASE}/history/${trip.id}`
    )

    if (!response.ok) {
      throw new Error("行程获取失败")
    }

    const data = await response.json()

    selectedTrip.value = data
    tripId.value = data.id
  } catch (error) {
    console.error(error)
    alert("历史行程加载失败")
  }
}

function closeHistoryDetail() {
  selectedTrip.value = null
  tripId.value = null
}

/* =========================
   知识库
========================= */

const knowledgeFiles = ref([])
const knowledgeLoading = ref(false)
const uploadLoading = ref(false)
const selectedFile = ref(null)

const allowedExtensions = [
  ".pdf",
  ".docx",
  ".txt"
]

function chooseFile(event) {
  const file = event.target.files[0]

  if (!file) {
    return
  }

  const fileName = file.name.toLowerCase()

  const valid = allowedExtensions.some(
    extension => fileName.endsWith(extension)
  )

  if (!valid) {
    alert("只支持 PDF、Word、TXT 文件")
    event.target.value = ""
    return
  }

  selectedFile.value = file
}

async function uploadKnowledgeFile() {
  if (!selectedFile.value) {
    alert("请选择文件")
    return
  }

  uploadLoading.value = true

  try {
    const formData = new FormData()

    formData.append(
      "file",
      selectedFile.value
    )

    const response = await fetch(
      `${API_BASE}/knowledge/upload`,
      {
        method: "POST",
        body: formData
      }
    )

    if (!response.ok) {
      const text = await response.text()
      throw new Error(text || "上传失败")
    }

    alert("文件上传成功")

    selectedFile.value = null

    const input =
      document.getElementById("knowledge-file-input")

    if (input) {
      input.value = ""
    }

    await loadKnowledgeFiles()
  } catch (error) {
    console.error(error)
    alert("文件上传失败")
  } finally {
    uploadLoading.value = false
  }
}

async function loadKnowledgeFiles() {
  knowledgeLoading.value = true

  try {
    const response = await fetch(
      `${API_BASE}/knowledge/files`
    )

    if (!response.ok) {
      throw new Error("文件列表获取失败")
    }

    const data = await response.json()

    knowledgeFiles.value = data.files || []
  } catch (error) {
    console.error(error)
    alert("知识库文件加载失败，请检查后端服务")
  } finally {
    knowledgeLoading.value = false
  }
}

async function deleteKnowledgeFile(filename) {
  const confirmed = confirm(
    `确定删除「${filename}」吗？\n\n删除后该文件将无法继续用于行程规划。`
  )

  if (!confirmed) {
    return
  }

  try {
    const response = await fetch(
      `${API_BASE}/knowledge/file/${encodeURIComponent(filename)}`,
      {
        method: "DELETE"
      }
    )

    if (!response.ok) {
      throw new Error("删除失败")
    }

    alert("文件删除成功")

    await loadKnowledgeFiles()
  } catch (error) {
    console.error(error)
    alert("文件删除失败")
  }
}

function getFileIcon(filename) {
  const name = filename.toLowerCase()

  if (name.endsWith(".pdf")) {
    return "📕"
  }

  if (name.endsWith(".docx")) {
    return "📘"
  }

  if (name.endsWith(".txt")) {
    return "📄"
  }

  return "📄"
}

function getFileType(filename) {
  const name = filename.toLowerCase()

  if (name.endsWith(".pdf")) {
    return "PDF"
  }

  if (name.endsWith(".docx")) {
    return "Word"
  }

  if (name.endsWith(".txt")) {
    return "TXT"
  }

  return "文件"
}

/* =========================
   页面初始化
========================= */

onMounted(() => {
  // 默认进入行程规划页面
})
</script>


<template>
  <div class="app">

    <!-- =========================
         顶部导航
    ========================== -->

    <header class="header">
      <div class="header-inner">

        <div
          class="brand"
          @click="switchPage('home')"
        >
          <div class="brand-icon">✈</div>

          <div>
            <h1>TripPlanner-AI</h1>
            <p>AI 智能旅游行程规划助手</p>
          </div>
        </div>

        <nav class="nav">

          <button
            class="nav-item"
            :class="{ active: currentPage === 'home' }"
            @click="switchPage('home')"
          >
            <span>🧭</span>
            行程规划
          </button>

          <button
            class="nav-item"
            :class="{ active: currentPage === 'history' }"
            @click="switchPage('history')"
          >
            <span>🕘</span>
            历史记录
          </button>

          <button
            class="nav-item"
            :class="{ active: currentPage === 'knowledge' }"
            @click="switchPage('knowledge')"
          >
            <span>📚</span>
            知识库
          </button>

        </nav>

        <div class="header-badge">
          <span class="badge-dot"></span>
          AI Travel Planner
        </div>

      </div>
    </header>


    <!-- =========================
         行程规划
    ========================== -->

    <main
      v-if="currentPage === 'home'"
      class="container"
    >

      <!-- 左侧表单 -->

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
              :class="{
                active: interests.includes(item)
              }"
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
          :disabled="loading"
          @click="createTrip"
        >

          <span v-if="loading">
            ✦ 正在规划你的旅程...
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


      <!-- 右侧结果 -->

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


            <template
              v-if="result && !loading"
            >

              <button
                class="export-button"
                @click="exportTrip('md')"
              >
                ↓ Markdown
              </button>

              <button
                class="export-button"
                @click="exportTrip('word')"
              >
                ↓ Word
              </button>

              <button
                class="export-button"
                @click="exportTrip('excel')"
              >
                ↓ Excel
              </button>

            </template>

          </div>

        </div>


        <!-- 执行过程 -->

        <div
          v-if="status.length"
          class="status-box"
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
            >

              <span
                class="status-icon"
                :class="{
                  current:
                    loading &&
                    index === status.length - 1,

                  finished:
                    !loading ||
                    index < status.length - 1
                }"
              >
                {{
                  loading &&
                  index === status.length - 1
                    ? "●"
                    : "✓"
                }}
              </span>

              <span>{{ item }}</span>

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


        <!-- 生成中 -->

        <div
          v-if="loading && !result"
          class="generating"
        >

          <div class="generating-icon">
            ✦
          </div>

          <p>
            AI 正在为你规划行程...
          </p>

          <span>
            正在检索旅游资料并生成方案
          </span>

        </div>


        <!-- Markdown -->

        <div
          v-if="result"
          class="markdown-body"
          v-html="renderMarkdown(result)"
        ></div>

      </section>

    </main>


    <!-- =========================
         历史记录
    ========================== -->

    <main
      v-if="currentPage === 'history'"
      class="page-container"
    >

      <section class="page-panel">

        <div class="page-header">

          <div>
            <h2>历史行程</h2>
            <p>
              查看你之前生成的旅游行程
            </p>
          </div>

          <button
            class="primary-small-button"
            @click="switchPage('home')"
          >
            + 创建新行程
          </button>

        </div>


        <!-- 详情 -->

        <div
          v-if="selectedTrip"
          class="history-detail"
        >

          <div class="detail-header">

            <button
              class="back-button"
              @click="closeHistoryDetail"
            >
              ← 返回历史记录
            </button>

            <div class="detail-actions">

              <button
                class="export-button"
                @click="exportTrip('md')"
              >
                ↓ Markdown
              </button>

              <button
                class="export-button"
                @click="exportTrip('word')"
              >
                ↓ Word
              </button>

              <button
                class="export-button"
                @click="exportTrip('excel')"
              >
                ↓ Excel
              </button>

            </div>

          </div>


          <div class="trip-meta">

            <div>
              <span>目的地</span>
              <strong>
                {{ selectedTrip.destination }}
              </strong>
            </div>

            <div>
              <span>游玩天数</span>
              <strong>
                {{ selectedTrip.days }} 天
              </strong>
            </div>

            <div>
              <span>行程节奏</span>
              <strong>
                {{ selectedTrip.pace }}
              </strong>
            </div>

            <div>
              <span>生成时间</span>
              <strong>
                {{ selectedTrip.created_at }}
              </strong>
            </div>

          </div>


          <div class="trip-interests">

            <span>兴趣偏好</span>

            <div class="interest-tags">

              <span
                v-for="item in selectedTrip.interests"
                :key="item"
              >
                {{ item }}
              </span>

            </div>

          </div>


          <div
            class="markdown-body history-markdown"
            v-html="
              renderMarkdown(selectedTrip.content)
            "
          ></div>

        </div>


        <!-- 列表 -->

        <template v-else>

          <div
            v-if="historyLoading"
            class="page-loading"
          >
            <div class="loading-spinner">✦</div>
            正在加载历史行程...
          </div>


          <div
            v-else-if="historyError"
            class="page-error"
          >
            {{ historyError }}

            <button
              class="primary-small-button"
              @click="loadHistory"
            >
              重新加载
            </button>
          </div>


          <div
            v-else-if="historyList.length === 0"
            class="page-empty"
          >

            <div class="large-empty-icon">
              🧳
            </div>

            <h3>还没有历史行程</h3>

            <p>
              创建一次旅行规划后，行程会自动保存到这里
            </p>

            <button
              class="primary-small-button"
              @click="switchPage('home')"
            >
              开始规划
            </button>

          </div>


          <div
            v-else
            class="history-list"
          >

            <div
              v-for="trip in historyList"
              :key="trip.id"
              class="history-card"
              @click="viewHistory(trip)"
            >

              <div class="history-card-icon">
                📍
              </div>

              <div class="history-card-content">

                <div class="history-card-title">
                  {{ trip.destination }}
                  {{ trip.days }}天旅游行程
                </div>

                <div class="history-card-info">

                  <span>
                    🌿 {{ trip.pace }}
                  </span>

                  <span>
                    🕘 {{ trip.created_at }}
                  </span>

                </div>


                <div class="history-card-tags">

                  <span
                    v-for="item in trip.interests"
                    :key="item"
                  >
                    {{ item }}
                  </span>

                </div>

              </div>


              <div class="history-card-arrow">
                →
              </div>

            </div>

          </div>

        </template>

      </section>

    </main>


    <!-- =========================
         知识库
    ========================== -->

    <main
      v-if="currentPage === 'knowledge'"
      class="page-container"
    >

      <section class="page-panel">

        <div class="page-header">

          <div>
            <h2>旅游知识库</h2>

            <p>
              上传目的地资料，为 AI 提供可靠的旅游信息
            </p>
          </div>

          <div class="knowledge-count">
            共 {{ knowledgeFiles.length }} 个文件
          </div>

        </div>


        <!-- 上传区域 -->

        <div class="upload-section">

          <div class="upload-icon">
            📚
          </div>

          <h3>
            上传旅游资料
          </h3>

          <p>
            支持 PDF、Word、TXT 文件
          </p>


          <input
            id="knowledge-file-input"
            type="file"
            accept=".pdf,.docx,.txt"
            hidden
            @change="chooseFile"
          />


          <label
            for="knowledge-file-input"
            class="choose-file-button"
          >
            选择文件
          </label>


          <div
            v-if="selectedFile"
            class="selected-file"
          >

            <div class="selected-file-info">

              <span class="file-icon">
                {{ getFileIcon(selectedFile.name) }}
              </span>

              <div>

                <strong>
                  {{ selectedFile.name }}
                </strong>

                <span>
                  {{
                    getFileType(selectedFile.name)
                  }}
                </span>

              </div>

            </div>


            <button
              class="upload-button"
              :disabled="uploadLoading"
              @click="uploadKnowledgeFile"
            >
              {{
                uploadLoading
                  ? "正在上传..."
                  : "开始上传"
              }}
            </button>

          </div>

        </div>


        <!-- 文件列表 -->

        <div class="file-section">

          <div class="file-section-header">

            <div>

              <h3>
                已上传资料
              </h3>

              <p>
                AI 会从这些资料中检索旅游信息
              </p>

            </div>

            <button
              class="refresh-button"
              @click="loadKnowledgeFiles"
            >
              ↻ 刷新
            </button>

          </div>


          <div
            v-if="knowledgeLoading"
            class="page-loading small"
          >
            <div class="loading-spinner">
              ✦
            </div>
            正在加载知识库...
          </div>


          <div
            v-else-if="knowledgeFiles.length === 0"
            class="file-empty"
          >

            <div>
              📄
            </div>

            <p>
              暂无知识库文件
            </p>

            <span>
              上传旅游资料后，AI 才能从本地知识库检索相关信息
            </span>

          </div>


          <div
            v-else
            class="file-list"
          >

            <div
              v-for="file in knowledgeFiles"
              :key="file"
              class="file-card"
            >

              <div class="file-main">

                <div class="file-icon-large">
                  {{ getFileIcon(file) }}
                </div>

                <div class="file-info">

                  <strong>
                    {{ file }}
                  </strong>

                  <span>
                    {{ getFileType(file) }}
                  </span>

                </div>

              </div>


              <button
                class="delete-button"
                @click="
                  deleteKnowledgeFile(file)
                "
              >
                删除
              </button>

            </div>

          </div>

        </div>


        <!-- 知识库说明 -->

        <div class="knowledge-tip">

          <span>💡</span>

          <div>

            <strong>
              知识库工作方式
            </strong>

            <p>
              上传文件后，系统会自动解析文档、进行文本分片、
              向量化并保存到 Chroma 向量数据库。
              生成旅游行程时，AI Agent 会从知识库中检索相关资料。
            </p>

          </div>

        </div>

      </section>

    </main>

  </div>
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

.app {
  min-height: 100vh;

  background:
    radial-gradient(
      circle at 10% 0%,
      rgba(99, 102, 241, 0.05),
      transparent 30%
    ),
    #f5f7fb;
}


/* =========================
   Header
========================= */

.header {
  background: rgba(255, 255, 255, 0.94);
  border-bottom: 1px solid #e8ebf0;
  backdrop-filter: blur(10px);
}

.header-inner {
  width: min(1400px, 92%);
  margin: 0 auto;
  min-height: 82px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 25px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 13px;

  cursor: pointer;
}

.brand-icon {
  width: 44px;
  height: 44px;

  border-radius: 12px;

  display: flex;
  align-items: center;
  justify-content: center;

  background:
    linear-gradient(
      135deg,
      #6366f1,
      #4f46e5
    );

  color: white;
  font-size: 21px;

  box-shadow:
    0 7px 18px
    rgba(79, 70, 229, 0.2);
}

.header h1 {
  margin: 0;

  font-size: 22px;
  letter-spacing: -0.4px;
}

.header p {
  margin: 4px 0 0;

  color: #8a93a3;
  font-size: 13px;
}


/* =========================
   Navigation
========================= */

.nav {
  display: flex;
  align-items: center;
  gap: 4px;

  margin-left: auto;
}

.nav-item {
  height: 38px;

  padding: 0 14px;

  display: flex;
  align-items: center;
  gap: 6px;

  border: none;
  border-radius: 8px;

  background: transparent;

  color: #7b8493;

  font-size: 13px;
  cursor: pointer;

  transition: all 0.18s;
}

.nav-item:hover {
  background: #f5f3ff;
  color: #6366f1;
}

.nav-item.active {
  background: #f0efff;
  color: #4f46e5;
  font-weight: 600;
}

.header-badge {
  display: flex;
  align-items: center;
  gap: 7px;

  padding: 7px 12px;

  border-radius: 20px;

  background: #f5f3ff;
  color: #6366f1;

  font-size: 12px;
  font-weight: 600;
}

.badge-dot {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: #6366f1;
}


/* =========================
   Common
========================= */

.container {
  width: min(1400px, 92%);
  margin: 30px auto 50px;

  display: grid;

  grid-template-columns: 370px 1fr;

  gap: 24px;

  align-items: start;
}

.panel,
.page-panel {
  background: white;

  border: 1px solid #e9ecf2;

  border-radius: 16px;

  box-shadow:
    0 5px 25px
    rgba(31, 41, 55, 0.045);
}


/* =========================
   Home
========================= */

.form-panel {
  padding: 28px;
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

  background: #f5f3ff;

  border-radius: 10px;

  font-size: 19px;
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
}

input[type="text"] {
  width: 100%;
  height: 44px;

  padding: 0 12px 0 39px;

  border: 1px solid #dfe3ea;

  border-radius: 9px;

  outline: none;

  background: #fafbfc;

  transition: all 0.2s;
}

input[type="text"]:focus {
  border-color: #818cf8;
  background: white;

  box-shadow:
    0 0 0 3px
    rgba(99, 102, 241, 0.08);
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
}

.days-input button {
  width: 44px;
  height: 100%;

  border: none;

  background: transparent;

  color: #6366f1;

  font-size: 21px;

  cursor: pointer;
}

.days-input button:hover:not(:disabled) {
  background: #f0efff;
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

  transition: all 0.18s;
}

.interest-option:hover {
  border-color: #b7b8f6;
  color: #6366f1;
}

.interest-option.active {
  border-color: #818cf8;

  background: #f4f3ff;

  color: #4f46e5;

  font-weight: 600;
}

.interest-option input {
  display: none;
}

.pace-options {
  display: grid;

  grid-template-columns:
    repeat(3, 1fr);

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

  transition: all 0.18s;
}

.pace-options button strong {
  font-size: 16px;
  font-weight: normal;
}

.pace-options button span {
  font-size: 12px;
}

.pace-options button:hover {
  border-color: #b7b8f6;
}

.pace-options button.active {
  border-color: #818cf8;

  background: #f4f3ff;

  color: #4f46e5;
}

.submit-button {
  width: 100%;
  height: 46px;

  margin-top: 28px;

  border: none;

  border-radius: 9px;

  background:
    linear-gradient(
      135deg,
      #6366f1,
      #4f46e5
    );

  color: white;

  font-size: 14px;
  font-weight: 600;

  cursor: pointer;

  box-shadow:
    0 8px 18px
    rgba(79, 70, 229, 0.18);

  transition: all 0.2s;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-1px);

  box-shadow:
    0 10px 22px
    rgba(79, 70, 229, 0.24);
}

.submit-button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
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
}


/* =========================
   Result
========================= */

.result-panel {
  min-height: 680px;

  padding: 28px 32px 36px;
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

  color: #6366f1;

  font-size: 12px;
}

.loading-dot {
  width: 7px;
  height: 7px;

  border-radius: 50%;

  background: #6366f1;

  animation: pulse 1.2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.35;
  }

  50% {
    opacity: 1;
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

  transition: all 0.18s;
}

.export-button:hover {
  border-color: #a5a7ee;

  color: #4f46e5;

  background: #fafaff;
}


/* =========================
   Status
========================= */

.status-box {
  margin-top: 20px;

  padding: 15px 17px;

  border: 1px solid #e8eaf5;

  border-radius: 11px;

  background:
    linear-gradient(
      135deg,
      #fafaff,
      #f8f9fc
    );
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
  color: #6366f1;
}

.status-state {
  padding: 3px 8px;

  border-radius: 10px;

  background: #f0efff;

  color: #6366f1;

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

  min-height: 25px;

  color: #7b8493;

  font-size: 12px;
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
}

.status-icon.finished {
  background: #dcfce7;
  color: #16a34a;
}

.status-icon.current {
  background: #ede9fe;
  color: #6366f1;

  animation: statusPulse 1s infinite;
}

@keyframes statusPulse {
  50% {
    opacity: 0.35;
  }
}


/* =========================
   Empty
========================= */

.empty {
  min-height: 520px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  color: #9ca3af;

  text-align: center;
}

.empty-illustration {
  width: 92px;
  height: 92px;

  margin-bottom: 18px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #f4f3ff;
}

.plane {
  color: #6366f1;

  font-size: 40px;

  transform: rotate(-10deg);
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
}

.generating {
  min-height: 300px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  color: #9ca3af;
}

.generating-icon {
  margin-bottom: 15px;

  color: #6366f1;

  font-size: 34px;

  animation: rotate 1.8s linear infinite;
}

.generating p {
  margin: 0 0 5px;

  color: #6b7280;

  font-size: 14px;
}

.generating span {
  font-size: 12px;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}


/* =========================
   Markdown
========================= */

.markdown-body {
  padding: 26px 8px 10px;

  color: #374151;

  line-height: 1.85;

  font-size: 14px;
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

  font-size: 16px;
}

.markdown-body p {
  margin: 9px 0;
}

.markdown-body ul,
.markdown-body ol {
  padding-left: 24px;
}

.markdown-body li {
  margin: 5px 0;
}

.markdown-body strong {
  color: #374151;
}


/* =========================
   Common Page
========================= */

.page-container {
  width: min(1200px, 92%);

  margin: 30px auto 60px;
}

.page-panel {
  padding: 30px;
}

.page-header {
  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 20px;

  padding-bottom: 22px;

  border-bottom: 1px solid #edf0f3;
}

.page-header h2 {
  margin: 0;

  font-size: 21px;

  color: #1f2937;
}

.page-header p {
  margin: 7px 0 0;

  color: #9aa2b1;

  font-size: 13px;
}

.primary-small-button {
  height: 36px;

  padding: 0 15px;

  border: none;

  border-radius: 8px;

  background:
    linear-gradient(
      135deg,
      #6366f1,
      #4f46e5
    );

  color: white;

  font-size: 12px;

  font-weight: 600;

  cursor: pointer;

  transition: all 0.18s;
}

.primary-small-button:hover {
  transform: translateY(-1px);

  box-shadow:
    0 5px 15px
    rgba(79, 70, 229, 0.2);
}


/* =========================
   History
========================= */

.history-list {
  padding-top: 22px;

  display: flex;

  flex-direction: column;

  gap: 12px;
}

.history-card {
  min-height: 105px;

  padding: 18px 20px;

  display: flex;

  align-items: center;

  gap: 16px;

  border: 1px solid #e8ebf0;

  border-radius: 12px;

  background: #fff;

  cursor: pointer;

  transition: all 0.2s;
}

.history-card:hover {
  border-color: #c9c8f8;

  background: #fcfcff;

  transform: translateY(-1px);

  box-shadow:
    0 6px 18px
    rgba(31, 41, 55, 0.06);
}

.history-card-icon {
  width: 46px;
  height: 46px;

  flex-shrink: 0;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 12px;

  background: #f4f3ff;

  font-size: 21px;
}

.history-card-content {
  flex: 1;
}

.history-card-title {
  color: #374151;

  font-size: 15px;

  font-weight: 600;
}

.history-card-info {
  display: flex;

  gap: 16px;

  margin-top: 7px;

  color: #9aa2b1;

  font-size: 11px;
}

.history-card-tags {
  display: flex;

  gap: 6px;

  margin-top: 9px;

  flex-wrap: wrap;
}

.history-card-tags span,
.interest-tags span {
  padding: 4px 8px;

  border-radius: 12px;

  background: #f5f3ff;

  color: #6366f1;

  font-size: 10px;
}

.history-card-arrow {
  color: #b1b7c3;

  font-size: 20px;
}


/* =========================
   History Detail
========================= */

.history-detail {
  padding-top: 20px;
}

.detail-header {
  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 15px;

  margin-bottom: 20px;
}

.back-button {
  border: none;

  background: transparent;

  color: #6366f1;

  font-size: 13px;

  cursor: pointer;
}

.detail-actions {
  display: flex;

  gap: 7px;
}

.trip-meta {
  display: grid;

  grid-template-columns:
    repeat(4, 1fr);

  gap: 12px;

  margin-bottom: 16px;
}

.trip-meta > div {
  padding: 14px;

  border-radius: 10px;

  background: #f8f9fc;
}

.trip-meta span {
  display: block;

  margin-bottom: 5px;

  color: #9aa2b1;

  font-size: 11px;
}

.trip-meta strong {
  color: #374151;

  font-size: 13px;
}

.trip-interests {
  display: flex;

  align-items: center;

  gap: 12px;

  padding: 13px 15px;

  margin-bottom: 10px;

  border-radius: 10px;

  background: #f8f9fc;

  color: #7b8493;

  font-size: 12px;
}

.interest-tags {
  display: flex;

  gap: 6px;

  flex-wrap: wrap;
}

.history-markdown {
  padding-top: 20px;
}


/* =========================
   Loading / Empty
========================= */

.page-loading {
  min-height: 350px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  gap: 12px;

  color: #9aa2b1;

  font-size: 13px;
}

.page-loading.small {
  min-height: 180px;
}

.loading-spinner {
  color: #6366f1;

  font-size: 30px;

  animation:
    rotate 1.5s linear infinite;
}

.page-error {
  min-height: 350px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  gap: 15px;

  color: #ef4444;

  font-size: 13px;
}

.page-empty {
  min-height: 430px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  text-align: center;

  color: #9aa2b1;
}

.large-empty-icon {
  width: 85px;
  height: 85px;

  display: flex;

  align-items: center;
  justify-content: center;

  margin-bottom: 16px;

  border-radius: 50%;

  background: #f4f3ff;

  font-size: 38px;
}

.page-empty h3 {
  margin: 0 0 8px;

  color: #4b5563;

  font-size: 17px;
}

.page-empty p {
  margin: 0 0 20px;

  font-size: 12px;
}


/* =========================
   Knowledge
========================= */

.knowledge-count {
  padding: 6px 11px;

  border-radius: 15px;

  background: #f5f3ff;

  color: #6366f1;

  font-size: 11px;

  font-weight: 600;
}

.upload-section {
  margin-top: 24px;

  padding: 35px;

  border: 1px dashed #cfd2df;

  border-radius: 14px;

  background: #fafaff;

  text-align: center;
}

.upload-icon {
  width: 58px;
  height: 58px;

  margin: 0 auto 13px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 15px;

  background: #f0efff;

  font-size: 25px;
}

.upload-section h3 {
  margin: 0;

  color: #374151;

  font-size: 16px;
}

.upload-section > p {
  margin: 7px 0 17px;

  color: #9aa2b1;

  font-size: 12px;
}

.choose-file-button {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  height: 36px;

  padding: 0 17px;

  border-radius: 8px;

  background: #6366f1;

  color: white;

  font-size: 12px;

  font-weight: 600;

  cursor: pointer;

  transition: all 0.18s;
}

.choose-file-button:hover {
  background: #4f46e5;
}

.selected-file {
  max-width: 650px;

  margin: 18px auto 0;

  padding: 11px 13px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 15px;

  border: 1px solid #e4e6ed;

  border-radius: 9px;

  background: white;

  text-align: left;
}

.selected-file-info {
  display: flex;

  align-items: center;

  gap: 10px;

  min-width: 0;
}

.file-icon {
  font-size: 23px;
}

.selected-file-info div {
  display: flex;

  flex-direction: column;

  min-width: 0;
}

.selected-file-info strong {
  max-width: 400px;

  overflow: hidden;

  text-overflow: ellipsis;

  white-space: nowrap;

  color: #374151;

  font-size: 12px;
}

.selected-file-info span {
  margin-top: 3px;

  color: #9aa2b1;

  font-size: 10px;
}

.upload-button {
  height: 32px;

  padding: 0 12px;

  flex-shrink: 0;

  border: none;

  border-radius: 7px;

  background: #6366f1;

  color: white;

  font-size: 11px;

  cursor: pointer;
}

.upload-button:disabled {
  opacity: 0.6;

  cursor: not-allowed;
}


/* =========================
   File List
========================= */

.file-section {
  margin-top: 30px;
}

.file-section-header {
  display: flex;

  align-items: center;

  justify-content: space-between;

  padding-bottom: 13px;

  border-bottom: 1px solid #edf0f3;
}

.file-section-header h3 {
  margin: 0;

  color: #374151;

  font-size: 15px;
}

.file-section-header p {
  margin: 5px 0 0;

  color: #9aa2b1;

  font-size: 11px;
}

.refresh-button {
  border: none;

  background: transparent;

  color: #6366f1;

  font-size: 12px;

  cursor: pointer;
}

.file-list {
  margin-top: 10px;

  display: flex;

  flex-direction: column;

  gap: 8px;
}

.file-card {
  min-height: 64px;

  padding: 11px 14px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 15px;

  border: 1px solid #e8ebf0;

  border-radius: 9px;

  transition: all 0.18s;
}

.file-card:hover {
  border-color: #d2d1f7;

  background: #fcfcff;
}

.file-main {
  display: flex;

  align-items: center;

  gap: 12px;

  min-width: 0;
}

.file-icon-large {
  width: 39px;
  height: 39px;

  flex-shrink: 0;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 9px;

  background: #f8f9fc;

  font-size: 20px;
}

.file-info {
  display: flex;

  flex-direction: column;

  min-width: 0;
}

.file-info strong {
  overflow: hidden;

  text-overflow: ellipsis;

  white-space: nowrap;

  color: #374151;

  font-size: 13px;
}

.file-info span {
  margin-top: 4px;

  color: #9aa2b1;

  font-size: 10px;
}

.delete-button {
  height: 30px;

  padding: 0 11px;

  flex-shrink: 0;

  border: 1px solid #fee2e2;

  border-radius: 7px;

  background: white;

  color: #ef4444;

  font-size: 11px;

  cursor: pointer;

  transition: all 0.18s;
}

.delete-button:hover {
  background: #fef2f2;

  border-color: #fecaca;
}

.file-empty {
  min-height: 220px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  text-align: center;

  color: #9aa2b1;
}

.file-empty > div {
  margin-bottom: 10px;

  font-size: 30px;
}

.file-empty p {
  margin: 0 0 5px;

  color: #6b7280;

  font-size: 13px;
}

.file-empty span {
  max-width: 420px;

  font-size: 11px;

  line-height: 18px;
}

.knowledge-tip {
  margin-top: 25px;

  padding: 14px 16px;

  display: flex;

  gap: 10px;

  border-radius: 9px;

  background: #f8f9fc;

  color: #9aa2b1;

  font-size: 11px;

  line-height: 18px;
}

.knowledge-tip strong {
  color: #6b7280;
}

.knowledge-tip p {
  margin: 4px 0 0;
}


/* =========================
   Responsive
========================= */

@media (max-width: 1000px) {

  .header-inner {
    flex-wrap: wrap;

    padding: 14px 0;
  }

  .nav {
    order: 3;

    width: 100%;

    justify-content: center;

    margin-left: 0;
  }

  .container {
    grid-template-columns: 1fr;
  }

  .trip-meta {
    grid-template-columns:
      repeat(2, 1fr);
  }

}


@media (max-width: 700px) {

  .header-badge {
    display: none;
  }

  .page-panel,
  .form-panel,
  .result-panel {
    padding: 20px;
  }

  .result-header,
  .page-header,
  .detail-header {
    flex-direction: column;
  }

  .result-actions,
  .detail-actions {
    justify-content: flex-start;
  }

  .history-card {
    padding: 14px;
  }

  .history-card-info {
    flex-direction: column;

    gap: 3px;
  }

  .trip-meta {
    grid-template-columns: 1fr;
  }

  .selected-file {
    flex-direction: column;

    align-items: stretch;
  }

  .upload-button {
    width: 100%;
  }

  .nav-item {
    flex: 1;

    justify-content: center;

    padding: 0 8px;
  }

}
</style>