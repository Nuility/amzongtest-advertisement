"""API路由模块"""
from app.api.metrics import router as metrics_router
from app.api.bidding import router as bidding_router
from app.api.keywords import router as keywords_router

__all__ = ["metrics_router", "bidding_router", "keywords_router"]
