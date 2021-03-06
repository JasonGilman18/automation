#!/Users/jasongilman/.local/share/virtualenvs/project-open-69beT2u5/bin/python
import argparse
import dill
import os


def main():
    parser = argparse.ArgumentParser(description="open a project")
    parser.set_defaults(which="none")
    subparsers = parser.add_subparsers(help="command help")

    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "popen.data")
    project_names = []
    try:
        projects_file = open(filename, "rb")
        projects = dill.load(projects_file)
        project_names = projects.keys()
    except OSError:
        if os.path.exists(filename):
            os.sys.exit("could not open projects file")

    open_parser = subparsers.add_parser('open')
    if len(project_names) == 0:
        open_parser.add_argument(dest='name', action="store", type=str, help="name of the project to open")
    else:
        open_parser.add_argument(dest='name', choices=project_names, action="store", type=str, help="name of the project to open")
    open_parser.set_defaults(which="open")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument(dest="name", action="store", type=str, help="name of the new project")
    add_parser.set_defaults(which="add")

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(which="list")

    args = parser.parse_args()
    
    if args.which == "open":
        open_project(args.name)
    elif args.which == "add":
        add_project(args.name)
    elif args.which == "list":
        list_projects(project_names)
    else:
        print("should do open or add")


def list_projects(project_names):
    if len(project_names) == 0:
        print("\nNo saved projects")
    else:
        print("SAVED PROJECTS\n")
        print("=================\n")
        for name in project_names:
            print(name, "\n")


def add_project(name):
    print("\nADDING PROJECT: {}\n".format(name))
    print("add programs/files/folders to open\n")
    print("=====================\n")

    program_file_tuples = []
    more_files = True
    while more_files:
        program_path = str(input("Program Path: "))
        file_path = str(input("File/Folder path: "))
        program_file_tuples.append((program_path, file_path))
        more_check = str(input("Add more programs/files/folders? (y/n) "))
        if more_check != "y" and more_check != "Y":
            more_files = False
        else:
            print("\n")

    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "popen.data")
    try:
        projects_file = open(filename, "rb")
        projects_dict = dill.load(projects_file)
        projects_file.close()
        projects_dict[name] = program_file_tuples
        projects_file = open(filename, "wb")
        dill.dump(projects_dict, projects_file)
        projects_file.close()
    except OSError:
        if os.path.exists(filename):
            os.sys.exit("could not save new project")
        else:
            projects_file = open(filename, "wb")
            projects_dict = {name: program_file_tuples}
            dill.dump(projects_dict, projects_file)
            projects_file.close()


def open_project(name):
    filename =os.path.join(os.path.dirname(os.path.abspath(__file__)), "popen.data")
    projects_dict = dill.load(open(filename, "rb"))
    program_file_tuples = projects_dict[name]
    for tuple in program_file_tuples:
        os.system('open -a \"{}\" \"{}\"'.format(get_path(tuple[0]), get_path(tuple[1])))
    

def get_path(path):
    path_list = path.split("/")
    for i in range(len(path_list)):
        index = path_list[i].find("\ ")
        while index != -1:
            path_list[i] = path_list[i].replace(path_list[i][index:index+2], " ")
            index = path_list[i].find("\ ")
    if path[0] == "/":
        return os.path.join("/", *path_list)
    else:
        return os.path.join(*path_list)


if __name__ == "__main__":
    main()