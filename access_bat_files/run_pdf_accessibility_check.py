import sys, os


def run():
    print("SDKLFGHSDLKFJSDLKFJLSKDJFLKSDJFLKSDJFLKDSMVLKDMSV")
    pdf_accessibility_check(int(sys.argv[1]), sys.argv[2])


if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    from job_scripts import pdf_accessibility_check
    run()