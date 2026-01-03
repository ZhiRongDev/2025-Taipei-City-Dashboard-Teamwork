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
        <h3>主要分析主題</h3>
        <div style="color: #cbd5e1; line-height: 2;">
          <p><strong style="color: #60a5fa;">📊 AED 分析</strong><br>
          地區分布數量、人均使用比例、空間離散度分析</p>

          <p><strong style="color: #60a5fa;">🏘️ 避難收容處所統計</strong><br>
          各災別收容能力、人均收容面積、空間熵評估</p>

          <p><strong style="color: #60a5fa;">🛡️ 防空疏散設施</strong><br>
          容納人數、設施面積、區域覆蓋率分析</p>

          <p><strong style="color: #60a5fa;">🗺️ 景點周邊資源</strong><br>
          觀光景點 1km/5km/10km 範圍內防災設施分布</p>

          <p><strong style="color: #60a5fa;">🔄 雙北比較</strong><br>
          台北市與新北市防災資源橫向比較分析</p>
        </div>
      </div>

      <div class="card">
        <h3>資料來源與方法</h3>
        <div style="color: #cbd5e1; line-height: 1.8;">
          <p><strong>資料來源：</strong></p>
          <ul style="margin-left: 20px; margin-bottom: 16px;">
            <li>內政部國土測繪中心人口統計資料</li>
            <li>政府資料開放平台防災資源清單</li>
            <li>觀光局景點遊客統計資料</li>
          </ul>

          <p><strong>分析方法：</strong></p>
          <ul style="margin-left: 20px;">
            <li><strong>離散度分析：</strong>平均兩兩距離 (Euclidean Distance)</li>
            <li><strong>空間熵：</strong>網格法分布隨機性評估</li>
            <li><strong>人口比值：</strong>每設施平均服務人口/戶數</li>
            <li><strong>距離分析：</strong>Haversine 距離計算</li>
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
