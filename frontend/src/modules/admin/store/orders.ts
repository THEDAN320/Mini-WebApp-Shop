import {
  getAllOrders,
  createOrder,
  updateOrder,
  deleteOrder,
  getOrderById,
} from "@/modules/admin/api/orders";

export default {
  namespaced: true,
  state: {
    DATA_ORDERS: [],
    TOTAL_ORDERS: 0,
    DETAIL_GOOD: null,
  },

  getters: {
    GET_ALL_ORDERS: (state: any) => {
      return state.DATA_ORDERS;
    },
    GET_TOTAL_ALL_ORDERS: (state: any) => {
      return state.TOTAL_ORDERS;
    },
    GET_DETAIL_GOOD: (state: any) => {
      return state.DETAIL_GOOD;
    },
  },

  mutations: {
    SET_ALL_ORDERS(state: any, data: any) {
      state.DATA_ORDERS = data;
    },
    SET_TOTAL_ALL_ORDERS(state: any, data: any) {
      state.TOTAL_ORDERS = data;
    },
    UPDATED_OBJ_FROM_ORDERS(state: any, data: any) {
      state.DATA_ORDERS = state.DATA_ORDERS.map((item: any) => {
        return item.id === data.id ? { ...item, ...data } : item;
      });
    },
    DELETE_OBJ_FROM_ORDERS(state: any, id: number) {
      state.DATA_ORDERS = state.DATA_ORDERS.filter((item: any) => {
        return item.id !== id;
      });
      state.TOTAL_ORDERS = state.TOTAL_ORDERS - 1;
    },
    SET_DETAIL_GOOD(state: any, data: any) {
      state.DETAIL_GOOD = data;
    },
  },

  actions: {
    async FETCH_ALL_ORDERS(context: any, payload: any) {
      try {
        const res = await getAllOrders(payload);
        if (res.status === 200) {
          context.commit("SET_TOTAL_ALL_ORDERS", res.data.total);
          context.commit("SET_ALL_ORDERS", res.data.items);
        }
      } catch (error: any) {
        console.log(`Error FETCH_ORDERS => ${error}`);
        console.log(error.response);
      }
    },

    async CREATE_ORDERS(context: any, payload: any) {
      try {
        const res = await createOrder(payload);
        if (res.status === 201) {
          await context.dispatch("FETCH_ORDERS");
          return res.data;
        }
      } catch (error: any) {
        console.log(`Error CREATE_ORDERS => ${error}`);
        console.log(error.response);
      }
    },

    async UPDATE_ORDERS(context: any, payload: any) {
      try {
        const { id, ...data } = payload;
        const res = await updateOrder(id, data);
        if (res.status === 200) {
          context.commit("UPDATED_OBJ_FROM_ORDERS", res.data);
          return res.data;
        }
      } catch (error: any) {
        console.log(`Error UPDATE_ORDERS => ${error}`);
        console.log(error.response);
      }
    },

    async DELETE_ORDERS(context: any, id: number) {
      try {
        const res = await deleteOrder(id);
        if (res.status === 204) {
          context.commit("DELETE_OBJ_FROM_ORDERS", id);
        }
      } catch (error: any) {
        console.log(`Error DELETE_ORDERS => ${error}`);
        console.log(error.response);
      }
    },

    async FETCH_DETAIL_GOOD(context: any, id: number) {
      try {
        const res = await getOrderById(id);
        context.commit("SET_DETAIL_GOOD", res.data);
      } catch (error: any) {
        console.log(`Error FETCH_DETAIL_GOOD => ${error}`);
        console.log(error.response);
      }
    },
  },
};
