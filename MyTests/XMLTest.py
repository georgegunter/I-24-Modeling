from lxml import etree
E = etree#.Element
import xml.etree.ElementTree as ET
from flow.core.util import makexml, printxml, ensure_dir

file = "/home/mesto/flow/MyTests/I24-62.add.xml"
tree = E.parse(file)
if __name__ == "__main__":
    root = tree.getroot()
    #tree.append(file)
    add = makexml('additional',
                      'http://sumo.dlr.de/xsd/additional_file.xsd')
    for child in root:
        add.append(child)
    #add.append(E('flow', id = 'Test'))
    printxml(add, "/home/mesto/flow/MyTests/test.xml")