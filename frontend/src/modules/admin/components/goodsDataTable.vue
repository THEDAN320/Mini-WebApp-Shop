<template>
  <TableWithOrdering
    :table-min-width="768"
    :column-data="columnData"
    :order-by="orderBy"
    @change-order-by="changeOrderBy"
  >
    <template v-slot:tbody>
      <tr
        v-for="row in getGoods"
        :key="row.id"
        class="odd:bg-white even:bg-gray-50 hover:bg-gray-100"
      >
        <td class="px-2 py-1.5">
          <div class="flex items-center">
            <div class="">{{ row.id }}</div>
          </div>
        </td>
        <td class="px-2 py-1.5">
          <div class="">{{ row.name }}</div>
        </td>
        <td class="px-2 py-1.5">
          <div class="">{{ row.article }}</div>
        </td>
        <td class="px-2 py-1.5">
          <div class="">{{ row.type }}</div>
        </td>
        <td class="px-2 py-1.5">
          <div class="">{{ row.description }}</div>
        </td>
        <td class="px-2 py-1.5">
          <div class="">{{ row.price }}</div>
        </td>
        <td class="px-2 py-1.5">
          <div class="">{{ row.count }}</div>
        </td>
        <td class="px-2 py-1.5">
          <div class="">{{ row.url }}</div>
        </td>

        <td class="px-2 py-1.5">
          <div class="flex items-center justify-end">
            <DropdownEditMenu align="right">
              <li>
                <a
                  href="#"
                  class="flex items-center rounded px-1.5 py-1 text-sm font-medium text-gray-600 transition duration-200 ease-in-out hover:bg-gray-100 hover:text-gray-800"
                  @click.stop="openModalAdd(row)"
                >
                  <n-icon size="16" style="margin-right: 6px">
                    <PencilSharp />
                  </n-icon>
                  <span>Изменить</span>
                </a>
              </li>
              <li>
                <a
                  href="#"
                  class="flex items-center rounded px-1.5 py-1 text-sm font-medium text-red-500 transition duration-200 ease-in-out hover:bg-gray-100 hover:text-red-600"
                  @click.stop="deleteRow(row)"
                >
                  <n-icon size="16" style="margin-right: 6px">
                    <trash-outline />
                  </n-icon>
                  <span>Удалить</span>
                </a>
              </li>
            </DropdownEditMenu>
          </div>
        </td>
      </tr>
      <tr v-if="!getGoods || getGoods.length === 0">
        <td colspan="3" class="p-6 text-center text-gray-500">Нет данных</td>
      </tr>
    </template>

    <template v-slot:footer>
      <div class="my-3 flex items-center justify-start gap-2 sm:auto-cols-max sm:justify-end">
        <span>Всего: {{ totalGoods }}</span>
        <Pagination v-model="pageNumber" :pages="pageCount" @update:modelValue="handlePageChange" />
      </div>
    </template>
  </TableWithOrdering>

  <ModalView
    id="modal-form-change"
    :modalOpen="addModalOpen"
    :title="'Изменить товар'"
    @open-modal="toggleModal(true)"
    @close-modal="toggleModal(false)"
  >
    <template v-slot:content>
      <GoodsFormChange
        :init-data="initData"
        @success="handleFormSuccess"
        @cancel="toggleModal(false)"
      />
    </template>
  </ModalView>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { NIcon } from "naive-ui";
import { PencilSharp, TrashOutline } from "@vicons/ionicons5";

import { TableWithOrdering, IColumnData } from "@/modules/common/components/TableWithOrdering";
import DropdownEditMenu from "@/modules/common/components/DropdownEditMenu.vue";
import ModalView from "@/modules/common/components/ModalView.vue";
import GoodsFormChange from "./goodsFormChange.vue";
import Pagination from "@/modules/common/components/Pagination";

import { formateLocalDataTime } from "@/modules/common/utils/date-time";
import { dispatchNotification } from "@/modules/common/utils/notifications";
import {
  getURIQueryParams,
  QueryParamEnum,
  generateDataForURIQueryParams,
} from "@/modules/common/utils/__useDynamicQueryParams";

