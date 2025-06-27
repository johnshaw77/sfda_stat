#!/usr/bin/env python3
"""
完整 MCP 整合測試
測試 MCP Server → sfda_stat 後端 的完整調用鏈
"""

import requests
import time
import json

def test_backend_api():
    """測試 sfda_stat 後端 API"""
    print("🧪 測試 sfda_stat 後端服務")
    print("-" * 40)
    
    backend_url = "http://localhost:8000"
    
    # 檢查服務是否運行
    try:
        response = requests.get(f"{backend_url}/")
        if response.status_code == 200:
            print("✅ sfda_stat 後端服務運行正常")
        else:
            print("❌ sfda_stat 後端服務異常")
            return False
    except:
        print("❌ sfda_stat 後端服務未啟動")
        return False
    
    # 測試關鍵統計功能
    test_cases = [
        {
            "name": "Mann-Whitney U 檢定",
            "endpoint": "/api/v1/inferential/mann_whitney",
            "data": {
                "sample1": [10, 12, 14, 16, 18],
                "sample2": [8, 10, 12, 14, 16],
                "alpha": 0.05
            }
        },
        {
            "name": "T 檢定",
            "endpoint": "/api/v1/inferential/ttest",
            "data": {
                "sample1": [140, 138, 145, 142, 139],
                "sample2": [128, 125, 132, 129, 126],
                "paired": True
            }
        },
        {
            "name": "Wilcoxon 檢定",
            "endpoint": "/api/v1/inferential/wilcoxon", 
            "data": {
                "sample1": [8, 7, 9, 6, 8],
                "sample2": [5, 4, 6, 3, 5]
            }
        },
        {
            "name": "Kruskal-Wallis 檢定",
            "endpoint": "/api/v1/inferential/kruskal_wallis",
            "data": {
                "groups": [
                    [75, 78, 72, 80],
                    [82, 85, 81, 88], 
                    [88, 92, 89, 95]
                ]
            }
        },
        {
            "name": "ANOVA 檢定",
            "endpoint": "/api/v1/inferential/anova",
            "data": {
                "groups": [
                    [3.2, 3.8, 3.1],
                    [5.1, 5.8, 5.2],
                    [7.2, 7.9, 7.1]
                ]
            }
        },
        {
            "name": "卡方檢定",
            "endpoint": "/api/v1/inferential/chisquare",
            "data": {
                "observed": [[35, 15], [42, 8]]
            }
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        try:
            start_time = time.time()
            response = requests.post(
                f"{backend_url}{test_case['endpoint']}", 
                json=test_case['data']
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {test_case['name']} - {end_time - start_time:.3f}s")
                
                # 檢查基本回應格式
                if 'success' in result or 'p_value' in result:
                    print(f"   📊 回應格式正確")
                else:
                    print(f"   ⚠️ 回應格式可能需要檢查")
                
                passed += 1
            else:
                print(f"❌ {test_case['name']} - 狀態碼: {response.status_code}")
                if response.status_code == 422:
                    error_detail = response.json().get('detail', [])
                    print(f"   錯誤: {error_detail}")
        except Exception as e:
            print(f"❌ {test_case['name']} - 錯誤: {str(e)}")
    
    print(f"\n📊 後端測試結果: {passed}/{total} 通過")
    return passed == total

def test_mcp_server():
    """測試 MCP Server 端點"""
    print("\n🚀 測試 MCP Server 端點")
    print("-" * 40)
    
    mcp_url = "http://localhost:8080"
    
    # 檢查服務是否運行
    try:
        response = requests.get(f"{mcp_url}/health")
        if response.status_code == 200:
            print("✅ MCP Server 運行正常")
        else:
            print("❌ MCP Server 異常")
            return False
    except:
        print("❌ MCP Server 未啟動，跳過 MCP 端點測試")
        return None
    
    # 測試 MCP 工具端點
    mcp_test_cases = [
        {
            "name": "MCP Mann-Whitney 工具",
            "endpoint": "/api/stat/perform_mann_whitney",
            "data": {
                "data": {
                    "sample1": [10, 12, 14, 16, 18],
                    "sample2": [8, 10, 12, 14, 16]
                }
            }
        },
        {
            "name": "MCP T 檢定工具",
            "endpoint": "/api/stat/perform_ttest",
            "data": {
                "data": {
                    "sample1": [140, 138, 145, 142, 139],
                    "sample2": [128, 125, 132, 129, 126],
                    "test_type": "paired"
                }
            }
        }
    ]
    
    passed = 0
    total = len(mcp_test_cases)
    
    for test_case in mcp_test_cases:
        try:
            start_time = time.time()
            response = requests.post(
                f"{mcp_url}{test_case['endpoint']}", 
                json=test_case['data']
            )
            end_time = time.time()
            
            if response.status_code == 200:
                print(f"✅ {test_case['name']} - {end_time - start_time:.3f}s")
                passed += 1
            else:
                print(f"❌ {test_case['name']} - 狀態碼: {response.status_code}")
        except Exception as e:
            print(f"❌ {test_case['name']} - 錯誤: {str(e)}")
    
    print(f"\n📊 MCP Server 測試結果: {passed}/{total} 通過")
    return passed == total

def main():
    """執行完整整合測試"""
    print("🔬 完整 MCP 整合測試")
    print("=" * 50)
    
    # 測試後端服務
    backend_ok = test_backend_api()
    
    # 測試 MCP Server（如果運行的話）
    mcp_ok = test_mcp_server()
    
    # 總結
    print("\n" + "=" * 50)
    print("📋 測試總結:")
    print(f"   sfda_stat 後端: {'✅ 通過' if backend_ok else '❌ 失敗'}")
    
    if mcp_ok is None:
        print(f"   MCP Server: ⚠️ 未啟動（可稍後測試）")
    else:
        print(f"   MCP Server: {'✅ 通過' if mcp_ok else '❌ 失敗'}")
    
    # 建議
    print("\n💡 建議:")
    if backend_ok:
        print("✅ sfda_stat 後端服務完全滿足 MCP 需求")
        if mcp_ok is None:
            print("🚀 請啟動 MCP Server 測試完整調用鏈")
        elif mcp_ok:
            print("🎉 完整 MCP 整合測試通過！系統準備就緒")
        else:
            print("🔧 需要檢查 MCP Server 的參數對應")
    else:
        print("🔧 需要修復 sfda_stat 後端的 API 問題")

if __name__ == "__main__":
    main()