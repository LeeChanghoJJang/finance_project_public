<!-- 이거 지금 안씀 -->


<template>
  <h1>{{ $route.params.id }} 토론 게시판</h1>
  <div class="container">
    <div class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>글 번호</th>
            <th>제목</th>
            <th>작성자</th>
            <th>작성 일시</th>
            <th>댓글 수</th>
          </tr>
        </thead>
        
        <tbody v-if="articleStore.article">
          <tr v-for="article in articleStore.article">
            <th>{{ article.id }}</th>
            <th class="text-truncate" style="max-width: 150px;" @click="goDetail(article.id)">{{ article.title }}</th>
            <th>{{ allUserPK[article.user] }}</th>
            <th>{{ formatDateTime(article.created_at) }}</th>
            <th>???</th>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="d-flex justify-content-between align-items-center">
      <nav class="mx-auto" aria-label="Page navigation example">
        <ul class="pagination mb-0">
          <li class="page-item">
            <a class="page-link" href="#" aria-label="Previous">
              <span aria-hidden="true">&laquo;</span>
            </a>
          </li>
          <li class="page-item"><a class="page-link" href="#">1</a></li>
          <li class="page-item"><a class="page-link" href="#">2</a></li>
          <li class="page-item"><a class="page-link" href="#">3</a></li>
          <li class="page-item">
            <a class="page-link" href="#" aria-label="Next">
              <span aria-hidden="true">&raquo;</span>
            </a>
          </li>
        </ul>
      </nav>
      <a class="btn btn-primary" @click.prevent="goWrite">글쓰기</a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { format, isToday, parseISO } from 'date-fns'
import {useArticleStore} from '@/stores/article'
import {useAccountsStore} from '@/stores/accounts'
import {useRoute, useRouter} from 'vue-router'

// 날짜와 시간 포맷팅 함수 (오늘 날짜면 시간 / 그 외엔 날짜만)
function formatDateTime(dateTime) {
  const date = parseISO(dateTime)
  if (isToday(date)) {
    return format(date, 'HH:mm')
  } else {
    return format(date, 'MM.dd')
  }
}

// articles에 전체 게시글 저장
const articleStore = useArticleStore()


const route = useRoute()
onMounted(() => {
  articleStore.getArticle(route.params.id)
})


// 게시글 작성자에 대응하는 user.pk 정보 저장
const accountsStore = useAccountsStore()
const allUserPK = accountsStore.allUserPK

const router = useRouter()
// 글쓰기로 이동
const goWrite = function () {
  router.push({name : 'articleWrite', params:{id:route.params.id}})
}

const goDetail = function (id) {
  router.push({name : 'articleDetail', params:{id:route.params.id, article:id}})
}
</script>

<style scoped>
.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
