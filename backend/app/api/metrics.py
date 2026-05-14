from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from decimal import Decimal

from app.core.database import get_db
from app.core.cache import get_cache, CacheService
from app.core.logger import logger
from app.models.schemas import (
    CampaignResponse,
    KeywordResponse,
    PerformanceMetricsResponse,
    DashboardOverview
)
from app.models.models import Campaign, Keyword
from app.services.metric_service import MetricCalculator

router = APIRouter(prefix="/metrics", tags=["metrics"])
metric_calculator = MetricCalculator()


@router.get("/campaigns", response_model=List[PerformanceMetricsResponse])
async def get_campaign_metrics(
    account_id: str = Query(..., description="Account ID"),
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache)
):
    cache_key = CacheService.build_key("campaign_metrics", account_id, str(start_date), str(end_date))
    
    cached_data = cache.get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for campaign metrics: {cache_key}")
        return cached_data
    
    campaigns = db.query(Campaign).filter(
        Campaign.account_id == account_id
    ).all()
    
    results = []
    for campaign in campaigns:
        metrics = metric_calculator.calculate_all_metrics(
            impressions=campaign.impressions or 0,
            clicks=campaign.clicks or 0,
            spend=Decimal(str(campaign.spend or 0)),
            orders=campaign.orders or 0,
            sales=Decimal(str(campaign.sales or 0))
        )
        
        results.append(PerformanceMetricsResponse(
            entity_id=campaign.campaign_id,
            entity_name=campaign.campaign_name,
            entity_type="campaign",
            impressions=campaign.impressions or 0,
            clicks=campaign.clicks or 0,
            ctr=metrics['ctr'],
            cpc=metrics['cpc'],
            spend=float(campaign.spend or 0),
            orders=campaign.orders or 0,
            sales=float(campaign.sales or 0),
            cvr=metrics['cvr'],
            acos=metrics['acos'],
            roas=metrics['roas']
        ))
    
    cache.set(cache_key, [r.dict() for r in results], ttl=300)
    logger.info(f"Retrieved {len(results)} campaign metrics for account {account_id}")
    
    return results


@router.get("/keywords", response_model=List[PerformanceMetricsResponse])
async def get_keyword_metrics(
    campaign_id: str = Query(..., description="Campaign ID"),
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache)
):
    cache_key = CacheService.build_key("keyword_metrics", campaign_id, str(start_date), str(end_date))
    
    cached_data = cache.get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for keyword metrics: {cache_key}")
        return cached_data
    
    keywords = db.query(Keyword).filter(
        Keyword.campaign_id == campaign_id
    ).all()
    
    results = []
    for keyword in keywords:
        metrics = metric_calculator.calculate_all_metrics(
            impressions=keyword.impressions or 0,
            clicks=keyword.clicks or 0,
            spend=Decimal(str(keyword.spend or 0)),
            orders=keyword.orders or 0,
            sales=Decimal(str(keyword.sales or 0))
        )
        
        results.append(PerformanceMetricsResponse(
            entity_id=keyword.keyword_id,
            entity_name=keyword.keyword_text,
            entity_type="keyword",
            impressions=keyword.impressions or 0,
            clicks=keyword.clicks or 0,
            ctr=metrics['ctr'],
            cpc=metrics['cpc'],
            spend=float(keyword.spend or 0),
            orders=keyword.orders or 0,
            sales=float(keyword.sales or 0),
            cvr=metrics['cvr'],
            acos=metrics['acos'],
            roas=metrics['roas']
        ))
    
    cache.set(cache_key, [r.dict() for r in results], ttl=300)
    logger.info(f"Retrieved {len(results)} keyword metrics for campaign {campaign_id}")
    
    return results


@router.get("/dashboard/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    account_id: str = Query(..., description="Account ID"),
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache)
):
    cache_key = CacheService.build_key("dashboard_overview", account_id, str(start_date), str(end_date))
    
    cached_data = cache.get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for dashboard overview: {cache_key}")
        return DashboardOverview(**cached_data)
    
    campaigns = db.query(Campaign).filter(
        Campaign.account_id == account_id
    ).all()
    
    total_spend = sum(float(c.spend or 0) for c in campaigns)
    total_sales = sum(float(c.sales or 0) for c in campaigns)
    total_clicks = sum(c.clicks or 0 for c in campaigns)
    total_orders = sum(c.orders or 0 for c in campaigns)
    active_campaigns = len(campaigns)
    
    total_keywords = 0
    for campaign in campaigns:
        keyword_count = db.query(Keyword).filter(
            Keyword.campaign_id == campaign.campaign_id
        ).count()
        total_keywords += keyword_count
    
    average_acos = metric_calculator.calculate_acos(
        Decimal(str(total_spend)),
        Decimal(str(total_sales))
    )
    
    average_roas = metric_calculator.calculate_roas(
        Decimal(str(total_sales)),
        Decimal(str(total_spend))
    )
    
    overview = DashboardOverview(
        total_spend=total_spend,
        total_sales=total_sales,
        average_acos=average_acos,
        average_roas=average_roas,
        total_clicks=total_clicks,
        total_orders=total_orders,
        active_campaigns=active_campaigns,
        active_keywords=total_keywords
    )
    
    cache.set(cache_key, overview.dict(), ttl=300)
    logger.info(f"Generated dashboard overview for account {account_id}")
    
    return overview
