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


### `data` Directory:

| File | Description |
|:----:|-----------|
| [`al_subcat_tree.txt`](./data/al_subcat_tree.txt)    | Represents the article inlinks amongst all articles of the corpus. Each line is represented as \<article_id\>: [comma separated list of (\<inlinked-article\>,\<edge-weight\>)]. The edge weight here represents the cumulative weighted sum of the number of times a particular article is referenced in the source article. The edge weight heuristics are: `wt = num_occurances*(10^(isInfobox))`. The script that can be used to generate this file is: [`./src/data_collection/get_inlinks_tree.py`](./src/data_collection/get_inlinks_tree.py)|
| [`al_inlinks_tree.txt`](./data/al_inlinks_tree.txt)    |  Represents the edges of the Wikipedia category tree. Each line is represented as \<category_id\>:[comma separated list of subcategories under this category] |
| [`article_cat_map.json`](./data/article_cat_map.json)     |   A file that maps every article to its corresponding list of categories. The file can be read as a json dictionary where the keys are the `article_ids` (as strings) and the values are the list of `category_ids` (as strings) associated with that article. The script that can be used to generate this file is: [`./src/data_collection/get_categories_for_articles.py`](./src/data_collection/get_categories_for_articles.py)        |
|[`article_id_name.txt`](./data/article_id_name.txt)      |  Maps every `article_id` to its corresponding `article name`. Each line is represented as \<article_id\>:\<article_name\>           |
|[`cat_embeddings.npy`](./data/cat_embeddings.npy)      |   Stories the Wikidata knowledge graph category embeddings for each category. The file is a numpy array of shape: `<number of categories> x <embedding size>`. Here the index of a category embedding does **not** correspond to its category ID. In order to map a category ID to its corresponding index in this file, use the file [`./date/cat2idx.json`](./date/cat2idx.json)          |
| [`cat2emb.txt`](./data/cat2emb.txt)     |  Each line represents `<category_id>:<N dimensional embedding with each the N dimensions as tab separated>`           |
| [`cat2idx.json`](./data/cat2idx.json)     | Represents the mapping between original category IDs and their corresponding index in the [`cat_embeddings.npy`](./data/cat_embeddings.npy) array.            |
|[`cat2kg_id.json`](./data/cat2kg_id.json)       | Represents the mapping between an original category ID and its corresponding Wikidata **Q-identifier** ID.             |
| [`categories_parent_ids.txt`](./data/categories_parent_ids.txt)     |  Each line of the file represents a \<category_id\>:\<tab separated list of parent_category IDs upto 3 levels up the category tree\>           |
| [`categories_parent.txt`](./data/categories_parent.txt)     |  Each line of the file represents a \<category_name\>:\<tab separated list of parent category names upto 3 levels up the category tree\>           |
| [`category2id.json`](./data/category2id.json)     |  Maps every category name to its corresponding category ID. Here, the category names are exactly as the wikipedia category names, all prefixed with `Category:`.           |
| [`combine.zip`](./data/combine.zip)     |  Extract to obtain a custom XML file containing only the articles corresponding to the Union Territory Subdomain. Each article in the union territories list has a separate `<page>` element in the XML file. The entire content of each interest article, as present in the wikipedia xml dump, is combined here. The link to this file is: [TODO](TODO)           |
| [`consolidated_subpages.txt`](./data/consolidated_subpages.txt)     |  Represents all the pages corresponding to each category. Each line represents a \<category_id\>:\<comma separated list of subpages that fall under this category\>. The script that can be used to generate this file is [`./src/data_collection/get_cat_tree.py`](./src/data_collection/get_cat_tree.py) |
| [`id2article.json`](./data/id2article.json)     |  A mapping of each article ID to its corresponding article name |
| [`missing_titles.txt`](./data/missing_titles.txt)     | A list of article IDs for which an error response was received while querying for the corresponding article name |

### `scripts` Directory:

| File | Description |
|:----:|-----------|
| [`adj.sh`](./scripts/adj.sh)    | Bash script to generate the **custom adjacency list via our pipeline** for a subset of articles |
| [`run.sh`](./scripts/run.sh)    | Bash script |

### `src/data_collection` Directory:

