# GitHub Pages 部署指南

## 自動部署設置

此專案已配置自動部署到 GitHub Pages。當你推送到 `main` 分支時，會自動觸發部署流程。

---

## 🚀 部署流程

### 1. 推送到 main 分支
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### 2. 自動構建和部署
GitHub Actions 會自動：
1. ✅ 檢出代碼
2. ✅ 安裝 Node.js 20
3. ✅ 安裝依賴 (`npm ci`)
4. ✅ 構建應用 (`npm run build`)
5. ✅ 部署到 GitHub Pages

### 3. 查看部署狀態
訪問你的 repository 的 **Actions** 標籤頁：
```
https://github.com/ZhiRongDev/2025-Taipei-City-Dashboard-Teamwork/actions
```

---

## 🌐 網站 URL

部署成功後，你的應用將可在以下網址訪問：

```
https://zhirongdev.github.io/2025-Taipei-City-Dashboard-Teamwork/
```

---

## ⚙️ 首次設置（僅需一次）

### 步驟 1: 啟用 GitHub Pages

1. 前往你的 repository 設置頁面：
   ```
   https://github.com/ZhiRongDev/2025-Taipei-City-Dashboard-Teamwork/settings/pages
   ```

2. 在 **Build and deployment** 區域：
   - **Source**: 選擇 **GitHub Actions**
   - 保存設置

### 步驟 2: 推送代碼

```bash
git add .github/workflows/deploy.yml
git add vite.config.js
git add public/.nojekyll
git add DEPLOYMENT_GUIDE.md
git commit -m "Add GitHub Pages deployment workflow"
git push origin main
```

### 步驟 3: 等待部署完成

