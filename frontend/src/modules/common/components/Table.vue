<template>
  <div ref="table" :class="[isExistHeight]">
    <!-- Table -->
    <div :class="[currentTableWidth >= tableMinWidth ? 'overflow-visible' : 'overflow-x-scroll']">
      <table class="w-full table-auto text-left" :style="{ minWidth: tableMinWidth + 'px' }">
        <!-- Table header -->
        <thead class="rounded-sm bg-gray-200 text-xs uppercase text-gray-500">
          <slot name="thead"></slot>
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

export default defineComponent({
  name: "TableView",
  props: {
    tableMinWidth: {
      type: Number,
      default: 0,
    },
    hieght: {
      type: null as unknown as PropType<number | null>,
      default: null,
    },
  },

  setup(props) {
    const table = ref();
    const currentTableWidth = ref(1);

    const handleWindowSizeChange = () => {
      if (table.value) {
        const tableRect = table.value.getBoundingClientRect();
        currentTableWidth.value = tableRect.width;
      }
    };
    onMounted(() => {
      window.addEventListener("resize", handleWindowSizeChange);
      handleWindowSizeChange();
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

    return {
      table,
      currentTableWidth,
      isExistHeight,
    };
  },
});
</script>

<style scoped></style>
