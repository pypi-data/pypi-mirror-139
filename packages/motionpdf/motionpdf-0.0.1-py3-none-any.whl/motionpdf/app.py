import argparse
from pathlib import Path
import errno
import os
import glob
from motionpdf.motion import convertPDF


def curate_pdfs(path: Path, o: str, 
                lang: str, lineS: int, verbose: bool) -> None:
    """Find the PDF files the user specified and send them to be converted"""
    o_path = None
    if o != os.getcwd():
        o_path = Path(o)
    else:
        o_path = Path(o + '/text')
    o_path.mkdir(parents=True, exist_ok=True)
        
    n = 0

    directory = path.is_dir()
    if directory:
        print(path)
        search_pdfs = list(glob.glob(str(path) + "/*.pdf")) \
            + list(glob.glob(str(path) + "/*.PDF"))
        search_pdfs = [Path(p) for p in search_pdfs]
        print(search_pdfs)
        n = convertPDF(search_pdfs,
                       o_path, lang, lineS, verbose)
    else:
        if path.suffix.lower() == '.pdf':
            n = convertPDF([path], o_path, lang, lineS, verbose)
        else:
            n = convertPDF([], o_path, lang, lineS, verbose)
    
    if verbose:
        print("Converted {} PDF files!".format(n))


def is_path(path_str: str) -> Path:
    """Type function to make sure a string is an existing path"""
    path = Path(path_str)
    if path.exists():
        return path
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path_str)


def main():
    """Commmand line entry point."""
    parser = argparse.ArgumentParser(description="A script built on "
                                    "Tesseract-OCR for converting .pdf to .txt")
    parser.add_argument('path', help="Path to PDF file(s).", type=is_path)
    parser.add_argument('--verbose', '-v', action='store_true', 
                    help="Print debug information")
    parser.add_argument('--out', '-o', help="Directory to put the resulting "
                    ".txt file(s). Default: [currect directory]", 
                    type=str, default=os.getcwd(), required=False)
    parser.add_argument('--language', '-l', help="Tesseract language code "
                        "(e.g.) 'eng', 'spa', 'fra'. Defaults to 'eng'.",
                        type=str, default='eng', required=False)
    parser.add_argument('--linewidth', '-L', help="Force output to wrap to "
                        "sized lines. Use 0 to try to preserve original lines "
                        "(default is 0)", type=int, default=0, required=False)
    args = parser.parse_args()
    if args.verbose:
        print(args)

    curate_pdfs(args.path, args.out,
                args.language, args.linewidth, args.verbose)


# for local debugging only
if __name__ == '__main__':
    main()
