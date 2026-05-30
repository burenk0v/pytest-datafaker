# pytest-datafaker

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A pytest plugin for simple generation of test data using the [Mimesis](https://github.com/lk-geimfari/mimesis) library. Provides a convenient `data_faker` fixture for creating realistic fake data in your tests.

## 🚀 Features

- 🌍 **Multilingual Support** - 30+ languages and locales
- 🔐 **Controlled Generation** - ability to set seed for reproducible results
- 🧵 **Thread Safety** - uses Singleton pattern with multithreading support
- ⚙️ **Flexible Configuration** - via `pyproject.toml` or command line parameters
- 📦 **Minimal Dependencies** - only pytest and mimesis

## 📦 Installation

```bash
pip install pytest-datafaker
```

Or with Poetry:

```bash
poetry add pytest-datafaker
```

## 🎯 Quick Start

### Basic Example

```python
import pytest

def test_user_creation(data_faker):
    """Test with fake data using default EN locale."""
    name = data_faker.api.person.full_name()
    email = data_faker.api.person.email()
    phone = data_faker.api.person.telephone()
    
    assert name
    assert email
    assert "@" in email
    assert phone
```

### Using Different Locales

```python
from mimesis.enums import Locale

def test_with_russian_data(data_faker):
    """Generate data in Russian using locale dictionary."""
    if Locale.RU in data_faker.locale:
        name_ru = data_faker.locale[Locale.RU].person.full_name()
        address_ru = data_faker.locale[Locale.RU].address.address()
        
        assert name_ru
        assert address_ru
```

### Accessing Default API

The `api` field provides direct access to the English (default) locale:

```python
def test_default_locale(data_faker):
    """Access methods through the default api field."""
    # Both are equivalent for EN locale
    data_faker.api.person.full_name()
```

## ⚙️ Configuration

### Via pyproject.toml

Add a `[tool.pytest_datafaker]` section to your `pyproject.toml` file:

```toml
[tool.pytest_datafaker]
seed = 42
locales = ["en", "ru", "de", "fr"]
```

### Via Command Line

```bash
pytest --datafaker-seed 123 tests/
```

## 📚 Available Methods

The `data_faker` fixture provides access to Mimesis methods through two fields:

- **`data_faker.api`** - Generic instance for the default English locale
- **`data_faker.locale`** - Dictionary of Generic instances for configured locales

### Examples

```python
def test_person_data(data_faker):
    """Methods for generating person data."""
    data_faker.api.person.full_name()
    data_faker.api.person.first_name()
    data_faker.api.person.last_name()
    data_faker.api.person.email()
    data_faker.api.person.telephone()
    data_faker.api.person.gender()

def test_address_data(data_faker):
    """Methods for generating address data."""
    data_faker.api.address.address()
    data_faker.api.address.street_name()
    data_faker.api.address.city()
    data_faker.api.address.country()
    data_faker.api.address.postal_code()

def test_internet_data(data_faker):
    """Methods for generating internet data."""
    data_faker.api.internet.url()
    data_faker.api.internet.ip_v4()
    data_faker.api.internet.username()
    data_faker.api.internet.password()

def test_datetime_data(data_faker):
    """Methods for generating dates and times."""
    data_faker.api.datetime.datetime()
    data_faker.api.datetime.date()
    data_faker.api.datetime.time()
    data_faker.api.datetime.year()
```

For a complete list of available methods, see the [Mimesis documentation](https://mimesis.name/).

## 🔧 Features

### Thread Safety

DataFaker uses the Singleton pattern with locking to ensure thread safety:

```python
from pytest_datafaker import DataFaker
from pytest_datafaker.config import DataFakerConfig

config = DataFakerConfig(seed=42)
faker1 = DataFaker(config)
faker2 = DataFaker(config)

assert faker1 is faker2  # Same instance
```

### Class Structure

The `DataFaker` class has the following structure:

- **`api`** - Generic instance for the default English locale. Use this for basic/default locale access
- **`locale`** - Dictionary mapping Locale to Generic instances for all configured locales. Use this when you need data in specific languages

```python
def test_class_structure(data_faker):
    """Understanding DataFaker class structure."""
    # Default EN locale
    data_faker.api.person.full_name()
    
    # Access other configured locales through the locale dictionary
    from mimesis.enums import Locale
    if Locale.RU in data_faker.locale:
        data_faker.locale[Locale.RU].address.address()
```

### Adding Custom Locales

```python
from mimesis.enums import Locale

def test_with_custom_locale(data_faker):
    """Add additional locale during test."""
    data_faker.add_locale(Locale.DE)  # Add German language
    
    name_de = data_faker.locale[Locale.DE].person.full_name()
    assert name_de
```

## 📋 Requirements

- Python 3.12+
- pytest >= 9.0.3
- mimesis >= 19.1.0

## 🧪 Running tests

Short instructions for running tests locally using Poetry:

```bash
# install Poetry (if not already installed)
pip install --user poetry

# install project dependencies and create virtual environment
poetry install

# run all tests inside the Poetry environment
poetry run pytest -q

# run a specific test file
poetry run pytest tests/test_datafaker.py -q
```

## 📄 License

This project is licensed under the [MIT](LICENSE) License.

## 👨‍💻 Author

**Oleg Burenkov** - [burenkov.oleg@gmail.com](mailto:burenkov.oleg@gmail.com)

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

If you have any questions or issues, please create an [issue](../../issues) in the repository.
