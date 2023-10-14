import pytest
import yaml
from guardian.config import get_config, BaseConfig  # Assuming your provided code is in 'your_module.py'
import os

current_folder = os.path.dirname(os.path.abspath(__file__))

test_config = f"{current_folder}/test_config.yml"

def test_get_config():
    # Load the config using the function
    config = get_config()
    print(config)
    # Ensure it returns a BaseConfig instance
    assert isinstance(config, BaseConfig)

    # Load the YAML data directly for comparison
    with open(test_config, 'r') as file:
        yaml_data = yaml.safe_load(file)
    
    # Compare data from the parsed config and the YAML file
    assert config.knowledge_graph == yaml_data["knowledge_graph"]
    assert config.my_name == yaml_data["created_by"]
    assert config.my_uri == yaml_data["created_uri"]
    assert config.my_description == yaml_data["description"]
    
    # Compare conformance standards
    for spec, yaml_spec in zip(config.my_specification, yaml_data["conformance_standards"]):
        assert spec.conformance == yaml_spec["conformance"]
        assert spec.formats == yaml_spec["formats"]

