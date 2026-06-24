<template>
  <el-container class="role-layout">
    <el-aside :width="isCollapse ? '64px' : '240px'" class="role-aside">
      <div class="role-brand">
        <div class="role-brand-logo">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M6.5 6C6.5 4.067 8.067 2.5 10 2.5H14C15.933 2.5 17.5 4.067 17.5 6V10C17.5 11.933 15.933 13.5 14 13.5H10C8.067 13.5 6.5 11.933 6.5 10V6Z" stroke="currentColor" stroke-width="1.5"/>
            <path d="M3.5 14C3.5 12.067 5.067 10.5 7 10.5H9V14C9 15.933 7.433 17.5 5.5 17.5C4.11929 17.5 3 16.3807 3 15V14H3.5Z" stroke="currentColor" stroke-width="1.5"/>
            <path d="M20.5 14C20.5 12.067 18.933 10.5 17 10.5H15V14C15 15.933 16.567 17.5 18.5 17.5C19.8807 17.5 21 16.3807 21 15V14H20.5Z" stroke="currentColor" stroke-width="1.5"/>
            <path d="M12 13.5V21.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M8.5 21.5H15.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </div>
        <span v-show="!isCollapse" class="role-brand-text">健身房管理系统</span>
      </div>

      <button
        type="button"
        class="role-collapse-btn"
        :aria-label="isCollapse ? '展开菜单' : '收起菜单'"
        @click="isCollapse = !isCollapse"
      >
        <el-icon><Arrow-Left-Bold v-if="!isCollapse" /><Arrow-Right-Bold v-else /></el-icon>
      </button>

      <el-menu
        :router="true"
        :default-active="activePath"
        :collapse="isCollapse"
        :collapse-transition="false"
        class="role-menu"
      >
        <template v-if="role === 'admin'">
          <el-menu-item index="/toAdminMain">
            <el-icon><House /></el-icon>
            <template #title>管理员主页</template>
          </el-menu-item>
          <el-menu-item index="/member/toSelByCard">
            <el-icon><CreditCard /></el-icon>
            <template #title>会员卡查询</template>
          </el-menu-item>
          <el-menu-item index="/member/selMember">
            <el-icon><User /></el-icon>
            <template #title>会员管理</template>
          </el-menu-item>
          <el-menu-item index="/employee/selEmployee">
            <el-icon><User-Filled /></el-icon>
            <template #title>员工管理</template>
          </el-menu-item>
          <el-menu-item index="/equipment/selEquipment">
            <el-icon><First-Aid-Kit /></el-icon>
            <template #title>器材管理</template>
          </el-menu-item>
          <el-menu-item index="/class/selClass">
            <el-icon><Calendar /></el-icon>
            <template #title>课程管理</template>
          </el-menu-item>
          <el-menu-item index="/class/selClassOrder">
            <el-icon><Document /></el-icon>
            <template #title>报名信息</template>
          </el-menu-item>
        </template>

        <template v-else>
          <el-menu-item index="/toUserMain">
            <el-icon><House /></el-icon>
            <template #title>会员主页</template>
          </el-menu-item>
          <el-menu-item index="/user/toUserInfo">
            <el-icon><User /></el-icon>
            <template #title>个人信息</template>
          </el-menu-item>
          <el-menu-item index="/user/toChat">
            <el-icon><Chat-Dot-Round /></el-icon>
            <template #title>智能问答</template>
          </el-menu-item>
          <el-sub-menu index="user-course">
            <template #title>
              <el-icon><Calendar /></el-icon>
              <span>课程管理</span>
            </template>
            <el-menu-item index="/user/toApplyClass">报名选课</el-menu-item>
            <el-menu-item index="/user/toUserClass">我的课程</el-menu-item>
          </el-sub-menu>
        </template>
      </el-menu>

      <div class="role-footer">
        <div v-show="!isCollapse" class="role-footer-title">当前身份</div>
        <div class="role-footer-role">
          <span class="role-footer-dot" />
          <span v-show="!isCollapse" class="role-footer-text">{{ role === 'admin' ? '管理员' : '会员' }}</span>
        </div>
      </div>
    </el-aside>

    <el-main class="role-main">
      <slot />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  ArrowLeftBold,
  ArrowRightBold,
  Calendar,
  ChatDotRound,
  CreditCard,
  Document,
  FirstAidKit,
  House,
  User,
  UserFilled
} from '@element-plus/icons-vue'

