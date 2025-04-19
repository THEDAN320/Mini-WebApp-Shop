import { createStore } from "vuex";
import notifications from "@/modules/notifications/store";
import main from "@/modules/main/store";
import goods from "@/modules/admin/store";
import users from "@/modules/admin/store/users";
import orders from "@/modules/admin/store/orders";
import orderGoods from "@/modules/admin/store/order_good";

const store = createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    notifications,
    main,
    goods,
    users,
    orders,
    orderGoods,
  },
});

export default store;