| File | Description |
|:----:|-----------|
| [`get_articles.py`](./src/data_collection/get_articles.py)    | Script to get the XML content of all required articles |
| [`get_cat_parent_ids.py`](./src/data_collection/get_cat_parent_ids.py)    | To collect the **IDs** of parent categories upto 3 levels up for all the categories in the Union Territory category tree.  |
| [`get_cat_parent.py`](./src/data_collection/get_cat_parent.py)    | To collect the **names** of parent categories upto 3 levels up for all the categories in the Union Territory category tree.  |
| [`get_cat_tree.py`](./src/data_collection/get_cat_tree.py)    | Constructs the wikipedia category tree **top-down** with the start node as the [Union Territories](https://en.wikipedia.org/wiki/Category:Union_territories_of_India) category. Generates the following files: <ul> <li>[`a file`](./Union_Territories/Union Territories of India_cat_keys.txt) that maps each category name to its corresponding category ID </li> <li>The subpages and subcats corresponding to each category. Files can be found [here](./Union_Territories/)</li> </ul> |
| [`get_cat_wikidata_ids.py`](./src/data_collection/get_cat_wikidata_ids.py)    | To collect Wikidata knowledge graph IDs corresponding to each category ID  |
| [`get_categories_for_articles.py`](./src/data_collection/get_categories_for_articles.py)    | Generates the list of categories corresponding to each article that is present under the Union Territories category (sub) tree. This is done since, the articles present in this tree need not necessarily have all their categories belonging to the UT tree itself. Hence this scripts helps get all the categories involved.  |
| [`get_inlinks_tree.py`](./src/data_collection/get_inlinks_tree.py)    | Obtains the in-links between different articles of interest by parsing their XML content. Generates the corresponding adjacency list with articles as nodes for the same.  |
| [`map_cat2emb_index.py`](./src/data_collection/map_cat2emb_index.py)    | Maps each category ID to its corresponding index in [`./data/cat_embeddings.npy`](./data/cat_embeddings.npy)  |
| [`utils.py`](./src/data_collection/utils.py)    | A class with a few utility functions that can be used while querying the wikipedia API  |
| [`xml_parser_withwrite.py`](./src/data_collection/xml_parser_withwrite.py)    | Parses multiple XML files as chunks of articles from the wikipedia data dump and then converts it to a custom XML file containing only those articles that are of interst. Rebuilds the XML element tree by selectively including articles that belong under the UT category tree.  |

### `src/parse_tree` Directory:

| File | Description |
|:----:|-----------|
| [`ArticleMap.py`](./src/parse_tree/ArticleMap.py)    | A class with functions to get a list of articles under a particular category, and get a list of categories for a particular article |
| [`LabelMatcher.py`](./src/parse_tree/LabelMatcher.py)    | **Main Class** that performs the entire pipeline of carefully parsing the category tree and generating a corresponding list of similar articles -- using the tree, and knowledge graph informaiton. More information about the pipeline can be found [TODO: Link paper pdf]()|
| [`cat_vec.py`](./src/parse_tree/cat_vec.py)    | Script to obtain the category embeddings from the WikiData knowledge graph. Uses embeddings from [PyTorch BigGraph](https://dl.fbaipublicfiles.com/torchbiggraph/wikidata_translation_v1.tsv.gz) |
| [`Tree.py`](./src/parse_tree/Tree.py)    | A class with several functions to parse the category tree. Functions include: <ul><li>Get neighbours of a particular node -- parents or children upto K hops</li><li>Mapping of a category ID to its corresponding height in the tree from the root node</li></ul> |
| [`WikiParser.py`](./src/parse_tree/WikiParser.py)    | [Deprecated] A class with functions to score articles and categories while parsing the cateogry tree for an input article. A diagramatic explanation of the same can be found [here](./documents/p1_n1_c1.drawio) |
| [`adj_<TYPE>.sh`](./src/parse_tree/adj_<TYPE>.sh)    | Bash scripts to create the adjacency lists based on the pipeline. TYPE can be -- train, test, val |

### `src/training` Directory:

| File | Description |
|:----:|-----------|
| [`create_train_test.py`](./src/training/create_train_test.py)    | Script to shuffle and split all the articles under the union territory domain into train, test and validation sets of articles. These are then used to prepare the corresponding adjacency list files. |