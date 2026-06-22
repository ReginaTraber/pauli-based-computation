# Pauli-Based Computation


📖 **Read online:** https://reginatraber.github.io/pauli-based-computation/

▶️ **Run it live:** [![Launch on Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ReginaTraber/pauli-based-computation/main?labpath=notebook.ipynb)
&nbsp; (opens JupyterLab in the browser, built from `environment.yml`, with no login)


## Publish

The **Quarto website** is deployed to GitHub Pages automatically on every push to `main`. The build
uses the **outputs already saved in the notebook** (`execute: enabled: false` in
`_quarto.yml`), so animations and results render without re-running qiskit in CI.
**Before pushing, run the notebook and save it** so the latest outputs are embedded.

**Binder** is separate: it is *not* deployed by the action. mybinder.org builds the
environment on demand from `environment.yml` the first time someone opens the badge
link after a new commit.

To preview locally (after [installing Quarto](https://quarto.org/docs/get-started/)):

```bash
quarto preview        # live preview at localhost
```

## Local Setup

Run these from the repository root:

```bash
conda env create -f environment-dev.yml   # create the environment
conda activate pbc-notebook-dev           # activate the dev environment
pip install -e .                          # link the pbc package into the env (run from root)
```

`pip install -e .` is a one-time step. After it succeeds once, `import pbc`
works from any directory and any notebook, so you never need to run it again
(unless you recreate the environment).

## Local Run of the notebook

```bash
conda activate pbc-notebook-dev
jupyter lab
```

## Test

```bash
python -m pytest -q
```