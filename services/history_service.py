import json
import os
import uuid
from datetime import datetime


HISTORY_FILE = "data/history.json"


class HistoryService:
    """
    Handles chat history storage.

    Stores conversations in a JSON file.

    Each conversation contains:
        - id
        - title
        - created_at
        - updated_at
        - messages
    """

    @staticmethod
    def initialize():

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(HISTORY_FILE):

            with open(HISTORY_FILE, "w", encoding="utf-8") as f:

                json.dump([], f, indent=4)

    @staticmethod
    def load():

        HistoryService.initialize()

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    @staticmethod
    def save(data):

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4)

    @staticmethod
    def create_chat(title="New Chat"):

        chats = HistoryService.load()

        chat = {

            "id": str(uuid.uuid4()),

            "title": title,

            "created_at": datetime.now().isoformat(),

            "updated_at": datetime.now().isoformat(),

            "messages": []

        }

        chats.insert(0, chat)

        HistoryService.save(chats)

        return chat

    @staticmethod
    def get_all():

        return HistoryService.load()

    @staticmethod
    def get(chat_id):

        chats = HistoryService.load()

        for chat in chats:

            if chat["id"] == chat_id:

                return chat

        return None

    @staticmethod
    def add_message(chat_id, role, content):

        chats = HistoryService.load()

        for chat in chats:

            if chat["id"] == chat_id:

                chat["messages"].append({

                    "role": role,

                    "content": content,

                    "timestamp": datetime.now().isoformat()

                })

                chat["updated_at"] = datetime.now().isoformat()

                HistoryService.save(chats)

                return

    @staticmethod
    def rename(chat_id, title):

        chats = HistoryService.load()

        for chat in chats:

            if chat["id"] == chat_id:

                chat["title"] = title

                chat["updated_at"] = datetime.now().isoformat()

                HistoryService.save(chats)

                return

    @staticmethod
    def delete(chat_id):

        chats = HistoryService.load()

        chats = [

            chat

            for chat in chats

            if chat["id"] != chat_id

        ]

        HistoryService.save(chats)
        