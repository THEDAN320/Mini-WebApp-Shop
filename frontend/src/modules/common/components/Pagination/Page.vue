<template>
  <li>
    <span v-if="page === 'dots'" class="dots-holder"> ... </span>
    <button
      v-else
      class="page"
      type="button"
      :aria-label="`Go to page ${page}`"
      :class="{ 'page-active': isActive }"
      :style="`background-color: ${isActive ? activeColor : 'transparent'};`"
      @click="clickHandler"
    >
      {{ page }}
    </button>
  </li>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";

export default defineComponent({
  name: "PageView",
  props: {
    page: {
      type: [String, Number],
      default: "dots",
    },
    current: {
      type: Number,
      default: 0,
    },
    activeColor: {
      type: String,
      default: "#e5e5e5",
    },
  },
  emits: ["update"],

  setup(props, { emit }) {
    const isActive = computed(() => {
      return props.page === props.current;
    });

    function clickHandler() {
      emit("update", props.page);
    }

    return { isActive, clickHandler };
  },
});
</script>

<style scoped lang="scss">
.page {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  margin: 0 4px;
  color: #333333;
  background-color: transparent;
  font-size: 16px;
  border-radius: 3px;
  box-sizing: border-box;
  border-color: transparent;
  cursor: pointer;
  outline: 0;
  user-select: none;

  &:hover {
    border: 1px solid #dedede;
  }

  &-active {
    color: #333333;
    // border: 1px solid #dedede;
  }
}

.dots-holder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  margin: 0 2px;
  box-sizing: border-box;
}
</style>
