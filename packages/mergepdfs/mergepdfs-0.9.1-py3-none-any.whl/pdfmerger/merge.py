from PyPDF2 import PdfFileMerger
import sys
import glob
import warnings

warnings.filterwarnings("ignore")

     
def merge(pdfs: list, outgoing_pdf: str):
    merger = PdfFileMerger()

    for pdf in pdfs:
        try:
            merger.append(pdf)
        except:
            print("Error {} occured when trying to add the file {} to the merger. Skips this file".format(sys.exc_info()[0], pdf))
            continue

    merger.write(outgoing_pdf)
    merger.close()


def main():
    if len(sys.argv) == 1:
        print('ERROR: Please write the files you wish to merge followed by the name of the new file. Remember to write the file with the type (ex.pdf)')
        exit()

    if sys.argv[1] == '*':
        pdfs = glob.glob('*.pdf')

        if len(pdfs) == 0:
            print('ERROR: There is no pdfs in this folder')

    else:
        pdfs = sys.argv[1:-1]

    outgoing_pdf = sys.argv[-1]
    merge(pdfs, outgoing_pdf)

 
if __name__ == '__main__':
    main()