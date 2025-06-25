from typing import List, Dict, Optional, Any
from pydantic import BaseModel


class BasicStatsResponse(BaseModel):
    """基本統計量回應模型"""

    mean: float
    median: float
    mode: Optional[List[float]]
    std: float
    variance: float
    min: float
    max: float
    range: float
    count: int


class DistributionStatsResponse(BaseModel):
    """分佈統計回應模型"""

    skewness: float
    kurtosis: float
    is_normal: bool
    normality_p_value: float


class PercentilesResponse(BaseModel):
    """百分位數回應模型"""

    percentiles: Dict[str, float]
    quartiles: Dict[str, float]


class TTestResponse(BaseModel):
    """t檢定回應模型"""

    statistic: float
    p_value: float
    degrees_of_freedom: float
    critical_value: float
    reject_null: bool
    confidence_interval: Optional[List[float]]
    effect_size: Optional[float] = None
    effect_size_interpretation: Optional[str] = None


class ChiSquareResponse(BaseModel):
    """卡方檢定回應模型"""

    statistic: float
    p_value: float
    degrees_of_freedom: int
    expected_frequencies: List[List[float]]
    reject_null: bool
    effect_size: Optional[float] = None
    effect_size_interpretation: Optional[str] = None


class ANOVAResponse(BaseModel):
    """ANOVA回應模型"""

    f_statistic: float
    p_value: float
    degrees_of_freedom_between: int
    degrees_of_freedom_within: int
    sum_of_squares_between: float
    sum_of_squares_within: float
    mean_square_between: float
    mean_square_within: float
    reject_null: bool
    effect_size: Optional[float] = None
    effect_size_interpretation: Optional[str] = None


class RegressionResponse(BaseModel):
    """迴歸分析回應模型"""

    coefficients: List[float]
    intercept: float
    r_squared: float
    adjusted_r_squared: float
    f_statistic: float
    p_value: float
    residuals: List[float]
    fitted_values: List[float]


class CorrelationResponse(BaseModel):
    """相關性分析回應模型"""

    correlation_coefficient: float
    p_value: float
    confidence_interval: List[float]
    interpretation: str
    effect_size: Optional[float] = None
    effect_size_interpretation: Optional[str] = None


class CorrelationMatrixResponse(BaseModel):
    """相關矩陣回應模型"""

    correlation_matrix: List[List[float]]
    p_values_matrix: List[List[float]]
    columns: List[str]


class DistributionAnalysisResponse(BaseModel):
    """分佈分析回應模型"""

    parameters: Dict[str, float]
    goodness_of_fit: float
    p_value: float
    is_good_fit: bool


class NonparametricTestResponse(BaseModel):
    """非參數檢定基礎回應模型"""

    statistic: float
    p_value: float
    reject_null: bool
    alpha: float
    effect_size: Optional[float] = None
    interpretation: str


class MannWhitneyResponse(NonparametricTestResponse):
    """Mann-Whitney U 檢定回應模型"""

    u_statistic: float
    z_score: Optional[float] = None
    rank_sum1: float
    rank_sum2: float


class WilcoxonResponse(NonparametricTestResponse):
    """Wilcoxon 符號等級檢定回應模型"""

    w_statistic: float
    z_score: Optional[float] = None
    n_pairs: int


class KruskalWallisResponse(NonparametricTestResponse):
    """Kruskal-Wallis 檢定回應模型"""

    h_statistic: float
    degrees_of_freedom: int
    n_groups: int


class ErrorResponse(BaseModel):
    """錯誤回應模型"""

    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
