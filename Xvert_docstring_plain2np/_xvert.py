# ----------------------------------------------------------------------------
# Copyright (c) 2020, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pkg_resources

ROOT = pkg_resources.resource_filename('Xvert_docstring_plain2np', '.')


def get_files_with_plain_docstring(folder: str) -> dict:
    """
    Get the code files containing docstring to convert from
    plain to NumPy format.

    Parameters
    ----------
    folder : str
        Name of the code_base to screen for files into.
    Returns
    -------
    files_to_convert : dict
        Input files containing docstring to convert from
        plain to NumPy format and their output file name.
    """
    files_to_convert = {}
    for root, dirs, files in os.walk(folder):
        for fil in files:
            if fil.endswith('.py') and not fil.endswith('xverted.py'):
                path = root + '/' + fil
                with open(path) as f:
                    for line in f:
                        if ':param' in line:
                            break
                    else:
                        continue
                    files_to_convert[path] = '%s_xverted.py' % path
    return files_to_convert


def parse_definition(line: str) -> tuple:
    """
    Parse function definition line to get:
    - input_types_default for each argument
    - output_type for the function

    Parameters
    ----------
    line: str
        A function definition code line.
    Returns
    -------
    Two dicts:
        input_types_default: dict
            function input argument -> (type value, default value)
        output_types: list
            type(s) of the function output(s)
    """
    function_args_line = '('.join(line.split('def ')[-1].split('(')[1:])

    output_types = []
    if '->' in function_args_line:
        output_type = function_args_line.split('->')[-1].split(':')[0].strip()
        function_args_line = ')'.join(function_args_line.split('->')[0].strip().split(')')[:-1])
        if ',' in output_type:
            for out in output_type.split(','):
                output_types.append(out.strip())
        else:
            output_types.append(output_type)

    input_types_default = {}
    function_args = [x.strip() for x in function_args_line.split(',')]
    for function_arg__ in function_args:
        if '=' in function_arg__:
            default = function_arg__.split('=')[-1].strip()
            function_arg_ = function_arg__.split('=')[0].strip()
        else:
            default = None
            function_arg_ = function_arg__
        if ':' in function_arg_:
            arg_type = function_arg_.split(':')[-1].strip()
            function_arg = function_arg_.split(':')[0].strip()
        else:
            arg_type = None
            function_arg = function_arg_
        input_types_default[function_arg] = (arg_type, default)
    return input_types_default, output_types


def convert_file(input: str) -> (dict, dict):
    """
    Convert the input .py file containing plain docstring
    into output .py.xvrted file containing NumPy docstring.
    output: str
        Output .py.xvrted file containing NumPy docstring.
    """
    return 0


def make_output_docstrings(functions: dict, docstrings: dict) -> tuple:
    """
    Make the NumPy docstrings lines to write
    instead of the current plain docstring per function.

    Parameters
    ----------
    functions: dict
        Input types and default, and output type per function name.
    docstrings: dict
        Docstring Header, Parameters and Returns info per function name.
    Returns
    -------
    output_docstrings: dict
        Docstrings in NumPy format per function name.
    output_checks: dict
        function and output(s) of the functions that pose problem.
    """
    output_checks = {}
    output_docstrings = {}
    for function, attributes in functions.items():

        if function not in docstrings:
            continue

        output_docstrings[function] = '    """\n'

        header = docstrings[function]['header']
        for h in header:
            output_docstrings[function] += '    %s\n' % h

        input_types_default = attributes['input_types_default']
        params = docstrings[function]['params']
        if params:
            output_docstrings[function] += '\n    Parameters\n    %s\n' % ('-' * 10)
        for param, param_text in params.items():
            if param in input_types_default and input_types_default[param][0]:
                output_docstrings[function] += '    %s : %s\n' % (param, input_types_default[param][0])
            else:
                output_docstrings[function] += '    %s\n' % param
            for p in param_text:
                output_docstrings[function] += '        %s\n' % p
            if param in input_types_default and input_types_default[param][1]:
                output_docstrings[function] += '        Default: %s\n' % input_types_default[param][1]

        output_names = attributes['returns']
        if output_names:
            output_types = attributes['output_types']
            output_docstrings[function] += '\n    Returns\n    %s\n' % ('-'*7)
            returns = docstrings[function]['return']

            if len(output_names) != len(output_types):
                if len(output_types) == 1:
                    output_docstrings[function] += '    Number of items in %s : %s\n' % (output_types[0],
                                                                                       len(output_names))
                for ret, ret_text in returns.items():
                    output_docstrings[function] += '    %s\n' % ret
                    for r in ret_text:
                        output_docstrings[function] += '        %s\n' % r
            else:
                for odx, output_name in enumerate(output_names):
                    if output_name in returns:
                        if output_types:
                            if len(output_names) == len(output_types):
                                output_docstrings[function] += '    %s : %s\n' % (output_name, output_types[odx])
                            else:
                                output_docstrings[function] += '    %s\n' % output_name
                        else:
                            output_docstrings[function] += '    %s\n' % output_name
                        for r in returns[output_name]:
                            output_docstrings[function] += '        %s\n' % r
                    else:
                        output_checks.setdefault(function, []).append(output_name)

        output_docstrings[function] += '    """\n'

    return output_docstrings, output_checks


