import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import VueApexCharts from 'vue3-apexcharts'
import App from './App.vue'
import Overview from './views/Overview.vue'
import Topic1 from './views/Topic1.vue'
import Topic2 from './views/Topic2.vue'
import Topic3 from './views/Topic3.vue'

import './style.css'

const routes = [
  { path: '/', component: Overview },
  { path: '/topic1', component: Topic1 },
  { path: '/topic2', component: Topic2 },
  { path: '/topic3', component: Topic3 }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.use(VueApexCharts)
app.mount('#app')
