"""Vendor listing endpoints."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.database import get_db
from api.models import VendorListing
from api.schemas import VendorOut

router = APIRouter(prefix="/api/vendors", tags=["vendors"])


@router.get("", response_model=list[VendorOut])
async def list_vendors(
    vendor_type: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    region_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    q = select(VendorListing).options(selectinload(VendorListing.venue))
    if vendor_type:
        q = q.where(VendorListing.vendor_type == vendor_type)
    if featured is not None:
        q = q.where(VendorListing.featured == featured)
    if region_id:
        q = q.where(VendorListing.region_id == region_id)
    q = q.order_by(VendorListing.featured.desc(), VendorListing.vendor_name).limit(200)
    result = await db.execute(q)
    return [VendorOut.model_validate(v) for v in result.scalars().all()]
