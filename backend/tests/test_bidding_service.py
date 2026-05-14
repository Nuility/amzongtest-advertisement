import pytest
from app.services.bidding_service import (
    BiddingEngine,
    ACoSTargetStrategy,
    CVRBasedStrategy
)
from decimal import Decimal


def test_acos_target_strategy_high_acos():
    strategy = ACoSTargetStrategy()
    
    new_bid = strategy.calculate_new_bid(
        current_bid=Decimal("1.0"),
        metrics={'acos': 0.35},
        target_metrics={'target_acos': 0.25}
    )
    
    assert new_bid < Decimal("1.0")


def test_acos_target_strategy_low_acos():
    strategy = ACoSTargetStrategy()
    
    new_bid = strategy.calculate_new_bid(
        current_bid=Decimal("1.0"),
        metrics={'acos': 0.15},
        target_metrics={'target_acos': 0.25}
    )
    
    assert new_bid > Decimal("1.0")


def test_cvr_based_strategy_high_cvr():
    strategy = CVRBasedStrategy()
    
    new_bid = strategy.calculate_new_bid(
        current_bid=Decimal("1.0"),
        metrics={'cvr': 0.10},
        target_metrics={'avg_cvr': 0.05}
    )
    
    assert new_bid > Decimal("1.0")


def test_bidding_engine():
    engine = BiddingEngine()
    
    new_bid = engine.execute_bidding(
        strategy_name='acos_target',
        current_bid=Decimal("1.0"),
        metrics={'acos': 0.35, 'clicks': 50},
        target_metrics={'target_acos': 0.25}
    )
    
    assert new_bid > 0
    assert new_bid <= Decimal("1.3")
    assert new_bid >= Decimal("0.5")
