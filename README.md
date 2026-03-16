# Serverless Cookbook

Runnable, workload-first examples for Serverless AI Jobs and Endpoints.

The repository demonstrates how to run real AI/ML workloads without managing infrastructure.
Examples focus on practical workloads such as:

- model training
- fine-tuning
- batch inference
- LLM serving

> ⚠️ This repository contains community-maintained examples for running workloads on Serverless AI.
> The examples are provided for experimentation and learning. Platform features and commands may change.
>
> For official documentation, see: <https://docs.nebius.com/serverless>

## Getting started

1. Set up the Nebius CLI once at repo level, then run examples without repeating setup in every tutorial.

    - Install Nebius CLI: <https://docs.nebius.com/cli/install>
    - Configure Nebius CLI profile/project: <https://docs.nebius.com/cli/configure>

2. Pick an example from `quickstarts/`, `training/`, or `inference/`.
3. Open the example markdown file (`README.md` or `*.md` quickstart).
4. Follow the commands and verify the expected output section.

## Repository map

```text
serverless-cookbook/
├─ README.md
├─ CONTRIBUTING.md
├─ DEVELOPER_GUIDE.md
├─ LICENSE
├─ quickstarts/
│  ├─ first-job.md
│  ├─ first-endpoint.md
├─ training/
│  ├─ axolotl-finetuning/
│  └─ ...
├─ inference/
│  ├─ vllm-endpoint/
│  └─ ...
```

## Section intent

- `quickstarts/`: lowest-friction first runs.
- `training/`: model training and fine-tuning workloads.
- `inference/`: endpoint serving and batch inference workloads.

## Example catalog

### 🚀 Quickstarts

- [`first-job.md`](./quickstarts/first-job.md) - run `nvidia-smi` in a Serverless AI job
- [`first-endpoint.md`](./quickstarts/first-endpoint.md) - deploy an authenticated nginx endpoint

### 🏋️ Training

- [`axolotl-finetuning`](./training/axolotl-finetuning/README.md) - get started fine-tuning with Axolotl

### ⚡ Inference

- [`vllm-endpoint`](./inference/vllm-endpoint/README.md) - serve Qwen via OpenAI-compatible vLLM endpoint

## Resources

- [Contributing](./CONTRIBUTING.md)
- [Developer Guide](./DEVELOPER_GUIDE.md)
- [Serverless AI overview docs](https://docs.nebius.com/serverless/overview)
- [CLI AI reference](https://docs.nebius.com/cli/reference/ai/)
