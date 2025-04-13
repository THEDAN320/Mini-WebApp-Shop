<template>
    <div class="admin-panel">
      <h1>Админ-панель</h1>
      <goods-data-table />
    </div>
  </template>

  <script setup lang="ts">
  import GoodsDataTable from '../components/goodsDataTable.vue'
  </script>

  <style scoped>
  .admin-panel {
    padding: 20px;
  }

  h1 {
    margin-bottom: 20px;
    color: #333;
  }
  </style>
