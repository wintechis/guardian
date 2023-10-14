import pytest
from guardian.guardian import Guardian
import pandas as pd


def test_valid_information():
    knowledge_graph: str = 'http://localhost:7200/repositories/testenvironment'
    component: str = 'myComponent'
    g = Guardian(knowledge_graph_url=knowledge_graph, pipeline_component=component)
    assert isinstance(g, Guardian)
    print(g)
    print(g.contracts)
    
    
def test_valid_query_result():
    knowledge_graph: str = 'http://localhost:7200/repositories/testenvironment'
    component: str = 'myComponent'
    g = Guardian(knowledge_graph_url=knowledge_graph, pipeline_component=component)
    assert isinstance(g, Guardian)
    
    df = pd.DataFrame(
        data={
            "MAC": ["02:ab:1d:2f:12:12"],
            "value": [123],
            "type": ["Temperature"]
        }
    )
    print(len(df))
    reports = g.validate(df)
    
    for report in reports:
        assert report.error_report is None
    #print(g.contracts)

def test_invalid_query_result_1():
    knowledge_graph: str = 'http://localhost:7200/repositories/GuardianExample'
    component: str = 'myComponent'
    g = Guardian(knowledge_graph_url=knowledge_graph, pipeline_component=component)
    assert isinstance(g, Guardian)
    
    df = pd.DataFrame(
        data={
            "MAC": ["02:ab:1d:2f:12:12"] * 31,
            "value": [123] * 31,
            "type": ["Temperature"] * 31
        }
    )
    print(len(df))
    reports = g.validate(df)
    
    result = all([_.value for _ in reports])
    assert not result 
        
        
def test_invalid_query_result_2():
    knowledge_graph: str = 'http://localhost:7200/repositories/GuardianExample'
    component: str = 'myComponent'
    g = Guardian(knowledge_graph_url=knowledge_graph, pipeline_component=component)
    assert isinstance(g, Guardian)
    
    df = pd.DataFrame(
        data={
            "MAC": ["02:ab:1d:2f:12:12"],
            "value": [123],
            "type": ["Nothing"]
        }
    )
    print(len(df))
    reports = g.validate(df)
    
    result = all([_.value for _ in reports])
    assert not result 
        
        
def test_invalid_query_result_3():
    knowledge_graph: str = 'http://localhost:7200/repositories/GuardianExample'
    component: str = 'myComponent'
    g = Guardian(knowledge_graph_url=knowledge_graph, pipeline_component=component)
    assert isinstance(g, Guardian)
    
    df = pd.DataFrame(
        data={
            "MAC": ["02:ab:1d:2f:12:12"],
            "value": [123],
        
        }
    )
    print(len(df))
    reports = g.validate(df)
    
    result = all([_.value for _ in reports])
    assert not result 
    
def test_shacl_validation():
    data = """
    @prefix sosa: <http://www.w3.org/ns/sosa/> .

    <http://example.org/my_place> a sosa:Platform ;
        sosa:hasFeatureOfInterest [ a sosa:Observation ;
                sosa:hasSimpleResult '11.8 °C' ] .
    """
    knowledge_graph: str = 'http://localhost:7200/repositories/GuardianExample'
    component: str = 'MapData'
    g = Guardian(knowledge_graph_url=knowledge_graph, pipeline_component=component)
    assert isinstance(g, Guardian)
    
    reports = g.validate(data)
    
    result = all([_.value for _ in reports])
    assert result 