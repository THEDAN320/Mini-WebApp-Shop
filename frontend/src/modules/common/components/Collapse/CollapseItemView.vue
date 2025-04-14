<template>
  <details class="group">
    <summary
      class="relative flex cursor-pointer list-none flex-wrap items-center group-open:z-[1] group-open:rounded-b-none"
    >
      <div class="w-8">
        <div class="flex items-center justify-center">
          <n-icon size="16" class="group-open:rotate-90">
            <ChevronForward />
          </n-icon>
        </div>
      </div>

      <h3 class="flex flex-1 px-2 py-4 text-base font-semibold">
        <slot name="title"></slot>
      </h3>
    </summary>
    <div class="p-2">
      <slot name="content"></slot>
    </div>
  </details>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { NIcon } from "naive-ui";

import { ChevronForward } from "@vicons/ionicons5";

export default defineComponent({
  components: {
    NIcon,
    ChevronForward,
  },
  setup() {
    return {};
  },
});
</script>

<style scoped></style>
