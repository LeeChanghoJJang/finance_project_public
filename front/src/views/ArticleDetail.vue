<template>
  <nav aria-label="breadcrumb" class="m-3">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="#" @click.prevnet="articleStore.goHome">홈</a></li>
    <li class="breadcrumb-item"><a href="#" @click.prevent="articleStore.goSearch">종목 검색</a></li>
    <li class="breadcrumb-item"><a href="#" @click.prevent="articleStore.goStock($route.params.id)">{{ $route.params.id }}</a></li>
    <li class="breadcrumb-item active" aria-current="page">종목 토론</li>
  </ol>
</nav>
  <div class="container mt-5 ms-auto me-auto" v-if="article">
    <div class="card ms-auto me-auto">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h2>{{ article.title }}</h2>
        <div class="">
        <p class="text-muted">작성자: {{ accountsStore.allUserPK[article.user] }}
          <button v-if="accountsStore.userId===accountsStore.allUserPK[article.user]" type="submit" class="btn btn-secondary" @click="deleteArticle">글 삭제</button>
        </p>
        <p class="text-muted">작성 일시 :{{ formatDate(article.created_at) }}</p>
      </div>
      </div>
      <div class="card-body">
        <p>{{ article.content }}</p>
      </div>
      <div class="card-footer">
        <h5>댓글 {{ articleStore.comments.length }} </h5>
        <ul class="list-group list-group-flush">
          <li class="list-group-item d-flex justify-content-between align-items-center bg-light" v-for="comment in articleStore.comments" :key="comment.id">
            <div>
              <div>{{ accountsStore.allUserPK[comment.user] }}: {{ comment.content }}</div>
            </div>
            <div>
            <small class="text-muted me-3">{{ formatDate(comment.create_at) }}</small>
            <button v-if="accountsStore.userId === accountsStore.allUserPK[comment.user]" @click="deleteComment(comment.id)" class="btn btn-close btn-sm"></button>
          </div>
          </li>
        </ul>
        <form class="mt-3" @submit.prevent="createComment">
          <div class="mb-3">
            <label for="comment" class="form-label">댓글</label>
            <input type="text" class="form-control" id="comment" placeholder="댓글을 입력하세요" v-model="comment">
          </div>
          <button type="submit" class="btn btn-primary">댓글 달기</button>
          
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUpdated, onBeforeUpdate } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { useAccountsStore } from '@/stores/accounts'

const accountsStore = useAccountsStore()
const route = useRoute()
const articleStore = useArticleStore()
const article = ref(null)
const comment = ref('')

const router = useRouter()
const createComment = function () {
  // 1. 로그인 여부 확인
  if (!(accountsStore.userId)) {
    if (window.confirm('로그인이 필요한 기능입니다. \n로그인 페이지로 이동하시겠습니까?')) {
    router.push({name : 'login'})}
    return 
  }
  // 2. 글이 있는지 확인
  else if (comment.value) {
  const data = {
    content: comment.value
  }
  articleStore.postComment(route.params.id, route.params.article, data)
  comment.value = ''  // 댓글 작성 후 입력 필드 비우기
  }
  // 없으면  
  else {
    window.alert('댓글을 작성해주세요.')
  } 
}

const deleteArticle = function () {
  // console.log(article.value.id)
  if (window.confirm("게시글을 삭제하시겠습니까?")) {
  articleStore.deleteArticle(route.params.id, article.value.id)
}
}

const deleteComment = function (commentId) {
  articleStore.deleteComment(route.params.id ,route.params.article, commentId)
}

// 시간 변경 함수
const formatDate = function (dateString) {
  const date = new Date(dateString);

  // Format options for month-day and hour-minute
  const optionsDate = { month: '2-digit', day: '2-digit' };
  const optionsTime = { hour: '2-digit', minute: '2-digit', hour12: false };

  const formattedDate = new Intl.DateTimeFormat('en-US', optionsDate).format(date);
  const formattedTime = new Intl.DateTimeFormat('en-US', optionsTime).format(date);

  return `${formattedDate} ${formattedTime}`;
}

onMounted(() => {
  article.value = articleStore.findArticle(route.params.article)
  articleStore.getComment(route.params.id, route.params.article)
})

const check = ref('')
onUpdated(() => {
  if (check.value !== articleStore.comments.length) {
    articleStore.getComment(route.params.id, route.params.article)
    check.value = articleStore.comments.length
  }
})

</script>

<style scoped>
.card {
  margin-top: 20px;
}
</style>
