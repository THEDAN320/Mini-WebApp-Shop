<template>
  <ul class="pagination">
    <li v-if="!hideFirstButton" class="pagination-control">
      <ChevronBackCircle
        class="control"
        :class="{ 'control-active': isPrevControlsActive }"
        @click="goToFirst"
      />
    </li>
    <li class="pagination-control">
      <ChevronBack
        class="control"
        :class="{ 'control-active': isPrevControlsActive }"
        @click="goToPrev"
      />
    </li>
    <Page
      v-for="page in pagination"
      :key="`pagination-page-${page}`"
      :page="page"
      :current="modelValue"
      :active-color="activeColor"
      @update="updatePageHandler"
    />
    <li class="pagination-control">
      <ChevronForward
        class="control"
        :class="{ 'control-active': isNextControlsActive }"
        @click="goToNext"
      />
    </li>
    <li v-if="!hideLastButton" class="pagination-control">
      <ChevronForwardCircle
        class="control"
        :class="{ 'control-active': isNextControlsActive }"
        @click="goToLast"
      />
    </li>
  </ul>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import Page from "./Page.vue";
import {
  ChevronBack,
  ChevronForward,
  ChevronBackCircle,
  ChevronForwardCircle,
} from "@vicons/ionicons5";

export default defineComponent({
  name: "PaginationView",
  components: { ChevronBack, ChevronForward, ChevronBackCircle, ChevronForwardCircle, Page },
  props: {
    pages: {
      type: Number,
      default: 0,
    },
    rangeSize: {
      type: Number,
      default: 1,
    },
    modelValue: {
      type: Number,
      default: 0,
    },
    activeColor: {
      type: String,
      default: "#e5e5e5",
    },
    hideFirstButton: {
      type: Boolean,
      default: false,
    },
    hideLastButton: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue"],

  setup(props, { emit }) {
    // pagination
    const pagination = computed((): (number | string)[] => {
      const res = [];
      const minPaginationElems = 5 + props.rangeSize * 2;

      let rangeStart = props.pages <= minPaginationElems ? 1 : props.modelValue - props.rangeSize;
      let rangeEnd =
        props.pages <= minPaginationElems ? props.pages : props.modelValue + props.rangeSize;

      rangeEnd = rangeEnd > props.pages ? props.pages : rangeEnd;
      rangeStart = rangeStart < 1 ? 1 : rangeStart;

      if (props.pages > minPaginationElems) {
        const isStartBoundaryReached = rangeStart - 1 < 3;
        const isEndBoundaryReached = props.pages - rangeEnd < 3;

        if (isStartBoundaryReached) {
          rangeEnd = minPaginationElems - 2;
          for (let i = 1; i < rangeStart; i++) {
            res.push(i);
          }
        } else {
          res.push(1);
          res.push("dots");
        }

        if (isEndBoundaryReached) {
          rangeStart = props.pages - (minPaginationElems - 3);
          for (let i = rangeStart; i <= props.pages; i++) {
            res.push(i);
          }
        } else {
          for (let i = rangeStart; i <= rangeEnd; i++) {
            res.push(i);
          }
          res.push("dots");
          res.push(props.pages);
        }
      } else {
        for (let i = rangeStart; i <= rangeEnd; i++) {
          res.push(i);
        }
      }

      return res;
    });

    function updatePageHandler(params: number) {
      emit("update:modelValue", params);
    }

    // controls
    const isPrevControlsActive = computed((): boolean => {
      return props.modelValue > 1;
    });
    const isNextControlsActive = computed((): boolean => {
      return props.modelValue < props.pages;
    });

    function goToFirst(): void {
      if (isPrevControlsActive.value) {
        emit("update:modelValue", 1);
      }
    }
    function goToPrev(): void {
      if (isPrevControlsActive.value) {
        emit("update:modelValue", props.modelValue - 1);
      }
    }

    function goToLast(): void {
      if (isNextControlsActive.value) {
        emit("update:modelValue", props.pages);
      }
    }
    function goToNext(): void {
      if (isNextControlsActive.value) {
        emit("update:modelValue", props.modelValue + 1);
      }
    }

    return {
      pagination,
      updatePageHandler,
      isPrevControlsActive,
      isNextControlsActive,
      goToFirst,
      goToLast,
      goToPrev,
      goToNext,
    };
  },
});
</script>

<style scoped lang="scss">
.pagination {
  display: flex;
  flex-flow: row;
  flex-wrap: wrap;
  align-items: center;
  margin: 0;
  padding: 0;
  list-style-type: none;
}

.pagination-control {
  display: flex;
  align-items: center;
}

.control {
  position: relative;
  display: block;
  width: 18px;
  height: 18px;
  margin: 0 2px;
  fill: #bbbbbb;

  &-active {
    fill: #333333;
    cursor: pointer;
    transition: fill 0.2s ease-in-out;

    &:hover {
      fill: #000000;
      transition: fill 0.2s ease-in-out;
    }
  }
}
</style>
