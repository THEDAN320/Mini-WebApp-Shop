import { createStore } from "vuex";
import notifications from "@/modules/notifications/store";
import main from "@/modules/main/store";
import goods from "@/modules/admin/store";

const store = createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    notifications,
    main,
    goods,
  },
});

export default store;
