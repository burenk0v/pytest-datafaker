"""Tests for DataFaker class and pytest integration."""

from mimesis.enums import Locale

from pytest_datafaker.config import DataFakerConfig, get_config
from pytest_datafaker.datafaker import DataFaker


class TestDataFakerBasics:
    """Basic tests for DataFaker class."""

    def test_datafaker_initialization_with_default_config(self):
        """Test DataFaker initialization with default English locale."""
        config = DataFakerConfig(seed=42)
        faker = DataFaker(config)

        assert faker.seed == 42
        assert faker.random is not None
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

    def test_datafaker_creates_independent_instances(self):
        """Test that each DataFaker call creates an independent instance."""
        config1 = DataFakerConfig(seed=222)
        faker1 = DataFaker(config1)

        config2 = DataFakerConfig(seed=333)
        faker2 = DataFaker(config2)

        assert faker1 is not faker2
        assert faker1.seed == 222
        assert faker2.seed == 333

    def test_datafaker_reproducible_results_with_seed(self):
        """Test that same seed produces same results."""
        config1 = DataFakerConfig(seed=12345, locales={Locale.EN})
        faker1 = DataFaker(config1)
        results1 = (
            faker1.api.person.full_name(),
            faker1.locale[Locale.EN].person.full_name(),
            faker1.random.randint(1, 1000),
            faker1.random.choice(["alpha", "beta", "gamma"]),
            faker1.docker_string(),
        )

        config2 = DataFakerConfig(seed=12345, locales={Locale.EN})
        faker2 = DataFaker(config2)
        results2 = (
            faker2.api.person.full_name(),
            faker2.locale[Locale.EN].person.full_name(),
            faker2.random.randint(1, 1000),
            faker2.random.choice(["alpha", "beta", "gamma"]),
            faker2.docker_string(),
        )

        assert results1 == results2

    def test_datafaker_token_urlsafe_remains_secure(self):
        """Test that token generation still returns a usable secure token."""
        faker = DataFaker(DataFakerConfig(seed=12345))

        token = faker.token_urlsafe()
        assert isinstance(token, str)
        assert token
        assert token


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


class TestGetConfigSeedSemantics:
    """Tests for seed normalization in get_config."""

    def test_get_config_uses_generated_seed_when_seed_is_none(self, monkeypatch):
        """Test that None seed falls back to generated timestamp-based seed."""
        monkeypatch.setattr("pytest_datafaker.config.time_ns", lambda: 100)

        config = get_config()

        assert config.seed == 100
        assert config.locales is None

    @pytest.mark.parametrize("seed", [0, 1, 42])
    def test_get_config_keeps_valid_integer_seed(self, seed):
        """Test that zero and positive integers remain deterministic seeds."""
        config = get_config(seed)

        assert config.seed == seed
        assert config.locales is None

    def test_get_config_converts_valid_string_seed_to_int(self):
        """Test that numeric string seeds are converted to integers."""
        config = get_config("123")

        assert config.seed == 123
        assert config.locales is None

    @pytest.mark.parametrize(
        ("seed"),
        [
            pytest.param(-1, id="negative-int"),
            pytest.param("-1", id="negative-str"),
            pytest.param("invalid", id="invalid-str"),
        ],
    )
    def test_get_config_falls_back_for_invalid_seed(self, seed, monkeypatch):
        """Test that negative and invalid seeds use the generated fallback seed."""
        monkeypatch.setattr("pytest_datafaker.config.time_ns", lambda: 777)

        config = get_config(seed)

        assert config.seed == 777
        assert config.locales is None

    def test_get_config_preserves_toml_locales_with_string_seed(self, tmp_path, monkeypatch):
        """Test that TOML locales are preserved when normalizing string seeds."""
        (tmp_path / "pyproject.toml").write_text(
            "[tool.pytest_datafaker]\nlocales = ['en', 'ru']\n",
        )
        monkeypatch.chdir(tmp_path)

        config = get_config("123")

        assert config.seed == 123
        assert config.locales == ["en", "ru"]

    def test_get_config_preserves_toml_locales_with_zero_seed(self, tmp_path, monkeypatch):
        """Test that TOML locales are preserved when using zero as a valid seed."""
        (tmp_path / "pyproject.toml").write_text(
            "[tool.pytest_datafaker]\nlocales = ['en', 'ru']\n",
        )
        monkeypatch.chdir(tmp_path)

        config = get_config(0)

        assert config.seed == 0
        assert config.locales == ["en", "ru"]
