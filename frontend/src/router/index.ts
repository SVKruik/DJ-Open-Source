import HomeView from '@/views/HomeView.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Views

// Pages

// Tabs (sub-pages)

const router = createRouter({
    history: createWebHistory(),
    linkActiveClass: "active-router-link",
    linkExactActiveClass: "active-exact-router-link",
    routes: [
        { path: "/", component: HomeView },
        { path: "/:pathMatch(.*)", redirect: "/" }
    ]
});

export default router;
