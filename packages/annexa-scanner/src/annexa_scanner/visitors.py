import ast


class AISDKVisitor(ast.NodeVisitor):

    TARGET_SDKS = {
        "openai",
        "anthropic",
        "google",
        "langchain",
        "langgraph",
        "llama_index",
        "transformers",
        "torch",
        "scikit_learn"
    }

    def __init__(self) -> None:
        self.found_sdks: set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            base_module = alias.name.split(".")[0]
            if base_module in self.TARGET_SDKS:
                self.found_sdks.add(base_module)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            base_module = node.module.split(".")[0]
            if base_module in self.TARGET_SDKS:
                self.found_sdks.add(base_module)

        self.generic_visit(node)
