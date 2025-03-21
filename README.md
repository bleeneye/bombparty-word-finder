# BombParty Word Finder

BombParty (BP) Word Finder is a keyboard-operated tool intended for assitance with BombParty prompts.
It can enter words which match the current prompt into the chat and autosolve prompts.

While the list of words included with the tool is relatively comprehensive,
it does not include all valid BombParty prompt solutions.

Due to various dependencies requiring access to mouse and keyboard states,
BP Word Finder does not work well on Windows Subsystem for Linux (WSL),
as it does not have access to the Windows GUI sustem.

*Note that I do not condone using this tool to cheat in public lobbies.
You may be kicked from lobbies if using BP Word Finder or any other prompt assistance.*

## Installation

### Install Conda

[Instructions for installing Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

### Create a Conda environment

In a terminal window, run the following command:

```
conda create -n bpfinder -y python=3.10
```

### Activate your Conda environment

In a terminal window, run the following command:

```
conda activate bpfinder
```

### Install BombParty Word Finder and dependencies

In a terminal window, run the following command:

```
pip install git+https://github.com/bleeneye/bombparty-word-finder.git@main#egg=bombparty-word-finder
```

## Usage

### Start

#### Ensure your Conda environment is activated:

```
conda activate bpfinder
```

#### Start BombParty Word Finder:

```
bpfinder
```

### Quit

Press `Esc` twice in quick succession to terminate BP Word Finder.

### Keyboard commands

Other than quitting and autosolving prompts, all commands require holding `Ctrl+Alt+Shift`.

- `Ctrl+Alt+Shift + .`: Set bombtext location (required)
- `Ctrl+Alt+Shift + ,`: Set textbox location (optional)
- `Ctrl+Alt+Shift + /`: Set chatbox location (optional)
- `Ctrl+Alt+Shift + q`: Enable/disable cheating, *i.e., autosolving* (default: disabled)
- `Ctrl+Alt+Shift + <0-9>`: Set number of extra words to be entered in chat (default: 0)
- `Ctrl+Alt+Shift + +`: Set sorting to forward (e.g., Common sorter sorts most to least common) (default)
- `Ctrl+Alt+Shift + -`: Set sorting to backward (e.g., Common sorter sorts least to most common)

Various letter commands are used to switch word sorters.

- `Ctrl+Alt+Shift + n`: Null sorter (does not sort words, defaults to alphabetical order)
- `Ctrl+Alt+Shift + r`: Random sorter (sorts words randomly)
- `Ctrl+Alt+Shift + c`: Common sorter (sorts words by use frequency)
- `Ctrl+Alt+Shift + u`: Roulette sorter (sorts words randomly, prioritizing by use frequency)

### Autosolve prompts

Press `F4` to autosolve prompts.

As long as a bombtext location is  set, BP Word Finder will find matching words for it.

If the textbox location is set and cheating is enabled, BP Word Finder will autocomplete the current prompt.

If the chatbox location is set, BP Word Finder will enter a number of words into it equal to the number of extra words.

## Uninstallation

### Remove configurations

In a terminal window, run the following command:

```
bpfinder-uninstall
```

Enter "y" or "yes" (case insensitive) to confirm.

This will remove all config files and directories associated with BP Word Finder.

### Uninstall package

In a terminal window, run the following command:

```
pip uninstall bombparty_word_finder
```

Alternatively, you may delete the entire Conda environment by running the following command:

```
conda remove -n bpfinder --all
```

## Editable Installations

For those wishing to contribute to BP Word Finder, having an editable installation is desirable
in order to view the effects of code changes without needing to reinstall the package.

Because BP Word Finder uses Poetry as a build backend,
simply running `pip install -e git+<repository URL>` will not properly install an editable version.
A Poetry installation is required to install an editable version.

### Install Poetry

[Instructions for installing Poetry](https://python-poetry.org/docs/)

### Create and activate a Conda environment

Like the normal installation, we will use a Conda environment.

In a terminal window, run the following commands:

```
conda create -n bpfinder-edit -y python=3.10
conda activate bpfinder-edit
```

*If you know Poetry and would rather use a Poetry virtual environment, you may
[create and activate a Poetry environment instead](https://python-poetry.org/docs/managing-environments/).*

### Clone this repository

In whichever directory you would like to store the BP Word Finder source code, run the following command:

```
git clone https://github.com/bleeneye/bombparty-word-finder.git
```

### Install dependencies

In the base directory of your local clone of `bomparty-word-finder` (`cd bombparty_word_finder`), run the following command:

```
poetry install
```

### Reinstall BP Word Finder as editable version

Again, in the base directory of you local clone of `bombparty-word-finder`, run the following command:

```
pip install -e .
```

Now any changes you make to the source code will immediately take effect when using
the `bpfinder-edit` Conda environment.

