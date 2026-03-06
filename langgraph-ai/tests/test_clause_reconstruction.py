from contract_ai.infrastructure.vision.clause_reconstructor import ClauseReconstructor

reconstructor = ClauseReconstructor()

clauses = reconstructor.extract_clauses(["sample_page.png"])

for c in clauses:
    print(c)