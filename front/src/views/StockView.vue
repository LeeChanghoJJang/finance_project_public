<template>
  <div class="container">
    <StockSearch />
    <div></div>
  </div>
</template>

<script setup>
import StockSearch from '@/components/StockSearch.vue';
</script>

<style>
.container {
  margin-left: 120px;
  margin-right: 120px;
  margin-top: 50px; /* 위쪽 마진을 추가합니다. 필요한 만큼 조정하세요. */
}

</style>
