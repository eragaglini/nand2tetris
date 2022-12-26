from xml.dom import minidom
import xml.etree.cElementTree as ET


def generate_xml_file(root, outFilename):

    """
    this works, but doesn't format the xml file in a way compliant to nand2tetris
    specifications

    xmlstr = minidom.parseString(ET.tostring(self.root)).toprettyxml(
        indent="   "
    )
    with open(outFilename, "w") as f:
        f.write(xmlstr)
    """

    # for nand2tetris we do like this:
    # https://stackoverflow.com/questions/16813938/python-print-pretty-xml-create-opening-and-closing-tags-for-empty-tags-text

    t = minidom.parseString(ET.tostring(root))

    def patcher(method):
        def patching(self, *args, **kwargs):
            old = self.childNodes
            try:
                if not self.childNodes:

                    class Dummy(list):
                        def __nonzero__(self):  # Python2
                            return True

                        def __bool__(self):  # Python3
                            return True

                    old, self.childNodes = self.childNodes, Dummy([])
                return method(self, *args, **kwargs)
            finally:
                self.childNodes = old

        return patching

    t.firstChild.__class__.writexml = patcher(t.firstChild.__class__.writexml)
    # childNodes[0] to omit the xml declaration
    xmlstr = t.childNodes[0].toprettyxml(indent="   ")

    with open(outFilename, "w") as f:
        f.write(xmlstr)

    # replace ampersand characters:
    # read input file
    with open(outFilename, "rt") as fin:
        # read file contents to string
        data = fin.read()
        # replace all occurrences of the required string
        data = (
            data.replace("&amp;lt;", "&lt;")
            .replace("&amp;amp;", "&amp;")
            .replace("&amp;gt;", "&gt;")
        )
    # open the input file in write mode
    with open(outFilename, "wt") as fin:
        # overrite the input file with the resulting data
        fin.write(data)
