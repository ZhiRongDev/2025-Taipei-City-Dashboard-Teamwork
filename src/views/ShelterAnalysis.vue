<template>
  <div class="shelter-analysis">
    <div class="card">
      <h2>避難收容處所分析 Shelter Analysis</h2>
      <p style="color: #94a3b8;">
        分析各災別避難收容處所分布、容量及空間熵指標
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
      <div class="filter-group">
        <label>災別類型：</label>
        <select v-model="selectedDisasterType">
          <option value="任一災別避難地點數">全部災別</option>
          <option value="flood_shelter_count">水災</option>
          <option value="earthquake_shelter_count">地震</option>
          <option value="landslide_shelter_count">土石流</option>
          <option value="tsunami_shelter_count">海嘯</option>
        </select>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">總避難處所</div>
        <div class="stat-value">{{ filteredStats.total }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">平均每區</div>
        <div class="stat-value">{{ filteredStats.avgPerDistrict }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-label">最高配置區</div>
        <div class="stat-value" style="font-size: 1.2rem;">{{ filteredStats.topDistrict }}</div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">最低配置區</div>
        <div class="stat-value" style="font-size: 1.2rem;">{{ filteredStats.lowDistrict }}</div>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>各區避難處所數量 ({{ disasterTypeLabel }})</h3>
        <apexchart type="bar" height="400" :options="shelterCountChartOptions" :series="shelterCountSeries"></apexchart>
      </div>

      <div class="card">
        <h3>各災別避難處所分布</h3>
        <apexchart type="radar" height="400" :options="disasterTypeChartOptions" :series="disasterTypeSeries">
        </apexchart>
      </div>
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
      <h3>避難處所分布地圖</h3>
      <div ref="shelterMapContainer" class="map-container"></div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>各區比較 (水平條形圖)</h3>
        <apexchart type="bar" height="500" :options="horizontalBarChartOptions" :series="horizontalBarSeries">
        </apexchart>
      </div>

      <div class="card">
        <h3>災別熱力圖</h3>
        <apexchart type="heatmap" height="500" :options="heatmapChartOptions" :series="heatmapSeries"></apexchart>
      </div>
    </div>

    <div class="card">
      <h3>詳細資料表</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>縣市</th>
              <th>行政區</th>
              <th>水災避難處</th>
              <th>地震避難處</th>
              <th>土石流避難處</th>
              <th>海嘯避難處</th>
              <th>總避難處所</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in filteredTableData" :key="`${row.city}-${row['鄉鎮']}`">
              <td>{{ row.city }}</td>
              <td>{{ row['鄉鎮'] }}</td>
              <td>{{ row.flood_shelter_count || 0 }}</td>
              <td>{{ row.earthquake_shelter_count || 0 }}</td>
              <td>{{ row.landslide_shelter_count || 0 }}</td>
              <td>{{ row.tsunami_shelter_count || 0 }}</td>
              <td><strong>{{ row['任一災別避難地點數'] || 0 }}</strong></td>
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
  name: 'ShelterAnalysis',
  setup() {
    const shelterMapContainer = ref(null)
    const selectedCity = ref('all')
    const selectedDisasterType = ref('任一災別避難地點數')
    const shelterData = ref([])
    const spatialMetricsData = ref([])

    const disasterTypeLabel = computed(() => {
      const labels = {
        '任一災別避難地點數': '全部災別',
        'flood_shelter_count': '水災',
        'earthquake_shelter_count': '地震',
        'landslide_shelter_count': '土石流',
        'tsunami_shelter_count': '海嘯'
      }
      return labels[selectedDisasterType.value] || '全部災別'
    })

    const filteredData = computed(() => {
      if (selectedCity.value === 'all') return shelterData.value
      return shelterData.value.filter(row => row.city === selectedCity.value)
    })

    const filteredTableData = computed(() => {
      return filteredData.value.slice().sort((a, b) =>
        (b['任一災別避難地點數'] || 0) - (a['任一災別避難地點數'] || 0)
      )
    })

    const filteredStats = computed(() => {
      const data = filteredData.value
      const total = data.reduce((sum, row) => sum + (row[selectedDisasterType.value] || 0), 0)
      const avgPerDistrict = data.length > 0 ? Math.round(total / data.length) : 0

      const sorted = data.slice().sort((a, b) =>
        (b[selectedDisasterType.value] || 0) - (a[selectedDisasterType.value] || 0)
      )
      const topDistrict = sorted[0] ? sorted[0]['鄉鎮'] : 'N/A'
      const lowDistrict = sorted[sorted.length - 1] ? sorted[sorted.length - 1]['鄉鎮'] : 'N/A'

      return { total, avgPerDistrict, topDistrict, lowDistrict }
    })

    const shelterCountSeries = computed(() => [{
      name: '避難處所數',
      data: filteredData.value.slice(0, 20).map(row => row[selectedDisasterType.value] || 0)
    }])

    const shelterCountChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: filteredData.value.slice(0, 20).map(row => row['鄉鎮']),
        labels: {
          style: { colors: '#94a3b8' },
          rotate: -45
        }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: {
        bar: {
          borderRadius: 4
        }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      }
    }))

    const disasterTypeSeries = computed(() => {
      const top10 = filteredData.value.slice(0, 10)

      return [
        {
          name: '水災',
          data: top10.map(row => row.flood_shelter_count || 0)
        },
        {
          name: '地震',
          data: top10.map(row => row.earthquake_shelter_count || 0)
        },
        {
          name: '土石流',
          data: top10.map(row => row.landslide_shelter_count || 0)
        },
        {
          name: '海嘯',
          data: top10.map(row => row.tsunami_shelter_count || 0)
        }
      ]
    })

    const disasterTypeChartOptions = computed(() => ({
      chart: {
        type: 'radar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: filteredData.value.slice(0, 10).map(row => row['鄉鎮']),
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        show: true,
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#60a5fa', '#34d399', '#fbbf24', '#f87171'],
      stroke: {
        width: 2
      },
      fill: {
        opacity: 0.2
      },
      markers: {
        size: 4
      },
      legend: {
        labels: { colors: '#94a3b8' }
      }
    }))

    const horizontalBarSeries = computed(() => [{
      name: '避難處所數',
      data: filteredData.value.slice(0, 15).map(row => row[selectedDisasterType.value] || 0)
    }])

    const horizontalBarChartOptions = computed(() => ({
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
        style: { colors: ['#fff'] }
      },
      colors: ['#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa', '#fb7185', '#2dd4bf', '#fb923c', '#c084fc', '#4ade80', '#38bdf8', '#facc15', '#f472b6', '#818cf8', '#6ee7b7'],
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      xaxis: {
        categories: filteredData.value.slice(0, 15).map(row => row['鄉鎮'])
      },
      legend: { show: false }
    }))

    const heatmapSeries = computed(() => {
      const disasters = ['flood_shelter_count', 'earthquake_shelter_count', 'landslide_shelter_count', 'tsunami_shelter_count']
      const labels = ['水災', '地震', '土石流', '海嘯']

      return disasters.map((disaster, idx) => ({
        name: labels[idx],
        data: filteredData.value.slice(0, 15).map(row => ({
          x: row['鄉鎮'],
          y: row[disaster] || 0
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
        style: { colors: ['#fff'] }
      },
      colors: ['#60a5fa'],
      xaxis: {
        labels: {
          style: { colors: '#94a3b8' },
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
              { from: 0, to: 10, color: '#1e293b', name: '低' },
              { from: 11, to: 20, color: '#3b82f6', name: '中' },
              { from: 21, to: 30, color: '#34d399', name: '高' },
              { from: 31, to: 50, color: '#fbbf24', name: '非常高' }
            ]
          }
        }
      }
    }))

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
          // 如果是 Dispersion 系列（index 0），顯示實際值（除以 1000）
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

    const initShelterMap = async () => {
      mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN

      const map = new mapboxgl.Map({
        container: shelterMapContainer.value,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [121.5654, 25.0330],
        zoom: 10
      })

      map.on('load', async () => {
        try {
          const geoData = await loadGeoJSON('/source/clean/合併/town.geojson')
          const shelData = shelterData.value

          const shelterMap = {}
          shelData.forEach(row => {
            const key = `${row.city}-${row['鄉鎮']}`
            shelterMap[key] = row['任一災別避難地點數'] || 0
          })

          geoData.features.forEach(feature => {
            const county = feature.properties.COUNTY
            const town = feature.properties.TOWN
            const key = `${county}-${town}`
            feature.properties.shelter_count = shelterMap[key] || 0
          })

          map.addSource('shelter-districts', {
            type: 'geojson',
            data: geoData
          })

          map.addLayer({
            id: 'shelter-districts-fill',
            type: 'fill',
            source: 'shelter-districts',
            paint: {
              'fill-color': [
                'interpolate',
                ['linear'],
                ['get', 'shelter_count'],
                0, '#1e293b',
                10, '#3b82f6',
                20, '#34d399',
                30, '#fbbf24',
                40, '#f87171'
              ],
              'fill-opacity': 0.7
            }
          })

          map.addLayer({
            id: 'shelter-districts-outline',
            type: 'line',
            source: 'shelter-districts',
            paint: {
              'line-color': '#475569',
              'line-width': 1
            }
          })

          map.on('click', 'shelter-districts-fill', (e) => {
            const props = e.features[0].properties
            new mapboxgl.Popup()
              .setLngLat(e.lngLat)
              .setHTML(`
                <div style="color: #1e293b; padding: 5px;">
                  <strong>${props.COUNTY} ${props.TOWN}</strong><br>
                  避難處所: ${props.shelter_count || 0} 處<br>
                  人口數: ${props.P_CNT?.toLocaleString() || 'N/A'}
                </div>
              `)
              .addTo(map)
          })

          map.on('mouseenter', 'shelter-districts-fill', () => {
            map.getCanvas().style.cursor = 'pointer'
          })

          map.on('mouseleave', 'shelter-districts-fill', () => {
            map.getCanvas().style.cursor = ''
          })

        } catch (error) {
          console.error('Error loading shelter map:', error)
        }
      })
    }

    onMounted(async () => {
      try {
        shelterData.value = await loadCSV('/source/component_ready/disaster.csv')

        // 載入避難收容處所的空間指標資料
        const taipeiMetrics = await loadCSV('/source/topic/taipei/topic1-2__City__regional_discrete_count(避難收容所).csv')
        const newTaipeiMetrics = await loadCSV('/source/topic/newtaipeis/topic1-2__City__regional_discrete_count(避難收容所).csv')
        spatialMetricsData.value = [...taipeiMetrics, ...newTaipeiMetrics]

        initShelterMap()
      } catch (error) {
        console.error('Error loading shelter data:', error)
      }
    })

    return {
      shelterMapContainer,
      selectedCity,
      selectedDisasterType,
      disasterTypeLabel,
      filteredStats,
      filteredTableData,
      shelterCountSeries,
      shelterCountChartOptions,
      disasterTypeSeries,
      disasterTypeChartOptions,
      horizontalBarSeries,
      horizontalBarChartOptions,
      heatmapSeries,
      heatmapChartOptions,
      spatialMetricsSeries,
      spatialMetricsChartOptions
    }
  }
}
</script>
