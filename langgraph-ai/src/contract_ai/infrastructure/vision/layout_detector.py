import re


class LayoutDetector:

    CLAUSE_PATTERNS = [
        re.compile(r"^\d+\."),            # 1.
        re.compile(r"^\d+\.\d+"),         # 1.1
        re.compile(r"^\d+\.\d+\.\d+"),    # 1.1.1
        re.compile(r"^\([a-z]\)"),        # (a)
        re.compile(r"^\([ivx]+\)"),       # (i)
        re.compile(r"^section\s+\d+", re.I),
        re.compile(r"^article\s+[ivx]+", re.I),
    ]

    def detect_clauses(self, text: str):

        lines = text.split("\n")

        clauses = []
        buffer = []

        position_index = 0

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if self._is_clause_start(line):

                if buffer:
                    clauses.append(
                        {
                            "text": " ".join(buffer),
                            "position_index": position_index,
                        }
                    )
                    position_index += 1
                    buffer = []

            buffer.append(line)

        if buffer:
            clauses.append(
                {
                    "text": " ".join(buffer),
                    "position_index": position_index,
                }
            )

        return clauses

    def _is_clause_start(self, line: str):

        for pattern in self.CLAUSE_PATTERNS:
            if pattern.match(line):
                return True

        return False