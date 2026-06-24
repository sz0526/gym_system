<template>
  <div class="auth-page">
    <div class="auth-backdrop" aria-hidden="true">
      <div class="auth-shape auth-shape-1" />
      <div class="auth-shape auth-shape-2" />
      <div class="auth-shape auth-shape-3" />
    </div>

    <div class="auth-card" role="main" aria-labelledby="login-title">
      <div class="auth-header">
        <div class="auth-brand">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M6.5 6C6.5 4.067 8.067 2.5 10 2.5H14C15.933 2.5 17.5 4.067 17.5 6V10C17.5 11.933 15.933 13.5 14 13.5H10C8.067 13.5 6.5 11.933 6.5 10V6Z" stroke="currentColor" stroke-width="1.5"/>
            <path d="M3.5 14C3.5 12.067 5.067 10.5 7 10.5H9V14C9 15.933 7.433 17.5 5.5 17.5C4.11929 17.5 3 16.3807 3 15V14H3.5Z" stroke="currentColor" stroke-width="1.5"/>
            <path d="M20.5 14C20.5 12.067 18.933 10.5 17 10.5H15V14C15 15.933 16.567 17.5 18.5 17.5C19.8807 17.5 21 16.3807 21 15V14H20.5Z" stroke="currentColor" stroke-width="1.5"/>
            <path d="M12 13.5V21.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M8.5 21.5H15.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </div>
        <h1 id="login-title" class="auth-title">会员登录</h1>
        <p class="auth-subtitle">欢迎回来，请登录您的会员账号</p>
      </div>

      <form class="auth-form" @submit.prevent="submit">
        <div class="field-group">
          <label class="field-label" for="username">用户名</label>
          <div class="input-wrap" :class="{ 'is-error': msg }">
            <el-icon class="input-icon"><User /></el-icon>
            <input
              id="username"
              v-model="form.username"
              type="text"
              autocomplete="username"
              placeholder="请输入用户名"
            />
          </div>
        </div>

        <div class="field-group">
          <label class="field-label" for="password">密码</label>
          <div class="input-wrap" :class="{ 'is-error': msg }">
            <el-icon class="input-icon"><Lock /></el-icon>
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
              placeholder="请输入密码"
            />
            <button
              type="button"
              class="input-suffix"
              tabindex="-1"
              :aria-label="showPassword ? '隐藏密码' : '显示密码'"
              @click="showPassword = !showPassword"
            >
              <el-icon><View v-if="showPassword" /><Hide v-else /></el-icon>
            </button>
          </div>
        </div>

        <transition name="field-error">
          <div v-if="msg" class="form-error" role="alert">{{ msg }}</div>
        </transition>

        <button
          type="submit"
          class="auth-submit"
          :disabled="loading"
          :aria-busy="loading"
        >
          <el-icon v-if="loading" class="submit-icon is-spin"><Loading /></el-icon>
          <span>{{ loading ? '登录中…' : '登录' }}</span>
        </button>

        <div class="auth-footer auth-footer-split">
          <router-link to="/toUserRegister">注册新账号</router-link>
          <router-link to="/">管理员登录</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { postForm } from '../api/client'
import { Hide, Loading, Lock, User, View } from '@element-plus/icons-vue'

const router = useRouter()
const form = reactive({
  username: '',
  password: ''
})
const msg = ref('')
const loading = ref(false)
const showPassword = ref(false)

async function submit() {
  msg.value = ''
  if (!form.username.trim() || !form.password) {
    msg.value = '请输入账号和密码'
    return
  }

  loading.value = true
  try {
    const resp = await postForm('/api/userLogin', {
      username: form.username,
      password: form.password
    })
    if (resp.data && resp.data.success) {
      // 登录成功，把用户名存起来给 SSE 用
      localStorage.setItem('memberAccount', form.username)
      router.push('/toUserMain')
    } else {
      msg.value = resp.data?.message || '登录失败'
    }
  } catch (e: any) {
    msg.value = e?.response?.data?.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-footer-split {
  display: flex;
  justify-content: space-between;
}
</style>

<style scoped src="../styles/auth.css"></style>