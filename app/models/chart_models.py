from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field


class ChartDataPoint(BaseModel):
    """圖表數據點模型"""
    label: str = Field(..., description="標籤")
    value: float = Field(..., description="數值")


class CreatePieChartRequest(BaseModel):
    """創建圓餅圖請求模型"""
    data: List[ChartDataPoint] = Field(..., description="圖表數據", min_items=1)
    title: Optional[str] = Field(None, description="圖表標題")
    generate_image: bool = Field(False, description="是否生成圖片")
    image_format: str = Field("png", description="圖片格式 (png, jpg, svg)")
    figsize: Optional[Tuple[int, int]] = Field((10, 8), description="圖片大小 (寬, 高)")
    dpi: int = Field(100, description="圖片解析度")


class CreateBarChartRequest(BaseModel):
    """創建長條圖請求模型"""
    data: List[ChartDataPoint] = Field(..., description="圖表數據", min_items=1)
    title: Optional[str] = Field(None, description="圖表標題")
    x_axis_label: Optional[str] = Field(None, description="X軸標籤")
    y_axis_label: Optional[str] = Field(None, description="Y軸標籤")
    generate_image: bool = Field(False, description="是否生成圖片")
    image_format: str = Field("png", description="圖片格式 (png, jpg, svg)")
    figsize: Optional[Tuple[int, int]] = Field((10, 6), description="圖片大小 (寬, 高)")
    dpi: int = Field(100, description="圖片解析度")


class CreateLineChartRequest(BaseModel):
    """創建折線圖請求模型"""
    data: List[ChartDataPoint] = Field(..., description="圖表數據", min_items=2)
    title: Optional[str] = Field(None, description="圖表標題")
    x_axis_label: Optional[str] = Field(None, description="X軸標籤")
    y_axis_label: Optional[str] = Field(None, description="Y軸標籤")
    generate_image: bool = Field(False, description="是否生成圖片")
    image_format: str = Field("png", description="圖片格式 (png, jpg, svg)")
    figsize: Optional[Tuple[int, int]] = Field((10, 6), description="圖片大小 (寬, 高)")
    dpi: int = Field(100, description="圖片解析度")


class ChartResponse(BaseModel):
    """圖表響應模型"""
    success: bool = Field(..., description="是否成功")
    chart_type: str = Field(..., description="圖表類型")
    data: List[Dict[str, Any]] = Field(..., description="圖表數據")
    title: Optional[str] = Field(None, description="圖表標題")
    confidence: float = Field(1.0, description="信心度")
    reasoning: str = Field(..., description="創建原因")
    metadata: Optional[Dict[str, Any]] = Field(None, description="附加元數據")
    # 新增圖片相關欄位
    image_base64: Optional[str] = Field(None, description="Base64 編碼的圖片資料")
    image_format: Optional[str] = Field("png", description="圖片格式 (png, jpg, svg)")
    has_image: bool = Field(False, description="是否包含圖片")


class SimpleChartRequest(BaseModel):
    """簡化圖表請求模型 - 支援直接傳入標籤和數值"""
    labels: List[str] = Field(..., description="標籤陣列", min_items=1)
    values: List[float] = Field(..., description="數值陣列", min_items=1)
    title: Optional[str] = Field(None, description="圖表標題")
    chart_type: str = Field(..., description="圖表類型", pattern="^(pie|bar|line)$")
    generate_image: bool = Field(False, description="是否生成圖片")
    image_format: str = Field("png", description="圖片格式 (png, jpg, svg)")
    figsize: Optional[Tuple[int, int]] = Field((10, 6), description="圖片大小 (寬, 高)")
    dpi: int = Field(100, description="圖片解析度")


class HistogramRequest(BaseModel):
    """直方圖請求模型"""
    values: List[float] = Field(..., description="數值陣列", min_items=5)
    bins: Optional[int] = Field(10, description="直方圖區間數", ge=5, le=50)
    title: Optional[str] = Field(None, description="圖表標題")
    x_axis_label: Optional[str] = Field("數值", description="X軸標籤")
    y_axis_label: Optional[str] = Field("頻率", description="Y軸標籤")
    generate_image: bool = Field(False, description="是否生成圖片")
    image_format: str = Field("png", description="圖片格式 (png, jpg, svg)")
    figsize: Optional[Tuple[int, int]] = Field((10, 6), description="圖片大小 (寬, 高)")
    dpi: int = Field(100, description="圖片解析度")


class BoxplotRequest(BaseModel):
    """盒鬚圖請求模型"""
    groups: List[List[float]] = Field(..., description="各組數據", min_items=1)
    group_labels: Optional[List[str]] = Field(None, description="組別標籤")
    title: Optional[str] = Field(None, description="圖表標題")
    y_axis_label: Optional[str] = Field("數值", description="Y軸標籤")
    generate_image: bool = Field(False, description="是否生成圖片")
    image_format: str = Field("png", description="圖片格式 (png, jpg, svg)")
    figsize: Optional[Tuple[int, int]] = Field((10, 6), description="圖片大小 (寬, 高)")
    dpi: int = Field(100, description="圖片解析度")


class ScatterRequest(BaseModel):
    """散點圖請求模型"""
    x: List[float] = Field(..., description="X軸數據", min_items=3)
    y: List[float] = Field(..., description="Y軸數據", min_items=3)
    title: Optional[str] = Field(None, description="圖表標題")
    x_axis_label: Optional[str] = Field("X", description="X軸標籤")
    y_axis_label: Optional[str] = Field("Y", description="Y軸標籤")
    show_regression_line: bool = Field(False, description="是否顯示迴歸線")
    generate_image: bool = Field(False, description="是否生成圖片")
    image_format: str = Field("png", description="圖片格式 (png, jpg, svg)")
    figsize: Optional[Tuple[int, int]] = Field((10, 6), description="圖片大小 (寬, 高)")
    dpi: int = Field(100, description="圖片解析度") 