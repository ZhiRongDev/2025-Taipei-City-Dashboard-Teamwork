<template>
  <div class="aed-analysis">
    <div class="card">
      <h2>AED 防災資源分析 AED Distribution Analysis</h2>
      <p style="color: #94a3b8;">
        分析台北市與新北市各行政區 AED 設備分布狀況、人均使用比例及空間離散度
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
        <div class="stat-label">AED 總數</div>
        <div class="stat-value">{{ filteredStats.total }}<span class="stat-unit">台</span></div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">平均每區 AED</div>
        <div class="stat-value">{{ filteredStats.avgPerDistrict }}<span class="stat-unit">台</span></div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-label">平均每台服務人數</div>
        <div class="stat-value">{{ filteredStats.avgPeoplePerAED }}<span class="stat-unit">人</span></div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">最高配置區</div>
        <div class="stat-value" style="font-size: 1.3rem;">{{ filteredStats.topDistrict }}</div>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>各區 AED 數量分布</h3>
        <apexchart
          type="bar"
          height="400"
          :options="aedCountChartOptions"
          :series="aedCountSeries"
        ></apexchart>
      </div>

      <div class="card">
        <h3>每台 AED 平均服務人數</h3>
        <apexchart
          type="bar"
          height="400"
          :options="peoplePerAEDChartOptions"
          :series="peoplePerAEDSeries"
        ></apexchart>
      </div>
    </div>

    <div class="card">
      <h3>AED 空間離散度分析</h3>
      <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
        空間離散度反映 AED 在各區域內的分散程度，數值越高表示分布越分散，覆蓋範圍越廣
      </p>
      <apexchart
        type="scatter"
        height="450"
        :options="dispersionChartOptions"
        :series="dispersionSeries"
      ></apexchart>
    </div>

    <div class="card">
      <h3>空間指標比較：平均兩兩距離 vs 空間熵</h3>
      <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
        比較兩種空間分析指標：<strong style="color: #60a5fa;">Dispersion (離散度)</strong> 衡量設施間的實際距離分散程度，
        <strong style="color: #34d399;">Spatial Entropy (空間熵)</strong> 衡量設施分布的均勻性與隨機性
      </p>
      <apexchart
        type="bar"
        height="400"
        :options="spatialMetricsChartOptions"
        :series="spatialMetricsSeries"
      ></apexchart>
    </div>

    <div class="card">
      <h3>AED 分布地圖</h3>
      <div ref="aedMapContainer" class="map-container"></div>
    </div>

    <div class="card">
      <h3>詳細資料表</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>縣市</th>
              <th>行政區</th>
              <th>AED 數量</th>
              <th>人口數</th>
              <th>每台服務人數</th>
              <th>空間離散度</th>
              <th>資源等級</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in filteredTableData" :key="row.key">
              <td>{{ row['場所縣市'] }}</td>
              <td>{{ row['場所區域'] }}</td>
              <td>{{ row.aed_count }}</td>
              <td>{{ row['人口數']?.toLocaleString() || 'N/A' }}</td>
              <td>{{ row.people_per_aed?.toLocaleString() || 'N/A' }}</td>
              <td>{{ row.spatial_dispersion_projected?.toFixed(0) || 'N/A' }}</td>
              <td>
                <span :class="getResourceBadge(row.people_per_aed)">
                  {{ getResourceLevel(row.people_per_aed) }}
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
  name: 'AEDAnalysis',
  setup() {
    const aedMapContainer = ref(null)
    const selectedCity = ref('all')
    const aedData = ref([])
    const detailedData = ref([])
    const spatialMetricsData = ref([])

    const filteredData = computed(() => {
      if (selectedCity.value === 'all') return aedData.value
      return aedData.value.filter(row => row['場所縣市'] === selectedCity.value)
    })

    const filteredDetailedData = computed(() => {
      if (selectedCity.value === 'all') return detailedData.value
      return detailedData.value.filter(row => row['場所縣市'] === selectedCity.value)
    })

    const filteredTableData = computed(() => {
      return filteredDetailedData.value.slice().sort((a, b) => (b.aed_count || 0) - (a.aed_count || 0))
    })

    const filteredStats = computed(() => {
      const data = filteredDetailedData.value
      const total = data.reduce((sum, row) => sum + (row.aed_count || 0), 0)
      const totalPop = data.reduce((sum, row) => sum + (row['人口數'] || 0), 0)
      const avgPerDistrict = data.length > 0 ? Math.round(total / data.length) : 0
      const avgPeoplePerAED = total > 0 ? Math.round(totalPop / total) : 0
      const topDistrictData = data.reduce((max, row) =>
        (row.aed_count || 0) > (max.aed_count || 0) ? row : max, data[0] || {})
      const topDistrict = topDistrictData ? `${topDistrictData['場所區域'] || ''}` : 'N/A'

      return { total, avgPerDistrict, avgPeoplePerAED, topDistrict }
    })

    const aedCountSeries = computed(() => [{
      name: 'AED 數量',
      data: filteredData.value.slice(0, 15).map(row => row.aed_count || 0)
    }])

    const aedCountChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: filteredData.value.slice(0, 15).map(row => row['場所區域']),
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: {
        bar: {
          borderRadius: 4,
          distributed: false
        }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      }
    }))

    const peoplePerAEDSeries = computed(() => [{
      name: '每台服務人數',
      data: filteredDetailedData.value.slice(0, 15).map(row => row.people_per_aed || 0)
    }])

    const peoplePerAEDChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: filteredDetailedData.value.slice(0, 15).map(row => row['場所區域']),
        labels: { style: { colors: '#94a3b8' } }
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

    const dispersionSeries = computed(() => {
      const taipei = filteredDetailedData.value.filter(r => r['場所縣市'] === '臺北市')
      const newTaipei = filteredDetailedData.value.filter(r => r['場所縣市'] === '新北市')

      const series = []
      if (selectedCity.value === 'all' || selectedCity.value === '臺北市') {
        series.push({
          name: '台北市',
          data: taipei.map(row => ({
            x: row.people_per_aed || 0,
            y: row.spatial_dispersion_projected || 0
          }))
        })
      }
      if (selectedCity.value === 'all' || selectedCity.value === '新北市') {
        series.push({
          name: '新北市',
          data: newTaipei.map(row => ({
            x: row.people_per_aed || 0,
            y: row.spatial_dispersion_projected || 0
          }))
        })
      }
      return series
    })

    const dispersionChartOptions = computed(() => ({
      chart: {
        type: 'scatter',
        background: 'transparent',
        toolbar: { show: true },
        zoom: { enabled: true }
      },
      theme: { mode: 'dark' },
      xaxis: {
        title: { text: '每台 AED 服務人數', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        title: { text: '空間離散度', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#60a5fa', '#34d399'],
      markers: {
        size: 6
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: {
        labels: { colors: '#94a3b8' }
      }
    }))

    const spatialMetricsSeries = computed(() => {
      const filteredMetrics = spatialMetricsData.value.filter(row => {
        if (selectedCity.value === 'all') return true
        return row.City === selectedCity.value
      })

      return [
        {
          name: '平均兩兩距離 (Dispersion)',
          data: filteredMetrics.map(row => ({
            x: row.City === '臺北市' ? '台北市' : '新北市',
            y: (row.Dispersion || 0) * 1000 // 放大以便顯示
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
      xaxis: {
        labels: { style: { colors: '#94a3b8', fontSize: '14px' } }
      },
      yaxis: [
        {
          title: { text: '離散度 (×1000)', style: { color: '#60a5fa' } },
          labels: { style: { colors: '#94a3b8' } }
        },
        {
          opposite: true,
          title: { text: '空間熵', style: { color: '#34d399' } },
          labels: { style: { colors: '#94a3b8' } }
        }
      ],
      colors: ['#60a5fa', '#34d399'],
      dataLabels: {
        enabled: true,
        style: { colors: ['#fff'] },
        formatter: (val) => val.toFixed(2)
      },
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
          formatter: (val, opts) => {
            if (opts.seriesIndex === 0) {
              return (val / 1000).toFixed(4) + ' (實際離散度)'
            }
            return val.toFixed(4)
          }
        }
      }
    }

    const getResourceLevel = (peoplePerAED) => {
      if (!peoplePerAED) return 'N/A'
      if (peoplePerAED < 1000) return '優良'
      if (peoplePerAED < 2000) return '良好'
      if (peoplePerAED < 3000) return '普通'
      return '待改善'
    }

    const getResourceBadge = (peoplePerAED) => {
      if (!peoplePerAED) return 'badge'
      if (peoplePerAED < 1000) return 'badge badge-low'
      if (peoplePerAED < 2000) return 'badge badge-low'
      if (peoplePerAED < 3000) return 'badge badge-medium'
      return 'badge badge-high'
    }

    const initAEDMap = async () => {
      mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN

      const map = new mapboxgl.Map({
        container: aedMapContainer.value,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [121.5654, 25.0330],
        zoom: 10
      })

      map.on('load', async () => {
        try {
          const geoData = await loadGeoJSON('/source/clean/合併/town.geojson')
          const aedDetailData = detailedData.value

          const aedMap = {}
          aedDetailData.forEach(row => {
            const key = `${row['場所縣市']}-${row['場所區域']}`
            aedMap[key] = {
              count: row.aed_count || 0,
              peoplePerAED: row.people_per_aed || 0
            }
          })

          geoData.features.forEach(feature => {
            const county = feature.properties.COUNTY
            const town = feature.properties.TOWN
            const key = `${county}-${town}`
            const data = aedMap[key] || { count: 0, peoplePerAED: 0 }
            feature.properties.aed_count = data.count
            feature.properties.people_per_aed = data.peoplePerAED
          })

          map.addSource('aed-districts', {
            type: 'geojson',
            data: geoData
          })

          map.addLayer({
            id: 'aed-districts-fill',
            type: 'fill',
            source: 'aed-districts',
            paint: {
              'fill-color': [
                'interpolate',
                ['linear'],
                ['get', 'people_per_aed'],
                0, '#34d399',
                1000, '#60a5fa',
                2000, '#fbbf24',
                4000, '#f87171'
              ],
              'fill-opacity': 0.7
            }
          })

          map.addLayer({
            id: 'aed-districts-outline',
            type: 'line',
            source: 'aed-districts',
            paint: {
              'line-color': '#475569',
              'line-width': 1
            }
          })

          map.on('click', 'aed-districts-fill', (e) => {
            const props = e.features[0].properties
            new mapboxgl.Popup()
              .setLngLat(e.lngLat)
              .setHTML(`
                <div style="color: #1e293b; padding: 5px;">
                  <strong>${props.COUNTY} ${props.TOWN}</strong><br>
                  AED 數量: ${props.aed_count || 0}<br>
                  人口數: ${props.P_CNT?.toLocaleString() || 'N/A'}<br>
                  每台服務人數: ${props.people_per_aed?.toLocaleString() || 'N/A'}
                </div>
              `)
              .addTo(map)
          })

          map.on('mouseenter', 'aed-districts-fill', () => {
            map.getCanvas().style.cursor = 'pointer'
          })

          map.on('mouseleave', 'aed-districts-fill', () => {
            map.getCanvas().style.cursor = ''
          })

        } catch (error) {
          console.error('Error loading AED map:', error)
        }
      })
    }

    onMounted(async () => {
      try {
        aedData.value = await loadCSV('/source/component_ready/aed_count_by_region.csv')
        detailedData.value = await loadCSV('/source/component_ready/people_per_aed_spatial_dispersion.csv')

        // Load spatial metrics data from topic files
        const taipeiMetrics = await loadCSV('/source/topic/taipei/topic1-2__City__regional_discrete_count(AED).csv')
        const newTaipeiMetrics = await loadCSV('/source/topic/newtaipeis/topic1-2__City__regional_discrete_count(AED).csv')
        spatialMetricsData.value = [...taipeiMetrics, ...newTaipeiMetrics]

        initAEDMap()
      } catch (error) {
        console.error('Error loading AED data:', error)
      }
    })

    return {
      aedMapContainer,
      selectedCity,
      filteredStats,
      filteredTableData,
      aedCountSeries,
      aedCountChartOptions,
      peoplePerAEDSeries,
      peoplePerAEDChartOptions,
      dispersionSeries,
      dispersionChartOptions,
      spatialMetricsSeries,
      spatialMetricsChartOptions,
      getResourceLevel,
      getResourceBadge
    }
  }
}
</script>
