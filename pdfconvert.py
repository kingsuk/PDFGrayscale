import os
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path # https://pypi.org/project/pdf2image/
from img2pdf import convert # https://pypi.org/project/img2pdf/

inputpath = 'in/'
outputpath = 'out/'

for dirpath, dirnames, filenames in os.walk(inputpath):
    structure = os.path.join(outputpath, dirpath[len(inputpath):])
    if not os.path.isdir(structure):
        os.mkdir(structure)
    else:
        print("Folder does already exits!")

inputpath = 'in'
outputpath = 'out'
fileList = []
for path, subdirs, files in os.walk(inputpath):
    for name in files:
        fileList.append(os.path.join(path, name))

i = 0
for name in fileList:
    inputFilePath = name
    outputFilePath = name.replace(inputpath, outputpath)
    with TemporaryDirectory() as temp_dir: # Saves images temporarily in disk rather than RAM to speed up parsing
        # Converting pages to images
        #print("Parsing pages to grayscale images. This may take a while")
        images = convert_from_path(
            inputFilePath,
            dpi=151,
            output_folder=temp_dir,
            grayscale=True,
            fmt="jpeg",
            thread_count=4,
            poppler_path = r"C:\Users\kingsuk.majumder\Downloads\Release-21.03.0\poppler-21.03.0\Library\bin"
        )

        image_list = list()
        for page_number in range(1, len(images) + 1):
            path = os.path.join(temp_dir, "page_" + str(page_number) + ".jpeg")
            image_list.append(path)
            images[page_number-1].save(path, "JPEG") # (page_number - 1) because index starts from 0

        with open(outputFilePath, "bw") as gray_pdf:
            gray_pdf.write(convert(image_list))
        i=i+1
        print("current file number ",i," and file name ",inputFilePath)

        #print("The new page is saved as Gray_PDF.pdf in the current directory.")
    