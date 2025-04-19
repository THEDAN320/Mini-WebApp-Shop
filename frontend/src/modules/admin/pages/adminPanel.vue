<template>
  <div class="admin-panel">
    <div class="flex">
      <sidebar />
      <div class="flex-1 p-6">
        <div class="mb-6 flex items-center justify-between">
          <h1 class="text-2xl font-semibold text-gray-900">Товары</h1>
          <n-button type="primary" @click="openAddModal">Добавить товар</n-button>
        </div>
        <goods-data-table />
      </div>
    </div>
  </div>

  <!-- Modal for adding new products -->
  <ModalView
    id="modal-add-product"
    :modalOpen="addModalOpen"
    title="Добавить товар"
    @open-modal="addModalOpen = true"
    @close-modal="addModalOpen = false"
  >
    <template v-slot:content>
      <GoodsFormChange @success="handleFormSuccess" @cancel="addModalOpen = false" />
    </template>
  </ModalView>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Sidebar from "@/modules/layouts/components/Sidebar.vue";
import GoodsDataTable from "../components/goodsDataTable.vue";
import GoodsFormChange from "../components/goodsFormChange.vue";
import ModalView from "@/modules/common/components/ModalView.vue";
import { NButton } from "naive-ui";

const addModalOpen = ref(false);

const openAddModal = () => {
  addModalOpen.value = true;
};

const handleFormSuccess = () => {
  addModalOpen.value = false;
  // Refresh the data table
  window.location.reload();
};
</script>

<style scoped>
.admin-panel {
  min-height: 100vh;
  background-color: #f9fafb;
}
</style>
