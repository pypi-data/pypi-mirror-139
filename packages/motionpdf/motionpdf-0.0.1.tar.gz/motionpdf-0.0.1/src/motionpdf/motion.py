from os import mkdir
from typing import List
from pathlib import Path
from pdf2image import convert_from_path
from datetime import datetime
import textwrap
import shutil
import traceback
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import glob

def convertPDF(files: List[Path], outdir: Path, 
               lang: str, lineS: int, verbose: bool) -> int:
    """Convert the list of PDF files to corresponding .txt files"""
    if len(files) == 0:
        if verbose:
            print("No PDF files found. Quitting.")
        return 0
    sucessfully_processed = 0
    try:
        # create image directory
        now = datetime.now()
        image_dir = Path(outdir / 
            ("images" + now.strftime("%Y%m%d%H%M%S"))) 
        image_dir.mkdir()
        for pdf in files:
            images = convert_from_path(pdf)
            # create directory for this PDF file
            this_pdf_dir = Path(image_dir / str(pdf.stem))
            this_pdf_dir.mkdir()
            # convert all files to jpegs
            img_paths = [] 
            for i in range(len(images)):
                imgp = str(this_pdf_dir) + "/page" + str(i) + ".jpg"
                images[i].save(imgp, "JPEG")
                img_paths.append(imgp)
            # read text to memory
            text = []
            for i in range(len(img_paths)):
                image = Image.open(img_paths[i])
                # double the image size to try and improve accuracy
                w, h = image.size
                image = image.resize((w * 2, h * 2), Image.BOX)
                page_text = pytesseract.image_to_string(image, 
                                                        lang=lang)
                text.append((i, page_text))
            # write read text to disk
            outfile_path = str(Path(outdir / (str(pdf.stem) + ".txt")))
            with open(outfile_path, "+w") as outfile:
                for line in text:
                    outfile.write("Page {}\n".format(line[0] + 1))
                    if lineS == 0:
                        outfile.write("{}\n\n".format(line[1]))
                    else:
                        wrapped = textwrap.fill(line[1], width=lineS)
                        outfile.write("{}\n\n".format(wrapped))
            # if not verbose, delete images
            if not verbose:
                shutil.rmtree(image_dir)
            # if verbose, print cute little dot, for we have successfully
            # outputted a single page
            if verbose:
                print(".")
            # increment success counter
            sucessfully_processed += 1
    except Exception as e:
        if verbose:
            traceback.print_exc()
            print(e.with_traceback)
        else:
            print(e)
        return sucessfully_processed
    return sucessfully_processed
