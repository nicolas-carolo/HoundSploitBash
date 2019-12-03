from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.models import Exploit, Shellcode
import os, sys
from tabulate import tabulate
from HoundSploit.console_manager.colors import W, O, R, G
from HoundSploit.searcher.engine.updates import is_db_update_available, is_hs_update_available, download_update, install_exploitdb_update,\
    get_latest_db_update_date
from shutil import copyfile
from HoundSploit.searcher.engine.string import get_vulnerability_extension


# Software information constants
SW_VERSION = '1.7.1'
RELEASE_DATE = '2019-12-03'
DEVELOPER = 'Nicolas Carolo'
LATEST_DB_UPDATE = get_latest_db_update_date()
LATEST_HS_COMMIT = "1.7.1: New directory for organizing files"


def print_guide():
    print_ascii_art('hsploit')
    print(O + 'USAGE:' + W)
    print(tabulate([[G + 'Perform a search' + W, 'hsploit "[search text]"'],
                    [G + 'Perform a search (without keywords highlighting)' + W,
                     'hsploit --nokeywords "[search text]"'],
                    [G + 'Perform a search (no table for results)' + W, 'hsploit --notable "[search text]"'],
                    [G + 'Show info about the exploit' + W, 'hsploit -ie [exploit\'s id]'],
                    [G + 'Show info about the shellcode' + W, 'hsploit -is [shellcode\'s id]'],
                    [G + 'Open the exploit\'s source code with nano' + W, 'hsploit -oe [exploit\'s id]'],
                    [G + 'Open the shellcode\'s source code with nano' + W,
                    'hsploit -os [shellcode\'s id]'],
                    [G + 'Copy the exploit\'s file into a chosen file or directory' + W,
                    'hsploit -cpe [exploit\'s id] [file or directory]'],
                    [G + 'Copy the shellcode\'s file into a chosen file or directory' + W,
                    'hsploit -cps [shellcode\'s id] [file or directory]'],
                    [G + 'Show software information' + W, 'hsploit -v'],
                    [G + 'Check for software updates' + W, 'hsploit -u'],
                    [G + 'Check for database updates' + W, 'hsploit -udb'],
                    [G + 'Show help' + W, 'hsploit -help']],
                   [R + 'ACTION' + W, R + 'COMMAND LINE' + W], tablefmt='grid'))
    exit(0)


def print_software_information():
    print_ascii_art('hsploit')
    print(tabulate([[O + 'Version:' + W, SW_VERSION],
                    [O + 'Release date:' + W, RELEASE_DATE],
                    [O + 'Developer:' + W, DEVELOPER],
                    [O + 'Latest Database update:' + W, LATEST_DB_UPDATE]], tablefmt='grid'))
    exit(0)


def open_exploit(id):
    """
    Open the exploit identified by the id.
    :param id: the exploit's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(Exploit.id == id)
    session.close()
    try:
        vulnerabilities_path = os.path.split(sys.executable)[0] + "/HoundSploit/vulnerabilities/"
        os.system('nano ' + vulnerabilities_path + queryset[0].file)
    except IndexError:
        print('ERROR: Exploit not found!')
    return exit(0)


def open_shellcode(id):
    """
    Open the shellcode identified by the id.
    :param id: the shellcode's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(Shellcode.id == id)
    session.close()
    try:
        vulnerabilities_path = os.path.split(sys.executable)[0] + "/HoundSploit/vulnerabilities/"
        os.system('nano ' + vulnerabilities_path + queryset[0].file)
    except IndexError:
        print('ERROR: Shellcode not found!')
    return exit(0)


