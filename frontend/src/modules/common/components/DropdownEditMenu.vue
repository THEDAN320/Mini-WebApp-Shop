<template>
  <div class="relative inline-flex">
    <button
      ref="trigger"
      class="flex h-8 w-8 items-center justify-center rounded-full text-gray-400 hover:text-gray-500"
      :class="{ 'bg-gray-200 text-gray-500': dropdownOpen }"
      aria-haspopup="true"
      @click.stop="toggleDropdownOpen"
      :aria-expanded="dropdownOpen"
    >
      <span class="sr-only">Menu</span>
      <n-icon size="20">
        <EllipsisHorizontal />
      </n-icon>
    </button>
    <div
      v-if="dropdownOpen"
      class="absolute top-full z-10 mt-1 min-w-36 origin-top-right overflow-hidden rounded bg-white p-1.5 shadow-lg"
      :class="align === 'right' ? 'right-0' : 'left-0'"
    >
      <ul ref="dropdown" @focusin="dropdownOpen = true" @focusout="dropdownOpen = false">
        <slot />
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted, defineComponent } from "vue";
import { NIcon } from "naive-ui";
import { EllipsisHorizontal } from "@vicons/ionicons5";

export default defineComponent({
  components: {
    NIcon,
    EllipsisHorizontal,
  },
  name: "DropdownEditMenu",
  props: ["align"],
  setup() {
    const dropdownOpen = ref(false);
    const trigger = ref();
    const dropdown = ref();

    const toggleDropdownOpen = () => {
      dropdownOpen.value = !dropdownOpen.value;
    };

    // close on click outside
    const clickHandler = ({ target }: { target: any }) => {
      if (!dropdownOpen.value || dropdown.value.contains(target) || trigger.value.contains(target))
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

    return {
      dropdownOpen,
      toggleDropdownOpen,
      trigger,
      dropdown,
    };
  },
});
</script>
