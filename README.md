# cy-jdeps
Scripts for analyzing dependencies in the Cytoscape App Store.
Uses python 2.7

### Download all Apps from the App Store

    python download_apps.py /path/to/download/folder
    
### Search for package dependencies

    python find_package.py /path/to/download/folder org.cytoscape.filter

Output:

```
org.cytoscape.filter
   BridgeDb-v1.1.0.jar
   CytoGEDEVO-v1.0.jar

org.cytoscape.filter.model
   BridgeDb-v1.1.0.jar
   CytoGEDEVO-v1.0.jar
```

### Search for class-level dependencies

    python find_package.py -c /path/to/download/folder org.cytoscape.filter

Output:

```
org.cytoscape.filter
   BridgeDb-v1.1.0.jar
   CytoGEDEVO-v1.0.jar

org.cytoscape.filter.model
   BridgeDb-v1.1.0.jar
   CytoGEDEVO-v1.0.jar

org.cytoscape.filter.model.CompositeFilter
   CytoGEDEVO-v1.0.jar

org.cytoscape.filter.model.NamedTransformer
   BridgeDb-v1.1.0.jar
   CytoGEDEVO-v1.0.jar

org.cytoscape.filter.model.Transformer
   CytoGEDEVO-v1.0.jar

org.cytoscape.filter.model.TransformerSink
   CytoGEDEVO-v1.0.jar

org.cytoscape.filter.model.TransformerSource
   CytoGEDEVO-v1.0.jar
```