type Role = 'admin' | 'user'

const props = defineProps<{
  role: Role
}>()

const route = useRoute()
const isCollapse = ref(false)
const activePath = computed(() => route.path)
</script>

<style scoped>
.role-layout {
  min-height: 100svh;
  background: var(--bg-body);
}

.role-aside {
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--bg-sidebar);
  color: var(--text-inverse);
  transition: width var(--duration-normal) var(--ease-out);
  box-shadow: var(--shadow-lg);
  z-index: 10;
}

.role-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  height: 64px;
  padding: 0 var(--space-4);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
}

.role-brand-logo {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  color: var(--color-accent-500);
  background: rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md);
}

.role-brand-logo svg {
  width: 20px;
  height: 20px;
}

.role-brand-text {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: #ffffff;
  white-space: nowrap;
  letter-spacing: 0.5px;
}

.role-collapse-btn {
  position: absolute;
  top: 72px;
  right: -14px;
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  background: var(--color-accent-600);
  color: #ffffff;
  border: 2px solid #ffffff;
  border-radius: var(--radius-full);
  cursor: pointer;
  box-shadow: var(--shadow-md);
  transition:
    background var(--duration-fast) var(--ease-out),
    transform var(--duration-fast) var(--ease-out);
  z-index: 20;
}

.role-collapse-btn:hover {
  background: var(--color-accent-700);
  transform: scale(1.08);
}

.role-menu {
  flex: 1;
  border-right: none;
  background: transparent;
  padding: var(--space-3) 0;
}

.role-menu :deep(.el-menu-item),
.role-menu :deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.75);
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}

.role-menu :deep(.el-menu-item:hover),
.role-menu :deep(.el-sub-menu__title:hover) {
  color: #ffffff;
  background-color: rgba(255, 255, 255, 0.06);
}

.role-menu :deep(.el-menu-item.is-active) {
  color: var(--color-accent-500);
  background-color: rgba(249, 115, 22, 0.12);
}

.role-menu :deep(.el-sub-menu.is-active .el-sub-menu__title) {
  color: var(--color-accent-500);
}

.role-menu :deep(.el-icon) {
  color: inherit;
}

.role-menu :deep(.el-sub-menu .el-menu-item) {
  background: rgba(0, 0, 0, 0.3);
  color: rgba(255, 255, 255, 0.75);
}

.role-menu :deep(.el-sub-menu .el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.06);
  color: #ffffff;
}

.role-menu :deep(.el-sub-menu .el-menu-item.is-active) {
  background: rgba(249, 115, 22, 0.12);
  color: var(--color-accent-500);
}

.role-footer {
  padding: var(--space-4);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.role-footer-title {
  font-size: var(--text-xs);
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: var(--space-1);
}

.role-footer-role {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: #ffffff;
  font-weight: var(--font-medium);
}

.role-footer-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
  background: var(--color-success);
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.25);
}

.role-main {
  padding: var(--space-6);
  background: var(--bg-body);
  overflow: auto;
}

@media (max-width: 768px) {
  .role-aside {
    position: fixed;
    inset-block: 0;
    left: 0;
    transform: translateX(-100%);
    width: 240px !important;
  }

  .role-aside.is-open {
    transform: translateX(0);
  }

  .role-collapse-btn {
    display: none;
  }

  .role-main {
    padding: var(--space-4);
  }
}
</style>
