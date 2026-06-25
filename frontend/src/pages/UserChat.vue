<template>
  <div class="chat-page">
    <div class="chat-header">
      <h2 class="chat-title">聊天</h2>
      <div class="chat-subtitle">与你的健身房智能助手对话</div>
    </div>

    <el-card class="chat-card" shadow="never">
      <el-scrollbar ref="scrollbarRef" class="chat-scroll">
        <div class="chat-list">
          <div v-for="m in messages" :key="m.id" class="chat-row" :class="m.role">
            <div class="bubble">
              <div class="bubble-meta">{{ m.role === 'user' ? '我' : 'AI' }}</div>
              <div class="bubble-text">{{ m.text }}</div>
            </div>
          </div>
        </div>
      </el-scrollbar>

      <div class="chat-input">
        <el-input
          v-model="draft"
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 4 }"
          placeholder="输入你想问的问题，例如：如何安排每周训练计划？"
          @keydown.enter.exact.prevent="send()"
        />
        <div class="chat-actions">
          <el-radio-group v-model="chatMode" size="small">
            <el-radio-button label="rag">知识问答</el-radio-button>
            <el-radio-button label="agent">智能助手</el-radio-button>
          </el-radio-group>
          <el-button :disabled="isSending || !draft.trim()" type="primary" @click="send()">
            {{ isSending ? '发送中…' : '发送' }}
          </el-button>
          <el-button :disabled="isSending || messages.length <= 1" @click="clearChat()">清空</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import axios from 'axios'

type ChatRole = 'user' | 'assistant'
type ChatMessage = {
  id: string
  role: ChatRole
  text: string
  createdAt: number
}

const draft = ref('')
const isSending = ref(false)
const scrollbarRef = ref<any>(null)
const ragSessionId = ref('')
const chatMode = ref<'rag' | 'agent'>('rag')

const messages = ref<ChatMessage[]>([
  {
    id: crypto.randomUUID(),
    role: 'assistant',
    text: '你好，我是系统内置的 AI 助手。你可以问我训练计划、饮食建议或课程安排相关的问题。',
    createdAt: Date.now()
  }
])

onMounted(async () => {
  try {
    const res = await axios.post('/api/chat/session/create')
    if (res.data.success) {
      ragSessionId.value = res.data.sessionId
    }
  } catch (e) {
    console.error('创建会话失败', e)
  }
})

function pushMessage(role: ChatRole, text: string) {
  messages.value.push({
    id: crypto.randomUUID(),
    role,
    text,
    createdAt: Date.now()
  })
}

async function scrollToBottom() {
  await nextTick()
  if (scrollbarRef.value) {
    const wrap = scrollbarRef.value.wrapRef
    if (wrap) {
      wrap.scrollTop = wrap.scrollHeight
    }
  }
}

async function send() {
  const content = draft.value.trim()
  if (!content || isSending.value) return

  draft.value = ''
  pushMessage('user', content)
  isSending.value = true

  const aiMsgId = crypto.randomUUID()
  messages.value.push({
    id: aiMsgId,
    role: 'assistant',
    text: '',
    createdAt: Date.now()
  })

  await scrollToBottom()

  const memberAccount = localStorage.getItem('memberAccount') ?? ''

  // 根据模式选择不同接口
  const apiPath = chatMode.value === 'agent'
    ? `/api/chat/agent/stream?${new URLSearchParams({ content, memberAccount }).toString()}`
    : `/api/chat/stream?${new URLSearchParams({ content, memberAccount, ragSessionId: ragSessionId.value }).toString()}`

  const source = new EventSource(apiPath)

  source.onmessage = (event) => {
    if (event.data === '[DONE]') {
      source.close()
      isSending.value = false
      return
    }
    const aiMsg = messages.value.find(m => m.id === aiMsgId)
    if (aiMsg) {
      aiMsg.text += event.data
    }
    scrollToBottom()
  }

  source.onerror = () => {
    source.close()
    isSending.value = false
    const aiMsg = messages.value.find(m => m.id === aiMsgId)
    if (aiMsg && !aiMsg.text) {
      aiMsg.text = '请求失败，请稍后重试'
    }
  }
}

function clearChat() {
  messages.value = [messages.value[0]].filter(Boolean) as ChatMessage[]
}
</script>

<style scoped>
.chat-page {
  padding: 24px;
}

.chat-header {
  margin-bottom: 12px;
}

.chat-title {
  margin: 0;
}

.chat-subtitle {
  color: #666;
  margin-top: 6px;
  font-size: 13px;
}

.chat-card {
  border: 1px solid #ebeef5;
}

.chat-scroll {
  height: min(60svh, 520px);
  padding: 8px 8px 0 8px;
}

.chat-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-bottom: 8px;
}

.chat-row {
  display: flex;
}

.chat-row.user {
  justify-content: flex-end;
}

.chat-row.assistant {
  justify-content: flex-start;
}

.bubble {
  max-width: min(680px, 88%);
  padding: 10px 12px;
  border-radius: 12px;
  line-height: 1.5;
  border: 1px solid rgba(0, 0, 0, 0.06);
  background: #ffffff;
}

.chat-row.assistant .bubble {
  background: #f8f9fa;
}

.chat-row.user .bubble {
  background: #ecf5ff;
  border-color: rgba(64, 158, 255, 0.25);
}

.bubble-meta {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.55);
  margin-bottom: 4px;
}

.chat-row.user .bubble-meta {
  text-align: right;
}

.chat-row.assistant .bubble-meta {
  text-align: left;
}

.bubble-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.chat-input {
  border-top: 1px solid #ebeef5;
  padding: 12px;
  display: grid;
  gap: 10px;
}

.chat-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  align-items: center;
}
</style>