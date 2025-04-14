<template>
  <div>
    <!-- Sidebar backdrop (mobile only) -->
    <div
      class="fixed inset-0 z-40 bg-slate-900 bg-opacity-30 transition-opacity duration-200 lg:z-auto lg:hidden"
      :class="sidebarOpen ? 'opacity-100' : 'pointer-events-none opacity-0'"
      aria-hidden="true"
    ></div>

    <!-- Sidebar -->
    <div
      id="sidebar"
      ref="sidebar"
      class="no-scrollbar absolute left-0 top-0 z-40 flex h-screen w-64 shrink-0 flex-col overflow-y-scroll bg-slate-800 p-4 transition-all duration-200 ease-in-out lg:static lg:left-auto lg:top-auto lg:w-20 lg:translate-x-0 lg:overflow-y-auto lg:sidebar-expanded:!w-64 xl:!w-64"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-64'"
    >
      <!-- Sidebar header -->
      <div class="mb-6 flex justify-between pr-3 sm:px-2">
        <!-- Close button -->
        <button
          ref="trigger"
          class="text-slate-500 hover:text-slate-400 lg:hidden"
          @click.stop="$emit('close-sidebar')"
          aria-controls="sidebar"
          :aria-expanded="sidebarOpen"
        >
          <span class="sr-only">Close sidebar</span>
          <svg class="size-6 fill-current" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M10.7 18.7l1.4-1.4L7.8 13H20v-2H7.8l4.3-4.3-1.4-1.4L4 12z" />
          </svg>
        </button>
      </div>

      <!-- Links -->
      <div class="space-y-8">
        <!-- Pages group -->
        <div>
          <h3 class="pl-3 text-xs font-semibold uppercase text-slate-500">
            <span
              class="hidden w-6 text-center lg:block lg:sidebar-expanded:hidden xl:hidden"
              aria-hidden="true"
              >•••</span
            >
            <span class="lg:hidden lg:sidebar-expanded:block xl:block">{{ $t("") }}</span>
          </h3>

          <template v-for="item in data" :key="`${item.type}_${item.name}`">
            <template v-if="item.type === 'group'">
              <ul v-if="item.groupAccess" class="mt-3">
                <SidebarLinkGroup
                  v-slot="parentLink"
                  :activeCondition="
                    currentRoute.fullPath.includes(item.routePartUriPath) ||
                    item.routePartUriPath === 'orders'
                  "
                >
                  <a
                    class="block truncate text-slate-200 transition duration-150"
                    :class="
                      currentRoute.fullPath === '/' ||
                      currentRoute.fullPath.includes(item.routePartUriPath)
                        ? 'hover:text-slate-200'
                        : 'hover:text-white'
                    "
                    href="#0"
                    @click.prevent="
                      sidebarExpanded ? parentLink.handleClick() : (sidebarExpanded = true)
                    "
                  >
                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <n-icon v-if="item.icon !== null" size="20" class="mr-3">
                          <component :is="item.icon"></component>
                        </n-icon>
                        <span
                          class="text-sm font-medium duration-200 lg:opacity-0 lg:sidebar-expanded:opacity-100 xl:opacity-100"
                          >{{ $t(item.name) }}</span
                        >
                      </div>
                      <!-- Icon -->
                      <div class="ml-2 flex shrink-0">
                        <svg
                          class="ml-1 size-3 shrink-0 fill-current text-slate-400"
                          :class="parentLink.expanded && 'rotate-180'"
                          viewBox="0 0 12 12"
                        >
                          <path d="M5.9 11.4L.5 6l1.4-1.4 4 4 4-4L11.3 6z" />
                        </svg>
                      </div>
                    </div>
                  </a>

                  <div class="lg:hidden lg:sidebar-expanded:block xl:block">
                    <template
                      v-for="child in item.children"
                      :key="`${item.type}_${item.name}_${child.name}`"
                    >
                      <ul class="mt-2 pl-9" :class="!parentLink.expanded && 'hidden'">
                        <router-link
                          v-if="child.access"
                          :to="child.url"
                          custom
                          v-slot="{ href, navigate, isExactActive }"
                        >
                          <li class="mb-1 last:mb-0">
                            <a
                              class="block truncate py-1 transition duration-150"
                              :class="
                                isExactActive
                                  ? 'text-indigo-500'
                                  : 'text-slate-400 hover:text-slate-200'
                              "
                              :href="href"
                              @click="navigate"
                            >
                              <span
                                class="text-sm font-medium duration-200 lg:opacity-0 lg:sidebar-expanded:opacity-100 xl:opacity-100"
                                >{{ $t(child.name) }}</span
                              >
                            </a>
                          </li>
                        </router-link>
                      </ul>
                    </template>
                  </div>
                </SidebarLinkGroup>
              </ul>
            </template>

            <template v-if="item.type === 'single'">
              <ul class="mt-2">
                <router-link
                  v-if="item.access"
                  :to="item.url"
                  custom
                  v-slot="{ href, navigate, isExactActive }"
                >
                  <li
                    class="mb-0.5 rounded-sm px-3 py-2 last:mb-0"
                    :class="isExactActive && 'bg-slate-900'"
                  >
                    <a
                      class="block truncate text-slate-200 transition duration-150"
                      :class="isExactActive ? 'hover:text-slate-200' : 'hover:text-white'"
                      :href="href"
                      @click="navigate"
                    >
                      <div class="flex items-center justify-between">
                        <div class="flex grow items-center">
                          <n-icon v-if="item.icon !== null" size="20" class="mr-3">
                            <component :is="item.icon"></component>
                          </n-icon>
                          <span
                            class="text-sm font-medium duration-200 lg:opacity-0 lg:sidebar-expanded:opacity-100 xl:opacity-100"
                            >{{ $t(item.name) }}</span
                          >
                        </div>
                      </div>
                    </a>
                  </li>
                </router-link>
              </ul>
            </template>
          </template>
        </div>
      </div>

      <!-- Expand / collapse button -->
      <div class="mt-auto hidden justify-end pt-3 lg:inline-flex xl:hidden">
        <div class="px-3 py-2">
          <button @click.prevent="sidebarExpanded = !sidebarExpanded">
            <span class="sr-only">Expand / collapse sidebar</span>
            <svg class="size-6 fill-current sidebar-expanded:rotate-180" viewBox="0 0 24 24">
              <path
                class="text-slate-400"
                d="M19.586 11l-5-5L16 4.586 23.414 12 16 19.414 14.586 18l5-5H7v-2z"
              />
              <path class="text-slate-600" d="M3 23H1V1h2z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";
