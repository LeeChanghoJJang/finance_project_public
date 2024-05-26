<template>
  <div class="">
  <ol class="breadcrumb">
    <li class="breadcrumb-item"><a href="#" @click.prevnet="articleStore.goHome">홈</a></li>
    <li class="breadcrumb-item"><a href="#" @click.prevent="articleStore.goSearch">종목 검색</a></li>
    <li class="breadcrumb-item active" aria-current="page">{{ $route.params.id }}</li>
  </ol>
  <h4>원하는 주식을 검색 해보세요!</h4>
  <figcaption class="blockquote-footer mt-1">
    초성으로도 검색이 가능합니다.
  </figcaption>
  <div class="ms-2 mt-3 d-flex align-items-center">
    <div class="me-3 fs-5">주식명 : </div>
    <form @submit.prevent="goDetail" class="d-flex position-relative">
      <div class="position-relative">
        <input class="form-control custom-border" list="datalistOptions" id="exampleDataList" placeholder="주식 검색" v-model="stockName">
        <ul v-if="filteredStockList.length && stockName && check" class="list-group position-absolute w-100 mt-1">
          <li v-for="stock in filteredStockList.slice(0,5)" class="list-group-item" @click="selectStock(stock)">{{ stock }}</li>
        </ul>
      </div>
      <button type="submit" class="btn btn-primary custom-size ms-2">검색</button>
    </form>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import {useArticleStore} from '@/stores/article'
import {chosungIncludes} from 'es-hangul'



const articleStore = useArticleStore()
const stockList = ref([])
const stockName = ref('')
const filteredStocks = ref([])
const router = useRouter()
const check = ref(true)
const chosungStocks = ref([])
const combined = ref([])
const filteredStockList = computed(() => {
  filteredStocks.value = stockList.value.filter(stock => stock.toLowerCase().includes(stockName.value.toLowerCase()))
  chosungStocks.value = stockList.value.filter(stock => chosungIncludes(stock,stockName.value))
  combined.value = filteredStocks.value.concat(chosungStocks.value)
  return combined.value
})

onMounted(() => {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/stock/삼성전자/search/'
  })
  .then(response => {
    stockList.value = response.data.company_list
  })
})

const selectStock = function (stock) {
  check.value = false
  stockName.value = stock
}

const goDetail = function () {
  if (stockList.value.includes(stockName.value)) {
    router.replace({ name: 'stockDetail', params: { id: stockName.value }});
  } else {
    window.alert('검색 결과가 없습니다. 정확한 종목명을 입력해주세요.');
  }
  stockName.value = '';
}

</script>

<style scoped>
.custom-size {
  height: 40px;
  width: 80px;
}

.custom-border {
  border: 2px solid skyblue;
}

.position-relative {
  position: relative;
}

.position-absolute {
  position: absolute;
  z-index: 1000;
}

.list-group {
  max-height: 200px; /* 연관 검색어 목록의 최대 높이를 조절하세요 */
  overflow-y: auto; /* 연관 검색어 목록이 넘칠 경우 스크롤이 생기도록 설정 */
}

.list-group-item {
  white-space: nowrap;
}
</style>
