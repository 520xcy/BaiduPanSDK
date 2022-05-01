import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
{
    path: '/',
    redirect: '/files'
}, {
    path: '/:patchMatch(.*)',
    redirect: '/404'
}, {
    path: "/",
    name: "Home",
    component: Home,
    children: [
    {
        path: "/files",
        name: "Files",
        meta: {
            title: '全部文件'
        },
        component: () => import( /* webpackChunkName: "files" */ "../views/files.vue")
    }, {
        path: "/run",
        name: "Run",
        meta: {
            title: '正在下载'
        },
        component: () => import( /* webpackChunkName: "run" */ "../views/run.vue")
    }, {
        path: "/status",
        name: "Status",
        meta: {
            title: '下载完成'
        },
        component: () => import( /* webpackChunkName: "status" */ "../views/status.vue")
    }, {
        path: '/404',
        name: '404',
        meta: {
            title: '找不到页面'
        },
        component: () => import( /* webpackChunkName: "404" */ '../views/404.vue')
    }]
}, {
    path: "/login",
    name: "Login",
    meta: {
        title: '登录'
    },
    component: () => import( /* webpackChunkName: "login" */ "../views/login.vue")
}, {
    path: "/getcode",
    name: "Code",
    meta: {
        title: '扫码'
    },
    component: () => import( /* webpackChunkName: "code" */ "../views/code.vue")
}];

const router = createRouter({
    history: createWebHashHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title} | 度盘管理`;
    const role = localStorage.getItem('baidusdk');
    if ((!role || role == 'undefined') && to.path !== '/login') {
        next('/login');
    } else {
        next();
    }
    next();
});

export default router;