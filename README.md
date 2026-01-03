# 雙北防災資源分析系統 Taipei Disaster Resource Dashboard

A comprehensive data visualization dashboard for analyzing disaster preparedness resources in Taipei and New Taipei City.

![Dashboard Preview](https://img.shields.io/badge/Vue.js-3.5-4FC08D?logo=vue.js&logoColor=white)
![ApexCharts](https://img.shields.io/badge/ApexCharts-5.3-00D8FF?logo=apexcharts)
![MapBox](https://img.shields.io/badge/MapBox-GL-4264FB?logo=mapbox)

## Features

### 📊 Overview Dashboard
- Summary statistics for disaster resources across both cities
- Interactive map showing regional AED distribution
- Quick access to all analysis modules

### 🏥 AED Analysis
- Regional AED distribution maps
- Per capita AED service ratio
- Spatial dispersion analysis
- Comparison charts between districts

### 🏘️ Shelter Analysis
- Disaster-specific shelter statistics (flood, earthquake, landslide, tsunami)
- Regional distribution maps
- Heatmap and radar chart visualizations
- Detailed capacity analysis

### 🛡️ Air Raid Shelter Analysis
- Capacity and area analysis
- Per capita space allocation
- Scatter plots showing capacity vs area
- Resource adequacy grading

### 🗺️ Tourist Spot Analysis
- Resources within 1km, 5km, and 10km of tourist attractions
- Interactive map with adjustable radius
- Comparative charts across different distances
- Heatmap showing resource concentration

### 🔄 Taipei vs New Taipei Comparison
- Side-by-side statistics comparison
- Box plots for spatial dispersion
- Population vs AED scatter analysis
- Radar charts for comprehensive comparison

## Tech Stack

- **Frontend Framework**: Vue.js 3.5
- **Build Tool**: Vite 7.3
- **Routing**: Vue Router 4.6
- **Charts**: ApexCharts 5.3 + Vue3-ApexCharts
- **Maps**: MapBox GL 3.17
- **Data Parsing**: PapaParse 5.5

## Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
2025-Taipei-City-Dashboard-Teamwork/
├── index.html
├── vite.config.js
├── package.json
├── src/
│   ├── main.js                 # App entry point
│   ├── App.vue                 # Root component
│   ├── style.css               # Global styles
│   ├── utils/
│   │   └── csvLoader.js        # CSV/GeoJSON data loader
│   ├── views/
│   │   ├── Overview.vue        # Overview dashboard
│   │   ├── AEDAnalysis.vue     # AED analysis page
│   │   ├── ShelterAnalysis.vue # Shelter analysis page
│   │   ├── AirRaidShelter.vue  # Air raid shelter page
│   │   ├── TouristSpotAnalysis.vue # Tourist spot page
│   │   └── ComparisonView.vue  # Comparison page
│   └── components/             # Reusable components
└── source/                     # Data files
    ├── component_ready/        # Processed CSV files
    ├── clean/                  # Cleaned data
    ├── topic/                  # Topic-specific data
    │   ├── taipei/
    │   └── newtaipeis/
    └── readme.md               # Data documentation
```

## Data Sources

All data is sourced from Taiwan government open data platforms:

1. **Population Statistics**: Ministry of Interior National Land Surveying and Mapping Center
2. **AED Locations**: National AED registry
3. **Air Raid Shelters**: Taipei/New Taipei City government datasets
4. **Evacuation Shelters**: Municipal emergency management datasets
5. **Emergency Services**: Fire and police department data
6. **Tourist Attractions**: Tourism Bureau statistics

## Analysis Methods

### Spatial Dispersion
Two complementary methods:
- **Euclidean Distance**: Average pairwise distance between facilities
- **Spatial Entropy**: Grid-based randomness and uniformity measure

### Population Ratio
- Facilities per 10,000 people
- People/households served per facility
- Resource adequacy grading

### Distance Analysis
- Haversine distance calculation for tourist spots
- 1km, 5km, and 10km radius resource counting

## MapBox Token

The dashboard uses MapBox GL for interactive maps. A token is pre-configured in the code. For production deployment, replace with your own token:

```javascript
mapboxgl.accessToken = 'YOUR_TOKEN_HERE'
```

Get a free token at: https://www.mapbox.com/

## Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Responsive design

## Development

### Adding New Visualizations

1. Create a new component in `src/views/`
2. Add route in `src/main.js`
3. Update navigation in `src/App.vue`
4. Load data using `src/utils/csvLoader.js`

### Data Processing

All data files are loaded from the `/source/` directory. CSV files are parsed with PapaParse, and GeoJSON files are loaded as JSON.

## Production Deployment

```bash
# Build static files
npm run build

# Deploy the dist/ folder to your hosting service
```

The build output is optimized for static hosting on platforms like:
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront

## License

ISC

## Contributing

This project was developed for the 2025 Taipei City Dashboard Teamwork initiative. For questions or contributions, please open an issue on GitHub.

## Acknowledgments

- Taiwan Government Open Data Platform
- Taipei City Government
- New Taipei City Government
- MapBox for mapping services
- ApexCharts for visualization library
