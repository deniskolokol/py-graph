# py-graph

A small study project for learning graphing and plotting in Python with Matplotlib and NumPy.

## Goals

- Practice plotting functions and sampled data.
- Learn axis customization (centered axes, ticks, formatting, path effects).
- Explore iterative plotting in notebooks and scripts.

## Project Structure

- `centered_axes.py` — script-based example with custom centered spines and arrowed axes.
- `plotting_examples.ipynb` — notebook for interactive plotting experiments.
- `requirements.txt` — Python dependencies.

## Setup

### 1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

## Run

### Script example

```bash
python centered_axes.py
```

### Notebook example

```bash
jupyter notebook
```

Then open `plotting_examples.ipynb` in your browser.

## Study Roadmap

1. Start with basic line plots (`plt.plot`).
2. Add labels, title, legend, and grid.
3. Customize axes (limits, equal aspect, centered spines).
4. Compare script-based vs notebook-based workflows.
5. Add your own functions (e.g., polynomial, trig, piecewise).

## Common Issues

- If `python centered_axes.py` fails but your venv works, verify your shell is using the venv interpreter:

	```bash
	which python
	```

- If plots do not display in notebook, install and enable Jupyter dependencies in the same environment.

## License

See `LICENSE`.