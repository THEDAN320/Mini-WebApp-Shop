import store from "@/store";
import { typeName } from "@/modules/notifications/types";

function dispatchNotification(
  type: typeName,
  title: string,
  content: string | null = null,
  autoClose = false,
  duration = 4000,
) {
  store.dispatch("notifications/CREATE_NOTIFICATION", {
    title: title,
    content: content,
    type: type,
    autoClose: autoClose,
    duration: duration,
  });
}

export { dispatchNotification };