def collect_input_docstrings(input_fp: str) -> tuple:
    """
    Collect the input/output types and default
    as  well as the docstring of each function.

    Parameters
    ----------
    input_fp: str
        Input .py file containing plain docstring.
    Returns
    -------
    Three dicts: tuple
        functions: dict
            parsed input types and default, and output type per function name.
        docstrings: dict
            Docstring Header, Parameters and Returns info per function name.
        to_replace: dict
            Start and end lines of the docstrings (incl. triple quotes).
    """
    functions = {}
    docstrings = {}
    to_replace = {}
    what_is = (0, 0, 0, 0)
    with open(input_fp) as f:
        for ldx, line_ in enumerate(f):
            line = line_.strip()
            if not len(line):
                continue
            if line.startswith('return '):
                ret_line = [x.strip() for x in line.split('return ')[-1].split(',')]
                returns = []
                for ret_ in ret_line:
                    if ret_[0] == '(' and ret_[-1] == ')':
                        ret = ret_
                    elif ret_[0] == '(':
                        ret = ret_[1:].strip()
                    elif ret_[-1] == ')':
                        ret = ret_[:-1].strip()
                    else:
                        ret = ret_
                    returns.append(ret)
                functions[function_name]['returns'] = returns

            elif line.startswith('def '):
                # respective for:
                # - is_docstring
                # - is_return
                # - is_param
                # - is_header
                what_is = (0, 0, 0, 0)
                function_name = line.split('def ')[-1].split('(')[0]
                input_types_default, output_types = parse_definition(line)
                functions[function_name] = {'input_types_default': input_types_default,
                                            'output_types': output_types,
                                            'returns': []}

            elif line.startswith('"""') and not what_is[0]:
                what_is = (1, 1, 0, 0)
                docstring = {'header': [],
                             'params': {},
                             'return': {}}
                to_replace[function_name] = [ldx]

            elif what_is[0]:
                if line.startswith('"""'):
                    what_is = (0, 0, 0, 0)
                    docstrings[function_name] = docstring
                    to_replace[function_name].append(ldx)
                elif line.startswith(':param'):
                    what_is = (1, 0, 1, 0)
                    param_split = line.split(':param')[-1].strip().split(':')
                    param = param_split[0].strip()
                    if param:
                        description = param_split[-1].strip()
                        docstring['params'][param] = [description]
                    else:
                        docstring['params'][param] = []
                elif line.startswith(':return'):
                    what_is = (1, 0, 0, 1)
                    return_split = line.split(':return:')[-1].strip().split(':')
                    return_ = return_split[0].strip()
                    if return_:
                        description = return_[-1].strip()
                        docstring['return'][return_] = [description]
                    else:
                        docstring['return'][return_] = []
                else:
                    if what_is == (1, 1, 0, 0):
                        docstring['header'].append(line)
                    elif what_is == (1, 0, 1, 0):
                        docstring['params'][param].append(line)
                    elif what_is == (1, 0, 0, 1):
                        docstring['return'][return_].append(line)
    return functions, docstrings, to_replace


def write_docstrings(input_fp: str, output_fp: str, to_replace: dict,
                     output_docstrings: dict) -> None:
    """
    Parameters
    ----------
    input_fp
    output_fp
    to_replace
    output_docstrings
    """
    start_line = None
    cur_range = []
    with open(input_fp) as f, open(output_fp, 'w') as o:
        for ldx, line_ in enumerate(f):
            line = line_.strip()
            if not len(line):
                o.write(line_)
            elif line.startswith('def '):
                function_name = line.split('def ')[-1].split('(')[0]
                if function_name not in to_replace:
                    continue
                start_line = to_replace[function_name][0]
                end_line = to_replace[function_name][1]
                cur_range = range(start_line, (end_line+1))
                o.write(line_)
            elif ldx == start_line:
                o.write(output_docstrings[function_name])
            elif ldx in cur_range:
                continue
            else:
                o.write(line_)


def give_notice(output_checks: dict) -> None:
    """
    Parameters
    ----------
    output_checks: dict
        Functions with outputs to manually check for sure.
    """
    if output_checks:
        for function, outputs in output_checks.items():
            print('\t* function: %s' % function)
            for output in outputs:
                print('\t└──── value:', output)


def xvert(folder: str, o_mv: str) -> None:
    """
    Parameters
    ----------
    folder: str
        Folder to start looking for .py files with docstring.
    o_mv: str
        File to write the replacement (mv) script.
    """
    files_to_convert = get_files_with_plain_docstring(folder)

    cmds = []
    all_output_checks = {}
    for input_fp, output_fp in sorted(files_to_convert.items()):
        functions, docstrings, to_replace = collect_input_docstrings(input_fp)
        output_docstrings, output_checks = make_output_docstrings(functions, docstrings)
        if output_checks:
            all_output_checks[output_fp] = output_checks
        write_docstrings(input_fp, output_fp, to_replace, output_docstrings)
        cmds.append('mv %s %s' % (output_fp, input_fp))

    if all_output_checks:
        print('"Returns" to check manually:')
        print('----------------------------')
        for input_fp in all_output_checks:
            print(input_fp)
            give_notice(all_output_checks[input_fp])


    print('Done! %s converted files to check.\n' % len(cmds))
    if o_mv:
        with open(o_mv, 'w') as o:
            for cmd in cmds:
                o.write('%s\n' % cmd)
        print(' - After checking, run this to overwrite original .py files with .xvrted files:')
        print(' sh', o_mv)
