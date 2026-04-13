"""Environment configurations and test data."""

from dataclasses import dataclass


@dataclass
class UserCredentials:
    """User credentials dataclass."""

    username: str
    password: str


@dataclass
class EnvironmentConfig:
    """Environment configuration dataclass."""

    base_url: str
    users: dict[str, UserCredentials]


ENVIRONMENTS: dict[str, EnvironmentConfig] = {
    "staging": EnvironmentConfig(
        base_url="https://www.saucedemo.com",
        users={
            "standard_user": UserCredentials("standard_user", "secret_sauce"),
            "locked_out_user": UserCredentials("locked_out_user", "secret_sauce"),
            "problem_user": UserCredentials("problem_user", "secret_sauce"),
            "performance_glitch_user": UserCredentials("performance_glitch_user", "secret_sauce"),
        },
    ),
    "production": EnvironmentConfig(
        base_url="https://www.saucedemo.com",
        users={
            "standard_user": UserCredentials("standard_user", "secret_sauce"),
            "locked_out_user": UserCredentials("locked_out_user", "secret_sauce"),
            "problem_user": UserCredentials("problem_user", "secret_sauce"),
            "performance_glitch_user": UserCredentials("performance_glitch_user", "secret_sauce"),
        },
    ),
}

# Product test data
PRODUCTS = {
    "Sauce Labs Backpack": {
        "id": "sauce-labs-backpack",
        "price": 29.99,
        "description": "carry.allTheThings() with the sleek, streamlined Sauce Labs backpack.",
    },
    "Sauce Labs Bike Light": {
        "id": "sauce-labs-bike-light",
        "price": 9.99,
        "description": "A red light isn't the desired state in testing.",
    },
    "Sauce Labs Bolt T-Shirt": {
        "id": "sauce-labs-bolt-t-shirt",
        "price": 15.99,
        "description": "Get your testing superhero on with the Sauce Labs bolt T-shirt.",
    },
    "Sauce Labs Fleece Jacket": {
        "id": "sauce-labs-fleece-jacket",
        "price": 49.99,
        "description": "It's not a hoodie, but it's close.",
    },
    "Sauce Labs Onesie": {
        "id": "sauce-labs-onesie",
        "price": 7.99,
        "description": "Onsies are one piece of furniture. They are not to be used.",
    },
    "Test.allTheThings() T-Shirt (Red)": {
        "id": "test-allthetings-t-shirt-red",
        "price": 15.99,
        "description": "This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard.",
    },
}


def get_credentials(env: str, user_type: str) -> UserCredentials:
    """Get user credentials for a given environment and user type.

    Args:
        env: Environment name (staging, production)
        user_type: User type (standard_user, locked_out_user, etc.)

    Returns:
        UserCredentials dataclass with username and password
    """
    if env not in ENVIRONMENTS:
        raise ValueError(f"Environment '{env}' not found in ENVIRONMENTS")
    if user_type not in ENVIRONMENTS[env].users:
        raise ValueError(f"User type '{user_type}' not found for environment '{env}'")
    return ENVIRONMENTS[env].users[user_type]
