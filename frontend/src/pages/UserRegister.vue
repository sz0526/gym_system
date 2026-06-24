<template>
  <div class="auth-page">
    <div class="auth-backdrop" aria-hidden="true">
      <div class="auth-shape auth-shape-1" />
      <div class="auth-shape auth-shape-2" />
      <div class="auth-shape auth-shape-3" />
    </div>

    <div class="auth-card" role="main" aria-labelledby="register-title">
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
        <h1 id="register-title" class="auth-title">创建会员账号</h1>
        <p class="auth-subtitle">填写下方信息，开启您的健身之旅</p>
      </div>

      <form class="auth-form" @submit.prevent="submit">
        <div class="field-group">
          <label class="field-label" for="username">
            用户名
            <span class="required" aria-hidden="true">*</span>
          </label>
          <div class="input-wrap" :class="{ 'is-error': errors.username }">
            <el-icon class="input-icon"><User /></el-icon>
            <input
              id="username"
              v-model="form.username"
              type="text"
              autocomplete="username"
              placeholder="6-20位，支持中英文、数字及下划线"
              @blur="validateField('username')"
              @input="onInput('username')"
            />
          </div>
          <transition name="field-error">
            <span v-if="errors.username" class="field-error">{{ errors.username }}</span>
          </transition>
        </div>

        <div class="field-group">
          <label class="field-label" for="email">
            邮箱
            <span class="required" aria-hidden="true">*</span>
          </label>
          <div class="input-wrap" :class="{ 'is-error': errors.email }">
            <el-icon class="input-icon"><Message /></el-icon>
            <input
              id="email"
              v-model="form.email"
              type="email"
              autocomplete="email"
              placeholder="example@email.com"
              @blur="validateField('email')"
              @input="onInput('email')"
            />
          </div>
          <transition name="field-error">
            <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
          </transition>
        </div>

        <div class="field-group">
          <label class="field-label" for="password">
            设置密码
            <span class="required" aria-hidden="true">*</span>
          </label>
          <div class="input-wrap" :class="{ 'is-error': errors.password }">
            <el-icon class="input-icon"><Lock /></el-icon>
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="new-password"
              placeholder="至少8位，含字母、数字及特殊符号"
              @blur="validateField('password')"
              @input="onInput('password')"
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
          <div v-if="form.password" class="strength-bar">
            <span class="strength-label">密码强度</span>
            <div class="strength-track">
              <div class="strength-segment" :class="{ 'active': passwordStrength.level >= 1, 'weak': passwordStrength.level === 1 }" />
              <div class="strength-segment" :class="{ 'active': passwordStrength.level >= 2, 'medium': passwordStrength.level >= 2 && passwordStrength.level < 3 }" />
              <div class="strength-segment" :class="{ 'active': passwordStrength.level >= 3, 'strong': passwordStrength.level === 3 }" />
            </div>
            <span class="strength-text" :class="`strength-${passwordStrength.level}`">
              {{ passwordStrength.label }}
            </span>
          </div>
          <transition name="field-error">
            <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
          </transition>
        </div>

        <div class="field-group">
          <label class="field-label" for="confirmPassword">
            确认密码
            <span class="required" aria-hidden="true">*</span>
          </label>
          <div class="input-wrap" :class="{ 'is-error': errors.confirmPassword }">
            <el-icon class="input-icon"><Lock /></el-icon>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              autocomplete="new-password"
              placeholder="请再次输入密码"
              @blur="validateField('confirmPassword')"
              @input="onInput('confirmPassword')"
            />
            <button
              type="button"
              class="input-suffix"
              tabindex="-1"
              :aria-label="showConfirmPassword ? '隐藏密码' : '显示密码'"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              <el-icon><View v-if="showConfirmPassword" /><Hide v-else /></el-icon>
            </button>
          </div>
          <transition name="field-error">
            <span v-if="errors.confirmPassword" class="field-error">{{ errors.confirmPassword }}</span>
          </transition>
        </div>

        <div class="field-group agreement">
          <label class="checkbox-label" :class="{ 'is-error': errors.agreement }">
            <input
              v-model="form.agreement"
              type="checkbox"
              class="checkbox-input"
              @change="validateField('agreement')"
            />
            <span class="checkbox-box" aria-hidden="true">
              <el-icon class="checkbox-check"><Check /></el-icon>
            </span>
            <span class="checkbox-text">
              我已阅读并同意
              <a href="#" @click.prevent="showAgreement = true">《会员注册协议》</a>
            </span>
          </label>
          <transition name="field-error">
            <span v-if="errors.agreement" class="field-error">{{ errors.agreement }}</span>
          </transition>
        </div>

        <button
          type="submit"
          class="auth-submit"
          :disabled="loading"
          :aria-busy="loading"
        >
          <el-icon v-if="loading" class="submit-icon is-spin"><Loading /></el-icon>
          <span>{{ loading ? '注册中…' : '立即注册' }}</span>
        </button>

        <div class="auth-footer">
          <span>已有账号？</span>
          <router-link to="/toUserLogin">直接登录</router-link>
        </div>
      </form>
    </div>

    <!-- 协议弹窗 -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="showAgreement" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="agreement-title">
          <div class="modal-panel">
            <h3 id="agreement-title" class="modal-title">会员注册协议</h3>
            <div class="modal-body">
              <p>欢迎使用健身房管理系统。注册会员账号即表示您同意遵守本系统的相关使用条款，包括但不限于：</p>
              <ul>
                <li>提供真实、准确、完整的个人信息；</li>
                <li>妥善保管账号及密码，对账号行为负责；</li>
                <li>遵守健身房相关管理规定及国家法律法规。</li>
              </ul>
              <p>本协议最终解释权归健身房管理系统所有。</p>
            </div>
            <div class="modal-actions">
              <button type="button" class="btn-primary" @click="confirmAgreement">我已阅读并同意</button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- 注册成功弹窗 -->
    <teleport to="body">
      <transition name="modal">
        <div v-if="successVisible" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="success-title">
          <div class="modal-panel modal-success">
            <div class="success-icon">
              <el-icon><Circle-Check /></el-icon>
            </div>
            <h3 id="success-title" class="modal-title">注册成功</h3>
            <p class="modal-desc">您的会员账号为 <strong>{{ registeredAccount }}</strong></p>
            <p class="modal-desc">{{ countdown }} 秒后自动跳转至登录页</p>
            <div class="modal-actions">
              <router-link to="/toUserLogin" class="btn-primary">立即登录</router-link>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { postForm } from '../api/client'
