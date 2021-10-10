# WikiCats: Leveraging Wikipedia Category Information to Enrich Content in Similar Articles

## Directory Structure:

. <br>
├── **data** <br>
├── **documents** <br>
├── LICENSE <br>
├── README.md <br>
├── **scripts** <br>
├── **src** <br>
└── **Union_Territories** <br>

***File Descriptions for each of the repository files can be obtained in [`./FileDescriptions.md`](./FileDescriptions.md)***

## Data Description:

* The project focuses on the [Union Territories](https://en.wikipedia.org/wiki/Category:Union_territories_of_India) subdomain. The Wikipedia category tree is used to explore the graph properties between the various nodes in the tree. 

* There are a total of 19625 Articles and 1969 Categories under the Union Territories category. 

* In order to represent a category by its knowledge graph embedding, the WikiData Embeddings by [PyTorch BigGraph](https://dl.fbaipublicfiles.com/torchbiggraph/wikidata_translation_v1.tsv.gz) were used. The size of these category embeddings are 200 dimensions. 

## Contributors:

* [Tanvi Karandikar](https://github.com/Tanvi141)
* [Mallika Subramanian](https://github.com/mallika2011)