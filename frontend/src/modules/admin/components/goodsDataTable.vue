<template>
    <n-data-table
      :columns="columns"
      :data="goods"
      :pagination="pagination"
      :loading="loading"
    />
  </template>

  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { NDataTable } from 'naive-ui'
  import { getAllGoods } from '@/modules/admin/api'

  const goods = ref([])
  const loading = ref(false)
  const pagination = ref({
    pageSize: 10
  })

  const columns = [
    {
      title: 'ID',
      key: 'id'
    },
    {
      title: 'Название',
      key: 'name'
    },
    {
      title: 'Цена',
      key: 'price'
    },
    {
      title: 'Описание',
      key: 'description'
    }
  ]

  onMounted(async () => {
    loading.value = true
    try {
      const response = await getAllGoods({})
      goods.value = response.data
    } catch (error) {
      console.error('Ошибка при загрузке товаров:', error)
    } finally {
      loading.value = false
    }
  })
  </script>
