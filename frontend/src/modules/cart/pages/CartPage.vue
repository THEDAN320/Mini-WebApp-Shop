<template>
  <div class="cart-page">
    <header class="header">
      <div class="container">
        <div class="header__logo">
          <img src="@/assets/images/logo.png" alt="LISSE-SHOP Logo" class="header__logo-image" />
          <span class="header__logo-text">LISSE-SHOP</span>
        </div>
        <nav class="header__nav">
          <a href="/" class="header__nav-link">О НАС</a>
          <a href="/catalog" class="header__nav-link">КАТАЛОГ</a>
          <a href="/cart" class="header__nav-link active">КОРЗИНА</a>
          <a href="/orders" class="header__nav-link">МОИ ЗАКАЗЫ</a>
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="cart-container">
        <h1 class="cart-title">Корзина</h1>

        <!-- Loading State -->
        <div v-if="loading" class="cart-items">
          <div v-for="n in 3" :key="n" class="cart-item is-loading">
            <div class="cart-item-image-skeleton"></div>
            <div class="cart-item-content-skeleton">
              <div class="skeleton-line"></div>
              <div class="skeleton-line"></div>
            </div>
          </div>
        </div>

        <!-- Cart Items -->
        <div v-else-if="cartItems?.length" class="cart-items">
          <div v-for="item in cartItems" :key="item.id" class="cart-item">
            <div class="cart-item-image">
              <img
                src="https://images.icon-icons.com/1875/PNG/512/airpods_119984.png"
                :alt="item.good?.name || 'Товар'"
              />
            </div>
            <div class="cart-item-content">
              <h3 class="cart-item-name">{{ item.good?.name || "Товар" }}</h3>
              <p class="cart-item-article" v-if="item.good?.article">
                Артикул: {{ item.good.article }}
              </p>
              <div class="cart-item-quantity">
                <button
                  class="quantity-btn"
                  @click="updateQuantity(item, item.count - 1)"
                  :disabled="item.count <= 1"
                >
                  -
                </button>
                <span class="quantity-value">{{ item.count }}</span>
                <button class="quantity-btn" @click="updateQuantity(item, item.count + 1)">
                  +
                </button>
              </div>
              <div class="cart-item-footer">
                <p class="cart-item-price">{{ formatPrice(item.price * item.count) }} ₽</p>
                <button class="remove-from-cart" @click="removeFromCart(item.id)">Удалить</button>
              </div>
            </div>
          </div>

          <!-- Cart Summary -->
          <div class="cart-summary">
            <div class="cart-summary-row">
              <span>Количество товаров:</span>
              <span>{{ totalItems }}</span>
            </div>
            <div class="cart-summary-row">
              <span>Итого:</span>
              <span class="cart-total-price">{{ formatPrice(totalPrice) }} ₽</span>
            </div>
            <button class="checkout-btn" @click="checkout">Оформить заказ</button>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <n-empty description="Корзина пуста" />
          <a href="/catalog" class="go-to-catalog-btn">Перейти в каталог</a>
        </div>
      </div>
    </main>

    <footer class="footer">
      <div class="container">
        <p class="footer__copyright">Все права защищены</p>
        <a href="https://t.me/lisse_shop" class="footer__telegram">Наш Telegram</a>
      </div>
    </footer>

    <!-- Checkout Modal -->
    <n-modal
      v-model:show="showCheckoutModal"
      preset="dialog"
      title="Оформление заказа"
      positive-text="Оформить"
      negative-text="Отмена"
      @positive-click="confirmCheckout"
      @negative-click="cancelCheckout"
    >
      <template #header>
        <div class="text-lg font-bold text-gray-800">Оформление заказа</div>
      </template>
      <div class="p-2">
        <p class="mb-4">Для оплаты заказа, пожалуйста, свяжитесь с администратором:</p>
        <ul class="mb-4 ml-4 list-disc">
          <li class="mb-2">
            Телефон: <a href="tel:+79991234567" class="text-blue-500">+7 (999) 123-45-67</a>
          </li>
          <li class="mb-2">
            Email:
            <a href="mailto:admin@lisse-shop.com" class="text-blue-500">admin@lisse-shop.com</a>
          </li>
          <li>
            Telegram:
            <a href="https://t.me/lisse_shop" target="_blank" class="text-blue-500">@lisse_shop</a>
          </li>
        </ul>
        <p class="font-semibold">Сумма заказа: {{ formatPrice(totalPrice) }} ₽</p>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { NEmpty, NModal } from "naive-ui";
