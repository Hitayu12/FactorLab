import pandas as pd

from app.services.factors.transforms import cross_sectional_zscore


def test_cross_sectional_zscore_population_std() -> None:
    idx = pd.to_datetime(["2020-01-31", "2020-02-29"])
    x = pd.DataFrame({"A": [0, 0], "B": [1, 1], "C": [2, 2]}, index=idx)
    z = cross_sectional_zscore(x)

    means = z.mean(axis=1)
    stds = z.std(axis=1, ddof=0)

    assert means.round(10).tolist() == [0.0, 0.0]
    assert stds.round(10).tolist() == [1.0, 1.0]
