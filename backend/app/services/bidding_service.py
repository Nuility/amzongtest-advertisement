from decimal import Decimal
from abc import ABC, abstractmethod
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class BiddingStrategy(ABC):
    
    @abstractmethod
    def calculate_new_bid(
        self,
        current_bid: Decimal,
        metrics: Dict[str, float],
        target_metrics: Dict[str, float]
    ) -> Decimal:
        pass
    
    @abstractmethod
    def should_skip(self, metrics: Dict[str, float]) -> bool:
        pass


class ACoSTargetStrategy(BiddingStrategy):
    
    def __init__(self, adjustment_factor: float = 0.1):
        self.adjustment_factor = adjustment_factor
    
    def calculate_new_bid(
        self,
        current_bid: Decimal,
        metrics: Dict[str, float],
        target_metrics: Dict[str, float]
    ) -> Decimal:
        current_acos = metrics.get('acos', 0.0)
        target_acos = target_metrics.get('target_acos', 0.25)
        
        if current_acos > target_acos * 1.2:
            adjustment = -self.adjustment_factor
        elif current_acos < target_acos * 0.8:
            adjustment = self.adjustment_factor
        else:
            adjustment = 0.0
        
        new_bid = current_bid * Decimal(str(1 + adjustment))
        return round(new_bid, 2)
    
    def should_skip(self, metrics: Dict[str, float]) -> bool:
        return metrics.get('clicks', 0) < 10


class CVRBasedStrategy(BiddingStrategy):
    
    def __init__(self, adjustment_factor: float = 0.15):
        self.adjustment_factor = adjustment_factor
    
    def calculate_new_bid(
        self,
        current_bid: Decimal,
        metrics: Dict[str, float],
        target_metrics: Dict[str, float]
    ) -> Decimal:
        cvr = metrics.get('cvr', 0.0)
        avg_cvr = target_metrics.get('avg_cvr', 0.05)
        
        if cvr > avg_cvr * 1.5:
            adjustment = self.adjustment_factor
        elif cvr < avg_cvr * 0.5:
            adjustment = -self.adjustment_factor * 1.5
        else:
            adjustment = 0.0
        
        new_bid = current_bid * Decimal(str(1 + adjustment))
        return round(new_bid, 2)
    
    def should_skip(self, metrics: Dict[str, float]) -> bool:
        return metrics.get('clicks', 0) < 20


class BiddingEngine:
    
    def __init__(self):
        self.strategies = {
            'acos_target': ACoSTargetStrategy(),
            'cvr_based': CVRBasedStrategy()
        }
    
    def get_strategy(self, strategy_name: str) -> BiddingStrategy:
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            raise ValueError(f"Strategy {strategy_name} not found")
        return strategy
    
    def execute_bidding(
        self,
        strategy_name: str,
        current_bid: Decimal,
        metrics: Dict[str, float],
        target_metrics: Dict[str, float]
    ) -> Decimal:
        strategy = self.get_strategy(strategy_name)
        
        if strategy.should_skip(metrics):
            logger.info(f"Skipping adjustment: insufficient data")
            return current_bid
        
        new_bid = strategy.calculate_new_bid(
            current_bid=current_bid,
            metrics=metrics,
            target_metrics=target_metrics
        )
        
        max_bid = current_bid * Decimal('1.3')
        min_bid = current_bid * Decimal('0.5')
        new_bid = max(min_bid, min(max_bid, new_bid))
        
        return new_bid
