# Combi-Puzzles Dataset

[![Paper](https://img.shields.io/badge/Paper-arXiv%3A2412.11908-B31B1B)](https://arxiv.org/abs/2412.11908)
[![Hugging Face Dataset](https://img.shields.io/badge/Hugging%20Face-Dataset-blue)](https://huggingface.co/datasets/andynik/combi-puzzles)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-181717?logo=github)](https://github.com/andynik/combi-puzzles)

This repository contains the Combi-Puzzles dataset used in the research paper titled "Can Language Models Rival Mathematics Students? Evaluating Mathematical Reasoning through Textual Manipulation and Human Experiments."

The dataset is available in `JSON` and in `Parquet` formats on the [Hugging Face](https://huggingface.co/datasets/andynik/combi-puzzles) repository.

## Abstract

In this study, we examine the ability of recent large language models (LLMs), including LLaMA-2, LLaMA-3.1, GPT-4, and Mixtral, in solving mathematical problems in combinatorics. We introduce the Combi-Puzzles dataset, consisting of 125 problem variants derived from 25 core combinatorial problems, to facilitate these comparisons. The dataset assesses the generalizability of LLMs and includes variations like adversarial, parameterization, and linguistic obfuscation to test models and humans alike. [Link to full paper]

## Dataset

### Dataset Description

The Combi-Puzzles dataset includes:
- **25 Base Combinatorial Problems**: Covers permutations, combinations, rules of addition/multiplication, and object arrangements.
- **5 Variations per Problem**:
  - **Common**: Standard textbook form.
  - **Mathematical**: Academic, technical presentation.
  - **Adversarial**: Includes additional irrelevant information.
  - **Parameterisation**: Altered numerical parameters.
  - **Linguistic Obfuscation**: Narrative fictional stories with problem context.

These variations are designed to thoroughly evaluate problem-solving strategies across different formats.

### Problem Example

![Problem Example](images/p10.png)

The image above illustrates an example of a combinatorial problem and its variations. The highlighted text indicates content modifications based on the common version. The mathematical and linguistic obfuscation variations constitute the new text

### Additional Information

The Combi-Puzzles dataset contains problems that have parameters expressed in string format (e.g. 12 as "twelve"). These problems are identified as:

- **Problems' ID with String Parameters**: 6, 12, 19, 20.

Please note that all parameters are stored as `strings` in the dataset to ensure consistency.

## Experimental setup

### Installation

To set up the environment and run the scripts, install the necessary Python (v3.10.12) libraries using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### GPU

NVIDIA Quadro RTX 8000 with 48 GB of RAM.

### OS
```
OS Ubuntu 22.04.5 LTS
OS kernel 6.2.0-37-generic
```

## Usage

You are encouraged to use this dataset to further evaluate problem-solving strategies in LLMs or other domains. Please cite our paper if you publish material based on this dataset.

### License

This dataset is licensed under the MIT License. See the `LICENSE` file for more details.

### Citation

Please cite the following if you use the dataset in your work:

```bibtex
@misc{nikolaiev2024languagemodelsrivalmathematics,
  title={Can Language Models Rival Mathematics Students? Evaluating Mathematical Reasoning through Textual Manipulation and Human Experiments},
  author={Andrii Nikolaiev and Yiannos Stathopoulos and Simone Teufel},
  year={2024},
  eprint={2412.11908},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2412.11908},
}
```
