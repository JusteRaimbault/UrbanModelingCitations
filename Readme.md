
## Dataset

The clean dataset is 
 - `processed/core_full_edges.csv` ; `processed/core_full_nodes.csv` for the full (incomplete) graph
 - `processed/core_hdepth400_filtered_{edges|nodes}.csv` for the filtered network at horizontal depth 400.

**We work on the second**

(both are core networks (remove vertices with degree <= 1 until no more))

### node attributes

 - `id` unique id
 - `title` title of the paper
 - `year` publication year
 - `depth` the vertical depth (between 0 : leafs and 2 : origin corpus)
 - `horizontalDepth` the minimal horizontal depth accross all origins - references in initial corpus have an horizontal depth corresponding
to request order ; it is them backward propagated to citing references recursively
 - attributes with keyword names : horizontal depth for each request - requests are coded by a key here, correspondance is in file `data/request_microsim_1.csv` (plus additional `spatialmicrosim` = spatial microsimulation done separately). NA means the reference is never reached for this request.

=> to filter at a given horizontal depth across all requests, use horizontalDepth ; for a given request use the corresponding attribute.


