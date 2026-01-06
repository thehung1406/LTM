"""Friend management endpoints."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status

from models.user import User
from schemas.friend import FriendRequestCreate, FriendRequestResponse, FriendResponse
from services.friend_service import (
    send_friend_request,
    accept_friend_request,
    reject_friend_request,
    get_friend_requests,
    get_friends_list,
    remove_friend,
    block_user
)
from utils.dependencies import get_current_user

router = APIRouter(prefix="/friends", tags=["Friends"])


@router.post("/request", response_model=FriendRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_friend_request(
    data: FriendRequestCreate,
    current_user: User = Depends(get_current_user)
):
    """Send a friend request to another user."""
    friend_request = await send_friend_request(current_user.id, data.addressee_id)
    return FriendRequestResponse(
        id=friend_request.id,
        requester_id=friend_request.requester_id,
        addressee_id=friend_request.addressee_id,
        status=friend_request.status,
        created_at=friend_request.created_at,
        updated_at=friend_request.updated_at
    )


@router.patch("/request/{request_id}/accept", response_model=FriendRequestResponse)
async def accept_request(
    request_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Accept a pending friend request."""
    friend_request = await accept_friend_request(request_id, current_user.id)
    return FriendRequestResponse(
        id=friend_request.id,
        requester_id=friend_request.requester_id,
        addressee_id=friend_request.addressee_id,
        status=friend_request.status,
        created_at=friend_request.created_at,
        updated_at=friend_request.updated_at
    )


@router.patch("/request/{request_id}/reject", response_model=FriendRequestResponse)
async def reject_request(
    request_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Reject a pending friend request."""
    friend_request = await reject_friend_request(request_id, current_user.id)
    return FriendRequestResponse(
        id=friend_request.id,
        requester_id=friend_request.requester_id,
        addressee_id=friend_request.addressee_id,
        status=friend_request.status,
        created_at=friend_request.created_at,
        updated_at=friend_request.updated_at
    )


@router.get("/requests", response_model=List[FriendRequestResponse])
async def list_friend_requests(current_user: User = Depends(get_current_user)):
    """Get all pending friend requests for the current user."""
    requests = await get_friend_requests(current_user.id)
    return [
        FriendRequestResponse(
            id=req.id,
            requester_id=req.requester_id,
            addressee_id=req.addressee_id,
            status=req.status,
            created_at=req.created_at,
            updated_at=req.updated_at
        )
        for req in requests
    ]


@router.delete("/{friendship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_friend(
    friendship_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Remove a friend."""
    await remove_friend(friendship_id, current_user.id)


@router.post("/block/{user_id}", response_model=FriendRequestResponse)
async def block_user_endpoint(
    user_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Block a user."""
    block = await block_user(current_user.id, user_id)
    return FriendRequestResponse(
        id=block.id,
        requester_id=block.requester_id,
        addressee_id=block.addressee_id,
        status=block.status,
        created_at=block.created_at,
        updated_at=block.updated_at
    )

