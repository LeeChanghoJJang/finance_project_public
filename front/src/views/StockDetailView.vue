<template>
  <div class="container-fluid">
    <StockSearch />
    <hr class="custom-border">
    <div class="row content-wrapper">
      <div v-if="stockInfo" class="col-12">
        <div class="row">
          <!-- 기본정보 -->
          <div class="basic-info col-md-4 mb-4">
            <div class="d-flex align-items-center">
              <h1>{{stockInfo.stock_info.name}}</h1>
              <button type="button" class="btn btn-primary ms-2" @click="toggleFavorite(stockInfo.stock_info.name)">
                <svg v-if="isFavorite" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
                  <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.56.56 0 0 0-.163-.505L1.71 6.745l4.052-.576a.53.53 0 0 0 .393-.288L8 2.223l1.847 3.658a.53.53 0 0 0 .393.288l4.052.575-2.906 2.77a.56.56 0 0 0-.163.506l.694 3.957-3.686-1.894a.5.5 0 0 0-.461 0z"></path>
                </svg>
                {{ isFavorite ? '관심 해제' : '관심 등록' }}
              </button>
            </div>
            <p class="info-text">현재가 : {{ formatNumber(stockInfo.stock_info.price)}}원</p>
            <p class="info-text">52주 최고 : {{ formatNumber(stockInfo.stock_info.highprice_52)}}원</p>
            <p class="info-text">52주 최저 : {{ formatNumber(stockInfo.stock_info.lowprice_52)}}원</p>
            <p class="info-text">배당수익률 : {{ formatNumber(stockInfo.stock_info.dividend_ratio)}}%</p>
            <p class="info-text">1주당 배당금 : {{ formatNumber(stockInfo.stock_info.dividend)}}원</p>
            <p class="info-text">시가 총액 : {{ stockInfo.stock_info.market_value}}원</p>
            <p class="info-text">PBR : {{ stockInfo.stock_info.pbr}}</p>
            <p class="info-text">PER : {{ stockInfo.stock_info.per}}</p>
          </div>

          <!-- 재무정보 및 주가차트, 버튼 섹션 -->
          <div class="financial-info col-md-8 mb-4">
            <h2>재무정보</h2>
            <table class="table">
              <thead>
                <tr>
                  <th style="width:50px;">구분</th>
                  <th>매출액 (억원)</th>
                  <th>영업이익 (억원)</th>
                  <th>당기순이익 (억원)</th>
                  <th>유동비율</th>
                  <th>부채비율</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>값</td>
                  <td v-if="stockInfo.finances[0]">{{ formatFinancial(stockInfo.finances[0].revenue) }}</td>
                  <td v-if="stockInfo.finances[0]">{{ formatFinancial(stockInfo.finances[0].operating_pr) }}</td>
                  <td v-if="stockInfo.finances[0]">{{ formatFinancial(stockInfo.finances[0].profits) }}</td>
                  <td v-if="stockInfo.finances[0]">{{ Math.round(stockInfo.finances[0].fluid_asset / stockInfo.finances[0].fluid_liabilites * 100) }}%</td>
                  <td v-if="stockInfo.finances[0]">{{ Math.round(stockInfo.finances[0].total_liabilites / stockInfo.finances[0].total_equity * 100) }}%</td>
                </tr>
              </tbody>
            </table>
            <div class="d-flex mt-4">
              <div class="stock-chart">
                <img :src="path" class="stock-chart-img" alt="Stock Price Graph" />
              </div>
              <div class="button-section ms-1">
                <button class="btn btn-primary mb-4 btn-size" type="button" data-bs-toggle="collapse" data-bs-target="#collapse1" aria-expanded="false" aria-controls="collapse1">
                  관련기사
                </button>
                <button class="btn btn-primary mb-4 btn-size" type="button" data-bs-toggle="collapse" data-bs-target="#collapse2" aria-expanded="false" aria-controls="collapse2">
                  종목토론
                </button>
                <button class="btn btn-primary btn-size" type="button" data-bs-toggle="collapse" data-bs-target="#collapse3" aria-expanded="false" aria-controls="collapse3">
                  리서치
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 기업소식 정보 -->
        <div class="col-12 mb-4">
          <div class="collapse" id="collapse1">
            <div class="card card-body">
              <div class="accordion accordion-flush" id="accordionFlushExample">
                <div v-for="(news, index) in stockInfo.naversearch" :key="index" class="accordion-item">
                  <h2 class="accordion-header">
                    <button 
                      class="accordion-button collapsed" 
                      type="button" 
                      :data-bs-toggle="'collapse'"
                      :data-bs-target="'#flush-collapse' + index" 
                      aria-expanded="false" 
                      :aria-controls="'flush-collapse' + index" 
                      v-html="news.title">
                    </button>
                  </h2>
                  <div 
                    :id="'flush-collapse' + index" 
                    class="accordion-collapse collapse" 
                    :data-bs-parent="'#accordionFlushExample'">
                    <a :href="news.link" target="_blank" rel="noopener" class="text-black link-underline link-underline-opacity-0">          
                      <div class="accordion-body" v-html="news.description"></div>
                      <div class="accordion-body text-secondary"> 클릭하시면 원문으로 이동합니다.</div>
                    </a>        
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 종목 토론 정보 -->
        <div class="col-12 mb-4">
          <div class="collapse" id="collapse2">
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
                <tr v-for="article in articleStore.article" :key="article.id">
                  <th>{{ article.id }}</th>
                  <th class="text-truncate" style="max-width: 150px;" @click="goDetail(article.id)">{{ article.title }}</th>
                  <th>{{ allUserPK[article.user] }}</th>
                  <th>{{ formatDateTime(article.created_at) }}</th>
                  <th>{{ article.comment_set.length }}</th>
                  <th>
                  </th>
                  <button v-if="accountsStore.userId===accountsStore.allUserPK[article.user]" type="submit" class="btn btn-secondary ms-2" @click="deleteArticle(article.id)">삭제</button>
                </tr>
              </tbody>
            </table>
            <a class="btn btn-primary" @click.prevent="goWrite">글쓰기</a>
          </div>
        </div>

        <!-- 리서치 정보 -->
        <div class="col-12 mb-4">
          <div class="collapse" id="collapse3">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>종목명</th>
                  <th>제목</th>
                  <th>작성일자</th>
                  <th>증권사</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="research in stockInfo.researches" :key="research.name">
                  <td>{{ research.name }}</td>
                  <td @click="goToResearch(research.url)" style="cursor: pointer; color: black; text-decoration: none;">{{ research.title }}</td>
                  <td>{{ research.date }}</td>
                  <td>{{ research.reporter }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div v-else class="col-12">
        <div class="text-center">
          <div class="spinner-border" role="status">
            <span class="visually-hidden"></span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 오른쪽에 고정된 관련 기업 섹션 -->
  <div v-if="stockInfo.relation_corporation" class="related">
    <button type="button" class="btn btn-primary align-items-right" @click="isClicked" v-if="clicked">
      숨기기
    </button>
    <button type="button" class="btn btn-primary align-items-right" @click="isClicked" v-if="!clicked">
      관련기업
      <span class="badge text-bg-secondary">{{ relatedLength }}</span>
    </button>
    <div v-if="clicked"> 
      <div v-for="related in stockInfo.relation_corporation" :key="related.name">
        <a href="" @click.prevent="goRelated(related.name)" class="text-black link-underline link-underline-opacity-0 mt-2">
          {{related.name}}
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUpdated } from 'vue';
import axios from 'axios';
import StockSearch from '@/components/StockSearch.vue';
import { useRoute, useRouter } from 'vue-router';
import { useArticleStore } from '@/stores/article';
import { format, isToday, parseISO } from 'date-fns';

