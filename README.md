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