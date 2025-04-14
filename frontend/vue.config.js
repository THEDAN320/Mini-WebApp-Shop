const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  css: {
    loaderOptions: {
      scss: {
        additionalData: `
          @import "@/assets/scss/tailwind.scss";
          @import "@/assets/scss/dashboard/style.scss";
          @import "@/assets/scss/vueform-multiselect.scss";
          @import "@/assets/scss/main.scss";
        `,
      },
    },
  },
});
