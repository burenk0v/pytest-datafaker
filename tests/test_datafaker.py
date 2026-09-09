"""Tests for DataFaker class and pytest integration."""

import pytest
from mimesis.enums import Locale

from pytest_datafaker.config import DataFakerConfig
from pytest_datafaker.datafaker import DataFaker


@pytest.fixture(autouse=True)
def reset_datafaker_singleton() -> None:
    """Reset DataFaker singleton between tests."""
    DataFaker._instance = None
    yield
    DataFaker._instance = None


class TestDataFakerBasics:
    """Basic tests for DataFaker class."""

    @staticmethod
    def _generated_values_sequence(faker: DataFaker) -> list[str]:
        """Generate a stable multi-provider sequence for behavioral seed checks."""
        return [
            faker.api.person.full_name(),
            faker.api.person.email(),
            faker.api.person.telephone(),
            faker.api.address.address(),
            faker.api.address.city(),
            faker.api.address.country(),
            faker.api.internet.url(),
            faker.api.internet.user_agent(),
            faker.api.internet.ip_v4(),
        ]

    def test_datafaker_initialization_with_default_config(self):
        """Test DataFaker initialization with default English locale."""
        config = DataFakerConfig(seed=42)
        faker = DataFaker(config)

        assert faker.seed == 42
        assert faker.api is not None
        assert faker.api.locale == Locale.EN

    def test_datafaker_with_multiple_locales(self):
        """Test DataFaker initialization with multiple locales."""
        locales = {Locale.EN, Locale.RU, Locale.DE}
        config = DataFakerConfig(seed=123, locales=locales)
        faker = DataFaker(config)

        assert faker.seed == 123
        assert len(faker.locale) == 3
        assert Locale.EN in faker.locale
        assert Locale.RU in faker.locale
        assert Locale.DE in faker.locale

    def test_datafaker_with_single_locale(self):
        """Test DataFaker initialization with single non-default locale."""
        locales = {Locale.FR}
        config = DataFakerConfig(seed=456, locales=locales)
        faker = DataFaker(config)

        assert faker.seed == 456
        assert len(faker.locale) == 1
        assert Locale.FR in faker.locale

    def test_datafaker_api_generates_data(self):
        """Test that api field generates correct fake data."""
        config = DataFakerConfig(seed=789)
        faker = DataFaker(config)

        # Generate some data using the api field
        name = faker.api.person.full_name()
        email = faker.api.person.email()

        assert isinstance(name, str)
        assert len(name) > 0
        assert isinstance(email, str)
        assert "@" in email

    def test_datafaker_locale_dict_generates_data(self):
        """Test that locale dictionary accesses generate correct data."""
        locales = {Locale.EN, Locale.RU}
        config = DataFakerConfig(seed=999, locales=locales)
        faker = DataFaker(config)

        # Generate data from English locale
        en_name = faker.locale[Locale.EN].person.full_name()
        # Generate data from Russian locale
        ru_name = faker.locale[Locale.RU].person.full_name()

        assert isinstance(en_name, str)
        assert len(en_name) > 0
        assert isinstance(ru_name, str)
        assert len(ru_name) > 0

    def test_datafaker_add_locale(self):
        """Test adding new locale after initialization."""
        config = DataFakerConfig(seed=111, locales={Locale.EN})
        faker = DataFaker(config)

        assert Locale.DE not in faker.locale

        faker.add_locale(Locale.DE)

        assert Locale.DE in faker.locale
        # Generate data to verify locale works
        de_name = faker.locale[Locale.DE].person.full_name()
        assert isinstance(de_name, str)
        assert len(de_name) > 0

    def test_datafaker_singleton_pattern(self):
        """Test that DataFaker uses Singleton pattern correctly."""
        config1 = DataFakerConfig(seed=222)
        faker1 = DataFaker(config1)

        config2 = DataFakerConfig(seed=333)
        faker2 = DataFaker(config2)

        # Both should be the same instance
        assert faker1 is faker2
        # Seed should be from the first initialization
        assert faker2.seed == 222

    def test_datafaker_reproducible_results_with_seed(self):
        """Test that same seed produces the same behavioral data sequence."""
        DataFaker._instance = None
        faker1 = DataFaker(DataFakerConfig(seed=12345, locales={Locale.EN}))
        values1 = self._generated_values_sequence(faker1)

        DataFaker._instance = None
        faker2 = DataFaker(DataFakerConfig(seed=12345, locales={Locale.EN}))
        values2 = self._generated_values_sequence(faker2)

        assert values1 == values2

    def test_datafaker_different_seeds_produce_different_sequences(self):
        """Test that different seeds produce different multi-value sequences."""
        DataFaker._instance = None
        faker1 = DataFaker(DataFakerConfig(seed=123, locales={Locale.EN}))
        values1 = self._generated_values_sequence(faker1)

        DataFaker._instance = None
        faker2 = DataFaker(DataFakerConfig(seed=456, locales={Locale.EN}))
        values2 = self._generated_values_sequence(faker2)

        assert values1 != values2


class TestDataFakerFixture:
    """Tests for pytest fixture integration."""

    def test_data_faker_fixture_available(self, data_faker):
        """Test that data_faker fixture is available in pytest."""
        assert data_faker is not None
        assert hasattr(data_faker, "api")
        assert hasattr(data_faker, "locale")

    def test_data_faker_fixture_generates_person_data(self, data_faker):
        """Test that fixture can generate person data."""
        name = data_faker.api.person.full_name()
        email = data_faker.api.person.email()
        phone = data_faker.api.person.telephone()

        assert isinstance(name, str)
        assert len(name) > 0
        assert isinstance(email, str)
        assert "@" in email
        assert isinstance(phone, str)
        assert len(phone) > 0

    def test_data_faker_fixture_generates_address_data(self, data_faker):
        """Test that fixture can generate address data."""
        address = data_faker.api.address.address()
        city = data_faker.api.address.city()
        country = data_faker.api.address.country()

        assert isinstance(address, str)
        assert len(address) > 0
        assert isinstance(city, str)
        assert len(city) > 0
        assert isinstance(country, str)
        assert len(country) > 0

    def test_data_faker_fixture_generates_internet_data(self, data_faker):
        """Test that fixture can generate internet data."""
        url = data_faker.api.internet.url()
        user_agent = data_faker.api.internet.user_agent()
        ip_address = data_faker.api.internet.ip_v4()

        assert isinstance(url, str)
        assert "://" in url
        assert isinstance(user_agent, str)
        assert len(user_agent) > 0
        assert isinstance(ip_address, str)
        assert len(ip_address) > 0


def test_datafaker_seed_option_in_config(pytestconfig):
    """Test that --datafaker-seed command line option is available."""
    assert pytestconfig.getoption("--datafaker-seed", default=None, skip=False) is None
    assert pytestconfig.getoption("datafaker-seed", default=None, skip=False) is None
