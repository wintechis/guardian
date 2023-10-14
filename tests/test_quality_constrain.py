import pytest
from guardian.models import QualityConstraint
from pandera import DataFrameSchema
import pandas as pd
import numpy as np
import guardian.exceptions as ge 
# Note: Replace 'your_module' with the name of the module where the above code resides.

def test_initiate_frictionless_function():
    # Create a dummy frictionless schema file
    file = '{ "fields": [{"name": "col1", "type": "integer"}]}'

    qc = QualityConstraint(
        enforced=True,
        artifact_uri='some_uri',
        format="application/json",
        checksum_algorithmus='some_algorithm',
        checksum="12345",
        conformance="https://specs.frictionlessdata.io/data-package/"
    )

    # Initiate frictionless function
    qc.initiate_function(file)

    # Check if validation_function is set and is of type Callable
    assert callable(qc.validation_function)

    


def test_failing_validation_frictionless_function():
    # Create a dummy frictionless schema file
    file = '{ "fields": [{"name": "col1", "type": "integer"}]}'

    qc = QualityConstraint(
        enforced=True,
        artifact_uri='some_uri',
        format="application/json",
        checksum_algorithmus='some_algorithm',
        checksum="12345",
        conformance="https://specs.frictionlessdata.io/data-package/"
    )

    # Initiate frictionless function
    qc.initiate_function(file)

    df = pd.DataFrame(data = {"col1": ["hi", "ho"]})
    with pytest.raises(ge.ValidationError):
        qc._validate(df)


def test_validation_frictionless_function():
    # Create a dummy frictionless schema file
    file = '{ "fields": [{"name": "col1", "type": "integer"}]}'

    qc = QualityConstraint(
        enforced=True,
        artifact_uri='some_uri',
        format="application/json",
        checksum_algorithmus='some_algorithm',
        checksum="12345",
        conformance="https://specs.frictionlessdata.io/data-package/"
    )

    # Initiate frictionless function
    qc.initiate_function(file)

    df = pd.DataFrame(data = {
        "col1": np.random.randint(low=0, high=10000, size=100)  # Random integers between 0 and 10000
    })
    
    res = qc._validate(df)
    # Check if validation_function is set and is of type Callable
    assert callable(qc.validation_function)
    assert res == True

def test_validate_function_not_implemented():
    qc = QualityConstraint(
        enforced=True,
        artifact_uri='some_uri',
        format="text/plain",
        checksum_algorithmus='some_algorithm',
        checksum="12345",
        conformance='some_conformance'
    )

    # Since the validate function is not implemented, 
    # we can only check if it's callable for now.
    assert callable(qc._validate)

def test_initiate_python_function_not_implemented():
    qc = QualityConstraint(
        enforced=True,
        artifact_uri='some_uri',
        format="text/plain",
        checksum_algorithmus='some_algorithm',
        checksum="12345",
        conformance='some_conformance'
    )

    # Since the _initate_python_function is not implemented, 
    # we can only check if it's callable for now.
    assert callable(qc._initate_python_function)
    

def test_initiate_python_function():
    qc = QualityConstraint(
        enforced=True,
        artifact_uri='some_uri',
        format="text/plain",
        checksum_algorithmus='some_algorithm',
        checksum="12345",
        conformance="http://python.org"
    )

    python_program = """
    def validate(temperature):
      if temperature < -5 or temperature > 30 :
        return False
    return True
    """
    # Since the _initate_python_function is not implemented, 
    # we can only check if it's callable for now.
    qc._initate_python_function(python_program)
    assert callable(qc._validate)
    

def test_initiate_shacl_function():
    qc = QualityConstraint(
        enforced=True,
        artifact_uri='some_uri',
        format="text/turtle",
        checksum_algorithmus='some_algorithm',
        checksum="12345",
        conformance="https://www.w3.org/ns/shacl"
    )


    shapes_file = '''
    @prefix dash: <http://datashapes.org/dash#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix schema: <http://schema.org/> .
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    schema:PersonShape
        a sh:NodeShape ;
        sh:targetClass schema:Person ;
        sh:property [
            sh:path schema:givenName ;
            sh:datatype xsd:string ;
            sh:name "given name" ;
        ] ;
        sh:property [
            sh:path schema:birthDate ;
            sh:lessThan schema:deathDate ;
            sh:maxCount 1 ;
        ] ;
        sh:property [
            sh:path schema:gender ;
            sh:in ( "female" "male" ) ;
        ] ;
        sh:property [
            sh:path schema:address ;
            sh:node schema:AddressShape ;
        ] .

    schema:AddressShape
        a sh:NodeShape ;
        sh:closed true ;
        sh:property [
            sh:path schema:streetAddress ;
            sh:datatype xsd:string ;
        ] ;
        sh:property [
            sh:path schema:postalCode ;
            sh:or ( [ sh:datatype xsd:string ] [ sh:datatype xsd:integer ] ) ;
            sh:minInclusive 10000 ;
            sh:maxInclusive 99999 ;
        ] .
    '''
    # Since the _initate_python_function is not implemented, 
    # we can only check if it's callable for now.
    qc._initiate_shacl_function(shapes_file)
    assert callable(qc._validate)
    
    

