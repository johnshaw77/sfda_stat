from fastapi import APIRouter, HTTPException
from app.models.request_models import (
    TTestRequest, ChiSquareRequest, ANOVARequest,
    MannWhitneyRequest, WilcoxonRequest, KruskalWallisRequest
)
from app.models.response_models import (
    TTestResponse, ChiSquareResponse, ANOVAResponse,
    MannWhitneyResponse, WilcoxonResponse, KruskalWallisResponse
)
from app.services.inferential_stats import InferentialStatsService

router = APIRouter()
stats_service = InferentialStatsService()


@router.post("/ttest", response_model=TTestResponse)
async def perform_ttest(request: TTestRequest):
    """
    執行 t 檢定

    支援單樣本、雙樣本獨立、配對 t 檢定
    """
    try:
        return stats_service.ttest(
            sample1=request.sample1,
            sample2=request.sample2,
            paired=request.paired,
            alpha=request.alpha,
            alternative=request.alternative,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/chisquare", response_model=ChiSquareResponse)
async def perform_chisquare_test(request: ChiSquareRequest):
    """
    執行卡方檢定

    適用於獨立性檢定和適合度檢定
    """
    try:
        return stats_service.chi_square_test(
            observed=request.observed, expected=request.expected
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/anova", response_model=ANOVAResponse)
async def perform_anova(request: ANOVARequest):
    """
    執行單因子變異數分析 (One-way ANOVA)

    檢定多個組別間是否有顯著差異
    """
    try:
        return stats_service.anova(request.groups)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/mann_whitney", response_model=MannWhitneyResponse)
async def perform_mann_whitney_test(request: MannWhitneyRequest):
    """
    執行 Mann-Whitney U 檢定（無母數雙樣本檢定）

    適用於：
    - 兩個獨立樣本的比較
    - 資料不符合常態分佈假設
    - 順序資料或連續資料
    """
    try:
        return stats_service.mann_whitney_test(
            sample1=request.sample1,
            sample2=request.sample2,
            alpha=request.alpha,
            alternative=request.alternative,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/wilcoxon", response_model=WilcoxonResponse)
async def perform_wilcoxon_test(request: WilcoxonRequest):
    """
    執行 Wilcoxon 符號等級檢定（無母數配對樣本檢定）

    適用於：
    - 配對樣本的比較（前後測、配對實驗）
    - 資料不符合常態分佈假設
    - 樣本數較小時的替代方案
    """
    try:
        return stats_service.wilcoxon_test(
            sample1=request.sample1,
            sample2=request.sample2,
            alpha=request.alpha,
            alternative=request.alternative,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/kruskal_wallis", response_model=KruskalWallisResponse)
async def perform_kruskal_wallis_test(request: KruskalWallisRequest):
    """
    執行 Kruskal-Wallis 檢定（無母數多組比較）

    適用於：
    - 三個或以上獨立組別的比較
    - 資料不符合常態分佈假設
    - ANOVA 的非參數替代方案
    """
    try:
        return stats_service.kruskal_wallis_test(
            groups=request.groups, alpha=request.alpha
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