import { useAccountsStore } from '@/stores/accounts';
const path = ref('');
const stockInfo = ref('');
const router = useRouter();
const query = ref('');
const detail = ref('');
const clicked = ref(false);
const accountsStore = useAccountsStore();
const isFavorite = ref(false);
const data = ref([]); // 빈 배열로 초기화

const goRelated = function(name) {
  router.push({ name: 'stockDetail', params: { id: name } });
};

const formatNumber = (numberString) => {
  return numberString.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

const formatFinancial = (number) => {
  return formatNumber(Math.round(number / 100000000));
};

onMounted(() => {
  const route = useRoute();
  const corp = route.params.id;
  axios.get(`http://127.0.0.1:8000/stock/${corp}/search_detail/`).then((response) => {
    path.value = response.data.image;
    query.value = corp;
  });
  axios.get(`http://127.0.0.1:8000/stock/${corp}/search/`).then((response) => {
    stockInfo.value = response.data;
  });
});

onUpdated(() => {
  const route = useRoute();
  const corp = route.params.id;
  if (query.value !== corp) {
    axios.get(`http://127.0.0.1:8000/stock/${corp}/search_detail/`).then((response) => {
      detail.value = response.data;
      path.value = response.data.image;
      query.value = corp;
      clicked.value = false;
    });
    axios.get(`http://127.0.0.1:8000/stock/${corp}/search/`).then((response) => {
      stockInfo.value = response.data;
    });
  }
});

const isClicked = () => {
  clicked.value = !clicked.value;
};

const relatedLength = computed(() => {
  return stockInfo.value.relation_corporation.length;
});

// 초기 로컬 스토리지에서 관심 등록 상태 가져오기
onMounted(async () => {
  try {
    const route = useRoute();
    const corp = route.params.id;
    const favoriteStocks = localStorage.getItem('favoriteStocks');
    if (favoriteStocks) {
      const favoriteStockCodes = JSON.parse(favoriteStocks);
      isFavorite.value = favoriteStockCodes.includes(corp);
    }
  } catch (error) {
    console.error('Error fetching stock data:', error);
  }
});

const toggleFavorite = async (stockName) => {

  if (accountsStore.userId === null) {
    if (window.confirm('로그인이 필요한 기능입니다. \n로그인 페이지로 이동하시겠습니까?')) {
    router.push({name : 'login'})}
    return
  }

  try {
    // 관심 등록/해제 요청
    const response = await accountsStore.addLikeStock(stockName);
    // 로컬 스토리지에서 관심 등록 상태 가져오기
    let favoriteStocks = localStorage.getItem('favoriteStocks');
    // 초기에 로컬 스토리지에 해당 키에 대한 항목이 존재하지 않으면 빈 배열로 설정
    if (!favoriteStocks) {
      favoriteStocks = '[]';
    }
    let favoriteStockCodes = JSON.parse(favoriteStocks);
    // 관심 등록 상태 토글
    if (response.action === 'added') {
      favoriteStockCodes.push(stockName);
    } else {
      favoriteStockCodes = favoriteStockCodes.filter(code => code !== stockName);
    }
    // 로컬 스토리지에 업데이트된 관심 등록 상태 저장
    localStorage.setItem('favoriteStocks', JSON.stringify(favoriteStockCodes));
    // isFavorite 상태 업데이트
    isFavorite.value = response.action === 'added';
  } catch (error) {
    console.error('Error toggling favorite:', error);
  }
};

function formatDateTime(dateTime) {
  const date = parseISO(dateTime);
  if (isToday(date)) {
    return format(date, 'HH:mm');
  } else {
    return format(date, 'MM.dd');
  }
}

// articles에 전체 게시글 저장
const articleStore = useArticleStore();

const route = useRoute();
const now = ref(route.params.id);

onMounted(() => {
  articleStore.getArticle(route.params.id);
});

onUpdated(() => {
  if (now.value !== route.params.id) {
    now.value = route.params.id;
    articleStore.getArticle(route.params.id);
  }
});
const goToResearch = (url) => {
  window.open(url, '_blank');
};

// 게시글 작성자에 대응하는 user.pk 정보 저장
const allUserPK = accountsStore.allUserPK;

// 글쓰기로 이동
const goWrite = function () {
  router.push({ name: 'articleWrite', params: { id: route.params.id } });
};

const goDetail = function (id) {
  console.log(articleStore.article);
  router.push({ name: 'articleDetail', params: { id: route.params.id, article: id } });
};

const deleteArticle = function (articleId) {
  // console.log(article.value.id)
  if (window.confirm("게시글을 삭제하시겠습니까?")) {
  articleStore.deleteArticle(route.params.id, articleId)
}
}
</script>

<style scoped>
/* Global Styles */
.container-fluid {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 800px; /* 화면 최소길이 조정 */
}

.content-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

h2 {
  color: #2c3e50;
}
.table {
  border-radius: 20px;
}
.table th,
.table td {
  color: #34495e;
}

.card-body {
  background-color: #f9f9f9;
}

.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
}