def test_shacl_successful_test():
    qc = QualityConstraint(
        enforced=True,
        artifact_uri='some_uri',
        format="text/turtle",
        checksum_algorithmus='some_algorithm',
        checksum="12345",
        conformance="https://www.w3.org/ns/shacl"
    )


    shapes_file = '''
    @prefix dash: <http://datashapes.org/dash#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix schema: <http://schema.org/> .
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    schema:PersonShape
        a sh:NodeShape ;
        sh:targetClass schema:Person ;
        sh:property [
            sh:path schema:givenName ;
            sh:datatype xsd:string ;
            sh:name "given name" ;
        ] ;
        sh:property [
            sh:path schema:birthDate ;
            sh:lessThan schema:deathDate ;
            sh:maxCount 1 ;
        ] ;
        sh:property [
            sh:path schema:gender ;
            sh:in ( "female" "male" ) ;
        ] ;
        sh:property [
            sh:path schema:address ;
            sh:node schema:AddressShape ;
        ] .

    schema:AddressShape
        a sh:NodeShape ;
        sh:closed true ;
        sh:property [
            sh:path schema:streetAddress ;
            sh:datatype xsd:string ;
        ] ;
        sh:property [
            sh:path schema:postalCode ;
            sh:or ( [ sh:datatype xsd:string ] [ sh:datatype xsd:integer ] ) ;
            sh:minInclusive 10000 ;
            sh:maxInclusive 99999 ;
        ] .
    '''
    # Since the _initate_python_function is not implemented, 
    # we can only check if it's callable for now.
    qc._initiate_shacl_function(shapes_file)
    
    
    data_file = '''
    @prefix schema: <http://schema.org/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.org/ns#Bob>
    a schema:Person ;
    schema:address <http://example.org/ns#BobsAddress> ;
    schema:birthDate "1967-07-07"^^xsd:string ;
    schema:deathDate "1968-09-10"^^xsd:string ;
    schema:familyName "Junior"^^xsd:string ;
    schema:gender "male";
    schema:givenName "Robert"^^xsd:string .

    <http://example.org/ns#BobsAddress>
    schema:postalCode 94204 ;
    schema:streetAddress "1600 Amphitheatre Pkway"^^xsd:string .
    '''
    assert qc._validate(data_file)
    
def test_shacl_failing_test():
    qc = QualityConstraint(
        enforced=True,
        artifact_uri='some_uri',
        format="text/turtle",
        checksum_algorithmus='some_algorithm',
        checksum="12345",
        conformance="https://www.w3.org/ns/shacl"
    )


    shapes_file = '''
    @prefix dash: <http://datashapes.org/dash#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix schema: <http://schema.org/> .
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    schema:PersonShape
        a sh:NodeShape ;
        sh:targetClass schema:Person ;
        sh:property [
            sh:path schema:givenName ;
            sh:datatype xsd:string ;
            sh:name "given name" ;
        ] ;
        sh:property [
            sh:path schema:birthDate ;
            sh:lessThan schema:deathDate ;
            sh:maxCount 1 ;
        ] ;
        sh:property [
            sh:path schema:gender ;
            sh:in ( "female" "male" ) ;
        ] ;
        sh:property [
            sh:path schema:address ;
            sh:node schema:AddressShape ;
        ] .
    '''
    # Since the _initate_python_function is not implemented, 
    # we can only check if it's callable for now.
    qc._initiate_shacl_function(shapes_file)
    
    
    data_file = '''
    @prefix schema: <http://schema.org/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    <http://example.org/ns#Bob>
    a schema:Person ;
    schema:birthDate "1969-07-07"^^xsd:string ;
    schema:deathDate "1968-09-10"^^xsd:string ;
    schema:familyName "Junior"^^xsd:string ;
    schema:gender "male";
    schema:givenName "Robert"^^xsd:string .
    '''
    with pytest.raises(ge.ValidationError):
        qc._validate(data_file)