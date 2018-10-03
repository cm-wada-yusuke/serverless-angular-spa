class UserResponse:
    def __init__(self, user_uuid, organization_id, email, company, display_user_name, created_at, updated_at):
        self.user_uuid = user_uuid
        self.organization_id = organization_id
        self.email = email
        self.company = company
        self.display_user_name = display_user_name
        self.created_at = created_at
        self.updated_at = updated_at


class GetUsers:

    def __init__(self, search_key, second_key=None, last_evaluated_key=None):
        self.search_key = search_key
        self.second_key = second_key
        self.last_evaluated_key = last_evaluated_key

    def get_by_organization_id(self):
        import infrastructures.user.user_repository as user_repository
        return user_repository.get_users_by_organization_id(self)
