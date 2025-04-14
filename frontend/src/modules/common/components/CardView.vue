<template>
  <div
    class="col-span-full flex-col rounded-sm border border-gray-200 bg-white shadow-lg sm:col-span-6"
  >
    <div v-if="showHeader" class="border-b border-gray-100 px-5 py-4">
      <div class="md:flex md:items-center md:justify-between">
        <div class="flex items-center justify-start">
          <h2 class="mr-4 text-lg font-semibold text-gray-800">
            {{ nameHeader }}
          </h2>
          <slot name="header-left"></slot>
        </div>

        <div class="mt-6 flex items-center justify-start md:mt-0 md:justify-end">
          <slot name="header-right"></slot>
        </div>
      </div>
    </div>

    <div class="p-3">
      <slot name="content"></slot>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    showHeader: {
      type: Boolean,
      default: () => false,
    },
    nameHeader: {
      type: String,
      default: () => "Название",
    },
  },
  setup() {
    return {};
  },
});
</script>

<style scoped></style>
