import luigi
from luigi import Task
import rdflib
from rdflib import Graph, URIRef, Literal, SOSA, BNode, RDF
import pandas as pd
from guardian.guardian import Guardian
import time

DATA = {}

class LoadData(Task): 
    task_param = luigi.Parameter()
    
    def run(self):
        print("**************** LoadData Task ****************")
        print("INITALIZE Guardian for component: 'LoadData'")
        g = Guardian('http://localhost:7200/repositories/GuardianExample', 'LoadData', 'pandas/dataframe')
        file = pd.read_csv(filepath_or_buffer=f"{self.task_param}") 
        results = g.validate(file)   
        for res in results:
            print("VALIDATION RESULT: ", res.value)
            assert res.value is True

        print("STORE RESULTS")
        DATA['loaded'] = file
    def complete(self):
        return 'loaded' in DATA.keys()
    
    
class ProcessData(Task):
    task_param = luigi.Parameter()
    def requires(self):
        return [LoadData(task_param=self.task_param)]
    
    def run(self):
        print("**************** ProcesData Task ****************")
        print("INITALIZE Guardian for component: 'ProcessData'")

        g = Guardian('http://localhost:7200/repositories/GuardianExample', 'ProcessData', 'pandas/dataframe')
        df = DATA['loaded']
        average_temperature = df[df['type'] == 'Temperature']['value'].mean()
        print(average_temperature)
        results = g.validate(average_temperature)
        for res in results:
            print("VALIDATION RESULT: ", res.value)
            if res.value == False:
                time.sleep(10)
            assert res.value is True

        print("STORE RESULTS")
        DATA['processed_temperature'] = average_temperature
        
    def complete(self):
        return 'processed_temperature' in DATA.keys()
    
class MapData(Task):
    task_param = luigi.Parameter()
    def requires(self):
        return [ProcessData(task_param=self.task_param)]
    
    def run(self):
        print("**************** MapData Task ****************")

        graph = Graph()
        
        temperature = DATA['processed_temperature']
        
        print("MAP DATA TO RDF")
        blankNode = BNode()
        graph.add((URIRef("my_place", base="http://example.org"), SOSA.hasFeatureOfInterest, blankNode))
        graph.add((URIRef("my_place", base="http://example.org"), RDF.type, SOSA.Platform))
        graph.add((blankNode, SOSA.hasSimpleResult, Literal(f"{temperature} °C")))
        graph.add((blankNode, RDF.type, SOSA.Observation))
        graph_data: str = graph.serialize(format="turtle",
                                          encoding="UTF-8").decode()
        
        print("INITALIZE Guardian for component: 'MapData'")
        g = Guardian('http://localhost:7200/repositories/GuardianExample', 'MapData', 'text/turtle')
        results = g.validate(graph_data)
        for res in results:
            print("VALIDATION RESULT: ", res.value)
            assert res.value is True
        print("FINISHED MapData Task")
        
        graph.serialize(destination="./output.ttl",
                                          format="turtle",
                                          encoding="UTF-8")
        
        time.sleep(10)
        
    def output(self):
        return luigi.LocalTarget('output.ttl')
    
    
if __name__ == '__main__':
    luigi.run()