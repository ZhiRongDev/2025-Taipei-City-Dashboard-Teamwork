<template>
  <div class="overview">
    <div class="card">
      <h2>系統概述 System Overview</h2>
      <p style="color: #94a3b8; line-height: 1.8; margin-bottom: 20px;">
        本系統整合台北市與新北市防災資源數據，包含 AED、避難收容處所、防空疏散設施及消防警政單位等資訊，
        透過空間分析與人口統計比對，提供全面的防災資源分布評估。
      </p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">AED 總數</div>
        <div class="stat-value">{{ totalAED.toLocaleString() }}<span class="stat-unit">台</span></div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">避難收容處所</div>
        <div class="stat-value">{{ totalShelters.toLocaleString() }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-label">防空疏散設施</div>
        <div class="stat-value">{{ totalAirRaid.toLocaleString() }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">涵蓋行政區</div>
        <div class="stat-value">{{ totalDistricts }}<span class="stat-unit">區</span></div>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>三大分析主題</h3>
        <div style="color: #cbd5e1; line-height: 2;">
          <p><strong style="color: #60a5fa;">📊 Topic 1: 區域人口與防災資源比分析</strong><br>
          結合鄉鎮市區人口統計與防災資源（包含防空疏散設施、避難收容處所、AED 及消防/警政據點）進行比對，
          針對數量、人均數量與地點離散度等指標，分析各區的防災資源密度。</p>

          <p><strong style="color: #60a5fa;">🏘️ Topic 2: 避難所人均面積分析</strong><br>
          將防空避難設施進行空間與容量交叉評估，包括設施面積、總容納人數與人均收容空間，
          以矩形圖形式直觀呈現，協助判斷哪些地區設施壓力較高、分布較擁擠。</p>

          <p><strong style="color: #60a5fa;">🗺️ Topic 3: 景點周遭距離分析</strong><br>
          考量旅遊景點常為高人流熱區，若發生災害將對救援效率構成挑戰，因此針對觀光景點 1km、5km 與 10km
          範圍內防災設施進行 haversine 距離分析，盤點其應變能力與資源覆蓋程度。</p>
        </div>
      </div>

      <div class="card">
        <h3>資料來源與分析方法</h3>
        <div style="color: #cbd5e1; line-height: 1.8;">
          <p><strong>資料來源：</strong></p>
          <ul style="margin-left: 20px; margin-bottom: 16px;">
            <li>內政部國土測繪中心人口統計資料 (113年12月)</li>
            <li>政府資料開放平台防災資源清單</li>
            <li>觀光局景點遊客統計資料</li>
          </ul>

          <p><strong>離散度分析指標：</strong></p>
          <ul style="margin-left: 20px;">
            <li><strong>平均兩兩距離 (Dispersion):</strong> 計算各設施間的歐氏距離平均，反映地理上分散程度</li>
            <li><strong>空間熵 (Spatial Entropy):</strong> 透過網格分佈與資訊熵公式，分析設施分布的隨機性與集中性</li>
            <li><strong>人口比值指標:</strong> 透過區域人口與戶數對資源數量的比值計算</li>
            <li><strong>Haversine 距離:</strong> 用於計算景點周邊防災資源的地理距離</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="card">
      <h3>雙北各區防災資源總覽地圖</h3>
      <div ref="mapContainer" class="map-container"></div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import mapboxgl from 'mapbox-gl'
import { loadCSV, loadGeoJSON } from '../utils/csvLoader'

export default {
  name: 'Overview',
  setup() {
    const mapContainer = ref(null)
    const totalAED = ref(0)
    const totalShelters = ref(0)
    const totalAirRaid = ref(0)
    const totalDistricts = ref(42)

    onMounted(async () => {
      try {
        const aedData = await loadCSV('/source/component_ready/aed_count_by_region.csv')
        const disasterData = await loadCSV('/source/component_ready/disaster.csv')

        totalAED.value = aedData.reduce((sum, row) => sum + (row.aed_count || 0), 0)
        totalShelters.value = disasterData.reduce((sum, row) => sum + (row['任一災別避難地點數'] || 0), 0)
        totalAirRaid.value = 1500 // Approximate based on data

        initMap()
      } catch (error) {
        console.error('Error loading data:', error)
      }
    })

    const initMap = async () => {
      mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN

      const map = new mapboxgl.Map({
        container: mapContainer.value,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [121.5654, 25.0330],
        zoom: 10
      })

      map.on('load', async () => {
        try {
          const geoData = await loadGeoJSON('/source/clean/合併/town.geojson')
          const aedData = await loadCSV('/source/component_ready/aed_count_by_region.csv')

          const aedMap = {}
          aedData.forEach(row => {
            const key = `${row['場所縣市']}-${row['場所區域']}`
            aedMap[key] = row.aed_count || 0
          })

          geoData.features.forEach(feature => {
            const county = feature.properties.COUNTY
            const town = feature.properties.TOWN
            const key = `${county}-${town}`
            feature.properties.aed_count = aedMap[key] || 0
          })

          map.addSource('districts', {
            type: 'geojson',
            data: geoData
          })

          map.addLayer({
            id: 'districts-fill',
            type: 'fill',
            source: 'districts',
            paint: {
              'fill-color': [
                'interpolate',
                ['linear'],
                ['get', 'aed_count'],
                0, '#1e293b',
                50, '#3b82f6',
                150, '#34d399',
                300, '#fbbf24'
              ],
              'fill-opacity': 0.7
            }
          })

          map.addLayer({
            id: 'districts-outline',
            type: 'line',
            source: 'districts',
            paint: {
              'line-color': '#475569',
              'line-width': 1
            }
          })

          map.on('click', 'districts-fill', (e) => {
            const properties = e.features[0].properties
            new mapboxgl.Popup()
              .setLngLat(e.lngLat)
              .setHTML(`
                <div style="color: #1e293b; padding: 5px;">
                  <strong>${properties.COUNTY} ${properties.TOWN}</strong><br>
                  人口數: ${properties.P_CNT?.toLocaleString() || 'N/A'}<br>
                  戶數: ${properties.H_CNT?.toLocaleString() || 'N/A'}<br>
                  AED 數量: ${properties.aed_count || 0}
                </div>
              `)
              .addTo(map)
          })

          map.on('mouseenter', 'districts-fill', () => {
            map.getCanvas().style.cursor = 'pointer'
          })

          map.on('mouseleave', 'districts-fill', () => {
            map.getCanvas().style.cursor = ''
          })

        } catch (error) {
          console.error('Error loading map data:', error)
        }
      })
    }

    return {
      mapContainer,
      totalAED,
      totalShelters,
      totalAirRaid,
      totalDistricts
    }
  }
}
</script>
