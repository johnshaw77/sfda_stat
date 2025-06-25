# SFDA 統計學 API 功能增強 TODO

> 針對 MCP 專案使用的簡化統計功能擴展計劃

## 📋 總體目標

為 MCP 專案提供更完整的統計分析功能，專注於實用性和易用性，避免過度複雜的架構設計。

## 🎯 階段一：基礎功能補強 (預估 2-3 週)

### ✅ 準備工作

- [ ] **安裝新套件**
  ```bash
  pip install pingouin>=0.5.3
  ```

- [ ] **更新 requirements.txt**
  ```
  新增: pingouin==0.5.3
  ```

### 🔧 1. 非參數統計檢定 (app/api/inferential.py)

- [ ] **新增 Mann-Whitney U 檢定端點**
  - 路由: `POST /api/v1/inferential/mann_whitney`
  - 功能: 雙樣本獨立非參數檢定
  - 回傳: U統計量、p值、效果量、解釋

- [ ] **新增 Wilcoxon 符號等級檢定端點**
  - 路由: `POST /api/v1/inferential/wilcoxon`
  - 功能: 配對樣本非參數檢定
  - 回傳: W統計量、p值、效果量、解釋

- [ ] **新增 Kruskal-Wallis 檢定端點**
  - 路由: `POST /api/v1/inferential/kruskal_wallis`
  - 功能: 多組獨立非參數檢定
  - 回傳: H統計量、p值、效果量、解釋

- [ ] **實現對應的服務類別** (app/services/inferential_stats.py)
  - `mann_whitney_test()` 方法
  - `wilcoxon_test()` 方法  
  - `kruskal_wallis_test()` 方法

- [ ] **新增請求/回應模型** (app/models/)
  - `MannWhitneyRequest/Response`
  - `WilcoxonRequest/Response`
  - `KruskalWallisRequest/Response`

### 📊 2. 效果量自動計算增強

- [ ] **增強現有 t 檢定**
  - 自動計算 Cohen's d
  - 添加效果量解釋 (小/中/大效果)
  - 更新回應模型包含效果量字段

- [ ] **增強現有 ANOVA**
  - 自動計算 Eta 平方 (η²)
  - 添加效果量解釋
  - 更新回應模型

- [ ] **增強現有相關分析**
  - 自動計算決定係數 (r²)
  - 添加相關強度解釋
  - 更新回應模型

### 📈 3. 統計圖表擴展 (app/api/charts.py)

- [ ] **新增直方圖端點**
  - 路由: `POST /api/v1/charts/histogram`
  - 功能: 數據分佈視覺化
  - 參數: 數據、bins數量、標題

- [ ] **新增盒鬚圖端點**
  - 路由: `POST /api/v1/charts/boxplot`
  - 功能: 分佈比較和異常值檢測
  - 參數: 單組或多組數據

- [ ] **新增散點圖端點**
  - 路由: `POST /api/v1/charts/scatter`
  - 功能: 雙變量關係視覺化
  - 參數: x, y 數據、迴歸線選項

- [ ] **實現對應的圖表服務** (app/services/chart_service.py)
  - `create_histogram()` 方法
  - `create_boxplot()` 方法
  - `create_scatter()` 方法

### ✅ 測試

- [ ] **撰寫非參數檢定測試**
  - `test_mann_whitney_api.py`
  - `test_wilcoxon_api.py`
  - `test_kruskal_wallis_api.py`

- [ ] **測試效果量計算**
  - 驗證 Cohen's d 計算正確性
  - 驗證 Eta 平方計算正確性

- [ ] **測試新圖表功能**
  - 驗證圖表數據結構
  - 測試參數驗證

## 🚀 階段二：實用功能擴展 (預估 2-3 週)

### 📊 4. 分佈檢定增強 (app/api/distribution.py)

- [ ] **新增 Q-Q 圖生成端點**
  - 路由: `POST /api/v1/distribution/qq_plot`
  - 功能: 常態性視覺化檢驗
  - 回傳: 圖表數據 + 常態性評估

