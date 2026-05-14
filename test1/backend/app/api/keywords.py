from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.cache import get_cache, CacheService
from app.core.logger import logger
from app.models.schemas import KeywordRecommendation
from app.models.models import Keyword

router = APIRouter(prefix="/keywords", tags=["keywords"])


@router.get("/recommend", response_model=List[KeywordRecommendation])
async def get_keyword_recommendations(
    asin: str = Query(..., description="ASIN to analyze"),
    limit: int = Query(default=20, le=100, description="Maximum number of recommendations"),
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache)
):
    cache_key = CacheService.build_key("keyword_recommendations", asin, str(limit))
    
    cached_data = cache.get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for keyword recommendations: {cache_key}")
        return cached_data
    
    keywords = db.query(Keyword).filter(
        Keyword.keyword_text.ilike(f"%{asin}%")
    ).limit(limit).all()
    
    recommendations = []
    for keyword in keywords:
        score = 0.5
        if keyword.orders and keyword.orders > 0:
            score = min(1.0, keyword.orders / 10.0)
        
        recommendations.append(KeywordRecommendation(
            keyword_text=keyword.keyword_text,
            match_type=keyword.match_type or "broad",
            suggested_bid=float(keyword.bid or 0.5),
            score=score,
            reason=f"Based on historical performance: {keyword.orders or 0} orders"
        ))
    
    if not recommendations:
        default_keywords = [
            KeywordRecommendation(
                keyword_text=f"{asin} product",
                match_type="broad",
                suggested_bid=0.50,
                score=0.7,
                reason="Default recommendation for new ASIN"
            ),
            KeywordRecommendation(
                keyword_text=f"{asin} buy",
                match_type="phrase",
                suggested_bid=0.75,
                score=0.8,
                reason="Purchase intent keyword"
            )
        ]
        recommendations.extend(default_keywords)
    
    cache.set(cache_key, [r.dict() for r in recommendations], ttl=300)
    logger.info(f"Generated {len(recommendations)} keyword recommendations for ASIN {asin}")
    
    return recommendations


@router.post("/negative")
async def add_negative_keywords(
    keyword_ids: List[str],
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache)
):
    added_count = 0
    
    for keyword_id in keyword_ids:
        keyword = db.query(Keyword).filter(
            Keyword.keyword_id == keyword_id
        ).first()
        
        if keyword:
            keyword.is_negative = True
            keyword.updated_at = datetime.utcnow()
            added_count += 1
    
    db.commit()
    
    cache.invalidate_pattern("keyword_*")
    
    logger.info(f"Added {added_count} negative keywords")
    
    return {"success": True, "added_count": added_count}


@router.get("/negative")
async def get_negative_keywords(
    campaign_id: str = Query(None),
    limit: int = Query(default=100, le=500),
    db: Session = Depends(get_db)
):
    query = db.query(Keyword).filter(Keyword.is_negative == True)
    
    if campaign_id:
        query = query.filter(Keyword.campaign_id == campaign_id)
    
    keywords = query.limit(limit).all()
    
    logger.info(f"Retrieved {len(keywords)} negative keywords")
    
    return keywords


@router.delete("/negative")
async def remove_negative_keywords(
    keyword_ids: List[str],
    db: Session = Depends(get_db),
    cache: CacheService = Depends(get_cache)
):
    removed_count = 0
    
    for keyword_id in keyword_ids:
        keyword = db.query(Keyword).filter(
            Keyword.keyword_id == keyword_id
        ).first()
        
        if keyword:
            keyword.is_negative = False
            keyword.updated_at = datetime.utcnow()
            removed_count += 1
    
    db.commit()
    
    cache.invalidate_pattern("keyword_*")
    
    logger.info(f"Removed {removed_count} negative keywords")
    
    return {"success": True, "removed_count": removed_count}
