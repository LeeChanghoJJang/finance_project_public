<template>
  <div class="inner container mt-5">
    <div class="d-flex justify-content-around m-auto">
      <div class="d-flex flex-column align-items-center justify-content-center text-center">
        <h1>추천페이지</h1>
        <div class="mb-3">오늘의 추천상품을 받아보세요!</div>
      </div>
      <div class="d-flex flex-column align-items-center justify-content-center mt-3 mb-3 g-5">
        <div class="group-box">
          <div class="group-title">수익률 기준</div>
          <div class="d-flex justify-content-center">
            <button class="btn btn-primary me-3" @click="recommend(1)" @mouseover="hoverButton" @mouseout="unhoverButton">매매차익</button>
            <button class="btn btn-info me-3 text-white" @click="recommend(2)" @mouseover="hoverButton" @mouseout="unhoverButton">매매차익 + 배당수익률</button>
            <button class="btn btn-danger" @click="recommend(3)" @mouseover="hoverButton" @mouseout="unhoverButton">변동성</button>
          </div>
        </div>
      </div>
    </div>
    <hr class="my-3 thick-hr">

    

    <div v-if="loading" class="loading-spinner">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="recommendations row">
      <div v-if="recommends" v-for="(recommend, index) in recommends" :key="index" class="recommendation-card col-md-6" @mouseover="hoverCard(index)" @mouseout="unhoverCard(index)" @click="goToDetail(recommend)">
        <div class="card-header">
          <span v-if="index === 'recommend_stock'">주식</span>
          <span v-else>예적금</span>
        </div>
        <div class="card-body">
          <div v-if="recommend.name" class="text-center">종목명 : {{ recommend.name }}</div>
          <div v-if="recommend.foreigner_buy" class="text-center">외국인 순매수 : {{ recommend.foreigner_buy }}</div>
          <div v-if="recommend.organ_buy" class="text-center">기관 순매수 : {{ recommend.organ_buy }}</div>
          <div v-if="recommend.individual_buy" class="text-center">개인 순매수 : {{ recommend.individual_buy }}</div>
          <div v-if="recommend.price" class="text-center">주가 : {{ recommend.price }}원</div>
          <div v-if="recommend.per" class="text-center">PER : {{ recommend.per }}</div>
          <div v-if="recommend.pbr" class="text-center">PBR : {{ recommend.pbr }}</div>
          <div v-if="recommend.dividend_ratio" class="text-center">배당수익률 : {{ recommend.dividend_ratio }}%</div>
          <div v-if="recommend.dividend" class="text-center">주당배당금 : {{ recommend.dividend }}원</div>
          <div v-if="recommend.highprice_52" class="text-center">52주 고가 : {{ recommend.highprice_52 }}원</div>
          <div v-if="recommend.lowprice_52" class="text-center">52주 저가 : {{ recommend.lowprice_52 }}원</div>

          <div v-if="recommend.deposit" class="text-center">
            <div v-if="recommend.deposit.bank">은행 : {{ recommend.deposit.bank }} </div>
            <div v-if="recommend.deposit.product">상품명 : {{ recommend.deposit.product }} </div>
            <div v-if="recommend.deposit.period">가입기간 : {{ recommend.deposit.period }}개월 </div>
            <div v-if="recommend.deposit.intr_type">금리유형 : {{ recommend.deposit.intr_type }} </div>
            <div v-if="recommend.deposit.intr_rate" class="intr-rate">기본금리 : {{ recommend.deposit.intr_rate }}% </div>
            <div v-if="recommend.deposit.intr_rate2" class="intr-rate">최고금리 : {{ recommend.deposit.intr_rate2 }}% </div>
            <div v-if="recommend.deposit.max_limit">가입한도 : {{ recommend.deposit.max_limit }} </div>
            <div v-if="recommend.deposit.mtrt_int">우대조건 : {{ recommend.deposit.mtrt_int }} </div>
          </div>
          <div v-if="recommend.effective_rate" class="effective-rate text-center rate-color">총 수익률 : {{ recommend.effective_rate }}%</div>
          <div v-if="recommend.market_vlue" class="text-center">시가총액 : {{ recommend.market_vlue }}원</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAccountsStore } from '@/stores/accounts'
