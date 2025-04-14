<template>
  <div>
    <ul class="mb-3 flex rounded bg-gray-100 p-1 text-center text-gray-500">
      <li v-for="item in dataTabs" :key="item.id">
        <div
          class="flex justify-center p-2"
          :class="{
            'cursor-pointer': canSwitchTabs,
            'rounded bg-white text-indigo-900 shadow': item.id === currentActiveTabId,
          }"
          @click.stop="canSwitchTabs && requestSetActiveTab(item.id)"
        >
          {{ item.name }}
        </div>
      </li>
    </ul>

    <!-- Content -->
    <div class="p-1">
      <!-- <template v-for="item in dataTabs" :key="item.id">
  <slot v-if="item.id === currentActiveTabId" :name="item.id"></slot>
</template> -->
      <slot :name="currentActiveTabId"></slot>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, PropType } from "vue";

export default defineComponent({
  props: {
    dataTabs: {
      type: Array as PropType<{ name: string; id: string }[]>,
      default: () => [
        { name: "Main", id: "main" },
        { name: "Second", id: "second" },
      ],
    },
    activeTabId: {
      type: String as PropType<string | null>,
      default: null,
    },
    canSwitchTabs: {
      type: Boolean,
      default: true,
    },
  },
  setup(props, context) {
    const currentActiveTabId = ref(
      props.activeTabId || (props.dataTabs.length > 0 ? props.dataTabs[0].id : null),
    );

    watch(
      () => props.activeTabId,
      (newVal) => {
        currentActiveTabId.value =
          newVal || (props.dataTabs.length > 0 ? props.dataTabs[0].id : null);
      },
    );

    watch(
      () => props.dataTabs,
      (newVal) => {
        if (!newVal.some((tab) => tab.id === currentActiveTabId.value)) {
          currentActiveTabId.value = newVal.length > 0 ? newVal[0].id : null;
        }
      },
    );

    const requestSetActiveTab = (activeTab: string) => {
      context.emit("change-active-tab", activeTab);
      currentActiveTabId.value = activeTab;
    };

    return {
      currentActiveTabId,
      requestSetActiveTab,
    };
  },
});
</script>

<style scoped></style>
