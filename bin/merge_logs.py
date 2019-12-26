#!/usr/bin/env python
import io
import sys

# Some global variables
import xml

from bin.convert_logs import Event

SVN_SEP = "------------------------------------------------------------------------"
CVS_SEP = "----------------------------"


def main(argv):
    output = sys.stdout
    output = open('E:\codebang\merged\log.xml', "w", encoding="utf-8")
    file_list = ['E:\codebang\merged\logA.xml', 'E:\codebang\merged\logB.xml']

    merge_log_file(file_list, output)

    # create_event_xml(file_list, output)

def merge_log_file(file_list, output):
    from xml.dom.minidom import parse
    import xml.dom.minidom

    big_list = []

    # Open XML document using minidom parser
    for file in file_list:
        log_file_DOMTree = xml.dom.minidom.parse(file)
        file_events = log_file_DOMTree.getElementsByTagName('file_events')
        event_nodes = file_events[0].getElementsByTagName('event')
        big_list += event_nodes

    big_list.sort(key=lambda x: x.getAttribute('date'))

    event_list = []
    for big in big_list:
        event_list.append(Event(big.getAttribute('filename'), big.getAttribute('date'), big.getAttribute('author')))

    create_event_xml(event_list, output)

    # debug code
    # for big in big_list:
    #     print(big.getAttribute('date'))

# # Get all the movies in the collection
# movies = collection.getElementsByTagName("movie")
#
# # Print detail of each movie.
# for movie in movies:
#     print ("*****Movie*****")
#     if movie.hasAttribute("title"):
#         print ("Title: %s" % movie.getAttribute("title"))
#
#     type = movie.getElementsByTagName('type')[0]
#     print ("Type: %s" % type.childNodes[0].data)
#     format = movie.getElementsByTagName('format')[0]
#     print ("Format: %s" % format.childNodes[0].data)
#     rating = movie.getElementsByTagName('rating')[0]
#     print ("Rating: %s" % rating.childNodes[0].data)
#     description = movie.getElementsByTagName('description')[0]
#     print ("Description: %s" % description.childNodes[0].data)

def create_event_xml(merged_events, output):
    # Write out the final XML given a list of XML files of certain repos.

    from xml.sax.saxutils import XMLGenerator

    fp = io.BytesIO()
    # generator = XMLGenerator(output, "utf-8")
    generator = XMLGenerator(fp, "utf-8")
    generator.startDocument()
    generator.startElement('file_events', {})

    qnames = {(None, "date"):"date",
              (None, "filename"):"filename",
              (None, "author"):"author"}

    for event in merged_events:
        generator.startElement("event", event.properties())
        generator.endElement("event")


    generator.endElement('file_events')

    generator.endDocument()


    # pretty-print it
    xml_string = fp.getvalue()
    parsed = xml.dom.minidom.parse(io.BytesIO(xml_string))
    output.write(parsed.toprettyxml())
    ## print(pretty_xml)



# Main entry point.
if __name__ == "__main__":
    main(sys.argv)
