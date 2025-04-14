import { createI18n } from "vue-i18n";
import ru from "@/modules/common/i18n/locales/ru.json";

const i18n = createI18n({
  legacy: true,
  locale: "ru",
  messages: {
    ru,
  },
});

export default i18n;