.accordion-button {
  background-color: #ecf0f1;
  color: #2c3e50;
}

/* Basic Info Styles */
.basic-info {
  background-color: #ecf0f1;
  padding: 20px;
  border-radius: 8px;
}

.basic-info h1 {
  display: flex;
  align-items: center;
  font-size: 2rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.basic-info p {
  margin: 15px 0; /* 세로 간격을 더 넓힘 */
  font-size: 1.2rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

/* Financial Info Styles */
.financial-info {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}

.financial-info h2 {
  margin-bottom: 20px;
}

.financial-info .table {
  background-color: #fff;
  table-layout: fixed; /* 표 레이아웃 고정 */
}

.stock-chart-img {
  max-width: 800px; /* 가로로 더 키움 */
  width: 95%;
  height: 101%;
  border-radius:20px;
}

/* Button Section Styles */
.button-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
}

/* Related Companies Styles */
.related {
  position: fixed;
  top: 12%;
  right: 0;
  min-width: 150px;
  max-width: 200px;
  max-height: 80%;
  overflow-y: auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000; /* 다른 콘텐츠 위에 고정되도록 z-index 설정 */
}

.related a {
  display: block;
  margin-bottom: 10px;
  color: #2c3e50;
}

.related a:hover {
  text-decoration: underline;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 0.3rem;
}

.btn-size {
  min-width : 90px;
}
.custom-border {
  border: 1px solid rgb(35, 83, 102);
}
</style>
