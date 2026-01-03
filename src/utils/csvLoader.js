import Papa from 'papaparse'

function getAssetPath(path) {
  const base = import.meta.env.BASE_URL || '/'
  return path.startsWith('/') ? `${base}${path.slice(1)}` : path
}

export async function loadCSV(path) {
  const fullPath = getAssetPath(path)
  const response = await fetch(fullPath)
  const csvText = await response.text()

  return new Promise((resolve, reject) => {
    Papa.parse(csvText, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: (results) => resolve(results.data),
      error: (error) => reject(error)
    })
  })
}

export async function loadGeoJSON(path) {
  const fullPath = getAssetPath(path)
  const response = await fetch(fullPath)
  return await response.json()
}
