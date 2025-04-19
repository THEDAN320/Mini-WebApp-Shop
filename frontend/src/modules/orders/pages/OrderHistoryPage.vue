<template>
  <div class="order-history-page">
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
          <a href="/orders" class="header__nav-link active">МОИ ЗАКАЗЫ</a>
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="orders-container">
        <h1 class="orders-title">История заказов</h1>

        <!-- Loading State -->
        <div v-if="loading" class="orders-list">
          <div v-for="n in 3" :key="n" class="order-item is-loading">
            <div class="order-header-skeleton"></div>
            <div class="order-content-skeleton">
              <div class="skeleton-line"></div>
              <div class="skeleton-line"></div>
            </div>
          </div>
        </div>

        <!-- Orders List -->
        <div v-else-if="orders.length" class="orders-list">
          <div v-for="order in orders" :key="order.id" class="order-item">
            <div class="order-header">
              <div class="order-info">
                <h3 class="order-number">Заказ #{{ order.id }}</h3>
                <p class="order-date">
                  {{ formatDate(order.created_at) }}
                </p>
              </div>
              <div class="order-status">
                {{ order.is_paid ? "Оплачено" : "Ожидает оплаты" }}
              </div>
            </div>

            <div class="order-content">
              <div v-if="orderDetails[order.id]?.goods?.length" class="order-products">
                <!-- Order Info Panel -->
                <div class="order-info-panel">
                  <div class="order-info-row">
                    <span class="order-info-label">Статус заказа:</span>
                    <span class="order-info-value">
                      {{ order.is_paid ? "Оплачено" : "Ожидает оплаты" }}
                    </span>
                  </div>
                  <div class="order-info-row">
                    <span class="order-info-label">Дата создания:</span>
                    <span class="order-info-value">{{ formatDate(order.created_at) }}</span>
                  </div>
                  <div class="order-info-row" v-if="order.address">
                    <span class="order-info-label">Адрес доставки:</span>
                    <span class="order-info-value">{{ order.address }}</span>
                  </div>
                  <div class="order-info-row" v-if="order.phone">
                    <span class="order-info-label">Телефон:</span>
                    <span class="order-info-value">{{ order.phone }}</span>
                  </div>
                </div>

                <h3 class="products-section-title">Товары в заказе</h3>

                <div
                  v-for="item in orderDetails[order.id].goods"
                  :key="item.id"
                  class="order-product"
                >
                  <div class="product-image">
                    <img
                      src="https://images.icon-icons.com/1875/PNG/512/airpods_119984.png"
                      :alt="item.good?.name || 'Товар'"
                    />
                  </div>
                  <div class="product-details">
                    <h4 class="product-name">{{ item.good?.name || "Товар" }}</h4>
                    <p class="product-article" v-if="item.good?.article">
                      Артикул: {{ item.good.article }}
                    </p>
                    <div class="product-meta">
                      <p class="product-price">
                        {{ formatPrice(item.price) }} ₽ × {{ item.count }}
                      </p>
                      <p class="product-subtotal">
                        Итого: <strong>{{ formatPrice(item.price * item.count) }} ₽</strong>
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="order-footer">
                <div class="order-total">
                  <span>Итого:</span>
                  <span class="total-price">{{ order.price_with_sale }} ₽</span>
                </div>
                <button
                  v-if="!orderDetailsLoading[order.id] && !orderDetails[order.id]"
                  class="view-details-btn"
                  @click="loadOrderDetails(order.id)"
                >
                  Показать детали
                </button>
                <button
                  v-else-if="orderDetails[order.id]"
                  class="hide-details-btn"
                  @click="hideOrderDetails(order.id)"
                >
                  Скрыть детали
                </button>
                <button v-else class="view-details-btn loading" disabled>Загрузка...</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <n-empty description="У вас пока нет заказов" />
          <a href="/catalog" class="go-to-catalog-btn">Перейти в каталог</a>
        </div>

        <!-- Pagination -->
        <div v-if="orders.length && totalPages > 1" class="pagination">
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
import { ref, onMounted, computed, reactive } from "vue";
import { NEmpty, NPagination } from "naive-ui";
import { useStore } from "vuex";
import { dispatchNotification } from "@/modules/common/utils/notifications";

