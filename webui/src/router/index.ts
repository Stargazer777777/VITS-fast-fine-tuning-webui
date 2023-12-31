import { createRouter, createWebHashHistory } from 'vue-router';

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home',
    },
    {
      path: '/home',
      component: () => import('@/views/homeFrame.vue'),
    },
    {
      path: '/train',
      component: () => import('@/views/tranningFrame.vue'),
    },
  ],
});

export default router;