import { useStore } from "vuex";
import { dispatchNotification } from "@/modules/common/utils/notifications";

const store = useStore();
const loading = ref(true);

interface Good {
  id: number;
  name: string;
  article: string;
  description: string;
  price: number;
  url: string;
  count: number;
  type: string;
}

interface CartItem {
  id: number;
  good_id: number;
  count: number;
  price: number;
  user_id: number;
  good?: Good;
}

const cartItems = ref<CartItem[]>([]);

// Fetch cart items from the orderGoods store
const fetchCartItems = async () => {
  loading.value = true;
  try {
    // Use user_id: 1 as a filter for this example
    const order = await store.dispatch("orders/CREATE_ORDERS", {
      user_id: 1,
    });
    await store.dispatch("orderGoods/FETCH_ALL_ORDERGOODS", {
      search_data: {
        user_id: 1,
        order_id: order.id,
      },
    });

    // Get items from store
    const items = store.getters["orderGoods/GET_ALL_ORDERGOODS"];
    cartItems.value = items;

    // Fetch product details for each cart item if not already included
    for (const item of cartItems.value) {
      if (!item.good && item.good_id) {
        try {
          await store.dispatch("goods/FETCH_DETAIL_GOOD", item.good_id);
          const good = store.getters["goods/GET_DETAIL_GOOD"];
          if (good) {
            item.good = good;
          }
        } catch (error) {
          console.error(`Error fetching details for product ${item.good_id}:`, error);
        }
      }
    }

    console.log("Fetched cart items:", cartItems.value);
  } catch (error) {
    console.error("Error fetching cart items:", error);
    cartItems.value = [];
  } finally {
    loading.value = false;
  }
};

// Update the quantity of an item in the cart
const updateQuantity = async (item: CartItem, newCount: number) => {
  if (newCount < 1) return;

  try {
    const payload = {
      id: item.id,
      count: newCount,
    };

    const result = await store.dispatch("orderGoods/UPDATE_ORDERGOODS", payload);
    if (result) {
      // Update the local item
      item.count = newCount;
      dispatchNotification(
        "success",
        "Количество обновлено",
        `Количество товара "${item.good?.name || "товар"}" изменено на ${newCount}`,
        true,
        3000,
      );
    }
  } catch (error) {
    console.error("Error updating cart item quantity:", error);
    dispatchNotification(
      "error",
      "Ошибка обновления",
      "Не удалось обновить количество товара",
      true,
      4000,
    );
  }
};

// Remove an item from the cart
const removeFromCart = async (itemId: number) => {
  try {
    const itemToRemove = cartItems.value.find((item) => item.id === itemId);
    const itemName = itemToRemove?.good?.name || "товар";

    await store.dispatch("orderGoods/DELETE_ORDERGOODS", itemId);
    // Remove item from local array
    cartItems.value = cartItems.value.filter((item) => item.id !== itemId);

    dispatchNotification(
      "info",
      "Товар удален",
      `Товар "${itemName}" удален из корзины`,
      true,
      3000,
    );
  } catch (error) {
    console.error("Error removing item from cart:", error);
    dispatchNotification(
      "error",
      "Ошибка удаления",
      "Не удалось удалить товар из корзины",
      true,
      4000,
    );
  }
};

// Calculate the total number of items in the cart
const totalItems = computed(() => {
  return cartItems.value.reduce((total, item) => total + item.count, 0);
});

// Calculate the total price of all items in the cart
const totalPrice = computed(() => {
  return cartItems.value.reduce((total, item) => total + item.price * item.count, 0);
});

// Format price with thousands separator
const formatPrice = (price: number) => {
  return price.toLocaleString("ru-RU");
};

