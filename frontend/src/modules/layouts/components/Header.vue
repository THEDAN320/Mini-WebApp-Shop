<template>
  <header class="sticky top-0 z-30 border-b border-gray-200 bg-white">
    <div class="px-4 sm:px-6 lg:px-8">
      <div class="-mb-px flex h-16 flex-row items-center">
        <!-- Header: Left side -->
        <div class="flex">
          <!-- Hamburger button -->
          <button
            class="mr-6 text-gray-500 hover:text-gray-600 lg:hidden"
            @click.stop="$emit('toggle-sidebar')"
            aria-controls="sidebar"
            :aria-expanded="sidebarOpen"
          >
            <span class="sr-only">Open sidebar</span>
            <svg
              class="h-6 w-6 fill-current"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect x="4" y="5" width="16" height="2" />
              <rect x="4" y="11" width="16" height="2" />
              <rect x="4" y="17" width="16" height="2" />
            </svg>
          </button>

          <!--<Button :icon="ArrowBack" @click.stop="goBack" />

          <Button :icon="ArrowForward" @click.stop="goForward" class="ml-2" />-->
          <BreadcrumbNavigation></BreadcrumbNavigation>
        </div>

        <div class="flex grow"></div>

        <!-- Header: Right side -->
        <div class="flex items-center justify-end space-x-3">
          <router-link v-if="isYouOnline" to="/telephony/callcenter/" class="cursor-pointer">
            <div
              class="duration-250 flex items-center justify-center rounded-lg bg-gray-500 px-1.5 py-1 text-white transition hover:bg-red-600"
            >
              <div class="font-bold">Колл-центр</div>
            </div>
          </router-link>

          <!-- <button
            class="ml-3 flex h-8 w-8 items-center justify-center rounded-full bg-gray-100 transition duration-150 hover:bg-gray-200"
            :class="{ 'bg-gray-200': searchModalOpen }"
            @click.stop="searchModalOpen = true"
            aria-controls="search-modal"
          >
            <span class="sr-only">Search</span>
            <svg class="h-4 w-4" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
              <path
                class="fill-current text-gray-500"
                d="M7 14c-3.86 0-7-3.14-7-7s3.14-7 7-7 7 3.14 7 7-3.14 7-7 7zM7 2C4.243 2 2 4.243 2 7s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5z"
              />
              <path
                class="fill-current text-gray-400"
                d="M15.707 14.293L13.314 11.9a8.019 8.019 0 01-1.414 1.414l2.393 2.393a.997.997 0 001.414 0 .999.999 0 000-1.414z"
              />
            </svg>
          </button> -->
          <!-- <HeaderModalSearch
            id="search-modal"
            searchId="search"
            :modalOpen="searchModalOpen"
            @open-modal="searchModalOpen = true"
            @close-modal="searchModalOpen = false"
          />
          <HeaderDropdownNotifications align="right" /> -->
          <!-- Divider -->
          <hr class="h-6 w-px bg-gray-200" />
          <HeaderDropdownProfile align="right" />
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed, watch } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { ArrowBack, ArrowForward } from "@vicons/ionicons5";

// import Button from "@/modules/common/components/Button.vue";
// import HeaderModalSearch from "./HeaderModalSearch.vue";
// import HeaderDropdownNotifications from "./HeaderDropdownNotifications.vue";
// import HeaderDropdownHelp from "./HeaderDropdownHelp.vue";
import HeaderDropdownProfile from "./HeaderDropdownProfile.vue";
import BreadcrumbNavigation from "@/modules/common/components/BreadcrumbNavigation.vue";

export default {
  name: "HeaderView",
  props: ["sidebarOpen"],
  components: {
    BreadcrumbNavigation,
    // Button,
    // HeaderModalSearch,
    // HeaderDropdownNotifications,
    // HeaderDropdownHelp,
    HeaderDropdownProfile,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const searchModalOpen = ref(false);
    const isYouOnline = computed(() => store.getters["callCenter/GET_YOU_ONLINE"]);

    const goBack = () => {
      router.go(-1);
    };
    const goForward = () => {
      router.go(1);
    };

    return {
      ArrowBack,
      ArrowForward,
      searchModalOpen,
      goBack,
      goForward,
      isYouOnline,
    };
  },
};
</script>
