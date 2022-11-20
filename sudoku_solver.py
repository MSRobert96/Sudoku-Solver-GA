'''
This is a terminal wrapper for sudoku_solver_ga.
Use this if you want to use the program from terminal.
'''

import argparse
import re
import time
from sudoku_solver_ga import Population

PROGRAM_NAME = 'Sudoku solver'
PROGRAM_AUTHOR = 'Roberto Milan'
PROGRAM_VERSION = '0.0.1'
PROGRAM_EPILOG = '''README:
The sudoku must be 81 characters long (whitespaces are ignored).
Any non 1-9 character will count as a blank cell, represented internally as a dot '.' .
'''


def main():
    params, terminal = init_terminal()
    sudoku: str = load_sudoku(params)

    time_start = time.monotonic_ns()
    p = Population(sudoku)
    solution = p.solve()
    time_elapsed = time.monotonic_ns() - time_start

    output(sudoku, solution, params['output'])
    print(f'Elapsed time : {time_elapsed/1000000000:.5f} s')

    terminal.exit(0)


def format_sudoku(string: str) -> str:
    '''Formats sudoku in a human readable format'''
    return (
        '+-------+-------+-------+\n'
        '| {} {} {} | {} {} {} | {} {} {} |\n'
        '| {} {} {} | {} {} {} | {} {} {} |\n'
        '| {} {} {} | {} {} {} | {} {} {} |\n'
        '+-------+-------+-------+\n'
        '| {} {} {} | {} {} {} | {} {} {} |\n'
        '| {} {} {} | {} {} {} | {} {} {} |\n'
        '| {} {} {} | {} {} {} | {} {} {} |\n'
        '+-------+-------+-------+\n'
        '| {} {} {} | {} {} {} | {} {} {} |\n'
        '| {} {} {} | {} {} {} | {} {} {} |\n'
        '| {} {} {} | {} {} {} | {} {} {} |\n'
        '+-------+-------+-------+\n'
    ).format(*string)

def load_sudoku(params: dict) -> str:
    '''Loads a sudoku as a 81-character string'''
    sudoku = load_sudoku_from_file(params['sudoku']) if params['file'] else params['sudoku']
    sudoku = re.sub(r'\s', '', sudoku)
    sudoku = re.sub(r'[^1-9]', '0', sudoku)
    return sudoku


def load_sudoku_from_file(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


def init_terminal():
    '''Load command line helper'''
    terminal = argparse.ArgumentParser(
        prefix_chars='-/',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'{PROGRAM_NAME} by {PROGRAM_AUTHOR}',
        epilog=f'{PROGRAM_EPILOG}'
    )
    terminal.add_argument('sudoku', type=str, help='String representing the sudoku', )
    terminal.add_argument('-f', '--file', action='store_true', help='Treat input as path to sudoku file')
    terminal.add_argument('-o', '--output', type=str, help='Specify path of solution file')
    terminal.add_argument('-v', '--verbose', action='store_true', help='Verbose (more output)', )
    return vars(terminal.parse_args()), terminal


def output(sudoku: str, solution: str, output_path: str):
    '''Outputs the solved sudoku to termina or to a file'''

    if solution:
        output = 'Found a solution to this sudoku: \n\n{}\nSOLUTION:\n\n{}'.format(format_sudoku(sudoku), format_sudoku(solution))
    else:
        output = 'Your input is not valid or it does not have any solution.'

    if(output_path):
        with open(output_path, 'w') as f:
            f.write(output)
    else:
        print(output)


if __name__ == '__main__':
    main()
