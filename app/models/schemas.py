"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    PURCHASE = "purchase"
    TRANSFER = "transfer"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"


class Transaction(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = Field(..., description="User identifier")
    amount: float = Field(..., gt=0, description="Transaction amount")
    transaction_type: TransactionType = Field(..., description="Type of transaction")
    merchant_id: Optional[str] = Field(None, description="Merchant identifier")
    card_present: bool = Field(True, description="Whether card was physically present")
    latitude: float = Field(..., ge=-90, le=90, description="Transaction latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Transaction longitude")
    device_id: Optional[str] = Field(None, description="Device identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "txn_123456",
                "user_id": "user_789",
                "amount": 1500.00,
                "transaction_type": "purchase",
                "merchant_id": "merch_456",
                "card_present": False,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "device_id": "device_abc"
            }
        }


class FraudPrediction(BaseModel):
    transaction_id: str
    is_fraud: bool
    fraud_probability: float = Field(..., ge=0, le=1)
    risk_level: Literal["low", "medium", "high", "critical"]
    model_version: str
    prediction_time_ms: float
    features_used: dict
    explanation: Optional[dict] = None


class FraudAlert(BaseModel):
    alert_id: str
    transaction_id: str
    user_id: str
    fraud_probability: float
    risk_level: str
    timestamp: datetime
    status: Literal["new", "investigating", "resolved", "false_positive"] = "new"
    assigned_to: Optional[str] = None


class HealthCheck(BaseModel):
    status: str
    version: str
    timestamp: datetime
    services: dict
