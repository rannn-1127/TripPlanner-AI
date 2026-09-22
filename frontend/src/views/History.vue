<template>
  <main class="history-page">
    <div class="history-container">

      <!-- 页面标题 -->
      <div class="page-header">
        <h1>历史行程</h1>
        <p>查看之前生成的旅游攻略</p>
      </div>

      <div class="history-layout">

        <!-- 左侧历史列表 -->
        <section class="history-list">
          <div class="section-title">
            <h2>我的行程</h2>
            <span>{{ trips.length }} 条</span>
          </div>

          <!-- 加载中 -->
          <div v-if="loading" class="empty-state">
            正在加载历史行程...
          </div>

          <!-- 没有历史记录 -->
          <div v-else-if="trips.length === 0" class="empty-state">
            <div class="empty-icon">🗺️</div>
            <p>还没有历史行程</p>
            <button @click="$router.push('/')">
              去生成行程
            </button>
          </div>

          <!-- 历史记录 -->
          <div
            v-else
            v-for="trip in trips"
            :key="trip.id"
            class="trip-card"
            :class="{ active: selectedTripId === trip.id }"
            @click="loadTripDetail(trip.id)"
          >
            <div class="trip-card-top">
              <h3>{{ trip.destination }}</h3>

              <div class="trip-card-actions">
                <span class="trip-days">
                  {{ trip.days }}天
                </span>

                <button
                  class="delete-button"
                  @click.stop="deleteHistory(trip.id)"
                >
                  删除
                </button>
              </div>
            </div>

            <div class="trip-info">
              <span>
                兴趣：{{ trip.interests?.join("、") || "未设置" }}
              </span>
            </div>

            <div class="trip-bottom">
              <span>节奏：{{ trip.pace }}</span>
              <span>{{ trip.created_at }}</span>
            </div>
          </div>
        </section>

        <!-- 右侧详情 -->
        <section class="history-detail">

          <!-- 未选择行程 -->
          <div v-if="!selectedTrip" class="detail-empty">
            <div class="detail-icon">📖</div>
            <h2>选择一份行程</h2>
            <p>点击左侧历史记录查看完整旅游攻略</p>
          </div>

          <!-- 行程详情 -->
          <div v-else class="detail-content">

            <div class="detail-header">

              <div class="detail-title">
                <h2>
                  {{ selectedTrip.destination }}
                  {{ selectedTrip.days }}天旅游行程
                </h2>

                <div class="detail-meta">
                  <span>
                    兴趣：
                    {{ selectedTrip.interests?.join("、") || "未设置" }}
                  </span>

                  <span>
                    节奏：{{ selectedTrip.pace }}
                  </span>

                  <span>
                    创建时间：{{ selectedTrip.created_at }}
                  </span>
                </div>
              </div>

              <!-- 操作按钮 -->
              <div class="detail-actions">

                <button
                  class="export-button"
                  :disabled="exporting"
                  @click="exportTrip('md')"
                >
                  Markdown
                </button>

                <button
                  class="export-button"
                  :disabled="exporting"
                  @click="exportTrip('word')"
                >
                  Word
                </button>

                <button
                  class="export-button"
                  :disabled="exporting"
                  @click="exportTrip('excel')"
                >
                  Excel
                </button>

                <button
                  class="back-button"
                  @click="selectedTrip = null"
                >
                  返回
                </button>

              </div>
            </div>

            <div
              class="markdown-body"
              v-html="renderMarkdown(selectedTrip.content)"
            >
            </div>

          </div>

        </section>

      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { marked } from "marked"

const trips = ref([])
const selectedTrip = ref(null)
const selectedTripId = ref(null)
const loading = ref(false)
const exporting = ref(false)


// 获取历史行程列表
async function loadHistory() {
  loading.value = true

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/history"
    )

    if (!response.ok) {
      throw new Error("获取历史行程失败")
    }

    const data = await response.json()

    trips.value = data.trips || []

  } catch (error) {
    console.error("获取历史行程失败：", error)
  } finally {
    loading.value = false
  }
}


