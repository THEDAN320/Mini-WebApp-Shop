import { getTimestampNow } from "@/modules/common/utils/date-time";
import { INotificationConfig, INotification } from "../types";

export default {
  namespaced: true,
  state: {
    DATA_ALL_NOTIFICATIONS: [] as Array<INotification>,
  },

  getters: {
    GET_DATA_ALL_NOTIFICATIONS: (state: any) => {
      return state.DATA_ALL_NOTIFICATIONS;
    },
    GET_COUNT_ALL_NOTIFICATIONS: (state: any) => {
      return state.DATA_ALL_NOTIFICATIONS.length;
    },
  },

  mutations: {
    ADD_NOTIFICATION(state: any, data: INotification) {
      state.DATA_ALL_NOTIFICATIONS = [data, ...state.DATA_ALL_NOTIFICATIONS];
    },

    REMOVE_NOTIFICATION(state: any, id: number) {
      state.DATA_ALL_NOTIFICATIONS = state.DATA_ALL_NOTIFICATIONS.filter(
        (notification: INotification) => notification.id !== id,
      );
    },
  },

  actions: {
    CREATE_NOTIFICATION(context: any, payload: INotificationConfig) {
      const data = {
        id: getTimestampNow(),
        type: payload.type,
        title: payload.title,
        content: payload.content,
        autoClose: payload.autoClose,
        duration: payload.duration,
      };
      context.commit("ADD_NOTIFICATION", data);
    },
  },
};
