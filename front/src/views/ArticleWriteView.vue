<template>
  <div class="mt-5 ms-5 me-5">
  <h1 class="m-2">새 글 쓰기</h1>
  <hr>
  <div class="m-2">
    <form @submit.prevent="write">
      <label for="title inputlg" class="form-label">제목</label>
      <div class="input-group">
        <input id="title" type="text" size="30" class="input-lg form-control" placeholder="제목" aria-label="title" v-model="title">
      </div>
      <label for="content" class="form-label mt-3">내용</label>
      <div class="input-group">
        <textarea class="form-control fixed-size inputlg" aria-label="content" placeholder="내용" v-model="content"></textarea>
      </div>
      <input type="submit" class="btn btn-primary mt-3">
    </form>
  </div>
  </div>
</template>

<script setup>
import {ref, onUpdated} from 'vue'
import {useArticleStore} from '@/stores/article'
import {useRoute, useRouter} from 'vue-router'


// 작성글의 제목과 내용 
const title = ref(null)
const content = ref(null)

// 현재 작성중인 종목
const route = useRoute()
const params = ref(route.params.id)

// store로 함수 보내기
const articleStore = useArticleStore()

const write = function () {
  const data = {
    title : title.value,
    content : content.value
  }
  articleStore.postArticle(params.value,data)
}


</script>

<style scoped>
.fixed-size {
  width: 300px;
  height: 200px;
}
</style>
