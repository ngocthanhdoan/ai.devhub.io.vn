import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // Corrected import path
import "./index.css"; // Tailwind CSS

createApp(App).use(router).mount("#app");