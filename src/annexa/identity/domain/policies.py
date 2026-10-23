from annexa.identity.domain.entities import Role, User


class RolePolicy:
    @staticmethod
    def can_approve_assessment(user: User) -> bool:
        return user.role in (Role.OWNER, Role.COMPLIANCE_OFFICER)

    @staticmethod
    def can_manage_api_keys(user: User) -> bool:
        return user.role in (Role.OWNER, Role.ADMIN)
