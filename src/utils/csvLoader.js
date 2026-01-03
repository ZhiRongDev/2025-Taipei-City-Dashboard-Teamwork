import Papa from 'papaparse'

export async function loadCSV(path) {
  const response = await fetch(path)
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
  const response = await fetch(path)
  return await response.json()
}
