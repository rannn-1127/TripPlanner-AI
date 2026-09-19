<template>
  <main class="knowledge-page">
    <div class="knowledge-container">

      <!-- 页面标题 -->
      <div class="page-header">
        <h1>知识库管理</h1>
        <p>上传和管理旅游目的地资料</p>
      </div>

      <!-- 上传区域 -->
      <section class="upload-section">
        <div class="section-header">
          <div>
            <h2>上传资料</h2>
            <p>支持 PDF、Word、TXT 文件</p>
          </div>
        </div>

        <div class="upload-box">
          <input
            ref="fileInput"
            type="file"
            accept=".pdf,.docx,.txt"
            @change="handleFileChange"
            hidden
          />

          <div class="upload-icon">📄</div>

          <p v-if="!selectedFile">
            选择旅游资料文件
          </p>

          <p v-else class="selected-file">
            已选择：{{ selectedFile.name }}
          </p>

          <button
            class="select-button"
            @click="fileInput.click()"
          >
            选择文件
          </button>

          <button
            v-if="selectedFile"
            class="upload-button"
            :disabled="uploading"
            @click="uploadFile"
          >
            {{ uploading ? "正在上传..." : "上传到知识库" }}
          </button>
        </div>

        <!-- 上传提示 -->
        <div v-if="message" class="message">
          {{ message }}
        </div>
      </section>

      <!-- 文件列表 -->
      <section class="files-section">
        <div class="section-header">
          <div>
            <h2>知识库文件</h2>
            <p>当前已上传的旅游资料</p>
          </div>

          <button
            class="refresh-button"
            @click="loadFiles"
          >
            刷新
          </button>
        </div>

        <!-- 加载 -->
        <div v-if="loading" class="empty-state">
          正在加载文件...
        </div>

        <!-- 没有文件 -->
        <div
          v-else-if="files.length === 0"
          class="empty-state"
        >
          <div class="empty-icon">📚</div>
          <p>知识库暂时没有文件</p>
        </div>

        <!-- 文件列表 -->
        <div v-else class="file-list">
          <div
            v-for="filename in files"
            :key="filename"
            class="file-item"
          >
            <div class="file-info">
              <div class="file-icon">
                {{ getFileIcon(filename) }}
              </div>

              <div>
                <h3>{{ filename }}</h3>
                <p>旅游知识库资料</p>
              </div>
            </div>

            <button
              class="delete-button"
              @click="deleteFile(filename)"
            >
              删除
            </button>
          </div>
        </div>
      </section>

    </div>
  </main>
</template>

<script setup>
import { onMounted, ref } from "vue"

const files = ref([])
const selectedFile = ref(null)
const fileInput = ref(null)

const loading = ref(false)
const uploading = ref(false)
const message = ref("")


// 获取知识库文件
async function loadFiles() {
  loading.value = true
  message.value = ""

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/knowledge/files"
    )

    if (!response.ok) {
      throw new Error("获取知识库文件失败")
    }

    const data = await response.json()

    files.value = data.files || []

  } catch (error) {
    console.error("获取知识库文件失败：", error)
    message.value = "获取知识库文件失败"
  } finally {
    loading.value = false
  }
}


// 选择文件
function handleFileChange(event) {
  const file = event.target.files[0]

  if (!file) {
    selectedFile.value = null
    return
  }

  const allowedExtensions = [".pdf", ".docx", ".txt"]
  const extension = file.name
    .substring(file.name.lastIndexOf("."))
    .toLowerCase()

  if (!allowedExtensions.includes(extension)) {
    message.value = "只支持 PDF、Word、TXT 文件"
    selectedFile.value = null
    return
  }

  selectedFile.value = file
  message.value = ""
}


