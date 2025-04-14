<template>
  <!-- Modal backdrop -->
  <div
    v-if="modalOpen"
    class="fixed inset-0 z-50 bg-gray-900 bg-opacity-30 transition-opacity"
    aria-hidden="true"
  ></div>
  <!-- Modal dialog -->
  <div
    v-if="modalOpen"
    :id="id"
    class="fixed inset-0 top-20 z-50 mb-4 flex items-start justify-center overflow-hidden px-4 sm:px-6"
    role="dialog"
    aria-modal="true"
  >
    <div
      ref="modalContent"
      class="elem-modal max-h-full overflow-y-scroll rounded bg-white shadow-lg"
      :style="contentStyles"
    >
      <div ref="content" class="relative p-4">
        <div v-if="title !== ''" class="pb-6 text-center text-lg font-semibold text-gray-800">
          {{ title }}
        </div>

        <div v-if="isClosable" class="absolute right-2 top-2">
          <n-icon
            size="30"
            class="rounded hover:cursor-pointer hover:bg-gray-200"
            @click="closeModal"
          >
            <close-outline />
          </n-icon>
        </div>
        <!-- Content -->
        <slot name="content"></slot>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from "vue";
import { NIcon } from "naive-ui";
import { CloseOutline } from "@vicons/ionicons5";

export default defineComponent({
  name: "ModalView",
  components: {
    NIcon,
    CloseOutline,
  },
  props: {
    id: {
      type: String,
      requered: true,
    },
    modalOpen: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: () => "",
    },
    minWidth: {
      type: String,
      default: "600px",
    },
    maxWidth: {
      type: String,
      default: "800px",
    },
    fullWidth: {
      type: Boolean,
      default: false,
    },
    isClosable: {
      type: Boolean,
      default: true,
    },
  },
  emits: ["open-modal", "close-modal"],

  setup(props, { emit }) {
    const modalContent = ref();

    const closeModal = () => {
      emit("close-modal");
    };

    const contentStyles = computed(() => {
      return {
        minWidth: props.fullWidth ? "100%" : props.minWidth,
        maxWidth: props.fullWidth ? "100%" : props.maxWidth,
      };
    });

    return {
      modalContent,
      closeModal,
      contentStyles,
    };
  },
});
</script>

<style lang="scss" scoped>
.elem-modal {
  overflow: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.elem-modal::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>
