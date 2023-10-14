{
  "properties" : {
    "current.location" : ""
  },
  "import.local" : {
    "GuardianExample;;Text snippet 2023-08-31 16:34:55.821" : {
      "name" : "Text snippet 2023-08-31 16:34:55.821",
      "status" : "DONE",
      "message" : "Imported successfully in less than a second.",
      "context" : "",
      "replaceGraphs" : [ ],
      "baseURI" : "file:/snippet/generated/ad6916e7-e5c6-4dbd-8466-a2854cbe49cc",
      "forceSerial" : false,
      "type" : "text",
      "format" : "text/turtle",
      "data" : "@prefix odrl: <http://www.w3.org/ns/odrl/2/> .\n@prefix prof: <http://www.w3.org/ns/dx/prof/> .\n@prefix dcat: <http://www.w3.org/ns/dcat#> .\n@prefix dct: <http://purl.org/dc/terms/> .\n@prefix spdx: <http://spdx.org/rdf/terms#> .\n@prefix val: <http://purl.org/graphguard/ontology#> .\n\nval:QualityContract1 a val:QualityContract ;\ndcat:identifier \"MyQualityContract\";\n    odrl:target [\n        a dcat:Dataset;\n        dcat:identifier \"LoadData\";\n        dcat:format \"pandas/dataframe\"\n    ] ;\n    prof:isProfileOf [\n        a val:QualityConstraint;\n        dcat:identifier \"LoadedDataConstraint\";\n        val:severeity \"error\" ;\n        prof:hasResource [\n            prof:hasArtifact <https://renedorsch.solidweb.org/validation_code/sensor_constraints.yml> ;\n            dct:conformsTo <https://specs.frictionlessdata.io/data-package/> ;\n            dct:format \"application/yaml\" ;\n            spdx:checksum [\n                spdx:algorithm <http://spdx.org/rdf/terms#checksumAlgorithm_sha256> ;\n                spdx:checksumValue \"54ed4c727f8ebaeab69ef8a6b57cb15a6d1fa26c20b0d80902f7357da4c797fd\"\n            ]\n        ]\n    ] .\nval:QualityContract2 a val:QualityContract ;\ndcat:identifier \"MyQualityContract\";\n    odrl:target [\n        a dcat:Dataset;\n        dcat:identifier \"ProcessData\";\n        dcat:format \"pandas/dataframe\"\n    ] ;\n    prof:isProfileOf [\n        a val:QualityConstraint;\n        dcat:identifier \"ProcessedDataConstraint\";\n        val:severeity \"error\" ;\n        prof:hasResource [\n            prof:hasArtifact <https://renedorsch.solidweb.org/validation_code/temperature_validation.py> ;\n            dct:conformsTo <http://python.org> ;\n            dct:format \"text/x-python\" ;\n            spdx:checksum [\n                spdx:algorithm <http://spdx.org/rdf/terms#checksumAlgorithm_md5> ;\n                spdx:checksumValue \"fda5c517ef55f972d553aca951caf506\"\n            ]\n        ]\n    ] .\n\nval:QualityContract3 a val:QualityContract ;\ndcat:identifier \"MyQualityContract\";\n    odrl:target [\n        a dcat:Dataset;\n        dcat:identifier \"MapData\";\n        dcat:format \"text/turtle\"\n    ] ;\n    prof:isProfileOf [\n        a val:QualityConstraint;\n        dcat:identifier \"ProcessedDataConstraint\";\n        val:severeity \"error\" ;\n        prof:hasResource [\n            prof:hasArtifact <https://renedorsch.solidweb.org/validation_code/valid_temperature_shape.ttl> ;\n            dct:conformsTo <https://www.w3.org/ns/shacl> ;\n            dct:format \"text/turtle\" ;\n            spdx:checksum [\n                spdx:algorithm <http://spdx.org/rdf/terms#checksumAlgorithm_md5> ;\n                spdx:checksumValue \"fda5c517ef55f972d553aca951caf506\"\n            ]\n        ]\n    ] .",
      "timestamp" : 1693492495858,
      "parserSettings" : {
        "preserveBNodeIds" : false,
        "failOnUnknownDataTypes" : false,
        "verifyDataTypeValues" : false,
        "normalizeDataTypeValues" : false,
        "failOnUnknownLanguageTags" : false,
        "verifyLanguageTags" : true,
        "normalizeLanguageTags" : false,
        "stopOnError" : true
      }
    }
  }
}