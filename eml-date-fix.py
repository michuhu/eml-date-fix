import argparse
import email.policy
import os.path
import datetime
import sys

from dateutil import parser
from email.parser import BytesHeaderParser
from email.errors import MissingHeaderBodySeparatorDefect
import glob


def arg_parser(arguments):
    argparser = argparse.ArgumentParser(arguments)
    argparser.add_argument("eml_folder", help="Folder with eml files")
    return argparser


def parse_str_to_datetime(data_str, ignoretz=False):
    return parser.parse(data_str, fuzzy=True, ignoretz=ignoretz).strftime("%d/%m/%Y %H:%M:%S %z")


def eml_chg_date(folder):
    """
    This script takes all *.eml files from eml_folder (input),
    fixes the dates to one standard format: %d/%m/%Y %H:%M:%S %z
    and places them in (input)/fixed folder.
    """
    x, y = 0, 0
    new_policy = email.policy.compat32.clone(raise_on_defect=True)

    if not glob.glob(args.eml_folder + "/*.eml"):
        sys.exit("No .eml files here")

    try:
        os.mkdir(folder + "/fixed")
    except FileExistsError:
        print("Folder ""fixed"" exists... continuing")
        pass

    print("EML DATE FIXER STARTS")

    for file in glob.glob(folder + "/*.eml"):
        with open(file, "rb") as fp:
            try:
                msg = BytesHeaderParser(policy=new_policy).parse(fp)
            except MissingHeaderBodySeparatorDefect:
                print("MissingHeaderBodySeparatorDefect : fixing : " + fp.name)
                # return to the first byte of fp
                fp.seek(0)
                fp_corrected = fp.read().replace(b"\r", b" ")
                msg = BytesHeaderParser().parsebytes(fp_corrected)

            try:
                date_parsed = parse_str_to_datetime(msg.get("Date"))

            except parser.ParserError:
                print("ParseError: Date: fixing : " + fp.name)
                date_parsed = msg.get("Date").split(" ")[:-1]
                date_parsed = " ".join(date_parsed)
                date_parsed = parse_str_to_datetime(date_parsed)

            except ValueError:
                date_parsed = parse_str_to_datetime(msg.get("Date"), True)

            except Exception as error:
                with open("logs.txt", 'a') as fl:
                    fl.write(str(datetime.datetime.now()) + " " + fp.name + ": " + type(error).__name__ + str(
                        error.args) + "\n")
                    continue

            msg.replace_header("Date", date_parsed)
            y += 1

            mail_fixed = os.path.join(folder + "/fixed", os.path.basename(file))
            with open(mail_fixed, 'wb') as fp2:
                fp2.write(msg.as_bytes())

    print("DATES FIXED: ", y)
    print("FILES in root folder: ", len(os.listdir(folder)) - 1)  # minus fixed folder
    print("FILES in fixed folder: ", len(os.listdir(folder + "/fixed")))


if __name__ == '__main__':

    print(eml_chg_date.__doc__)
    argparser = arg_parser(sys.argv)
    args = argparser.parse_args()

    eml_chg_date(args.eml_folder)
