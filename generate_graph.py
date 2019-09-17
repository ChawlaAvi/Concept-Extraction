from ontologies import *


class Graph():

    def __init__(self, ontology_pickle='all_ontologies.pickle'):

        self.ontology_pickle = ontology_pickle
        self.model = self.load_model()

        self.traverse_graph()

    def load_model(self):

        with open(self.ontology_pickle,'rb') as h:
            return pickle.load(h)


    def possible_match(self):
        pass


    def traverse_graph(self):

        pno = 4

        pprint( self.model.concept_model.text_data[pno])
        # pprint(self.model.match_list[pno])
        print("\n\n")
        for i in (self.model.match_list[pno]):

            # key = list(self.model.match_list[pno].keys())[0]

            key = i

            for k in range(len(self.model.match_list[pno][key])):

                j = (self.model.match_list[pno][key][k])
                pprint(j)


                print("\nSPO on subject")
                a = []
                for i in (list(self.model.graph.predicate_objects(subject = j[2]))):

                        a.append((j[2], i[0], i[1] ))
                pprint(a)
                print("\nSPO on object")
                a=[]
                for i in (list(self.model.graph.subject_predicates(object = j[2]))):

                        a.append((i[0], i[1], j[2]))

                pprint(a)

                print("\n\n")





        # print("SPO on predicate")
        # a = []
        # for i in (list(self.model.graph.subjects(predicate=j[2]))):
        #
        #     for k in (list(self.model.graph.objects(predicate=j[2], subject=i))):
        #
        #         a.append(( i, j[2], k))

        # pprint(a)
        # print("Predicates on Object")
        # pprint(list(self.model.graph.predicates(object=j[2])))
        #
        # print("Subject on Object")
        # pprint(list(self.model.graph.subjects(object=j[2])))
        #
        # print("Object on Subject")
        # pprint(list(self.model.graph.objects(subject=j[2])))

        # print("SP's")
        # pprint(list(self.model.graph.subject_predicates(j[2])))
        #
        # print("PO's")
        # pprint(list(self.model.graph.predicate_objects(j[2])))
        #
        # print("SO's")
        # pprint(list(self.model.graph.subject_objects(j[2])))



        # for i in self.model.match_list[pno]:
        #
        #     temp_list = self.model.match_list[pno][i]
        #
        #     for idx, j in enumerate(temp_list):
        #
        #         pprint(list(self.model.graph.subject_predicates(j[2])))




if __name__ == "__main__":

    graph = Graph()

    with open('final_model.pickle','wb') as h:
        pickle.dump(graph, h)



