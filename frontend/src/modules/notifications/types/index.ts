type typeName = "info" | "success" | "warning" | "error";

interface INotificationConfig {
  type: typeName;
  title: string;
  content: string | null;
  autoClose: boolean;
  duration: number;
}

interface INotification extends INotificationConfig {
  id: number;
}

export { typeName, INotificationConfig, INotification };
