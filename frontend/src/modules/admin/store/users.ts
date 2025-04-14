import {
  getAllUsers,
  createUser,
  updateUser,
  deleteUser,
  getUserById,
} from "@/modules/admin/api/users";

export default {
  namespaced: true,
  state: {
    DATA_USERS: [],
    TOTAL_USERS: 0,
    DETAIL_GOOD: null,
  },

  getters: {
    GET_ALL_USERS: (state: any) => {
      return state.DATA_USERS;
    },
    GET_TOTAL_ALL_USERS: (state: any) => {
      return state.TOTAL_USERS;
    },
    GET_DETAIL_GOOD: (state: any) => {
      return state.DETAIL_GOOD;
    },
  },

  mutations: {
    SET_ALL_USERS(state: any, data: any) {
      state.DATA_USERS = data;
    },
    SET_TOTAL_ALL_USERS(state: any, data: any) {
      state.TOTAL_USERS = data;
    },
    UPDATED_OBJ_FROM_USERS(state: any, data: any) {
      state.DATA_USERS = state.DATA_USERS.map((item: any) => {
        return item.id === data.id ? { ...item, ...data } : item;
      });
    },
    DELETE_OBJ_FROM_USERS(state: any, id: number) {
      state.DATA_USERS = state.DATA_USERS.filter((item: any) => {
        return item.id !== id;
      });
      state.TOTAL_USERS = state.TOTAL_USERS - 1;
    },
    SET_DETAIL_GOOD(state: any, data: any) {
      state.DETAIL_GOOD = data;
    },
  },

  actions: {
    async FETCH_ALL_USERS(context: any, payload: any) {
      try {
        const res = await getAllUsers(payload);
        if (res.status === 200) {
          context.commit("SET_TOTAL_ALL_USERS", res.data.total);
          context.commit("SET_ALL_USERS", res.data.items);
        }
      } catch (error: any) {
        console.log(`Error FETCH_USERS => ${error}`);
        console.log(error.response);
      }
    },

    async CREATE_USERS(context: any, payload: any) {
      try {
        const res = await createUser(payload);
        if (res.status === 201) {
          await context.dispatch("FETCH_USERS");
          return res.data;
        }
      } catch (error: any) {
        console.log(`Error CREATE_USERS => ${error}`);
        console.log(error.response);
      }
    },

    async UPDATE_USERS(context: any, payload: any) {
      try {
        const { id, ...data } = payload;
        const res = await updateUser(id, data);
        if (res.status === 200) {
          context.commit("UPDATED_OBJ_FROM_USERS", res.data);
          return res.data;
        }
      } catch (error: any) {
        console.log(`Error UPDATE_USERS => ${error}`);
        console.log(error.response);
      }
    },

    async DELETE_USERS(context: any, id: number) {
      try {
        const res = await deleteUser(id);
        if (res.status === 204) {
          context.commit("DELETE_OBJ_FROM_USERS", id);
        }
      } catch (error: any) {
        console.log(`Error DELETE_USERS => ${error}`);
        console.log(error.response);
      }
    },

    async FETCH_DETAIL_GOOD(context: any, id: number) {
      try {
        const res = await getUserById(id);
        context.commit("SET_DETAIL_GOOD", res.data);
      } catch (error: any) {
        console.log(`Error FETCH_DETAIL_GOOD => ${error}`);
        console.log(error.response);
      }
    },
  },
};
