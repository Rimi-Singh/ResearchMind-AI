from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from scripts.query import answer_question
from services.history_service import HistoryService


router = APIRouter()


# ======================================================
# Request Model
# ======================================================

class ChatRequest(BaseModel):
    question: str
    chat_id: str | None = None


# ======================================================
# Chat Endpoint
# ======================================================

@router.post("/chat")
async def chat(data: ChatRequest):

    try:

        # --------------------------------------------
        # Create a new chat if none exists
        # --------------------------------------------

        if data.chat_id is None:

            new_chat = HistoryService.create_chat(
                title=data.question[:40]
            )

            chat_id = new_chat["id"]

        else:

            chat_id = data.chat_id

        # --------------------------------------------
        # Save User Message
        # --------------------------------------------

        HistoryService.add_message(
            chat_id=chat_id,
            role="user",
            content=data.question
        )

        # --------------------------------------------
        # Get AI Answer
        # --------------------------------------------

        result = answer_question(
            data.question
        )

        # --------------------------------------------
        # Save AI Message
        # --------------------------------------------

        HistoryService.add_message(
            chat_id=chat_id,
            role="assistant",
            content=result["answer"]
        )

        # --------------------------------------------
        # Return Response
        # --------------------------------------------

        result["chat_id"] = chat_id

        return JSONResponse(
            content=result
        )

    except Exception as e:

        return JSONResponse(

            status_code=500,

            content={

                "answer": "Unable to generate answer.",

                "sources": [],

                "retrieved_chunks": [],

                "error": str(e)

            }

        )