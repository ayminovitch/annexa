class DomainError(Exception):
    def __init__(self, code: str, title: str, detail: str, status: int = 400) -> None:
        super().__init__(detail)
        self.code = code
        self.title = title
        self.status = status
        self.detail = detail


class ResourceNotFoundError(DomainError):
    def __init__(self, resource_type: str, resource_id: str) -> None:
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            title=f"{resource_type} not found",
            detail=f"The {resource_type.lower()} with id {resource_id} does not exist",
            status=404,
        )
