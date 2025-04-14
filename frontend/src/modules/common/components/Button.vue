<template>
  <button
    class="h-fill 0 relative flex items-center justify-center rounded transition duration-300 ease-in-out"
    :disabled="disabled"
    :class="[
      {
        'cursor-not-allowed': disabled,
        'opacity-40': disabled,
        'opacity-90': !disabled,
        'hover:opacity-100': !disabled,
      },
      typeData,
    ]"
    :style="{ padding: buttonSizeStyle }"
  >
    <slot name="left-content"></slot>

    <i v-if="icon" :style="iconSizeStyle">
      <component :is="icon" />
    </i>

    <span v-if="name !== ''" class="px-1">{{ name }}</span>

    <sup
      v-if="badge !== null && badge !== 0 && badge !== ''"
      class="absolute right-[-4px] top-[-6px] flex h-[18px] min-w-[18px] cursor-default items-center justify-center rounded-lg bg-red-500 px-1 leading-6 text-white"
    >
      <span>{{ badge }}</span>
    </sup>

    <slot name="right-content"></slot>
  </button>
</template>

<script lang="ts">
import { defineComponent, computed, PropType } from "vue";

type TypePropName = "default" | "default_light" | "info" | "success" | "warning" | "error";

export default defineComponent({
  name: "ButtonView",

  props: {
    icon: {
      type: Object,
      default: () => null,
    },
    name: {
      type: String,
      default: () => "",
    },
    size: {
      type: String,
      default: () => "medium",
    },
    disabled: {
      type: Boolean,
      default: () => false,
    },
    type: {
      type: String as PropType<TypePropName>,
      default: () => "default",
    },
    badge: {
      type: null as unknown as PropType<number | string | null>,
      default: () => null,
    },
  },

  setup(props) {
    const iconSizeStyle = computed(() => {
      if (props.size === "small") {
        return "height:18px;width:18px";
      } else if (props.size === "large") {
        return "height:26px;width:26px";
      }
      return "height:20px;width:20px";
    });

    const buttonSizeStyle = computed(() => {
      if (props.size === "small") {
        return "4px";
      } else if (props.size === "large") {
        return "8px";
      }
      return "6px";
    });

    const typeData = computed(() => {
      if (props.type === "default") {
        return "bg-indigo-500 text-white";
      } else if (props.type === "default_light") {
        return "bg-indigo-100 hover:bg-indigo-500 hover:text-white";
      } else if (props.type === "info") {
        return "bg-blue-500 text-white";
      } else if (props.type === "success") {
        return "bg-green-600 text-white";
      } else if (props.type === "warning") {
        return "bg-orange-500 text-white";
      } else if (props.type === "error") {
        return "bg-red-500 text-white";
      }
      return "";
    });

    return {
      buttonSizeStyle,
      iconSizeStyle,
      typeData,
    };
  },
});
</script>

<style scoped></style>
