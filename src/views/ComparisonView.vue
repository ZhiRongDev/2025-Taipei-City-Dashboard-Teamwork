<template>
  <div class="comparison-view">
    <div class="card">
      <h2>雙北防災資源比較 Taipei vs New Taipei Comparison</h2>
      <p style="color: #94a3b8;">
        台北市與新北市防災資源全面比較分析
      </p>
    </div>

    <div class="grid grid-2">
      <div class="stat-card" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
        <div class="stat-label" style="color: #dbeafe;">台北市</div>
        <div class="stat-value">{{ taipeiStats.districts }}<span class="stat-unit">個行政區</span></div>
        <div style="color: #dbeafe; font-size: 0.9rem; margin-top: 8px;">
          人口: {{ taipeiStats.population.toLocaleString() }}
        </div>
      </div>
      <div class="stat-card" style="background: linear-gradient(135deg, #34d399 0%, #10b981 100%);">
        <div class="stat-label" style="color: #d1fae5;">新北市</div>
        <div class="stat-value">{{ newTaipeiStats.districts }}<span class="stat-unit">個行政區</span></div>
        <div style="color: #d1fae5; font-size: 0.9rem; margin-top: 8px;">
          人口: {{ newTaipeiStats.population.toLocaleString() }}
        </div>
      </div>
    </div>

    <div class="card">
      <h3>防災資源總數比較</h3>
      <apexchart
        type="bar"
        height="400"
        :options="resourceComparisonChartOptions"
        :series="resourceComparisonSeries"
      ></apexchart>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>AED 人均比較</h3>
        <apexchart
          type="bar"
          height="350"
          :options="aedPerCapitaChartOptions"
          :series="aedPerCapitaSeries"
        ></apexchart>
      </div>

      <div class="card">
        <h3>避難收容處所比較</h3>
        <apexchart
          type="bar"
          height="350"
          :options="shelterComparisonChartOptions"
          :series="shelterComparisonSeries"
        ></apexchart>
      </div>
    </div>

    <div class="card">
      <h3>空間離散度比較 (Spatial Dispersion)</h3>
      <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
        比較兩市 AED 在各行政區的空間分散程度
      </p>
      <apexchart
        type="boxPlot"
        height="400"
        :options="dispersionBoxPlotOptions"
        :series="dispersionBoxPlotSeries"
      ></apexchart>
    </div>

    <div class="card">
      <h3>人口 vs AED 數量散點圖</h3>
      <apexchart
        type="scatter"
        height="450"
        :options="populationAEDScatterOptions"
        :series="populationAEDScatterSeries"
      ></apexchart>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <h3>台北市 Top 10 AED 配置區</h3>
        <apexchart
          type="bar"
          height="400"
          :options="taipeiTop10ChartOptions"
          :series="taipeiTop10Series"
        ></apexchart>
      </div>

      <div class="card">
        <h3>新北市 Top 10 AED 配置區</h3>
        <apexchart
          type="bar"
          height="400"
          :options="newTaipeiTop10ChartOptions"
          :series="newTaipeiTop10Series"
        ></apexchart>
      </div>
    </div>

    <div class="card">
      <h3>雙北各資源類型分布雷達圖</h3>
      <apexchart
        type="radar"
        height="500"
        :options="resourceRadarOptions"
        :series="resourceRadarSeries"
      ></apexchart>
    </div>

    <div class="card">
      <h3>詳細統計比較表</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>項目</th>
              <th>台北市</th>
              <th>新北市</th>
              <th>差異</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>行政區數</strong></td>
              <td>{{ taipeiStats.districts }}</td>
              <td>{{ newTaipeiStats.districts }}</td>
              <td>{{ newTaipeiStats.districts - taipeiStats.districts }}</td>
            </tr>
            <tr>
              <td><strong>總人口數</strong></td>
              <td>{{ taipeiStats.population.toLocaleString() }}</td>
              <td>{{ newTaipeiStats.population.toLocaleString() }}</td>
              <td>{{ (newTaipeiStats.population - taipeiStats.population).toLocaleString() }}</td>
            </tr>
            <tr>
              <td><strong>AED 總數</strong></td>
              <td>{{ taipeiStats.totalAED }}</td>
              <td>{{ newTaipeiStats.totalAED }}</td>
              <td>{{ newTaipeiStats.totalAED - taipeiStats.totalAED }}</td>
            </tr>
            <tr>
              <td><strong>平均每區 AED</strong></td>
              <td>{{ taipeiStats.avgAEDPerDistrict }}</td>
              <td>{{ newTaipeiStats.avgAEDPerDistrict }}</td>
              <td>{{ (newTaipeiStats.avgAEDPerDistrict - taipeiStats.avgAEDPerDistrict).toFixed(1) }}</td>
            </tr>
            <tr>
              <td><strong>每台 AED 服務人數</strong></td>
              <td>{{ taipeiStats.peoplePerAED }}</td>
              <td>{{ newTaipeiStats.peoplePerAED }}</td>
              <td>{{ newTaipeiStats.peoplePerAED - taipeiStats.peoplePerAED }}</td>
            </tr>
            <tr>
              <td><strong>避難收容處所總數</strong></td>
              <td>{{ taipeiStats.totalShelter }}</td>
              <td>{{ newTaipeiStats.totalShelter }}</td>
              <td>{{ newTaipeiStats.totalShelter - taipeiStats.totalShelter }}</td>
            </tr>
            <tr>
              <td><strong>平均空間離散度</strong></td>
              <td>{{ taipeiStats.avgDispersion }}</td>
              <td>{{ newTaipeiStats.avgDispersion }}</td>
              <td>{{ (newTaipeiStats.avgDispersion - taipeiStats.avgDispersion).toFixed(0) }}</td>
            </tr>
            <tr>
              <td><strong>空間熵 (Spatial Entropy)</strong></td>
              <td>{{ taipeiStats.spatialEntropy.toFixed(3) }}</td>
              <td>{{ newTaipeiStats.spatialEntropy.toFixed(3) }}</td>
              <td>{{ (newTaipeiStats.spatialEntropy - taipeiStats.spatialEntropy).toFixed(3) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { loadCSV } from '../utils/csvLoader'

export default {
  name: 'ComparisonView',
  setup() {
    const aedData = ref([])
    const detailedData = ref([])
    const disasterData = ref([])
    const cityMetricsData = ref([])

    const taipeiData = computed(() => aedData.value.filter(r => r['場所縣市'] === '臺北市'))
    const newTaipeiData = computed(() => aedData.value.filter(r => r['場所縣市'] === '新北市'))

    const taipeiDetailedData = computed(() => detailedData.value.filter(r => r['場所縣市'] === '臺北市'))
    const newTaipeiDetailedData = computed(() => detailedData.value.filter(r => r['場所縣市'] === '新北市'))

    const taipeiShelterData = computed(() => disasterData.value.filter(r => r.city === '臺北市'))
    const newTaipeiShelterData = computed(() => disasterData.value.filter(r => r.city === '新北市'))

    const taipeiStats = computed(() => {
      const data = taipeiData.value
      const detailedD = taipeiDetailedData.value
      const shelterD = taipeiShelterData.value
      const cityMetrics = cityMetricsData.value.find(r => r.City === '臺北市')

      return {
        districts: data.length,
        population: detailedD.reduce((sum, r) => sum + (r['人口數'] || 0), 0),
        totalAED: data.reduce((sum, r) => sum + (r.aed_count || 0), 0),
        avgAEDPerDistrict: data.length > 0 ? Math.round(data.reduce((sum, r) => sum + (r.aed_count || 0), 0) / data.length) : 0,
        peoplePerAED: detailedD.length > 0 ? Math.round(detailedD.reduce((sum, r) => sum + (r.people_per_aed || 0), 0) / detailedD.length) : 0,
        totalShelter: shelterD.reduce((sum, r) => sum + (r['任一災別避難地點數'] || 0), 0),
        avgDispersion: detailedD.length > 0 ? Math.round(detailedD.reduce((sum, r) => sum + (r.spatial_dispersion_projected || 0), 0) / detailedD.length) : 0,
        spatialEntropy: cityMetrics?.SpatialEntropy || 0
      }
    })

    const newTaipeiStats = computed(() => {
      const data = newTaipeiData.value
      const detailedD = newTaipeiDetailedData.value
      const shelterD = newTaipeiShelterData.value
      const cityMetrics = cityMetricsData.value.find(r => r.City === '新北市')

      return {
        districts: data.length,
        population: detailedD.reduce((sum, r) => sum + (r['人口數'] || 0), 0),
        totalAED: data.reduce((sum, r) => sum + (r.aed_count || 0), 0),
        avgAEDPerDistrict: data.length > 0 ? Math.round(data.reduce((sum, r) => sum + (r.aed_count || 0), 0) / data.length) : 0,
        peoplePerAED: detailedD.length > 0 ? Math.round(detailedD.reduce((sum, r) => sum + (r.people_per_aed || 0), 0) / detailedD.length) : 0,
        totalShelter: shelterD.reduce((sum, r) => sum + (r['任一災別避難地點數'] || 0), 0),
        avgDispersion: detailedD.length > 0 ? Math.round(detailedD.reduce((sum, r) => sum + (r.spatial_dispersion_projected || 0), 0) / detailedD.length) : 0,
        spatialEntropy: cityMetrics?.SpatialEntropy || 0
      }
    })

    const resourceComparisonSeries = computed(() => [
      {
        name: '台北市',
        data: [taipeiStats.value.totalAED, taipeiStats.value.totalShelter]
      },
      {
        name: '新北市',
        data: [newTaipeiStats.value.totalAED, newTaipeiStats.value.totalShelter]
      }
    ])

    const resourceComparisonChartOptions = {
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: ['AED 總數', '避難收容處所'],
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#3b82f6', '#34d399'],
      dataLabels: {
        enabled: true,
        style: { colors: ['#fff'] }
      },
      plotOptions: {
        bar: {
          borderRadius: 4,
          columnWidth: '60%'
        }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: {
        labels: { colors: '#94a3b8' }
      }
    }

    const aedPerCapitaSeries = computed(() => [
      {
        name: '每台 AED 服務人數',
        data: [
          { x: '台北市', y: taipeiStats.value.peoplePerAED },
          { x: '新北市', y: newTaipeiStats.value.peoplePerAED }
        ]
      }
    ])

    const aedPerCapitaChartOptions = {
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      plotOptions: {
        bar: {
          borderRadius: 4,
          distributed: true
        }
      },
      xaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#3b82f6', '#34d399'],
      dataLabels: {
        enabled: true,
        style: { colors: ['#fff'] }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: { show: false }
    }

    const shelterComparisonSeries = computed(() => [
      {
        name: '避難收容處所',
        data: [
          { x: '台北市', y: taipeiStats.value.totalShelter },
          { x: '新北市', y: newTaipeiStats.value.totalShelter }
        ]
      }
    ])

    const shelterComparisonChartOptions = {
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      plotOptions: {
        bar: {
          borderRadius: 4,
          distributed: true
        }
      },
      xaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#3b82f6', '#34d399'],
      dataLabels: {
        enabled: true,
        style: { colors: ['#fff'] }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: { show: false }
    }

    const dispersionBoxPlotSeries = computed(() => {
      const taipeiDispersion = taipeiDetailedData.value.map(r => r.spatial_dispersion_projected || 0)
      const newTaipeiDispersion = newTaipeiDetailedData.value.map(r => r.spatial_dispersion_projected || 0)

      return [
        {
          name: '台北市',
          type: 'boxPlot',
          data: [{
            x: '台北市',
            y: taipeiDispersion.sort((a, b) => a - b)
          }]
        },
        {
          name: '新北市',
          type: 'boxPlot',
          data: [{
            x: '新北市',
            y: newTaipeiDispersion.sort((a, b) => a - b)
          }]
        }
      ]
    })

    const dispersionBoxPlotOptions = {
      chart: {
        type: 'boxPlot',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      colors: ['#3b82f6', '#34d399'],
      plotOptions: {
        boxPlot: {
          colors: {
            upper: '#60a5fa',
            lower: '#34d399'
          }
        }
      },
      xaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        title: { text: '空間離散度', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      }
    }

    const populationAEDScatterSeries = computed(() => [
      {
        name: '台北市',
        data: taipeiDetailedData.value.map(r => ({
          x: r['人口數'] || 0,
          y: r.aed_count || 0
        }))
      },
      {
        name: '新北市',
        data: newTaipeiDetailedData.value.map(r => ({
          x: r['人口數'] || 0,
          y: r.aed_count || 0
        }))
      }
    ])

    const populationAEDScatterOptions = {
      chart: {
        type: 'scatter',
        background: 'transparent',
        toolbar: { show: true },
        zoom: { enabled: true }
      },
      theme: { mode: 'dark' },
      xaxis: {
        title: { text: '人口數', style: { color: '#94a3b8' } },
        labels: {
          style: { colors: '#94a3b8' },
          formatter: (val) => val.toLocaleString()
        }
      },
      yaxis: {
        title: { text: 'AED 數量', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#3b82f6', '#34d399'],
      markers: { size: 8 },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      },
      legend: {
        labels: { colors: '#94a3b8' }
      }
    }

    const taipeiTop10Series = computed(() => [{
      name: 'AED 數量',
      data: taipeiData.value.slice().sort((a, b) => b.aed_count - a.aed_count).slice(0, 10).map(r => r.aed_count)
    }])

    const taipeiTop10ChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: taipeiData.value.slice().sort((a, b) => b.aed_count - a.aed_count).slice(0, 10).map(r => r['場所區域']),
        labels: {
          style: { colors: '#94a3b8' },
          rotate: -45
        }
      },
      yaxis: {
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#3b82f6'],
      dataLabels: { enabled: false },
      plotOptions: {
        bar: { borderRadius: 4 }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      }
    }))

    const newTaipeiTop10Series = computed(() => [{
      name: 'AED 數量',
      data: newTaipeiData.value.slice().sort((a, b) => b.aed_count - a.aed_count).slice(0, 10).map(r => r.aed_count)
    }])

    const newTaipeiTop10ChartOptions = computed(() => ({
      chart: {
        type: 'bar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: newTaipeiData.value.slice().sort((a, b) => b.aed_count - a.aed_count).slice(0, 10).map(r => r['場所區域']),
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
        bar: { borderRadius: 4 }
      },
      grid: {
        borderColor: '#334155',
        strokeDashArray: 3
      }
    }))

    const resourceRadarSeries = computed(() => [
      {
        name: '台北市',
        data: [
          taipeiStats.value.totalAED / 10,
          taipeiStats.value.totalShelter,
          taipeiStats.value.avgAEDPerDistrict,
          100 - taipeiStats.value.peoplePerAED / 50,
          taipeiStats.value.avgDispersion / 50
        ]
      },
      {
        name: '新北市',
        data: [
          newTaipeiStats.value.totalAED / 10,
          newTaipeiStats.value.totalShelter,
          newTaipeiStats.value.avgAEDPerDistrict,
          100 - newTaipeiStats.value.peoplePerAED / 50,
          newTaipeiStats.value.avgDispersion / 50
        ]
      }
    ])

    const resourceRadarOptions = {
      chart: {
        type: 'radar',
        background: 'transparent',
        toolbar: { show: false }
      },
      theme: { mode: 'dark' },
      xaxis: {
        categories: ['AED 總數 (÷10)', '避難所總數', '平均每區 AED', '人均服務品質', '空間覆蓋度'],
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        show: true,
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#3b82f6', '#34d399'],
      stroke: { width: 2 },
      fill: { opacity: 0.3 },
      markers: { size: 5 },
      legend: {
        labels: { colors: '#94a3b8' }
      }
    }

    onMounted(async () => {
      try {
        aedData.value = await loadCSV('/source/component_ready/aed_count_by_region.csv')
        detailedData.value = await loadCSV('/source/component_ready/people_per_aed_spatial_dispersion.csv')
        disasterData.value = await loadCSV('/source/component_ready/disaster.csv')

        // 載入 City 級別的 AED 空間指標資料（包含 Dispersion 和 SpatialEntropy）
        const taipeiCityMetrics = await loadCSV('/source/topic/taipei/topic1-2__City__regional_discrete_count(AED).csv')
        const newTaipeiCityMetrics = await loadCSV('/source/topic/newtaipeis/topic1-2__City__regional_discrete_count(AED).csv')
        cityMetricsData.value = [...taipeiCityMetrics, ...newTaipeiCityMetrics]
      } catch (error) {
        console.error('Error loading comparison data:', error)
      }
    })

    return {
      taipeiStats,
      newTaipeiStats,
      resourceComparisonSeries,
      resourceComparisonChartOptions,
      aedPerCapitaSeries,
      aedPerCapitaChartOptions,
      shelterComparisonSeries,
      shelterComparisonChartOptions,
      dispersionBoxPlotSeries,
      dispersionBoxPlotOptions,
      populationAEDScatterSeries,
      populationAEDScatterOptions,
      taipeiTop10Series,
      taipeiTop10ChartOptions,
      newTaipeiTop10Series,
      newTaipeiTop10ChartOptions,
      resourceRadarSeries,
      resourceRadarOptions
    }
  }
}
</script>
