<template>
  <div ref="table" :class="[isExistHeight]">
    <!-- Table -->
    <div :class="[currentTableWidth >= tableMinWidth ? 'overflow-visible' : 'overflow-x-scroll']">
      <table
        class="relative w-full table-auto text-left"
        :style="{ minWidth: tableMinWidth + 'px' }"
      >
        <div v-if="isLoading" class="absolute flex h-14 w-full items-center justify-center">
          <n-spin size="large" />
        </div>

        <!-- Table header -->
        <thead class="rounded-sm bg-gray-200 text-xs uppercase text-gray-500">
          <template v-if="columnData === null || columnData === undefined">
            <slot name="thead"></slot>
          </template>
          <template v-else>
            <tr>
              <th
                v-for="column in newColumnData"
                :key="column.key"
                class="select-none p-2 hover:bg-gray-300"
                @click.stop="column.isSortable ? sortColumn(column.key) : ''"
              >
                <div class="flex font-semibold" :class="{ 'cursor-pointer': column.isSortable }">
                  <span>{{ column.title }}</span>

                  <div class="flex w-4 items-center justify-center">
                    <span
                      v-if="column.isSortable && column.sortingOrder !== undefined"
                      class="flex items-center justify-center"
                    >
                      <n-icon v-if="column.sortingOrder === 'asc'" size="14">
                        <CaretUp />
                      </n-icon>
                      <n-icon v-if="column.sortingOrder === 'desc'" size="14">
                        <CaretDown />
                      </n-icon>
                    </span>
                  </div>
                </div>
              </th>
            </tr>
          </template>
        </thead>

        <!-- Table body -->
        <tbody class="divide-y divide-gray-50 text-sm font-medium">
          <!-- Row -->
          <slot name="tbody"></slot>
        </tbody>
      </table>
    </div>
    <!-- Table footer -->
    <slot name="footer"></slot>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted, PropType, computed } from "vue";
import { NIcon, NSpin } from "naive-ui";
import { CaretUp, CaretDown } from "@vicons/ionicons5";

import { IColumnData, IExtentedColumnData } from "./types";
import type { typeSortingOrder } from "./types";

export default defineComponent({
  name: "TableView",
  emits: ["change-order-by"],
  components: {
    NIcon,
    NSpin,
    CaretUp,
    CaretDown,
  },

  props: {
    tableMinWidth: {
      type: Number,
      default: 0,
    },
    hieght: {
      type: null as unknown as PropType<number | null>,
      default: null,
    },
    columnData: {
      type: null as unknown as PropType<IColumnData[] | null>,
      default: null,
    },
    orderBy: {
      type: null as unknown as PropType<string[] | null>,
      default: null,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
  },

  setup(props, context) {
    const table = ref();
    const currentTableWidth = ref(1);
    const newColumnData = ref<IExtentedColumnData[] | null>(null);

    const handleWindowSizeChange = () => {
      const tableRect = table.value.getBoundingClientRect();
      currentTableWidth.value = tableRect.width;
    };
    onMounted(() => {
      window.addEventListener("resize", handleWindowSizeChange);
      handleWindowSizeChange();

      if (props.columnData !== null) {
        newColumnData.value = [...props.columnData];

        if (props.orderBy !== null) {
          for (const item of props.orderBy) {
            const targetKey: string = item.split("__")[0];
            const targetSortingOrder: typeSortingOrder = item.split("__")[1];
            const res = newColumnData.value.map((item: IExtentedColumnData) => {
              if (item.key === targetKey) {
                item.sortingOrder = targetSortingOrder;
              }
              return item;
            });
          }
        }
      }
    });

    onUnmounted(() => {
      window.removeEventListener("resize", handleWindowSizeChange);
    });

    const isExistHeight = computed(() => {
      if (props.hieght !== null) {
        return `h-[${props.hieght}px] overflow-hidden overflow-y-auto`;
      }
      return null;
    });

    // Ordering

    const sortColumn = (key: string) => {
      let newOrderBy: string[] | null = null;
      if (newColumnData.value !== null) {
        let targetColumnData = removeOtherSortingOrderForColumnData(newColumnData.value, key);
        const result = targetColumnData.map((item: IExtentedColumnData) => {
          if (item.key === key) {
            if (item.sortingOrder === undefined) {
              item.sortingOrder = "asc";
              newOrderBy = [key + "__asc"];
            } else if (item.sortingOrder === "asc") {
              item.sortingOrder = "desc";
              newOrderBy = [key + "__desc"];
            } else {
              item.sortingOrder = undefined;
              newOrderBy = null;
            }
          }
          return item;
        });
        targetColumnData = result;
      }
      context.emit("change-order-by", newOrderBy);
    };

    /**
     * Ф-ция удаляет данные о sortingOrder у каждой колонки, кроме выбранной.
     */
    const removeOtherSortingOrderForColumnData = (
      columnData: IExtentedColumnData[],
      key: string,
    ) => {
      return columnData.map((item: IExtentedColumnData) => {
        if (item.key !== key) {
          item.sortingOrder = undefined;
        }
        return item;
      });
    };

    return {
      table,
      currentTableWidth,
      isExistHeight,
      //
      newColumnData,
      sortColumn,
    };
  },
});
</script>

<style scoped></style>
