from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')  # 使用非互動式後端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import base64
import io
from app.models.chart_models import ChartDataPoint, ChartResponse


class ChartService:
    """圖表服務類"""
    
    def __init__(self):
        """初始化圖表服務，設定中文字體"""
        # 設定 matplotlib 支援中文
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 設定 seaborn 樣式
        sns.set_style("whitegrid")
        sns.set_palette("husl")

    def create_pie_chart(
        self, 
        data: List[ChartDataPoint], 
        title: Optional[str] = None,
        generate_image: bool = False,
        image_format: str = "png",
        figsize: Tuple[int, int] = (10, 8),
        dpi: int = 100
    ) -> ChartResponse:
        """
        創建圓餅圖
        
        Args:
            data: 圖表數據點列表
            title: 圖表標題
            
        Returns:
            ChartResponse: 圖表響應
        """
        try:
            # 驗證數據
            if not data:
                raise ValueError("數據不能為空")
            
            # 轉換數據格式，與現有 SmartChart 組件兼容
            chart_data = []
            for point in data:
                chart_data.append({
                    "label": point.label,
                    "value": point.value
                })
            
            # 計算總和用於驗證
            total_value = sum(point.value for point in data)
            
            response = ChartResponse(
                success=True,
                chart_type="pie",
                data=chart_data,
                title=title or "圓餅圖",
                confidence=1.0,
                reasoning=f"成功創建包含 {len(data)} 個數據點的圓餅圖，總值為 {total_value}",
                metadata={
                    "total_value": total_value,
                    "data_points_count": len(data)
                }
            )
            
            # 如果需要生成圖片
            if generate_image:
                try:
                    image_base64 = self._generate_chart_image(
                        chart_type="pie",
                        data=chart_data,
                        title=response.title or "圓餅圖",
                        metadata=response.metadata,
                        figsize=figsize,
                        dpi=dpi,
                        image_format=image_format
                    )
                    
                    if image_base64:
                        response.image_base64 = image_base64
                        response.image_format = image_format
                        response.has_image = True
                        response.reasoning += f"，並成功生成 {image_format.upper()} 圖片"
                    else:
                        response.reasoning += "，但圖片生成失敗"
                        
                except Exception as e:
                    response.reasoning += f"，但圖片生成失敗: {str(e)}"
            
            return response
            
        except Exception as e:
            return ChartResponse(
                success=False,
                chart_type="pie",
                data=[],
                title=title,
                confidence=0.0,
                reasoning=f"創建圓餅圖失敗: {str(e)}"
            )

    def create_bar_chart(
        self, 
        data: List[ChartDataPoint], 
        title: Optional[str] = None,
        x_axis_label: Optional[str] = None,
        y_axis_label: Optional[str] = None,
        generate_image: bool = False,
        image_format: str = "png",
        figsize: Tuple[int, int] = (10, 6),
        dpi: int = 100
    ) -> ChartResponse:
        """
        創建長條圖
        
        Args:
            data: 圖表數據點列表
            title: 圖表標題
            x_axis_label: X軸標籤
            y_axis_label: Y軸標籤
            
        Returns:
            ChartResponse: 圖表響應
        """
        try:
            # 驗證數據
            if not data:
                raise ValueError("數據不能為空")
            
            # 轉換數據格式
            chart_data = []
            for point in data:
                chart_data.append({
                    "label": point.label,
                    "value": point.value
                })
            
            # 計算統計信息
            values = [point.value for point in data]
            max_value = max(values)
            min_value = min(values)
            
            response = ChartResponse(
                success=True,
                chart_type="bar",
                data=chart_data,
                title=title or "長條圖",
                confidence=1.0,
                reasoning=f"成功創建包含 {len(data)} 個數據點的長條圖，數值範圍 {min_value} - {max_value}",
                metadata={
                    "max_value": max_value,
                    "min_value": min_value,
                    "data_points_count": len(data),
                    "x_axis_label": x_axis_label,
                    "y_axis_label": y_axis_label
                }
            )
            
            # 如果需要生成圖片
            if generate_image:
                try:
                    image_base64 = self._generate_chart_image(
                        chart_type="bar",
                        data=chart_data,
                        title=response.title or "長條圖",
                        metadata=response.metadata,
                        figsize=figsize,
                        dpi=dpi,
                        image_format=image_format
                    )
                    
                    if image_base64:
                        response.image_base64 = image_base64
                        response.image_format = image_format
                        response.has_image = True
                        response.reasoning += f"，並成功生成 {image_format.upper()} 圖片"
                    else:
                        response.reasoning += "，但圖片生成失敗"
                        
                except Exception as e:
                    response.reasoning += f"，但圖片生成失敗: {str(e)}"
            
            return response
            
        except Exception as e:
            return ChartResponse(
                success=False,
                chart_type="bar",
                data=[],
                title=title,
                confidence=0.0,
                reasoning=f"創建長條圖失敗: {str(e)}"
            )

    def create_line_chart(
        self, 
        data: List[ChartDataPoint], 
        title: Optional[str] = None,
        x_axis_label: Optional[str] = None,
        y_axis_label: Optional[str] = None,
        generate_image: bool = False,
        image_format: str = "png",
        figsize: Tuple[int, int] = (10, 6),
        dpi: int = 100
    ) -> ChartResponse:
        """
        創建折線圖
        
        Args:
            data: 圖表數據點列表
            title: 圖表標題
            x_axis_label: X軸標籤
            y_axis_label: Y軸標籤
            
        Returns:
            ChartResponse: 圖表響應
        """
        try:
            # 驗證數據
            if len(data) < 2:
                raise ValueError("折線圖至少需要2個數據點")
            
            # 轉換數據格式
            chart_data = []
            for point in data:
                chart_data.append({
                    "label": point.label,
                    "value": point.value
                })
            
            # 計算統計信息
            values = [point.value for point in data]
            max_value = max(values)
            min_value = min(values)
            
            response = ChartResponse(
                success=True,
                chart_type="line",
                data=chart_data,
                title=title or "折線圖",
                confidence=1.0,
                reasoning=f"成功創建包含 {len(data)} 個數據點的折線圖，數值範圍 {min_value} - {max_value}",
                metadata={
                    "max_value": max_value,
                    "min_value": min_value,
                    "data_points_count": len(data),
                    "x_axis_label": x_axis_label,
                    "y_axis_label": y_axis_label
                }
            )
            
            # 如果需要生成圖片
            if generate_image:
                try:
                    image_base64 = self._generate_chart_image(
                        chart_type="line",
                        data=chart_data,
                        title=response.title or "折線圖",
                        metadata=response.metadata,
                        figsize=figsize,
                        dpi=dpi,
                        image_format=image_format
                    )
                    
                    if image_base64:
                        response.image_base64 = image_base64
                        response.image_format = image_format
                        response.has_image = True
                        response.reasoning += f"，並成功生成 {image_format.upper()} 圖片"
                    else:
                        response.reasoning += "，但圖片生成失敗"
                        
                except Exception as e:
                    response.reasoning += f"，但圖片生成失敗: {str(e)}"
            
            return response
            
        except Exception as e:
            return ChartResponse(
                success=False,
                chart_type="line",
                data=[],
                title=title,
                confidence=0.0,
                reasoning=f"創建折線圖失敗: {str(e)}"
            )

    def create_chart_from_simple_data(
        self, 
        labels: List[str], 
        values: List[float], 
        chart_type: str,
        title: Optional[str] = None
    ) -> ChartResponse:
        """
        從簡單的標籤和數值數組創建圖表
        
        Args:
            labels: 標籤列表
            values: 數值列表
            chart_type: 圖表類型 (pie, bar, line)
            title: 圖表標題
            
        Returns:
            ChartResponse: 圖表響應
        """
        try:
            # 驗證數據
            if len(labels) != len(values):
                raise ValueError("標籤和數值的數量必須相同")
            
            if not labels or not values:
                raise ValueError("標籤和數值不能為空")
            
            # 轉換為 ChartDataPoint 格式
            data_points = [
                ChartDataPoint(label=label, value=value)
                for label, value in zip(labels, values)
            ]
            
            # 根據圖表類型調用對應方法
            if chart_type == "pie":
                return self.create_pie_chart(data_points, title)
            elif chart_type == "bar":
                return self.create_bar_chart(data_points, title)
            elif chart_type == "line":
                return self.create_line_chart(data_points, title)
            else:
                raise ValueError(f"不支援的圖表類型: {chart_type}")
                
        except Exception as e:
            return ChartResponse(
                success=False,
                chart_type=chart_type,
                data=[],
                title=title,
                confidence=0.0,
                reasoning=f"創建圖表失敗: {str(e)}"
            )

    def create_chart_from_simple_data_with_image(
        self, 
        labels: List[str], 
        values: List[float], 
        chart_type: str,
        title: Optional[str] = None,
        generate_image: bool = False,
        image_format: str = "png",
        figsize: Tuple[int, int] = (10, 6),
        dpi: int = 100
    ) -> ChartResponse:
        """
        從簡單的標籤和數值數組創建圖表，支援圖片生成
        
        Args:
            labels: 標籤列表
            values: 數值列表
            chart_type: 圖表類型 (pie, bar, line)
            title: 圖表標題
            generate_image: 是否生成圖片
            image_format: 圖片格式
            figsize: 圖片大小
            dpi: 圖片解析度
            
        Returns:
            ChartResponse: 圖表響應
        """
        # 先創建基本圖表
        response = self.create_chart_from_simple_data(labels, values, chart_type, title)
        
        # 如果需要生成圖片且基本圖表創建成功
        if generate_image and response.success:
            try:
                image_base64 = self._generate_chart_image(
                    chart_type=chart_type,
                    data=response.data,
                    title=response.title or "圖表",
                    metadata=response.metadata,
                    figsize=figsize,
                    dpi=dpi,
                    image_format=image_format
                )
                
                if image_base64:
                    response.image_base64 = image_base64
                    response.image_format = image_format
                    response.has_image = True
                    response.reasoning += f"，並成功生成 {image_format.upper()} 圖片"
                else:
                    response.reasoning += "，但圖片生成失敗"
                    
            except Exception as e:
                response.reasoning += f"，但圖片生成失敗: {str(e)}"
        
        return response

    def create_histogram(
        self,
        values: List[float],
        bins: int = 10,
        title: Optional[str] = None,
        x_axis_label: str = "數值",
        y_axis_label: str = "頻率",
        generate_image: bool = False,
        image_format: str = "png",
        figsize: Tuple[int, int] = (10, 6),
        dpi: int = 100
    ) -> ChartResponse:
        """創建直方圖"""
        try:
            values_array = np.array(values)
            
            # 計算直方圖
            counts, bin_edges = np.histogram(values_array, bins=bins)
            
            # 建立圖表數據
            chart_data = []
            for i in range(len(counts)):
                bin_center = (bin_edges[i] + bin_edges[i + 1]) / 2
                chart_data.append({
                    "bin_start": float(bin_edges[i]),
                    "bin_end": float(bin_edges[i + 1]),
                    "bin_center": float(bin_center),
                    "count": int(counts[i]),
                    "frequency": float(counts[i] / len(values))
                })
            
            # 計算統計摘要
            mean_val = float(np.mean(values_array))
            std_val = float(np.std(values_array))
            
            response = ChartResponse(
                success=True,
                chart_type="histogram",
                data=chart_data,
                title=title or "直方圖",
                confidence=1.0,
                reasoning=f"成功創建包含 {len(values)} 個數據點的直方圖，分為 {bins} 個區間",
                metadata={
                    "bins": bins,
                    "data_count": len(values),
                    "mean": mean_val,
                    "std": std_val,
                    "x_axis_label": x_axis_label,
                    "y_axis_label": y_axis_label
                }
            )
            
            # 如果需要生成圖片
            if generate_image:
                try:
                    image_base64 = self._generate_chart_image(
                        chart_type="histogram",
                        data=chart_data,
                        title=response.title or "直方圖",
                        metadata=response.metadata,
                        figsize=figsize,
                        dpi=dpi,
                        image_format=image_format
                    )
                    
                    if image_base64:
                        response.image_base64 = image_base64
                        response.image_format = image_format
                        response.has_image = True
                        response.reasoning += f"，並成功生成 {image_format.upper()} 圖片"
                    else:
                        response.reasoning += "，但圖片生成失敗"
                        
                except Exception as e:
                    response.reasoning += f"，但圖片生成失敗: {str(e)}"
            
            return response
            
        except Exception as e:
            return ChartResponse(
                success=False,
                chart_type="histogram",
                data=[],
                title=title,
                confidence=0.0,
                reasoning=f"創建直方圖失敗: {str(e)}"
            )

    def create_boxplot(
        self,
        groups: List[List[float]],
        group_labels: Optional[List[str]] = None,
        title: Optional[str] = None,
        y_axis_label: str = "數值",
        generate_image: bool = False,
        image_format: str = "png",
        figsize: Tuple[int, int] = (10, 6),
        dpi: int = 100
    ) -> ChartResponse:
        """創建盒鬚圖"""
        try:
            if group_labels and len(group_labels) != len(groups):
                raise ValueError("組別標籤數量必須與組別數量相同")
            
            chart_data = []
            for i, group in enumerate(groups):
                group_array = np.array(group)
                
                # 計算五數概括
                q1 = float(np.percentile(group_array, 25))
                q2 = float(np.percentile(group_array, 50))  # 中位數
                q3 = float(np.percentile(group_array, 75))
                
                # 計算四分位距和異常值範圍
                iqr = q3 - q1
                lower_whisker = float(np.max([np.min(group_array), q1 - 1.5 * iqr]))
                upper_whisker = float(np.min([np.max(group_array), q3 + 1.5 * iqr]))
                
                # 找出異常值
                outliers = []
                for val in group_array:
                    if val < lower_whisker or val > upper_whisker:
                        outliers.append(float(val))
                
                group_label = group_labels[i] if group_labels else f"組別 {i+1}"
                
                chart_data.append({
                    "group": group_label,
                    "q1": q1,
                    "median": q2,
                    "q3": q3,
                    "lower_whisker": lower_whisker,
                    "upper_whisker": upper_whisker,
                    "outliers": outliers,
                    "mean": float(np.mean(group_array)),
                    "count": len(group)
                })
            
            total_points = sum(len(group) for group in groups)
            
            response = ChartResponse(
                success=True,
                chart_type="boxplot",
                data=chart_data,
                title=title or "盒鬚圖",
                confidence=1.0,
                reasoning=f"成功創建包含 {len(groups)} 個組別，總計 {total_points} 個數據點的盒鬚圖",
                metadata={
                    "groups_count": len(groups),
                    "total_points": total_points,
                    "y_axis_label": y_axis_label
                }
            )
            
            # 如果需要生成圖片
            if generate_image:
                try:
                    image_base64 = self._generate_chart_image(
                        chart_type="boxplot",
                        data=chart_data,
                        title=response.title or "盒鬚圖",
                        metadata=response.metadata,
                        figsize=figsize,
                        dpi=dpi,
                        image_format=image_format
                    )
                    
                    if image_base64:
                        response.image_base64 = image_base64
                        response.image_format = image_format
                        response.has_image = True
                        response.reasoning += f"，並成功生成 {image_format.upper()} 圖片"
                    else:
                        response.reasoning += "，但圖片生成失敗"
                        
                except Exception as e:
                    response.reasoning += f"，但圖片生成失敗: {str(e)}"
            
            return response
            
        except Exception as e:
            return ChartResponse(
                success=False,
                chart_type="boxplot",
                data=[],
                title=title,
                confidence=0.0,
                reasoning=f"創建盒鬚圖失敗: {str(e)}"
            )

    def create_scatter(
        self,
        x: List[float],
        y: List[float],
        title: Optional[str] = None,
        x_axis_label: str = "X",
        y_axis_label: str = "Y",
        show_regression_line: bool = False,
        generate_image: bool = False,
        image_format: str = "png",
        figsize: Tuple[int, int] = (10, 6),
        dpi: int = 100
    ) -> ChartResponse:
        """創建散點圖"""
        try:
            if len(x) != len(y):
                raise ValueError("X 和 Y 數據的長度必須相同")
            
            x_array = np.array(x)
            y_array = np.array(y)
            
            # 建立散點數據
            chart_data = []
            for i in range(len(x)):
                chart_data.append({
                    "x": float(x[i]),
                    "y": float(y[i])
                })
            
            metadata = {
                "data_points_count": len(x),
                "x_axis_label": x_axis_label,
                "y_axis_label": y_axis_label,
                "x_range": [float(np.min(x_array)), float(np.max(x_array))],
                "y_range": [float(np.min(y_array)), float(np.max(y_array))]
            }
            
            # 如果要顯示迴歸線，計算線性迴歸
            if show_regression_line:
                slope, intercept, r_value, p_value, std_err = stats.linregress(x_array, y_array)
                
                # 計算迴歸線點
                x_min, x_max = np.min(x_array), np.max(x_array)
                regression_points = [
                    {"x": float(x_min), "y": float(slope * x_min + intercept)},
                    {"x": float(x_max), "y": float(slope * x_max + intercept)}
                ]
                
                metadata.update({
                    "regression_line": regression_points,
                    "correlation": float(r_value),
                    "r_squared": float(r_value ** 2),
                    "slope": float(slope),
                    "intercept": float(intercept),
                    "p_value": float(p_value)
                })
            
            reasoning = f"成功創建包含 {len(x)} 個數據點的散點圖"
            if show_regression_line:
                reasoning += f"，相關係數 r = {metadata.get('correlation', 0):.3f}"
            
            response = ChartResponse(
                success=True,
                chart_type="scatter",
                data=chart_data,
                title=title or "散點圖",
                confidence=1.0,
                reasoning=reasoning,
                metadata=metadata
            )
            
            # 如果需要生成圖片
            if generate_image:
                try:
                    image_base64 = self._generate_chart_image(
                        chart_type="scatter",
                        data=chart_data,
                        title=response.title or "散點圖",
                        metadata=response.metadata,
                        figsize=figsize,
                        dpi=dpi,
                        image_format=image_format
                    )
                    
                    if image_base64:
                        response.image_base64 = image_base64
                        response.image_format = image_format
                        response.has_image = True
                        response.reasoning += f"，並成功生成 {image_format.upper()} 圖片"
                    else:
                        response.reasoning += "，但圖片生成失敗"
                        
                except Exception as e:
                    response.reasoning += f"，但圖片生成失敗: {str(e)}"
            
            return response
            
        except Exception as e:
            return ChartResponse(
                success=False,
                chart_type="scatter",
                data=[],
                title=title,
                confidence=0.0,
                reasoning=f"創建散點圖失敗: {str(e)}"
            )

    def _generate_chart_image(
        self,
        chart_type: str,
        data: List[Dict[str, Any]],
        title: str,
        metadata: Optional[Dict[str, Any]] = None,
        figsize: Tuple[int, int] = (10, 6),
        dpi: int = 100,
        image_format: str = "png"
    ) -> Optional[str]:
        """
        生成圖表圖片並回傳 base64 編碼字串
        
        Args:
            chart_type: 圖表類型
            data: 圖表數據
            title: 圖表標題
            metadata: 附加元數據
            figsize: 圖片大小 (寬, 高)
            dpi: 圖片解析度
            image_format: 圖片格式
            
        Returns:
            base64 編碼的圖片字串，失敗時回傳 None
        """
        try:
            fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
            
            if chart_type == "pie":
                self._create_pie_chart_image(ax, data, title)
            elif chart_type == "bar":
                self._create_bar_chart_image(ax, data, title, metadata)
            elif chart_type == "line":
                self._create_line_chart_image(ax, data, title, metadata)
            elif chart_type == "histogram":
                self._create_histogram_image(ax, data, title, metadata)
            elif chart_type == "boxplot":
                self._create_boxplot_image(ax, data, title, metadata)
            elif chart_type == "scatter":
                self._create_scatter_image(ax, data, title, metadata)
            else:
                raise ValueError(f"不支援的圖表類型: {chart_type}")
            
            # 調整布局
            plt.tight_layout()
            
            # 將圖片轉換為 base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format=image_format, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            
            # 編碼為 base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # 清理內存
            plt.close(fig)
            buffer.close()
            
            return image_base64
            
        except Exception as e:
            print(f"圖片生成失敗: {str(e)}")
            if 'fig' in locals():
                plt.close(fig)
            return None

    def _create_pie_chart_image(self, ax, data: List[Dict[str, Any]], title: str):
        """生成圓餅圖圖片"""
        labels = [item['label'] for item in data]
        values = [item['value'] for item in data]
        
        # 創建圓餅圖
        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', 
                                         startangle=90, textprops={'fontsize': 10})
        
        # 設定標題
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # 確保圓餅圖是圓形
        ax.axis('equal')

    def _create_bar_chart_image(self, ax, data: List[Dict[str, Any]], title: str, metadata: Optional[Dict]):
        """生成長條圖圖片"""
        labels = [item['label'] for item in data]
        values = [item['value'] for item in data]
        
        # 創建長條圖
        bars = ax.bar(labels, values, color=sns.color_palette("husl", len(data)))
        
        # 在長條上顯示數值
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                   f'{value:.1f}', ha='center', va='bottom', fontsize=9)
        
        # 設定標題和軸標籤
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        if metadata:
            ax.set_xlabel(metadata.get('x_axis_label', '類別'), fontsize=12)
            ax.set_ylabel(metadata.get('y_axis_label', '數值'), fontsize=12)
        
        # 美化圖表
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')

    def _create_line_chart_image(self, ax, data: List[Dict[str, Any]], title: str, metadata: Optional[Dict]):
        """生成折線圖圖片"""
        labels = [item['label'] for item in data]
        values = [item['value'] for item in data]
        
        # 創建折線圖
        ax.plot(labels, values, marker='o', linewidth=2, markersize=6)
        
        # 在點上顯示數值
        for i, value in enumerate(values):
            ax.text(i, value + max(values)*0.02, f'{value:.1f}', 
                   ha='center', va='bottom', fontsize=9)
        
        # 設定標題和軸標籤
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        if metadata:
            ax.set_xlabel(metadata.get('x_axis_label', '時間'), fontsize=12)
            ax.set_ylabel(metadata.get('y_axis_label', '數值'), fontsize=12)
        
        # 美化圖表
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')

    def _create_histogram_image(self, ax, data: List[Dict[str, Any]], title: str, metadata: Optional[Dict]):
        """生成直方圖圖片"""
        # 從數據中重建原始值（近似）
        values = []
        for item in data:
            bin_center = item['bin_center']
            count = item['count']
            values.extend([bin_center] * count)
        
        # 創建直方圖
        bins = metadata.get('bins', 10) if metadata else 10
        ax.hist(values, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
        
        # 設定標題和軸標籤
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        if metadata:
            ax.set_xlabel(metadata.get('x_axis_label', '數值'), fontsize=12)
            ax.set_ylabel(metadata.get('y_axis_label', '頻率'), fontsize=12)
            
            # 顯示統計資訊
            mean_val = metadata.get('mean', 0)
            std_val = metadata.get('std', 0)
            ax.axvline(mean_val, color='red', linestyle='--', alpha=0.7, 
                      label=f'平均值: {mean_val:.2f}')
            ax.legend()
        
        # 美化圖表
        ax.grid(True, alpha=0.3)

    def _create_boxplot_image(self, ax, data: List[Dict[str, Any]], title: str, metadata: Optional[Dict]):
        """生成盒鬚圖圖片"""
        # 準備盒鬚圖數據
        box_data = []
        labels = []
        
        for item in data:
            # 構建用於 matplotlib 的盒鬚圖數據格式
            box_stats = {
                'med': item['median'],
                'q1': item['q1'],
                'q3': item['q3'],
                'whislo': item['lower_whisker'],
                'whishi': item['upper_whisker'],
                'fliers': item['outliers']
            }
            box_data.append(box_stats)
            labels.append(item['group'])
        
        # 創建盒鬚圖
        bp = ax.bxp(box_data, positions=range(len(box_data)), patch_artist=True)
        
        # 美化盒鬚圖
        colors = sns.color_palette("husl", len(box_data))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # 設定標題和軸標籤
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xticklabels(labels)
        if metadata:
            ax.set_ylabel(metadata.get('y_axis_label', '數值'), fontsize=12)
        
        # 美化圖表
        ax.grid(True, alpha=0.3)

    def _create_scatter_image(self, ax, data: List[Dict[str, Any]], title: str, metadata: Optional[Dict]):
        """生成散點圖圖片"""
        x_values = [item['x'] for item in data]
        y_values = [item['y'] for item in data]
        
        # 創建散點圖
        ax.scatter(x_values, y_values, alpha=0.6, s=50)
        
        # 如果有迴歸線數據，繪製迴歸線
        if metadata and 'regression_line' in metadata:
            reg_data = metadata['regression_line']
            reg_x = [point['x'] for point in reg_data]
            reg_y = [point['y'] for point in reg_data]
            ax.plot(reg_x, reg_y, 'r--', alpha=0.8, linewidth=2, 
                   label=f"R² = {metadata.get('r_squared', 0):.3f}")
            ax.legend()
        
        # 設定標題和軸標籤
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        if metadata:
            ax.set_xlabel(metadata.get('x_axis_label', 'X'), fontsize=12)
            ax.set_ylabel(metadata.get('y_axis_label', 'Y'), fontsize=12)
        
        # 美化圖表
        ax.grid(True, alpha=0.3) 