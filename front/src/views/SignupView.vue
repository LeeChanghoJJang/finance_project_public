<template>
  <h1 class="text-center mt-5">회원가입</h1>
  <form class="row p-5 g-4" @submit.prevent="signUp">
    
    <div class="col-2 col-lg-4"></div>

    <div class="col-8 col-lg-4">
      <label for="username" class="form-label">아이디</label>
      <input type="text" class="form-control" id="username" v-model.trim="username">
      <div class="text-secondary"> 아이디는 6-12자만 가능합니다.</div>
    </div>

    <div class="col-2 col-lg-4"></div>

    <div class="col-2 col-lg-4"></div>

    <div class="col-8 col-lg-4">
      <label for="email" class="form-label">이메일</label>
      <input type="email" class="form-control" id="email" v-model.trim="email">
    </div>

    <div class="col-2 col-lg-4"></div>

    <div class="col-2 col-lg-4"></div>

    <div class="col-8 col-lg-4">
      <label for="password1" class="form-label">비밀번호</label>
      <input type="password" class="form-control" id="password1" v-model.trim="password1">
    </div>
    <div class="col-2 col-lg-4"></div>


    <div class="col-2 col-lg-4"></div>

    <div class="col-8 col-lg-4">
      <label for="password2" class="form-label">비밀번호 확인</label>
      <input type="password" class="form-control" id="password2" v-model.trim="password2">
      <div v-if="password2 && password1!== password2" class="text-danger">비밀번호가 일치하지 않습니다.</div>
    </div>   
    <div class="col-2 col-lg-4"></div>


    <div class="col-2 col-lg-4"></div>

    <div class="col-8 col-lg-4">
      <label for="inputState" class="form-label">주거래 은행</label>
      <select id="inputState" class="form-select" v-model.trim="likeBank">
        <option selected disabled>은행 선택</option>
        <option v-for="bank in bankStore.banks">
        {{ bank }}</option>
      </select>
    </div>
    <div class="col-2 col-lg-4"></div>
    
    <div class="col-2 col-lg-4"></div>
    <div class="col-8 col-lg-4">
    <button type="submit" class="btn btn-primary">회원가입</button>
  </div>

</form>


</template>

<script setup>
import {ref} from 'vue'
import {useAccountsStore} from '@/stores/accounts'
import {useBankStore} from '@/stores/bank'

const bankStore = useBankStore()


const store = useAccountsStore()
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const email = ref(null)
const likeBank = ref('은행 선택')



const signUp = function () { 
  if (likeBank.value === '은행 선택') {
    alert ('주거래 은행을 선택해주세요.') }
  else if (!username.value) {
    alert ('아이디를 입력해주세요.')}
  else if (!email.value) {
    alert ('이메일을 입력해주세요.')
  }
  else if (!password1.value) {
    alert ('비밀번호를 입력해주세요.')}
  else if (!password2.value) {
    alert ('비밀번호 확인을 입력해주세요.')}
  else if (password1.value!== password2.value) {
    alert ('비밀번호가 일치하지 않습니다.')}
  else if (!(6<=username.value.length<=12)) {
    alert ('아이디는 6-12자만 가능합니다.')}
  else if (password1.value.length < 8) {
    alert ('비밀번호는 8자리 이상 입력해주세요.')}
  else if (Object.values(store.allUserPK).includes(username.value)) {
    alert ("이미 등록된 아이디 입니다.")
  }
    else {

  const payload = {
    username : username.value,
    password1 : password1.value,
    password2 : password2.value,
    email : email.value,
    like_bank : likeBank.value,
  }
    store.signUp(payload)
  }
}
</script>

<style>

</style>
