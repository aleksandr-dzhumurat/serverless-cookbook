---
title: First Job
category: quickstarts
type: job
runtime: gpu
frameworks:
  - nebius-cli
keywords:
  - jobs
  - gpu
  - nvidia-smi
difficulty: quickstart
---

## Getting started with Serverless AI jobs: Run `nvidia-smi` within a job

Use this quickstart to validate that a GPU job can start, run, and return logs in your project.

Official docs example: [Getting started with Serverless AI jobs](https://docs.nebius.com/serverless/quickstart/jobs)

## What this example does

Runs a Serverless AI job that executes `nvidia-smi` and prints GPU details from inside the container.

## Why this is useful

It is the fastest way to verify quota, subnet routing, image startup, and GPU visibility before running heavier workloads.

## Prerequisites

- Nebius CLI is installed and configured (see [Setup](../README.md#setup))
- you are in a tenant group with admin permissions
- VM quota is available (Administration -> Limits -> Quotas -> Compute -> Number of virtual machines)

Check that your project configuration is present:

```bash
cat ~/.nebius/config.yaml
```

## Runtime / compute

- image: `nvidia/cuda:13.1.1-runtime-ubuntu24.04`
- platform: `gpu-h200-sxm`
- preset: `1gpu-16vcpu-200gb`
- timeout: `15m`

## Files

- `first-job.md`: this quickstart document

## Quickstart

```bash
SUBNET_ID=$(nebius vpc subnet get-by-name --name default-subnet \
  --format jsonpath='{.metadata.id}')

nebius ai job create \
  --name my-job \
  --image nvidia/cuda:13.1.1-runtime-ubuntu24.04 \
  --container-command bash \
  --args "-c nvidia-smi" \
  --platform gpu-h200-sxm \
  --preset 1gpu-16vcpu-200gb \
  --timeout 15m \
  --subnet-id "$SUBNET_ID"

export JOB_ID=$(nebius ai job get-by-name --name my-job \
  --format jsonpath='{.metadata.id}')
nebius ai job get "$JOB_ID"
nebius ai logs "$JOB_ID"
```

## Expected output

- job reaches running/succeeded status
- logs include `nvidia-smi` output and GPU table

## How to adapt

- replace `--image` with your own container image
- replace `--args` with your workload command
- adjust platform/preset/timeout for your runtime

## Troubleshooting

- if job is stuck pending, verify VM quota and subnet
- if job creation fails, confirm active profile and `parent-id` in CLI setup
- if logs are empty, re-check image/command and inspect job status repeatedly

Optional cleanup:

```bash
nebius ai job delete "$JOB_ID"
```