import {
  Check,
  CircleCheck,
  Hide,
  Loading,
  Lock,
  Message,
  User,
  View
} from '@element-plus/icons-vue'

const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreement: false
})

const errors = reactive<Record<keyof typeof form, string>>({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreement: ''
})

const touched = reactive<Record<keyof typeof form, boolean>>({
  username: false,
  email: false,
  password: false,
  confirmPassword: false,
  agreement: false
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const showAgreement = ref(false)
const loading = ref(false)
const successVisible = ref(false)
const registeredAccount = ref('')
const countdown = ref(3)
let countdownTimer: ReturnType<typeof setInterval> | null = null

const USERNAME_RE = /^[\u4e00-\u9fa5a-zA-Z0-9_]{6,20}$/
const EMAIL_RE = /^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/
const PASSWORD_RE = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&_#^~.,:;\-+=|\/\[\]{}()<>])[A-Za-z\d@$!%*?&_#^~.,:;\-+=|\/\[\]{}()<>]{8,}$/

function onInput(field: keyof typeof form) {
  if (touched[field]) {
    validateField(field)
  }
}

function validateField(field: keyof typeof form): boolean {
  touched[field] = true
  let message = ''

  switch (field) {
    case 'username':
      if (!form.username.trim()) {
        message = '用户名不能为空'
      } else if (!USERNAME_RE.test(form.username)) {
        message = '用户名须为6-20位中文、英文、数字或下划线'
      }
      break
    case 'email':
      if (!form.email.trim()) {
        message = '邮箱不能为空'
      } else if (!EMAIL_RE.test(form.email)) {
        message = '邮箱格式不正确'
      }
      break
    case 'password':
      if (!form.password) {
        message = '密码不能为空'
      } else if (!PASSWORD_RE.test(form.password)) {
        message = '密码至少8位，且需包含字母、数字及特殊符号'
      }
      if (form.confirmPassword && touched.confirmPassword) {
        validateField('confirmPassword')
      }
      break
    case 'confirmPassword':
      if (!form.confirmPassword) {
        message = '请再次输入密码'
      } else if (form.confirmPassword !== form.password) {
        message = '两次输入的密码不一致'
      }
      break
    case 'agreement':
      if (!form.agreement) {
        message = '请阅读并同意会员注册协议'
      }
      break
  }

  errors[field] = message
  return !message
}

function validateAll(): boolean {
  (Object.keys(form) as Array<keyof typeof form>).forEach((k) => validateField(k))
  return (Object.values(errors) as string[]).every((v) => !v)
}

const passwordStrength = computed(() => {
  const pwd = form.password
  if (!pwd) return { level: 0, label: '未输入' }
  let score = 0
  if (pwd.length >= 8) score++
  if (pwd.length >= 12) score++
  if (/[A-Z]/.test(pwd) && /[a-z]/.test(pwd)) score++
  if (/\d/.test(pwd)) score++
  if (/[^A-Za-z0-9]/.test(pwd)) score++

  if (score <= 2) return { level: 1, label: '弱' }
  if (score <= 4) return { level: 2, label: '中' }
  return { level: 3, label: '强' }
})

function confirmAgreement() {
  form.agreement = true
  showAgreement.value = false
  validateField('agreement')
}

async function submit() {
  if (loading.value) return
  if (!validateAll()) return

  loading.value = true
  try {
    const resp = await postForm('/api/userRegister', {
      memberUsername: form.username,
      memberEmail: form.email,
      memberPassword: form.password
    })
    const data = resp.data || {}
    if (data.success) {
      registeredAccount.value = String(data.memberAccount || '')
      successVisible.value = true
      startCountdown()
    } else {
      errors.username = data.message || '注册失败'
    }
  } catch (e: any) {
    const msg = e?.response?.data?.message || '网络异常，请稍后重试'
    const status = e?.response?.status
    if (status === 409) {
      errors.username = msg
    } else {
      errors.username = msg
    }
  } finally {
    loading.value = false
  }
}

function startCountdown() {
  countdown.value = 3
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      if (countdownTimer) clearInterval(countdownTimer)
      router.push('/toUserLogin')
    }
  }, 1000)
}

