import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import VueApexCharts from 'vue3-apexcharts'
import App from './App.vue'
import Overview from './views/Overview.vue'
import AEDAnalysis from './views/AEDAnalysis.vue'
import ShelterAnalysis from './views/ShelterAnalysis.vue'
import AirRaidShelter from './views/AirRaidShelter.vue'
import TouristSpotAnalysis from './views/TouristSpotAnalysis.vue'
import ComparisonView from './views/ComparisonView.vue'

import './style.css'

const routes = [
  { path: '/', component: Overview },
  { path: '/aed', component: AEDAnalysis },
  { path: '/shelter', component: ShelterAnalysis },
  { path: '/air-raid', component: AirRaidShelter },
  { path: '/tourist', component: TouristSpotAnalysis },
  { path: '/comparison', component: ComparisonView }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.use(VueApexCharts)
app.mount('#app')
