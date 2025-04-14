<template>
  <div class="admin-panel">
    <div class="flex">
      <sidebar />
      <div class="flex-1 p-6">
        <h1 class="mb-6 text-2xl font-semibold text-gray-900">Товары</h1>
        <goods-data-table />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from "@/modules/layouts/components/Sidebar.vue";
import GoodsDataTable from "../components/goodsDataTable.vue";
</script>

<style scoped>
.admin-panel {
  min-height: 100vh;
  background-color: #f9fafb;
}
</style>
