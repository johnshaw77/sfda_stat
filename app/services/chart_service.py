from typing import List, Dict, Any, Optional
import numpy as np
from scipy import stats
from app.models.chart_models import ChartDataPoint, ChartResponse


class ChartService:
    """圖表服務類"""

    def create_pie_chart(
        self, 
        data: List[ChartDataPoint], 
        title: Optional[str] = None
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
            
            return ChartResponse(
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
        y_axis_label: Optional[str] = None
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
            
            return ChartResponse(
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
        y_axis_label: Optional[str] = None
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
            
            return ChartResponse(
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

    def create_histogram(
        self,
        values: List[float],
        bins: int = 10,
        title: Optional[str] = None,
        x_axis_label: str = "數值",
        y_axis_label: str = "頻率"
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
            
            return ChartResponse(
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
        y_axis_label: str = "數值"
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
            
            return ChartResponse(
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
        show_regression_line: bool = False
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
            
            return ChartResponse(
                success=True,
                chart_type="scatter",
                data=chart_data,
                title=title or "散點圖",
                confidence=1.0,
                reasoning=reasoning,
                metadata=metadata
            )
            
        except Exception as e:
            return ChartResponse(
                success=False,
                chart_type="scatter",
                data=[],
                title=title,
                confidence=0.0,
                reasoning=f"創建散點圖失敗: {str(e)}"
            ) 