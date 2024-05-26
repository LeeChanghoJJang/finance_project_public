import { ref, computed } from 'vue'
import { createPinia, defineStore } from 'pinia'
import { useAccountsStore } from '@/stores/accounts'
import {useRouter} from 'vue-router'
import axios from 'axios'

export const useArticleStore = defineStore('article', () => {
  const router = useRouter()

  const accountsStore = useAccountsStore()
  const API_URL = accountsStore.API_URL
  // 토큰 받아오기 
  const token = computed(() => {
    return accountsStore.token
  })
  // 게시글
  const article = ref()
  // 게시글 조회
  const getArticle = function (params) {
    axios ({
      method : 'get',
      url : `${API_URL}/stock/${params}/article/`
    })
    .then (response => {
      article.value = response.data
      return response.data
    })
    .catch (error => {
      console.log(error)
    })
  }
  // 게시글 작성

  const postArticle = function (params,data) {
    axios ({
      method : 'post',
      url : `${API_URL}/stock/${params}/article/`,
      headers : { 
        'Authorization' : `Token ${token.value}`
      },
      data : data
    })
    .then (response => {
      window.alert('새 글이 작성되었습니다.')
      getArticle(params)
      router.push({name:'stockDetail', params:{id:params.value}})
    })
  }
  
  const deleteArticle = function (params,articleId) {
    axios({
      method : 'delete',
      url : `${API_URL}/stock/${params}/article/${articleId}`,
      headers : { 
        'Authorization' : `Token ${token.value}`
      },
    })
      .then (response => {
        getArticle(params)
        window.alert('게시글이 삭제되었습니다.')
        router.push({name:'stockDetail', params:{id:params}})
      })
  }   

  const findArticle = function (id) {
    return article.value.find(item => item.id.toString() === id.toString())
  }
  
  const comments = ref()
  
  const getComment = function (params,article) {
    axios({
      method : 'get',
      url : `${API_URL}/stock/${params}/article/${article}/comments/`,
    })
    .then (response => {
      comments.value = response.data
    })
  }

  const postComment = function (stockName,articleId,data) {
    axios({
      method : 'post',
      url : `${API_URL}/stock/${stockName}/article/${articleId}/comments/`,
      data : data,
      headers : { 
        'Authorization' : `Token ${token.value}`
      },
    })
    .then (response => {
      window.alert('댓글이 작성되었습니다.')
      getComment(stockName,articleId)
      router.push({name : 'articleDetail', params:{id:stockName, article:articleId}})
    })
  }

  const deleteComment = function (stockName, articleId, commentId) {
    axios({
      method : 'delete',
      url : `${API_URL}/stock/${stockName}/article/${articleId}/comments/${commentId}`,
      headers : { 
        'Authorization' : `Token ${token.value}`
      },
    })
    .then (response => {
      window.alert('삭제되었습니다.')
      getComment(stockName,articleId)
      router.push({name : 'articleDetail', params:{id:stockName, article:articleId}})
    })
  }


  const goHome = function() { 
    router.push({name :'home'})
  }

  const goSearch = function() {
    router.push({name :'stock'})
  }

  const goStock = function (stock) {
    router.push({name : 'stockDetail', params:{id : stock}})
  }



  return {
    article, 
    comments,  
    deleteArticle, getArticle, postArticle, findArticle,
    postComment, getComment, deleteComment, 
    goHome, goSearch, goStock
  }
}, { persist: true })

