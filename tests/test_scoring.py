"""
Unit tests for the scoring logic.
Run with: pytest tests/test_scoring.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.factors import score_standard, score_inflation, compute_all_sub_scores
from core.scoring import compute_national_score, get_score_band, compute_city_scores


# ---------------------------------------------------------------------------
# score_standard
# ---------------------------------------------------------------------------

class TestScoreStandard:
    def test_at_bullish_extreme(self):
        # interest_rate at bullish (2.0%) should return 100
        assert score_standard(2.0, "interest_rate") == pytest.approx(100.0)

    def test_at_bearish_extreme(self):
        # interest_rate at bearish (7.0%) should return 0
        assert score_standard(7.0, "interest_rate") == pytest.approx(0.0)

    def test_clamp_below_zero(self):
        # interest_rate above bearish should clamp to 0
        assert score_standard(9.0, "interest_rate") == pytest.approx(0.0)

    def test_clamp_above_100(self):
        # interest_rate well below bullish should clamp to 100
        assert score_standard(0.0, "interest_rate") == pytest.approx(100.0)

    def test_midpoint(self):
        # interest_rate midpoint is now (2.0 + 6.0) / 2 = 4.0% after threshold update
        assert score_standard(4.0, "interest_rate") == pytest.approx(50.0)

    def test_higher_is_better_factor(self):
        # wages_growth at bullish (4.5%) should be 100
        assert score_standard(4.5, "wages_growth") == pytest.approx(100.0)

    def test_higher_is_better_at_bearish(self):
        # wages_growth at bearish (1.5%) should be 0
        assert score_standard(1.5, "wages_growth") == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# score_inflation
# ---------------------------------------------------------------------------

class TestScoreInflation:
    def test_ideal_midpoint(self):
        # 2.5% = ideal midpoint = 100
        assert score_inflation(2.5) == pytest.approx(100.0)

    def test_within_band(self):
        # 2.0% and 3.0% are close to midpoint, should be high
        assert score_inflation(2.0) > 80
        assert score_inflation(3.0) > 80

    def test_high_inflation(self):
        # 6.0% is 3.5 from midpoint = max deviation = 0
        assert score_inflation(6.0) == pytest.approx(0.0)

    def test_deflation(self):
        # -1.0% is 3.5 from midpoint = 0
        assert score_inflation(-1.0) == pytest.approx(0.0)

    def test_clamped_below(self):
        # Values further than max_deviation should clamp to 0
        assert score_inflation(10.0) == pytest.approx(0.0)

    def test_score_drops_symmetrically(self):
        # Equal distance above and below midpoint = equal score
        assert score_inflation(2.5 + 1.0) == pytest.approx(score_inflation(2.5 - 1.0))


# ---------------------------------------------------------------------------
# compute_all_sub_scores
# ---------------------------------------------------------------------------

class TestComputeAllSubScores:
    def test_returns_all_factors(self):
        sample = {
            "interest_rate": 4.10,
            "inflation": 3.2,
            "unemployment": 4.1,
            "wages_growth": 3.4,
            "population_growth": 395000,
            "housing_supply": 163000,
            "rental_vacancy": 1.0,
            "consumer_sentiment": 84,
            "global_macro_risk": 3,
        }
        scores = compute_all_sub_scores(sample)
        assert set(scores.keys()) == set(sample.keys())

    def test_all_scores_in_range(self):
        sample = {
            "interest_rate": 4.10,
            "inflation": 3.2,
            "unemployment": 4.1,
            "wages_growth": 3.4,
            "population_growth": 395000,
            "housing_supply": 163000,
            "rental_vacancy": 1.0,
            "consumer_sentiment": 84,
            "global_macro_risk": 3,
        }
        scores = compute_all_sub_scores(sample)
        for key, val in scores.items():
            assert 0.0 <= val <= 100.0, f"{key} out of range: {val}"


# ---------------------------------------------------------------------------
# compute_national_score
# ---------------------------------------------------------------------------

class TestComputeNationalScore:
    def test_all_100_gives_100(self):
        perfect = {k: 100.0 for k in [
            "interest_rate", "inflation", "unemployment", "wages_growth",
            "population_growth", "consumer_sentiment", "housing_supply",
            "rental_vacancy", "global_macro_risk"
        ]}
        assert compute_national_score(perfect) == 100

    def test_all_zero_gives_zero(self):
        worst = {k: 0.0 for k in [
            "interest_rate", "inflation", "unemployment", "wages_growth",
            "population_growth", "consumer_sentiment", "housing_supply",
            "rental_vacancy", "global_macro_risk"
        ]}
        assert compute_national_score(worst) == 0

    def test_realistic_score_in_range(self):
        sample = {
            "interest_rate": 4.10,
            "inflation": 3.2,
            "unemployment": 4.1,
            "wages_growth": 3.4,
            "population_growth": 395000,
            "housing_supply": 163000,
            "rental_vacancy": 1.0,
            "consumer_sentiment": 84,
            "global_macro_risk": 3,
        }
        from core.factors import compute_all_sub_scores
        scores = compute_all_sub_scores(sample)
        national = compute_national_score(scores)
        assert 0 <= national <= 100


# ---------------------------------------------------------------------------
# get_score_band
# ---------------------------------------------------------------------------

class TestGetScoreBand:
    def test_100_is_strong_conditions(self):
        label, _ = get_score_band(100)
        assert label == "Strong Conditions"

    def test_0_is_poor_conditions(self):
        label, _ = get_score_band(0)
        assert label == "Poor Conditions"

    def test_60_is_cautiously_favourable(self):
        label, _ = get_score_band(60)
        assert label == "Cautiously Favourable"

    def test_50_is_neutral(self):
        label, _ = get_score_band(50)
        assert "Neutral" in label

    def test_30_is_caution(self):
        label, _ = get_score_band(30)
        assert "Caution" in label


# ---------------------------------------------------------------------------
# compute_city_scores
# ---------------------------------------------------------------------------

class TestComputeCityScores:
    def test_all_cities_present(self):
        city_scores = compute_city_scores(60)
        expected = {"Perth", "Brisbane", "Adelaide", "Sydney", "Canberra", "Hobart", "Melbourne", "Darwin"}
        assert set(city_scores.keys()) == expected

    def test_scores_clamped_0_100(self):
        for national in [0, 50, 100]:
            city_scores = compute_city_scores(national)
            for city, data in city_scores.items():
                assert 0 <= data["score"] <= 100, f"{city} score out of range at national={national}"

    def test_perth_higher_than_darwin(self):
        city_scores = compute_city_scores(60)
        assert city_scores["Perth"]["score"] > city_scores["Darwin"]["score"]

    def test_offset_direction_arrows(self):
        city_scores = compute_city_scores(60)
        assert city_scores["Perth"]["offset_direction"] == "↑"
        assert city_scores["Melbourne"]["offset_direction"] == "↓"
        assert city_scores["Sydney"]["offset_direction"] == "→"
