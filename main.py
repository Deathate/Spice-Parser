import networkx
import re
from pprint import pprint
from pathlib import Path
from PySpice.Spice.Parser import SpiceParser
from PySpice.Spice.Netlist import Circuit, Element
import Levenshtein


def parse_netlist(file_path):
    file_path = Path(file_path)
    main_circuit_name = file_path.stem
    text = open(file_path, 'r').read()
    text = text.replace("\n+", " ")
    subckts = re.findall(r'(\.subckt\s+(\S+)\s+[\S\s]*?\.ends)', text, re.IGNORECASE)

    min_dis = 1e5
    for i, element in enumerate(subckts):
        if (d := Levenshtein.distance(main_circuit_name, element[1])) < min_dis:
            min_dis = d
            main_circuit_id = i
    subckts[main_circuit_id] = "\n".join(
        subckts[main_circuit_id][0].split("\n")[1:-1]), subckts[main_circuit_id][1]
    # source = "\n".join([x[0] for x in subckts])
    source = subckts[main_circuit_id][0]

    G = networkx.Graph()
    parser = SpiceParser(source=source)
    circuit = parser.build_circuit()
    device_names = []
    node_names = set()
    excludes = []
    for element in circuit.elements:
        # Elements have 'pins' attributes which show their connected nodes
        pins = element.pins
        # print(element.name)
        device_names.append(element.name)
        for pin in pins:
            if pin.name == "bulk":
                excludes.append(str(pin.node))
            # print(f"   Connected to {pin}")
            # G.add_node(element.name)
            # G.add_node(str(pin.node))
            G.add_edge(element.name, str(pin.node))
            node_names.add(str(pin.node))
    G.remove_nodes_from(excludes)
    # print(G.edges(G.nodes(0)))
    for node_name in node_names:
        if G.edges(node_name):
            connected_device = list(list(zip(*G.edges(node_name)))[1])
            if len(connected_device) > 1:
                connected_device.append(node_name)
                print(connected_device)
                pass
    # print(G.edges())
    exit()

    # subckts = {subckt[0]: subckt[1] for subckt in subckts}
    # pprint(subckts)
    # # main_circuit = [[c, subckts[c]] for c in subckts if main_circuit_name.lower() == c.lower()][0]
    # # if not main_circuit:
    # #     [[c, subckts[c]] for c in subckts if main_circuit_name.lower() in c.lower()][0]
    # subckts.pop(main_circuit_name, None)
    # print(main_circuit)
    netlist_path = "netlist_OP_new copy.txt"  # Change to your SPICE file path

    print("\nComponents and Connections:")

    exit()
    # for line in main_circuit[1].split("\n")[1:]:
    #     if line:
    #         # print(line)
    #         # print(ahkab.netlist_parser.parse_lin)
    #         line = line.strip().split()
    #         device, other, mos = line[0], line[1:4], line[5]
    #         # print(device)
    #         # print(other)
    #         G.add_node(device)
    #         G.add_nodes_from(other)
    # return components


def main():
    netlist_path = "netlist_OP_new copy.txt"  # Change to your SPICE file path
    parse_netlist(netlist_path)


if __name__ == "__main__":
    main()
