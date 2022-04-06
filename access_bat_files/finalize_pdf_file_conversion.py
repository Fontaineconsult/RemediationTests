import sys, os


def run():
    finalize_pdf_file_conversion(int(sys.argv[1]))


if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    from job_scripts import finalize_pdf_file_conversion
    run()