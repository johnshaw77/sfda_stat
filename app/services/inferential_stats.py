from typing import List, Optional, Tuple
import numpy as np
from scipy import stats
import pingouin as pg
from app.models.response_models import (
    TTestResponse, ChiSquareResponse, ANOVAResponse,
    MannWhitneyResponse, WilcoxonResponse, KruskalWallisResponse
)


class InferentialStatsService:
    """推論統計服務類別"""

    @staticmethod
    def _interpret_cohens_d(d: float) -> str:
        """解釋 Cohen's d 效果量"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "微小"
        elif abs_d < 0.5:
            return "小"
        elif abs_d < 0.8:
            return "中等"
        else:
            return "大"

    @staticmethod
    def _interpret_eta_squared(eta_sq: float) -> str:
        """解釋 Eta 平方效果量"""
        if eta_sq < 0.01:
            return "微小"
        elif eta_sq < 0.06:
            return "小"
        elif eta_sq < 0.14:
            return "中等"
        else:
            return "大"

    @staticmethod
    def _interpret_correlation_effect_size(r: float) -> str:
        """解釋相關係數效果量"""
        abs_r = abs(r)
        if abs_r < 0.1:
            return "微小"
        elif abs_r < 0.3:
            return "小"
        elif abs_r < 0.5:
            return "中等"
        else:
            return "大"

    def ttest(
        self,
        sample1: List[float],
        sample2: Optional[List[float]] = None,
        paired: bool = False,
        alpha: float = 0.05,
        alternative: str = "two-sided",
    ) -> TTestResponse:
        """執行 t 檢定"""
        try:
            sample1_array = np.array(sample1)

            if sample2 is None:
                # 單樣本 t 檢定
                statistic, p_value = stats.ttest_1samp(sample1_array, 0)
                degrees_of_freedom = len(sample1) - 1
            else:
                sample2_array = np.array(sample2)
                if paired:
                    # 配對樣本 t 檢定
                    statistic, p_value = stats.ttest_rel(sample1_array, sample2_array)
                    degrees_of_freedom = len(sample1) - 1
                else:
                    # 獨立樣本 t 檢定
                    statistic, p_value = stats.ttest_ind(sample1_array, sample2_array)
                    degrees_of_freedom = len(sample1) + len(sample2) - 2

            # 調整 p 值根據對立假設
            if alternative == "less":
                p_value = p_value / 2 if statistic < 0 else 1 - p_value / 2
            elif alternative == "greater":
                p_value = p_value / 2 if statistic > 0 else 1 - p_value / 2

            # 計算臨界值
            if alternative == "two-sided":
                critical_value = stats.t.ppf(1 - alpha / 2, degrees_of_freedom)
            else:
                critical_value = stats.t.ppf(1 - alpha, degrees_of_freedom)

            # 判斷是否拒絕虛無假設
            reject_null = p_value < alpha

            # 計算信賴區間（僅針對雙側檢定）
            if alternative == "two-sided" and sample2 is None:
                margin_error = critical_value * stats.sem(sample1_array)
                mean = np.mean(sample1_array)
                confidence_interval = [mean - margin_error, mean + margin_error]
            else:
                confidence_interval = None

            # 計算 Cohen's d 效果量
            effect_size = None
            effect_size_interpretation = None
            
            if sample2 is None:
                # 單樣本 Cohen's d: (mean - mu) / std
                effect_size = np.mean(sample1_array) / np.std(sample1_array, ddof=1)
            else:
                if paired:
                    # 配對樣本 Cohen's d: mean_diff / std_diff
                    diff = sample1_array - sample2_array
                    effect_size = np.mean(diff) / np.std(diff, ddof=1)
                else:
                    # 獨立樣本 Cohen's d: (mean1 - mean2) / pooled_std
                    mean1, mean2 = np.mean(sample1_array), np.mean(sample2_array)
                    var1, var2 = np.var(sample1_array, ddof=1), np.var(sample2_array, ddof=1)
                    n1, n2 = len(sample1), len(sample2)
                    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
                    effect_size = (mean1 - mean2) / pooled_std

            if effect_size is not None:
                effect_size_interpretation = self._interpret_cohens_d(effect_size)

            return TTestResponse(
                statistic=float(statistic),
                p_value=float(p_value),
                degrees_of_freedom=int(degrees_of_freedom),
                critical_value=float(critical_value),
                reject_null=reject_null,
                confidence_interval=confidence_interval,
                effect_size=effect_size,
                effect_size_interpretation=effect_size_interpretation,
            )

        except Exception as e:
            raise ValueError(f"t 檢定計算失敗: {str(e)}")

    def chi_square_test(
        self, observed: List[List[int]], expected: Optional[List[List[float]]] = None
    ) -> ChiSquareResponse:
        """執行卡方檢定"""
        try:
            observed_array = np.array(observed)

            if expected is None:
                # 獨立性檢定
                statistic, p_value, dof, expected_freq = stats.chi2_contingency(
                    observed_array
                )
                expected_frequencies = expected_freq.tolist()
            else:
                # 適合度檢定
                expected_array = np.array(expected)
                statistic, p_value = stats.chisquare(
                    observed_array.flatten(), expected_array.flatten()
                )
                dof = observed_array.size - 1
                expected_frequencies = expected

            # 判斷是否拒絕虛無假設（使用 α = 0.05）
            alpha = 0.05
            critical_value = stats.chi2.ppf(1 - alpha, dof)
            reject_null = p_value < alpha

            return ChiSquareResponse(
                statistic=float(statistic),
                p_value=float(p_value),
                degrees_of_freedom=int(dof),
                expected_frequencies=expected_frequencies,
                reject_null=reject_null,
            )

        except Exception as e:
            raise ValueError(f"卡方檢定計算失敗: {str(e)}")

    def anova(self, groups: List[List[float]]) -> ANOVAResponse:
        """執行單因子 ANOVA"""
        try:
            # 轉換為 numpy 陣列
            group_arrays = [np.array(group) for group in groups]

            # 執行 ANOVA
            f_statistic, p_value = stats.f_oneway(*group_arrays)

            # 計算自由度
            k = len(groups)  # 組數
            n = sum(len(group) for group in groups)  # 總樣本數
            df_between = k - 1
            df_within = n - k

            # 計算平方和
            grand_mean = np.mean(np.concatenate(group_arrays))

            # 組間平方和 (SSB)
            ssb = sum(
                len(group) * (np.mean(group) - grand_mean) ** 2
                for group in group_arrays
            )

            # 組內平方和 (SSW)
            ssw = sum(
                np.sum((np.array(group) - np.mean(group)) ** 2)
                for group in group_arrays
            )

            # 均方
            msb = ssb / df_between
            msw = ssw / df_within

            # 判斷是否拒絕虛無假設（使用 α = 0.05）
            alpha = 0.05
            reject_null = p_value < alpha

            # 計算 Eta 平方效果量
            total_ss = ssb + ssw
            eta_squared = ssb / total_ss if total_ss > 0 else 0
            effect_size_interpretation = self._interpret_eta_squared(eta_squared)

            return ANOVAResponse(
                f_statistic=float(f_statistic),
                p_value=float(p_value),
                degrees_of_freedom_between=int(df_between),
                degrees_of_freedom_within=int(df_within),
                sum_of_squares_between=float(ssb),
                sum_of_squares_within=float(ssw),
                mean_square_between=float(msb),
                mean_square_within=float(msw),
                reject_null=reject_null,
                effect_size=float(eta_squared),
                effect_size_interpretation=effect_size_interpretation,
            )

        except Exception as e:
            raise ValueError(f"ANOVA 計算失敗: {str(e)}")

    def mann_whitney_test(
        self,
        sample1: List[float],
        sample2: List[float],
        alpha: float = 0.05,
        alternative: str = "two-sided",
    ) -> MannWhitneyResponse:
        """執行 Mann-Whitney U 檢定"""
        try:
            sample1_array = np.array(sample1)
            sample2_array = np.array(sample2)

            # 執行 Mann-Whitney U 檢定
            statistic, p_value = stats.mannwhitneyu(
                sample1_array, sample2_array, alternative=alternative
            )

            # 計算效果量 (r = Z / sqrt(N))
            n1, n2 = len(sample1), len(sample2)
            total_n = n1 + n2
            
            # 計算 Z 分數（對於大樣本）
            if total_n > 20:
                mean_u = n1 * n2 / 2
                std_u = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
                z_score = (statistic - mean_u) / std_u
                effect_size = abs(z_score) / np.sqrt(total_n)
            else:
                z_score = None
                effect_size = None

            # 計算等級和
            combined = np.concatenate([sample1_array, sample2_array])
            ranks = stats.rankdata(combined)
            rank_sum1 = np.sum(ranks[:len(sample1)])
            rank_sum2 = np.sum(ranks[len(sample1):])

            # 判斷是否拒絕虛無假設
            reject_null = p_value < alpha

            # 解釋結果
            if reject_null:
                interpretation = f"在 α = {alpha} 的顯著水準下，拒絕虛無假設，兩組分佈有顯著差異"
            else:
                interpretation = f"在 α = {alpha} 的顯著水準下，無法拒絕虛無假設，兩組分佈無顯著差異"
            
            if effect_size is not None:
                if effect_size < 0.1:
                    effect_desc = "微小"
                elif effect_size < 0.3:
                    effect_desc = "小"
                elif effect_size < 0.5:
                    effect_desc = "中等"
                else:
                    effect_desc = "大"
                interpretation += f"，效果量為 {effect_desc} (r = {effect_size:.3f})"

            return MannWhitneyResponse(
                statistic=float(statistic),
                p_value=float(p_value),
                reject_null=reject_null,
                alpha=alpha,
                effect_size=effect_size,
                interpretation=interpretation,
                u_statistic=float(statistic),
                z_score=z_score,
                rank_sum1=float(rank_sum1),
                rank_sum2=float(rank_sum2),
            )

        except Exception as e:
            raise ValueError(f"Mann-Whitney U 檢定計算失敗: {str(e)}")

    def wilcoxon_test(
        self,
        sample1: List[float],
        sample2: List[float],
        alpha: float = 0.05,
        alternative: str = "two-sided",
    ) -> WilcoxonResponse:
        """執行 Wilcoxon 符號等級檢定"""
        try:
            sample1_array = np.array(sample1)
            sample2_array = np.array(sample2)

            # 檢查樣本大小是否相等
            if len(sample1) != len(sample2):
                raise ValueError("配對樣本檢定需要兩組樣本大小相等")

            # 執行 Wilcoxon 符號等級檢定
            statistic, p_value = stats.wilcoxon(
                sample1_array, sample2_array, alternative=alternative
            )

            # 計算效果量 (r = Z / sqrt(N))
            n_pairs = len(sample1)
            
            # 計算 Z 分數（對於大樣本 n > 25）
            if n_pairs > 25:
                mean_w = n_pairs * (n_pairs + 1) / 4
                std_w = np.sqrt(n_pairs * (n_pairs + 1) * (2 * n_pairs + 1) / 24)
                z_score = (statistic - mean_w) / std_w
                effect_size = abs(z_score) / np.sqrt(n_pairs)
            else:
                z_score = None
                effect_size = None

            # 判斷是否拒絕虛無假設
            reject_null = p_value < alpha

            # 解釋結果
            if reject_null:
                interpretation = f"在 α = {alpha} 的顯著水準下，拒絕虛無假設，配對樣本有顯著差異"
            else:
                interpretation = f"在 α = {alpha} 的顯著水準下，無法拒絕虛無假設，配對樣本無顯著差異"
            
            if effect_size is not None:
                if effect_size < 0.1:
                    effect_desc = "微小"
                elif effect_size < 0.3:
                    effect_desc = "小"
                elif effect_size < 0.5:
                    effect_desc = "中等"
                else:
                    effect_desc = "大"
                interpretation += f"，效果量為 {effect_desc} (r = {effect_size:.3f})"

            return WilcoxonResponse(
                statistic=float(statistic),
                p_value=float(p_value),
                reject_null=reject_null,
                alpha=alpha,
                effect_size=effect_size,
                interpretation=interpretation,
                w_statistic=float(statistic),
                z_score=z_score,
                n_pairs=n_pairs,
            )

        except Exception as e:
            raise ValueError(f"Wilcoxon 符號等級檢定計算失敗: {str(e)}")

    def kruskal_wallis_test(
        self, groups: List[List[float]], alpha: float = 0.05
    ) -> KruskalWallisResponse:
        """執行 Kruskal-Wallis 檢定"""
        try:
            # 轉換為 numpy 陣列
            group_arrays = [np.array(group) for group in groups]

            # 執行 Kruskal-Wallis 檢定
            statistic, p_value = stats.kruskal(*group_arrays)

            # 計算自由度
            k = len(groups)  # 組數
            df = k - 1

            # 計算效果量 (eta squared)
            total_n = sum(len(group) for group in groups)
            effect_size = (statistic - k + 1) / (total_n - k) if total_n > k else None

            # 判斷是否拒絕虛無假設
            reject_null = p_value < alpha

            # 解釋結果
            if reject_null:
                interpretation = f"在 α = {alpha} 的顯著水準下，拒絕虛無假設，各組分佈有顯著差異"
            else:
                interpretation = f"在 α = {alpha} 的顯著水準下，無法拒絕虛無假設，各組分佈無顯著差異"
            
            if effect_size is not None:
                if effect_size < 0.01:
                    effect_desc = "微小"
                elif effect_size < 0.06:
                    effect_desc = "小"
                elif effect_size < 0.14:
                    effect_desc = "中等"
                else:
                    effect_desc = "大"
                interpretation += f"，效果量為 {effect_desc} (η² = {effect_size:.3f})"

            return KruskalWallisResponse(
                statistic=float(statistic),
                p_value=float(p_value),
                reject_null=reject_null,
                alpha=alpha,
                effect_size=effect_size,
                interpretation=interpretation,
                h_statistic=float(statistic),
                degrees_of_freedom=df,
                n_groups=k,
            )

        except Exception as e:
            raise ValueError(f"Kruskal-Wallis 檢定計算失敗: {str(e)}")
