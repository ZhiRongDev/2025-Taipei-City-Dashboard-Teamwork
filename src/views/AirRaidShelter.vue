<template>
  <div class="air-raid-shelter">
    <div class="card">
      <h2>防空疏散避難設施分析 Air Raid Shelter Analysis</h2>
      <p style="color: #94a3b8;">
        分析防空疏散設施容納人數、收容所面積與人均可分配空間
      </p>
    </div>

    <div class="filter-bar">
      <div class="filter-group">
        <label>選擇縣市：</label>
        <select v-model="selectedCity">
          <option value="all">全部</option>
          <option value="臺北市">台北市</option>
          <option value="新北市">新北市</option>
        </select>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">總容納人數</div>
        <div class="stat-value">{{ filteredStats.totalCapacity.toLocaleString() }}<span class="stat-unit">人</span></div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">總收容面積</div>
        <div class="stat-value">{{ filteredStats.totalArea.toLocaleString() }}<span class="stat-unit">m²</span></div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-label">平均每人可分配面積</div>
        <div class="stat-value">{{ filteredStats.avgAreaPerPerson }}<span class="stat-unit">m²</span></div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">最高配置區</div>
        <div class="stat-value" style="font-size: 1.2rem;">{{ filteredStats.topDistrict }}</div>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>各區容納人數</h3>
        <apexchart type="bar" height="400" :options="capacityChartOptions" :series="capacitySeries"></apexchart>
      </div>

      <div class="card">
        <h3>各區收容所總面積</h3>
        <apexchart type="bar" height="400" :options="areaChartOptions" :series="areaSeries"></apexchart>
      </div>
    </div>

    <div class="card">
      <h3>每萬人可分配收容所面積比較</h3>
      <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
        數值越高表示該區防空疏散設施人均空間越充足
      </p>
      <apexchart type="bar" height="450" :options="perCapitaChartOptions" :series="perCapitaSeries"></apexchart>
    </div>

    <div class="card">
      <h3>容納人數 vs 收容所面積散點圖</h3>
      <apexchart type="scatter" height="450" :options="scatterChartOptions" :series="scatterSeries"></apexchart>
    </div>

    <div class="card">
      <h3>空間指標比較：平均兩兩距離 vs 空間熵</h3>
      <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
        比較兩種空間分析指標：<strong style="color: #60a5fa;">Dispersion (離散度)</strong> 衡量設施間的實際距離分散程度，
        <strong style="color: #34d399;">Spatial Entropy (空間熵)</strong> 衡量設施分布的均勻性與隨機性
      </p>
      <apexchart type="bar" height="400" :options="spatialMetricsChartOptions" :series="spatialMetricsSeries">
      </apexchart>
    </div>

    <div class="card">
      <h3>防空疏散設施分布地圖</h3>
      <div ref="airRaidMapContainer" class="map-container"></div>
    </div>

    <div class="card">
      <h3>詳細資料表</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>縣市</th>
              <th>行政區</th>
              <th>容納人數</th>
              <th>收容所面積 (m²)</th>
              <th>人口數</th>
              <th>每人可分配面積 (m²)</th>
              <th>每萬人可分配面積 (m²)</th>
              <th>空間等級</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in filteredTableData" :key="`${row.City}-${row.Town}`">
              <td>{{ row.City }}</td>
              <td>{{ row.Town }}</td>
              <td>{{ row['容納人數']?.toLocaleString() || 0 }}</td>
              <td>{{ row['收容所面積（平方公尺）']?.toLocaleString() || 0 }}</td>
              <td>{{ row['人口數']?.toLocaleString() || 0 }}</td>
              <td>{{ row['每人可分配收容所面積（平方公尺）']?.toFixed(3) || 'N/A' }}</td>
              <td>{{ row['每萬人可分配收容所面積（平方公尺）']?.toFixed(2) || 'N/A' }}</td>
              <td>
                <span :class="getSpaceBadge(row['每萬人可分配收容所面積（平方公尺）'])">
                  {{ getSpaceLevel(row['每萬人可分配收容所面積（平方公尺）']) }}
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
import { ref, computed, onMounted } from 'vue'
import mapboxgl from 'mapbox-gl'
import { loadCSV, loadGeoJSON } from '../utils/csvLoader'

