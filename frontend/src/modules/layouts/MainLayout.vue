<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <Sidebar :sidebarOpen="sidebarOpen" @close-sidebar="sidebarOpen = false" />

    <!-- Content area -->
    <div class="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
      <div class="absolute z-60 h-screen bg-gray-100 font-sans text-gray-900 antialiased">
        <NotificationsProvider />
      </div>

      <!-- Site header -->
      <Header :sidebarOpen="sidebarOpen" @toggle-sidebar="sidebarOpen = !sidebarOpen" />

      <main>
        <div class="mx-auto w-full p-4 sm:px-6">
          <router-view />
        </div>
      </main>
      <!-- <Banner /> -->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRoute } from "vue-router";
import Sidebar from "@/modules/layouts/components/Sidebar.vue";
import Header from "@/modules/layouts/components/Header.vue";

import NotificationsProvider from "@/modules/notifications/components/NotificationsProvider.vue";

export default defineComponent({
  name: "MainLayout",
  components: {
    Sidebar,
    Header,
    // Banner,
    NotificationsProvider,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const sidebarOpen = ref(false);

    const fetchLocales = async (totalShowObjs: number, currentPage: number) =>
      await store.dispatch("locales/FETCH_LOCALES", {
        limit: totalShowObjs,
        offset: currentPage > 0 ? currentPage - 1 : 0,
      });

    onMounted(() => {
      fetchLocales(9999, 0);
      const userMe = store.getters["users/GET_USER_ME_WITH_PERMISSIONS"];
      if (userMe && userMe.id) {
        store.dispatch("orders/FETCH_OPERATOR_USER", userMe.id);
      }
    });

    return {
      route,
      sidebarOpen,
    };
  },
});
</script>

<style scoped></style>
