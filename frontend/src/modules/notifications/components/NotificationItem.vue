<template>
  <div class="pointer-events-auto rounded-lg bg-white shadow-lg">
    <div class="overflow-hidden rounded-lg shadow-xl">
      <div class="p-4">
        <div class="flex items-start">
          <div class="shrink-0" v-if="notification.type">
            <SuccessIcon v-if="notification.type === 'success'" />
            <InfoIcon v-else-if="notification.type === 'info'" />
            <WarningIcon v-else-if="notification.type === 'warning'" />
            <ErrorIcon v-else-if="notification.type === 'error'" />
          </div>
          <div class="ml-3 w-0 flex-1 pt-0.5">
            <p class="text-sm font-medium leading-5 text-gray-900" v-if="notification.title">
              {{ notification.title }}
            </p>
            <p :class="`${notification.title ? 'mt-1' : ''} text-sm leading-5 text-gray-500`">
              {{ notification.content }}
            </p>
          </div>
          <div class="ml-4 flex shrink-0">
            <button
              @click="() => closeNotification(notification.id)"
              class="inline-flex text-gray-400 focus:text-gray-500 focus:outline-none"
            >
              <CloseIcon />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, onMounted } from "vue";
import { useStore } from "vuex";

import { ErrorIcon, InfoIcon, WarningIcon, SuccessIcon, CloseIcon } from "./icons";
import { INotification } from "../types";

export default defineComponent({
  components: {
    ErrorIcon,
    InfoIcon,
    WarningIcon,
    SuccessIcon,
    CloseIcon,
  },

  props: {
    notification: {
      type: Object as PropType<INotification>,
      required: true,
    },
  },

  setup(props) {
    const store = useStore();

    const closeNotification = (id: number) => {
      store.commit("notifications/REMOVE_NOTIFICATION", id);
    };

    onMounted(() => {
      if (props.notification.autoClose) {
        setTimeout(() => {
          store.commit("notifications/REMOVE_NOTIFICATION", props.notification.id);
        }, props.notification.duration);
      }
    });

    return {
      closeNotification,
    };
  },
});
</script>

<style lang="scss" scoped></style>
