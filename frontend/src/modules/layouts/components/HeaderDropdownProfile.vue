<template>
  <div class="relative inline-flex">
    <button
      ref="trigger"
      class="group inline-flex items-center justify-center"
      aria-haspopup="true"
      @click.prevent="dropdownOpen = !dropdownOpen"
      :aria-expanded="dropdownOpen"
    >
      <!-- <img
        class="h-8 w-8 rounded-full"
        src="@/assets/images/user-avatar-32.png"
        width="32"
        height="32"
        alt="User"
      /> -->
      <div class="rounded-full bg-gray-200 p-1.5">
        {{ getFirstSymbolUser }}
      </div>

      <div class="flex items-center truncate">
        <span class="ml-2 truncate text-sm font-medium group-hover:text-gray-800">
          {{ getUserFio }}
        </span>
        <svg class="ml-1 h-3 w-3 shrink-0 fill-current text-gray-400" viewBox="0 0 12 12">
          <path d="M5.9 11.4L.5 6l1.4-1.4 4 4 4-4L11.3 6z" />
        </svg>
      </div>
    </button>

    <transition
      enter-active-class="transition ease-out duration-200 transform"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-out duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-show="dropdownOpen"
        class="absolute top-full z-10 mt-1 min-w-44 origin-top-right overflow-hidden rounded border border-gray-200 bg-white p-1.5 shadow-lg"
        :class="align === 'right' ? 'right-0' : 'left-0'"
      >
        <ul ref="dropdown" @focusin="dropdownOpen = true" @focusout="dropdownOpen = false">
          <li>
            <router-link
              class="flex items-center rounded px-1.5 py-1 text-sm font-medium text-gray-600 transition duration-200 ease-in-out hover:bg-gray-100 hover:text-gray-800"
              to="/user-profile"
              @click="dropdownOpen = false"
            >
              <n-icon size="16" style="margin-right: 6px">
                <PersonOutline />
              </n-icon>
              <span>Профиль</span>
            </router-link>
          </li>

          <li>
            <router-link
              class="flex items-center rounded px-1.5 py-1 text-sm font-medium text-gray-600 transition duration-200 ease-in-out hover:bg-gray-100 hover:text-gray-800"
              to="/"
              @click="getLogout"
            >
              <n-icon size="16" style="margin-right: 6px">
                <LogOutOutline />
              </n-icon>
              <span>Выйти</span>
            </router-link>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted, computed } from "vue";
import { useStore } from "vuex";
import { NIcon } from "naive-ui";
import { PersonOutline, LogOutOutline } from "@vicons/ionicons5";

export default defineComponent({
  name: "HeaderDropdownProfile",

  components: {
    NIcon,
    PersonOutline,
    LogOutOutline,
  },

  props: ["align"],
  data() {
    return {};
  },
  setup() {
    const store = useStore();

    const dropdownOpen: any = ref(false);
    const trigger: any = ref(null);
    const dropdown: any = ref(null);

    // close on click outside
    const clickHandler = ({ target }: { target: any }) => {
      if (
        !dropdownOpen.value ||
        dropdown.value?.contains(target) ||
        trigger.value?.contains(target)
      )
        return;
      dropdownOpen.value = false;
    };

    // close if the esc key is pressed
    const keyHandler = ({ keyCode }: { keyCode: number }) => {
      if (!dropdownOpen.value || keyCode !== 27) return;
      dropdownOpen.value = false;
    };

    onMounted(() => {
      document.addEventListener("click", clickHandler);
      document.addEventListener("keydown", keyHandler);
    });

    onUnmounted(() => {
      document.removeEventListener("click", clickHandler);
      document.removeEventListener("keydown", keyHandler);
    });

    const getLogout = () => {
      store.dispatch("auth/SIGN_OUT");
    };

    const getUserData = computed(() => store.getters["users/GET_USER_ME_WITH_PERMISSIONS"]);
    const getUserFio = computed(() => {
      if (getUserData.value) {
        return `${getUserData.value.last_name} ${getUserData.value.name} ${getUserData.value.middle_name}`;
      }
      return "";
    });
    const getFirstSymbolUser = computed(() => {
      if (
        getUserData.value &&
        getUserData.value.last_name !== null &&
        getUserData.value.name !== null
      ) {
        return `${getUserData.value.last_name[0]}${getUserData.value.name[0]}`.toUpperCase();
      }
      return "NN";
    });

    return {
      dropdownOpen,
      trigger,
      dropdown,
      getLogout,
      getUserFio,
      getFirstSymbolUser,
    };
  },
});
</script>
