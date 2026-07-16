from services.rag_service import rag_service
from scripts.logger import logger


# =====================================================
# Answer Question
# =====================================================

def answer_question(question: str):
    """
    Main entry point for answering user questions.
    """

    logger.info("=" * 70)
    logger.info(f"Question Received: {question}")

    try:

        result = rag_service.answer(question)

        logger.info("Answer generated successfully.")

        return result

    except Exception as e:

        logger.exception("Failed to answer question.")

        return {

            "answer": "Unable to generate an answer.",

            "sources": [],

            "retrieved_chunks": [],

            "error": str(e)

        }


# =====================================================
# Command Line Testing
# =====================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ResearchMind AI CLI")
    print("=" * 70)

    while True:

        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        result = answer_question(question)

        print("\n" + "=" * 70)
        print("ANSWER")
        print("=" * 70)
        print(result["answer"])

        print("\n" + "=" * 70)
        print("SOURCES")
        print("=" * 70)

        if result["sources"]:

            for source in result["sources"]:
                print(f"• {source}")

        else:

            print("No sources found.")