from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from ..models.parent import ParentCreate, ParentProfileUpdate
from ..models.child import ChildCreate
from ..models.auth import ParentForgotPassword, ParentLogin, ChildLogin
from ..services.auth_service import AuthService
from ..services.parent_service import ParentService
from ..services.child_service import ChildService
from ..dependencies import get_current_parent_id
from ..models.child import ChildLoginRequest

router = APIRouter(tags=["auth"])


@router.post("/register-parent")
async def register_parent(parent: ParentCreate):
    """Register a new parent account."""
    existing = await ParentService.get_by_email(parent.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    created = await ParentService.create(parent)
    token = AuthService.create_parent_token(created.id)
    return {
        "message": "Parent registered successfully",
        "parent": {
            "id": created.id,
            "name": created.name,
            "email": created.email,
        },
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/login-parent")
async def login_parent(credentials: ParentLogin):
    """Login as parent. Returns JWT access token."""
    parent = await ParentService.get_by_email(credentials.email)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not AuthService.verify_password(credentials.password, parent.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = AuthService.create_parent_token(parent.id)
    return {
        "message": "Login successful",
        "parent": {
            "id": parent.id,
            "name": parent.name,
            "email": parent.email,
        },
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/forgot-parent-password")
async def forgot_parent_password(body: ParentForgotPassword):
    """Reset parent password using registered email."""
    updated = await ParentService.reset_password_by_email(
        body.email,
        body.new_password,
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )
    return {"message": "Password updated successfully"}


@router.get("/parent-profile")
async def get_parent_profile(parent_id: str = Depends(get_current_parent_id)):
    parent = await ParentService.get_by_id(parent_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    children = await ChildService.get_by_parent(parent_id)
    return {
        "parent": {
            "id": parent.id,
            "name": parent.name,
            "email": parent.email,
            "phone": parent.phone,
        },
        "child_count": len(children),
    }


@router.put("/parent-profile")
async def update_parent_profile(
    body: ParentProfileUpdate,
    parent_id: str = Depends(get_current_parent_id),
):
    if body.email is not None:
        existing = await ParentService.get_by_email(body.email)
        if existing and existing.id != parent_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    updated = await ParentService.update_profile(parent_id, body)
    if not updated:
        raise HTTPException(status_code=404, detail="Parent not found")

    children = await ChildService.get_by_parent(parent_id)
    return {
        "message": "Profile updated successfully",
        "parent": {
            "id": updated.id,
            "name": updated.name,
            "email": updated.email,
            "phone": updated.phone,
        },
        "child_count": len(children),
    }


@router.get("/children")
async def get_children(parent_id: str = Depends(get_current_parent_id)):
    """Get all children for the authenticated parent."""
    children = await ChildService.get_by_parent(parent_id)
    return {
        "children": [
            {"id": c.id, "parent_id": c.parent_id, "name": c.name, "age": c.age}
            for c in children
        ],
    }


@router.post("/add-child")
async def add_child(
    child: ChildCreate,
    parent_id: str = Depends(get_current_parent_id),
):
    """Add a child. Requires parent JWT in Authorization header."""
    created = await ChildService.create(child, parent_id)
    return {
        "message": "Child added successfully",
        "child": {
            "id": created.id,
            "parent_id": created.parent_id,
            "name": created.name,
            "age": created.age,
        },
    }


@router.post("/login-child")
async def login_child(body: ChildLoginRequest):
    parent_id = None
    child_input = body.child_id.strip()
    parent_email = (body.parent_email or "").strip().lower()

    if parent_email:
        parent = await ParentService.get_by_email(parent_email)
        if not parent:
            raise HTTPException(401, "Invalid login credentials")
        parent_id = parent.id

    # If login input is a name and multiple matches exist, require parent context.
    if not ObjectId.is_valid(child_input) and not parent_id:
        same_name_count = await ChildService.count_by_name(child_input)
        if same_name_count > 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Multiple children found with this name. Enter parent email to continue.",
            )

    # find child by id OR name (optionally parent-scoped)
    child = await ChildService.get_by_id_or_name(child_input, parent_id=parent_id)

    if not child:
        raise HTTPException(401, "Invalid login credentials")

    # verify password
    if not AuthService.verify_password(
        body.password,
        child.hashed_password
    ):
        raise HTTPException(401, "Invalid login credentials")

    token = AuthService.create_child_token(child.id)

    return {
        "access_token": token,
        "child": {
            "id": child.id,
            "name": child.name
        }
    }
