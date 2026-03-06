import re


class ClauseCleaner:

    MIN_CLAUSE_LENGTH = 40

    def clean(self, clauses):

        cleaned = []

        for clause in clauses:

            text = clause.get("text", "").strip()

            if not text:
                continue

            # remove repeated whitespace
            text = re.sub(r"\s+", " ", text)

            # remove page headers / footers
            if self._is_header_or_footer(text):
                continue

            # ignore very short fragments
            if len(text) < self.MIN_CLAUSE_LENGTH:
                continue

            clause["text"] = text

            cleaned.append(clause)

        return cleaned

    def _is_header_or_footer(self, text):

        text_lower = text.lower()

        if "page" in text_lower and "of" in text_lower:
            return True

        if "confidential" in text_lower:
            return True

        return False