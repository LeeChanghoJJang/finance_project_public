import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import MyPageView from '@/views/MyPageView.vue'
import StockView from '@/views/StockView.vue'
import StockDetailView from '@/views/StockDetailView.vue'
import StockArticleView from '@/views/StockArticleView.vue'
import DepositView from '@/views/DepositView.vue'
import RecommendView from '@/views/RecommendView.vue'
import UpdateUserView from '@/views/UpdateUserView.vue'
import ArticleWriteView from '@/views/ArticleWriteView.vue'
import ArticleDetail from '@/views/ArticleDetail.vue'
import {useAccountsStore} from '@/stores/accounts'
import LoginView from '@/views/LoginView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path : '/accounts/signup',
      name : 'signup',
      component : () => import('@/views/SignupView.vue'),
      beforeEnter : () => {
        const accountsStore = useAccountsStore()
        if (accountsStore.userId) {
          return {name:'home'}
        }
      }
    },
    {
      path : '/accounts/login',
      name : 'login',
      component : LoginView
    },
    {
      path : '/accounts/:id',
      name : 'mypage',
      component : MyPageView,
      beforeEnter : () => {
        const accountsStore = useAccountsStore()
        if (!(accountsStore.userId)) {
          window.alert('로그인이 필요한 기능입니다.')
          return {name:'login'}
        }
      }
      
    },
    {
      path : '/stock',
      name : 'stock',
      component : StockView
    },
    {
      path : '/stock/:id/article',
      name : 'article',
      component : StockArticleView
    },
    {
      path : '/stock/:id/article/write',
      name : 'articleWrite',
      component : ArticleWriteView,
      beforeEnter : () => {
        const accountsStore = useAccountsStore()
        if (!(accountsStore.userId)) {
          window.alert('로그인이 필요한 기능입니다.')
          return {name:'login'}
        }
      }
    },
    {
      path : '/stock/:id',
      name : 'stockDetail',
      component :  StockDetailView,
    },
    {
      path : '/stock/:id/article/:article',
      name : 'articleDetail',
      component : ArticleDetail
    },
    {
      path : '/deposit',
      name : 'deposit',
      component : DepositView
    },
    {
      path : '/recommend',
      name : 'recommend',
      component : RecommendView,
      beforeEnter : () => {
        const accountsStore = useAccountsStore()
        if (!(accountsStore.userId)) {
          window.alert('로그인이 필요한 기능입니다.')
          return {name:'login'}
        }
      }
    },
    {
      path : '/updateuser',
      name : 'updateuser',
      component : UpdateUserView,
      beforeEnter : () => {
        const accountsStore = useAccountsStore()
        if (!(accountsStore.userId)) {
          window.alert('로그인이 필요한 기능입니다.')
          return {name:'login'}
        }
      }
    },
  ]
})

// // 이창호가 작성한 부분
// router.beforeEach((to, from, next) => {
//   const store = useAccountsStore()
//   const isAuthenticated = store.isLogin
  
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     if (!isAuthenticated) {
//       // 인증이 필요한 페이지에 접근하려고 할 때 로그인 페이지로 리다이렉트
//       next({ name: 'login' })
//     } else {
//       // 인증된 사용자인 경우 요청한 페이지로 이동
//       next()
//     }
//   } else {
//     // 인증이 필요하지 않은 페이지는 그대로 진행
//     next()
//   }
// })
// // 이창호가 작성한 부분

export default router
