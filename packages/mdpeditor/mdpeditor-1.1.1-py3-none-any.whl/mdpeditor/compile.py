""" Put together .mdp option blocks, parameters and input .mdp files """
import configparser
from collections import OrderedDict

from rich.console import Console

import mdpeditor.mdpblocks.provide
from mdpeditor.mdpblocks.process import apply_instructions


def transform_input_token_to_parameters(token: str) -> OrderedDict:
    """Take a literal input and return a dictionary with .mdp parameters.

        Attempt to interpret token as
         1. single .mdp parameter (aka option=value)
         2. parameter block (prefix.suffix)
         3. an .mdp file

        return with whatever succeeds first.
    Args:
        token (str): a parameter block name, a string setting an .mdp option,
                    or an .mdp file

    Raises:
        ValueError: if there is no way to interpret the input

    Returns:
        OrderedDict: parameters for simulation input
    """
    # token sets a parameter like key=value
    try:
        return mdpeditor.mdpblocks.provide.mdp_string_to_ordered_dict(token)
    except configparser.ParsingError:
        pass

    # token represents a parameter block prefix.suffix
    try:
        return mdpeditor.mdpblocks.provide.read_parameter_block(token)
    # depending on the token format we'll fail at different positions
    # if this is not a well formed parameter block name a.b
    except ModuleNotFoundError:
        # has form a.b , where a does not exist as a module
        pass
    except FileNotFoundError:
        # has form a.b where a exists, but not b
        pass
    except IndexError:
        # does not have form a.b
        pass

    # token represents an .mdp file to be read
    try:
        with open(token, encoding="utf-8") as file:
            mdp_input_as_string = file.read()
        return mdpeditor.mdpblocks.provide.mdp_string_to_ordered_dict(
            mdp_input_as_string)
    except FileNotFoundError:
        pass
    except configparser.ParsingError:
        pass

    # no way of parsing the token yields a result to be returned
    raise ValueError(f"{token}" +
                     "cannot be read as an .mdp file, a block name or "
                     "an attempt to set an .mdp option.")


def compile_parameters(compile_input_tokens):

    parameter_blocks = [
        transform_input_token_to_parameters(token)
        for token in compile_input_tokens
    ]

    parameters = OrderedDict()
    duplicate_keys = set()

    for block in parameter_blocks:

        # collect overlapping parameters in the blocks
        duplicate_keys |= set(parameters.keys()) & set(block.keys())
        parameters.update(block)

    apply_instructions(parameters, compile_input_tokens)

    return OutputParameters(parameters, duplicate_keys)


class OutputParameters:
    """
    Handle parameter output like printing and cleaning
    """
    def __init__(self, parameters, duplicate_keys):

        # open default .mdp and fill in the "other parameters"
        # discard all non-default parameters
        self.parameters = mdpeditor.mdpblocks.provide.default_parameter_block()
        for key in self.parameters.keys():
            if key in parameters.keys():
                self.parameters[key] = parameters[key]

        self.duplicate_keys = duplicate_keys
        self.modified_keys = parameters.keys()

    def keep_only_modified(self):
        """ Remove all parameters that have not been modified """

        keys_to_pop = [
            key for key in self.parameters.keys()
            if key not in self.modified_keys
        ]
        for key in keys_to_pop:
            self.parameters.pop(key)

    def as_string(self):
        """ write the parameters as a string in .mdp format"""

        if not self.parameters:
            return ""

        modifed_key_style = "bold"

        max_key_length = max(map(len, self.parameters.keys()))

        formatted_mdp_entries = [
            f'[{modifed_key_style}]{key:{max_key_length}s} = '
            f'{value}[/{modifed_key_style}]' if key in self.modified_keys else
            f'{key:{max_key_length}s} = {value}'
            for key, value in self.parameters.items()
        ]

        return '\n'.join(formatted_mdp_entries) + "\n"


def help_compile_string(blocks):

    help_string = (
        "compile your .mdp file by setting individual parameters, "
        "reading an input .mdp file (not recommended for reproducible "
        "work) and these predefined blocks ")

    help_string += ("\n[bold]" + blocks + "[/]\n")

    help_string += ("\nUse [italic]--explain[/] to "
                    "learn more about these blocks.\n")

    help_string += "\nExamples:\n"
    help_string += (
        "\n\t[italic] density_guided.vanilla pixel-size-in-nm=0.98 "
        "reference-density-filename=map.mrc some.mdp"
        "\n\tforce_field.amber "
        "pressure.atomspheric[/]\n")

    return help_string


def run_compile(compile_command: str, merge_right, full_mdp):
    """Put together one or more compile commands.

    Args:
        compile_command (str): whitespace separated tokens
        merge_right (bool)   : whether overwriting previously set parameters
                               is allowed
        full_mdp (bool)      : whether to write all default parameters

    Raises:
        SystemExit: Exit without stacktrace if compile_command cannot be
                    interpreted
        SystemExit: Exit without stacktrace if compile_command cannot be
                    interpreted
        SystemExit: Exit without stacktrace if parameters would be overwritten
                    but was not allowed by merge_right

    Returns:
        str: output parameters in .mdp format
    """
    # print some hints if the input string is empty
    if not compile_command or compile_command[0].strip() == "help":
        return help_compile_string(
            mdpeditor.mdpblocks.provide.formatted_blocks())

    try:
        output_parameters = compile_parameters(compile_command)
    except ValueError as error:
        raise SystemExit(error.__str__()) from error
    except AttributeError:
        raise SystemExit() from error

    if (not merge_right and output_parameters.duplicate_keys):
        raise SystemExit(
            "\nAborting compilation due to duplicate parameter(s)\n\n\t" +
            "\n\t".join(list(output_parameters.duplicate_keys)) +
            "\n\nUse --merge-duplicates to override parameters\n")

    if not full_mdp:
        # discard all parameters that were not explicitely chosen
        output_parameters.keep_only_modified()

    return output_parameters.as_string()


def print_annotated_output(console, output_string, version, arguments,
                           output_file):
    """Generate an annotated .mdp file including command name and version.

    Args:
        console ()         : rich console to print to
        output_string (str): the output mdp
        version (str)      : version of the programme
        arguments          : command line arguments to the programme
        output_file        : file to write to
    """
    # keep track of the command used to generate
    # the output by prepending a commented line
    prefix = f"; Created by mdpeditor version {version}\n;"
    prefix += ' '.join(arguments)
    prefix += ("\n; To create self-documenting workflows, do not edit this"
               " file but rerun this tool with different settings\n")

    # direct output to outputfile
    if output_file:
        console = Console(file=output_file)

    console.print(prefix + output_string, style="")
