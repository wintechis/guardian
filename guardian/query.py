from SPARQLWrapper import SPARQLWrapper2
from guardian.models import QualityConstraint, QualityContract, Report
from typing import List, Union
from guardian.config import get_logger, get_config
from urllib.parse import urlsplit
from datetime import datetime


CONFIG = get_config()
LOGGER = get_logger()

SPARQL: SPARQLWrapper2 = None
def is_valid_url(url: str) -> bool:
    try:
        result = urlsplit(url)
        return True
    except ValueError:
        return False

def _get_sparql(knowledge_graph_uri: str, method: str) -> SPARQLWrapper2:
    global SPARQL
    allowed_vendor_list: List = ["fuseki", "graphdb", "rdf4j", "stardog"]
    if CONFIG.vendor in allowed_vendor_list:
        if CONFIG.vendor == "graphdb" and method == "POST":
            SPARQL = SPARQLWrapper2(f"{knowledge_graph_uri}/statements")
        else:    
            SPARQL = SPARQLWrapper2(knowledge_graph_uri)
    return SPARQL

def query_quality_contract_information(knowledge_graph_uri: str, component: str, mime_type: Union[str, None]) -> List[QualityContract]:
    
    sparql = _get_sparql(knowledge_graph_uri, "GET")
    query = """
    PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
    PREFIX prof: <http://www.w3.org/ns/dx/prof/>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX spdx: <http://spdx.org/rdf/terms#>
    PREFIX val: <http://purl.org/graphguard/ontology#>
    SELECT ?qualityContract ?severeityLevel ?artifact_uri ?conformance ?format ?checksum_algorithmn ?checksum
    WHERE {
        ?qualityContract a val:QualityContract;
            odrl:target [
                dcat:identifier "COMPONENT_IDENTIFIER"
                ; dcat:format "MIME_TYPE"
            ];
            prof:isProfileOf [
                val:severeity ?severeityLevel;
                prof:hasResource [
                    prof:hasArtifact ?artifact_uri;
                    dct:conformsTo ?conformance;
                    dct:format ?format;
                    spdx:checksum [
                        spdx:algorithm ?checksum_algorithmn;
                        spdx:checksumValue ?checksum
                    ]
                ]
            ]
    }
    """

    
    query = query.replace("COMPONENT_IDENTIFIER", component)

    if mime_type is None:
        query = query.replace('; dcat:format "MIME_TYPE"\n', '')
    else:
        query = query.replace('MIME_TYPE', mime_type)
    
    sparql.setQuery(query)
    
  
    quality_contracts: List[QualityContract] = []
    try: 
        _contracts = {}
        for result in sparql.query().bindings:
            
            if result['qualityContract'].value not in _contracts:
                _contracts[result['qualityContract'].value] = QualityContract(dataset_identifier=component, mime_type=mime_type)
            
            quality_contract = _contracts[result['qualityContract'].value]
            severity_level = result['severeityLevel'].value
            enforced: bool = severity_level == 'error'
            quality_contract.constraints.append(
                QualityConstraint(
                    enforced=enforced,
                    artifact_uri=result['artifact_uri'].value,
                    checksum_algorithmus=result['checksum_algorithmn'].value,
                    checksum=result['checksum'].value,
                    conformance=result['conformance'].value,
                    format=result['format'].value,
                )
            )
        quality_contracts = list(_contracts.values())
    except Exception as e:
        LOGGER.debug(e)
    return quality_contracts



def _send_report_to_graph(knowledge_graph_uri: str, contract: QualityContract, constraint: QualityConstraint, result: Report):
    sparql = _get_sparql(knowledge_graph_uri, "POST")
    
    query = """
    PREFIX dqv:  <http://www.w3.org/ns/dqv#> 
    PREFIX prof: <http://www.w3.org/ns/dx/prof/>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX spdx: <http://spdx.org/rdf/terms#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX val: <http://purl.org/graphguard/ontology#>
    INSERT  {
        [] a val:QualityReport;
            dqv:computedOn ?dataset;
            dqv:result "RESULT"^^xsd:boolean;
            prov:generatedAtTime "NOW"^^xsd:dateTime;
            prov:generatedBy [
                a val:QualityValidation;
                prov:startedAtTime "STARTTIME"^^xsd:dateTime;
                prov:endedAtTime "ENDTIME"^^xsd:dateTime;
                prov:used ?resource, ?dataset;
                prov:wasAssociatedWith <ME>
            ];
            val:report '''REPORT'''
            
    } WHERE {
        ?qualityContract a val:QualityContract;
            odrl:target ?dataset.
        ?dataset dcat:identifier "COMPONENT_IDENTIFIER".
        ?qualityContract prof:isProfileOf [ prof:hasResource ?resource ].
        ?resource spdx:checksum [ spdx:checksumValue ?checksum ].
                    
        FILTER (?checksum = "CHECKSUM")
        
    } 
    """
    query = query.replace("NOW", datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
    query = query.replace("STARTTIME", result.start_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
    query = query.replace("ENDTIME", result.end_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
    query = query.replace("ME", CONFIG.my_uri)
    
    if result.value:
        validation_result = "true"
    else:
        validation_result = "false"
    query = query.replace("RESULT", validation_result)

    report_message = str(result.error_report)
    if result.value == True:
        report_message = 'Validation was successful. No validation errors detected. '
    
    query = query.replace("REPORT", f"{report_message}")
    
    query = query.replace("COMPONENT_IDENTIFIER", contract.dataset_identifier)
    query = query.replace("CHECKSUM", constraint.checksum)

    LOGGER.debug(f"Prepared Report to send it to graph")
    LOGGER.debug(query)
    sparql.setQuery(query)
    sparql.method = 'POST'
    
    post_result = sparql.query()
    LOGGER.debug(f"Returned POST message with result: {post_result}")