const store = useStore();
const loading = ref(true);
const currentPage = ref(1);
const pageSize = ref(10);
const totalPages = ref(1);
const totalItems = ref(0);

interface Good {
  id: number;
  name: string;
  article: string;
  description: string;
  price: number;
  url: string;
}

interface OrderGood {
  id: number;
  good_id: number;
  count: number;
  price: number;
  user_id: number;
  order_id: number;
  good?: Good;
}

interface Order {
  id: number;
  user_id: number;
  status: string;
  price_with_sale: number;
  address: string;
  phone: string;
  created_at: string;
  updated_at: string;
  is_paid: boolean;
  is_closed: boolean;
  goods?: OrderGood[];
}

interface OrderDetail {
  order: Order;
  goods: OrderGood[];
}

const orders = ref<Order[]>([]);
const orderDetails = reactive<Record<number, OrderDetail>>({});
const orderDetailsLoading = reactive<Record<number, boolean>>({});

// Fetch user orders
const fetchOrders = async () => {
  loading.value = true;
  try {
    // Hardcoded user_id = 1 for this example
    await store.dispatch("orders/FETCH_ALL_ORDERS", {
      search_data: {
        user_id: 1,
        is_closed: true,
      },
      pagi: {
        limit: pageSize.value,
        offset: (currentPage.value - 1) * pageSize.value,
      },
    });

    // Get data from store
    orders.value = store.getters["orders/GET_ALL_ORDERS"];
    totalItems.value = store.getters["orders/GET_TOTAL_ALL_ORDERS"];
    totalPages.value = Math.ceil(totalItems.value / pageSize.value);

    console.log("Fetched orders:", orders.value);
  } catch (error) {
    console.error("Error fetching orders:", error);
    dispatchNotification(
      "error",
      "Ошибка загрузки",
      "Не удалось загрузить историю заказов",
      true,
      4000,
    );
    orders.value = [];
    totalItems.value = 0;
    totalPages.value = 1;
  } finally {
    loading.value = false;
  }
};