export default defineComponent({
  components: {
    TableWithOrdering,
    NIcon,
    DropdownEditMenu,
    PencilSharp,
    TrashOutline,
    ModalView,
    GoodsFormChange,
    Pagination,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const router = useRouter();

    //
    const queryParamsConfig = {
      pageNumber: { default: 1, type: QueryParamEnum.Number },
      pageSize: { default: 20, type: QueryParamEnum.Number },
      orderBy: { default: null, type: QueryParamEnum.StringArray },
    };
    const queryParams = ref(getURIQueryParams(route.query, queryParamsConfig));
    const pageNumber = ref<number>(Number(queryParams.value.pageNumber) || 1);
    const pageSize = ref<number>(Number(queryParams.value.pageSize) || 20);
    const orderBy = ref<any>(queryParams.value.orderBy);
    //

    const pageCount = ref<number>(1);
    const columnData = ref<IColumnData[]>([
      {
        title: "ID",
        key: "id",
        isSortable: true,
      },
      {
        title: "Название",
        key: "name",
        isSortable: true,
      },
      {
        title: "Артикул",
        key: "article",
        isSortable: true,
      },
      {
        title: "Тип",
        key: "type",
        isSortable: true,
      },
      {
        title: "Описание",
        key: "description",
        isSortable: true,
      },
      {
        title: "Цена",
        key: "price",
        isSortable: true,
      },
      {
        title: "Количество",
        key: "count",
        isSortable: true,
      },
      {
        title: "Ссылка",
        key: "url",
        isSortable: true,
      },
      {
        title: "",
        key: "salconversiones",
        isSortable: false,
      },
    ]);

    const addModalOpen = ref(false);
    const toggleModal = (status: boolean) => (addModalOpen.value = status);
    const initData = ref();

    const getGoods = computed(() => {
      const goods = store.getters["goods/GET_ALL_GOODS"];
      return goods;
    });

    const totalGoods = computed(() => {
      const total = store.getters["goods/GET_TOTAL_ALL_GOODS"];
      return total;
    });

    const fetchGoods = async (totalShowObjs: number, currentPage: number) => {
      try {
        const response = await store.dispatch("goods/FETCH_ALL_GOODS", {
          pagi: {
            limit: 20,
            offset: currentPage > 0 ? currentPage - 1 : 0,
          },
        });
        return response;
      } catch (error) {
        dispatchNotification(
          "error",
          "Ошибка",
          "Не удалось загрузить данные. Пожалуйста, попробуйте позже.",
          true,
          5000,
        );
      }
    };

    const deleteGoods = async (id: number) => {
      try {
        await store.dispatch("goods/DELETE_GOODS", id);
        dispatchNotification("success", "Успешно", "Товар успешно удален", true, 3000);
        getDataForTable(); // Обновляем данные после удаления
      } catch (error) {
        dispatchNotification(
          "error",
          "Ошибка",
          "Не удалось удалить товар. Пожалуйста, попробуйте позже.",
          true,
          5000,
        );
      }
    };

    const timerForDataTebleSearch = ref<any>(null);
    const getDataForTable = async () => {
      clearTimeout(timerForDataTebleSearch.value);
      timerForDataTebleSearch.value = setTimeout(async () => {
        const currentPageSize = Math.max(Number(pageSize.value) || 20, 1);
        const currentPage = Math.max(Number(pageNumber.value) || 1, 1);

        await fetchGoods(currentPageSize, currentPage).then(() => {
          const total = Number(totalGoods.value) || 0;
          if (total > 0) {
            pageCount.value = Math.max(Math.ceil(total / currentPageSize), 1);
          } else {
            pageCount.value = 1;
          }
        });
      }, 500);
    };

    onMounted(() => {
      const params = getURIQueryParams(route.query, queryParamsConfig);
      pageNumber.value = Math.max(Number(params.pageNumber) || 1, 1);
      pageSize.value = Math.max(Number(params.pageSize) || 20, 1);
      orderBy.value = params.orderBy;
      getDataForTable();
    });

    const openModalAdd = (row: any) => {
      initData.value = {
        id: row.id,
        name: row.name,
        article: row.article,
        type: row.type,
        description: row.description,
        price: row.price,
        count: row.count,
        url: row.url,
      };
      addModalOpen.value = true;
    };
    const deleteRow = async (row: any) => {
      await deleteGoods(row.id);
    };
    watch(pageCount, (currentValue: any, oldValue: any) => {
      if (currentValue < 1) {
        pageCount.value = 1;
        pageNumber.value = 1;
      }
    });

    watch(
      () => route.query,
      (currentValue: any, oldValue: any) => {
        const params = getURIQueryParams(route.query, queryParamsConfig);
        pageNumber.value = Math.max(Number(params.pageNumber) || 1, 1);
        pageSize.value = Math.max(Number(params.pageSize) || 20, 1);
        orderBy.value = params.orderBy;
        getDataForTable();
      },
    );

    const changeOrderBy = (data: string[] | null) => {
      orderBy.value = data;
      router.push({
        query: generateDataForURIQueryParams({ ...route.query, orderBy: data, pageNumber: 1 }),
      });
    };

    const handlePageChange = async (currentPage: number) => {
      pageNumber.value = currentPage;
      const qp = {
        ...queryParams.value,
        pageNumber: pageNumber.value,
      };
      router.push({ query: generateDataForURIQueryParams({ ...route.query, ...qp }) });
    };

    const handleFormSuccess = () => {
      toggleModal(false);
      getDataForTable();
    };

    return {
      formateLocalDataTime,
      getGoods,
      addModalOpen,
      toggleModal,
      initData,
      openModalAdd,
      deleteRow,
      totalGoods,
      pageCount,
      handlePageChange,
      handleFormSuccess,
      columnData,
      orderBy,
      changeOrderBy,
      pageNumber,
    };
  },
});
</script>

<style scoped></style>
