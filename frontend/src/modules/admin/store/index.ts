import { getAllGoods, createGood, updateGood, deleteGood, getGoodById } from "@/modules/admin/api";
import { dispatchNotification } from "@/modules/common/utils/notifications";

export default {
  namespaced: true,
  state: {
    DATA_GOODS: [],
    TOTAL_GOODS: 0,
    DETAIL_GOOD: null,
  },

  getters: {
    GET_ALL_GOODS: (state: any) => {
      return state.DATA_GOODS;
    },
    GET_TOTAL_ALL_GOODS: (state: any) => {
      return state.TOTAL_GOODS;
    },
    GET_DETAIL_GOOD: (state: any) => {
      return state.DETAIL_GOOD;
    },
  },

  mutations: {
    SET_ALL_GOODS(state: any, data: any) {
      state.DATA_GOODS = data;
    },
    SET_TOTAL_ALL_GOODS(state: any, data: any) {
      state.TOTAL_GOODS = data;
    },
    UPDATED_OBJ_FROM_GOODS(state: any, data: any) {
      state.DATA_GOODS = state.DATA_GOODS.map((item: any) => {
        return item.id === data.id ? { ...item, ...data } : item;
      });
    },
    DELETE_OBJ_FROM_GOODS(state: any, id: number) {
      state.DATA_GOODS = state.DATA_GOODS.filter((item: any) => {
        return item.id !== id;
      });
      state.TOTAL_GOODS = state.TOTAL_GOODS - 1;
    },
    SET_DETAIL_GOOD(state: any, data: any) {
      state.DETAIL_GOOD = data;
    },
  },

  actions: {
    async FETCH_ALL_GOODS(context: any, payload: any) {
      try {
        const res = await getAllGoods(payload);
        if (res.status === 200) {
          context.commit("SET_TOTAL_ALL_GOODS", res.data.total);
          context.commit("SET_ALL_GOODS", res.data.items);
        }
      } catch (error: any) {
        console.log(`Error FETCH_GOODS => ${error}`);
        console.log(error.response);
      }
    },

    async CREATE_GOODS(context: any, payload: any) {
      try {
        const res = await createGood(payload);
        if (res.status === 201) {
          await context.dispatch("FETCH_GOODS");
          return res.data;
        }
      } catch (error: any) {
        console.log(`Error CREATE_GOODS => ${error}`);
        console.log(error.response);
      }
    },

    async UPDATE_GOODS(context: any, payload: any) {
      try {
        const { id, ...data } = payload;
        const res = await updateGood(id, data);
        if (res.status === 200) {
          context.commit("UPDATED_OBJ_FROM_GOODS", res.data);
          return res.data;
        }
      } catch (error: any) {
        console.log(`Error UPDATE_GOODS => ${error}`);
        console.log(error.response);
      }
    },

    async DELETE_GOODS(context: any, id: number) {
      try {
        const res = await deleteGood(id);
        if (res.status === 204) {
          context.commit("DELETE_OBJ_FROM_GOODS", id);
        }
      } catch (error: any) {
        console.log(`Error DELETE_GOODS => ${error}`);
        console.log(error.response);
      }
    },

    async FETCH_DETAIL_GOOD(context: any, id: number) {
      try {
        const res = await getGoodById(id);
        context.commit("SET_DETAIL_GOOD", res.data);
      } catch (error: any) {
        console.log(`Error FETCH_DETAIL_GOOD => ${error}`);
        console.log(error.response);
      }
    },
  },
};
