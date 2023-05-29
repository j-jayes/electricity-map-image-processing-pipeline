# Electricity Map Image Processing Pipeline

## Scope

**Project Title: Preprocessing of Historical Document Scans for OCR Processing** 

**Objective** : Develop a software solution that can take scanned pages of tables from historical documents (PDFs), crop them to the table area, perform image correction and stitching operations, and finally export the processed image to be ready for OCR (Optical Character Recognition) API processing.

**Job Description:**  
1. **Image Extraction and Cropping** : The software must be able to extract individual pages from the PDF files and identify the table area on each page. This may involve detecting the boundaries of the table and cropping out the surrounding blank space, titles, and page numbers. This will likely require techniques in computer vision, possibly edge detection or similar algorithms. 
2. **Image Correction** : After the table area is isolated, the software must be capable of performing image corrections. This includes straightening (deskewing) and dewarping the image to ensure it is as flat and straight as possible for the OCR processing. This might involve using OpenCV or similar libraries. 
3. **Image Stitching** : The software must then stitch together the left and right halves of the table from successive pages. This will require identifying matching sections of the table across pages and joining them together in a seamless manner. 
4. **Image Export** : After the tables are stitched together, the software must export the resulting image in a format that can be processed by an OCR API.

**Skills Required** :
- Strong proficiency in a programming language such as Python
- Familiarity with libraries for working with PDFs (like PyPDF2, PDFMiner)
- Strong experience with image processing libraries (like OpenCV, PIL/Pillow)
- Experience with computer vision techniques, including image segmentation, edge detection, and image transformations
- Familiarity with OCR technologies and their requirements
- Strong problem-solving skills and attention to detail
- Ability to work independently and propose solutions based on requirements

**Deliverable** : A software solution, preferably a well-documented script or application, which can perform the above tasks. It should be able to take a PDF as input and output an image file that is ready for OCR processing.

This project will require both an understanding of the technical aspects and a bit of creativity to deal with the unique challenges that come with processing historical document scans.


## File structure

project_root/
    |--- .gitignore
    |--- README.md
    |--- requirements.txt
    |--- src/
    |     |--- __init__.py
    |     |--- pdf_to_image.py
    |     |--- image_crop.py
    |     |--- image_dewarp.py
    |     |--- image_stitch.py
    |--- test/
    |     |--- __init__.py
    |     |--- test_pdf_to_image.py
    |     |--- test_image_crop.py
    |     |--- test_image_dewarp.py
    |     |--- test_image_stitch.py
    |--- data/
          |--- input/
          |     |--- pdfs/
          |--- intermediate/
          |     |--- images/
          |     |--- cropped_images/
          |     |--- dewarped_images/
          |--- output/
                |--- stitched_images/


### What do we care about in the tables?

1. Name of power station
2. Location of power station
3. Source of power.
4. Amount of power generated (kVA)

1. name
2. location
3. source
4. amount