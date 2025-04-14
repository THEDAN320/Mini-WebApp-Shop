import { createApp, watch } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import i18n from "./modules/i18n";

// Begin // This parameter resolves the conflict of Tailwind CSS styles with naive.
const meta = document.createElement("meta");
meta.name = "naive-ui-style";
document.head.appendChild(meta);
// End

const app = createApp(App);

app.use(store);
app.use(router);
app.use(i18n);
app.mount("#app");
