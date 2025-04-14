<template>
  <section class="flex h-full items-center p-16 dark:text-gray-100">
    <div class="container mx-auto my-8 flex flex-col items-center justify-center px-5">
      <div class="max-w-md text-center">
        <h2 class="mb-8 text-9xl font-extrabold dark:text-gray-600">
          <span class="sr-only">Error</span>404
        </h2>
        <p class="text-2xl font-semibold dark:text-gray-900">Sorry, we couldn't find this page.</p>
        <p class="mb-8 mt-4 dark:text-gray-400">
          But dont worry, you can find plenty of other things on our homepage.
        </p>
        <a
          rel="noopener noreferrer"
          href="/"
          class="rounded px-8 py-3 font-semibold dark:bg-violet-400 dark:text-gray-900"
          >Back to homepage</a
        >
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  setup() {
    return {};
  },
});
</script>

<style scoped></style>
