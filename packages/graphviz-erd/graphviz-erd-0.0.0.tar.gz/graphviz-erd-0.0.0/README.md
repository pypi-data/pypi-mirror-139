# graphviz-erd

Draw Entity Relationship Diagrams (ERD) with python and graphviz.

This code is built on top of the [graphviz](https://pypi.org/project/graphviz/) python package and provides methods to facilitate the declaration of blocks commonly used in ERD such as entities and attributes.


## Example

We can draw diagrams like
![erd](https://media.githubusercontent.com/media/mashi/graphviz-erd/main/fig/erd.png)
<!--
Link to the image because it was not showing in pypi.org.
To obtain the link:
1. Go to the image address in the Github repository.
2. right click on the image and select 'Copy Image Link'
-->

using the code:
```
    gr = graphviz.Graph("ER", filename="erd", engine="dot", format="png")
    obj = ERD(gr)

    # node name and node label
    obj.entity("entity1", "entity 1")
    # the label is optional as it is in graphviz
    obj.attribute("attr")
    # new lines using the html notation
    obj.multivalue("multi", "multivalued<BR/>attribute")
    obj.key("key", "key attribute")
    obj.derived("derived")
    obj.weak_key("weak")

    obj.associative_entity("assoc", "associative<BR/>entity")

    obj.weak_entity("entity2", "weak entity 2")

    # draw relation between entities
    obj.relation("relationship", "entity1", "entity2", "(1,2)", "(2, 1)", "yes")

    # connect the attributes
    obj.gr.edges(
        [
            ("entity1", "attr"),
            ("entity1", "multi"),
            ("entity1", "key"),
            ("entity1", "weak"),
            ("entity1", "derived"),
        ]
    )

    obj.gr.view()
```


## Instructions (Development)

Assuming a linux environment (Ubuntu), to develop inside a virtual environment using git hooks:
```
python3 -m venv .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt
pre-commit install
```
