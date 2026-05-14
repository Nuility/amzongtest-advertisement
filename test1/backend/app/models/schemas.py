from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Any
from decimal import Decimal


class CampaignBase(BaseModel):
    campaign_id: str
    campaign_name: str
    campaign_type: str
    budget: Decimal
    status: str


class CampaignResponse(CampaignBase):
    account_id: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class KeywordBase(BaseModel):
    keyword_id: str
    keyword_text: str
    match_type: str
    bid: Decimal
    status: str


class KeywordResponse(KeywordBase):
    campaign_id: str
    ad_group_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class MetricBase(BaseModel):
    impressions: int = Field(default=0)
    clicks: int = Field(default=0)
    spend: Decimal = Field(default=Decimal("0"))
    orders: int = Field(default=0)
    sales: Decimal = Field(default=Decimal("0"))


class CalculatedMetrics(MetricBase):
    ctr: float = Field(default=0.0)
    cpc: float = Field(default=0.0)
    cvr: float = Field(default=0.0)
    acos: float = Field(default=0.0)
    roas: float = Field(default=0.0)


class PerformanceMetricsResponse(BaseModel):
    entity_id: str = Field(..., description="Entity ID (campaign or keyword)")
    entity_name: str = Field(..., description="Entity name")
    entity_type: str = Field(..., description="Entity type: campaign or keyword")
    impressions: int = Field(default=0, description="Number of impressions")
    clicks: int = Field(default=0, description="Number of clicks")
    ctr: float = Field(default=0.0, description="Click-through rate")
    cpc: float = Field(default=0.0, description="Cost per click")
    spend: float = Field(default=0.0, description="Total spend")
    orders: int = Field(default=0, description="Number of orders")
    sales: float = Field(default=0.0, description="Total sales")
    cvr: float = Field(default=0.0, description="Conversion rate")
    acos: float = Field(default=0.0, description="Advertising Cost of Sales")
    roas: float = Field(default=0.0, description="Return on Advertising Spend")
    
    class Config:
        json_schema_extra = {
            "example": {
                "entity_id": "camp_123",
                "entity_name": "Summer Sale Campaign",
                "entity_type": "campaign",
                "impressions": 10000,
                "clicks": 500,
                "ctr": 0.05,
                "cpc": 0.75,
                "spend": 375.0,
                "orders": 25,
                "sales": 1250.0,
                "cvr": 0.05,
                "acos": 0.30,
                "roas": 3.33
            }
        }


class BiddingStrategyRequest(BaseModel):
    strategy_name: str = Field(..., description="Strategy name: acos_target or cvr_based")
    keyword_ids: List[str] = Field(..., description="List of keyword IDs to adjust")
    target_acos: Optional[Decimal] = Field(None, description="Target ACoS for acos_target strategy")
    target_cvr: Optional[Decimal] = Field(None, description="Target CVR for cvr_based strategy")
    
    @validator('strategy_name')
    def validate_strategy_name(cls, v):
        if v not in ['acos_target', 'cvr_based']:
            raise ValueError('strategy_name must be either "acos_target" or "cvr_based"')
        return v


class BiddingResult(BaseModel):
    keyword_id: str = Field(..., description="Keyword ID")
    old_bid: Decimal = Field(..., description="Previous bid amount")
    new_bid: Decimal = Field(..., description="New bid amount")
    reason: str = Field(..., description="Reason for adjustment")
    timestamp: datetime = Field(..., description="Timestamp of adjustment")
    
    class Config:
        json_schema_extra = {
            "example": {
                "keyword_id": "kw_123",
                "old_bid": 0.75,
                "new_bid": 0.82,
                "reason": "ACoS target adjustment",
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class KeywordRecommendation(BaseModel):
    keyword_text: str = Field(..., description="Recommended keyword text")
    match_type: str = Field(default="broad", description="Match type: broad, phrase, or exact")
    suggested_bid: float = Field(..., description="Suggested bid amount")
    score: float = Field(..., ge=0.0, le=1.0, description="Recommendation score (0-1)")
    reason: str = Field(..., description="Reason for recommendation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "keyword_text": "wireless headphones",
                "match_type": "phrase",
                "suggested_bid": 0.85,
                "score": 0.85,
                "reason": "High conversion keyword with strong performance history"
            }
        }


class DashboardOverview(BaseModel):
    total_spend: float = Field(default=0.0, description="Total advertising spend")
    total_sales: float = Field(default=0.0, description="Total sales revenue")
    average_acos: float = Field(default=0.0, description="Average ACoS across all campaigns")
    average_roas: float = Field(default=0.0, description="Average ROAS across all campaigns")
    total_clicks: int = Field(default=0, description="Total number of clicks")
    total_orders: int = Field(default=0, description="Total number of orders")
    active_campaigns: int = Field(default=0, description="Number of active campaigns")
    active_keywords: int = Field(default=0, description="Number of active keywords")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_spend": 5000.0,
                "total_sales": 20000.0,
                "average_acos": 0.25,
                "average_roas": 4.0,
                "total_clicks": 8000,
                "total_orders": 400,
                "active_campaigns": 15,
                "active_keywords": 350
            }
        }


class ErrorResponse(BaseModel):
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[List[Any]] = Field(None, description="Error details")
    request_id: str = Field(..., description="Request ID for tracking")
    timestamp: str = Field(..., description="Error timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error_code": "DATABASE_ERROR",
                "message": "Database operation failed",
                "details": None,
                "request_id": "uuid-1234-5678",
                "timestamp": "2024-01-15T10:30:00"
            }
        }
