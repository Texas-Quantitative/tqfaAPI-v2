# Architecture (tqfaAPI)

- FastAPI app in app/ with modular routes.
- Scenario routes call GNN serving adapter in app/gnn/serve.py.
- DSL compiles to parameterized Cypher in app/dsl/compiler.py.
