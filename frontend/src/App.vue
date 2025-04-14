<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <router-view />
  </n-config-provider>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useRoute } from "vue-router";
import { NConfigProvider } from "naive-ui";
import { GlobalThemeOverrides } from "naive-ui";

const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: "#6366F1",
    primaryColorHover: "#4F46E5",
  },
};

export default defineComponent({
  components: {
    NConfigProvider,
  },

  setup() {
    const route = useRoute();
    const layout = computed(() => {
      return (route.meta.layout || "empty") + "-layout";
    });

    return {
      themeOverrides,
      layout,
    };
  },
});
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.disabled-overlay {
  pointer-events: none;
  opacity: 0.5;
}
</style>