export default {
  name: 'AirRaidShelter',
  setup() {
    const airRaidMapContainer = ref(null)
    const selectedCity = ref('all')
    const taipeiData = ref([])
    const newTaipeiData = ref([])
    const spatialMetricsData = ref([])

    const allData = computed(() => [...taipeiData.value, ...newTaipeiData.value])

    const filteredData = computed(() => {
      if (selectedCity.value === 'all') return allData.value
      return allData.value.filter(row => row.City === selectedCity.value)
    })

    const filteredTableData = computed(() => {
      return filteredData.value.slice().sort((a, b) =>
        (b['每萬人可分配收容所面積（平方公尺）'] || 0) - (a['每萬人可分配收容所面積（平方公尺）'] || 0)
      )
    })

    const filteredStats = computed(() => {
      const data = filteredData.value
      const totalCapacity = data.reduce((sum, row) => sum + (row['容納人數'] || 0), 0)
      const totalArea = Math.round(data.reduce((sum, row) => sum + (row['收容所面積（平方公尺）'] || 0), 0))
      const totalPopulation = data.reduce((sum, row) => sum + (row['人口數'] || 0), 0)
      const avgAreaPerPerson = totalPopulation > 0 ? (totalArea / totalPopulation).toFixed(3) : 0

      const sorted = data.slice().sort((a, b) =>
        (b['每萬人可分配收容所面積（平方公尺）'] || 0) - (a['每萬人可分配收容所面積（平方公尺）'] || 0)
      )
      const topDistrict = sorted[0] ? sorted[0].Town : 'N/A'

      return { totalCapacity, totalArea, avgAreaPerPerson, topDistrict }
    })

    const capacitySeries = computed(() => [{
      name: '容納人數',
      data: filteredData.value.slice(0, 20).map(row => row['容納人數'] || 0)
    }])

    const capacityChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: filteredData.value.slice(0, 20).map(row => row.Town),
        labels: {
          style: { colors: '#94a3b8' },
          rotate: -45
        }
      },
      yaxis: {
        labels: {
          style: { colors: '#94a3b8' },
          formatter: (val) => val.toLocaleString()
        }
      },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: {
        bar: { borderRadius: 4 }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      }
    }))

    const areaSeries = computed(() => [{
      name: '收容所面積 (m²)',
      data: filteredData.value.slice(0, 20).map(row => Math.round(row['收容所面積（平方公尺）'] || 0))
    }])

    const areaChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: filteredData.value.slice(0, 20).map(row => row.Town),
        labels: {
          style: { colors: '#94a3b8' },
          rotate: -45
        }
      },
      yaxis: {
        labels: {
          style: { colors: '#94a3b8' },
          formatter: (val) => val.toLocaleString()
        }
      },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: {
        bar: { borderRadius: 4 }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      }
    }))

    const perCapitaSeries = computed(() => [{
      name: '每萬人可分配面積 (m²)',
      data: filteredData.value.map(row => ({
        x: row.Town,
        y: parseFloat((row['每萬人可分配收容所面積（平方公尺）'] || 0).toFixed(2))
      }))
    }])

    const perCapitaChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      plotOptions: {
        bar: {
          borderRadius: 4,
          horizontal: true,
          distributed: true
        }
      },
      xaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      dataLabels: {
        enabled: true,
        style: { colors: ['#fff'] },
        formatter: (val) => val.toFixed(0)
      },
      colors: ['#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa', '#fb7185', '#2dd4bf', '#fb923c'],
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: { show: false }
    }))

    const scatterSeries = computed(() => {
      const taipei = filteredData.value.filter(r => r.City === '臺北市')
      const newTaipei = filteredData.value.filter(r => r.City === '新北市')

      const series = []
      if (selectedCity.value === 'all' || selectedCity.value === '臺北市') {
        series.push({
          name: '台北市',
          data: taipei.map(row => ({
            x: row['容納人數'] || 0,
            y: Math.round(row['收容所面積（平方公尺）'] || 0)
          }))
        })
      }
      if (selectedCity.value === 'all' || selectedCity.value === '新北市') {
        series.push({
          name: '新北市',
          data: newTaipei.map(row => ({
            x: row['容納人數'] || 0,
            y: Math.round(row['收容所面積（平方公尺）'] || 0)
          }))
        })
      }
      return series
    })

    const scatterChartOptions = computed(() => ({
      chart: {
        type: 'scatter',
        background: 'transparent',
        toolbar: { show: true },
        zoom: { enabled: true }
      },
      theme: { mode: 'dark' },
      xaxis: {
        title: { text: '容納人數', style: { color: '#94a3b8' } },
        labels: {
          style: { colors: '#94a3b8' },
          formatter: (val) => val.toLocaleString()
        }
      },
      yaxis: {
        title: { text: '收容所面積 (m²)', style: { color: '#94a3b8' } },
        labels: {
          style: { colors: '#94a3b8' },
          formatter: (val) => val.toLocaleString()
        }
      },
      colors: ['#60a5fa', '#34d399'],
      markers: { size: 8 },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: {
        labels: { colors: '#94a3b8' }
      }
    }))

    const getSpaceLevel = (perCapitaArea) => {
      if (!perCapitaArea) return 'N/A'
      if (perCapitaArea >= 1000) return '優良'
      if (perCapitaArea >= 500) return '良好'
      if (perCapitaArea >= 300) return '普通'
      return '待改善'
    }

    const getSpaceBadge = (perCapitaArea) => {
      if (!perCapitaArea) return 'badge'
      if (perCapitaArea >= 1000) return 'badge badge-low'
      if (perCapitaArea >= 500) return 'badge badge-low'
      if (perCapitaArea >= 300) return 'badge badge-medium'
      return 'badge badge-high'
    }

    const spatialMetricsSeries = computed(() => {
      const filteredMetrics = selectedCity.value === 'all'
        ? spatialMetricsData.value
        : spatialMetricsData.value.filter(r => r.City === selectedCity.value)

      return [
        {
          name: '平均兩兩距離 (Dispersion)',
          data: filteredMetrics.map(row => ({
            x: row.City === '臺北市' ? '台北市' : '新北市',
            y: (row.Dispersion || 0) * 1000 // 放大 1000 倍以便顯示
          }))
        },
        {
          name: '空間熵 (Spatial Entropy)',
          data: filteredMetrics.map(row => ({
            x: row.City === '臺北市' ? '台北市' : '新北市',
            y: row.SpatialEntropy || 0
          }))
        }
      ]
    })

    const spatialMetricsChartOptions = {
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      plotOptions: {
        bar: {
          borderRadius: 4,
          columnWidth: '60%',
          dataLabels: {
            position: 'top'
          }
        }
      },
      dataLabels: {
        enabled: true,
        formatter: function (val, opts) {
          if (opts.seriesIndex === 0) {
            return (val / 1000).toFixed(3)
          }
          return val.toFixed(2)
        },
        style: {
          colors: ['#fff'],
          fontSize: '11px'
        },
        offsetY: -20
      },
      xaxis: {
        labels: {
          style: { colors: '#94a3b8' }
        }
      },
      yaxis: [
        {
          title: {
            text: '平均兩兩距離 (×1000)',
            style: { color: '#60a5fa' }
          },
          labels: {
            style: { colors: '#94a3b8' },
            formatter: (val) => val.toFixed(0)
          }
        },
        {
          opposite: true,
          title: {
            text: '空間熵',
            style: { color: '#34d399' }
          },
          labels: {
            style: { colors: '#94a3b8' },
            formatter: (val) => val.toFixed(2)
          }
        }
      ],
      colors: ['#60a5fa', '#34d399'],
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: {
        labels: { colors: '#94a3b8' },
        position: 'top'
      },
      tooltip: {
        theme: 'dark',
        y: {
          formatter: function (val, opts) {
            if (opts.seriesIndex === 0) {
              return '離散度: ' + (val / 1000).toFixed(4)
            }
            return '空間熵: ' + val.toFixed(3)
          }
        }
      }
    }

    const initAirRaidMap = async () => {
      mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN

      const map = new mapboxgl.Map({
        container: airRaidMapContainer.value,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [121.5654, 25.0330],
        zoom: 10
      })

      map.on('load', async () => {
        try {
          const geoData = await loadGeoJSON('/source/clean/合併/town.geojson')
          const airData = allData.value

          const airMap = {}
          airData.forEach(row => {
            const key = `${row.City}-${row.Town}`
            airMap[key] = row['每萬人可分配收容所面積（平方公尺）'] || 0
          })

          geoData.features.forEach(feature => {
            const county = feature.properties.COUNTY
            const town = feature.properties.TOWN
            const key = `${county}-${town}`
            feature.properties.per_capita_area = airMap[key] || 0
          })

          map.addSource('air-raid-districts', {
            type: 'geojson',
            data: geoData
          })

          map.addLayer({
            id: 'air-raid-districts-fill',
            type: 'fill',
            source: 'air-raid-districts',
            paint: {
              'fill-color': [
                'interpolate',
                ['linear'],
                ['get', 'per_capita_area'],
                0, '#1e293b',
                300, '#f87171',
                500, '#fbbf24',
                1000, '#34d399',
                2000, '#60a5fa'
              ],
              'fill-opacity': 0.7
            }
          })

          map.addLayer({
            id: 'air-raid-districts-outline',
            type: 'line',
            source: 'air-raid-districts',
            paint: {
              'line-color': '#475569',
              'line-width': 1
            }
          })

          map.on('click', 'air-raid-districts-fill', (e) => {
            const props = e.features[0].properties
            new mapboxgl.Popup()
              .setLngLat(e.lngLat)
              .setHTML(`
                <div style="color: #1e293b; padding: 5px;">
                  <strong>${props.COUNTY} ${props.TOWN}</strong><br>
                  每萬人可分配面積: ${props.per_capita_area?.toFixed(2) || 'N/A'} m²<br>
                  人口數: ${props.P_CNT?.toLocaleString() || 'N/A'}
                </div>
              `)
              .addTo(map)
          })

          map.on('mouseenter', 'air-raid-districts-fill', () => {
            map.getCanvas().style.cursor = 'pointer'
          })

          map.on('mouseleave', 'air-raid-districts-fill', () => {
            map.getCanvas().style.cursor = ''
          })

        } catch (error) {
          console.error('Error loading air raid map:', error)
        }
      })
    }

    onMounted(async () => {
      try {
        taipeiData.value = await loadCSV('/source/topic/taipei/topic2-1__Town__asylum__pol_land_rate.csv')
        newTaipeiData.value = await loadCSV('/source/topic/newtaipeis/topic2-1__Town__asylum__pol_land_rate.csv')

        // 載入防空疏散地點的空間指標資料
        const taipeiMetrics = await loadCSV('/source/topic/taipei/topic1-2__City__regional_discrete_count(防空疏散地點).csv')
        const newTaipeiMetrics = await loadCSV('/source/topic/newtaipeis/topic1-2__City__regional_discrete_count(防空疏散地點).csv')
        spatialMetricsData.value = [...taipeiMetrics, ...newTaipeiMetrics]

        initAirRaidMap()
      } catch (error) {
        console.error('Error loading air raid data:', error)
      }
    })

    return {
      airRaidMapContainer,
      selectedCity,
      filteredStats,
      filteredTableData,
      capacitySeries,
      capacityChartOptions,
      areaSeries,
      areaChartOptions,
      perCapitaSeries,
      perCapitaChartOptions,
      scatterSeries,
      scatterChartOptions,
      getSpaceLevel,
      getSpaceBadge,
      spatialMetricsSeries,
      spatialMetricsChartOptions
    }
  }
}
</script>
