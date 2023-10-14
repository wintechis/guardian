from pydantic import BaseModel, ValidationError, Field
from typing import List
import yaml

import logging
import logging.config
from logging import Logger
import sys
import os

PATH = os.path.dirname(__file__)
# Load the logging configuration
logging.config.fileConfig(f"{PATH}/logging.conf")

# Get the logger

class Specification(BaseModel):
    conformance: str
    formats: List[str]
    
class BaseConfig(BaseModel):
    knowledge_graph: str = Field(alias="knowledge_graph")
    vendor: str = Field(alias="knowledge_graph_vendor")
    my_name: str = Field(alias="created_by")
    my_uri: str = Field(alias="created_uri")
    my_description: str = Field(alias="description")
    my_specification: List[Specification] = Field(alias="conformance_standards")

__CONFIG: BaseConfig = None
__LOGGER: Logger = None


def get_logger() -> Logger:
    global LOGGER
    if __LOGGER is None:
        return logging.getLogger('sampleLogger')
    return __LOGGER



def get_config() -> BaseConfig:
    """ Returns the current config. """
    global __CONFIG
    if __CONFIG is None:
        with open((f"{PATH}/config.yml"), 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        try:
            __CONFIG = BaseConfig(**yaml_data)
        except ValidationError as e:
            print(f"Validation error: {e}")
    return __CONFIG



