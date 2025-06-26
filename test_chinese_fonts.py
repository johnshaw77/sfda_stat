#!/usr/bin/env python3
"""
測試中文字體可用性
"""

from app.services.chart_service import ChartService
import matplotlib.font_manager as fm

def test_chinese_fonts():
    """測試中文字體"""
    print("🔍 檢查系統可用的中文字體...")
    
    chart_service = ChartService()
    
    # 列出可用的中文字體
    chinese_fonts = chart_service.list_available_chinese_fonts()
    print(f"\n找到 {len(chinese_fonts)} 個可能的中文字體:")
    for i, font in enumerate(chinese_fonts, 1):
        print(f"  {i}. {font}")
    
    # 測試圖表生成
    print(f"\n📊 測試中文圖表生成...")
    from app.models.chart_models import ChartDataPoint
    
    test_data = [
        ChartDataPoint(label="蘋果", value=30),
        ChartDataPoint(label="香蕉", value=25),
        ChartDataPoint(label="橘子", value=20),
        ChartDataPoint(label="草莓", value=25)
    ]
    
    result = chart_service.create_pie_chart(
        data=test_data,
        title="水果銷售比例圖",
        generate_image=True,
        image_format="png"
    )
    
    print(f"圖表生成成功: {result.success}")
    print(f"包含圖片: {result.has_image}")
    if result.image_base64:
        print(f"Base64 長度: {len(result.image_base64)}")
        
        # 儲存圖片進行檢查
        import base64
        try:
            decoded = base64.b64decode(result.image_base64)
            with open("chinese_font_test.png", "wb") as f:
                f.write(decoded)
            print("✅ 測試圖片已儲存為 chinese_font_test.png")
        except Exception as e:
            print(f"❌ 儲存圖片失敗: {e}")

if __name__ == "__main__":
    test_chinese_fonts()