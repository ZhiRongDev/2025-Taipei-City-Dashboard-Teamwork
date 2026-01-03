<template>
  <div class="topic2">
    <div class="card">
      <h2>Topic 2: 避難所人均面積分析</h2>
      <p style="color: #94a3b8; line-height: 1.8;">
        將防空避難設施進行空間與容量交叉評估，包括設施面積、總容納人數與人均收容空間，
        以矩形圖形式直觀呈現，協助判斷哪些地區設施壓力較高、分布較擁擠。
      </p>
    </div>

    <!-- Section Selector -->
    <div class="filter-bar">
      <div class="filter-group">
        <label>選擇視角：</label>
        <select v-model="selectedSection">
          <option value="taipei">台北市 (Taipei)</option>
          <option value="newtaipei">新北市 (New Taipei)</option>
          <option value="comparison">雙北比較 (Comparison)</option>
        </select>
      </div>
    </div>

    <!-- Statistics Summary -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">總容納人數</div>
        <div class="stat-value">{{ currentStats.totalCapacity.toLocaleString() }}<span class="stat-unit">人</span></div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">總收容所面積</div>
        <div class="stat-value">{{ currentStats.totalArea.toLocaleString() }}<span class="stat-unit">m²</span></div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-label">平均每人可分配面積</div>
        <div class="stat-value">{{ currentStats.avgAreaPerPerson.toFixed(2) }}<span class="stat-unit">m²</span></div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">最佳配置區</div>
        <div class="stat-value" style="font-size: 1.3rem;">{{ currentStats.topDistrict }}</div>
      </div>
    </div>

    <!-- Taipei Section -->
    <div v-if="selectedSection === 'taipei'" class="section-content">
      <h3 class="section-title">台北市避難所人均面積分析</h3>

      <!-- Map Visualization -->
      <div class="card">
        <h3>地圖視覺化 - 各行政區人均收容所面積</h3>
        <div ref="taipeiMapContainer" class="map-container"></div>
      </div>

      <!-- Charts -->
      <div class="grid grid-2">
        <div class="card">
          <h3>各行政區容納人數</h3>
          <apexchart
            type="bar"
            height="400"
            :options="taipeiCapacityChartOptions"
            :series="taipeiCapacitySeries"
          ></apexchart>
        </div>

        <div class="card">
          <h3>每人可分配收容所面積</h3>
          <apexchart
            type="bar"
            height="400"
            :options="taipeiAreaPerPersonChartOptions"
            :series="taipeiAreaPerPersonSeries"
          ></apexchart>
        </div>
      </div>

      <!-- Treemap -->
      <div class="card">
        <h3>收容所面積分布矩形樹狀圖</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          矩形大小代表收容所總面積，顏色深淺代表每人可分配面積（顏色越深表示每人可分配空間越大）
        </p>
        <apexchart
          type="treemap"
          height="500"
          :options="taipeiTreemapOptions"
          :series="taipeiTreemapSeries"
        ></apexchart>
      </div>

      <!-- Scatter Plot -->
      <div class="card">
        <h3>容納人數 vs 每萬人可分配面積</h3>
        <apexchart
          type="scatter"
          height="450"
          :options="taipeiScatterOptions"
          :series="taipeiScatterSeries"
        ></apexchart>
      </div>
    </div>

    <!-- New Taipei Section -->
    <div v-if="selectedSection === 'newtaipei'" class="section-content">
      <h3 class="section-title">新北市避難所人均面積分析</h3>

      <!-- Map Visualization -->
      <div class="card">
        <h3>地圖視覺化 - 各行政區人均收容所面積</h3>
        <div ref="newtaipeiMapContainer" class="map-container"></div>
      </div>

      <!-- Charts -->
      <div class="grid grid-2">
        <div class="card">
          <h3>各行政區容納人數</h3>
          <apexchart
            type="bar"
            height="400"
            :options="newtaipeiCapacityChartOptions"
            :series="newtaipeiCapacitySeries"
          ></apexchart>
        </div>

        <div class="card">
          <h3>每人可分配收容所面積</h3>
          <apexchart
            type="bar"
            height="400"
            :options="newtaipeiAreaPerPersonChartOptions"
            :series="newtaipeiAreaPerPersonSeries"
          ></apexchart>
        </div>
      </div>

      <!-- Treemap -->
      <div class="card">
        <h3>收容所面積分布矩形樹狀圖</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          矩形大小代表收容所總面積，顏色深淺代表每人可分配面積（顏色越深表示每人可分配空間越大）
        </p>
        <apexchart
          type="treemap"
          height="500"
          :options="newtaipeiTreemapOptions"
          :series="newtaipeiTreemapSeries"
        ></apexchart>
      </div>

      <!-- Scatter Plot -->
      <div class="card">
        <h3>容納人數 vs 每萬人可分配面積</h3>
        <apexchart
          type="scatter"
          height="450"
          :options="newtaipeiScatterOptions"
          :series="newtaipeiScatterSeries"
        ></apexchart>
      </div>
    </div>

    <!-- Comparison Section -->
    <div v-if="selectedSection === 'comparison'" class="section-content">
      <h3 class="section-title">雙北避難所人均面積比較</h3>

      <!-- City-level Comparison -->
      <div class="card">
        <h3>縣市層級比較</h3>
        <div class="grid grid-2">
          <apexchart
            type="bar"
            height="300"
            :options="cityComparisonCapacityOptions"
            :series="cityComparisonCapacitySeries"
          ></apexchart>
          <apexchart
            type="bar"
            height="300"
            :options="cityComparisonAreaOptions"
            :series="cityComparisonAreaSeries"
          ></apexchart>
        </div>
      </div>

      <!-- Combined Treemap -->
      <div class="card">
        <h3>雙北收容所面積分布總覽</h3>
        <apexchart
          type="treemap"
          height="600"
          :options="combinedTreemapOptions"
          :series="combinedTreemapSeries"
        ></apexchart>
      </div>

      <!-- District Ranking -->
      <div class="card">
        <h3>各行政區人均收容所面積排名 (Top 20)</h3>
        <apexchart
          type="bar"
          height="500"
          :options="districtRankingOptions"
          :series="districtRankingSeries"
        ></apexchart>
      </div>

      <!-- Comparison Summary -->
      <div class="card">
        <h3>分析摘要</h3>
        <div class="grid grid-2">
          <div class="comparison-summary">
            <h4 style="color: #60a5fa;">台北市</h4>
            <div v-html="taipeiSummary" style="color: #cbd5e1; line-height: 1.8;"></div>
          </div>
          <div class="comparison-summary">
            <h4 style="color: #34d399;">新北市</h4>
            <div v-html="newtaipeiSummary" style="color: #cbd5e1; line-height: 1.8;"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import mapboxgl from 'mapbox-gl'
