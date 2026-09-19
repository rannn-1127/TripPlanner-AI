# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).

```text
                 TripPlanner-AI
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       行程规划      历史记录       知识库
          │            │            │
          │            │            ├── 上传文件
          │            │            ├── 文件列表
          │            │            └── 删除文件
          │            │
          │            ├── 历史列表
          │            └── 查看详情
          │
          ├── 输入目的地
          ├── 输入偏好
          ├── SSE生成
          └── Markdown结果
```