- [ ] **增強多重常態性檢定端點**
  - 路由: `POST /api/v1/distribution/multiple_normality_test`
  - 功能: 同時執行多種常態性檢定
  - 回傳: Shapiro-Wilk、Kolmogorov-Smirnov、Anderson-Darling 結果

### 🔍 5. 迴歸診斷基礎 (app/api/regression.py)

- [ ] **新增基本迴歸診斷端點**
  - 路由: `POST /api/v1/regression/diagnostics`
  - 功能: 殘差分析、影響點檢測
  - 回傳: 殘差統計、R² 調整、異常值警告

### ✅ 測試

- [ ] **測試分佈檢定功能**
- [ ] **測試迴歸診斷功能**

## 🎯 階段三：進階實用功能 (預估 3-4 週)

### 📊 6. 多組比較

- [ ] **新增多重比較校正端點**
  - 路由: `POST /api/v1/inferential/multiple_comparison`
  - 功能: Bonferroni、Holm、FDR 校正
  - 用途: ANOVA 後續分析

### 🧮 7. 實用統計工具

- [ ] **新增樣本數計算端點**
  - 路由: `POST /api/v1/utils/sample_size`
  - 功能: 基於效果量計算所需樣本數
  - 適用: t檢定、ANOVA、相關分析

- [ ] **新增信賴區間計算端點**
  - 路由: `POST /api/v1/utils/confidence_interval`
  - 功能: 各種統計量的信賴區間
  - 適用: 平均數、比例、差異

### ✅ 最終測試

- [ ] **完整功能測試**
- [ ] **MCP 整合測試**
- [ ] **效能測試**

## 📚 文檔更新

- [ ] **更新 CLAUDE.md**
  - 新增功能說明
  - 更新指令範例
  - 新增使用建議

- [ ] **更新 API 文檔**
  - 新端點說明
  - 參數格式
  - 回應範例

- [ ] **撰寫 MCP 使用指南**
  - 常用統計分析流程
  - 最佳實踐建議

## 🔧 技術債務處理

- [ ] **程式碼品質**
  - 執行 `black app/ tests/`
  - 執行 `flake8 app/ tests/`
  - 執行 `mypy app/`

- [ ] **測試覆蓋率**
  - 目標: 達到 85% 以上覆蓋率
  - 執行 `pytest --cov=app --cov-report=html`

## 📈 驗收標準

### 功能性需求
- ✅ 所有新端點正常運作
- ✅ 統計計算結果正確
- ✅ 錯誤處理完善
- ✅ API 回應格式一致

### 非功能性需求
- ✅ 單次 API 調用響應時間 < 2 秒
- ✅ 支援樣本數至少 10,000 筆
- ✅ 記憶體使用穩定
- ✅ 與現有功能完全相容

### MCP 整合需求
- ✅ 適合 MCP 工具單次調用
- ✅ 結果易於解釋和使用
- ✅ 參數設計簡潔直觀

## 📅 時程安排

| 階段 | 內容 | 預估時間 | 完成日期 |
|------|------|----------|----------|
| 階段一 | 非參數檢定 + 效果量 + 圖表 | 2-3 週 | _待填入_ |
| 階段二 | 分佈檢定 + 迴歸診斷 | 2-3 週 | _待填入_ |
| 階段三 | 多重比較 + 實用工具 | 3-4 週 | _待填入_ |
| 文檔 | 更新文檔和測試 | 1 週 | _待填入_ |

## 🎉 專案完成指標

- [ ] 統計功能完整度從 75% 提升至 90%
- [ ] 支援完整的統計分析工作流程
- [ ] MCP 專案可以無縫使用所有新功能
- [ ] 測試覆蓋率達到 85% 以上
- [ ] 文檔完整且易於理解

---

**注意事項**:
1. 保持現有 API 完全向後相容
2. 優先實現最常用的功能
3. 注重 MCP 使用體驗的簡潔性
4. 每完成一個功能立即進行測試驗證