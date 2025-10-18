from .person_creator_validator import person_creator_validator

class MockRequest:
    def __init__(self, body) -> None:
        self.body = body

def test_person_creator_validator_valid_input():
    request = MockRequest({
        "name": "JohnDoe",
        "owner_team": "DevTeam",
        "repo_url": "https://github.com/JohnDoe/Repo"
    })

    person_creator_validator(request)