// 上传文件
async function uploadFile() {
  if (!selectedFile.value) {
    message.value = "请先选择文件"
    return
  }

  uploading.value = true
  message.value = ""

  try {
    const formData = new FormData()

    formData.append("file", selectedFile.value)

    const response = await fetch(
      "http://127.0.0.1:8000/knowledge/upload",
      {
        method: "POST",
        body: formData
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || "文件上传失败")
    }

    message.value = "文件上传成功"

    selectedFile.value = null

    if (fileInput.value) {
      fileInput.value.value = ""
    }

    await loadFiles()

  } catch (error) {
    console.error("文件上传失败：", error)
    message.value = error.message || "文件上传失败"
  } finally {
    uploading.value = false
  }
}


// 删除文件
async function deleteFile(filename) {
  const confirmed = window.confirm(
    `确定要删除「${filename}」吗？`
  )

  if (!confirmed) {
    return
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/knowledge/file/${encodeURIComponent(filename)}`,
      {
        method: "DELETE"
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || "删除文件失败")
    }

    message.value = "文件删除成功"

    await loadFiles()

  } catch (error) {
    console.error("删除文件失败：", error)
    message.value = error.message || "删除文件失败"
  }
}


// 根据文件类型显示图标
function getFileIcon(filename) {
  const extension = filename
    .substring(filename.lastIndexOf("."))
    .toLowerCase()

  if (extension === ".pdf") {
    return "📕"
  }

  if (extension === ".docx") {
    return "📘"
  }

  if (extension === ".txt") {
    return "📄"
  }

  return "📁"
}


// 页面加载时获取文件
onMounted(() => {
  loadFiles()
})
</script>

<style scoped>
.knowledge-page {
  min-height: calc(100vh - 64px);
  padding: 40px 24px;
}

.knowledge-container {
  max-width: 1100px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0 0 8px;
  font-size: 32px;
}

.page-header p {
  margin: 0;
  color: #888;
}

.upload-section,
.files-section {
  padding: 28px;
  margin-bottom: 24px;
  border: 1px solid #eee;
  border-radius: 16px;
  background: #fff;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  margin: 0 0 6px;
  font-size: 21px;
}

.section-header p {
  margin: 0;
  color: #999;
  font-size: 14px;
}

/* 上传区域 */

.upload-box {
  padding: 45px 20px;
  border: 2px dashed #ddd;
  border-radius: 14px;
  text-align: center;
}

.upload-icon {
  margin-bottom: 15px;
  font-size: 42px;
}

.upload-box p {
  margin: 0 0 18px;
  color: #666;
}

.selected-file {
  color: #333 !important;
  font-weight: 500;
}

.select-button,
.upload-button,
.refresh-button,
.delete-button {
  padding: 9px 18px;
  border-radius: 8px;
  cursor: pointer;
}

.select-button {
  border: 1px solid #ddd;
  background: #fff;
}

.select-button:hover {
  background: #f5f5f5;
}

.upload-button {
  margin-left: 10px;
  border: none;
  background: #333;
  color: #fff;
}

.upload-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.message {
  margin-top: 15px;
  color: #666;
  font-size: 14px;
}

/* 文件列表 */

.file-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 18px;
  border: 1px solid #eee;
  border-radius: 12px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.file-icon {
  font-size: 28px;
}

.file-info h3 {
  margin: 0 0 5px;
  font-size: 16px;
  word-break: break-all;
}

.file-info p {
  margin: 0;
  color: #999;
  font-size: 13px;
}

.delete-button {
  flex-shrink: 0;
  border: 1px solid #ddd;
  background: #fff;
  color: #666;
}

.delete-button:hover {
  background: #f5f5f5;
}

.refresh-button {
  border: 1px solid #ddd;
  background: #fff;
}

.refresh-button:hover {
  background: #f5f5f5;
}

/* 空状态 */

.empty-state {
  padding: 50px 20px;
  text-align: center;
  color: #999;
}

.empty-icon {
  margin-bottom: 12px;
  font-size: 40px;
}

@media (max-width: 700px) {
  .knowledge-page {
    padding: 24px 15px;
  }

  .upload-section,
  .files-section {
    padding: 20px;
  }

  .file-item {
    align-items: flex-start;
  }

  .section-header {
    align-items: flex-start;
  }
}
</style>