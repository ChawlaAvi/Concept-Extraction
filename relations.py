import ontospy

class Relations():

    def __init__(self, file_name):

        self.file_name = file_name
        self.load_model()


    def load_model(self):

        self.onto_model = ontospy.Ontospy(self.file_name)
        self.get_properties()
        self.get_classes()


    def get_properties(self):

        self.properties = {}

        for i in self.onto_model.all_properties:

            a = i.qname.split(":")

            if a[0] not in self.properties:
                self.properties[a[0]] = []
            self.properties[a[0]].append(a[1])


    def get_classes(self):

        self.classes = {}

        for i in self.onto_model.all_classes:

            if not i.qname.lower().startswith("http"):

                a = i.qname.split(":")



                if a[0] not in self.classes:
                    self.classes[a[0]] = []
                self.classes[a[0]].append(a[1])


if __name__ == "__main__":


    relation = Relations('./ontologies/Agreements/statement.ttl')
    print(relation.properties)
    print(relation.classes)