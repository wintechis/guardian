import pytest
from guardian.guardian import Guardian 
from requests import HTTPError
import hashlib

def test_fetch_sensor_constraints_yml_success():
    g = Guardian('','')
    
    valid_url = "https://renedorsch.solidweb.org/validation_code/sensor_constraints.yml"
    content = g._download_resource_constraint_executable(valid_url)
    
    # Basic checks to ensure content is fetched
    assert content is not None
    assert len(content) > 0
    assert "MAC" in content  # Assuming the term "MAC" should be in the YAML

def test_fetch_sensor_constraints_yml_failure():
    g = Guardian('','')
    # Modifying the URL to an invalid one to simulate a failure
    invalid_url = "https://renedorsch.solidweb.org/validation_code/nonexistent.yml"
    
    with pytest.raises(HTTPError):
        g._download_resource_constraint_executable(invalid_url)
        
        
def test_select_1_algorithmn_valid_algorithmn():
    g = Guardian('','')
    # Test with a valid algorithm name
    selected_algo = g._select_algorithmn("http://spdx.org/rdf/terms#checksumAlgorithm_sha256")
    assert selected_algo == hashlib.sha256

def test_select_2_algorithmn_valid_algorithmn():
    g = Guardian('','')
    # Test with a valid algorithm name
    selected_algo = g._select_algorithmn("http://spdx.org/rdf/terms#checksumAlgorithm_sha3_512")
    assert selected_algo == hashlib.sha3_512

def test_select_3_algorithmn_valid_algorithmn():
    g = Guardian('','')
    # Test with a valid algorithm name
    selected_algo = g._select_algorithmn("http://spdx.org/rdf/terms#checksumAlgorithm_sha1")
    assert selected_algo == hashlib.sha1

def test_select_4_algorithmn_valid_algorithmn():
    g = Guardian('','')
    # Test with a valid algorithm name
    algorithmn = hashlib.md5
    content = "my test content"
    selected_algo = g._select_algorithmn("http://spdx.org/rdf/terms#checksumAlgorithm_md5")
    assert selected_algo == algorithmn
    correct_checksum = algorithmn(str.encode(content)).hexdigest()
    assert g.validate_integrity(content, algorithmn, correct_checksum) == True

def test_select_algorithmn_invalid_algorithmn():
    g = Guardian('','')
    # Test with an invalid algorithm name
    with pytest.raises(Exception):
        g._select_algorithmn("unsupported_algorithmn")

def test_validate_integrity_valid_checksum():
    g = Guardian('','')
    content = "test content"
    algorithmn = hashlib.sha256
    correct_checksum = algorithmn(str.encode(content)).hexdigest()
    assert g.validate_integrity(content, algorithmn, correct_checksum) == True

def test_validate_integrity_invalid_checksum():
    g = Guardian('','')
    content = "test content"
    algorithmn = hashlib.sha256
    incorrect_checksum = "incorrectchecksum1234567890"
    assert g.validate_integrity(content, algorithmn, incorrect_checksum) == False