def show_exploit_info(id):
    """
    Show the information about the exploit identified by the id.
    :param id: the exploit's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(Exploit.id == id)
    session.close()
    try:
        exploit = queryset[0]
        if exploit.port:
            print(tabulate([[O + 'DESCRIPTION:' + W, exploit.description], [O + 'AUTHOR:' + W, exploit.author],
                            [O + 'FILE:' + W, exploit.file], [O + 'DATE:' + W, exploit.date],
                            [O + 'TYPE:' + W, exploit.type], [O + 'PLATFORM:' + W, exploit.platform],
                            [O + 'PORT:' + W, exploit.port]], tablefmt='grid'))
        else:
            print(tabulate([[O + 'DESCRIPTION:' + W, exploit.description], [O + 'AUTHOR:' + W, exploit.author],
                            [O + 'FILE:' + W, exploit.file], [O + 'DATE:' + W, exploit.date],
                            [O + 'TYPE:' + W, exploit.type], [O + 'PLATFORM:' + W, exploit.platform]], tablefmt='grid'))
    except IndexError:
        print('ERROR: Exploit not found!')
    return exit(0)


def show_shellcode_info(id):
    """
    Show the information about the shellcode identified by the id.
    :param id: the shellcode's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(Shellcode.id == id)
    session.close()
    try:
        shellcode = queryset[0]
        print(tabulate([[O + 'DESCRIPTION:' + W, shellcode.description], [O + 'AUTHOR:' + W, shellcode.author],
                        [O + 'FILE:' + W, shellcode.file], [O + 'DATE:' + W, shellcode.date],
                        [O + 'TYPE:' + W, shellcode.type], [O + 'PLATFORM:' + W, shellcode.platform]], tablefmt='grid'))
    except IndexError:
        print('ERROR: Shellcode not found!')
    return exit(0)


def print_ascii_art(text_to_print):
    from colorama import init
    init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
    from termcolor import cprint
    from pyfiglet import figlet_format

    cprint(figlet_format(text_to_print, font='starwars'),
           'yellow', attrs=['bold'])


def check_for_updates():
    if is_hs_update_available(LATEST_HS_COMMIT):
        print('A new software update is available!')
        choice = input('Do you want to download it? (Y/N): ')
        if choice.upper() == 'Y' or choice.upper() == 'YES':
            download_update()
        elif choice.upper() == 'N' or choice.upper() == 'NO':
            exit(0)
        else:
            print('ERROR: Bad input! Choose yes (Y) or no (N)')
            check_for_updates()
    else:
        print('The software is up-to-date!')
    exit(0)


def check_for_exploitdb_updates():
    latest_db_update_path = os.path.split(sys.executable)[0] + "/HoundSploit/etc/latest_exploitdb_commit.txt"
    if is_db_update_available(latest_db_update_path):
        print('A new database update is available!')
        choice = input('Do you want to download and install it? (Y/N): ')
        if choice.upper() == 'Y' or choice.upper() == 'YES':
            install_exploitdb_update(os.path.split(sys.executable)[0])
        elif choice.upper() == 'N' or choice.upper() == 'NO':
            exit(0)
        else:
            print('ERROR: Bad input! Choose yes (Y) or no (N)')
            check_for_updates()
    else:
        print('The database is up-to-date!')
    exit(0)


def copy_exploit(id, dst):
    """
    Copy the exploit identified by the id into the destination specified by the user.
    :param id: the exploit's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(Exploit.id == id)
    session.close()
    try:
        vulnerabilities_path = os.path.split(sys.executable)[0] + "/HoundSploit/vulnerabilities/"
        src = vulnerabilities_path + queryset[0].file
        try:
            copyfile(src, dst)
        except IsADirectoryError:
            if src[-1:] == '/':
                dst = dst + queryset[0].id + get_vulnerability_extension(queryset[0].file)
            else:
                dst = dst + '/' + queryset[0].id + get_vulnerability_extension(queryset[0].file)
            copyfile(src, dst)
    except IndexError:
        print('ERROR: Exploit not found!')
    return exit(0)


def copy_shellcode(id, dst):
    """
    Copy the shellcode identified by the id into the destination specified by the user.
    :param id: the shellcode's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(Shellcode.id == id)
    session.close()
    try:
        vulnerabilities_path = os.path.split(sys.executable)[0] + "/HoundSploit/vulnerabilities/"
        src = vulnerabilities_path + queryset[0].file
        try:
            copyfile(src, dst)
        except IsADirectoryError:
            if src[-1:] == '/':
                dst = dst + queryset[0].id + get_vulnerability_extension(queryset[0].file)
            else:
                dst = dst + '/' + queryset[0].id + get_vulnerability_extension(queryset[0].file)
            copyfile(src, dst)
    except IndexError:
        print('ERROR: Exploit not found!')
    return exit(0)