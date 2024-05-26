<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="flex-shrink-0">예적금 검색</h1>
      <select class="form-select custom-border flex-grow-0 ms-3" style="width: 300px; min-width: 200px;" aria-label="Default select example" v-model="selectedBank" @mouseover="check">
        <option selected disabled v-show="isCheck">은행 선택</option>
        <option v-if="banks.length" v-for="(bank, index) in banks" :key="index" :value="bank">{{ bank }}</option>
      </select>
    </div>
    <hr class="my-3 mb-4 custom-border">

    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4  g-4">
      <div v-for="datum in filteredData" class="col" :key="datum.product" @click="goDetail(datum)">
        <div class="card p-2">
          <img :src="`BankIcon/${datum.bank_code}.jpg`" class="card-img-top clickable-image" @click.stop="goDetail(datum)" alt="...">
          <hr>
          <div class="card-body">
            <h5 class="card-title font-weight-bold">{{ datum.product }}</h5>
            <p class="card-text">
              <div v-if="datum.standard && datum.standard.rsrv_type_nm">
                <strong>상품 정보:</strong> 적금
              </div>
              <div v-else>
                <strong>상품 정보:</strong> 예금
              </div>
              <div v-if="datum.standard">
                <div><strong>최저 금리:</strong> {{ datum.standard.intr_rate }} %</div>
              </div>
            </p>
          </div>
          <div class="card-footer">
              <div v-if="datum">
                <button
                  type="button"
                  @click="toggleLikeDeposit(datum.id)"
                  @mouseover="buttonOver"
                  @mouseleave="buttonLeave"
                  :class="{'btn btn-primary': !datum.isLiked, 'btn btn-danger': datum.isLiked}">
                  {{ datum.isLiked ? '관심 상품 제거' : '관심 상품 추가' }}
                </button>
              </div>
            </div>
        </div>
      </div>
    </div>
    <div 
      v-if="item" 
      class="detail-overlay" 
      @click="closeDetail">
      <div 
        class="detail" 
        @click.stop>
        <button @click="closeDetail">x</button>
        <div>{{ item.bank }}</div>
        <h3>{{ item.product }}</h3>
        <p>{{ item.mtrt_int }}</p>
        <p>{{ item.spcl_cnd }}</p>
        <p>비고: {{ item.etc_note }}</p>
        <div>기간별 비교</div>
        <hr>
        <div v-for="options in item.depositoption_set" :key="options.period">
          <div><strong>가입 기간:</strong> {{ options.period }}개월 이상</div>
          <div><strong>이자 방식:</strong> {{ options.intr_type }} </div>
          <div><strong>최저 금리:</strong> {{ options.intr_rate }} %</div>
          <div><strong>최고 금리:</strong> {{ options.intr_rate2 }} %</div>
          <hr>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAccountsStore } from '@/stores/accounts'
import { useBankStore } from '@/stores/bank'
import axios from 'axios'
import {useRouter} from 'vue-router'

const accountsStore = useAccountsStore()
const selectedBank = ref('은행 선택')

onMounted(() => {
  const likeBank = accountsStore.userStock.user.like_bank
  if (likeBank) {
    selectedBank.value = likeBank
  }
})

const data = ref([])
const bankStore = useBankStore()
const banks = ref([])
const item = ref(null)
const isCheck = ref(true)

const check = () => {
  isCheck.value = false
}

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/bank/search/')
    data.value = response.data
    banks.value = [...new Set(response.data.map(obj => obj.bank))].sort()

    const likedDeposits = localStorage.getItem('likedDeposits')
    if (likedDeposits) {
      const likedIds = JSON.parse(likedDeposits)
      data.value.forEach(deposit => {
        deposit.isLiked = likedIds.includes(deposit.id)
      })
    }
  } catch (error) {
    console.error('Error fetching bank data:', error)
  }
})

const filteredData = computed(() => {
  return data.value.filter(obj => obj.bank === selectedBank.value)
})

const buttonCheck = ref(true)

const buttonLeave = (event) => {
  buttonCheck.value = true
}
const buttonOver = (event) => {
  buttonCheck.value = false
}
const goDetail = (datum) => {
  if (buttonCheck.value) {
    item.value = datum
  }
}

const closeDetail = () => {
  item.value = null
}

const router = useRouter()
const toggleLikeDeposit = async (depositId) => {
  if (accountsStore.userId === null ) {
    if (window.confirm('로그인이 필요한 기능입니다. \n로그인 페이지로 이동하시겠습니까?')) {
    router.push({name : 'login'})}
    return 
  }
  try {
    const response = await accountsStore.addLikeDeposit(depositId)
    const updatedDeposit = data.value.find(deposit => deposit.id === depositId)
    if (updatedDeposit) {
      updatedDeposit.isLiked = response.action === 'added'
      localStorage.setItem('likedDeposits', JSON.stringify(data.value.filter(deposit => deposit.isLiked).map(deposit => deposit.id)))
    }
  } catch (error) {
    console.error('Error in toggleLikeDeposit:', error)
  }
}


</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
  background-color: #f0f4f8;
  font-family: 'Roboto', sans-serif;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  min-width: 230px; /* 카드 최소 너비 설정 */
  min-height : 280px;
  flex: 1 1 auto; /* 카드가 유동적으로 늘어날 수 있게 설정 */
}

.card:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card-title {
  font-weight: bold;
}

.card-body {
  background-color: #f8f9fa;
}

.clickable-image {
  cursor: pointer;
}

.detail-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.detail {
  position: relative;
  width: 70%;
  max-width: 400px;
  max-height: 80%;
  overflow-x: auto;
  overflow-y: auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.detail button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: #777;
}

/* 반응형 웹사이트를 위한 미디어 쿼리 */
@media (max-width: 767px) {
  .card {
    margin-bottom: 20px;
    width: 100%; /* 작은 화면에서는 카드 너비 100% */
  }

  .detail {
    width: 90%;
  }

  .form-select {
    width: 100%;
  }

  .d-flex {
    flex-direction: column;
    align-items: flex-start;
  }

  .d-flex select {
    width: 100%;
    margin-top: 10px;
  }
}
.card-footer {
  margin-top: auto; /* 카드의 하단으로 버튼을 내림 */
}

.thick-hr {
    border: 0;
    height: 3px; /* 원하는 높이로 설정 */
    background-color: rgb(51, 171, 182); /* 원하는 색상으로 설정 */
  }

.custom-border {
  border: 1px solid rgb(35, 83, 102);
}
</style>
