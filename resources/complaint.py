from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from managers.auth import oauth2_schema, is_complainer, is_admin, is_approver
from managers.complain import ComplaintManager
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut

router = APIRouter(tags=["Complaints"])


@router.get("/complaints", dependencies=[Depends(oauth2_schema)], response_model=List[ComplaintOut])
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_complaints(user)


@router.post(
    "/complaints",
    dependencies=[
        Depends(oauth2_schema),
        Depends(is_complainer)
    ],
    response_model=ComplaintOut
)
async def create_complaint(request: Request, compliant: ComplaintIn):
    return await ComplaintManager.create_complaint(request, compliant.dict())


@router.delete(
    "/complaints/{complaint_id}", dependencies=[Depends(oauth2_schema), Depends(is_admin)], status_code=204
)
async def delete_complaint(complaint_id: int):
    await ComplaintManager.delete_complaint(complaint_id)


@router.put("/complaints/{complaint_id}/approve",
            dependencies=[Depends(oauth2_schema), Depends(is_approver)],
            status_code=204
            )
async def approve_complaint(complaint_id):
    await ComplaintManager.approve(complaint_id)


@router.put("/complaints/{complaint_id}/reject",
            dependencies=[Depends(oauth2_schema), Depends(is_approver)],
            status_code=204
            )
async def reject_complaint(complaint_id):
    await ComplaintManager.reject(complaint_id)