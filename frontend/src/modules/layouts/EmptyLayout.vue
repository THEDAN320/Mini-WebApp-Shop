<template>
  <div>
    <NotificationsProvider />
    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import NotificationsProvider from "@/modules/notifications/components/NotificationsProvider.vue";

export default defineComponent({
  name: "EmptyLayout",
  components: { NotificationsProvider },
  setup() {
    return {};
  },
});
</script>

<style scoped></style>
