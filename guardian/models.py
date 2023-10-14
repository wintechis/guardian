from pydantic import BaseModel
from typing import List, Optional, Callable, Any, Union
from datetime import datetime 
from pandera import DataFrameSchema
from pandera.errors import SchemaError, SchemaDefinitionError
from pandera.io import from_frictionless_schema
from guardian.config import get_logger
import yaml
import json
import re
import guardian.exceptions as ge 
import string
import random
import pyshacl

LOGGER = get_logger()

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def _match_function_name(function_string: str):
    match = re.search(r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)', function_string)
    return match.group(1) if match else None


def replace_function_name(function_string: str, new_name: str):
    
    match = re.sub(r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)', new_name, function_string)
    return match

def make_function_executable(__function: str) -> Callable:
    if not isinstance(__function, str):
        return None
    
    

    #_function_name = get_random_string(16)
    #__function = replace_function_name(__function, _function_name)
    _function_name = _match_function_name(__function)
    
    LOGGER.debug(f"Create new verification function called: {_function_name}" )
    LOGGER.debug(f"Function: {__function}" )
    
    if not isinstance(_function_name, str):
        return None
    


    exec(__function)
    function: Callable = eval(_function_name)
    return function





class QualityConstraint(BaseModel):
    
    enforced: bool
    artifact_uri: str
    checksum_algorithmus: str
    checksum: str
    conformance: str
    format: str
    validation_function: Callable = None

    def initiate_function(self, file: str):
        """Initiate validation function"""
        LOGGER.debug("Initate validation function with information:")
        LOGGER.debug(file)
        if self.conformance == "https://specs.frictionlessdata.io/data-package/":
            self._initate_frictionless_function(file)
        if self.conformance == 'http://python.org':
            self._initate_python_function(file)
        if self.conformance == "https://www.w3.org/ns/shacl":
            self._initiate_shacl_function(file)

    def _initiate_shacl_function(self, file: str):
        """ Initates the validation function for a frictionless schema. """
        LOGGER.debug("Initiate shacl function. ")
        
        def validate_shacl(shacl_rules):
            def validate_shacl(data_graph):
                rules = shacl_rules
                conforms, _, error_message = pyshacl.validate(data_graph=data_graph,
                                        shacl_graph=rules, 
                                        shacl_graph_format=self.format)
                if conforms:
                    return conforms
                else:
                    raise ge.ValidationError(message="A Validation Error occured",
                                            data=error_message)
                
            return validate_shacl
        validate = validate_shacl(file)
        self.validation_function = validate
        
    def _initate_frictionless_function(self, file: str):
        """ Initates the validation function for a frictionless schema. """
        LOGGER.debug("Initiate fricitionless function. ")
        if self.format == "application/yaml":
            file = yaml.safe_load(file)
        if self.format == "application/json":
            file = json.loads(file)
        
        def validate_frictionless_schema(file):
            schema: DataFrameSchema = from_frictionless_schema(file)
            def validate_schema(data, *args):
                try:
                    df = schema.validate(data, *args)
                    return True
                
                except SchemaError as err:
                    raise ge.ValidationError(message="A SchemaValidationError occured",
                                     data=err)
                except SchemaDefinitionError as err:
                    raise ge.ValidationError(message="A SchemaDefinitionValidationError occured",
                                            data=err)
            return validate_schema
        

        self.validation_function = validate_frictionless_schema(file)

    def _initate_python_function(self, file: str):
        """ Initates an abritrary python function as a validation procedure. """
        def validate_python_function(file):
            def validate(data):
                validation_function = make_function_executable(file)
                try:
                    res: bool = validation_function(data)
                    if res == True:
                        return True
                    else:
                        return False
                except Exception:
                    raise ge.ValidationError(message="A SchemaDefinitionValidationError occured",
                                            data='No error report provided')
            return validate
        
        self.validation_function = validate_python_function(file)
        

    def _validate(self, data, args: dict = {}):
        """ Validates data """
        
        results = self.validation_function(data)
        LOGGER.debug(f"Validation results are: {results}")
        return results

        
    

class QualityContract(BaseModel):
    identifier: str = ''
    constraints: List[QualityConstraint] = []
    dataset_identifier: str
    mime_type: Union[str, None]


class Report(BaseModel):
    value: bool
    error_report: Any = None
    error: str = ''
    contract_name: str
    #constraint_name: str
    start_time: datetime
    end_time: datetime
    
class ValidationProcedure(BaseModel):
    started: datetime
    ended: datetime
    used: List[str]
    result: bool

