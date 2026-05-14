import pytest
from decimal import Decimal
from app.services.metric_service import MetricCalculator


class TestMetricCalculator:
    
    def test_calculate_ctr_normal_case(self):
        calculator = MetricCalculator()
        ctr = calculator.calculate_ctr(clicks=100, impressions=1000)
        assert ctr == 0.1
    
    def test_calculate_ctr_zero_impressions(self):
        calculator = MetricCalculator()
        ctr = calculator.calculate_ctr(clicks=100, impressions=0)
        assert ctr == 0.0
    
    def test_calculate_ctr_zero_clicks(self):
        calculator = MetricCalculator()
        ctr = calculator.calculate_ctr(clicks=0, impressions=1000)
        assert ctr == 0.0
    
    def test_calculate_cpc_normal_case(self):
        calculator = MetricCalculator()
        cpc = calculator.calculate_cpc(spend=Decimal("100.00"), clicks=200)
        assert cpc == 0.5
    
    def test_calculate_cpc_zero_clicks(self):
        calculator = MetricCalculator()
        cpc = calculator.calculate_cpc(spend=Decimal("100.00"), clicks=0)
        assert cpc == 0.0
    
    def test_calculate_cvr_normal_case(self):
        calculator = MetricCalculator()
        cvr = calculator.calculate_cvr(orders=50, clicks=1000)
        assert cvr == 0.05
    
    def test_calculate_cvr_zero_clicks(self):
        calculator = MetricCalculator()
        cvr = calculator.calculate_cvr(orders=50, clicks=0)
        assert cvr == 0.0
    
    def test_calculate_acos_normal_case(self):
        calculator = MetricCalculator()
        acos = calculator.calculate_acos(spend=Decimal("250.00"), sales=Decimal("1000.00"))
        assert acos == 0.25
    
    def test_calculate_acos_zero_sales(self):
        calculator = MetricCalculator()
        acos = calculator.calculate_acos(spend=Decimal("250.00"), sales=Decimal("0"))
        assert acos == 0.0
    
    def test_calculate_roas_normal_case(self):
        calculator = MetricCalculator()
        roas = calculator.calculate_roas(sales=Decimal("1000.00"), spend=Decimal("250.00"))
        assert roas == 4.0
    
    def test_calculate_roas_zero_spend(self):
        calculator = MetricCalculator()
        roas = calculator.calculate_roas(sales=Decimal("1000.00"), spend=Decimal("0"))
        assert roas == 0.0
    
    def test_calculate_all_metrics_normal_case(self):
        calculator = MetricCalculator()
        metrics = calculator.calculate_all_metrics(
            impressions=10000,
            clicks=500,
            spend=Decimal("375.00"),
            orders=25,
            sales=Decimal("1250.00")
        )
        
        assert metrics['ctr'] == 0.05
        assert metrics['cpc'] == 0.75
        assert metrics['cvr'] == 0.05
        assert metrics['acos'] == 0.3
        assert metrics['roas'] == pytest.approx(3.33, rel=0.01)
    
    def test_calculate_all_metrics_zero_values(self):
        calculator = MetricCalculator()
        metrics = calculator.calculate_all_metrics(
            impressions=0,
            clicks=0,
            spend=Decimal("0"),
            orders=0,
            sales=Decimal("0")
        )
        
        assert metrics['ctr'] == 0.0
        assert metrics['cpc'] == 0.0
        assert metrics['cvr'] == 0.0
        assert metrics['acos'] == 0.0
        assert metrics['roas'] == 0.0
    
    def test_calculate_all_metrics_partial_zero_values(self):
        calculator = MetricCalculator()
        metrics = calculator.calculate_all_metrics(
            impressions=1000,
            clicks=0,
            spend=Decimal("0"),
            orders=0,
            sales=Decimal("0")
        )
        
        assert metrics['ctr'] == 0.0
        assert metrics['cpc'] == 0.0
        assert metrics['cvr'] == 0.0
        assert metrics['acos'] == 0.0
        assert metrics['roas'] == 0.0
