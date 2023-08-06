import graphviz


class ERD:
    """
    Parameters
    ----------
    input: graphviz.Graph
        The object from the graphviz.Graph class.
    """

    def __init__(self, gr) -> None:
        self.gr = gr

    @staticmethod
    def process_label(str):
        if str is not None:
            return f"<{str}>"
        else:
            return None

    def entity(self, node_name="course", node_label=None):
        self.gr.node(node_name, self.process_label(node_label), shape="box")

    def weak_entity(self, node_name, node_label=None):
        self.gr.node(
            node_name,
            self.process_label(node_label),
            shape="box",
            peripheries="2",
        )

    def associative_entity(self, node_name, node_label=None):
        self.gr.node(node_name, self.process_label(node_label), shape="Msquare")

    def attribute(self, node_name, node_label=None):
        self.gr.node(node_name, self.process_label(node_label), shape="ellipse")

    def multivalue(self, node_name, node_label=None):
        # self.gr.node(node_name, node_label, {"shape": "ellipse", "peripheries": "2"})
        self.gr.node(
            node_name,
            self.process_label(node_label),
            shape="ellipse",
            peripheries="2",
        )

    def key(self, node_name, node_label=None):
        if node_label is None:
            text = node_name
        else:
            text = node_label
        self.gr.node(node_name, self._str_key(text), shape="ellipse")

    @staticmethod
    def _str_key(label):
        return f"<<u>{label}</u>>"

    def derived(self, node_name, node_label=None):
        self.gr.node(
            node_name,
            self.process_label(node_label),
            shape="ellipse",
            style="dashed",
        )

    def weak_key(self, node_name, node_label=None):
        if node_label is None:
            text = node_name
        else:
            text = node_label
        self.gr.node(node_name, label=self._weak_key(text), shape="ellipse")

    @staticmethod
    def _weak_key(label):
        return f"""<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0">
    <TR>
        <TD COLSPAN="1" SIDES="B" STYLE="dashed">{label}</TD>
    </TR>
    </TABLE>>"""

    def relation(
        self,
        relation_name,
        attr1,
        attr2,
        label_attr1=None,
        label_attr2=None,
        identifying="no",
    ):
        """
        Parameters
        ----------
            identifying: str
                No: single lines. Yes: double lines.
        """
        if identifying == "no":
            lines = "1"
        else:
            lines = "2"
        self.gr.node(relation_name, shape="diamond", peripheries=lines)
        # e.edge('C-I', 'institute', label='1', len='1.00')
        self.gr.edge(
            attr1, relation_name, label=self.process_label(label_attr1)
        )
        self.gr.edge(
            attr2, relation_name, label=self.process_label(label_attr2)
        )


if __name__ == "__main__":
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
    obj.relation("relationship", "entity1", "entity2", "(1,2)", "(2, 1)", "yes")

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
