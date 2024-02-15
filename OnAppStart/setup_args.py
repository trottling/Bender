import argparse


def Setup_args():

    parser = argparse.ArgumentParser(description="Windows Vulnerability Scanner", formatter_class=argparse.ArgumentDefaultsHelpFormatter, epilog='Search for vulnerabilities in your Windows system')

    parser.add_argument("-d", "--debug", action="store_true", default=False, dest="debug", help="Enable debug")
    parser.add_argument("-df", "--debug-file", type=str, default=None, dest="debug_file", help="Enable debug file")

    args = parser.parse_args()
    config = vars(args)
    return config
