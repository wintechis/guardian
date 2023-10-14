from guardian.models import QualityContract, QualityConstraint, Report
import requests
from guardian.config import get_config
from typing import Callable, Dict, List, Any
import hashlib
from guardian.query import is_valid_url, query_quality_contract_information, _send_report_to_graph
import guardian.exceptions as ge 
from datetime import datetime


CONFIG = get_config()


class Guardian:
 
    def __init__(self, knowledge_graph_url: str,  pipeline_component: str, mime_type: str = None):
        """ Initalizes the guardian for a given knowledge graph and a pipeline component. """
        self.contracts: Dict[str, List[QualityContract]] = {}
        self.knowledge_graph_uri: str = ''
        assert is_valid_url(knowledge_graph_url)
        
        self.knowledge_graph_uri = knowledge_graph_url
        
        contracts: List[QualityContract] = query_quality_contract_information(
                                                knowledge_graph_uri=knowledge_graph_url,
                                                component=pipeline_component,
                                                mime_type=mime_type )
        
        # Filter all contracts by the conformance
        for contract in contracts:
            for constraint in contract.constraints:
                if not (self.validate_conformance(constraint.conformance, constraint.format)):
                    contract.constraints.remove(constraint)
                    continue
                
                quality_constraint_ressource = self._download_resource_constraint_executable(
                                                constraint.artifact_uri)    
                
                self.load_resource_constraint_executable(constraint, quality_constraint_ressource)
        
        self.contracts[pipeline_component] = contracts
       

    def _select_algorithmn(self, algorithmn_name: str) -> Callable:
        integrity_algorithmns = {
            "http://spdx.org/rdf/terms#checksumAlgorithm_sha256": hashlib.sha256,
            "http://spdx.org/rdf/terms#checksumAlgorithm_sha3_256": hashlib.sha3_256,
            "http://spdx.org/rdf/terms#checksumAlgorithm_sha3_384": hashlib.sha3_384,
            "http://spdx.org/rdf/terms#checksumAlgorithm_sha3_512": hashlib.sha3_512,
            "http://spdx.org/rdf/terms#checksumAlgorithm_sha224": hashlib.sha224,
            "http://spdx.org/rdf/terms#checksumAlgorithm_sha384": hashlib.sha384,
            "http://spdx.org/rdf/terms#checksumAlgorithm_sha512": hashlib.sha512,
            "http://spdx.org/rdf/terms#checksumAlgorithm_sha1": hashlib.sha1,
            "http://spdx.org/rdf/terms#checksumAlgorithm_md5": hashlib.md5,
        }
        if algorithmn_name in integrity_algorithmns:
            return integrity_algorithmns[algorithmn_name]
        raise Exception()
            
    def validate_integrity(self, file: str, algorithmn: Callable, integrity_constraint: str) -> bool:
        result: bool = algorithmn((str.encode(file))).hexdigest() == integrity_constraint 
        return result

    def validate_conformance(self, conformance: str, format: str) -> bool:
        for _ in CONFIG.my_specification:
            allowed_conformance: bool = conformance == _.conformance
            allowed_format: bool = format in _.formats
            if allowed_conformance and allowed_format:
                return True
        return False

    def _download_resource_constraint_executable(self, url: str) -> str:
        """ Loads data from a source url. """
        assert is_valid_url(url)
        
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()
        return None

    def load_resource_constraint_executable(self, constraint: QualityConstraint, resource: str):
        """ Loads data from a source url. """
        constraint.initiate_function(resource)

    def validate(self, data: Any, args: Dict = {}) -> List[Report]:
        results = []
        for contract_name, contracts in self.contracts.items():
            for contract in contracts:
                for constraint in contract.constraints:
                    start_time = datetime.now()
                    value = True
                    try:
                        result = constraint._validate(data, args)
                        # If there is some result we try to evaluate it
                        if isinstance(result, bool):
                            value = result
                        
                        end_time=datetime.now()
                        result = Report(
                            value=value,
                            contract_name=contract_name,
                            #constraint_name=constraint,
                            start_time=start_time,
                            end_time=end_time
                        )
                    except ge.ValidationError as error:
                        end_time=datetime.now()
                        result = Report(
                            value=False,
                            error_report=error.data,
                            error=error.message,
                            contract_name=contract_name,
                           # constraint_name=constraint,
                            start_time=start_time,
                            end_time=end_time
                        )
                        
                    _send_report_to_graph(
                        knowledge_graph_uri=self.knowledge_graph_uri,
                        contract=contract,
                        constraint=constraint,
                        result=result)
                        
                    
                    results.append(result)
        return results
    
