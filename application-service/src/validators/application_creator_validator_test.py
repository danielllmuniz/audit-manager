from .application_creator_validator import application_creator_validator

class MockRequest:
    def __init__(self, body) -> None:
        self.body = body

def test_application_creator_validator_valid_input():
    request = MockRequest({
        "name": "JohnDoe",
        "owner_team": "DevTeam",
        "repo_url": "https://github.com/JohnDoe/Repo"
    })

    application_creator_validator(request)
