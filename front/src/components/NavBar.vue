<template>
  <div class="nav-sticky"> 
  <header class="bg-header d-flex justify-content-end align-items-center" style="background-color:#90caf9;">
    <div v-if="store.userId" class="d-flex mt-1 me-5">
    <RouterLink :to="{name :'mypage', params:{id : store.userId}}" class="link-underline link-underline-opacity-0 me-3 text-color"> {{store.userId}} 님 </RouterLink>
    <button type="button" class="nav-link btn btn-link text-color" @click="store.logout">로그아웃</button>
  </div>
    <div v-else>
    <RouterLink class="nav-link text-success-emphasis" :to="{name : 'login' }"> 로그인 해주세요. </RouterLink>
  </div>
  </header>
  <nav class="navbar navbar-expand-lg bg-nav text-success-emphasis border-bottom shadow-sm" style="background-color: #90caf9;">
  <div class="container-fluid">
    <RouterLink class="navbar-brand text-success-emphasis" :to="{name : 'home' }">
      <img src="@/assets/logo.png" style="width:100px; height:40px;"alt="">
    </RouterLink>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <!-- store에서 isLogin 변수를 가지고 와서 회원가입/로그인 ---- 마이페이지/로그아웃/정보 토글 -->
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0" v-if="!store.isLogin">
        <li class="nav-item">
          <RouterLink class="nav-link text-success-emphasis" :to="{name : 'signup' }"> 회원가입 </RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link text-success-emphasis" :to="{name : 'login' }"> 로그인 </RouterLink>
        </li>
      </ul>
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0" v-if="store.isLogin">
        <li class="nav-item me-5">
          <RouterLink :to="{name:'deposit'}" class="nav-link text-success-emphasis">예·적금</RouterLink>
        </li>
        <li class="nav-item me-5">
          <RouterLink :to="{name:'stock'}" class="nav-link text-success-emphasis"> 주식 </RouterLink>
        </li>
        <li class="nav-item me-4">
          <RouterLink :to="{name:'recommend'}" class="nav-link text-success-emphasis"> 상품 추천 </RouterLink>
        </li>
        <!-- 로그아웃 (완료)-->
        <!-- 로그아웃 시 alert를 통해 확인 가능하도록 수정 -->
        
        <!-- 정보 (주식, 예금 등 드롭다운으로 관리할 예정 { 변동 가능 }) -->
      </ul>
    </div>
  </div>
</nav>

</div>

<RouterView />

</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAccountsStore } from '@/stores/accounts'
import { ref } from 'vue'
const store = useAccountsStore()
</script>

<style scoped>

.nav-sticky {
  position : sticky;
  top : 0 ;
  z-index : 1000;
}
.wrapper {
  padding: 8rem 0 6rem 0 ;
  position: relative;
  z-index: 1; }
  @media screen and (max-width: 1280px) {
    .wrapper {
      padding: 4rem 0 2rem 0 ; } }
  @media screen and (max-width: 736px) {
    .wrapper {
      padding: 3rem 0 1rem 0 ; } }
  @media screen and (max-width: 480px) {
    .wrapper {
      padding: 2rem 0 0.1rem 0 ; } }

.inner {
  margin: 0 auto;
  width: 100%;
  max-width: calc(100%); }
  @media screen and (max-width: 480px) {
    .inner {
      max-width: calc(100%); } }

.bg-header{
  background-color: #D3E1FB;
}
.bg-nav{
  background-color: #D3E1FB;
  font-weight: bold;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.text-color {
  color : #002046;
}
</style>