// Load details for a specific order
const loadOrderDetails = async (orderId: number) => {
  if (orderDetailsLoading[orderId]) return;

  orderDetailsLoading[orderId] = true;

  try {
    const order = orders.value.find((o) => o.id === orderId);

    if (order && order.goods) {
      // Use the goods data that already exists in the order object
      orderDetails[orderId] = {
        order,
        goods: order.goods,
      };
    } else {
      // Fallback to the original implementation if goods are not included in the order
      await store.dispatch("orders/FETCH_DETAIL_GOOD", orderId);
      const orderDetail = store.getters["orders/GET_DETAIL_GOOD"];

      if (orderDetail) {
        // Check if the detailed order has goods
        if (orderDetail.goods) {
          orderDetails[orderId] = {
            order: orderDetail,
            goods: orderDetail.goods,
          };
        } else {
          // If no goods in the detailed order, fetch them separately
          await store.dispatch("orderGoods/FETCH_ALL_ORDERGOODS", {
            search_data: {
              order_id: orderId,
            },
          });

          const orderGoods = store.getters["orderGoods/GET_ALL_ORDERGOODS"];

          // For each order good, fetch the product details if not already included
          const orderGoodsWithDetails = [...orderGoods];
          for (const item of orderGoodsWithDetails) {
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

          // Store the full order details
          orderDetails[orderId] = {
            order: orderDetail,
            goods: orderGoodsWithDetails,
          };
        }
      }
    }
  } catch (error) {
    console.error(`Error loading details for order ${orderId}:`, error);
    dispatchNotification(
      "error",
      "Ошибка загрузки",
      `Не удалось загрузить детали заказа #${orderId}`,
      true,
      4000,
    );
  } finally {
    orderDetailsLoading[orderId] = false;
  }
};

// Hide order details
const hideOrderDetails = (orderId: number) => {
  delete orderDetails[orderId];
};

// Format price with thousands separator
const formatPrice = (price: number) => {
  return price.toLocaleString("ru-RU");
};

// Format date
const formatDate = (dateString: string) => {
  if (!dateString) return "Нет данных";

  const date = new Date(dateString);
  return new Intl.DateTimeFormat("ru-RU", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
};

// Get text representation of order status
const getStatusText = (status: string) => {
  switch (status?.toLowerCase()) {
    case "pending":
      return "В обработке";
    case "processing":
      return "Обрабатывается";
    case "shipped":
      return "Отправлен";
    case "delivered":
      return "Доставлен";
    case "cancelled":
      return "Отменен";
    case "closed":
      return "Завершен";
    default:
      return "Неизвестный статус";
  }
};

onMounted(() => {
  fetchOrders();
});
</script>

<style scoped>
@import "@/assets/css/styles.css";

.order-history-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #4a4238;
}

.main {
  flex: 1;
}

.orders-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.orders-title {
  color: #ffffff;
  font-size: 36px;
  font-weight: 600;
  text-align: center;
  margin-bottom: 40px;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 40px;
}

.order-item {
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.order-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.order-header {
  padding: 15px 20px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-info {
  display: flex;
  align-items: baseline;
  gap: 15px;
}

.order-number {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.order-date {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.order-status {
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.status-pending {
  background-color: #ffeeba;
  color: #856404;
}

.status-processing {
  background-color: #bee5eb;
  color: #0c5460;
}

.status-shipped {
  background-color: #c3e6cb;
  color: #155724;
}

.status-delivered {
  background-color: #d4edda;
  color: #155724;
}

.status-cancelled {
  background-color: #f8d7da;
  color: #721c24;
}

.status-closed {
  background-color: #d6d8d9;
  color: #1b1e21;
}

.status-unknown {
  background-color: #f8f9fa;
  color: #333;
}

.order-content {
  padding: 20px;
}

.order-products {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.order-product {
  display: flex;
  gap: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.product-image {
  flex: 0 0 60px;
  height: 60px;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.product-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.product-article {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-price {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

.order-total {
  font-size: 16px;
  font-weight: 500;
}

.total-price {
  font-size: 18px;
  font-weight: 600;
  color: #ff6b35;
  margin-left: 10px;
}

.view-details-btn,
.hide-details-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.view-details-btn {
  background: #ff6b35;
  color: white;
}

.view-details-btn:hover {
  background: #e85a2c;
}

.hide-details-btn {
  background: #5a5a5a;
  color: white;
}

.hide-details-btn:hover {
  background: #444444;
}

.view-details-btn.loading {
  opacity: 0.7;
  cursor: not-allowed;
}

.order-empty,
.order-loading {
  padding: 20px;
  text-align: center;
  color: #666;
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
.order-item.is-loading {
  pointer-events: none;
  height: 200px;
}

.order-header-skeleton {
  height: 58px;
  background: #eee;
  animation: pulse 1.5s infinite;
}

.order-content-skeleton {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-line {
  height: 16px;
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

@media (max-width: 768px) {
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .order-status {
    align-self: flex-start;
  }

  .order-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }

  .order-footer {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .view-details-btn,
  .hide-details-btn {
    width: 100%;
  }
}

@media (max-width: 640px) {
  .orders-container {
    padding: 20px;
  }

  .orders-title {
    font-size: 28px;
    margin-bottom: 24px;
  }

  .header__logo-text {
    font-size: 20px;
  }

  .header__nav {
    gap: 10px;
  }

  .header__nav-link {
    font-size: 14px;
  }
}

.order-info-panel {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  border: 1px solid #eee;
}

.order-info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.order-info-row:last-child {
  margin-bottom: 0;
}

.order-info-label {
  font-weight: 500;
  color: #666;
}

.order-info-value {
  font-weight: 500;
  color: #333;
}

.products-section-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 15px 0;
  color: #333;
}

.product-subtotal {
  font-size: 14px;
  color: #333;
  text-align: right;
}

.product-meta {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

@media (min-width: 640px) {
  .product-meta {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
