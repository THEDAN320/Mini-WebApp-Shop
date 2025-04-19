<template>
  <div
    class="product-card overflow-hidden rounded-xl bg-white shadow-lg transition-transform hover:scale-[1.02]"
  >
    <div class="relative aspect-square overflow-hidden">
      <img
        :src="product.url || '/images/no-image.png'"
        :alt="product.name"
        class="size-full object-cover"
      />
    </div>
    <div class="space-y-2 p-4">
      <h3 class="line-clamp-2 text-lg font-semibold text-gray-800">{{ product.name }}</h3>
      <p class="line-clamp-2 text-sm text-gray-600">{{ product.description }}</p>
      <div class="mt-4 flex items-center justify-between">
        <span class="text-xl font-bold text-orange-500">{{ product.price }} ₽</span>
        <n-button
          type="primary"
          class="bg-orange-500 hover:bg-orange-600"
          @click="addToCart(product)"
        >
          В корзину
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { NButton } from "naive-ui";
import { useStore } from "vuex";
import { defineProps } from "vue";

const store = useStore();

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  url: string;
}

const props = defineProps<{
  product: Product;
}>();

const addToCart = (product: Product) => {
  // TODO: Implement add to cart functionality
  console.log("Adding to cart:", product);
};
</script>

<style scoped>
.product-card {
  transition: all 0.3s ease;
}

.product-card:hover {
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}
</style>
