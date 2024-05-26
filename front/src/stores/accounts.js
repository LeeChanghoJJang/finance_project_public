import { ref, computed, onMounted } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAccountsStore = defineStore('counter', () => {
  const userId = ref(null)
  const router = useRouter()
  const token = ref(null)
  const API_URL = 'http://127.0.0.1:8000'
  const allUserPK = ref()
  const user = ref(null)

  const getUserList = function () {
    axios({
      method : 'get',
      url : `${API_URL}/accounts/mypage/get_all_users`
    })
      .then(response => {
        allUserPK.value = response.data
      })
  }

  onMounted(() => {
    getUserList()
  })



  const signUp = function (payload) {
    const { username, password1, password2, like_bank, email } = payload
    const password = password1
  
    axios ({
      method : 'post',
      url : `${API_URL}/accounts/signup/`,
      data : {
        username, password1, password2, like_bank, email
      }
    })
      .then((response) => {
        console.log(response.data)
        login ({ username, password })
        getUserList()
        router.push({ name: 'home' })
      })
      .catch((error) => {
        console.log(error)
        router.push({ name:'signup' })
      })
  }

  const login = function (payload) { 
    const { username, password } = payload
    axios ({
      method : 'post',
      url : `${API_URL}/accounts/login/`,
      data : {
        username, 
        password
      }
    })
      .then ((response)=> {
        userId.value = username
        token.value = response.data.key
        fetchUser()
        router.push({ name: 'home' })
      })
      .catch ((error) => {
        router.push({ name: 'login' })
        window.alert('아이디 또는 비밀번호를 확인해주세요.')
      })
  }
  
  const fetchUser = function () {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/user/`, 
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
      .then((response) => {
        console.log(response.data)
        user.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }
  
  const updateUser = function (payload) {
    axios({
      method: 'put',
      url: `${API_URL}/accounts/mypage/`,
      headers: {
        'Authorization': `Token ${token.value}`
      },
      data: payload
    })
      .then((response) => {
        user.value = response.data
        window.alert('정보 수정이 완료되었습니다.')
        router.push({ name:'mypage', params:{ id: userId.value } })
      })
      .catch((error) => {
        console.log(error)
        window.alert('입력을 확인해주세요.')
      })
  }

  const userStock = ref(null)
  const userDeposit = ref(null)

  const getMyPageUserStock = function () {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/mypage/get_user_stocks/`,
      headers: {
        'Authorization': `Token ${token.value}`
      },
    })
      .then((response) => {
        userStock.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const getMyPageUserDeposit = function () {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/mypage/get_user_deposits/`,
      headers: {
        'Authorization': `Token ${token.value}`
      },
    })
      .then((response) => {
        userDeposit.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const deleteUserStock = function (StockId) {
    axios({
      method: 'delete',
      url: `${API_URL}/accounts/mypage/delete_userstock/${StockId}`,
      headers: {
        'Authorization': `Token ${token.value}`
      },
    })
      .then(() => {
        getMyPageUserStock() // 삭제 후 최신 데이터를 가져옴
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const deleteUserDeposit = function (DepositId) {
    axios({
      method: 'delete',
      url: `${API_URL}/accounts/mypage/delete_userdeposit/${DepositId}`,
      headers: {
        'Authorization': `Token ${token.value}`
      },
    })
      .then(() => {
        getMyPageUserDeposit() // 삭제 후 최신 데이터를 가져옴
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const addLikeDeposit = function (depositId) {
    return axios ({
      method : 'post',
      url : `${API_URL}/bank/${depositId}/likes/`,
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
      .then((response) => {
        console.log(response.data)
        return response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 로그인 여부 확인용
  const isLogin = computed(() => {
    return token.value !== null
  })

  // 로그아웃
  const logout = function () {
    token.value = null
    userId.value = null
    window.alert("로그아웃 되었습니다.")
    router.push({ name :"home" })
  }
  const recommend_list = ref(null)
  // 상품 추천받기
  const recommend = function (standard) {
    axios({
      method: 'get',
      url: `${API_URL}/stock/recommend/${standard}`,
      headers: {
        'Authorization': `Token ${token.value}`
      },
    })
      .then((response) => {
        recommend_list.value = response.data
        console.log(response.data)
        return recommend_list
      })
      .catch((error) => {
        console.log(error)
      })
  }

  // 주식 관심종목 등록 및 해제
  const addLikeStock = function (stockName) {
    return axios ({
      method : 'post',
      url : `${API_URL}/accounts/mypage/create_userstock/${stockName}/`,
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
      .then((response) => {
        console.log(response.data)
        return response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  return {
    allUserPK,
    API_URL, 
    signUp, 
    token, 
    login, 
    isLogin, 
    logout, 
    userId,
    updateUser,
    getMyPageUserStock,
    getMyPageUserDeposit,
    userStock,
    userDeposit,
    deleteUserStock,
    deleteUserDeposit,
    addLikeDeposit,
    recommend,
    recommend_list,
    addLikeStock
  }
}, { persist : true }
)
