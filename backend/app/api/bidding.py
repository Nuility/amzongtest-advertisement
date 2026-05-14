from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.schemas import (
    BiddingStrategyRequest,
    BiddingResult,
    KeywordRecommendation
)
from app.services.bidding_service import BiddingEngine
from app.models.models import Keyword, BiddingLog

router = APIRouter(prefix="/bidding", tags=["bidding"])
bidding_engine = BiddingEngine()


@router.post("/execute", response_model=List[BiddingResult])
async def execute_bidding(
    request: BiddingStrategyRequest,
    db: Session = Depends(get_db)
):
    results = []
    
    try:
        for keyword_id in request.keyword_ids:
            keyword = db.query(Keyword).filter(
                Keyword.keyword_id == keyword_id
            ).first()
            
            if not keyword:
                continue
            
            new_bid = bidding_engine.execute_bidding(
                strategy_name=request.strategy_name,
                current_bid=keyword.bid,
                metrics={'acos': 0.25, 'clicks': 50},
                target_metrics={'target_acos': float(request.target_acos or 0.25)}
            )
            
            if new_bid != keyword.bid:
                old_bid_value = keyword.bid  # 先保存旧值
                log = BiddingLog(
                    log_id=f"log_{keyword_id}_{datetime.now().timestamp()}",
                    keyword_id=keyword_id,
                    old_bid=old_bid_value,
                    new_bid=new_bid,
                    strategy=request.strategy_name,
                    reason=f"ACoS target adjustment"
                )
                db.add(log)
                
                keyword.bid = new_bid
                db.commit()
                
                results.append(BiddingResult(
                    keyword_id=keyword_id,
                    old_bid=old_bid_value,
                    new_bid=new_bid,
                    reason="ACoS adjustment",
                    timestamp=datetime.now()
                ))
        
        return results
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Bidding execution failed: {str(e)}")


@router.get("/logs")
async def get_bidding_logs(
    account_id: str,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    logs = db.query(BiddingLog).limit(limit).all()
    return logs
