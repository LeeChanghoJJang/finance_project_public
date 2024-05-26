<template>
  <div class="outer-container">
    <div class="inner">
      <h1 class="fw-bold text-color">금융의 균형을 맞추다</h1>
      <h1 class="text-color-40 mb-5">Faest Balance Investment</h1>
      <h4 class="text-secondary">보다 용이한 수익 비교를 위해</h4>
      <h4 class="text-secondary">간편한 상품 검색을 이용해보세요!</h4>
      <button @click="goRecommend()" class="btn bg-black text-white fs-4 ps-3 pe-3 mt-3">상품 추천받기</button>
    </div>
    <!-- <div class="d-flex justify-content-center"> 
      <a class="text-center" href="#chart">
        <img src="@/assets/화살표.png" style="width:50px; height:50px" alt="">
      </a> 
    </div> 화살표 이동 구현해볼라고 했음 -->
  </div>
  <div id='chart' class="container ms-auto me-auto mt-5" v-if="bankStore">
    <div class="row">
      <div class="col-12 col-lg-6">
        <h3  class="text-center mt-5 mb-5 fw-bold">주식 순위 차트</h3>
        <div class="row g-2 p-2 mb-5">
          <div class="col-6">
            <div class="card-header fs-6 bg-primary bg-gradient pt-2 pb-2 text-white text-center rounded z-2">외국인 소진율 순</div>
            <img :src="path1" class="img-fluid animate-graph z-1" alt="Stock Price Graph" />
          </div>
          <div class="col-6">
            <div class="card-header fs-6 bg-primary bg-gradient pt-2 pb-2 text-white text-center rounded">거래량 순</div>
            <img :src="path2" class="img-fluid animate-graph" alt="Stock Price Graph" />
          </div>
        </div>
          <div class="row g-2 p-2 mb-5">
          <div class="col-6">
            <div class="card-header fs-6 bg-primary bg-gradient pt-2 pb-2 text-white text-center rounded">시가총액 순</div>
            <img :src="path3" class="img-fluid animate-graph" alt="Stock Price Graph" />
          </div>
          <div class="col-6">
            <div class="card-header fs-6 bg-primary bg-gradient pt-2 pb-2 text-white text-center rounded">배당수익률 순</div>
            <img :src="path4" class="img-fluid animate-graph" alt="Stock Price Graph" />
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6">
        <div class="d-flex align-items-center justify-content-center">
        <h3 class="mt-5 text-center fw-bold">시장지표</h3>
        <div class="d-flex align-items-center justify-content-center mb-4">
          <button class="btn btn-success mt-5 ms-3" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">환율 계산기</button>
          <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
            <div class="offcanvas-header">
              <h5 class="offcanvas-title" id="offcanvasRightLabel">환율 계산기</h5>
              <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
              <form class="form-floating" @submit.prevent>
                <input
                  type="text"
                  class="form-control"
                  id="floatingInputValue"
                  placeholder="숫자만 입력해 주세요"
                  v-model="won"
                  @input="filterInput"
                >
                <label for="floatingInputValue">숫자만 입력해 주세요</label>
              </form>
              <div>
                {{ formatNumber(won / 1) }} 원 ≒ {{ computedUSD }} 달러 ≒ {{ computedJPY }} 엔
              </div>
            </div>
          </div>
        </div>
      </div>
  <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
    <div class="carousel-inner">
      <div class="carousel-item active">
        <div class="d-flex flex-wrap justify-content-center g-3">
          <div class="d-flex">
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">원-옌 </h5>
              <p>{{ KRWToCNY }}</p>
            </div>
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">원-유로 </h5>
              <p>{{ KRWToEURO }}</p>
            </div>
          </div>
          <div class="d-flex">
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">원-달러 </h5>
              <p>{{ KRWToUSD }}</p>
            </div>
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">원-엔화 </h5>
              <p>{{ KRWToJPY }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="carousel-item">
        <div class="d-flex flex-wrap justify-content-center g-3">
          <div class="d-flex">
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">KOSPI</h5>
              <p>{{ kospi }}</p>
            </div>
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">KOSDAQ</h5>
              <p>{{ kosdaq }}</p>
            </div>
          </div>
          <div class="d-flex">
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">GDP</h5>
              <p>{{ gdp }}</p>
            </div>
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">Growth</h5>
              <p>{{ growth }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="carousel-item">
        <div class="d-flex flex-wrap justify-content-center g-3">
          <div class="d-flex">
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">기준금리</h5>
              <p>{{ basemoneyrate }}</p>
            </div>
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">콜금리</h5>
              <p>{{ callrate }}</p>
            </div>
          </div>
          <div class="d-flex">
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">CD금리</h5>
              <p>{{ cdrate }}</p>
            </div>
            <div class="market-box bg-white p-3 m-2 rounded shadow animate-box">
              <h5 class="fw-bold">KORIBOR</h5>
              <p>{{ koribor }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="align-middle">
      <button class="custom-carousel-bgc carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      </button>
      <button class="custom-carousel-bgc carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span> 
      </button>
    </div>
  </div>

        <hr class="section-divider border-top my-5">
        <h1 class="text-center mt-5 fw-bold">이용 서비스</h1>
        <div class="d-flex flex-wrap justify-content-center border-dark pt-4 pb-4">
          <div class="text-center m-3 service-item">
            <a href="" @click.prevent="goStock" class="link-underline link-underline-opacity-0 me-3 text-color">
              <img src="@/assets/stockmarket.jpg" class="img-fluid service-img" alt="">
              <div>주식 검색</div>
            </a>
          </div>
          <a href="" @click.prevent="goDeposit" class="link-underline link-underline-opacity-0 me-3 text-color">
            <div class="text-center m-3 service-item">
              <img src="@/assets/savings.jpg" class="img-fluid service-img" alt="">
              <div>예적금 검색</div>
            </div>
          </a>
          <a href="" @click.prevent="goRecommend" class="link-underline link-underline-opacity-0 me-3 text-color">
            <div class="text-center m-3 service-item">
              <img src="@/assets/dividends.jpg" class="img-fluid service-img" alt="">
              <div>상품 추천</div>
            </div>  
          </a>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden"></span>
      </div>
    </div>
  </div>

</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useAccountsStore } from '@/stores/accounts'
import { useBankStore } from '@/stores/bank'
import { useRouter } from 'vue-router'
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const store = useAccountsStore()
const bankStore = useBankStore()

const KRWToUSD = bankStore.KRWToUSD
const KRWToJPY = bankStore.KRWToJPY
const KRWToEURO = bankStore.KRWToEURO
const KRWToCNY = bankStore.KRWToCNY

const kospi = bankStore.kospi
const kosdaq = bankStore.kosdaq
const gdp = bankStore.gdp
const growth = bankStore.growth

const basemoneyrate = bankStore.basemoneyrate      
const callrate = bankStore.callrate
const cdrate = bankStore.cdrate
const koribor = bankStore.koribor

const dividend_ratio = bankStore.dividend_ratio 
const makret_value = bankStore.makret_value
const foreigner = bankStore.foreigner
const total_trade = bankStore.total_trade

const won = ref(0)

const path1 = bankStore.path1
const path2 = bankStore.path2
const path3 = bankStore.path3
const path4 = bankStore.path4

const router = useRouter()

const computedUSD = computed(() => {
  return formatNumber((won.value / KRWToUSD).toFixed(2))
})
const computedJPY = computed(() => {
  return formatNumber((won.value / KRWToJPY * 100).toFixed(2))
})

const formatNumber = (numberString) => {
  return numberString.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const goRecommend = function () {
  router.push({ name: 'recommend' })
}

const goStock = function() {
  router.push({name : 'stock'})
}

const goDeposit = function () {
  router.push({name: 'deposit'})
}

const filterInput = (event) => {
  const value = event.target.value
  const filteredValue = value.replace(/[^\d]/g, '')
  won.value = filteredValue
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
  background-color: #f0f4f8;
  font-family: 'Roboto', sans-serif;
}

.outer-container {
  position: relative;
  width: 100%;
  height: 100vh;
  background-image: url('@/assets/mains.jpg');
  background-size: cover;
  background-position: center;
}

.containers {
  height: 80vh;

}

.inner {
  width: 100%;
  max-width: 1200px;
  margin: 0;
  padding: 10%;
}

.img-fluid {
  width: 100%;
  height: 110%;
}

.text-center {
  font-weight: bold;
  font-size: 1.5rem;
  color: #333;
}

.border {
  border-width: 2px !important;
}

.border-top { 
  border-top :3px solid rgb(55, 127, 194) !important;
}

.border-bottom {
  border-bottom-width: 2px !important;
}

.border-dark {
  border-color: #000 !important;
}

.animate-graph {
  transition: transform 0.3s ease-in-out;
}

.animate-graph:hover {
  transform: translateY(-10px);
}

.animate-box {
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  min-width : 135px;
  min-height : 110px;
}

.animate-box:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.section-divider {
  border: 0;
  border-top: 1px solid #ccc;
  margin: 50px 0;
}

.card-header,
.service-item {
  font-weight: bold;
}

.card-header {
  background-color: #007bff;
  color: #fff;
}

.market-box {
  width: 120px;
  height: 100px;
  text-align: center;
  min-width: 100px;
  vertical-align: middle;
  gap:5px;
  /* display: flex;
  justify-content: center;
  align-items: center; */
  margin: 3px;
}

.service-img {
  min-width: 120px;
  height: 140px;
}

.carousel-inner .carousel-item h5,
.carousel-inner .carousel-item p {
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.carousel-control-prev,
.carousel-control-next {
  top: 50%;
  transform: translateY(-50%);
  border-radius: 50%; /* 둥근 모서리 적용 (선택 사항) */
  width: 40px; /* 버튼 크기 조정 (선택 사항) */
  height: 40px; /* 버튼 크기 조정 (선택 사항) */
  background-color: #fff;
  background-image: none; /* 기본 배경 이미지 제거 */
}

.custom-carousel-bgc {
  background-color: #fff !important;
  border: none !important;
  width: 40px; /* Adjust as needed */
  height: 40px; /* Adjust as needed */
  border-radius: 50%; /* Optional: Makes the button circular */
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-caption {
  background-color: rgba(0, 0, 0, 0.5);
  padding: 10px;
  border-radius: 5px;
}


.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-color: white; /* 원하는 색상으로 변경 */
  background-image: none; /* 기본 배경 이미지 제거 */
  width: 30px; /* 아이콘 크기 조정 (선택 사항) */
  height: 30px; /* 아이콘 크기 조정 (선택 사항) */
}

.carousel-control-prev-icon {
  border: solid #d3e0f9;
  border-width: 0 4px 4px 0;
  display: inline-block;
  padding: 6px;
  transform: rotate(135deg);
  -webkit-transform: rotate(135deg);
}

.carousel-control-next-icon {
  border: solid #d3e0f9;
  border-width: 0 4px 4px 0;
  display: inline-block;
  padding: 6px;
  transform: rotate(-45deg);
  -webkit-transform: rotate(-45deg);
}


.offcanvas-body {
  background-color: #fff;
}
.text-color {
  color : #002046;
}
.text-color-40 {
  color : #2a5c96;
}

.service-item {
  position: relative;
  overflow: hidden;
}

.service-item img {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.service-item:hover img {
  transform: translateY(-10px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 그림자 추가 */
}


</style>
