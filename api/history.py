from fastapi import APIRouter

from services.history_service import HistoryService


router = APIRouter(
    prefix="/history",
    tags=["History"]
)


# ======================================================
# Get all chats
# ======================================================

@router.get("/")
async def get_history():

    return HistoryService.get_all()


# ======================================================
# Create new chat
# ======================================================

@router.post("/new")
async def create_chat():

    return HistoryService.create_chat()


# ======================================================
# Get one chat
# ======================================================

@router.get("/{chat_id}")
async def get_chat(chat_id: str):

    chat = HistoryService.get(chat_id)

    if chat is None:

        return {
            "success": False,
            "message": "Chat not found."
        }

    return chat


# ======================================================
# Rename chat
# ======================================================

@router.put("/{chat_id}/rename")
async def rename_chat(
    chat_id: str,
    title: str
):

    HistoryService.rename(
        chat_id,
        title
    )

    return {
        "success": True
    }


# ======================================================
# Delete chat
# ======================================================

@router.delete("/{chat_id}")
async def delete_chat(chat_id: str):

    HistoryService.delete(chat_id)

    return {
        "success": True
    }