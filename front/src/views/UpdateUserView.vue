<template>
  <div>

    <div v-if="isLogin">
      <form class="row p-5 g-4" @submit.prevent="updateUserInfo">

      <div class="col-2 col-lg-4"></div>
      <div class="col-8 col-lg-4">
        <label for="Email" class="form-label me-3">ID</label>
        <p> {{ userId }}</p>
      </div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-8 col-lg-4">
        <p>
        <label for="button" class="form-label me-3">password</label>
        </p>
        <!-- 비밀번호 변경으로 이어주기 -->
        <button type="button" class="btn btn-primary" @click="">비밀번호 변경</button>
      </div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-8 col-lg-4">
        <label for="Email" class="form-label me-3">E-mail</label>
        <input v-model="email" class="form-control" placeholder="Email">
      </div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-8 col-lg-4">
        <label for="FirstName" class="form-label me-3">First Name</label>
        <input v-model="firstName" class="form-control" placeholder="First Name">
      </div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-8 col-lg-4">
        <label for="LastName" class="form-label me-3">Last Name</label>
        <input v-model="lastName" class="form-control" placeholder="Last Name">
      </div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-2 col-lg-4"></div>
      <div class="col-8 col-lg-4">
        <label for="inputState" class="form-label">주거래 은행</label>
      <select id="inputState" class="form-select" v-model.trim="likeBank">
        <option v-for="bank in bankStore.banks">
        {{ bank }}</option>
      </select>
        <button type="submit" class="btn btn-primary mt-2">Update</button>
      </div>
      <div class="col-2 col-lg-4"></div>
    </form>
    </div>
    <div v-else>
      <p>Please log in</p>
    </div>
  </div>
</template>

<script setup>
import { ref,watch } from 'vue'
import { useAccountsStore } from '@/stores/accounts'
import { useBankStore } from '@/stores/bank'

const bankStore = useBankStore()
const store = useAccountsStore()
const { userStock, userId, isLogin, logout, updateUser } = store
// 유저가 미리 입력한 값이 있는 경우 들고오기
const email = ref(userStock.user.email)
const firstName= ref(userStock.user.first_name)
const lastName= ref(userStock.user.last_name)
const likeBank = ref(userStock.user.like_bank)
// 유저정보와 보유종목을 들고 오기 위해 axios 요청


const updateUserInfo = () => {
  console.log(likeBank.value)
  const form = {
    email : email.value,
    first_name : firstName.value,
    last_name : lastName.value,
    like_bank : likeBank.value
  }
  console.log(form)
  updateUser(form)
}

// watch(userInfo,(newUser) => {
//   if (newUser) {
//     form.value.email = newUser.email || ''
//     form.value.first_name = newUser.first_name || ''
//     form.value.last_name = newUser.last_name || ''
//   }
// }, { immediate: true }) 


</script>

<style scoped>

</style>