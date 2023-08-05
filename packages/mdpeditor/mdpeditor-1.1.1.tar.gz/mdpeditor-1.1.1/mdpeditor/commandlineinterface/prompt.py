import readline

import mdpeditor.mdpblocks.provide
import mdpeditor.mdpblocks.process
import mdpeditor.compile
import mdpeditor.parameterhelp.explain


class Completer:
    def __init__(self, blocks, parameter_keys):
        self.blocks = blocks
        self.parameter_keys = parameter_keys

    def complete_compile(self, text, state):
        """ add a = for parameters tab completion
        """
        results = [x + " " for x in self.blocks if x.startswith(text)] + [
            x + "=" for x in self.parameter_keys if x.startswith(text)
        ] + [None]
        return results[state]

    def complete_explain(self, text, state):
        results = [x + " " for x in self.blocks if x.startswith(text)] + [
            x + " " for x in self.parameter_keys if x.startswith(text)
        ] + [None]
        return results[state]


def console_prompt_string(compile_mode):

    output_string = ("\nPress [bold][ENTER][/bold] to switch to ")

    if compile_mode:
        output_string += "normal"
    else:
        output_string += "--explain"

    output_string += " mode.\n"
    output_string += ("Press [bold][TAB][/bold] to list input options.\n")
    output_string += ("Press [bold][CTRL]+C[/bold] to exit, type "
                      "[bold]help[/] for more details on usage.")

    output_string += "\n>"

    if compile_mode:
        output_string += "[italic] mdpeditor[/] "
    else:
        output_string += "[italic] mdpeditor --explain[/] "

    return output_string


def run_interactive_prompt(console, version):

    # introductory message
    console.rule(f"mdpeditor {version}", style="")
    console.print(
        "Welcome to the interactive mode of mdpeditor!"
        "\n\nHere you"
        " can learn about .mdp parameters and parameter blocks "
        "and test different parameter combinations.\n\nFor production"
        " code in workflows, copy paste the prompt below"
        " and have a look at [bold]mdpeditor --help[/].\n")

    # set up tab completion
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(" ")
    completer = Completer(
        mdpeditor.mdpblocks.provide.available_parameter_blocks(),
        mdpeditor.parameterhelp.explain.mdp_options_list() +
        mdpeditor.mdpblocks.process.tab_completion_hints())
    readline.set_completer(completer.complete_compile)

    merge_right = False
    full_mdp = False

    line = ""
    compile_mode = False
    while line is not None or line == "end":
        # swap mode if only [Enter] was pressed
        # alter tab completion
        if line == "":
            compile_mode = not compile_mode
            if compile_mode:
                readline.set_completer(completer.complete_compile)
            else:
                readline.set_completer(completer.complete_explain)

        try:
            console.rule(style="")
            line = console.input(console_prompt_string(compile_mode))
            if line == "":
                continue
            if compile_mode:
                output = mdpeditor.compile.run_compile(line.split(),
                                                       merge_right, full_mdp)
            else:
                output = mdpeditor.parameterhelp.explain.run_explain(line)
            console.rule()
            console.print(output)

        # end gracefully when the user interrupts
        except KeyboardInterrupt:
            line = None
        except EOFError:
            line = None
        # do not exit like we do when running pure command line mode
        except SystemExit as error:
            console.print(error.__str__() + "\n")

    console.print("\n\nThanks for using mdpeditor!")

    console.print(
        "\nDiscuss .mdp parameters at "
        "https://gromacs.bioexcel.eu/tag/mdp-parameters",
        justify="right")

    console.print(
        "Report issues and suggestions for mdpeditor at "
        "https://gitlab.com/cblau/mdpeditor/-/issues",
        justify="right")

    console.print("\n:Copyright: 2021,2022  Christian Blau", justify="right")