// 获取某一条行程详情
async function loadTripDetail(tripId) {
  selectedTripId.value = tripId

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/history/${tripId}`
    )

    if (!response.ok) {
      throw new Error("获取行程详情失败")
    }

    selectedTrip.value = await response.json()

  } catch (error) {
    console.error("获取行程详情失败：", error)

    selectedTrip.value = null
  }
}


// 删除历史行程
async function deleteHistory(tripId) {
  const confirmed = window.confirm(
    "确定要删除这条历史行程吗？"
  )

  if (!confirmed) {
    return
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/history/${tripId}`,
      {
        method: "DELETE"
      }
    )

    if (!response.ok) {
      throw new Error("删除历史行程失败")
    }

    // 从前端列表中移除
    trips.value = trips.value.filter(
      trip => trip.id !== tripId
    )

    // 如果删除的是当前正在查看的行程
    if (selectedTripId.value === tripId) {
      selectedTripId.value = null
      selectedTrip.value = null
    }

  } catch (error) {
    console.error("删除历史行程失败：", error)

    window.alert("删除失败，请稍后重试")
  }
}


// 导出旅游行程
async function exportTrip(format) {
  if (!selectedTrip.value) {
    return
  }

  exporting.value = true

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/export/trip/${selectedTrip.value.id}?format=${format}`,
      {
        method: "POST"
      }
    )

    if (!response.ok) {
      throw new Error("导出失败")
    }

    // 获取文件数据
    const blob = await response.blob()

    // 创建临时下载地址
    const url = window.URL.createObjectURL(blob)

    // 创建下载链接
    const link = document.createElement("a")
    link.href = url

    // 根据导出格式确定文件后缀
    const extension = {
      md: "md",
      word: "docx",
      excel: "xlsx"
    }

    link.download =
      `${selectedTrip.value.destination}${selectedTrip.value.days}天旅游攻略.${extension[format]}`

    document.body.appendChild(link)
    link.click()

    // 清理临时元素和 URL
    link.remove()
    window.URL.revokeObjectURL(url)

  } catch (error) {
    console.error("导出旅游行程失败：", error)

    window.alert("导出失败，请稍后重试")

  } finally {
    exporting.value = false
  }
}


// Markdown 转 HTML
function renderMarkdown(content) {
  if (!content) {
    return ""
  }

  return marked.parse(content)
}


// 页面加载时获取历史记录
onMounted(() => {
  loadHistory()
})
</script>

<style scoped>
.history-page {
  min-height: calc(100vh - 64px);
  padding: 40px 24px;
  background: linear-gradient(180deg, #fffaf2, #ffffff);
}

.history-container {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  margin: 0 0 8px;
  font-size: 34px;
  font-weight: 700;
  background: linear-gradient(135deg,#f59e0b,#fb923c);
  -webkit-background-clip:text;
  color:transparent;
}

.page-header p {
  margin:0;
  color:#999;
  font-size:15px;
}

.history-layout {
  display:grid;
  grid-template-columns:380px 1fr;
  gap:24px;
  min-height:650px;
}

.history-list,
.history-detail {
  padding:26px;
  border-radius:22px;
  background:rgba(255,255,255,.8);
  backdrop-filter:blur(12px);
  border:1px solid rgba(245,158,11,.15);
  box-shadow:0 10px 35px rgba(0,0,0,.05);
}

/* 左侧标题 */

.section-title {
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:22px;
}

.section-title h2 {
  margin:0;
  font-size:21px;
}

.section-title span {
  padding:4px 12px;
  border-radius:20px;
  background:#fff3d6;
  color:#d97706;
  font-size:13px;
}

/* 行程卡片 */

.trip-card {
  padding:18px;
  margin-bottom:14px;
  border-radius:16px;
  border:1px solid #f1e7d5;
  background:#fff;
  cursor:pointer;
  transition:.25s;
}

.trip-card:hover {
  transform:translateY(-3px);
  border-color:#f59e0b;
  box-shadow:0 8px 20px rgba(245,158,11,.12);
}

.trip-card.active {
  border-color:#f59e0b;
  background:linear-gradient(
    135deg,
    #fffaf0,
    #fff
  );
  box-shadow:0 8px 25px rgba(245,158,11,.18);
}

.trip-card-top {
  display:flex;
  justify-content:space-between;
  align-items:center;
}

.trip-card-top h3 {
  margin:0;
  font-size:18px;
}

.trip-card-actions {
  display:flex;
  align-items:center;
  gap:10px;
}

.trip-days {
  padding:3px 10px;
  border-radius:20px;
  background:#fff3d6;
  color:#d97706;
  font-size:13px;
}

.delete-button {
  padding:4px 8px;
  border:none;
  border-radius:8px;
  background:transparent;
  color:#aaa;
  cursor:pointer;
}

.delete-button:hover {
  color:#ef4444;
  background:#fff1f2;
}

.trip-info {
  margin-top:14px;
  font-size:14px;
  color:#666;
}

.trip-bottom {
  display:flex;
  justify-content:space-between;
  gap:10px;
  margin-top:14px;
  font-size:12px;
  color:#999;
}


/* 详情区域 */

.history-detail {
  min-width:0;
}

.detail-empty {
  min-height:500px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  text-align:center;
  color:#999;
}

.detail-icon {
  font-size:50px;
  margin-bottom:18px;
}

.detail-empty h2 {
  margin:0 0 8px;
  color:#444;
}


/* 详情头 */

.detail-header {
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  gap:20px;
  margin-bottom:30px;
  padding-bottom:22px;
  border-bottom:1px solid #f3e8d2;
}

.detail-header h2 {
  margin:0 0 14px;
  font-size:27px;
}

.detail-meta {
  display:flex;
  flex-wrap:wrap;
  gap:12px;
  font-size:14px;
  color:#777;
}

.detail-meta span {
  padding:5px 12px;
  border-radius:20px;
  background:#fff8e7;
}


/* 按钮 */

.detail-actions {
  display:flex;
  gap:8px;
  flex-wrap:wrap;
}

.export-button,
.back-button {
  padding:9px 16px;
  border-radius:10px;
  cursor:pointer;
  transition:.2s;
}

.export-button {
  border:none;
  background:linear-gradient(
    135deg,
    #f59e0b,
    #fb923c
  );
  color:white;
}

.export-button:hover:not(:disabled) {
  transform:translateY(-2px);
  box-shadow:0 6px 15px rgba(245,158,11,.25);
}

.export-button:disabled {
  opacity:.5;
}

.back-button {
  border:1px solid #f3d9a8;
  background:white;
  color:#d97706;
}

.back-button:hover {
  background:#fff7ed;
}


/* Markdown */

.markdown-body {
  line-height:1.8;
  color:#333;
}

.markdown-body :deep(h1) {
  margin-top:0;
  color:#d97706;
}

.markdown-body :deep(h2) {
  margin-top:30px;
  padding-left:12px;
  border-left:4px solid #f59e0b;
}

.markdown-body :deep(h3) {
  margin-top:22px;
}

.markdown-body :deep(li) {
  margin:7px 0;
}


/* 空状态 */

.empty-state {
  padding:60px 20px;
  text-align:center;
  color:#999;
}

.empty-icon {
  font-size:42px;
  margin-bottom:15px;
}

.empty-state button {
  margin-top:15px;
  padding:10px 20px;
  border:none;
  border-radius:12px;
  background:linear-gradient(
    135deg,
    #f59e0b,
    #fb923c
  );
  color:white;
  cursor:pointer;
}


/* 移动端 */

@media(max-width:900px){

.history-layout{
  grid-template-columns:1fr;
}

.history-list{
  max-height:500px;
  overflow-y:auto;
}

.detail-header{
  flex-direction:column;
}

}
</style>