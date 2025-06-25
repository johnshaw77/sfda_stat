# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

SFDA 統計學分析 API - 使用 FastAPI 建構的統計學分析服務，提供描述性統計、推論統計、迴歸分析、相關性分析、機率分佈分析及圖表創建功能。

## 常用指令

### 環境設置
```bash
# 啟動 conda 環境
conda activate py310_stat

# 安裝相依套件
pip install -r requirements.txt
```

### 開發指令
```bash
# 啟動開發服務器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 執行測試
pytest tests/ -v --cov=app --cov-report=html

# 程式碼格式化
black app/ tests/
isort app/ tests/

# 程式碼品質檢查
flake8 app/ tests/
mypy app/
```

### 測試指令
```bash
# 執行所有測試
pytest

# 執行特定測試檔案
pytest tests/test_descriptive.py
pytest tests/test_ttest_api.py
pytest tests/test_realistic_scenarios.py

# 執行測試並生成覆蓋率報告
pytest --cov=app --cov-report=html --cov-report=term-missing
```

## 專案架構

### 核心架構設計
- **分層架構**: API Layer → Service Layer → Statistical Computing
- **模組化設計**: 按統計功能領域分組
- **無狀態計算**: 純函數式統計分析，無需數據庫

### 主要目錄結構
```
app/
├── main.py              # FastAPI 應用程式入口
├── api/                 # API 路由層
│   ├── descriptive.py   # 描述性統計 API
│   ├── inferential.py   # 推論統計 API
│   ├── regression.py    # 迴歸分析 API
│   ├── correlation.py   # 相關性分析 API
│   ├── distribution.py  # 機率分佈 API
│   └── charts.py        # 圖表創建 API
├── services/            # 業務邏輯層
│   ├── descriptive_stats.py      # 描述性統計服務
│   ├── inferential_stats.py      # 推論統計服務
│   ├── regression_analysis.py    # 迴歸分析服務
│   ├── correlation_analysis.py   # 相關性分析服務
│   ├── distribution_analysis.py  # 分佈分析服務
│   └── chart_service.py          # 圖表服務
└── models/              # 資料模型層
    ├── request_models.py   # 請求模型
    ├── response_models.py  # 回應模型
    └── chart_models.py     # 圖表模型
```

### API 路由設計
所有 API 端點使用 `/api/v1/` 前綴：

- **描述性統計** (`/api/v1/descriptive/`): basic, distribution, percentiles
- **推論統計** (`/api/v1/inferential/`): ttest, chisquare, anova  
- **迴歸分析** (`/api/v1/regression/`): linear, multiple, polynomial
- **相關性分析** (`/api/v1/correlation/`): pearson, spearman, kendall, matrix
- **機率分佈** (`/api/v1/distribution/`): normal, test
- **圖表創建** (`/api/v1/charts/`): pie, bar, line, simple

## 技術棧與相依套件

### 核心技術
- **FastAPI**: 現代化 Web 框架，自動產生 API 文檔
- **NumPy**: 高效數值計算基礎
- **SciPy**: 統計函數和科學計算
- **Pandas**: 資料處理和分析
- **scikit-learn**: 機器學習和迴歸分析
- **Pydantic**: 資料驗證和序列化

### 開發工具
- **pytest**: 測試框架
- **black**: 程式碼格式化
- **isort**: import 排序
- **flake8**: 程式碼檢查
- **mypy**: 靜態類型檢查

## 統計功能實作要點

### 資料驗證策略
- 使用 Pydantic 模型進行嚴格的輸入驗證
- 檢查最小樣本數要求（如 t 檢定需要至少 2 個數值）
- 數值範圍和類型驗證
- 提供詳細的錯誤訊息

### 統計計算原則
- 使用科學計算庫確保數值穩定性
- 回傳完整統計資訊：統計量、p 值、置信區間、效應量
- 提供統計結果的解釋和建議
- 處理邊界條件和異常情況

### 回應格式標準化
所有統計分析都回傳結構化的 JSON，包含：
- 描述性統計：mean, median, std_dev, variance, min, max
- 假設檢定：statistic, p_value, confidence_interval, interpretation
- 迴歸分析：coefficients, r_squared, f_statistic, residuals

## 測試策略

### 測試資料
`test_data/` 目錄包含豐富的測試資料集：
- 標準統計分佈資料
- 真實場景資料（醫療、教育、工業等）
- 涵蓋各種統計檢定情境

### 測試場景
- **基礎功能測試**: API 連通性和基本統計功能
- **專項功能測試**: 針對特定統計方法的深度測試
- **真實場景測試**: 模擬實際應用情境的整合測試

### 關鍵測試檔案
- `test_descriptive.py`: 描述性統計基礎測試
- `test_ttest_api.py`: t 檢定專項測試
- `test_realistic_scenarios.py`: 五個真實場景的完整測試流程

## 開發環境

### 環境管理
專案使用 `conda` 進行 Python 環境管理：
```bash
# 啟動環境
conda activate py310_stat

# 安裝套件
pip install -r requirements.txt
```

### 程式碼品質
- 使用 `black` 進行一致的程式碼格式化（行長度 88）
- 使用 `isort` 管理 import 順序
- 使用 `mypy` 進行靜態類型檢查
- 使用 `flake8` 進行程式碼風格檢查

### API 文檔
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康檢查端點: http://localhost:8000/health