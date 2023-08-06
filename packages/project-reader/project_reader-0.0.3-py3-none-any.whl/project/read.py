import os
import argparse

from .folder_reader import kill_project, print_statement
from .folder_visualizer import assign_classes, draw
from .folder_summary import summarize_pr, f_types

par = argparse.ArgumentParser()
par.add_argument("path", type=str, help="Path of the project to read")
par.add_argument("--ignore", type=str, help="Comma separated string of folders to ignore")
par.add_argument("--output", type=str, help="Name of file to write the output to")
args = par.parse_args()
path = args.path

# ignore folders
ignore = []
if args.ignore:
    ignore = [fol.strip() for fol in args.ignore.split(",")]

# output file
outfile = None
if args.output:
    outfile = args.output
    if not outfile.split(".")[-1] == "txt":
        outfile = None


def main(project_path, **kwargs):
    print("NOW READING")
    # load file types from data.json
    os.chdir("\\".join(__file__.split("\\")[:-1]))
    files_dict = f_types
    # go to folder
    os.chdir(project_path)

    file = print_statement(
        kill_project(os.getcwd(), ignore=kwargs.get('ignore', []))
    )

    klasses = assign_classes(file)
    summarize_pr(klasses, files_dict)
    try:
        file_name = kwargs['output_file']
        if file_name:
            draw(klasses, file_name=file_name)
        else:
            draw(klasses)
    except KeyError:
        draw(klasses)

    print("DONE READING")


main(path, ignore=ignore, output_file=outfile)
