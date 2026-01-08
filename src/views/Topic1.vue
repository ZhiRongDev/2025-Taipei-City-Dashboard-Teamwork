<template>
  <div class="topic1">
    <div class="card">
      <h2>Topic 1: 區域人口與防災資源比分析</h2>
      <p style="color: #94a3b8; line-height: 1.8;">
        結合鄉鎮市區人口統計與防災資源（包含防空疏散設施、避難收容處所、AED 及消防/警政據點）進行比對，
        針對數量、人均數量與地點離散度等指標，分析各區的防災資源密度。
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
      <div class="filter-group">
        <label>資源類型：</label>
        <select v-model="selectedResourceType">
          <option value="AED">AED</option>
          <option value="警消">警消單位</option>
          <option value="避難收容所">避難收容所</option>
          <option value="防空疏散地點">防空疏散地點</option>
        </select>
      </div>
    </div>

    <!-- Statistics Summary -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">資源總數</div>
        <div class="stat-value">{{ currentStats.total }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">平均每區資源數</div>
        <div class="stat-value">{{ currentStats.avgPerDistrict }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-label">平均每處服務人數</div>
        <div class="stat-value">{{ currentStats.avgPeoplePerResource }}<span class="stat-unit">人</span></div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">最高配置區</div>
        <div class="stat-value" style="font-size: 1.3rem;">{{ currentStats.topDistrict }}</div>
      </div>
    </div>

    <!-- Taipei Section -->
    <div v-if="selectedSection === 'taipei'" class="section-content">
      <h3 class="section-title">台北市 {{ selectedResourceType }} 分析</h3>

      <!-- Map Visualization -->
      <div class="card">
        <h3>地圖視覺化 - 各行政區 {{ selectedResourceType }} 分布</h3>
        <div ref="taipeiMapContainer" class="map-container"></div>
      </div>

      <!-- Charts -->
      <div class="grid grid-2">
        <div class="card">
          <h3>各行政區 {{ selectedResourceType }} 數量</h3>
          <p style="color: #94a3b8; margin-bottom: 12px; font-size: 0.95rem;">
            <strong style="color: #60a5fa;">數據分析：</strong>
            <span v-if="selectedResourceType === 'AED'">
              大安區擁有最多 AED（327台），其次為中山區（306台）與中正區（274台），
              這三區合計佔台北市 AED 總數約 35%，反映商業與行政中心的設備配置較為密集。
            </span>
            <span v-else-if="selectedResourceType === '避難收容所'">
              文山區擁有最多避難收容所（52處），其次為士林區（40處）、北投區與內湖區（各37處），
              這些區域面積較大，提供較多收容場所。
            </span>
            <span v-else>
              各行政區資源數量分布反映當地人口密度與地理特性，
              核心都會區域通常配置較多防災資源以因應高人口密度需求。
            </span>
          </p>
          <apexchart
            type="bar"
            height="400"
            :options="taipeiCountChartOptions"
            :series="taipeiCountSeries"
          ></apexchart>
        </div>

        <div class="card">
          <h3>人均資源比 (人口數/資源數)</h3>
          <p style="color: #94a3b8; margin-bottom: 12px; font-size: 0.95rem;">
            <strong style="color: #34d399;">數據分析：</strong>
            此指標數值越低代表每項資源服務的人數越少，資源配置相對充裕。
            若數值過高，表示該區可能面臨資源不足的壓力，需要優先補強防災設施。
          </p>
          <apexchart
            type="bar"
            height="400"
            :options="taipeiPopRatioChartOptions"
            :series="taipeiPopRatioSeries"
          ></apexchart>
        </div>
      </div>

      <!-- Spatial Metrics -->
      <div class="card">
        <h3>離散度分析指標</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #60a5fa;">平均兩兩距離 (Dispersion):</strong> 計算各設施間的歐氏距離平均，反映地理上分散程度。
          數值越高表示設施分布越分散，覆蓋範圍越廣。<br>
          <strong style="color: #34d399;">空間熵 (Spatial Entropy):</strong> 透過網格分佈與資訊熵公式，分析設施分布的隨機性與集中性。
          數值越高表示分布越均勻，越低則表示資源集中於特定區域。
        </p>
        <div class="grid grid-2">
          <apexchart
            type="bar"
            height="350"
            :options="taipeiDispersionChartOptions"
            :series="taipeiDispersionSeries"
          ></apexchart>
          <apexchart
            type="bar"
            height="350"
            :options="taipeiEntropyChartOptions"
            :series="taipeiEntropySeries"
          ></apexchart>
        </div>
      </div>
    </div>

    <!-- New Taipei Section -->
    <div v-if="selectedSection === 'newtaipei'" class="section-content">
      <h3 class="section-title">新北市 {{ selectedResourceType }} 分析</h3>

      <!-- Map Visualization -->
      <div class="card">
        <h3>地圖視覺化 - 各行政區 {{ selectedResourceType }} 分布</h3>
        <div ref="newtaipeiMapContainer" class="map-container"></div>
      </div>

      <!-- Charts -->
      <div class="grid grid-2">
        <div class="card">
          <h3>各行政區 {{ selectedResourceType }} 數量</h3>
          <p style="color: #94a3b8; margin-bottom: 12px; font-size: 0.95rem;">
            <strong style="color: #60a5fa;">數據分析：</strong>
            <span v-if="selectedResourceType === 'AED'">
              板橋區擁有最多 AED（194台），其次為新莊區（165台）與新店區（119台），
              這三區為新北市人口最密集區域，AED 配置密度較高以因應緊急醫療需求。
            </span>
            <span v-else>
              資源數量與各區人口規模、都市發展程度密切相關，
              人口密集的核心都會區域配置較多防災資源。
            </span>
          </p>
          <apexchart
            type="bar"
            height="400"
            :options="newtaipeiCountChartOptions"
            :series="newtaipeiCountSeries"
          ></apexchart>
        </div>

        <div class="card">
          <h3>人均資源比 (人口數/資源數)</h3>
          <p style="color: #94a3b8; margin-bottom: 12px; font-size: 0.95rem;">
            <strong style="color: #34d399;">數據分析：</strong>
            人均資源比反映每項資源需服務的平均人數。新北市因幅員廣闊、人口分散，
            部分偏遠區域雖資源絕對數量較少，但人均比可能優於都會核心區。
          </p>
          <apexchart
            type="bar"
            height="400"
            :options="newtaipeiPopRatioChartOptions"
            :series="newtaipeiPopRatioSeries"
          ></apexchart>
        </div>
      </div>

      <!-- Spatial Metrics -->
      <div class="card">
        <h3>離散度分析指標</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #60a5fa;">平均兩兩距離 (Dispersion):</strong> 計算各設施間的歐氏距離平均，反映地理上分散程度。
          新北市因地理範圍較大，離散度指標通常高於台北市。<br>
          <strong style="color: #34d399;">空間熵 (Spatial Entropy):</strong> 透過網格分佈與資訊熵公式，分析設施分布的隨機性與集中性。
          數值越高表示資源分布越均勻。
        </p>
        <div class="grid grid-2">
          <apexchart
            type="bar"
            height="350"
            :options="newtaipeiDispersionChartOptions"
            :series="newtaipeiDispersionSeries"
          ></apexchart>
          <apexchart
            type="bar"
            height="350"
            :options="newtaipeiEntropyChartOptions"
            :series="newtaipeiEntropySeries"
          ></apexchart>
        </div>
      </div>
    </div>

    <!-- Comparison Section -->
    <div v-if="selectedSection === 'comparison'" class="section-content">
      <h3 class="section-title">雙北 {{ selectedResourceType }} 比較</h3>

      <!-- City-level Comparison -->
      <div class="card">
        <h3>縣市層級比較</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #60a5fa;">數據分析：</strong>
          雙北在防災資源總量上各有特色。台北市雖然面積較小，但因都市密度高、商業活動集中，
          人均資源配置相對較為充裕。新北市幅員廣闊，資源分布需兼顧都會核心與偏遠區域的平衡。
        </p>
        <div class="grid grid-2">
          <apexchart
            type="bar"
            height="300"
            :options="cityComparisonCountOptions"
            :series="cityComparisonCountSeries"
          ></apexchart>
          <apexchart
            type="bar"
            height="300"
            :options="cityComparisonMetricsOptions"
            :series="cityComparisonMetricsSeries"
          ></apexchart>
        </div>
      </div>

      <!-- Side-by-side District Comparison -->
      <div class="card">
        <h3>行政區橫向比較 - 資源數量排名</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #fbbf24;">數據分析：</strong>
          此圖呈現雙北資源數量前 20 名的行政區排名。台北市的大安區、中山區、中正區，
          以及新北市的板橋區、新莊區、新店區等核心都會區通常位居前列，
          反映這些區域在防災資源建設上的投入力度。
        </p>
        <apexchart
          type="bar"
          height="500"
          :options="districtComparisonOptions"
          :series="districtComparisonSeries"
        ></apexchart>
      </div>

      <!-- Spatial Metrics Comparison -->
      <div class="card">
        <h3>離散度指標比較</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #34d399;">數據分析：</strong>
          雷達圖呈現雙北在離散度、空間熵、人均資源比等多維度的比較。
          台北市通常在人均指標上表現較優，新北市則在空間分散度上數值較高，
          反映兩市在都市型態與資源配置策略上的差異。
        </p>
        <div class="grid grid-2">
          <apexchart
            type="radar"
            height="400"
            :options="spatialComparisonOptions"
            :series="spatialComparisonSeries"
          ></apexchart>
          <div class="comparison-summary">
            <h4 style="color: #60a5fa; margin-bottom: 16px;">分析摘要</h4>
            <div v-html="comparisonSummary" style="color: #cbd5e1; line-height: 1.8;"></div>
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
  name: 'Topic1',
  setup() {
    const selectedSection = ref('taipei')
    const selectedResourceType = ref('AED')

    const taipeiMapContainer = ref(null)
    const newtaipeiMapContainer = ref(null)

    const taipeiData = ref({
      AED: [],
      '警消': [],
      '避難收容所': [],
      '防空疏散地點': []
    })

    const newtaipeiData = ref({
      AED: [],
      '警消': [],
      '避難收容所': [],
      '防空疏散地點': []
    })

    const taipeiCityData = ref({})
    const newtaipeiCityData = ref({})

    // Current Statistics
    const currentStats = computed(() => {
      let data = []
      if (selectedSection.value === 'taipei') {
        data = taipeiData.value[selectedResourceType.value] || []
      } else if (selectedSection.value === 'newtaipei') {
        data = newtaipeiData.value[selectedResourceType.value] || []
      } else {
        data = [...(taipeiData.value[selectedResourceType.value] || []), ...(newtaipeiData.value[selectedResourceType.value] || [])]
      }

      const total = data.reduce((sum, row) => sum + (row.Count || 0), 0)
      const totalPop = data.reduce((sum, row) => sum + (row.population || 0), 0)
      const avgPerDistrict = data.length > 0 ? Math.round(total / data.length) : 0
      const avgPeoplePerResource = total > 0 ? Math.round(totalPop / total) : 0
      const topDistrictData = data.reduce((max, row) =>
        (row.Count || 0) > (max.Count || 0) ? row : max, data[0] || {})
      const topDistrict = topDistrictData ? `${topDistrictData.Town || 'N/A'}` : 'N/A'

      return { total, avgPerDistrict, avgPeoplePerResource, topDistrict }
    })

    // Taipei Charts
    const taipeiCountSeries = computed(() => {
      const data = taipeiData.value[selectedResourceType.value] || []
      return [{
        name: '資源數量',
        data: data.map(row => row.Count || 0)
      }]
    })

    const taipeiCountChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: (taipeiData.value[selectedResourceType.value] || []).map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const taipeiPopRatioSeries = computed(() => {
      const data = taipeiData.value[selectedResourceType.value] || []
      return [{
        name: '人口/資源數',
        data: data.map(row => row.population_per_count || 0)
      }]
    })

    const taipeiPopRatioChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: (taipeiData.value[selectedResourceType.value] || []).map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const taipeiDispersionSeries = computed(() => {
      const data = taipeiData.value[selectedResourceType.value] || []
      return [{
        name: '平均兩兩距離',
        data: data.map(row => (row.Dispersion || 0) * 1000) // Scale for visibility
      }]
    })

    const taipeiDispersionChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      title: { text: '平均兩兩距離 (Dispersion)', style: { color: '#94a3b8' } },
      xaxis: {
        categories: (taipeiData.value[selectedResourceType.value] || []).map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const taipeiEntropySeries = computed(() => {
      const data = taipeiData.value[selectedResourceType.value] || []
      return [{
        name: '空間熵',
        data: data.map(row => row.SpatialEntropy || 0)
      }]
    })

    const taipeiEntropyChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      title: { text: '空間熵 (Spatial Entropy)', style: { color: '#94a3b8' } },
      xaxis: {
        categories: (taipeiData.value[selectedResourceType.value] || []).map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    // New Taipei Charts (similar structure)
    const newtaipeiCountSeries = computed(() => {
      const data = newtaipeiData.value[selectedResourceType.value] || []
      return [{
        name: '資源數量',
        data: data.map(row => row.Count || 0)
      }]
    })

    const newtaipeiCountChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: (newtaipeiData.value[selectedResourceType.value] || []).map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const newtaipeiPopRatioSeries = computed(() => {
      const data = newtaipeiData.value[selectedResourceType.value] || []
      return [{
        name: '人口/資源數',
        data: data.map(row => row.population_per_count || 0)
      }]
    })

    const newtaipeiPopRatioChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: (newtaipeiData.value[selectedResourceType.value] || []).map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const newtaipeiDispersionSeries = computed(() => {
      const data = newtaipeiData.value[selectedResourceType.value] || []
      return [{
        name: '平均兩兩距離',
        data: data.map(row => (row.Dispersion || 0) * 1000)
      }]
    })

    const newtaipeiDispersionChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      title: { text: '平均兩兩距離 (Dispersion)', style: { color: '#94a3b8' } },
      xaxis: {
        categories: (newtaipeiData.value[selectedResourceType.value] || []).map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const newtaipeiEntropySeries = computed(() => {
      const data = newtaipeiData.value[selectedResourceType.value] || []
      return [{
        name: '空間熵',
        data: data.map(row => row.SpatialEntropy || 0)
      }]
    })

    const newtaipeiEntropyChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      title: { text: '空間熵 (Spatial Entropy)', style: { color: '#94a3b8' } },
      xaxis: {
        categories: (newtaipeiData.value[selectedResourceType.value] || []).map(row => row.Town),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    // Comparison Charts
    const cityComparisonCountSeries = computed(() => {
      const taipeiCity = taipeiCityData.value[selectedResourceType.value] || {}
      const newtaipeiCity = newtaipeiCityData.value[selectedResourceType.value] || {}

      return [{
        name: '總資源數',
        data: [taipeiCity.Count || 0, newtaipeiCity.Count || 0]
      }]
    })

    const cityComparisonCountOptions = {
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      title: { text: '總資源數比較', style: { color: '#94a3b8' } },
      xaxis: {
        categories: ['台北市', '新北市'],
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      plotOptions: { bar: { borderRadius: 4, columnWidth: '50%' } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    const cityComparisonMetricsSeries = computed(() => {
      const taipeiCity = taipeiCityData.value[selectedResourceType.value] || {}
      const newtaipeiCity = newtaipeiCityData.value[selectedResourceType.value] || {}

      return [
        {
          name: '平均兩兩距離',
          data: [(taipeiCity.Dispersion || 0) * 1000, (newtaipeiCity.Dispersion || 0) * 1000]
        },
        {
          name: '空間熵',
          data: [taipeiCity.SpatialEntropy || 0, newtaipeiCity.SpatialEntropy || 0]
        }
      ]
    })

    const cityComparisonMetricsOptions = {
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      title: { text: '空間指標比較', style: { color: '#94a3b8' } },
      xaxis: {
        categories: ['台北市', '新北市'],
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa', '#34d399'],
      plotOptions: { bar: { borderRadius: 4, columnWidth: '70%' } },
      legend: { labels: { colors: '#94a3b8' } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    const districtComparisonSeries = computed(() => {
      const taipeiDistricts = taipeiData.value[selectedResourceType.value] || []
      const newtaipeiDistricts = newtaipeiData.value[selectedResourceType.value] || []

      const allDistricts = [
        ...taipeiDistricts.map(d => ({ ...d, city: '台北市' })),
        ...newtaipeiDistricts.map(d => ({ ...d, city: '新北市' }))
      ].sort((a, b) => (b.Count || 0) - (a.Count || 0)).slice(0, 20)

      return [{
        name: '資源數量',
        data: allDistricts.map(d => d.Count || 0)
      }]
    })

    const districtComparisonOptions = computed(() => {
      const taipeiDistricts = taipeiData.value[selectedResourceType.value] || []
      const newtaipeiDistricts = newtaipeiData.value[selectedResourceType.value] || []

      const allDistricts = [
        ...taipeiDistricts.map(d => ({ ...d, city: '台北市' })),
        ...newtaipeiDistricts.map(d => ({ ...d, city: '新北市' }))
      ].sort((a, b) => (b.Count || 0) - (a.Count || 0)).slice(0, 20)

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

    const spatialComparisonSeries = computed(() => {
      const taipeiCity = taipeiCityData.value[selectedResourceType.value] || {}
      const newtaipeiCity = newtaipeiCityData.value[selectedResourceType.value] || {}

      return [
        {
          name: '台北市',
          data: [
            (taipeiCity.Dispersion || 0) * 1000,
            taipeiCity.SpatialEntropy || 0,
            taipeiCity.population_per_count || 0,
            taipeiCity.households_per_count || 0
          ]
        },
        {
          name: '新北市',
          data: [
            (newtaipeiCity.Dispersion || 0) * 1000,
            newtaipeiCity.SpatialEntropy || 0,
            newtaipeiCity.population_per_count || 0,
            newtaipeiCity.households_per_count || 0
          ]
        }
      ]
    })

    const spatialComparisonOptions = {
      chart: { type: 'radar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: ['平均兩兩距離', '空間熵', '人口/資源', '戶數/資源']
      },
      yaxis: { show: false },
      colors: ['#60a5fa', '#34d399'],
      stroke: { width: 2 },
      fill: { opacity: 0.2 },
      markers: { size: 4 },
      legend: { labels: { colors: '#94a3b8' } }
    }

    const comparisonSummary = computed(() => {
      const taipeiCity = taipeiCityData.value[selectedResourceType.value] || {}
      const newtaipeiCity = newtaipeiCityData.value[selectedResourceType.value] || {}

      return `
        <p><strong>台北市:</strong></p>
        <ul style="margin-left: 20px; margin-bottom: 12px;">
          <li>總資源數: ${taipeiCity.Count || 0}</li>
          <li>平均每處服務人數: ${Math.round(taipeiCity.population_per_count || 0)}</li>
          <li>離散度: ${((taipeiCity.Dispersion || 0) * 1000).toFixed(2)}</li>
        </ul>
        <p><strong>新北市:</strong></p>
        <ul style="margin-left: 20px;">
          <li>總資源數: ${newtaipeiCity.Count || 0}</li>
          <li>平均每處服務人數: ${Math.round(newtaipeiCity.population_per_count || 0)}</li>
          <li>離散度: ${((newtaipeiCity.Dispersion || 0) * 1000).toFixed(2)}</li>
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
          const resourceData = taipeiData.value[selectedResourceType.value] || []

          const resourceMap = {}
          resourceData.forEach(row => {
            resourceMap[row.Town] = {
              count: row.Count || 0,
              popRatio: row.population_per_count || 0
            }
          })

          geoData.features.forEach(feature => {
            const town = feature.properties.TOWN
            const data = resourceMap[town] || { count: 0, popRatio: 0 }
            feature.properties.resource_count = data.count
            feature.properties.pop_ratio = data.popRatio
          })

          map.addSource('taipei-districts', {
            type: 'geojson',
            data: geoData
          })

          // Calculate max value for better color distribution
          const maxResourceCount = Math.max(...resourceData.map(r => r.Count || 0))
          let colorStops
          if (maxResourceCount > 2000) {
            // For resources with very high counts (like 防空疏散地點: ~3500)
            colorStops = [0, '#1e293b', 500, '#1e3a5f', 1000, '#2563eb', 1500, '#3b82f6', 2000, '#22c55e', 2500, '#34d399', 3000, '#fbbf24', 3500, '#f59e0b']
          } else if (maxResourceCount > 1000) {
            // For resources with high counts (1000-2000)
            colorStops = [0, '#1e293b', 200, '#1e3a5f', 400, '#2563eb', 600, '#3b82f6', 800, '#22c55e', 1000, '#34d399', 1200, '#fbbf24', 1400, '#f59e0b']
          } else if (maxResourceCount > 200) {
            // For resources with medium-high counts (like 臺北市 AED: ~300)
            colorStops = [0, '#1e293b', 50, '#2563eb', 100, '#3b82f6', 150, '#22c55e', 200, '#34d399', 250, '#fbbf24', 330, '#f59e0b']
          } else if (maxResourceCount > 100) {
            // For resources with medium counts (like 新北市 AED: ~200)
            colorStops = [0, '#1e293b', 20, '#1e3a5f', 50, '#2563eb', 80, '#3b82f6', 110, '#22c55e', 140, '#34d399', 170, '#fbbf24', 200, '#f59e0b']
          } else if (maxResourceCount > 50) {
            // For resources with low-medium counts (50-100)
            colorStops = [0, '#1e293b', 10, '#1e3a5f', 20, '#2563eb', 35, '#3b82f6', 50, '#22c55e', 65, '#34d399', 80, '#fbbf24', 100, '#f59e0b']
          } else {
            // For resources with low counts (like 避難收容所: ~40)
            colorStops = [0, '#1e293b', 5, '#1e3a5f', 10, '#2563eb', 18, '#3b82f6', 25, '#22c55e', 32, '#34d399', 40, '#fbbf24', 50, '#f59e0b']
          }

          map.addLayer({
            id: 'taipei-fill',
            type: 'fill',
            source: 'taipei-districts',
            paint: {
              'fill-color': [
                'interpolate',
                ['linear'],
                ['get', 'resource_count'],
                ...colorStops
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
                  資源數量: ${props.resource_count || 0}<br>
                  人均比: ${Math.round(props.pop_ratio || 0)}
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
          const resourceData = newtaipeiData.value[selectedResourceType.value] || []

          const resourceMap = {}
          resourceData.forEach(row => {
            resourceMap[row.Town] = {
              count: row.Count || 0,
              popRatio: row.population_per_count || 0
            }
          })

          geoData.features.forEach(feature => {
            const town = feature.properties.TOWN
            const data = resourceMap[town] || { count: 0, popRatio: 0 }
            feature.properties.resource_count = data.count
            feature.properties.pop_ratio = data.popRatio
          })

          map.addSource('newtaipei-districts', {
            type: 'geojson',
            data: geoData
          })

          // Calculate max value for better color distribution
          const maxResourceCount = Math.max(...resourceData.map(r => r.Count || 0))
          let colorStops
          if (maxResourceCount > 2000) {
            // For resources with very high counts (like 防空疏散地點: ~3500)
            colorStops = [0, '#1e293b', 500, '#1e3a5f', 1000, '#2563eb', 1500, '#3b82f6', 2000, '#22c55e', 2500, '#34d399', 3000, '#fbbf24', 3500, '#f59e0b']
          } else if (maxResourceCount > 1000) {
            // For resources with high counts (1000-2000)
            colorStops = [0, '#1e293b', 200, '#1e3a5f', 400, '#2563eb', 600, '#3b82f6', 800, '#22c55e', 1000, '#34d399', 1200, '#fbbf24', 1400, '#f59e0b']
          } else if (maxResourceCount > 200) {
            // For resources with medium-high counts (like 臺北市 AED: ~300)
            colorStops = [0, '#1e293b', 50, '#2563eb', 100, '#3b82f6', 150, '#22c55e', 200, '#34d399', 250, '#fbbf24', 330, '#f59e0b']
          } else if (maxResourceCount > 100) {
            // For resources with medium counts (like 新北市 AED: ~200)
            colorStops = [0, '#1e293b', 20, '#1e3a5f', 50, '#2563eb', 80, '#3b82f6', 110, '#22c55e', 140, '#34d399', 170, '#fbbf24', 200, '#f59e0b']
          } else if (maxResourceCount > 50) {
            // For resources with low-medium counts (50-100)
            colorStops = [0, '#1e293b', 10, '#1e3a5f', 20, '#2563eb', 35, '#3b82f6', 50, '#22c55e', 65, '#34d399', 80, '#fbbf24', 100, '#f59e0b']
          } else {
            // For resources with low counts (like 避難收容所: ~40)
            colorStops = [0, '#1e293b', 5, '#1e3a5f', 10, '#2563eb', 18, '#3b82f6', 25, '#22c55e', 32, '#34d399', 40, '#fbbf24', 50, '#f59e0b']
          }

          map.addLayer({
            id: 'newtaipei-fill',
            type: 'fill',
            source: 'newtaipei-districts',
            paint: {
              'fill-color': [
                'interpolate',
                ['linear'],
                ['get', 'resource_count'],
                ...colorStops
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
                  資源數量: ${props.resource_count || 0}<br>
                  人均比: ${Math.round(props.pop_ratio || 0)}
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
        // Taipei data
        taipeiData.value.AED = await loadCSV('/source/topic/taipei/topic1-1__Town__regional_discrete_count(AED).csv')
        taipeiData.value['警消'] = await loadCSV('/source/topic/taipei/topic1-1__Town__regional_discrete_count(警消).csv')
        taipeiData.value['避難收容所'] = await loadCSV('/source/topic/taipei/topic1-1__Town__regional_discrete_count(避難收容所).csv')
        taipeiData.value['防空疏散地點'] = await loadCSV('/source/topic/taipei/topic1-1__Town__regional_discrete_count(防空疏散地點).csv')

        // New Taipei data
        newtaipeiData.value.AED = await loadCSV('/source/topic/newtaipeis/topic1-1__Town__regional_discrete_count(AED).csv')
        newtaipeiData.value['警消'] = await loadCSV('/source/topic/newtaipeis/topic1-1__Town__regional_discrete_count(警消).csv')
        newtaipeiData.value['避難收容所'] = await loadCSV('/source/topic/newtaipeis/topic1-1__Town__regional_discrete_count(避難收容所).csv')
        newtaipeiData.value['防空疏散地點'] = await loadCSV('/source/topic/newtaipeis/topic1-1__Town__regional_discrete_count(防空疏散地點).csv')

        // City-level data
        const taipeiCityAED = await loadCSV('/source/topic/taipei/topic1-2__City__regional_discrete_count(AED).csv')
        const taipeiCityPolice = await loadCSV('/source/topic/taipei/topic1-2__City__regional_discrete_count(警消).csv')
        const taipeiCityShelter = await loadCSV('/source/topic/taipei/topic1-2__City__regional_discrete_count(避難收容所).csv')
        const taipeiCityAirRaid = await loadCSV('/source/topic/taipei/topic1-2__City__regional_discrete_count(防空疏散地點).csv')

        taipeiCityData.value = {
          'AED': taipeiCityAED[0] || {},
          '警消': taipeiCityPolice[0] || {},
          '避難收容所': taipeiCityShelter[0] || {},
          '防空疏散地點': taipeiCityAirRaid[0] || {}
        }

        const newtaipeiCityAED = await loadCSV('/source/topic/newtaipeis/topic1-2__City__regional_discrete_count(AED).csv')
        const newtaipeiCityPolice = await loadCSV('/source/topic/newtaipeis/topic1-2__City__regional_discrete_count(警消).csv')
        const newtaipeiCityShelter = await loadCSV('/source/topic/newtaipeis/topic1-2__City__regional_discrete_count(避難收容所).csv')
        const newtaipeiCityAirRaid = await loadCSV('/source/topic/newtaipeis/topic1-2__City__regional_discrete_count(防空疏散地點).csv')

        newtaipeiCityData.value = {
          'AED': newtaipeiCityAED[0] || {},
          '警消': newtaipeiCityPolice[0] || {},
          '避難收容所': newtaipeiCityShelter[0] || {},
          '防空疏散地點': newtaipeiCityAirRaid[0] || {}
        }

      } catch (error) {
        console.error('Error loading Topic 1 data:', error)
      }
    }

    // Watch for section changes to initialize maps
    watch(selectedSection, (newVal) => {
      setTimeout(() => {
        if (newVal === 'taipei') {
          initTaipeiMap()
        } else if (newVal === 'newtaipei') {
          initNewtaipeiMap()
        }
      }, 100)
    })

    watch(selectedResourceType, () => {
      setTimeout(() => {
        if (selectedSection.value === 'taipei') {
          initTaipeiMap()
        } else if (selectedSection.value === 'newtaipei') {
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
      selectedResourceType,
      taipeiMapContainer,
      newtaipeiMapContainer,
      currentStats,
      taipeiCountSeries,
      taipeiCountChartOptions,
      taipeiPopRatioSeries,
      taipeiPopRatioChartOptions,
      taipeiDispersionSeries,
      taipeiDispersionChartOptions,
      taipeiEntropySeries,
      taipeiEntropyChartOptions,
      newtaipeiCountSeries,
      newtaipeiCountChartOptions,
      newtaipeiPopRatioSeries,
      newtaipeiPopRatioChartOptions,
      newtaipeiDispersionSeries,
      newtaipeiDispersionChartOptions,
      newtaipeiEntropySeries,
      newtaipeiEntropyChartOptions,
      cityComparisonCountSeries,
      cityComparisonCountOptions,
      cityComparisonMetricsSeries,
      cityComparisonMetricsOptions,
      districtComparisonSeries,
      districtComparisonOptions,
      spatialComparisonSeries,
      spatialComparisonOptions,
      comparisonSummary
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
