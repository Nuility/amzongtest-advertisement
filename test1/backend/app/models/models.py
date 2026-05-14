from sqlalchemy import Column, String, DECIMAL, DateTime, Enum, JSON, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class CampaignType(enum.Enum):
    SP = "sponsored_products"
    SB = "sponsored_brands"
    SD = "sponsored_display"


class CampaignStatus(enum.Enum):
    ENABLED = "enabled"
    PAUSED = "paused"
    ARCHIVED = "archived"


class Campaign(Base):
    __tablename__ = "campaigns"
    
    campaign_id = Column(String(50), primary_key=True)
    account_id = Column(String(50), nullable=False, index=True)
    campaign_name = Column(String(255))
    campaign_type = Column(Enum(CampaignType))
    budget = Column(DECIMAL(10, 2))
    status = Column(Enum(CampaignStatus))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    targeting_type = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class AdGroup(Base):
    __tablename__ = "ad_groups"
    
    ad_group_id = Column(String(50), primary_key=True)
    campaign_id = Column(String(50), index=True)
    ad_group_name = Column(String(255))
    default_bid = Column(DECIMAL(10, 2))
    status = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class MatchType(enum.Enum):
    BROAD = "broad"
    PHRASE = "phrase"
    EXACT = "exact"


class Keyword(Base):
    __tablename__ = "keywords"
    
    keyword_id = Column(String(50), primary_key=True)
    campaign_id = Column(String(50), index=True)
    ad_group_id = Column(String(50), index=True)
    keyword_text = Column(String(255))
    match_type = Column(Enum(MatchType))
    bid = Column(DECIMAL(10, 2))
    status = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Account(Base):
    __tablename__ = "accounts"
    
    account_id = Column(String(50), primary_key=True)
    account_name = Column(String(255))
    seller_id = Column(String(50))
    marketplace = Column(String(10))
    region = Column(String(10))
    credentials = Column(JSON)
    is_active = Column(String(10), default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class BiddingLog(Base):
    __tablename__ = "bidding_logs"
    
    log_id = Column(String(50), primary_key=True)
    keyword_id = Column(String(50), index=True)
    old_bid = Column(DECIMAL(10, 2))
    new_bid = Column(DECIMAL(10, 2))
    strategy = Column(String(50))
    reason = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class TeamMember(Base):
    __tablename__ = "team_members"
    
    member_id = Column(String(50), primary_key=True)
    user_id = Column(String(50))
    team_id = Column(String(50), index=True)
    role = Column(String(20))
    managed_accounts = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())


class KPIConfig(Base):
    __tablename__ = "kpi_configs"
    
    kpi_id = Column(String(50), primary_key=True)
    account_id = Column(String(50), index=True)
    member_id = Column(String(50), index=True)
    metric_type = Column(String(50))
    target_value = Column(DECIMAL(10, 4))
    weight = Column(DECIMAL(5, 2))
    period = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())


user_role_table = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', String(50), ForeignKey('users.user_id'), primary_key=True),
    Column('role_id', String(50), ForeignKey('roles.role_id'), primary_key=True)
)

role_permission_table = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', String(50), ForeignKey('roles.role_id'), primary_key=True),
    Column('permission_id', String(50), ForeignKey('permissions.permission_id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    roles = relationship("Role", secondary=user_role_table, back_populates="users")


class Role(Base):
    __tablename__ = "roles"
    
    role_id = Column(String(50), primary_key=True)
    role_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    
    users = relationship("User", secondary=user_role_table, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permission_table, back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"
    
    permission_id = Column(String(50), primary_key=True)
    permission_name = Column(String(100), unique=True, nullable=False)
    resource = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    
    roles = relationship("Role", secondary=role_permission_table, back_populates="permissions")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    log_id = Column(String(50), primary_key=True)
    user_id = Column(String(50), index=True)
    action = Column(String(100), nullable=False)
    resource = Column(String(100), nullable=False)
    resource_id = Column(String(50))
    details = Column(JSON)
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
