"""
ResearchMind AI Guardrails

This module contains lightweight guardrails for validating
user questions before they reach the RAG pipeline.
"""

import re


class Guardrails:

    # -----------------------------------------------------
    # Prompt Injection Patterns
    # -----------------------------------------------------

    PROMPT_INJECTION_PATTERNS = [

        "ignore previous instructions",
        "ignore all previous instructions",
        "forget previous instructions",
        "forget all instructions",
        "system prompt",
        "developer prompt",
        "developer message",
        "reveal prompt",
        "show prompt",
        "print prompt",
        "repeat your instructions",
        "act as chatgpt",
        "act like chatgpt",
        "jailbreak",
        "bypass",
        "override"

    ]

    # -----------------------------------------------------
    # Harmful Requests
    # -----------------------------------------------------

    HARMFUL_PATTERNS = [

        "hack",
        "hacking",
        "malware",
        "virus",
        "trojan",
        "ransomware",
        "phishing",
        "ddos",
        "exploit",
        "sql injection",
        "keylogger",
        "bomb",
        "weapon"

    ]

    # -----------------------------------------------------
    # Off-topic Questions
    # -----------------------------------------------------

    OFF_TOPIC_PATTERNS = [

        "weather",
        "ipl",
        "cricket",
        "football",
        "movie",
        "movies",
        "actor",
        "actress",
        "netflix",
        "amazon prime",
        "capital of",
        "prime minister",
        "president of",
        "recipe",
        "song",
        "lyrics"

    ]

    # -----------------------------------------------------
    # Empty Question
    # -----------------------------------------------------

    @staticmethod
    def is_empty(question: str):

        return len(question.strip()) == 0

    # -----------------------------------------------------
    # Prompt Injection
    # -----------------------------------------------------

    @classmethod
    def is_prompt_injection(cls, question: str):

        q = question.lower()

        return any(pattern in q for pattern in cls.PROMPT_INJECTION_PATTERNS)

    # -----------------------------------------------------
    # Harmful Request
    # -----------------------------------------------------

    @classmethod
    def is_harmful(cls, question: str):

        q = question.lower()

        return any(pattern in q for pattern in cls.HARMFUL_PATTERNS)

    # -----------------------------------------------------
    # Off Topic
    # -----------------------------------------------------

    @classmethod
    def is_off_topic(cls, question: str):

        q = question.lower()

        return any(pattern in q for pattern in cls.OFF_TOPIC_PATTERNS)

    # -----------------------------------------------------
    # Validate
    # -----------------------------------------------------

    @classmethod
    def validate(cls, question: str):

        if cls.is_empty(question):

            return False, "Please enter a question."

        if cls.is_prompt_injection(question):

            return (
                False,
                "I can't comply with requests that attempt to reveal or modify my internal instructions."
            )

        if cls.is_harmful(question):

            return (
                False,
                "I can't assist with harmful or illegal requests."
            )

        if cls.is_off_topic(question):

            return (
                False,
                "I'm designed to answer questions based on the uploaded research papers."
            )

        return True, None