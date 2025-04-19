import {
  getAllOrderGoods,
  createOrderGoods,
  updateOrderGoods,
  deleteOrderGoods,
  getOrderGoodsById,
} from "@/modules/admin/api/orderGoods";

export default {
  namespaced: true,
  state: {
    DATA_ORDERGOODS: [],
    TOTAL_ORDERGOODS: 0,
    DETAIL_GOOD: null,
  },

  getters: {
    GET_ALL_ORDERGOODS: (state: any) => {
      return state.DATA_ORDERGOODS;
    },
    GET_TOTAL_ALL_ORDERGOODS: (state: any) => {
      return state.TOTAL_ORDERGOODS;
    },
    GET_DETAIL_GOOD: (state: any) => {
      return state.DETAIL_GOOD;
    },
  },

  mutations: {
    SET_ALL_ORDERGOODS(state: any, data: any) {
      state.DATA_ORDERGOODS = data;
    },
    SET_TOTAL_ALL_ORDERGOODS(state: any, data: any) {
      state.TOTAL_ORDERGOODS = data;
    },
    UPDATED_OBJ_FROM_ORDERGOODS(state: any, data: any) {
      state.DATA_ORDERGOODS = state.DATA_ORDERGOODS.map((item: any) => {
        return item.id === data.id ? { ...item, ...data } : item;
      });
    },
    DELETE_OBJ_FROM_ORDERGOODS(state: any, id: number) {
      state.DATA_ORDERGOODS = state.DATA_ORDERGOODS.filter((item: any) => {
        return item.id !== id;
      });
      state.TOTAL_ORDERGOODS = state.TOTAL_ORDERGOODS - 1;
    },
    SET_DETAIL_GOOD(state: any, data: any) {
      state.DETAIL_GOOD = data;
    },
  },

  actions: {
    async FETCH_ALL_ORDERGOODS(context: any, payload: any) {
      try {
        const res = await getAllOrderGoods(payload);
        if (res.status === 200) {
          context.commit("SET_TOTAL_ALL_ORDERGOODS", res.data.total);
          context.commit("SET_ALL_ORDERGOODS", res.data.items);
        }
      } catch (error: any) {
        console.log(`Error FETCH_ORDERGOODS => ${error}`);
        console.log(error.response);
      }
    },

    async CREATE_ORDERGOODS(context: any, payload: any) {
      try {
        const res = await createOrderGoods(payload);
        if (res.status === 201) {
          await context.dispatch("FETCH_ORDERGOODS");
          return res.data;
        }
      } catch (error: any) {
        console.log(`Error CREATE_ORDERGOODS => ${error}`);
        console.log(error.response);
      }
    },

    async UPDATE_ORDERGOODS(context: any, payload: any) {
      try {
        const { id, ...data } = payload;
        const res = await updateOrderGoods(id, data);
        if (res.status === 200) {
          context.commit("UPDATED_OBJ_FROM_ORDERGOODS", res.data);
          return res.data;
        }
      } catch (error: any) {
        console.log(`Error UPDATE_ORDERGOODS => ${error}`);
        console.log(error.response);
      }
    },

    async DELETE_ORDERGOODS(context: any, id: number) {
      try {
        const res = await deleteOrderGoods(id);
        if (res.status === 204) {
          context.commit("DELETE_OBJ_FROM_ORDERGOODS", id);
        }
      } catch (error: any) {
        console.log(`Error DELETE_ORDERGOODS => ${error}`);
        console.log(error.response);
      }
    },

    async FETCH_DETAIL_ORDERGOODS(context: any, id: number) {
      try {
        const res = await getOrderGoodsById(id);
        context.commit("SET_DETAIL_ORDERGOODS", res.data);
      } catch (error: any) {
        console.log(`Error FETCH_DETAIL_ORDERGOODS => ${error}`);
        console.log(error.response);
      }
    },
  },
};
