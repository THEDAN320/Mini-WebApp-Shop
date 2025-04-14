<template>
  <nav class="flex" aria-label="Breadcrumb">
    <ol class="inline-flex items-center space-x-0.5 md:space-x-0.5">
      <li v-for="(crumb, index) in breadcrumbs" :key="index" class="inline-flex items-center">
        <span v-if="index !== 0" class="mx-0.5 text-gray-800">/</span>
        <a
          v-if="isRouteValid(crumbsPath(index))"
          :href="getPath(crumbsPath(index))"
          class="text-base font-medium text-gray-700 hover:text-blue-600 md:ml-0.5"
          aria-current="page"
        >
          {{ isNaN(Number(crumb)) ? $t(`breadcrumbs.${crumb}`) : crumb }}
        </a>
        <span v-else class="text-base font-medium text-gray-500 md:ml-0.5">
          {{ isNaN(Number(crumb)) ? $t(`breadcrumbs.${crumb}`) : crumb }}
        </span>
      </li>
    </ol>
  </nav>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useRoute, useRouter } from "vue-router";

export default defineComponent({
  setup() {
    const route = useRoute();
    const router = useRouter();

    const breadcrumbs = computed(() => {
      const crumbs = route.path.split("/").filter((crumb) => crumb);
      return crumbs;
    });

    const crumbsPath = (index: number) => {
      const path = "/" + breadcrumbs.value.slice(0, index + 1).join("/") + "/";
      return path;
    };

    const normalizePath = (path: string): string => {
      return path.replace(/\/\d+\/|\/:[a-zA-Z]+\/?/g, "/:placeholder/");
    };

    const arePathsEqual = (path1: string, path2: string): boolean => {
      return normalizePath(path1) === normalizePath(path2);
    };

    const isRouteValid = (currentPath: string): boolean => {
      const checkPaths = (routes: any, parentPath = ""): boolean => {
        for (const route of routes) {
          const fullPath = parentPath + route.path;
          if (route.component && arePathsEqual(fullPath, currentPath)) {
            return true;
          }
          if (route.children && checkPaths(route.children, fullPath)) {
            return true;
          }
        }
        return false;
      };

      return checkPaths(router.options.routes);
    };

    const getPath = (path: string) => {
      const resolvedPath = router.resolve(path).href;
      return resolvedPath;
    };

    return {
      breadcrumbs,
      crumbsPath,
      isRouteValid,
      getPath,
    };
  },
});
</script>

<style scoped></style>
