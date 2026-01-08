<template>
  <div class="topic3">
    <div class="card">
      <h2>Topic 3: 景點周遭距離分析</h2>
      <p style="color: #94a3b8; line-height: 1.8;">
        考量旅遊景點常為高人流熱區，若發生災害將對救援效率構成挑戰，因此本主題針對觀光景點 1km、5km 與 10km
        範圍內防災設施（包含 AED、避難所、警消單位等）進行 haversine 距離分析，盤點其應變能力與資源覆蓋程度。
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
        <label>分析範圍：</label>
        <select v-model="selectedRadius">
          <option value="1km">1 公里內</option>
          <option value="5km">5 公里內</option>
          <option value="10km">10 公里內</option>
        </select>
      </div>
    </div>

    <!-- Statistics Summary -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">分析景點數</div>
        <div class="stat-value">{{ currentStats.totalSpots }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card green">
        <div class="stat-label">平均 AED 數</div>
        <div class="stat-value">{{ currentStats.avgAED }}<span class="stat-unit">台</span></div>
      </div>
      <div class="stat-card yellow">
        <div class="stat-label">平均避難所數</div>
        <div class="stat-value">{{ currentStats.avgShelters }}<span class="stat-unit">處</span></div>
      </div>
      <div class="stat-card red">
        <div class="stat-label">資源最豐富景點</div>
        <div class="stat-value" style="font-size: 1.1rem;">{{ currentStats.topSpot }}</div>
      </div>
    </div>

    <!-- Taipei Section -->
    <div v-if="selectedSection === 'taipei'" class="section-content">
      <h3 class="section-title">台北市景點周邊防災資源分析 ({{ selectedRadius }})</h3>

      <!-- Resource Overview -->
      <div class="card">
        <h3>各景點防災資源總覽</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #60a5fa;">數據分析：</strong>
          此堆疊長條圖呈現各景點周邊的綜合防災資源配置。陽明公園、龍鳳谷、市立美術館等景點
          在 1km 範圍內擁有較多 AED 與避難收容所，顯示這些高人流景點周邊的防災應變能力較強。
          部分郊區景點如小油坑遊憩區資源相對稀少，需特別注意遊客安全管理。
        </p>
        <apexchart
          type="bar"
          height="500"
          :options="taipeiResourceChartOptions"
          :series="taipeiResourceSeries"
        ></apexchart>
      </div>

      <!-- Resource Type Distribution -->
      <div class="grid grid-2">
        <div class="card">
          <h3>AED 分布</h3>
          <p style="color: #94a3b8; margin-bottom: 12px; font-size: 0.95rem;">
            <strong style="color: #60a5fa;">數據分析：</strong>
            位於都會區的景點如陽明公園、市立美術館周邊 AED 配置密度較高（超過 150 台），
            有助於緊急情況下的快速醫療救援。郊區景點則相對較少，建議加強行動 AED 設備配置。
          </p>
          <apexchart
            type="bar"
            height="400"
            :options="taipeiAEDChartOptions"
            :series="taipeiAEDSeries"
          ></apexchart>
        </div>

        <div class="card">
          <h3>避難收容所分布</h3>
          <p style="color: #94a3b8; margin-bottom: 12px; font-size: 0.95rem;">
            <strong style="color: #34d399;">數據分析：</strong>
            陽明公園、龍鳳谷等景點周邊避難收容所數量較多（7-15 處），
            能在災害發生時提供緊急庇護。部分景點如國立故宮博物院周邊收容所較少，
            可能需要規劃額外的疏散路線與臨時收容方案。
          </p>
          <apexchart
            type="bar"
            height="400"
            :options="taipeiShelterChartOptions"
            :series="taipeiShelterSeries"
          ></apexchart>
        </div>
      </div>

      <!-- Radar Chart -->
      <div class="card">
        <h3>綜合防災資源雷達圖 (Top 10 景點)</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #fbbf24;">數據分析：</strong>
          雷達圖呈現各景點在四類防災資源的綜合表現。面積越大表示該景點周邊資源越豐富。
          陽明公園、龍鳳谷等景點在多項指標上表現均衡，具備較完善的防災應變能力。
        </p>
        <apexchart
          type="radar"
          height="500"
          :options="taipeiRadarOptions"
          :series="taipeiRadarSeries"
        ></apexchart>
      </div>

      <!-- Heatmap -->
      <div class="card">
        <h3>防災資源熱力分布</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          顏色越深表示該類型資源數量越多
        </p>
        <apexchart
          type="heatmap"
          height="600"
          :options="taipeiHeatmapOptions"
          :series="taipeiHeatmapSeries"
        ></apexchart>
      </div>
    </div>

    <!-- New Taipei Section -->
    <div v-if="selectedSection === 'newtaipei'" class="section-content">
      <h3 class="section-title">新北市景點周邊防災資源分析 ({{ selectedRadius }})</h3>

      <!-- Resource Overview -->
      <div class="card">
        <h3>各景點防災資源總覽</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #60a5fa;">數據分析：</strong>
          新北市景點分布廣泛，從都會區到山區海岸皆有涵蓋。碧潭風景特定區、法鼓山世界佛教教育園區等
          位於人口密集區的景點周邊資源豐富；而龍洞灣公園、翡翠灣濱海遊憩區等偏遠海岸景點
          防災資源相對稀缺，建議加強行動應變設備配置與緊急疏散路線規劃。
        </p>
        <apexchart
          type="bar"
          height="600"
          :options="newtaipeiResourceChartOptions"
          :series="newtaipeiResourceSeries"
        ></apexchart>
      </div>

      <!-- Resource Type Distribution -->
      <div class="grid grid-2">
        <div class="card">
          <h3>AED 分布</h3>
          <p style="color: #94a3b8; margin-bottom: 12px; font-size: 0.95rem;">
            <strong style="color: #60a5fa;">數據分析：</strong>
            法鼓山、碧潭風景區、新北市黃金博物園區等景點周邊 AED 配置密集（超過 90 台），
            顯示都會區與熱門景點的醫療救援能力較佳。偏遠景點如龍洞灣、龍門露營區周邊 AED 數量為零或極少，
            遊客發生緊急狀況時救援時效性較低，建議增設行動 AED 或加強救護車待命機制。
          </p>
          <apexchart
            type="bar"
            height="500"
            :options="newtaipeiAEDChartOptions"
            :series="newtaipeiAEDSeries"
          ></apexchart>
        </div>

        <div class="card">
          <h3>避難收容所分布</h3>
          <p style="color: #94a3b8; margin-bottom: 12px; font-size: 0.95rem;">
            <strong style="color: #34d399;">數據分析：</strong>
            碧潭風景區、法鼓山、淡水漁人碼頭等景點周邊避難收容所數量充足（10-16 處），
            能有效應對大規模災害事件。然而龍洞灣公園、龍門露營區等海岸景點避難收容所為零，
            地理位置偏遠且疏散路線受限，建議規劃臨時避難據點與海上救援機制。
          </p>
          <apexchart
            type="bar"
            height="500"
            :options="newtaipeiShelterChartOptions"
            :series="newtaipeiShelterSeries"
          ></apexchart>
        </div>
      </div>

      <!-- Radar Chart -->
      <div class="card">
        <h3>綜合防災資源雷達圖 (Top 10 景點)</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #fbbf24;">數據分析：</strong>
          雷達圖呈現新北市防災資源最豐富的前 10 個景點。碧潭、法鼓山、黃金博物園區等景點
          在四類資源上皆有顯著配置，反映其作為熱門觀光地點的防災重要性。部分景點在特定資源類型上
          表現突出但其他類型偏弱，顯示資源配置策略有優化空間。
        </p>
        <apexchart
          type="radar"
          height="500"
          :options="newtaipeiRadarOptions"
          :series="newtaipeiRadarSeries"
        ></apexchart>
      </div>

      <!-- Heatmap -->
      <div class="card">
        <h3>防災資源熱力分布</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #f87171;">數據分析：</strong>
          熱力圖清楚呈現新北市景點的資源配置落差。顏色越深表示資源數量越多。
          可明顯看出都會區景點（碧潭、法鼓山）與偏遠海岸景點（龍洞、翡翠灣）的資源差距，
          建議針對偏遠地區制定差異化的防災應變策略，如行動救援隊、直升機救援等機制。
        </p>
        <apexchart
          type="heatmap"
          height="700"
          :options="newtaipeiHeatmapOptions"
          :series="newtaipeiHeatmapSeries"
        ></apexchart>
      </div>
    </div>

    <!-- Comparison Section -->
    <div v-if="selectedSection === 'comparison'" class="section-content">
      <h3 class="section-title">雙北景點周邊防災資源比較 ({{ selectedRadius }})</h3>

      <!-- City-level Comparison -->
      <div class="card">
        <h3>縣市層級資源平均值比較</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #60a5fa;">數據分析：</strong>
          比較台北市與新北市各景點周邊的平均資源配置。台北市景點多位於都會核心區，
          周邊防災資源密度通常較高；新北市景點分布較廣，包含郊區與山區景點，
          資源配置呈現較大差異性。
        </p>
        <div class="grid grid-2">
          <apexchart
            type="bar"
            height="350"
            :options="cityAvgResourceOptions"
            :series="cityAvgResourceSeries"
          ></apexchart>
          <div class="comparison-summary">
            <h4 style="color: #60a5fa; margin-bottom: 16px;">比較摘要</h4>
            <div v-html="comparisonSummary" style="color: #cbd5e1; line-height: 1.8;"></div>
          </div>
        </div>
      </div>

      <!-- Resource Type Comparison -->
      <div class="card">
        <h3>各類型資源平均數量比較</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #34d399;">數據分析：</strong>
          此圖呈現雙北景點在 AED、警消、防空疏散地點、避難收容所四類資源的平均配置比較。
          可以觀察到不同資源類型在兩市的配置策略差異，作為未來資源優化配置的參考依據。
        </p>
        <apexchart
          type="bar"
          height="400"
          :options="resourceTypeComparisonOptions"
          :series="resourceTypeComparisonSeries"
        ></apexchart>
      </div>

      <!-- Top Spots Comparison -->
      <div class="card">
        <h3>資源最豐富景點排名 (雙北 Top 15)</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          <strong style="color: #fbbf24;">數據分析：</strong>
          此排名呈現雙北防災資源最豐富的前 15 個景點。位於都會核心區的景點
          （如陽明公園、市立美術館）通常位居前列，反映這些高人流區域在防災資源配置上的優先性。
          此排名可作為觀光安全管理與應變資源配置的重要參考。
        </p>
        <apexchart
          type="bar"
          height="500"
          :options="topSpotsComparisonOptions"
          :series="topSpotsComparisonSeries"
        ></apexchart>
      </div>

      <!-- Scatter Plot -->
      <div class="card">
        <h3>AED vs 避難所數量散佈圖</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          此圖表顯示各景點周邊的 AED 與避難所數量關係，右上角代表資源較豐富的景點
        </p>
        <apexchart
          type="scatter"
          height="500"
          :options="scatterComparisonOptions"
          :series="scatterComparisonSeries"
        ></apexchart>
      </div>

      <!-- Radius Comparison -->
      <div class="card">
        <h3>不同範圍資源覆蓋比較</h3>
        <p style="color: #94a3b8; margin-bottom: 16px; font-size: 0.95rem;">
          比較 1km、5km、10km 範圍內的平均資源數量
        </p>
        <apexchart
          type="line"
          height="400"
          :options="radiusComparisonOptions"
          :series="radiusComparisonSeries"
        ></apexchart>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { loadCSV } from '../utils/csvLoader'

export default {
  name: 'Topic3',
  setup() {
    const selectedSection = ref('taipei')
    const selectedRadius = ref('1km')

    const taipeiData = ref({
      '1km': [],
      '5km': [],
      '10km': []
    })

    const newtaipeiData = ref({
      '1km': [],
      '5km': [],
      '10km': []
    })

    // Get current data based on selection
    const currentTaipeiData = computed(() => taipeiData.value[selectedRadius.value] || [])
    const currentNewtaipeiData = computed(() => newtaipeiData.value[selectedRadius.value] || [])

    // Current Statistics
    const currentStats = computed(() => {
      let data = []
      if (selectedSection.value === 'taipei') {
        data = currentTaipeiData.value
      } else if (selectedSection.value === 'newtaipei') {
        data = currentNewtaipeiData.value
      } else {
        data = [...currentTaipeiData.value, ...currentNewtaipeiData.value]
      }

      const totalSpots = data.length
      const avgAED = totalSpots > 0 ? Math.round(data.reduce((sum, row) => sum + (row[`AED_${selectedRadius.value}`] || 0), 0) / totalSpots) : 0
      const avgShelters = totalSpots > 0 ? Math.round(data.reduce((sum, row) => sum + (row[`避難收容所_${selectedRadius.value}`] || 0), 0) / totalSpots) : 0

      // Find spot with most total resources
      const topSpotData = data.reduce((max, row) => {
        const totalResources = (row[`AED_${selectedRadius.value}`] || 0) +
          (row[`避難收容所_${selectedRadius.value}`] || 0) +
          (row[`警消_${selectedRadius.value}`] || 0) +
          (row[`防空疏散地點_${selectedRadius.value}`] || 0)
        const maxResources = (max[`AED_${selectedRadius.value}`] || 0) +
          (max[`避難收容所_${selectedRadius.value}`] || 0) +
          (max[`警消_${selectedRadius.value}`] || 0) +
          (max[`防空疏散地點_${selectedRadius.value}`] || 0)
        return totalResources > maxResources ? row : max
      }, data[0] || {})

      const topSpot = topSpotData ? (topSpotData['旅遊景點'] || 'N/A') : 'N/A'

      return { totalSpots, avgAED, avgShelters, topSpot }
    })

    // Helper function to get column name based on radius
    const getColumnName = (type) => `${type}_${selectedRadius.value}`

    // Taipei Charts
    const taipeiResourceSeries = computed(() => {
      const data = currentTaipeiData.value.slice(0, 15)
      return [
        {
          name: 'AED',
          data: data.map(row => row[getColumnName('AED')] || 0)
        },
        {
          name: '警消',
          data: data.map(row => row[getColumnName('警消')] || 0)
        },
        {
          name: '防空疏散地點',
          data: data.map(row => row[getColumnName('防空疏散地點')] || 0)
        },
        {
          name: '避難收容所',
          data: data.map(row => row[getColumnName('避難收容所')] || 0)
        }
      ]
    })

    const taipeiResourceChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false }, stacked: true },
      theme: { mode: 'dark' },
      xaxis: {
        categories: currentTaipeiData.value.slice(0, 15).map(row => row['旅遊景點'] || ''),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa', '#34d399', '#fbbf24', '#f87171'],
      plotOptions: { bar: { borderRadius: 4 } },
      legend: { labels: { colors: '#94a3b8' } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const taipeiAEDSeries = computed(() => [{
      name: 'AED',
      data: currentTaipeiData.value.slice(0, 15).map(row => row[getColumnName('AED')] || 0)
    }])

    const taipeiAEDChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: currentTaipeiData.value.slice(0, 15).map(row => row['旅遊景點'] || ''),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const taipeiShelterSeries = computed(() => [{
      name: '避難收容所',
      data: currentTaipeiData.value.slice(0, 15).map(row => row[getColumnName('避難收容所')] || 0)
    }])

    const taipeiShelterChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: currentTaipeiData.value.slice(0, 15).map(row => row['旅遊景點'] || ''),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const taipeiRadarSeries = computed(() => {
      const data = currentTaipeiData.value.slice(0, 10)
      return data.map(row => ({
        name: row['旅遊景點'] || '',
        data: [
          row[getColumnName('AED')] || 0,
          row[getColumnName('警消')] || 0,
          row[getColumnName('防空疏散地點')] || 0,
          row[getColumnName('避難收容所')] || 0
        ]
      }))
    })

    const taipeiRadarOptions = {
      chart: { type: 'radar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: ['AED', '警消', '防空疏散地點', '避難收容所']
      },
      yaxis: { show: false },
      stroke: { width: 2 },
      fill: { opacity: 0.2 },
      markers: { size: 4 },
      legend: { labels: { colors: '#94a3b8' }, position: 'bottom' }
    }

    const taipeiHeatmapSeries = computed(() => {
      const data = currentTaipeiData.value.slice(0, 20)
      return [
        {
          name: 'AED',
          data: data.map(row => ({
            x: row['旅遊景點'] || '',
            y: row[getColumnName('AED')] || 0
          }))
        },
        {
          name: '警消',
          data: data.map(row => ({
            x: row['旅遊景點'] || '',
            y: row[getColumnName('警消')] || 0
          }))
        },
        {
          name: '防空疏散地點',
          data: data.map(row => ({
            x: row['旅遊景點'] || '',
            y: row[getColumnName('防空疏散地點')] || 0
          }))
        },
        {
          name: '避難收容所',
          data: data.map(row => ({
            x: row['旅遊景點'] || '',
            y: row[getColumnName('避難收容所')] || 0
          }))
        }
      ]
    })

    const taipeiHeatmapOptions = {
      chart: { type: 'heatmap', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      dataLabels: { enabled: true, style: { colors: ['#fff'] } },
      colors: ['#60a5fa'],
      xaxis: { labels: { style: { colors: '#94a3b8' }, rotate: -45 } },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      plotOptions: {
        heatmap: {
          colorScale: {
            ranges: [
              { from: 0, to: 5, color: '#1e293b', name: '極少' },
              { from: 6, to: 20, color: '#60a5fa', name: '少' },
              { from: 21, to: 100, color: '#34d399', name: '中' },
              { from: 101, to: 500, color: '#fbbf24', name: '多' },
              { from: 501, to: 10000, color: '#f87171', name: '極多' }
            ]
          }
        }
      }
    }

    // New Taipei Charts (similar structure)
    const newtaipeiResourceSeries = computed(() => {
      const data = currentNewtaipeiData.value.slice(0, 20)
      return [
        {
          name: 'AED',
          data: data.map(row => row[getColumnName('AED')] || 0)
        },
        {
          name: '警消',
          data: data.map(row => row[getColumnName('警消')] || 0)
        },
        {
          name: '防空疏散地點',
          data: data.map(row => row[getColumnName('防空疏散地點')] || 0)
        },
        {
          name: '避難收容所',
          data: data.map(row => row[getColumnName('避難收容所')] || 0)
        }
      ]
    })

    const newtaipeiResourceChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false }, stacked: true },
      theme: { mode: 'dark' },
      xaxis: {
        categories: currentNewtaipeiData.value.slice(0, 20).map(row => row['旅遊景點'] || ''),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa', '#34d399', '#fbbf24', '#f87171'],
      plotOptions: { bar: { borderRadius: 4 } },
      legend: { labels: { colors: '#94a3b8' } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const newtaipeiAEDSeries = computed(() => [{
      name: 'AED',
      data: currentNewtaipeiData.value.slice(0, 20).map(row => row[getColumnName('AED')] || 0)
    }])

    const newtaipeiAEDChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: currentNewtaipeiData.value.slice(0, 20).map(row => row['旅遊景點'] || ''),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const newtaipeiShelterSeries = computed(() => [{
      name: '避難收容所',
      data: currentNewtaipeiData.value.slice(0, 20).map(row => row[getColumnName('避難收容所')] || 0)
    }])

    const newtaipeiShelterChartOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: currentNewtaipeiData.value.slice(0, 20).map(row => row['旅遊景點'] || ''),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#34d399'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const newtaipeiRadarSeries = computed(() => {
      const data = currentNewtaipeiData.value.slice(0, 10)
      return data.map(row => ({
        name: row['旅遊景點'] || '',
        data: [
          row[getColumnName('AED')] || 0,
          row[getColumnName('警消')] || 0,
          row[getColumnName('防空疏散地點')] || 0,
          row[getColumnName('避難收容所')] || 0
        ]
      }))
    })

    const newtaipeiRadarOptions = {
      chart: { type: 'radar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: ['AED', '警消', '防空疏散地點', '避難收容所']
      },
      yaxis: { show: false },
      stroke: { width: 2 },
      fill: { opacity: 0.2 },
      markers: { size: 4 },
      legend: { labels: { colors: '#94a3b8' }, position: 'bottom' }
    }

    const newtaipeiHeatmapSeries = computed(() => {
      const data = currentNewtaipeiData.value.slice(0, 25)
      return [
        {
          name: 'AED',
          data: data.map(row => ({
            x: row['旅遊景點'] || '',
            y: row[getColumnName('AED')] || 0
          }))
        },
        {
          name: '警消',
          data: data.map(row => ({
            x: row['旅遊景點'] || '',
            y: row[getColumnName('警消')] || 0
          }))
        },
        {
          name: '防空疏散地點',
          data: data.map(row => ({
            x: row['旅遊景點'] || '',
            y: row[getColumnName('防空疏散地點')] || 0
          }))
        },
        {
          name: '避難收容所',
          data: data.map(row => ({
            x: row['旅遊景點'] || '',
            y: row[getColumnName('避難收容所')] || 0
          }))
        }
      ]
    })

    const newtaipeiHeatmapOptions = {
      chart: { type: 'heatmap', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      dataLabels: { enabled: true, style: { colors: ['#fff'] } },
      colors: ['#34d399'],
      xaxis: { labels: { style: { colors: '#94a3b8' }, rotate: -45 } },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      plotOptions: {
        heatmap: {
          colorScale: {
            ranges: [
              { from: 0, to: 5, color: '#1e293b', name: '極少' },
              { from: 6, to: 20, color: '#60a5fa', name: '少' },
              { from: 21, to: 100, color: '#34d399', name: '中' },
              { from: 101, to: 500, color: '#fbbf24', name: '多' },
              { from: 501, to: 10000, color: '#f87171', name: '極多' }
            ]
          }
        }
      }
    }

    // Comparison Charts
    const cityAvgResourceSeries = computed(() => {
      const taipeiAvgAED = currentTaipeiData.value.length > 0
        ? currentTaipeiData.value.reduce((sum, row) => sum + (row[getColumnName('AED')] || 0), 0) / currentTaipeiData.value.length
        : 0
      const newtaipeiAvgAED = currentNewtaipeiData.value.length > 0
        ? currentNewtaipeiData.value.reduce((sum, row) => sum + (row[getColumnName('AED')] || 0), 0) / currentNewtaipeiData.value.length
        : 0

      const taipeiAvgShelter = currentTaipeiData.value.length > 0
        ? currentTaipeiData.value.reduce((sum, row) => sum + (row[getColumnName('避難收容所')] || 0), 0) / currentTaipeiData.value.length
        : 0
      const newtaipeiAvgShelter = currentNewtaipeiData.value.length > 0
        ? currentNewtaipeiData.value.reduce((sum, row) => sum + (row[getColumnName('避難收容所')] || 0), 0) / currentNewtaipeiData.value.length
        : 0

      return [
        {
          name: '台北市',
          data: [taipeiAvgAED, taipeiAvgShelter]
        },
        {
          name: '新北市',
          data: [newtaipeiAvgAED, newtaipeiAvgShelter]
        }
      ]
    })

    const cityAvgResourceOptions = {
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      title: { text: '平均資源數量', style: { color: '#94a3b8' } },
      xaxis: {
        categories: ['AED', '避難收容所'],
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa', '#34d399'],
      plotOptions: { bar: { borderRadius: 4, columnWidth: '70%' } },
      legend: { labels: { colors: '#94a3b8' } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    const comparisonSummary = computed(() => {
      const taipeiAvg = currentTaipeiData.value.length > 0
        ? (currentTaipeiData.value.reduce((sum, row) =>
          sum + (row[getColumnName('AED')] || 0) + (row[getColumnName('避難收容所')] || 0), 0) / currentTaipeiData.value.length).toFixed(1)
        : 0
      const newtaipeiAvg = currentNewtaipeiData.value.length > 0
        ? (currentNewtaipeiData.value.reduce((sum, row) =>
          sum + (row[getColumnName('AED')] || 0) + (row[getColumnName('避難收容所')] || 0), 0) / currentNewtaipeiData.value.length).toFixed(1)
        : 0

      return `
        <p><strong>台北市:</strong></p>
        <ul style="margin-left: 20px; margin-bottom: 12px;">
          <li>分析景點數: ${currentTaipeiData.value.length}</li>
          <li>平均資源總數: ${taipeiAvg}</li>
        </ul>
        <p><strong>新北市:</strong></p>
        <ul style="margin-left: 20px;">
          <li>分析景點數: ${currentNewtaipeiData.value.length}</li>
          <li>平均資源總數: ${newtaipeiAvg}</li>
        </ul>
      `
    })

    const resourceTypeComparisonSeries = computed(() => {
      const calculateAvg = (data, type) => {
        return data.length > 0
          ? data.reduce((sum, row) => sum + (row[getColumnName(type)] || 0), 0) / data.length
          : 0
      }

      return [
        {
          name: '台北市',
          data: [
            calculateAvg(currentTaipeiData.value, 'AED'),
            calculateAvg(currentTaipeiData.value, '警消'),
            calculateAvg(currentTaipeiData.value, '防空疏散地點'),
            calculateAvg(currentTaipeiData.value, '避難收容所')
          ]
        },
        {
          name: '新北市',
          data: [
            calculateAvg(currentNewtaipeiData.value, 'AED'),
            calculateAvg(currentNewtaipeiData.value, '警消'),
            calculateAvg(currentNewtaipeiData.value, '防空疏散地點'),
            calculateAvg(currentNewtaipeiData.value, '避難收容所')
          ]
        }
      ]
    })

    const resourceTypeComparisonOptions = {
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: ['AED', '警消', '防空疏散地點', '避難收容所'],
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#60a5fa', '#34d399'],
      plotOptions: { bar: { borderRadius: 4, columnWidth: '70%' } },
      legend: { labels: { colors: '#94a3b8' } },
      dataLabels: { enabled: true, formatter: (val) => val.toFixed(1) },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    const topSpotsData = computed(() => {
      const allSpots = [
        ...currentTaipeiData.value.map(s => ({ ...s, city: '台北市' })),
        ...currentNewtaipeiData.value.map(s => ({ ...s, city: '新北市' }))
      ].map(s => ({
        ...s,
        total: (s[getColumnName('AED')] || 0) + (s[getColumnName('避難收容所')] || 0) +
               (s[getColumnName('警消')] || 0) + (s[getColumnName('防空疏散地點')] || 0)
      }))

      // Remove duplicates by using city + spot name as key
      const uniqueSpots = new Map()
      allSpots.forEach(spot => {
        const key = `${spot.city}_${spot['旅遊景點']}`
        if (!uniqueSpots.has(key)) {
          uniqueSpots.set(key, spot)
        }
      })

      return Array.from(uniqueSpots.values())
        .sort((a, b) => b.total - a.total)
        .slice(0, 15)
    })

    const topSpotsComparisonSeries = computed(() => [{
      name: '總資源數',
      data: topSpotsData.value.map(s => s.total)
    }])

    const topSpotsComparisonOptions = computed(() => ({
      chart: { type: 'bar', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: topSpotsData.value.map(s => `${s.city} ${s['旅遊景點']}`),
        labels: { style: { colors: '#94a3b8' }, rotate: -45 }
      },
      yaxis: { labels: { style: { colors: '#94a3b8' } } },
      colors: ['#fbbf24'],
      dataLabels: { enabled: false },
      plotOptions: { bar: { borderRadius: 4 } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }))

    const scatterComparisonSeries = computed(() => [
      {
        name: '台北市',
        data: currentTaipeiData.value.map(row => ({
          x: row[getColumnName('AED')] || 0,
          y: row[getColumnName('避難收容所')] || 0
        }))
      },
      {
        name: '新北市',
        data: currentNewtaipeiData.value.map(row => ({
          x: row[getColumnName('AED')] || 0,
          y: row[getColumnName('避難收容所')] || 0
        }))
      }
    ])

    const scatterComparisonOptions = {
      chart: { type: 'scatter', background: 'transparent', toolbar: { show: true }, zoom: { enabled: true } },
      theme: { mode: 'dark' },
      xaxis: {
        title: { text: 'AED 數量', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        title: { text: '避難收容所數量', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#60a5fa', '#34d399'],
      markers: { size: 6 },
      legend: { labels: { colors: '#94a3b8' } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    const radiusComparisonSeries = computed(() => {
      const calculateAvgForRadius = (data, radius) => {
        if (data.length === 0) return 0
        return data.reduce((sum, row) =>
          sum + (row[`AED_${radius}`] || 0) + (row[`避難收容所_${radius}`] || 0), 0) / data.length
      }

      return [
        {
          name: '台北市',
          data: ['1km', '5km', '10km'].map(r => calculateAvgForRadius(taipeiData.value[r], r))
        },
        {
          name: '新北市',
          data: ['1km', '5km', '10km'].map(r => calculateAvgForRadius(newtaipeiData.value[r], r))
        }
      ]
    })

    const radiusComparisonOptions = {
      chart: { type: 'line', background: 'transparent', toolbar: { show: false } },
      theme: { mode: 'dark' },
      xaxis: {
        categories: ['1 公里', '5 公里', '10 公里'],
        labels: { style: { colors: '#94a3b8' } }
      },
      yaxis: {
        title: { text: '平均資源數', style: { color: '#94a3b8' } },
        labels: { style: { colors: '#94a3b8' } }
      },
      colors: ['#60a5fa', '#34d399'],
      stroke: { width: 3, curve: 'smooth' },
      markers: { size: 6 },
      legend: { labels: { colors: '#94a3b8' } },
      grid: { borderColor: '#334155', strokeDashArray: 3 }
    }

    // Load data
    const loadData = async () => {
      try {
        // Taipei data
        taipeiData.value['1km'] = await loadCSV('/source/topic/taipei/topic_3-1_spot_source_count_in__1km.csv')
        taipeiData.value['5km'] = await loadCSV('/source/topic/taipei/topic_3-1_spot_source_count_in__5km.csv')
        taipeiData.value['10km'] = await loadCSV('/source/topic/taipei/topic_3-1_spot_source_count_in__10km.csv')

        // New Taipei data
        newtaipeiData.value['1km'] = await loadCSV('/source/topic/newtaipeis/topic_3-1_spot_source_count__1km.csv')
        newtaipeiData.value['5km'] = await loadCSV('/source/topic/newtaipeis/topic_3-1_spot_source_count__5km.csv')
        newtaipeiData.value['10km'] = await loadCSV('/source/topic/newtaipeis/topic_3-1_spot_source_count__10km.csv')
      } catch (error) {
        console.error('Error loading Topic 3 data:', error)
      }
    }

    onMounted(async () => {
      await loadData()
    })

    return {
      selectedSection,
      selectedRadius,
      currentStats,
      taipeiResourceSeries,
      taipeiResourceChartOptions,
      taipeiAEDSeries,
      taipeiAEDChartOptions,
      taipeiShelterSeries,
      taipeiShelterChartOptions,
      taipeiRadarSeries,
      taipeiRadarOptions,
      taipeiHeatmapSeries,
      taipeiHeatmapOptions,
      newtaipeiResourceSeries,
      newtaipeiResourceChartOptions,
      newtaipeiAEDSeries,
      newtaipeiAEDChartOptions,
      newtaipeiShelterSeries,
      newtaipeiShelterChartOptions,
      newtaipeiRadarSeries,
      newtaipeiRadarOptions,
      newtaipeiHeatmapSeries,
      newtaipeiHeatmapOptions,
      cityAvgResourceSeries,
      cityAvgResourceOptions,
      comparisonSummary,
      resourceTypeComparisonSeries,
      resourceTypeComparisonOptions,
      topSpotsComparisonSeries,
      topSpotsComparisonOptions,
      scatterComparisonSeries,
      scatterComparisonOptions,
      radiusComparisonSeries,
      radiusComparisonOptions
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
