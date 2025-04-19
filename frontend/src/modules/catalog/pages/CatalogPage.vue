<template>
  <div class="catalog-page">
    <header class="header">
      <div class="container">
        <div class="header__logo">
          <img src="@/assets/images/logo.png" alt="LISSE-SHOP Logo" class="header__logo-image" />
          <span class="header__logo-text">LISSE-SHOP</span>
        </div>
        <nav class="header__nav">
          <a href="/" class="header__nav-link">О НАС</a>
          <a href="/catalog" class="header__nav-link">КАТАЛОГ</a>
          <a href="/cart" class="header__nav-link">КОРЗИНА</a>
          <a href="/orders" class="header__nav-link">МОИ ЗАКАЗЫ</a>
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="catalog-container">
        <h1 class="catalog-title">Каталог</h1>

        <!-- Loading State -->
        <div v-if="loading" class="products-grid">
          <div v-for="n in 6" :key="n" class="product-card is-loading">
            <div class="product-image-skeleton"></div>
            <div class="product-content-skeleton">
              <div class="skeleton-line"></div>
              <div class="skeleton-line"></div>
            </div>
          </div>
        </div>

        <!-- Products Grid -->
        <div v-else-if="products?.length" class="products-grid">
          <div v-for="product in products" :key="product.id" class="product-card">
            <div class="product-image" v-if="product.url">
              <img :src="product.url" :alt="product.name" />
            </div>
            <div class="product-image" v-else>
              <img
                src="https://images.icon-icons.com/1875/PNG/512/airpods_119984.png"
                :alt="product.name"
              />
            </div>

            <div class="product-content">
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-article">Артикул: {{ product.article }}</p>
              <p class="product-description">{{ product.description }}</p>
              <div class="product-footer">
                <p class="product-price">{{ product.price }} ₽</p>
                <button class="add-to-cart" @click="addToCart(product)">В корзину</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <n-empty description="Товары не найдены" />
        </div>

        <!-- Pagination -->
        <div v-if="products?.length" class="pagination">
          <n-pagination v-model:page="currentPage" :page-count="totalPages" :page-size="pageSize" />
        </div>
      </div>
    </main>

    <footer class="footer">
      <div class="container">
        <p class="footer__copyright">Все права защищены</p>
        <a href="https://t.me/lisse_shop" class="footer__telegram">Наш Telegram</a>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { NPagination, NEmpty } from "naive-ui";
import { useStore } from "vuex";

const store = useStore();
const loading = ref(true);
const currentPage = ref(1);
const pageSize = ref(10);
const totalPages = ref(1);
const totalItems = ref(0);

interface Product {
  id: number;
  name: string;
  article: string;
  description: string;
  price: number;
  url: string;
  count: number;
  type: string;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
}

const products = ref<Product[]>([]);

const fetchProducts = async () => {
  loading.value = true;
  try {
    await store.dispatch("goods/FETCH_ALL_GOODS", {
      pagi: {
        limit: pageSize.value,
        offset: (currentPage.value - 1) * pageSize.value,
      },
    });

    // Get data from store after dispatch
    products.value = store.getters["goods/GET_ALL_GOODS"];
    totalItems.value = store.getters["goods/GET_TOTAL_ALL_GOODS"];
    totalPages.value = Math.ceil(totalItems.value / pageSize.value);
    console.log("Fetched products:", products.value);
  } catch (error) {
    console.error("Error fetching products:", error);
    products.value = [];
    totalItems.value = 0;
    totalPages.value = 1;
  } finally {
    loading.value = false;
  }
};

const addToCart = async (product: Product) => {
  try {
    const payload = {
      good_id: product.id,
      count: 1, // Default count when adding to cart
      user_id: 1,
    };
    // Dispatch action to add to cart
    const result = await store.dispatch("orderGoods/CREATE_ORDERGOODS", payload);
    if (result) {
      // You could add notification here if needed
      console.log("Product added to cart successfully:", product.name);
    }
  } catch (error) {
    console.error("Error adding product to cart:", error);
  }
};

watch(currentPage, () => {
  fetchProducts();
});

onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
@import "@/assets/css/styles.css";

.catalog-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #4a4238;
}

.main {
  flex: 1;
}

.catalog-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.catalog-title {
  color: #ffffff;
  font-size: 36px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 40px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.product-card {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.product-image {
  position: relative;
  padding-top: 100%;
  background: #f5f5f5;
  border-bottom: 1px solid #eee;
}

.product-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 16px;
}

.product-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
  height: 2.8em;
}

.product-article {
  font-size: 13px;
  color: #666;
  margin: 0;
}

.product-description {
  font-size: 14px;
  color: #666;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
  flex-grow: 1;
}

.product-footer {
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.product-price {
  font-size: 20px;
  font-weight: 600;
  color: #ff6b35;
  margin: 0 0 12px 0;
}

.add-to-cart {
  width: 100%;
  padding: 10px;
  background: #ff6b35;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.add-to-cart:hover {
  background: #e85a2c;
}

/* Loading State */
.product-card.is-loading {
  pointer-events: none;
}

.product-image-skeleton {
  width: 100%;
  padding-top: 100%;
  background: #eee;
  animation: pulse 1.5s infinite;
}

.product-content-skeleton {
  padding: 16px;
}

.skeleton-line {
  height: 12px;
  background: #eee;
  margin-bottom: 8px;
  animation: pulse 1.5s infinite;
}

.skeleton-line:last-child {
  width: 60%;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #ffffff;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header {
  background-color: #4a4238;
  padding: 20px 0;
  border-bottom: 1px solid rgba(230, 213, 184, 0.1);
}

.header__logo {
  display: flex;
  align-items: center;
}

.header__logo-image {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.header__logo-text {
  color: #ff6b35;
  font-size: 24px;
  font-weight: bold;
}

.header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header__nav {
  display: flex;
  gap: 20px;
}

.header__nav-link {
  color: #e6d5b8;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s ease;
}

.header__nav-link:hover {
  color: #ff6b35;
}

.footer {
  background-color: #4a4238;
  padding: 20px 0;
  color: #e6d5b8;
  border-top: 1px solid rgba(230, 213, 184, 0.1);
}

.footer .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer__copyright {
  font-size: 16px;
  margin: 0;
}

.footer__telegram {
  color: #e6d5b8;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s ease;
}

.footer__telegram:hover {
  color: #ff6b35;
}

@media (max-width: 640px) {
  .catalog-container {
    padding: 20px;
  }

  .catalog-title {
    font-size: 28px;
    margin-bottom: 24px;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }

  .product-content {
    padding: 12px;
  }

  .product-name {
    font-size: 14px;
  }

  .product-price {
    font-size: 18px;
  }

  .header__logo-text {
    font-size: 20px;
  }

  .header__nav {
    gap: 15px;
  }

  .header__nav-link {
    font-size: 14px;
  }
}
</style>
