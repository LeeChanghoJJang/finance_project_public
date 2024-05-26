<template>

<h1 class="text-center mt-5">로그인</h1>

<form class="row p-5 g-4" @submit.prevent="login">
  <div class="col-2 col-lg-4"></div>
  <div class="col-8 col-lg-4">
    <label for="username" class="form-label">아이디</label>
    <input type="text" class="form-control" id="username" v-model.trim="username">
  </div>
  <div class="col-2 col-lg-4"></div>
  <div class="col-2 col-lg-4"></div>
  <div class="col-8 col-lg-4">
    <label for="password1" class="form-label">비밀번호</label>
    <input type="password" class="form-control" id="password1" v-model.trim="password">
  </div>
  <div class="col-2 col-lg-4"></div>
  <div class="col-2 col-lg-4"></div>
  <div class="col-8 col-lg-4">
    <button type="submit" class="btn btn-primary">로그인</button>
    <button class="btn btn-primary ms-2" @click.prevent="goSignup">회원가입</button>
  </div>
  
</form>

</template>

<script setup>
import {ref} from 'vue'
import {useAccountsStore} from '@/stores/accounts'
import {useRouter} from 'vue-router'

const store = useAccountsStore()
const username = ref(null)
const password = ref(null)
const router = useRouter()
const login = function () { 
  const payload = {
    username : username.value,
    password : password.value,
  }
    store.login(payload)
  password.value = null
}

const goSignup = function () {
  router.push({name:'signup'})
}

</script>

<style>

</style>