- 前往 [Actions 頁面](https://github.com/ZhiRongDev/2025-Taipei-City-Dashboard-Teamwork/actions)
- 查看 "Deploy to GitHub Pages" workflow
- 等待綠色勾選標記 ✅
- 部署通常需要 2-3 分鐘

---

## 📁 相關檔案

### 1. `.github/workflows/deploy.yml`
GitHub Actions 工作流程配置檔案：
- 當推送到 `main` 分支時觸發
- 自動安裝依賴、構建和部署

### 2. `vite.config.js`
Vite 配置檔案：
```javascript
base: process.env.NODE_ENV === 'production'
  ? '/2025-Taipei-City-Dashboard-Teamwork/'
  : '/'
```
- 開發環境：使用 `/` 作為基礎路徑
- 生產環境：使用 `/2025-Taipei-City-Dashboard-Teamwork/` 作為基礎路徑

### 3. `public/.nojekyll`
空檔案，告訴 GitHub Pages 不要使用 Jekyll 處理：
- 確保以 `_` 開頭的檔案不被忽略
- 確保 Vue Router 正常工作

---

## 🔧 本地測試生產構建

在推送到 GitHub 之前，你可以在本地測試生產構建：

```bash
# 構建應用
npm run build

# 預覽構建結果
npm run preview
```

預覽 URL：`http://localhost:4173/2025-Taipei-City-Dashboard-Teamwork/`

---

## 🐛 故障排除

### 問題 1: 部署失敗

**檢查**：
- 訪問 [Actions 頁面](https://github.com/ZhiRongDev/2025-Taipei-City-Dashboard-Teamwork/actions)
- 查看失敗的工作流程日誌
- 檢查構建錯誤訊息

**常見原因**：
- `package-lock.json` 與 `package.json` 不同步
- 構建過程中有編譯錯誤
- 缺少必要的環境變數

**解決方案**：
```bash
# 重新生成 package-lock.json
rm package-lock.json
npm install

# 本地測試構建
npm run build

# 推送修復
git add package-lock.json
git commit -m "Fix package-lock.json"
git push origin main
```

### 問題 2: 頁面顯示空白或 404

**檢查**：
- `vite.config.js` 中的 `base` 路徑是否正確
- GitHub Pages 設置中的 Source 是否選擇了 "GitHub Actions"

**解決方案**：
```bash
# 確認 base URL 正確
cat vite.config.js | grep base

# 應該顯示：
# base: process.env.NODE_ENV === 'production'
#   ? '/2025-Taipei-City-Dashboard-Teamwork/'
#   : '/'
```

### 問題 3: 資源載入 404

**檢查**：
- 資源路徑是否使用相對路徑
- `public/.nojekyll` 檔案是否存在

**解決方案**：
```bash
# 確保 .nojekyll 檔案存在
ls -la public/.nojekyll

# 如果不存在，創建它
touch public/.nojekyll
git add public/.nojekyll
git commit -m "Add .nojekyll file"
git push origin main
```

### 問題 4: 路由刷新後 404

這是 SPA 應用在 GitHub Pages 上的常見問題。

**解決方案 1**: 使用 Hash 模式路由（已實現）
在 `src/router/index.js` 中使用 `createWebHashHistory`：
```javascript
import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [...]
})
```

**解決方案 2**: 使用 404.html 重定向
如果使用 HTML5 History 模式，需要添加 `404.html`：
```bash
cp public/index.html public/404.html
```

---

## 📊 工作流程詳解

### Build Job
```yaml
- Checkout code
- Setup Node.js 20
- Install dependencies (npm ci)
- Build application (npm run build)
- Upload build artifact
```

### Deploy Job
```yaml
- Deploy artifact to GitHub Pages
- Set deployment URL
```

### 權限
```yaml
permissions:
  contents: read    # 讀取代碼
  pages: write      # 寫入 GitHub Pages
  id-token: write   # 生成部署令牌
```

### 並發控制
```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false  # 不取消進行中的部署
```

---

## 🎯 部署檢查清單

在推送到 main 之前：

- [ ] 本地構建成功 (`npm run build`)
- [ ] 本地預覽正常 (`npm run preview`)
- [ ] 所有測試通過
- [ ] 提交訊息清晰明確
- [ ] `.github/workflows/deploy.yml` 存在
- [ ] `public/.nojekyll` 存在
- [ ] `vite.config.js` base URL 正確

---

## 📈 監控部署

### GitHub Actions 頁面
```
https://github.com/ZhiRongDev/2025-Taipei-City-Dashboard-Teamwork/actions
```

### Environments 頁面
```
https://github.com/ZhiRongDev/2025-Taipei-City-Dashboard-Teamwork/deployments
```

### 部署歷史
每次推送到 main 都會創建一個新的部署記錄，你可以：
- 查看部署狀態（成功/失敗）
- 查看部署時間
- 查看部署日誌
- 回滾到之前的版本（需要手動操作）

---

## 🔄 更新部署

只需要推送到 main 分支，其他的自動完成！

```bash
# 日常工作流程
git add .
git commit -m "Update feature X"
git push origin main

# 等待 2-3 分鐘
# 訪問 https://zhirongdev.github.io/2025-Taipei-City-Dashboard-Teamwork/
```

---

## 🌟 最佳實踐

1. **使用有意義的提交訊息**
   ```bash
   git commit -m "Add spatial metrics to all analysis pages"
   ```

2. **本地測試後再推送**
   ```bash
   npm run build && npm run preview
   ```

3. **小步提交，頻繁部署**
   - 每個功能單獨提交
   - 方便追蹤問題
   - 容易回滾

4. **監控部署狀態**
   - 推送後檢查 Actions 頁面
   - 確認部署成功
   - 訪問網站驗證

---

## 📞 需要幫助？

如果遇到問題：

1. 檢查 [GitHub Actions 日誌](https://github.com/ZhiRongDev/2025-Taipei-City-Dashboard-Teamwork/actions)
2. 參考上面的故障排除部分
3. 查看 [GitHub Pages 文檔](https://docs.github.com/en/pages)
4. 查看 [Vite 部署文檔](https://vitejs.dev/guide/static-deploy.html)

---

**部署配置完成日期**: 2026-01-03  
**配置者**: Claude Sonnet 4.5
