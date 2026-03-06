from contract_ai.infrastructure.vision.clause_reconstructor import ClauseReconstructor

reconstructor = ClauseReconstructor()


def reconstruct_clauses_node(state):
    pages = state["page_images"]
    print(f"[DEBUG reconstruct] page_images count: {len(pages)}")

    clauses = reconstructor.extract_clauses(pages)
    print(f"[DEBUG reconstruct] clauses extracted: {len(clauses)}")

    # Build raw_text from vision-extracted clauses — single source of truth.
    # This is what document_classifier_node will use to classify the document.
    raw_text = "\n\n".join(
        c.get("text", "") for c in clauses if c.get("text")
    )
    print(f"[DEBUG reconstruct] raw_text length: {len(raw_text)}")

    return {
        "clauses_detected": clauses,
        "raw_text":         raw_text,
    }