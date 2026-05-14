import pytest
from app.services.metric_service import MetricCalculator
from decimal import Decimal


def test_calculate_ctr():
    calc = MetricCalculator()
    
    assert calc.calculate_ctr(100, 1000) == 0.1
    assert calc.calculate_ctr(0, 1000) == 0.0
    assert calc.calculate_ctr(100, 0) == 0.0


def test_calculate_cvr():
    calc = MetricCalculator()
    
    assert calc.calculate_cvr(10, 100) == 0.1
    assert calc.calculate_cvr(0, 100) == 0.0
    assert calc.calculate_cvr(10, 0) == 0.0


def test_calculate_acos():
    calc = MetricCalculator()
    
    assert calc.calculate_acos(Decimal("100"), Decimal("400")) == 0.25
    assert calc.calculate_acos(Decimal("0"), Decimal("400")) == 0.0
    assert calc.calculate_acos(Decimal("100"), Decimal("0")) == 0.0


def test_calculate_roas():
    calc = MetricCalculator()
    
    assert calc.calculate_roas(Decimal("400"), Decimal("100")) == 4.0
    assert calc.calculate_roas(Decimal("0"), Decimal("100")) == 0.0
    assert calc.calculate_roas(Decimal("400"), Decimal("0")) == 0.0


def test_calculate_all_metrics():
    calc = MetricCalculator()
    
    metrics = calc.calculate_all_metrics(
        impressions=10000,
        clicks=500,
        spend=Decimal("1000"),
        orders=25,
        sales=Decimal("5000")
    )
    
    assert metrics['ctr'] == 0.05
    assert metrics['cvr'] == 0.05
    assert metrics['acos'] == 0.2
    assert metrics['roas'] == 5.0
