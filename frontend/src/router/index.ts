import { createRouter, createWebHistory } from 'vue-router'
import NotImplemented from '../pages/NotImplemented.vue'
import AdminLogin from '../pages/AdminLogin.vue'
import UserLogin from '../pages/UserLogin.vue'
import UserRegister from '../pages/UserRegister.vue'
import api from '../api/client'

const routes = [
  { path: '/', component: AdminLogin },
  { path: '/toUserLogin', component: UserLogin },
  { path: '/toUserRegister', component: UserRegister },

  { path: '/toAdminMain', component: () => import('../pages/AdminMain.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/toUserMain', component: () => import('../pages/UserMain.vue'), meta: { requiresAuth: true, role: 'user' } },

  // 管理端（先占位，后续把 templates 全量迁移为 Vue 页面组件）
  { path: '/member/selMember', component: () => import('../pages/MemberSelMember.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/member/toAddMember', component: () => import('../pages/MemberToAddMember.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/member/toUpdateMember', component: () => import('../pages/MemberToUpdateMember.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/member/toSelByCard', component: () => import('../pages/MemberToSelByCard.vue'), meta: { requiresAuth: true, role: 'admin' } },

  { path: '/employee/selEmployee', component: () => import('../pages/EmployeeSelEmployee.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/employee/toAddEmployee', component: () => import('../pages/EmployeeToAddEmployee.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/employee/toUpdateEmployee', component: () => import('../pages/EmployeeToUpdateEmployee.vue'), meta: { requiresAuth: true, role: 'admin' } },

  { path: '/equipment/selEquipment', component: () => import('../pages/EquipmentSelEquipment.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/equipment/toAddEquipment', component: () => import('../pages/EquipmentToAddEquipment.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/equipment/toUpdateEquipment', component: () => import('../pages/EquipmentToUpdateEquipment.vue'), meta: { requiresAuth: true, role: 'admin' } },

  { path: '/class/selClass', component: () => import('../pages/ClassSelClass.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/class/toAddClass', component: () => import('../pages/ClassToAddClass.vue'), meta: { requiresAuth: true, role: 'admin' } },
  { path: '/class/selClassOrder', component: () => import('../pages/ClassSelClassOrder.vue'), meta: { requiresAuth: true, role: 'admin' } },

  // 用户端
  { path: '/user/toUserInfo', component: () => import('../pages/UserToUserInfo.vue'), meta: { requiresAuth: true, role: 'user' } },
  { path: '/user/toUpdateInfo', component: () => import('../pages/UserToUpdateInfo.vue'), meta: { requiresAuth: true, role: 'user' } },
  { path: '/user/toUserClass', component: () => import('../pages/UserToUserClass.vue'), meta: { requiresAuth: true, role: 'user' } },
  { path: '/user/toApplyClass', component: () => import('../pages/UserToApplyClass.vue'), meta: { requiresAuth: true, role: 'user' } },
  { path: '/user/toChat', component: () => import('../pages/UserChat.vue'), meta: { requiresAuth: true, role: 'user' } },

  // fallback
  { path: '/:pathMatch(.*)*', component: NotImplemented }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach(async (to) => {
  const meta = to.meta as any
  if (!meta?.requiresAuth) return true

  const role = meta.role as string | undefined
  try {
    if (role === 'user') {
      await api.get('/api/toUserMain')
    } else {
      await api.get('/api/toAdminMain')
    }
    return true
  } catch (e) {
    // 未登录/会话失效：按角色回登录页
    return { path: role === 'user' ? '/toUserLogin' : '/' }
  }
})

export default router