onUnmounted(() => {
  if (countdownTimer) clearInterval(countdownTimer)
})
</script>

<style scoped>
.strength-bar {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding-top: var(--space-1);
}

.strength-label {
  font-size: var(--text-xs);
  color: var(--text-muted);
  min-width: 56px;
}

.strength-track {
  flex: 1;
  display: flex;
  gap: 4px;
  height: 6px;
}

.strength-segment {
  flex: 1;
  background: var(--color-neutral-200);
  border-radius: var(--radius-full);
  transition:
    background-color var(--duration-normal) var(--ease-out),
    box-shadow var(--duration-normal) var(--ease-out);
}

.strength-segment.active.weak {
  background: var(--color-error);
}

.strength-segment.active.medium {
  background: var(--color-warning);
}

.strength-segment.active.strong {
  background: var(--color-success);
}

.strength-segment.active:not(.medium):not(.strong):not(.weak) {
  background: var(--color-error);
}

.strength-text {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  min-width: 32px;
  text-align: right;
}

.strength-text.strength-0 { color: var(--text-muted); }
.strength-text.strength-1 { color: var(--color-error); }
.strength-text.strength-2 { color: var(--color-warning); }
.strength-text.strength-3 { color: var(--color-success); }

.agreement {
  margin-top: calc(var(--space-1) * -1);
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  cursor: pointer;
}

.checkbox-label.is-error .checkbox-box {
  border-color: var(--color-error);
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.checkbox-box {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  margin-top: 2px;
  display: grid;
  place-items: center;
  border: 2px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: var(--bg-card);
  transition:
    border-color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}

.checkbox-input:checked + .checkbox-box {
  border-color: var(--color-accent-600);
  background: var(--color-accent-600);
}

.checkbox-input:focus-visible + .checkbox-box {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}

.checkbox-check {
  color: #ffffff;
  font-size: 12px;
  opacity: 0;
  transform: scale(0.8);
  transition: opacity var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}

.checkbox-input:checked + .checkbox-box .checkbox-check {
  opacity: 1;
  transform: scale(1);
}

.checkbox-text {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.5;
}

.checkbox-text a {
  color: var(--color-accent-600);
  font-weight: var(--font-medium);
}

.checkbox-text a:hover {
  color: var(--color-accent-700);
  text-decoration: underline;
}
</style>

<style scoped src="../styles/auth.css"></style>
