# SerenLexAI

SerenLexAI is a modular, AI-powered contract risk intelligence platform designed to provide structured, explainable legal analysis for non-lawyers. Built with a multi-stage LLM pipeline architecture, it decomposes contract evaluation into clause extraction, semantic classification, calibrated risk scoring, recommendation synthesis, and executive summarization. The system leverages vector embeddings (pgvector) for clause-level semantic indexing, asynchronous task orchestration via Celery, and graph-based workflow control using LangGraph to ensure deterministic, inspectable reasoning flows rather than monolithic prompt execution.

The backend is implemented with FastAPI, SQLAlchemy, and Postgres, emphasizing type-safe structured outputs through Pydantic schemas to prevent malformed AI responses. Each clause is processed independently in parallel, enabling scalable analysis of contracts up to 20 pages while maintaining token discipline and contextual integrity. The frontend, built in React with TypeScript, presents a risk-calibrated dashboard optimized for rapid executive scanning and drill-down inspection. SerenLexAI is engineered not as a chatbot wrapper, but as a composable legal inference engine with configurable risk sensitivity, jurisdiction-aware prompting, and auditable AI decision boundaries.


