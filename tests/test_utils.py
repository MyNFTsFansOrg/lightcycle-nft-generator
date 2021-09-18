import os
import sys

# third-party
import pytest
import yaml

# src
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(TEST_DIR, ".."))
import src.utils as su


def test_validation_fail():
    config = yaml.safe_load(
        """example:
  settings:
    address: REPLACEME
"""
    )
    with pytest.raises(su.ValidationException):
        su.validate_config(config=config, project_name="example")

    with pytest.raises(su.ValidationException):
        su.validate_config(config=config, project_name="missing")


def test_validation_pass():
    config = yaml.safe_load(
        """example:
  settings:
    address: OK
"""
    )
    assert su.validate_config(config=config, project_name="example")


def test_generate_random_attributes_without_trait_restrictions():
    traits = {
        "trait_types": ["top", "bottom"],
        "trait_values": {
            "top": {"black": 1, "red": 2},
            "bottom": {"blue": 1, "green": 2},
        },
    }
    metadata_attributes = su.generate_random_attributes(traits=traits)
    assert metadata_attributes
    for trait in metadata_attributes:
        ttype = trait["trait_type"]
        assert ttype in traits["trait_values"].keys()


def test_generate_random_attributes_with_trait_restrictions():
    traits = {
        "trait_types": ["class", "body", "head", "hat"],
        "trait_restrictions": ["class"],
        "trait_values": {
            "class": {"archer": 2, "warrior": 1},
            "body": {"archer": {"orange": 1, "white": 1}, "warrior": {"white": 1}},
            "head": {"archer": {"normal": 1, "angry": 1}, "warrior": {"angry": 1}},
            "hat": {
                "archer": {"long": 1, "short": 1},
                "warrior": {"long": 1, "short": 1},
            },
        },
    }
    metadata_attributes = su.generate_random_attributes(traits=traits)
    assert metadata_attributes
    for trait in metadata_attributes:
        ttype = trait["trait_type"]
        assert ttype in traits["trait_values"].keys()


def test_simplify():
    nft_attributes = [
        {"trait_type": "class", "trait_value": "archer"},
        {"trait_type": "body", "trait_value": "orange"},
        {"trait_type": "head", "trait_value": "angry"},
        {"trait_type": "hat", "trait_value": "short"},
    ]
    flattened = su.flatten_nft_attributes(nft_attributes=nft_attributes)
    assert flattened["class"] == "archer"
    assert flattened["body"] == "orange"
    assert flattened["head"] == "angry"
    assert flattened["hat"] == "short"


def test_parse_cache():
    cache_payload = {
        "program": {
            "uuid": "LightR",
            "config": "LightRxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        },
        "items": {
            "0": {
                "link": "https://arweave.net/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "name": "hero #0",
                "onChain": True,
            },
            "1": {
                "link": "https://arweave.net/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "name": "hero #1",
                "onChain": True,
            },
            "2": {
                "link": "https://arweave.net/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "name": "hero #2",
                "onChain": True,
            },
        },
    }
    program_config = su.program_config_from_cache(cache_payload)
    assert program_config == "LightRxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


def test_parse_start_date_to_timestamp():
    assert su.start_date_to_timestamp("01 Jan 2021 00:00:00 GMT") == 1609459200
    assert su.start_date_to_timestamp("15 Mar 2021 12:34:56 GMT") == 1615811696
    assert su.start_date_to_timestamp("31 Dec 2021 00:00:00 GMT") == 1640908800