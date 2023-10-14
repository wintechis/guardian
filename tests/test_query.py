import pytest
from typing import List
from guardian.query import query_quality_contract_information

# Assuming the function and required imports are defined here...

def test_query_quality_contract_information_valid_component():
    # Call the function with valid parameters
    contracts = query_quality_contract_information("http://localhost:7200/repositories/GuardianExample",
                                       "myComponent",
                                       None)
    
    assert contracts != []
    assert contracts is not None