// Modal state
const showCheckoutModal = ref(false);

// Opens the checkout modal
const openCheckoutModal = () => {
  if (cartItems.value.length === 0) {
    dispatchNotification(
      "warning",
      "Корзина пуста",
      "Добавьте товары в корзину, прежде чем оформить заказ.",
      true,
      4000,
    );
    return;
  }
  showCheckoutModal.value = true;
};

// Cancels the checkout process
const cancelCheckout = () => {
  showCheckoutModal.value = false;
};

// Confirms the checkout and processes the order
const confirmCheckout = async () => {
  try {
    const user_id = 1;
    await store.dispatch("orders/CLOSE_ORDERS", user_id);
    cartItems.value = [];
    showCheckoutModal.value = false;
    dispatchNotification(
      "success",
      "Заказ оформлен",
      "Ваш заказ успешно оформлен! Благодарим за покупку!",
      true,
      5000,
    );
  } catch (error) {
    console.error("Error during checkout:", error);
    dispatchNotification(
      "error",
      "Ошибка оформления",
      "Произошла ошибка при оформлении заказа. Пожалуйста, попробуйте снова.",
      true,
      5000,
    );
  }
};

// Replace the previous checkout function with the modal opening function
const checkout = () => {
  openCheckoutModal();
};

onMounted(() => {
  fetchCartItems();
});
</script>

<style scoped>
@import "@/assets/css/styles.css";

.cart-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #4a4238;
}

.main {
  flex: 1;
}

.cart-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.cart-title {
  color: #ffffff;
  font-size: 36px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 40px;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}

.cart-item {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  padding: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.cart-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.cart-item-image {
  flex: 0 0 100px;
  height: 100px;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
  margin-right: 20px;
}

.cart-item-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.cart-item-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cart-item-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.cart-item-article {
  font-size: 13px;
  color: #666;
  margin: 0;
}

.cart-item-quantity {
  display: flex;
  align-items: center;
  gap: 10px;
}

.quantity-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #f0f0f0;
  border: none;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.quantity-btn:hover:not(:disabled) {
  background: #e0e0e0;
}

.quantity-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-value {
  font-size: 16px;
  font-weight: 500;
}

.cart-item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.cart-item-price {
  font-size: 20px;
  font-weight: 600;
  color: #ff6b35;
  margin: 0;
}

.remove-from-cart {
  padding: 8px 16px;
  background: #ff6b35;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.remove-from-cart:hover {
  background: #e85a2c;
}

.cart-summary {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.cart-summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 16px;
}

.cart-total-price {
  font-size: 24px;
  font-weight: 600;
  color: #ff6b35;
}

.checkout-btn {
  width: 100%;
  padding: 12px;
  background: #ff6b35;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 15px;
}

.checkout-btn:hover {
  background: #e85a2c;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.go-to-catalog-btn {
  padding: 12px 24px;
  background: #ff6b35;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  text-decoration: none;
}

.go-to-catalog-btn:hover {
  background: #e85a2c;
}

/* Loading State */
.cart-item.is-loading {
  pointer-events: none;
  height: 140px;
}

.cart-item-image-skeleton {
  flex: 0 0 100px;
  height: 100px;
  background: #eee;
  border-radius: 8px;
  margin-right: 20px;
  animation: pulse 1.5s infinite;
}

.cart-item-content-skeleton {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-line {
  height: 12px;
  background: #eee;
  margin-bottom: 8px;
  animation: pulse 1.5s infinite;
  border-radius: 4px;
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

.header__nav-link.active {
  color: #ff6b35;
  border-bottom: 2px solid #ff6b35;
  padding-bottom: 3px;
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

@media (max-width: 768px) {
  .cart-item {
    flex-direction: column;
  }

  .cart-item-image {
    width: 100%;
    margin-right: 0;
    margin-bottom: 15px;
  }

  .cart-item-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .remove-from-cart {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .cart-container {
    padding: 20px;
  }

  .cart-title {
    font-size: 28px;
    margin-bottom: 24px;
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
