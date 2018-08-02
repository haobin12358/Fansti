import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/** note: submenu only apppear when children.length>=1
 *   detail see  https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 **/

/**
 * hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
 *                                if not set alwaysShow, only more than one route under the children
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']     will control the page roles (you can set multiple roles)
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
    noCache: true                if true ,the page will no be cached(default is false)
  }
 **/
export const constantRouterMap = [
  { path: '/', component: () => import('../views/login/index'),   redirect: 'news_manage', hidden: true },
  { path: '/login', component: () => import('../views/login/index'), hidden: true },
  { path: '/forgetPwd', component: () => import('../views/login/forgetPwd'), hidden: true },
  { path: '/error', component: () => import('../views/error/error'), hidden: true },
  {
    path: '/news_manage',
    component: Layout,
    children: [{
      path: '',
      component: () => import('../views/news_manage'),
      name: 'news_manage',
      meta: { title: 'news_manage', icon: 'news_manage', noCache: true }
    }
    ]
  },
  {
    path: '/upload_news',
    component: Layout,
    children: [{
      path: '',
      component: () => import('../views/upload_news'),
      name: 'upload_news',
      meta: { title: 'upload_news', icon: 'upload_news', noCache: true }
    }
    ]
  },
  {
    path: '/search_info',
    component: Layout,
    children: [{
      path: '',
      component: () => import('../views/search_info'),
      name: 'search_info',
      meta: { title: 'search_info', icon: 'search_info', noCache: true }
    }
    ]
  },
  {
    path: '/user_query',
    component: Layout,
    children: [{
      path: '',
      component: () => import('../views/user_query'),
      name: 'user_query',
      meta: { title: 'user_query', icon: 'user_query', noCache: true }
    }
    ]
  },
  {
    path: '/user_message',
    component: Layout,
    children: [{
      path: '',
      component: () => import('../views/user_message'),
      name: 'user_message',
      meta: { title: 'user_message', icon: 'user_message', noCache: true }
    }
    ]
  },
  {
    path: '/customer_information',
    component: Layout,
    children: [{
      path: '',
      component: () => import('../views/customer_information'),
      name: 'customer_information',
      meta: { title: 'customer_information', icon: 'customer_information', noCache: true }
    }
    ]
  }


]

export default new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})

