import os
import glob
from tqdm import tqdm
from xml.dom import minidom
import json

# Constants:
ANNOTATIONS_PATH = "sample-noncommon-classes/page_annotations/*.xml"

def main():
    print("Generating stats for all files...")
    xml_files = glob.glob(ANNOTATIONS_PATH)
    
    all_files_classnames_stats = {}
    for xml_file in tqdm(xml_files, desc="XML Files"):
    # Parse XML Document
        xmldoc = minidom.parse(xml_file)

        nodes = xmldoc.getElementsByTagName("Node")

        for node in nodes:
        # Classname
            node_classname = node.getElementsByTagName("ClassName")[0]
            node_classname_str = node_classname.firstChild.data 

            if node_classname_str not in all_files_classnames_stats.keys():
                all_files_classnames_stats[node_classname_str] = 0
            all_files_classnames_stats[node_classname_str] += 1

    with open("classname_stats.json", 'w') as fp:
        json.dump(all_files_classnames_stats, fp)
        
if __name__ == "__main__":
    main()