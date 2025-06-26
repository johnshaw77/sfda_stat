from fastapi import APIRouter, HTTPException
from app.models.chart_models import (
    CreatePieChartRequest,
    CreateBarChartRequest,
    CreateLineChartRequest,
    SimpleChartRequest,
    HistogramRequest,
    BoxplotRequest,
    ScatterRequest,
    ChartResponse,
)
from app.services.chart_service import ChartService

router = APIRouter()
chart_service = ChartService()


@router.post("/pie", response_model=ChartResponse)
async def create_pie_chart(request: CreatePieChartRequest):
    """
    創建圓餅圖

    用於顯示各部分占整體的比例關係
    """
    try:
        return chart_service.create_pie_chart(request.data, request.title)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bar", response_model=ChartResponse)
async def create_bar_chart(request: CreateBarChartRequest):
    """
    創建長條圖

    用於比較不同類別的數值大小
    """
    try:
        return chart_service.create_bar_chart(
            request.data, 
            request.title, 
            request.x_axis_label, 
            request.y_axis_label
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/line", response_model=ChartResponse)
async def create_line_chart(request: CreateLineChartRequest):
    """
    創建折線圖

    用於顯示數據隨時間或其他連續變量的變化趨勢
    """
    try:
        return chart_service.create_line_chart(
            request.data, 
            request.title, 
            request.x_axis_label, 
            request.y_axis_label
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/simple", response_model=ChartResponse)
async def create_simple_chart(request: SimpleChartRequest):
    """
    創建簡單圖表

    接受標籤和數值數組，根據指定類型創建圖表
    這是最常用的端點，適合 MCP 工具調用
    支援圖片生成功能 (設定 generate_image=true)
    """
    try:
        if request.generate_image:
            return chart_service.create_chart_from_simple_data_with_image(
                labels=request.labels,
                values=request.values,
                chart_type=request.chart_type,
                title=request.title,
                generate_image=True,
                image_format=request.image_format,
                figsize=request.figsize,
                dpi=request.dpi
            )
        else:
            return chart_service.create_chart_from_simple_data(
                request.labels,
                request.values,
                request.chart_type,
                request.title
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/histogram", response_model=ChartResponse)
async def create_histogram(request: HistogramRequest):
    """
    創建直方圖

    用於顯示數據的分佈情況和頻率
    適用於：
    - 數據分佈視覺化
    - 常態性檢查
    - 異常值識別
    """
    try:
        return chart_service.create_histogram(
            values=request.values,
            bins=request.bins,
            title=request.title,
            x_axis_label=request.x_axis_label,
            y_axis_label=request.y_axis_label
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/boxplot", response_model=ChartResponse)
async def create_boxplot(request: BoxplotRequest):
    """
    創建盒鬚圖

    用於比較多組數據的分佈和識別異常值
    適用於：
    - 組間比較
    - 異常值檢測
    - 分佈形狀比較
    """
    try:
        return chart_service.create_boxplot(
            groups=request.groups,
            group_labels=request.group_labels,
            title=request.title,
            y_axis_label=request.y_axis_label
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/scatter", response_model=ChartResponse)
async def create_scatter(request: ScatterRequest):
    """
    創建散點圖

    用於顯示兩個變數之間的關係
    適用於：
    - 相關性視覺化
    - 線性關係檢查
    - 回歸分析視覺化
    支援圖片生成功能 (設定 generate_image=true)
    """
    try:
        return chart_service.create_scatter(
            x=request.x,
            y=request.y,
            title=request.title,
            x_axis_label=request.x_axis_label,
            y_axis_label=request.y_axis_label,
            show_regression_line=request.show_regression_line,
            generate_image=request.generate_image,
            image_format=request.image_format,
            figsize=request.figsize,
            dpi=request.dpi
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def chart_health_check():
    """
    圖表服務健康檢查
    """
    return {
        "status": "healthy",
        "service": "chart_service",
        "supported_types": ["pie", "bar", "line", "histogram", "boxplot", "scatter"]
    } 