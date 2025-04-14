<template>
  <div
    v-if="isBlocked"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
  >
    <n-spin size="large" />
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { NSpin } from "naive-ui";

export default defineComponent({
  components: {
    NSpin,
  },
  props: {
    isBlocked: {
      type: Boolean,
      required: true,
    },
  },
});
</script>

<style scoped></style>
