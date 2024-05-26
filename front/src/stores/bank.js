import { ref, onMounted } from 'vue'
import { createPinia, defineStore } from 'pinia'
import axios from 'axios'

export const useBankStore = defineStore('bank', () => {
  const path1 = ref('')  
  const path2 = ref('')
  const path3 = ref('')
  const path4 = ref('')
  const kospi = ref(0)
  const kosdaq = ref(0)
  const KRWToUSD = ref(0)
  const KRWToJPY = ref(0)
  const KRWToEURO = ref(0)
  const KRWToCNY = ref(0)
  const growth = ref(0)
  const employ = ref(0)
  const five = ref(0)
  const gini = ref(0)
  const unemploy = ref(0)
  const basemoneyrate =ref(0)
  const callrate = ref(0)
  const cdrate = ref(0)
  const koribor = ref(0)
  const gdp = ref(0)
  const data = ref([])
  const banks = ref([])
  const makret_value = ref([])
  const total_trade = ref([])
  const foreigner = ref([])
  const dividend_ratio = ref([])

  const fetchData = async () => {
    if (KRWToJPY.value != 0) {
    try {
      const mainPage = await axios({
        method: 'get',
        url: `http://localhost:8000/bank/main/`,
      })
      console.log(mainPage.data)
      employ.value = mainPage.data.important_index[0].employ
      five.value = mainPage.data.important_index[0].five
      gini.value = mainPage.data.important_index[0].gini
      unemploy.value = mainPage.data.important_index[0].gini

      kospi.value = mainPage.data.market_index[0].kospi
      kosdaq.value = mainPage.data.market_index[0].kosdaq
      growth.value = mainPage.data.market_index[0].growth
      gdp.value = mainPage.data.market_index[0].gdp
      
      basemoneyrate.value = mainPage.data.interest_rate[0].basemoneyrate      
      callrate.value = mainPage.data.interest_rate[0].call_rate
      cdrate.value = mainPage.data.interest_rate[0].cdrate
      koribor.value = mainPage.data.interest_rate[0].koribor

      KRWToUSD.value = mainPage.data.exchange_rate[0].dollar
      KRWToJPY.value = mainPage.data.exchange_rate[0].yen
      KRWToEURO.value = mainPage.data.exchange_rate[0].euro
      KRWToCNY.value = mainPage.data.exchange_rate[0].cny
      
      path1.value = mainPage.data.image1
      path2.value = mainPage.data.image2
      path3.value = mainPage.data.image3
      path4.value = mainPage.data.image4

      dividend_ratio.value =mainPage.data.dividend_ratio
      foreigner.value =mainPage.data.foreigner
      total_trade.value =mainPage.data.total_trade
      makret_value.value =mainPage.data.makret_value

      const depositData = await axios({
        method : 'get',
        url : 'http://127.0.0.1:8000/bank/search/'
      })
      
      data.value = depositData.data
      banks.value = [...new Set(depositData.data.map(obj => obj.bank))].sort()

    } catch (error) {
      console.error('Error fetching data:', error)
    }}
  }

  // Store의 생성 시점에 데이터를 가져옵니다.
  onMounted(() => {
    fetchData()
  })


  return {
    path1,   
  path2,
  path3,
  path4,
  kospi, 
  kosdaq ,
  KRWToUSD,
  KRWToJPY,
  KRWToEURO,
  KRWToCNY,
  growth,
  employ,
  five,
  gini,
  unemploy,
  basemoneyrate,
  callrate,
  cdrate,
  koribor,
  gdp,
  data,
  banks,
  makret_value,
  total_trade,
  foreigner,
  dividend_ratio 
  }
}, { persist: true })

  