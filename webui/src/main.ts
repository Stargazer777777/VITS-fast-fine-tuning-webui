import { createApp } from 'vue';
import App from './App.vue';
const app = createApp(App);

import 'element-plus/dist/index.css';
import './scss/_index.scss';

const asyncRegister = async () => {
  const { default: store } = await import('./stores/index');
  app.use(store);

  const { default: router } = await import('./router/index');
  app.use(router);

  app.mount('#app');
};
asyncRegister();
