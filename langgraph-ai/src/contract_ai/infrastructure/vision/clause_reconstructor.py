from contract_ai.infrastructure.vision.llm_vision_parser import LLMVisionParser


class ClauseReconstructor:

    def __init__(self):
        self.parser = LLMVisionParser()

    def extract_clauses(self, page_images):

        clauses = []

        position = 0
        page_number = 1

        for image_path in page_images:

            structure = self.parser.parse_page(image_path)

            for clause in structure.clauses:

                clauses.append(
                    {
                        "text": clause.text,
                        "position_index": position,
                        "page_number": page_number,
                        "number": clause.number,
                        "title": clause.title,
                    }
                )

                position += 1

            page_number += 1

        return clauses