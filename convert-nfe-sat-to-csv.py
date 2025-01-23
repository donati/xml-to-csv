import os
import xml.etree.ElementTree as ET
import csv

def process_xml_files(directory, output_csv, static_tags, product_tags):
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Combine static and product tags for the header
        header = static_tags + product_tags
        csvwriter.writerow(header)

        for filename in os.listdir(directory):
            if filename.endswith('.xml'):
                filepath = os.path.join(directory, filename)
                try:
                    tree = ET.parse(filepath)
                    root = tree.getroot()

                    # Extract static tags (nCFe, dEmi, hEmi)
                    static_data = []
                    for tag in static_tags:
                        element = root.find(f".//{tag}")
                        static_data.append(element.text if element is not None else "")

                    # Process each <det> block for product tags
                    for det in root.findall(".//det"):
                        product_data = []
                        for tag in product_tags:
                            element = det.find(f".//{tag}")
                            product_data.append(element.text if element is not None else "")
                        
                        # Write a row combining static and product data
                        csvwriter.writerow(static_data + product_data)
                
                except ET.ParseError as e:
                    print(f"Error parsing {filename}: {e}")

if __name__ == "__main__":
    # Input directory
    input_directory = input("Enter the directory containing XML files: ").strip()
    output_file = "output.csv"

    # Static and product tags
    static_tags = ['nCFe', 'dEmi', 'hEmi']  # Tags appearing once per file
    product_tags = ['xProd', 'qCom', 'vUnCom', 'vProd']  # Tags appearing per product

    process_xml_files(input_directory, output_file, static_tags, product_tags)
    print(f"CSV file '{output_file}' created successfully!")