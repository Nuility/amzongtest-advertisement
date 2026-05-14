import pytest
from decimal import Decimal
from app.services.bidding_service import BiddingEngine, ACoSTargetStrategy, CVRBasedStrategy


class TestACoSTargetStrategy:
    
    def test_calculate_new_bid_high_acos(self):
        strategy = ACoSTargetStrategy(adjustment_factor=0.1)
        current_bid = Decimal("1.00")
        metrics = {'acos': 0.35, 'clicks': 50}
        target_metrics = {'target_acos': 0.25}
        
        new_bid = strategy.calculate_new_bid(current_bid, metrics, target_metrics)
        assert new_bid == Decimal("0.90")
    
    def test_calculate_new_bid_low_acos(self):
        strategy = ACoSTargetStrategy(adjustment_factor=0.1)
        current_bid = Decimal("1.00")
        metrics = {'acos': 0.18, 'clicks': 50}
        target_metrics = {'target_acos': 0.25}
        
        new_bid = strategy.calculate_new_bid(current_bid, metrics, target_metrics)
        assert new_bid == Decimal("1.10")
    
    def test_calculate_new_bid_normal_acos(self):
        strategy = ACoSTargetStrategy(adjustment_factor=0.1)
        current_bid = Decimal("1.00")
        metrics = {'acos': 0.26, 'clicks': 50}
        target_metrics = {'target_acos': 0.25}
        
        new_bid = strategy.calculate_new_bid(current_bid, metrics, target_metrics)
        assert new_bid == Decimal("1.00")
    
    def test_should_skip_insufficient_clicks(self):
        strategy = ACoSTargetStrategy()
        metrics = {'clicks': 5}
        
        assert strategy.should_skip(metrics) is True
    
    def test_should_skip_sufficient_clicks(self):
        strategy = ACoSTargetStrategy()
        metrics = {'clicks': 15}
        
        assert strategy.should_skip(metrics) is False


class TestCVRBasedStrategy:
    
    def test_calculate_new_bid_high_cvr(self):
        strategy = CVRBasedStrategy(adjustment_factor=0.15)
        current_bid = Decimal("1.00")
        metrics = {'cvr': 0.10, 'clicks': 50}
        target_metrics = {'avg_cvr': 0.05}
        
        new_bid = strategy.calculate_new_bid(current_bid, metrics, target_metrics)
        assert new_bid == Decimal("1.15")
    
    def test_calculate_new_bid_low_cvr(self):
        strategy = CVRBasedStrategy(adjustment_factor=0.15)
        current_bid = Decimal("1.00")
        metrics = {'cvr': 0.02, 'clicks': 50}
        target_metrics = {'avg_cvr': 0.05}
        
        new_bid = strategy.calculate_new_bid(current_bid, metrics, target_metrics)
        assert new_bid == Decimal("0.78")
    
    def test_should_skip_insufficient_clicks(self):
        strategy = CVRBasedStrategy()
        metrics = {'clicks': 10}
        
        assert strategy.should_skip(metrics) is True
    
    def test_should_skip_sufficient_clicks(self):
        strategy = CVRBasedStrategy()
        metrics = {'clicks': 25}
        
        assert strategy.should_skip(metrics) is False


class TestBiddingEngine:
    
    def test_execute_bidding_acos_strategy(self):
        engine = BiddingEngine()
        current_bid = Decimal("1.00")
        metrics = {'acos': 0.35, 'clicks': 50}
        target_metrics = {'target_acos': 0.25}
        
        new_bid = engine.execute_bidding('acos_target', current_bid, metrics, target_metrics)
        assert new_bid == Decimal("0.90")
    
    def test_execute_bidding_cvr_strategy(self):
        engine = BiddingEngine()
        current_bid = Decimal("1.00")
        metrics = {'cvr': 0.10, 'clicks': 50}
        target_metrics = {'avg_cvr': 0.05}
        
        new_bid = engine.execute_bidding('cvr_based', current_bid, metrics, target_metrics)
        assert new_bid == Decimal("1.15")
    
    def test_execute_bidding_insufficient_data(self):
        engine = BiddingEngine()
        current_bid = Decimal("1.00")
        metrics = {'acos': 0.35, 'clicks': 5}
        target_metrics = {'target_acos': 0.25}
        
        new_bid = engine.execute_bidding('acos_target', current_bid, metrics, target_metrics)
        assert new_bid == current_bid
    
    def test_execute_bidding_invalid_strategy(self):
        engine = BiddingEngine()
        current_bid = Decimal("1.00")
        metrics = {'acos': 0.35, 'clicks': 50}
        target_metrics = {'target_acos': 0.25}
        
        with pytest.raises(ValueError, match="Strategy invalid_strategy not found"):
            engine.execute_bidding('invalid_strategy', current_bid, metrics, target_metrics)
    
    def test_execute_bidding_respects_max_adjustment(self):
        engine = BiddingEngine()
        current_bid = Decimal("1.00")
        metrics = {'acos': 0.50, 'clicks': 50}
        target_metrics = {'target_acos': 0.25}
        
        new_bid = engine.execute_bidding('acos_target', current_bid, metrics, target_metrics)
        max_bid = current_bid * Decimal('1.3')
        assert new_bid <= max_bid