import { NIcon } from "naive-ui";
import { LocationOutline, PeopleOutline, Menu } from "@vicons/ionicons5";
import { useI18n } from "vue-i18n";

import SidebarLinkGroup from "./SidebarLinkGroup.vue";
import StorageLogger from "@/modules/common/utils/storageLogger";

export default {
  name: "SidebarView",
  props: ["sidebarOpen"],
  components: {
    NIcon,
    LocationOutline,
    PeopleOutline,
    SidebarLinkGroup,
    Menu,
  },
  setup(props, { emit }) {
    const { t } = useI18n();
    const trigger = ref(null);
    const sidebar = ref(null);

    const storedSidebarExpanded = StorageLogger.getItem("sidebar-expanded");
    const sidebarExpanded = ref(
      storedSidebarExpanded === null ? false : storedSidebarExpanded === "true",
    );

    const currentRoute = useRouter().currentRoute.value;

    // close on click outside
    const clickHandler = ({ target }) => {
      if (!sidebar.value || !trigger.value) return;
      if (!props.sidebarOpen || sidebar.value.contains(target) || trigger.value.contains(target))
        return;
      emit("close-sidebar");
    };

    // close if the esc key is pressed
    const keyHandler = ({ keyCode }) => {
      if (!props.sidebarOpen || keyCode !== 27) return;
      emit("close-sidebar");
    };

    onMounted(() => {
      StorageLogger.setItem("sidebar-expanded", false);
      document.addEventListener("click", clickHandler);
      document.addEventListener("keydown", keyHandler);
    });

    onUnmounted(() => {
      document.removeEventListener("click", clickHandler);
      document.removeEventListener("keydown", keyHandler);
    });

    watch(sidebarExpanded, () => {
      StorageLogger.setItem("sidebar-expanded", String(sidebarExpanded.value));
      if (sidebarExpanded.value) {
        document.querySelector("body")?.classList.add("sidebar-expanded");
      } else {
        document.querySelector("body")?.classList.remove("sidebar-expanded");
      }
    });

    const data = [
      {
        type: "group",
        name: "Админ панель",
        routePartUriPath: "admin",
        icon: Menu,
        groupAccess: true,
        children: [
          {
            name: "Товары",
            url: "/admin/goods/",
            access: true,
          },
          {
            name: "Пользователи",
            url: "/admin/users/",
            access: true,
          },
          {
            name: "Заказы",
            url: "/admin/orders/",
            access: true,
          },
        ],
      },
    ];

    return {
      trigger,
      sidebar,
      sidebarExpanded,
      currentRoute,
      data,
      t,
    };
  },
};
</script>
