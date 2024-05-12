import matplotlib.pyplot as plt
import networkx as nx
from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import Event, EventTypes, ConnectorTypes
from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LinkLayer.GenericLinkLayer import GenericLinkLayer
from adhoccomputing.Networking.NetworkLayer.GenericNetworkLayer import GenericNetworkLayer
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel
import csv
from ConveniantByzantineAuth import BANode

_topology = Topology()
global_nodes = []
global_byzantine_count = 0
is_general = False
is_byzantine = False
global_bc_nodes = []

def setup_csv_logger(filename='ByzantineAuth.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Source Node', 'Message', 'Signature_chain','Delivered Node', 'Pulse'])

class AdHocNode(GenericModel):

    def on_init(self, eventobj: Event):
        print(
            f"\033[0;92mInitializing {self.componentname}.{self.componentinstancenumber}\033[0m")
    def on_message_from_top(self, eventobj: Event):
        self.send_down(Event(self, EventTypes.MFRT, eventobj.eventcontent))

    def on_message_from_bottom(self, eventobj: Event):
        self.send_up(Event(self, EventTypes.MFRB, eventobj.eventcontent))

    def __init__(self, componentname, componentid, topology=None):
        super().__init__(componentname, componentid, topology=_topology)
        self.components = []
        # SUBCOMPONENTS
        self.appllayer = BANode(
            "ApplicationLayer", componentid, k=global_byzantine_count, is_general=is_general, is_byzantine=is_byzantine, nodes=global_nodes, topology=topology)
        self.netlayer = GenericNetworkLayer(
            "NetworkLayer", componentid, topology=topology)
        self.linklayer = GenericLinkLayer("LinkLayer", componentid)
        self.components.append(self.appllayer)
        self.components.append(self.netlayer)
        self.components.append(self.linklayer)

        # CONNECTIONS AMONG SUBCOMPONENTS
        self.appllayer.connect_me_to_component(
            ConnectorTypes.DOWN, self.netlayer)
        self.netlayer.connect_me_to_component(
            ConnectorTypes.UP, self.appllayer)
        self.netlayer.connect_me_to_component(
            ConnectorTypes.DOWN, self.linklayer)
        self.linklayer.connect_me_to_component(
            ConnectorTypes.UP, self.netlayer)
        
        self.linklayer.connect_me_to_component(ConnectorTypes.DOWN, self)
        self.connect_me_to_component(ConnectorTypes.UP, self.linklayer)


def main():

    n = 10
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(i):
            G.add_edge(i, j)
    pos = nx.spring_layout(G)
    options = {'font_size': 15,
               'node_size': 800,
               }
    setup_csv_logger() 
    nx.draw(G, pos, with_labels=True, **options)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, **options)

    _topology.construct_from_graph(G, AdHocNode, GenericChannel)


    global_nodes = _topology.nodes


    for i in range(len(global_nodes)):
        for component in global_nodes[i].components:
            if isinstance(component,BANode):
                global_bc_nodes.append(component)

    global_byzantine_count = 3
    for i in range(len(global_nodes)):
        for component in _topology.nodes[i].components:
            if isinstance(component,BANode):
                component.nodes = global_bc_nodes
                component.k = global_byzantine_count
  

    for component in _topology.nodes[1].components:
        if isinstance(component,BANode):
            component.is_byzantine = True
    for component in _topology.nodes[0].components:
        if isinstance(component,BANode):
            component.is_byzantine = True
    for component in _topology.nodes[2].components:
        if isinstance(component,BANode):
            component.is_byzantine = True
    # for component in _topology.nodes[3].components:
    #     if isinstance(component,BANode):
    #         component.is_byzantine = True
    for component in _topology.nodes[4].components:
        if isinstance(component,BANode):
            component.is_general = True

    _topology.start()
    plt.savefig("graph.png")


if __name__ == "__main__":

    main()