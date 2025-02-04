# ml_platform_comparison

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Evaluate the UX of different ML platforms by building the same models across them. The study will focus on ease of use, feature comprehensiveness, and developer experience.

## Prerequisites
Before running `make create_environment`, ensure you have `virtualenvwrapper` installed:
**Linux/macOS**:  
  ```sh
  pip install virtualenvwrapper
  echo "source $(which virtualenvwrapper.sh)" >> ~/.bashrc
  source ~/.bashrc
  ```

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         ml_platform_comparison and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── ml_platform_comparison   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes ml_platform_comparison a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

## Phase 0
Goal: Assess the ease of getting started with basic ML experimentation in the platform.

### Key Aspects

	•	Data: Simple synthetic dataset with a small number of labeled transactions.
	•	Compute: Notebooks instead of full pipelines.
	•	Storage: Local storage (e.g., CSV files, in-memory Pandas).
	•	Feature Engineering: Basic transformations in the notebook.
	•	Libraries: Minimal dependencies (numpy, pandas, sklearn).

### Usability Metrics

| Metric                  | Description                                                                 | Target      |
|-------------------------|---------------------------------------------------------------------------|------------|
| **Time to First Model (TTFM)** | Time taken to load data, train a basic model, and get predictions | < 30 min   |
| **Setup Friction Score** | Number of manual steps needed to install dependencies, configure the environment, and start working (lower is better) | < 5 steps  |
| **Notebook UX Score**    | Subjective rating (1–5) on ease of code execution, visualization, debugging | ≥ 4        |
| **Data Ingestion Ease**  | Number of steps to load data from
 