<template>
  <div class="container">
    <h1 class="mt-4">마이페이지</h1>
    <div v-if="userStock" class="user-info">
      <div class="user-detail mt-3">
        <h3 class="section-title text-white">사용자 정보</h3>
        <table class="table table-bordered user-table no-side-borders rounded-table">
          <tbody>
            <tr>
              <th style="width:20%">사용자명</th>
              <td>{{ userStock.user.username }}</td>
            </tr>
            <tr>
              <th>이메일</th>
              <td>{{ userStock.user.email }}</td>
            </tr>
            <tr>
              <th>이름</th>
              <td>{{ userStock.user.first_name }} {{ userStock.user.last_name }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="user-stocks mt-3">
        <h3 class="section-title text-white">관심 종목 정보</h3>
        <div class="table-container">
          <table class="table table-bordered stocks-table no-side-borders rounded-table">
            <thead>
              <tr>
                <th>종목명</th>
                <th>종목코드</th>
                <th>전일가격</th>
                <th style="width:12%">주당배당금</th>
                <th>PBR</th>
                <th>PER</th>
                <th style="width:14%">52주 최저가</th>
                <th style="width:14%">52주 최고가</th>
                <th>삭제</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(stock, index) in userStock.user_stocks" :key="index" class="stock-item" :class="{'odd-row': index % 2 === 1, 'even-row': index % 2 === 0}">
                <td>{{ stock.stock.name }}</td>
                <td>{{ stock.stock.stock_code }}</td>
                <td>{{ stock.stock.price }}</td>
                <td>{{ stock.stock.dividend_ratio }}</td>
                <td>{{ stock.stock.pbr }}</td>
                <td>{{ stock.stock.per }}</td>
                <td>{{ stock.stock.highprice_52 }}</td>
                <td>{{ stock.stock.lowprice_52 }}</td>
                <td>
                  <button class="btn btn-danger" @click="deleteUserStock(stock.stock.id)">삭제</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="userDeposit" class="user-info">
        <div class="user-detail mt-3">
          <h3 class="section-title text-white">관심 예적금 정보</h3>
          <div class="table-container">
            <table class="table table-bordered deposits-table no-side-borders rounded-table">
              <thead>
                <tr>
                  <th style="width:20%">상품명</th>
                  <th style="width:10%">은행</th>
                  <th style="width:33%">이자율</th>
                  <th style="width:37%">우대조건</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(deposits, index) in userDeposit.user_deposits" :key="index" class="deposit-item">
                  <td>{{ deposits.product }}</td>
                  <td>{{ deposits.bank }}</td>
                  <td>
                    <table class="inner-table">
                      <thead>
                        <tr>
                          <th>가입기간</th>
                          <th>최고금리</th>
                          <th>기본금리</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(depositOption, index) in deposits.depositoption_set" :key="index">
                          <td>{{ depositOption.period }}개월</td>
                          <td v-if="depositOption.intr_rate2">{{ depositOption.intr_rate2 }}%</td>
                          <td v-else>-</td>
                          <td>{{ depositOption.intr_rate }}%</td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                  <td>{{ deposits.spcl_cnd }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <button class="btn btn-primary ms-2" @click="updateuserinfo">내 정보 수정하기</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted, watch } from 'vue';
import { useAccountsStore } from '@/stores/accounts/'
const router = useRouter()
const store = useAccountsStore()
const userStock = ref()
const userDeposit = ref()

const updateuserinfo = function () {
  router.push({ name: 'updateuser' })
}

const deleteUserStock = async function (stockId) {
  await store.deleteUserStock(stockId)
  userStock.value.user_stocks = userStock.value.user_stocks.filter(stock => stock.stock.id !== stockId)
}

const deleteUserDeposit = async function (depositId) {
  if (userDeposit.value && userDeposit.value.user_deposits) {
    userDeposit.value.user_deposits = userDeposit.value.user_deposits.filter(deposit => deposit.deposit.id !== depositId)
  }
  await store.deleteUserDeposit(depositId)
}

onMounted(async () => {
  await store.getMyPageUserStock()
  await store.getMyPageUserDeposit()
  userStock.value = store.userStock
  userDeposit.value = store.userDeposit
})

watch(
  () => store.userStock,
  (newVal) => {
    userStock.value = newVal
  }
)

watch(
  () => store.userDeposit,
  (newVal) => {
    userDeposit.value = newVal
  }
)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
  background-color: #94c3da;
  font-family: 'Roboto', sans-serif;
}

.container {
  margin: 20px;
  padding: 0 100px;
}

.user-info {
  margin-bottom: 20px;
}

.section-title {
  background-color: #5089EB;
  padding: 10px;
  color: #002B5E;
  border-radius: 5px;
  
}

.table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden; /* Ensures the border-radius is applied */
 
}

.table th,
.table td {
  border: 1px solid #A7BBC7;
  padding: 8px;
  text-align: center;
  vertical-align: middle;
  
}

.table th {
  background-color: #D3E1FB;
  color: #002B5E;
}

.table tbody tr.odd-row {
  background-color: #397ba4 !important;
}

.table tbody tr.even-row {
  background-color: #885151 !important;
}

.table-bordered th,
.table-bordered td {
  border: 1px solid #A7BBC7;
}

.inner-table th,
.inner-table td {
  border: 1px solid #EFF1F3;
  padding: 8px;
  text-align: center;
  vertical-align: middle;
}

.table-container {
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
}

.table-container table {
  width: 100%;
  table-layout: fixed;
}

.stocks-table thead th,
.deposits-table thead th {
  background-color: #D3E1FB;
  color: #002B5E;
  position: sticky;
  top: 0;
  z-index: 1;
}
/* #003675, #2A5C96, #D3E1FB, #002B5E */
/* 페이지 전체에 양쪽 여백 추가 */
@media (min-width: 768px) {
  .container {
    margin-left: auto;
    margin-right: auto;
    max-width: 1000px;
  }
}

/* 반응형 웹사이트를 위한 미디어 쿼리 */
@media (max-width: 767px) {
  .container {
    padding: 0 10px;
  }

  .table th, .table td {
    padding: 5px;
    font-size: 12px;
  }

  .inner-table th, .inner-table td {
    padding: 5px;
    font-size: 12px;
  }

  .section-title {
    font-size: 16px;
    padding: 8px;
  }
}

/* Remove border from the sides of the tables */
.no-side-borders th,
.no-side-borders td {
  border-left: none !important;
  border-right: none !important;
}

/* Rounded corners for the table */
.rounded-table {
  border-radius: 8px;
  overflow: hidden;
}
</style>
