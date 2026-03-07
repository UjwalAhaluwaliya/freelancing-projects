from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict

from services.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


# simple hard-coded FAQ map; keys should be lowercase
FAQ: Dict[str, str] = {
    "reset password": "To reset your password, go to the profile page and click the `Reset password` button. An email with further instructions will be sent.",
    "vehicle types": "The system currently supports vans, trucks, and motorcycles. More types may be added later.",
    "how do i create a shipment": "Use the Shipments page and click on `New Shipment` to fill in the details.",
    "what is the on\-time rate": "The on-time rate shown in Analytics represents the percentage of delivered shipments that arrived by or before their estimated delivery time.",
    "how can i track a shipment": "Go to the Tracking page and enter the shipment ID or use the filters to locate it. You'll see its current status and ETA.",
    "who can manage users": "Only users with the `admin` role can access User Management to add, edit, or deactivate accounts.",
    "can i change my role": "Roles are assigned by administrators. If you need a different role, contact an admin to request the change.",
    "what happens when a vehicle is under maintenance": "A vehicle marked as `maintenance` won't be assigned new deliveries until its status is changed back to `available` or `in_transit`.",
}


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    """Return a canned response matching one of the predefined questions.

    The match is very simple (substring search); you can improve it later.
    """
    txt = request.question.strip().lower()
    for key, ans in FAQ.items():
        if key in txt:
            return ChatResponse(answer=ans)

    return ChatResponse(answer="Sorry, I don't know the answer to that question.")