import { useRouter } from 'vue-router'

const accountsStore = useAccountsStore()
const recommends = ref(null)
const loading = ref(false)
const router = useRouter()

const recommend = async function (standard) {
  loading.value = true
  try {
    await accountsStore.recommend(standard)
    recommends.value = accountsStore.recommend_list.value
  } finally {
    loading.value = false
  }
}

watch(() => accountsStore.recommend_list, (newVal) => {
  recommends.value = newVal
  console.log('추천 목록 업데이트됨:', newVal)
})

const hoverButton = (event) => {
  event.target.style.transform = 'scale(1.05)'
  event.target.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.2)'
}

const unhoverButton = (event) => {
  event.target.style.transform = 'scale(1)'
  event.target.style.boxShadow = 'none'
}

const hoverCard = (index) => {
  const cards = document.getElementsByClassName('recommendation-card')
  if (cards[index]) {
    const card = cards[index]
    card.style.transform = 'scale(1.05)'
    card.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.2)'
    const img = card.querySelector('img')
    if (img) {
      img.style.transform = 'scale(1.05)'
    }
    document.querySelector('.recommendations').style.backgroundColor = 'rgba(0, 0, 0, 0.5)'
  }
}

const unhoverCard = (index) => {
  const cards = document.getElementsByClassName('recommendation-card')
  if (cards[index]) {
    const card = cards[index]
    card.style.transform = 'scale(1)'
    card.style.boxShadow = 'none'
    const img = card.querySelector('img')
    if (img) {
      img.style.transform = 'scale(1)'
    }
    document.querySelector('.recommendations').style.backgroundColor = 'transparent'
  }
}

const goToDetail = (recommend) => {
  if (recommend.name) {
    router.push(`/stock/${recommend.name}/`)
  } else if (recommend.deposit) {
    router.push('/deposit')
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
  background-color: #f0f4f8;
  font-family: 'Roboto', sans-serif;
}

.inner {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.text-center {
  text-align: center;
}

.d-flex {
  display: flex;
}

.align-items-center {
  align-items: center;
}

.group-box {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.group-title {
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
}

.btn-primary,
.btn-success,
.btn-danger,
.btn-info {
  transition: transform 0.2s, box-shadow 0.2s;
}

.recommendations {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.recommendation-card {
  background-color: #ffffff;
  width: calc(50% - 20px);
  padding: 20px;
  border-radius: 5px;
  transition: transform 0.2s, box-shadow 0.2s;
  text-align: center;
  cursor: pointer;
  position: relative;
}

.recommendation-card .card-header {
  background-color: #a1dff1;
  color: #fff;
  padding: 10px;
  font-weight: bold;
  border-radius: 5px 5px 0 0;
}

.recommendation-card .card-body {
  background-color: #e4f3fc;
  border-radius: 0 0 5px 5px;
  padding: 10px;
}

.recommendation-card:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.recommendation-card img {
  transition: transform 0.2s;
}

.loading-spinner {
  text-align: center;
  font-size: 1.5em;
}

@media screen and (max-width: 768px) {
  .recommendation-card {
    width: calc(100% - 20px);
  }
}

.name {
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.price, .price-diff, .dividend, .foreigner-ratio, .intr-rate, .effective-rate {
  margin-top: 10px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.rate-color {
  color: #e67f10;
  font-weight: bold;
}

.thick-hr {
    border: 0;
    height: 3px; /* 원하는 높이로 설정 */
    background-color: rgb(51, 171, 182); /* 원하는 색상으로 설정 */
  }
</style>
