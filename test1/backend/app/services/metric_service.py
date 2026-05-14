from decimal import Decimal
from typing import Dict


class MetricCalculator:
    
    @staticmethod
    def calculate_ctr(clicks: int, impressions: int) -> float:
        if impressions <= 0:
            return 0.0
        return clicks / impressions
    
    @staticmethod
    def calculate_cvr(orders: int, clicks: int) -> float:
        if clicks <= 0:
            return 0.0
        return orders / clicks
    
    @staticmethod
    def calculate_cpc(spend: Decimal, clicks: int) -> float:
        if clicks <= 0:
            return 0.0
        return float(spend / clicks)
    
    @staticmethod
    def calculate_acos(spend: Decimal, sales: Decimal) -> float:
        if sales <= 0:
            return 0.0
        return float(spend / sales)
    
    @staticmethod
    def calculate_roas(sales: Decimal, spend: Decimal) -> float:
        if spend <= 0:
            return 0.0
        return float(sales / spend)
    
    def calculate_all_metrics(
        self,
        impressions: int,
        clicks: int,
        spend: Decimal,
        orders: int,
        sales: Decimal
    ) -> Dict[str, float]:
        return {
            'ctr': self.calculate_ctr(clicks, impressions),
            'cpc': self.calculate_cpc(spend, clicks),
            'cvr': self.calculate_cvr(orders, clicks),
            'acos': self.calculate_acos(spend, sales),
            'roas': self.calculate_roas(sales, spend)
        }