import { loadCSV, loadGeoJSON } from '../utils/csvLoader'

export default {
  name: 'Topic2',
  setup() {
    const selectedSection = ref('taipei')
    const taipeiMapContainer = ref(null)
    const newtaipeiMapContainer = ref(null)

    const taipeiData = ref([])
    const newtaipeiData = ref([])

    // Current Statistics
    const currentStats = computed(() => {
      let data = []
      if (selectedSection.value === 'taipei') {
        data = taipeiData.value
      } else if (selectedSection.value === 'newtaipei') {
        data = newtaipeiData.value
      } else {
        data = [...taipeiData.value, ...newtaipeiData.value]
      }

      const totalCapacity = data.reduce((sum, row) => sum + (row['容納人數'] || 0), 0)
      const totalArea = data.reduce((sum, row) => sum + (row['收容所面積（平方公尺）'] || 0), 0)
      const avgAreaPerPerson = totalCapacity > 0 ? totalArea / totalCapacity : 0

      const topDistrictData = data.reduce((max, row) =>
        (row['每人可分配收容所面積（平方公尺）'] || 0) > (max['每人可分配收容所面積（平方公尺）'] || 0) ? row : max,
        data[0] || {}
      )
      const topDistrict = topDistrictData ? `${topDistrictData.Town || 'N/A'}` : 'N/A'

      return { totalCapacity, totalArea, avgAreaPerPerson, topDistrict }
    })

    // Taipei Charts
    const taipeiCapacitySeries = computed(() => [{
      name: '容納人數',
      data: taipeiData.value.map(row => row['容納人數'] || 0)
    }])

    const taipeiCapacityChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: taipeiData.value.map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const taipeiAreaPerPersonSeries = computed(() => [{
      name: '每人可分配面積',
      data: taipeiData.value.map(row => row['每人可分配收容所面積（平方公尺）'] || 0)
    }])

    const taipeiAreaPerPersonChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: taipeiData.value.map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const taipeiTreemapSeries = computed(() => [{
      data: taipeiData.value.map(row => ({
        x: row.Town,
        y: row['收容所面積（平方公尺）'] || 0
      }))
    }])

    const taipeiTreemapOptions = {
      chart: { type: 'treemap', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      plotOptions: {
        treemap: {
          enableShades: true,
          shadeIntensity: 0.5,
          reverseNegativeShade: true,
          colorScale: {
            ranges: [
              { from: 0, to: 0.05, color: '#f87171', name: '低' },
              { from: 0.05, to: 0.1, color: '#fbbf24', name: '中' },
              { from: 0.1, to: 0.2, color: '#34d399', name: '高' },
              { from: 0.2, to: 10, color: '#60a5fa', name: '優' }
            ]
          }
        }
      },
      dataLabels: {
        enabled: true,
        style: { fontSize: '12px', colors: ['#fff'] },
        formatter: (text, op) => [text, op.value.toLocaleString() + ' m²']
      }
    }

    const taipeiScatterSeries = computed(() => [{
      name: '台北市各區',
      data: taipeiData.value.map(row => ({
        x: row['容納人數'] || 0,
        y: row['每萬人可分配收容所面積（平方公尺）'] || 0
      }))
    }])

    const taipeiScatterOptions = {
      chart: { type: 'scatter', background: 'transparent', toolbar: { show: true }, zoom: { enabled: true } },
      theme: { mode: 'dark' },
      xaxis: {
        title: { text: '容納人數', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        title: { text: '每萬人可分配面積 (m²)', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#60a5fa'],
      markers: { size: 6 },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    // New Taipei Charts
    const newtaipeiCapacitySeries = computed(() => [{
      name: '容納人數',
      data: newtaipeiData.value.map(row => row['容納人數'] || 0)
    }])

    const newtaipeiCapacityChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: newtaipeiData.value.map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const newtaipeiAreaPerPersonSeries = computed(() => [{
      name: '每人可分配面積',
      data: newtaipeiData.value.map(row => row['每人可分配收容所面積（平方公尺）'] || 0)
    }])

    const newtaipeiAreaPerPersonChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: newtaipeiData.value.map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const newtaipeiTreemapSeries = computed(() => [{
      data: newtaipeiData.value.map(row => ({
        x: row.Town,
        y: row['收容所面積（平方公尺）'] || 0
      }))
    }])

    const newtaipeiTreemapOptions = {
      chart: { type: 'treemap', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      plotOptions: {
        treemap: {
          enableShades: true,
          shadeIntensity: 0.5,
          reverseNegativeShade: true,
          colorScale: {
            ranges: [
              { from: 0, to: 0.05, color: '#f87171', name: '低' },
              { from: 0.05, to: 0.1, color: '#fbbf24', name: '中' },
              { from: 0.1, to: 0.2, color: '#34d399', name: '高' },
              { from: 0.2, to: 10, color: '#60a5fa', name: '優' }
            ]
          }
        }
      },
      dataLabels: {
        enabled: true,
        style: { fontSize: '12px', colors: ['#fff'] },
        formatter: (text, op) => [text, op.value.toLocaleString() + ' m²']
      }
    }

    const newtaipeiScatterSeries = computed(() => [{
      name: '新北市各區',
      data: newtaipeiData.value.map(row => ({
        x: row['容納人數'] || 0,
        y: row['每萬人可分配收容所面積（平方公尺）'] || 0
      }))
    }])

    const newtaipeiScatterOptions = {
      chart: { type: 'scatter', background: 'transparent', toolbar: { show: true }, zoom: { enabled: true } },
      theme: { mode: 'dark' },
      xaxis: {
        title: { text: '容納人數', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        title: { text: '每萬人可分配面積 (m²)', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#34d399'],
      markers: { size: 6 },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    // Comparison Charts
    const cityComparisonCapacitySeries = computed(() => {
      const taipeiTotal = taipeiData.value.reduce((sum, row) => sum + (row['容納人數'] || 0), 0)
      const newtaipeiTotal = newtaipeiData.value.reduce((sum, row) => sum + (row['容納人數'] || 0), 0)

      return [{
        name: '總容納人數',
        data: [taipeiTotal, newtaipeiTotal]
      }]
    })

    const cityComparisonCapacityOptions = {
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      title: { text: '總容納人數比較', style: { color: '#94a3b8' } },
      xaxis: {
        categories: ['台北市', '新北市'],
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      plotOptions: { bar: { borderRadius: 4, columnWidth: '50%' } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    const cityComparisonAreaSeries = computed(() => {
      const taipeiArea = taipeiData.value.reduce((sum, row) => sum + (row['收容所面積（平方公尺）'] || 0), 0)
      const newtaipeiArea = newtaipeiData.value.reduce((sum, row) => sum + (row['收容所面積（平方公尺）'] || 0), 0)

      return [{
        name: '總收容所面積',
        data: [taipeiArea, newtaipeiArea]
      }]
    })

    const cityComparisonAreaOptions = {
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      title: { text: '總收容所面積比較', style: { color: '#94a3b8' } },
      xaxis: {
        categories: ['台北市', '新北市'],
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#34d399'],
      plotOptions: { bar: { borderRadius: 4, columnWidth: '50%' } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    const combinedTreemapSeries = computed(() => [{
      data: [
        ...taipeiData.value.map(row => ({
          x: `台北-${row.Town}`,
          y: row['收容所面積（平方公尺）'] || 0
        })),
        ...newtaipeiData.value.map(row => ({
          x: `新北-${row.Town}`,
          y: row['收容所面積（平方公尺）'] || 0
        }))
      ]
    }])

    const combinedTreemapOptions = {
      chart: { type: 'treemap', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      plotOptions: {
        treemap: {
          enableShades: true,
          shadeIntensity: 0.5,
          colorScale: {
            ranges: [
              { from: 0, to: 50000, color: '#f87171' },
              { from: 50000, to: 150000, color: '#fbbf24' },
              { from: 150000, to: 300000, color: '#34d399' },
              { from: 300000, to: 1000000, color: '#60a5fa' }
            ]
          }
        }
      },
      dataLabels: {
        enabled: true,
        style: { fontSize: '11px', colors: ['#fff'] },
        formatter: (text, op) => [text, op.value.toLocaleString() + ' m²']
      }
    }

    const districtRankingSeries = computed(() => {
      const allDistricts = [
        ...taipeiData.value.map(d => ({ ...d, city: '台北市' })),
        ...newtaipeiData.value.map(d => ({ ...d, city: '新北市' }))
      ].sort((a, b) => (b['每人可分配收容所面積（平方公尺）'] || 0) - (a['每人可分配收容所面積（平方公尺）'] || 0))
        .slice(0, 20)

      return [{
        name: '每人可分配面積',
        data: allDistricts.map(d => d['每人可分配收容所面積（平方公尺）'] || 0)
      }]
    })

    const districtRankingOptions = computed(() => {
      const allDistricts = [
        ...taipeiData.value.map(d => ({ ...d, city: '台北市' })),
        ...newtaipeiData.value.map(d => ({ ...d, city: '新北市' }))
      ].sort((a, b) => (b['每人可分配收容所面積（平方公尺）'] || 0) - (a['每人可分配收容所面積（平方公尺）'] || 0))
        .slice(0, 20)

      return {
        chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
        theme: { mode: 'dark' },
        xaxis: {
          categories: allDistricts.map(d => `${d.city} ${d.Town}`),
          labels: { style: { colors: '#94a3b8' }, rotate: -45 }
        },
        yaxis: { labels: { style: { colors: '#94a3b8' } } },
        colors: ['#fbbf24'],
        dataLabels: { enabled: false },
        plotOptions: { bar: { borderRadius: 4 } },
        grid: { borderColor: '#334155', strokeDashArray: 3 }
      }
    })

    const taipeiSummary = computed(() => {
      const totalCapacity = taipeiData.value.reduce((sum, row) => sum + (row['容納人數'] || 0), 0)
      const totalArea = taipeiData.value.reduce((sum, row) => sum + (row['收容所面積（平方公尺）'] || 0), 0)
      const avgAreaPerPerson = totalCapacity > 0 ? (totalArea / totalCapacity).toFixed(3) : 0

      return `
        <ul style="margin-left: 20px;">
          <li>總容納人數: ${totalCapacity.toLocaleString()}</li>
          <li>總收容所面積: ${totalArea.toLocaleString()} m²</li>
          <li>平均每人可分配面積: ${avgAreaPerPerson} m²</li>
          <li>行政區數: ${taipeiData.value.length}</li>
        </ul>
      `
    })

    const newtaipeiSummary = computed(() => {
      const totalCapacity = newtaipeiData.value.reduce((sum, row) => sum + (row['容納人數'] || 0), 0)
      const totalArea = newtaipeiData.value.reduce((sum, row) => sum + (row['收容所面積（平方公尺）'] || 0), 0)
      const avgAreaPerPerson = totalCapacity > 0 ? (totalArea / totalCapacity).toFixed(3) : 0

      return `
        <ul style="margin-left: 20px;">
          <li>總容納人數: ${totalCapacity.toLocaleString()}</li>
          <li>總收容所面積: ${totalArea.toLocaleString()} m²</li>
          <li>平均每人可分配面積: ${avgAreaPerPerson} m²</li>
          <li>行政區數: ${newtaipeiData.value.length}</li>
        </ul>
      `
    })

    // Map initialization
    const initTaipeiMap = async () => {
      if (!taipeiMapContainer.value) return

      mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN

      const map = new mapboxgl.Map({
        container: taipeiMapContainer.value,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [121.5654, 25.0330],
        zoom: 10.5
      })

      map.on('load', async () => {
        try {
          const geoData = await loadGeoJSON('/source/clean/台北/town_taipei.geojson')

          const shelterMap = {}
          taipeiData.value.forEach(row => {
            shelterMap[row.Town] = {
              capacity: row['容納人數'] || 0,
              areaPerPerson: row['每人可分配收容所面積（平方公尺）'] || 0
            }
          })

          geoData.features.forEach(feature => {
            const town = feature.properties.TOWN
            const data = shelterMap[town] || { capacity: 0, areaPerPerson: 0 }
            feature.properties.shelter_capacity = data.capacity
            feature.properties.area_per_person = data.areaPerPerson
          })

          map.addSource('taipei-districts', {
            type: 'geojson',
            data: geoData
          })

          map.addLayer({
            id: 'taipei-fill',
            type: 'fill',
            source: 'taipei-districts',
            paint: {
              'fill-color': [
                'interpolate',
                ['linear'],
                ['get', 'area_per_person'],
                0, '#f87171',
                0.05, '#fbbf24',
                0.1, '#34d399',
                0.2, '#60a5fa'
              ],
              'fill-opacity': 0.7
            }
          })

          map.addLayer({
            id: 'taipei-outline',
            type: 'line',
            source: 'taipei-districts',
            paint: {
              'line-color': '#475569',
              'line-width': 1
            }
          })

          map.on('click', 'taipei-fill', (e) => {
            const props = e.features[0].properties
            new mapboxgl.Popup()
              .setLngLat(e.lngLat)
              .setHTML(`
                <div style="color: #1e293b; padding: 5px;">
                  <strong>${props.TOWN}</strong><br>
                  容納人數: ${props.shelter_capacity?.toLocaleString() || 0}<br>
                  每人可分配面積: ${props.area_per_person?.toFixed(3) || 0} m²
                </div>
              `)
              .addTo(map)
          })

          map.on('mouseenter', 'taipei-fill', () => {
            map.getCanvas().style.cursor = 'pointer'
          })

          map.on('mouseleave', 'taipei-fill', () => {
            map.getCanvas().style.cursor = ''
          })

        } catch (error) {
          console.error('Error loading Taipei map:', error)
        }
      })
    }

    const initNewtaipeiMap = async () => {
      if (!newtaipeiMapContainer.value) return

      mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN

      const map = new mapboxgl.Map({
        container: newtaipeiMapContainer.value,
        style: 'mapbox://styles/mapbox/dark-v11',
        center: [121.4491, 25.0120],
        zoom: 9.5
      })

      map.on('load', async () => {
        try {
          const geoData = await loadGeoJSON('/source/clean/新北/town_newtaipei.geojson')

          const shelterMap = {}
          newtaipeiData.value.forEach(row => {
            shelterMap[row.Town] = {
              capacity: row['容納人數'] || 0,
              areaPerPerson: row['每人可分配收容所面積（平方公尺）'] || 0
            }
          })

          geoData.features.forEach(feature => {
            const town = feature.properties.TOWN
            const data = shelterMap[town] || { capacity: 0, areaPerPerson: 0 }
            feature.properties.shelter_capacity = data.capacity
            feature.properties.area_per_person = data.areaPerPerson
          })

          map.addSource('newtaipei-districts', {
            type: 'geojson',
            data: geoData
          })

          map.addLayer({
            id: 'newtaipei-fill',
            type: 'fill',
            source: 'newtaipei-districts',
            paint: {
              'fill-color': [
                'interpolate',
                ['linear'],
                ['get', 'area_per_person'],
                0, '#f87171',
                0.05, '#fbbf24',
                0.1, '#34d399',
                0.2, '#60a5fa'
              ],
              'fill-opacity': 0.7
            }
          })

          map.addLayer({
            id: 'newtaipei-outline',
            type: 'line',
            source: 'newtaipei-districts',
            paint: {
              'line-color': '#475569',
              'line-width': 1
            }
          })

          map.on('click', 'newtaipei-fill', (e) => {
            const props = e.features[0].properties
            new mapboxgl.Popup()
              .setLngLat(e.lngLat)
              .setHTML(`
                <div style="color: #1e293b; padding: 5px;">
                  <strong>${props.TOWN}</strong><br>
                  容納人數: ${props.shelter_capacity?.toLocaleString() || 0}<br>
                  每人可分配面積: ${props.area_per_person?.toFixed(3) || 0} m²
                </div>
              `)
              .addTo(map)
          })

          map.on('mouseenter', 'newtaipei-fill', () => {
            map.getCanvas().style.cursor = 'pointer'
          })

          map.on('mouseleave', 'newtaipei-fill', () => {
            map.getCanvas().style.cursor = ''
          })

        } catch (error) {
          console.error('Error loading New Taipei map:', error)
        }
      })
    }

    // Load data
    const loadData = async () => {
      try {
        taipeiData.value = await loadCSV('/source/topic/taipei/topic2-1__Town__asylum__pol_land_rate.csv')
        newtaipeiData.value = await loadCSV('/source/topic/newtaipeis/topic2-1__Town__asylum__pol_land_rate.csv')
      } catch (error) {
        console.error('Error loading Topic 2 data:', error)
      }
    }

    // Watch for section changes
    watch(selectedSection, (newVal) => {
      setTimeout(() => {
        if (newVal === 'taipei') {
          initTaipeiMap()
        } else if (newVal === 'newtaipei') {
          initNewtaipeiMap()
        }
      }, 100)
    })

    onMounted(async () => {
      await loadData()
      setTimeout(() => {
        initTaipeiMap()
      }, 100)
    })

    return {
      selectedSection,
      taipeiMapContainer,
      newtaipeiMapContainer,
      currentStats,
      taipeiCapacitySeries,
      taipeiCapacityChartOptions,
      taipeiAreaPerPersonSeries,
      taipeiAreaPerPersonChartOptions,
      taipeiTreemapSeries,
      taipeiTreemapOptions,
      taipeiScatterSeries,
      taipeiScatterOptions,
      newtaipeiCapacitySeries,
      newtaipeiCapacityChartOptions,
      newtaipeiAreaPerPersonSeries,
      newtaipeiAreaPerPersonChartOptions,
      newtaipeiTreemapSeries,
      newtaipeiTreemapOptions,
      newtaipeiScatterSeries,
      newtaipeiScatterOptions,
      cityComparisonCapacitySeries,
      cityComparisonCapacityOptions,
      cityComparisonAreaSeries,
      cityComparisonAreaOptions,
      combinedTreemapSeries,
      combinedTreemapOptions,
      districtRankingSeries,
      districtRankingOptions,
      taipeiSummary,
      newtaipeiSummary
    }
  }
}
</script>

<style scoped>
.section-title {
  color: #60a5fa;
  font-size: 1.5rem;
  margin: 24px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #334155;
}

.comparison-summary {
  padding: 20px;
  background: rgba(51, 65, 85, 0.3);
  border-radius: 8px;
  border: 1px solid #334155;
}

.comparison-summary h4 {
  margin-top: 0;
}
</style>
