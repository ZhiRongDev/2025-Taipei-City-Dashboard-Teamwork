# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Development Server
```bash
npm run dev
```

### 3. Open Browser
Navigate to: `http://localhost:3000`

## 📱 What You'll See

### Main Navigation Tabs:
1. **總覽 (Overview)** - Dashboard summary and overview map
2. **AED 分析** - AED distribution and analysis
3. **避難收容處所** - Shelter statistics and maps
4. **防空疏散設施** - Air raid shelter capacity analysis
5. **景點周邊資源** - Tourist spot surrounding resources
6. **雙北比較** - Comparison between Taipei and New Taipei

## 🎯 Key Features to Try

### Interactive Maps
- Click on any district to see detailed information
- Hover over regions to highlight them
- Zoom and pan using mouse/touch gestures

### Charts and Visualizations
- Bar charts showing resource distribution
- Scatter plots for correlation analysis
- Radar charts for multi-dimensional comparison
- Heatmaps for spatial patterns
- Box plots for statistical distribution

### Filters
- Select city (Taipei/New Taipei/All)
- Choose disaster type (flood, earthquake, landslide, tsunami)
- Search tourist spots by name
- Adjust distance radius (1km/5km/10km)

### Data Tables
- Sortable columns
- Color-coded resource levels
- Export-ready format

## 🔧 Common Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build

# Troubleshooting
npm install          # Reinstall dependencies
rm -rf node_modules  # Clean install
npm cache clean --force
```

## 📊 Understanding the Data

### AED Analysis
- **數量 (Count)**: Number of AED devices in each district
- **每台服務人數 (People per AED)**: Lower is better (more coverage)
- **空間離散度 (Spatial Dispersion)**: Higher means more spread out
- **資源等級 (Resource Level)**:
  - 優良 (Excellent): < 1000 people per AED
  - 良好 (Good): 1000-2000
  - 普通 (Fair): 2000-3000
  - 待改善 (Needs Improvement): > 3000

### Shelter Analysis
- **災別 (Disaster Types)**:
  - 水災 (Flood)
  - 地震 (Earthquake)
  - 土石流 (Landslide)
  - 海嘯 (Tsunami)
- **任一災別避難地點數**: Total shelters for any disaster type

### Air Raid Shelters
- **容納人數 (Capacity)**: Maximum people capacity
- **收容所面積 (Area)**: Total shelter area in m²
- **每人可分配面積**: Space allocation per person
- **每萬人可分配面積**: Space per 10,000 population

### Tourist Spot Analysis
- **1km/5km/10km**: Resources within different radius
- Total resources = AED + Police/Fire + Air Raid + Shelters

## 🎨 UI/UX Features

### Color Coding
- **Blue (#60a5fa)**: Taipei City
- **Green (#34d399)**: New Taipei City
- **Yellow (#fbbf24)**: Medium/Warning
- **Red (#f87171)**: Low/Critical
- **Purple (#a78bfa)**: Additional categories

### Responsive Design
- Desktop: Full layout with side-by-side charts
- Tablet: Adaptive grid layout
- Mobile: Stacked vertical layout

## 🗺️ Map Interactions

### Available Actions:
- **Click**: Show popup with details
- **Zoom**: Mouse wheel or pinch gesture
- **Pan**: Click and drag
- **Hover**: Highlight regions

### Color Scale:
Maps use color gradients to show resource density:
- Darker = Less resources
- Lighter/Brighter = More resources

## 📈 Chart Types Used

1. **Bar Charts**: Compare quantities across districts
2. **Horizontal Bars**: Better for many categories
3. **Scatter Plots**: Show correlations
4. **Radar Charts**: Multi-dimensional comparison
5. **Heatmaps**: Pattern recognition
6. **Box Plots**: Statistical distribution
7. **Treemaps**: Hierarchical data (future)

## 💡 Tips

### Performance
- Charts lazy-load when you navigate to each section
- Maps render progressively
- Tables paginate for large datasets

### Best Practices
- Use filters to focus on specific areas
- Compare charts side-by-side
- Export data tables for further analysis
- Check both absolute numbers and per-capita metrics

### Keyboard Shortcuts (in development)
- `Ctrl/Cmd + K`: Search
- `Ctrl/Cmd + B`: Toggle sidebar
- Arrow keys: Navigate tabs

## 🐛 Troubleshooting

### Map Not Loading
1. Check internet connection
2. Verify MapBox token is valid
3. Clear browser cache
4. Try a different browser

### Charts Not Displaying
1. Ensure JavaScript is enabled
2. Check browser console for errors
3. Refresh the page
4. Update browser to latest version

### Data Not Loading
1. Verify `source/` folder exists
2. Check CSV files are present
3. Look for CORS errors in console
4. Ensure dev server is running

## 📞 Need Help?

Check the full documentation:
- [README.md](README.md) - Project overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [source/readme.md](source/readme.md) - Data documentation

Happy exploring! 🎉
