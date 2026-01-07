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
            針對數量、人均數量與地點離散度等指標，分析各區的防災資源密度。<br>
            <span style="color: #94a3b8; font-size: 0.9rem;">
              <strong>關鍵發現：</strong>大安區、中山區（台北市）與板橋區、新莊區（新北市）為防災資源配置密度最高的區域，
              反映都會核心區在防災建設上的優先投入。
            </span>
          </p>

          <p><strong style="color: #60a5fa;">🏘️ Topic 2: 避難所人均面積分析</strong><br>
            將防空避難設施進行空間與容量交叉評估，包括設施面積、總容納人數與人均收容空間，
            以矩形圖形式直觀呈現，協助判斷哪些地區設施壓力較高、分布較擁擠。<br>
            <span style="color: #94a3b8; font-size: 0.9rem;">
              <strong>關鍵發現：</strong>台北市萬華區每人可分配面積最大（0.192 m²），新北市板橋區雖容納人數最高但人均空間相對緊張（0.024 m²），
              顯示人口密集區需持續優化收容空間配置。
            </span>
          </p>

          <p><strong style="color: #60a5fa;">🗺️ Topic 3: 景點周遭距離分析</strong><br>
            考量旅遊景點常為高人流熱區，若發生災害將對救援效率構成挑戰，因此針對觀光景點 1km、5km 與 10km
            範圍內防災設施進行 haversine 距離分析，盤點其應變能力與資源覆蓋程度。<br>
            <span style="color: #94a3b8; font-size: 0.9rem;">
              <strong>關鍵發現：</strong>位於都會區的景點（如陽明公園、市立美術館）周邊防災資源密度較高，
              郊區與山區景點資源相對稀少，建議加強行動資源配置與疏散規劃。
            </span>
          </p>
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
      <div class="filter-bar" style="margin-bottom: 16px;">
        <div class="filter-group">
          <label>資源類型：</label>
          <select v-model="selectedMapResource">
            <option value="aed">AED</option>
            <option value="shelter">避難收容處所</option>
            <option value="police">警消單位</option>
          </select>
        </div>
      </div>
      <p style="color: #94a3b8; margin-bottom: 16px; line-height: 1.8;">
        <strong style="color: #60a5fa;">地圖說明：</strong>
        此互動式地圖以顏色分佈呈現各行政區的防災資源配置密度，從 深藍→藍→綠→黃 表示資源少到多。
        點擊任一行政區可查看該區的詳細資訊，包括人口數、戶數與各類防災資源數量。<br>
        <strong style="color: #34d399;">數據觀察：</strong>
        台北市的大安區、中山區、中正區以及新北市的板橋區、新莊區等都會核心區防災資源密度明顯較高，
        呈現由都市中心向外遞減的分布特徵。這反映了防災資源配置與都市化程度、人口密度的高度相關性，
        也凸顯偏遠區域在防災資源配置上仍有提升空間。
      </p>
      <div ref="mapContainer" class="map-container"></div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
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
    const selectedMapResource = ref('aed')

    let mapInstance = null
    let geoDataCache = null
    let resourceDataCache = {}

    onMounted(async () => {
      try {
        const aedData = await loadCSV('/source/component_ready/aed_count_by_region.csv')
        const disasterData = await loadCSV('/source/component_ready/disaster.csv')
        const policeDataTaipei = await loadCSV('/source/topic/taipei/topic1-1__Town__regional_discrete_count(警消).csv')
        const policeDataNewTaipei = await loadCSV('/source/topic/newtaipeis/topic1-1__Town__regional_discrete_count(警消).csv')

        totalAED.value = aedData.reduce((sum, row) => sum + (row.aed_count || 0), 0)
        totalShelters.value = disasterData.reduce((sum, row) => sum + (row['任一災別避難地點數'] || 0), 0)
        totalAirRaid.value = 1500 // Approximate based on data

        // Cache resource data
        resourceDataCache.aed = aedData
        resourceDataCache.shelter = disasterData
        resourceDataCache.police = [...policeDataTaipei, ...policeDataNewTaipei]

        await initMap()
      } catch (error) {
        console.error('Error loading data:', error)
      }
    })

    watch(selectedMapResource, () => {
      if (mapInstance && geoDataCache) {
        updateMapData()
      }
    })

    const getResourceConfig = (type) => {
      const configs = {
        aed: {
          property: 'aed_count',
          label: 'AED 數量',
          maxValue: 300
        },
        shelter: {
          property: 'shelter_count',
          label: '避難收容處所',
          maxValue: 50
        },
        police: {
          property: 'police_count',
          label: '警消單位',
          maxValue: 20
        }
      }
      return configs[type] || configs.aed
    }

    const updateMapData = () => {
      if (!mapInstance || !geoDataCache) return

      const config = getResourceConfig(selectedMapResource.value)

      // Update fill color based on selected resource
      mapInstance.setPaintProperty('districts-fill', 'fill-color', [
        'interpolate',
        ['linear'],
        ['get', config.property],
        0, '#1e293b',
        config.maxValue * 0.15, '#3b82f6',
        config.maxValue * 0.5, '#34d399',
        config.maxValue, '#fbbf24'
      ])
    }

    const initMap = async () => {
      mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN

      const map = new mapboxgl.Map({
        container: mapContainer.value,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [121.5654, 25.0330],
        zoom: 10
      })

      mapInstance = map

      map.on('load', async () => {
        try {
          const geoData = await loadGeoJSON('/source/clean/合併/town.geojson')
          geoDataCache = geoData

          // Load and map AED data
          const aedMap = {}
          resourceDataCache.aed.forEach(row => {
            const key = `${row['場所縣市']}-${row['場所區域']}`
            aedMap[key] = row.aed_count || 0
          })

          // Load and map shelter data
          const shelterMap = {}
          resourceDataCache.shelter.forEach(row => {
            const key = `${row.city}-${row['鄉鎮']}`
            shelterMap[key] = row['任一災別避難地點數'] || 0
          })

          // Load and map police data
          const policeMap = {}
          resourceDataCache.police.forEach(row => {
            const key = `${row.City}-${row.Town}`
            policeMap[key] = row.Count || 0
          })

          // Attach all resource data to features
          geoData.features.forEach(feature => {
            const county = feature.properties.COUNTY
            const town = feature.properties.TOWN
            const key = `${county}-${town}`

            feature.properties.aed_count = aedMap[key] || 0
            feature.properties.shelter_count = shelterMap[key] || 0
            feature.properties.police_count = policeMap[key] || 0
          })

          map.addSource('districts', {
            type: 'geojson',
            data: geoData
          })

          const config = getResourceConfig(selectedMapResource.value)

          map.addLayer({
            id: 'districts-fill',
            type: 'fill',
            source: 'districts',
            paint: {
              'fill-color': [
                'interpolate',
                ['linear'],
                ['get', config.property],
                0, '#1e293b',
                config.maxValue * 0.15, '#3b82f6',
                config.maxValue * 0.5, '#34d399',
                config.maxValue, '#fbbf24'
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
                <div style="color: #1e293b; padding: 8px;">
                  <strong style="font-size: 14px;">${properties.COUNTY} ${properties.TOWN}</strong><br>
                  <div style="margin-top: 8px; line-height: 1.6;">
                    人口數: ${properties.P_CNT?.toLocaleString() || 'N/A'}<br>
                    戶數: ${properties.H_CNT?.toLocaleString() || 'N/A'}<br>
                    <hr style="margin: 6px 0; border-color: #cbd5e1;">
                    AED 數量: ${properties.aed_count || 0} 台<br>
                    避難收容處所: ${properties.shelter_count || 0} 處<br>
                    警消單位: ${properties.police_count || 0} 處
                  </div>
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
      totalDistricts,
      selectedMapResource
    }
  }
}
</script>
