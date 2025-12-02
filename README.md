# LL(1) & SLR(1) Grammar Analyzer

Academic project developed for a course on Formal Languages / Compilers.  
The goal of the application is to **analyze context-free grammars**, determine whether they are **LL(1)** and/or **SLR(1)**, and (when possible) use the corresponding parsing tables to validate input strings.

##  Overview

Given a context-free grammar entered from the console, the program:

- Reads the grammar productions.
- Computes **FIRST** and **FOLLOW** sets for all non-terminals.
- Builds the **LL(1) parsing table**.
- Builds the **SLR(1) ACTION and GOTO tables** from the LR(0) automaton.
- Detects whether the grammar is:
  - LL(1)
  - SLR(1)
  - Both LL(1) and SLR(1)
  - Neither
- If the grammar is LL(1) and/or SLR(1), the program can **analyze strings** and answer whether each string is accepted by the grammar.

This project focuses on implementing the theory behind parsing algorithms in a clean and didactic way.

## Main Features

- Interactive **grammar input** from the console.
- Computation of:
  - FIRST sets
  - FOLLOW sets
- Construction of:
  - LL(1) parsing table
  - SLR(1) ACTION and GOTO tables
- Detection of **conflicts** (non-LL(1) or non-SLR(1) grammars).
- **String parsing** using:
  - LL(1) predictive parser
  - SLR(1) shift-reduce parser
- Nicely formatted tables using `tabulate` for better readability in the terminal.

## Tech Stack

- **Language:** Python 3.x  
- **Libraries:**
  - Standard Python library
  - [`tabulate`](https://pypi.org/project/tabulate/) (for pretty-printing tables in the console)

> Note: In a typical setup you will need to install `tabulate` via `pip`.

## Installation

```bash
# Clone this repository
git clone https://github.com/<your-username>/<your-repo-name>.git

# Go into the project folder
cd <your-repo-name>/src

# (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install tabulate
