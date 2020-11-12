
import os
import glob
from tqdm import tqdm
from xml.dom import minidom
from PIL import Image
import numpy as np

# Constants:
ANNOTATIONS_PATH = "/page_annotations/*.xml"
IMGS_PATH = "/sample-noncommon-classes/images"

def main():
    print("Sampling DOREMI non-common images...")

    # Define which ClassNames we want to sample
    # For example, we might not want noteheadBlack since it's very common
    to_be_sampled = ["accidentalDoubleFlat"]

    to_be_sampled_index = {}
    # Dictionary to keep the current index 
    # (We might have accidentalSharp_1, accidentalSharp_2,...accidentalSharp_n)
    # We can start at 0 or 1
    for classname in to_be_sampled:
        to_be_sampled_index[classname] = 1

    # Now try to fund to find items in "to_be_sampled" in the XML file and corresponding image
    xml_files = glob.glob(ANNOTATIONS_PATH)
    
    for xml_file in tqdm(xml_files, desc="XML Files"):
        filename = os.path.basename(xml_file)
        # Remove .xml from end of file
        filename = filename[:-4]

        # Parse XML Document
        xmldoc = minidom.parse(xml_file)

        # Get image name from XML file name
        page = xmldoc.getElementsByTagName("Page")
        page_index_str = page[0].attributes["pageIndex"].value
        # Here we add 1 because dorico XML starts pageIndex at 0, but when exporting to image it starts with 1
        # THERE MIGHT BE SOME EXCEPTIONS
        # For ex: Au Tombeau de Rachmanimoff exports a page 0 which is EMPTY and needs to be discarded
        page_index_int = int(page_index_str) + 1
        # Open image related to XML file
        # Parsed_Winstead - Cygnus, The Swan-layout-0-muscima_Page_3.xml
        # Winstead - Cygnus, The Swan-001
        # Also remove "layout-0-muscima_Page_" (22 chars) + len of page_index_str
        ending = 22 + len(str(page_index_int))
        # If page is 0, we need to add "000"
        leading_zeroes = str(page_index_int).zfill(3)
        img_filename = filename[7:-ending]+leading_zeroes
        img_path = IMGS_PATH + "/" + img_filename + ".png"
        img = Image.open(img_path)
        img_arr = np.array(img)

        nodes = xmldoc.getElementsByTagName("Node")
        for node in nodes:
            # Classname
            node_classname = node.getElementsByTagName("ClassName")[0]
            node_classname_str = node_classname.firstChild.data 
            # Top
            node_top = node.getElementsByTagName("Top")[0]
            node_top_int = int(node_top.firstChild.data)
            # Left
            node_left = node.getElementsByTagName("Left")[0]
            node_left_int = int(node_left.firstChild.data)
            # Width
            node_width = node.getElementsByTagName("Width")[0]
            node_width_int = int(node_width.firstChild.data)
            # Height
            node_height = node.getElementsByTagName("Height")[0]
            node_height_int = int(node_height.firstChild.data)

            # If we want to sample this class, cut it from the image
            if node_classname_str in to_be_sampled:
                class_arr = img_arr[node_top_int:node_top_int+node_height_int,node_left_int:node_left_int+node_width_int]
                I = class_arr
                I8 = (((I - I.min()) / (I.max() - I.min())) * 255.9).astype(np.uint8)
                class_image = Image.fromarray(I8)
                sample_index = str(to_be_sampled_index[node_classname_str])
                class_image.save("samples/sample"+node_classname_str+"_"+sample_index+".jpeg")
                to_be_sampled_index[classname] += 1

            # Uncomment below to test the first classname and then break execution 
            # class_arr = img_arr[node_top_int:node_top_int+node_height_int,node_left_int:node_left_int+node_width_int]
            # I = class_arr
            # I8 = (((I - I.min()) / (I.max() - I.min())) * 255.9).astype(np.uint8)
            # class_image = Image.fromarray(I8)
            # class_image.save("class_image.jpeg")
            # break
        # break



if __name__ == "__main__":
    main()