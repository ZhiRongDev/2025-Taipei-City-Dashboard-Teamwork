<template>
  <div class="tourist-spot-analysis">
    <div class="card">
      <h2>景點周邊防災資源分析 Tourist Spot Disaster Resource Analysis</h2>
      <p style="color: #94a3b8;">
        分析觀光景點周邊 1km、5km、10km 範圍內防災資源分布情況
      </p>
    </div>

    <div class="filter-bar">
      <div class="filter-group">
        <label>選擇縣市：</label>
        <select v-model="selectedCity">
          <option value="taipei">台北市</option>
          <option value="newtaipei">新北市</option>
        </select>
      </div>
      <div class="filter-group">
        <label>搜尋景點：</label>
        <input v-model="searchTerm" type="text" placeholder="輸入景點名稱..." style="min-width: 200px;" />
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">分析景點總數</div>
        <div class="stat-value">{{ filteredSpots.length }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">1km 內平均 AED</div>
        <div class="stat-value">{{ avgResources('1km', 'AED') }}<span class="stat-unit">台</span></div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-label">5km 內平均避難所</div>
        <div class="stat-value">{{ avgResources('5km', '避難收容所') }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">10km 內平均警消</div>
        <div class="stat-value">{{ avgResources('10km', '警消') }}<span class="stat-unit">處</span></div>
      </div>
    </div>

    <div class="card">
      <h3>景點周邊資源分布地圖</h3>
      <div class="filter-bar" style="margin-bottom: 16px;">
        <div class="filter-group">
          <label>顯示範圍：</label>
          <select v-model="mapRange">
            <option value="1km">1 公里</option>
            <option value="5km">5 公里</option>
            <option value="10km">10 公里</option>
          </select>
        </div>
      </div>
      <div ref="touristMapContainer" class="map-container"></div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>景點周邊 AED 資源 (不同距離比較)</h3>
        <apexchart type="bar" height="400" :options="aedDistanceChartOptions" :series="aedDistanceSeries"></apexchart>
      </div>

      <div class="card">
        <h3>景點周邊避難收容所 (不同距離比較)</h3>
        <apexchart type="bar" height="400" :options="shelterDistanceChartOptions" :series="shelterDistanceSeries">
        </apexchart>
      </div>
    </div>

    <div class="card">
      <h3>景點防災資源雷達圖 (Top 10)</h3>
      <apexchart type="radar" height="500" :options="radarChartOptions" :series="radarSeries"></apexchart>
    </div>

    <div class="card">
      <h3>景點 1km / 5km / 10km 資源熱力圖</h3>
      <apexchart type="heatmap" height="600" :options="heatmapChartOptions" :series="heatmapSeries"></apexchart>
    </div>

    <div class="card">
      <h3>詳細資料表 ({{ mapRange.replace('km', ' 公里') }}範圍)</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>景點名稱</th>
              <th>AED</th>
              <th>警消單位</th>
              <th>防空疏散地點</th>
              <th>避難收容所</th>
              <th>資源總數</th>
              <th>資源等級</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in filteredTableData" :key="idx">
              <td><strong>{{ row['旅遊景點'] }}</strong></td>
              <td>{{ row[`AED_${mapRange}`] || 0 }}</td>
              <td>{{ row[`警消_${mapRange}`] || 0 }}</td>
              <td>{{ row[`防空疏散地點_${mapRange}`] || 0 }}</td>
              <td>{{ row[`避難收容所_${mapRange}`] || 0 }}</td>
              <td>{{ getTotalResources(row, mapRange) }}</td>
              <td>
                <span :class="getResourceBadge(getTotalResources(row, mapRange))">
                  {{ getResourceLevel(getTotalResources(row, mapRange)) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import mapboxgl from 'mapbox-gl'
import { loadCSV } from '../utils/csvLoader'

export default {
  name: 'TouristSpotAnalysis',
  setup() {
    const touristMapContainer = ref(null)
    const selectedCity = ref('taipei')
    const searchTerm = ref('')
    const mapRange = ref('1km')
    const data1km = ref([])
    const data5km = ref([])
    const data10km = ref([])
    let map = null

    const allData = computed(() => {
      if (mapRange.value === '1km') return data1km.value
      if (mapRange.value === '5km') return data5km.value
      return data10km.value
    })

    const filteredSpots = computed(() => {
      let data = allData.value
      if (searchTerm.value) {
        data = data.filter(row =>
          row['旅遊景點']?.toLowerCase().includes(searchTerm.value.toLowerCase())
        )
      }
      return data
    })

    const filteredTableData = computed(() => {
      return filteredSpots.value.slice().sort((a, b) =>
        getTotalResources(b, mapRange.value) - getTotalResources(a, mapRange.value)
      )
    })

    const getTotalResources = (row, range) => {
      const aed = row[`AED_${range}`] || 0
      const police = row[`警消_${range}`] || 0
      const airRaid = row[`防空疏散地點_${range}`] || 0
      const shelter = row[`避難收容所_${range}`] || 0
      return aed + police + airRaid + shelter
    }

    const avgResources = (range, type) => {
      const data = mapRange.value === range ? allData.value :
        (range === '1km' ? data1km.value : range === '5km' ? data5km.value : data10km.value)

      const typeMap = {
        'AED': `AED_${range}`,
        '避難收容所': `避難收容所_${range}`,
        '警消': `警消_${range}`
      }
      const key = typeMap[type]
      if (!key || data.length === 0) return 0

      const sum = data.reduce((acc, row) => acc + (row[key] || 0), 0)
      return Math.round(sum / data.length)
    }

    const getResourceLevel = (total) => {
      if (total >= 500) return '優良'
      if (total >= 200) return '良好'
      if (total >= 50) return '普通'
      return '待改善'
    }

    const getResourceBadge = (total) => {
      if (total >= 500) return 'badge badge-low'
      if (total >= 200) return 'badge badge-low'
      if (total >= 50) return 'badge badge-medium'
      return 'badge badge-high'
    }

    const aedDistanceSeries = computed(() => {
      const top10 = filteredSpots.value.slice(0, 10)
      return [
        {
          name: '1km',
          data: top10.map(row => row['AED_1km'] || 0)
        },
        {
          name: '5km',
          data: top10.map(row => row['AED_5km'] || 0)
        },
        {
          name: '10km',
          data: top10.map(row => row['AED_10km'] || 0)
        }
      ]
    })

    const aedDistanceChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: filteredSpots.value.slice(0, 10).map(row => {
          const name = row['旅遊景點'] || ''
          return name.length > 8 ? name.substring(0, 8) + '...' : name
        }),
        labels: {
          style: { colors: '#94a3b8' },
          rotate: -45
        }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#60a5fa', '#34d399', '#fbbf24'],
      dataLabels: { enabled: false },
      plotOptions: {
        bar: {
          borderRadius: 4
        }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: {
        labels: { colors: '#94a3b8' }
      }
    }))

    const shelterDistanceSeries = computed(() => {
      const top10 = filteredSpots.value.slice(0, 10)
      return [
        {
          name: '1km',
          data: top10.map(row => row['避難收容所_1km'] || 0)
        },
        {
          name: '5km',
          data: top10.map(row => row['避難收容所_5km'] || 0)
        },
        {
          name: '10km',
          data: top10.map(row => row['避難收容所_10km'] || 0)
        }
      ]
    })

    const shelterDistanceChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: filteredSpots.value.slice(0, 10).map(row => {
          const name = row['旅遊景點'] || ''
          return name.length > 8 ? name.substring(0, 8) + '...' : name
        }),
        labels: {
          style: { colors: '#94a3b8' },
          rotate: -45
        }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#a78bfa', '#fb7185', '#2dd4bf'],
      dataLabels: { enabled: false },
      plotOptions: {
        bar: {
          borderRadius: 4
        }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: {
        labels: { colors: '#94a3b8' }
      }
    }))

    const radarSeries = computed(() => {
      const top10 = filteredSpots.value.slice(0, 10)
      const range = mapRange.value

      return [
        {
          name: 'AED',
          data: top10.map(row => row[`AED_${range}`] || 0)
        },
        {
          name: '警消',
          data: top10.map(row => row[`警消_${range}`] || 0)
        },
        {
          name: '防空疏散',
          data: top10.map(row => row[`防空疏散地點_${range}`] || 0)
        },
        {
          name: '避難收容所',
          data: top10.map(row => row[`避難收容所_${range}`] || 0)
        }
      ]
    })

    const radarChartOptions = computed(() => ({
      chart: {
        type: 'radar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: filteredSpots.value.slice(0, 10).map(row => {
          const name = row['旅遊景點'] || ''
          return name.length > 10 ? name.substring(0, 10) + '...' : name
        }),
        labels: { style: { colors: '#94a3b8', fontSize: '11px' } }
      },
      yaxis: {
        show: true,
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#60a5fa', '#34d399', '#fbbf24', '#f87171'],
      stroke: { width: 2 },
      fill: { opacity: 0.2 },
      markers: { size: 4 },
      legend: {
        labels: { colors: '#94a3b8' }
      }
    }))

    const heatmapSeries = computed(() => {
      const resources = ['AED', '警消', '防空疏散地點', '避難收容所']
      const spots = filteredSpots.value.slice(0, 20)

      return resources.map(resource => ({
        name: resource,
        data: spots.map(row => ({
          x: row['旅遊景點']?.substring(0, 10) || '',
          y: (row[`${resource}_1km`] || 0) + (row[`${resource}_5km`] || 0) + (row[`${resource}_10km`] || 0)
        }))
      }))
    })

    const heatmapChartOptions = computed(() => ({
      chart: {
        type: 'heatmap',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      dataLabels: {
        enabled: true,
        style: { colors: ['#fff'], fontSize: '10px' }
      },
      colors: ['#60a5fa'],
      xaxis: {
        labels: {
          style: { colors: '#94a3b8', fontSize: '10px' },
          rotate: -45
        }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      plotOptions: {
        heatmap: {
          colorScale: {
            ranges: [
              { from: 0, to: 50, color: '#1e293b', name: '低' },
              { from: 51, to: 200, color: '#3b82f6', name: '中' },
              { from: 201, to: 500, color: '#34d399', name: '高' },
              { from: 501, to: 2000, color: '#fbbf24', name: '非常高' }
            ]
          }
        }
      }
    }))

    const initTouristMap = () => {
      if (map) {
        map.remove()
      }

      mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN

      map = new mapboxgl.Map({
        container: touristMapContainer.value,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [121.5654, 25.0330],
        zoom: 10
      })

      map.on('load', () => {
        updateMapMarkers()
      })
    }

    const updateMapMarkers = () => {
      if (!map) return

      // Remove existing layers and sources
      if (map.getLayer('spots')) map.removeLayer('spots')
      if (map.getSource('spots')) map.removeSource('spots')

      const spots = filteredSpots.value.filter(row => row.lat && row.lon)

      const features = spots.map(spot => ({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [spot.lon, spot.lat]
        },
        properties: {
          name: spot['旅遊景點'],
          aed: spot[`AED_${mapRange.value}`] || 0,
          police: spot[`警消_${mapRange.value}`] || 0,
          airRaid: spot[`防空疏散地點_${mapRange.value}`] || 0,
          shelter: spot[`避難收容所_${mapRange.value}`] || 0,
          total: getTotalResources(spot, mapRange.value)
        }
      }))

      map.addSource('spots', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features
        }
      })

      map.addLayer({
        id: 'spots',
        type: 'circle',
        source: 'spots',
        paint: {
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['get', 'total'],
            0, 5,
            100, 10,
            500, 15,
            1000, 20
          ],
          'circle-color': [
            'interpolate',
            ['linear'],
            ['get', 'total'],
            0, '#f87171',
            50, '#fbbf24',
            200, '#34d399',
            500, '#60a5fa'
          ],
          'circle-opacity': 0.8,
          'circle-stroke-width': 2,
          'circle-stroke-color': '#fff'
        }
      })

      map.on('click', 'spots', (e) => {
        const props = e.features[0].properties
        new mapboxgl.Popup()
          .setLngLat(e.lngLat)
          .setHTML(`
            <div style="color: #1e293b; padding: 8px; min-width: 180px;">
              <strong style="font-size: 14px;">${props.name}</strong><br>
              <div style="margin-top: 8px; line-height: 1.6;">
                AED: ${props.aed}<br>
                警消: ${props.police}<br>
                防空疏散: ${props.airRaid}<br>
                避難收容所: ${props.shelter}<br>
                <strong>總計: ${props.total}</strong>
              </div>
            </div>
          `)
          .addTo(map)
      })

      map.on('mouseenter', 'spots', () => {
        map.getCanvas().style.cursor = 'pointer'
      })

      map.on('mouseleave', 'spots', () => {
        map.getCanvas().style.cursor = ''
      })
    }

    watch([selectedCity, mapRange], () => {
      if (map && map.loaded()) {
        updateMapMarkers()
      }
    })

    onMounted(async () => {
      try {
        const cityPath = selectedCity.value === 'taipei' ? 'taipei' : 'newtaipeis'
        data1km.value = await loadCSV(`/source/topic/${cityPath}/topic_3-1_spot_source_count_in__1km.csv`)

        if (selectedCity.value === 'taipei') {
          data5km.value = await loadCSV('/source/topic/taipei/topic_3-1_spot_source_count_in__5km.csv')
          data10km.value = await loadCSV('/source/topic/taipei/topic_3-1_spot_source_count_in__10km.csv')
        } else {
          data5km.value = await loadCSV('/source/topic/newtaipeis/topic_3-1_spot_source_count__5km.csv')
          data10km.value = await loadCSV('/source/topic/newtaipeis/topic_3-1_spot_source_count__10km.csv')
        }

        initTouristMap()
      } catch (error) {
        console.error('Error loading tourist data:', error)
      }
    })

    return {
      touristMapContainer,
      selectedCity,
      searchTerm,
      mapRange,
      filteredSpots,
      filteredTableData,
      avgResources,
      getTotalResources,
      getResourceLevel,
      getResourceBadge,
      aedDistanceSeries,
      aedDistanceChartOptions,
      shelterDistanceSeries,
      shelterDistanceChartOptions,
      radarSeries,
      radarChartOptions,
      heatmapSeries,
      heatmapChartOptions
    }
  }
}
</script>
