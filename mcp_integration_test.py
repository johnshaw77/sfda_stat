#!/usr/bin/env python3
"""
MCP 整合測試腳本
快速驗證 sfda_stat 後端服務是否滿足 MCP 工具需求
"""

import requests
import time
import json

# 測試基礎 URL
BASE_URL = "http://localhost:8000"

def test_api_response_time(endpoint, data, max_time=2.0):
    """測試 API 響應時間"""
    start_time = time.time()
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        end_time = time.time()
        
        response_time = end_time - start_time
        success = response.status_code == 200 and response_time < max_time
        
        print(f"{'✅' if success else '❌'} {endpoint}")
        print(f"   響應時間: {response_time:.3f}s (限制: {max_time}s)")
        print(f"   狀態碼: {response.status_code}")
        
        if success:
            result = response.json()
            print(f"   回應格式: {'✅ 正常' if 'success' in result else '⚠️ 需檢查'}")
        
        return success
    except Exception as e:
        print(f"❌ {endpoint} - 錯誤: {str(e)}")
        return False

def main():
    """執行 MCP 整合測試"""
    print("🧪 MCP 後端服務整合測試")
    print("=" * 50)
    
    # 測試案例：模擬真實 MCP 工具調用
    test_cases = [
        {
            "name": "Mann-Whitney 檢定",
            "endpoint": "/api/v1/inferential/mann_whitney",
            "data": {
                "sample1": [10, 12, 14, 16, 18],
                "sample2": [8, 10, 12, 14, 16],
                "alpha": 0.05,
                "alternative": "two-sided"
            }
        },
        {
            "name": "T 檢定",
            "endpoint": "/api/v1/inferential/ttest", 
            "data": {
                "sample1": [140, 138, 145, 142, 139],
                "sample2": [128, 125, 132, 129, 126],
                "paired": True,
                "alpha": 0.05
            }
        },
        {
            "name": "盒鬚圖創建",
            "endpoint": "/api/v1/charts/boxplot",
            "data": {
                "groups": [[75, 82, 78, 85], [68, 74, 71, 77]],
                "group_labels": ["組A", "組B"],
                "title": "測試盒鬚圖",
                "generate_image": True
            }
        },
        {
            "name": "直方圖創建", 
            "endpoint": "/api/v1/charts/histogram",
            "data": {
                "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "bins": 5,
                "title": "測試直方圖",
                "generate_image": True
            }
        }
    ]
    
    # 執行測試
    total_tests = len(test_cases)
    passed_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/{total_tests}] 測試: {test_case['name']}")
        if test_api_response_time(test_case['endpoint'], test_case['data']):
            passed_tests += 1
    
    # 測試結果
    print("\n" + "=" * 50)
    print(f"🎯 測試結果: {passed_tests}/{total_tests} 通過")
    
    if passed_tests == total_tests:
        print("✅ 所有 MCP 整合測試通過！後端服務準備就緒。")
    else:
        print("❌ 部分測試失敗，需要檢查後端服務。")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    main()