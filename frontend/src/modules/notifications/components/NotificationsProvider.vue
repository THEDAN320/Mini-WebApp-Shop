<template>
  <div class="pointer-events-none fixed inset-0 flex items-start justify-end px-4 py-6 sm:p-6">
    <div class="w-full max-w-sm">
      <TransitionGroup
        appear
        tag="div"
        :enter-active-class="
          getNotificationsCount > 1
            ? 'transform ease-out delay-200 duration-200 transition'
            : 'transform ease-out duration-200 transition'
        "
        enter-from-class="translate-x-4 opacity-0"
        enter-to-class="translate-x-0 opacity-100"
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
        move-class="transition ease-in-out duration-300"
      >
        <Notification
          v-for="(notification, idx) in getNotifications"
          :key="notification.id"
          :notification="notification"
          :class="idx > 0 ? 'mt-4' : ''"
        />
      </TransitionGroup>
    </div>
  </div>
  <slot></slot>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useStore } from "vuex";

import Notification from "./NotificationItem.vue";

export default defineComponent({
  components: {
    Notification,
  },

  setup() {
    const store = useStore();

    const getNotifications = computed(
      () => store.getters["notifications/GET_DATA_ALL_NOTIFICATIONS"],
    );

    const getNotificationsCount = computed(
      () => store.getters["notifications/GET_COUNT_ALL_NOTIFICATIONS"],
    );

    return {
      getNotifications,
      getNotificationsCount,
    };
  },
});
</script>

<style lang="scss" scoped>
.delay-200 {
  transition-delay: 200ms;
}
</style>
