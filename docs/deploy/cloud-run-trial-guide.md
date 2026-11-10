# Cloud Run trial deployment guide

| Owner | Written | Tested on | Related |
|---|---|---|---|
| Utku Uçar | 07/11/2026 | 07/11/2026, Windows 11, Google Cloud SDK 592.0.0 | Spike S5; C-07; Cost & Funding rows 17–20; [S5 trial results](../spikes/s5-cloud-run-trial-results.md) |

This guide deploys the trial question-answering service in `deploy/trial/` to Cloud Run in two forms:

- **CPU:** the small model `qwen2.5:1.5b`, no GPU.
- **GPU:** the larger model `qwen2.5:7b` on one NVIDIA L4 GPU.

The trial ran in a personal project (`utku-llm-deneme`), separate from the team project. Every command below runs in Windows CMD.

## Contents of `deploy/trial/`

| File | Purpose |
|---|---|
| `app.py` | Web page, BM25 search (5-letter prefixes, paragraphs joined up to 900 characters, 977 passages) and calls to the model. Python standard library only. |
| `Dockerfile` | The `ollama/ollama` image with Python and the model. The model is pulled at build time. |
| `.gcloudignore` | Files that are not uploaded. |
| `data/text/` | Copy of the 8 extracted documents. Not committed (listed in `.gitignore`). |

## Prerequisites

- An education credit coupon redeemed at https://console.cloud.google.com/education. The coupon is valid for one year after it is redeemed.
- Google Cloud CLI installed (https://cloud.google.com/sdk/docs/install), with the Beta Commands component. Docker, Python and Ollama are not needed on the laptop, because Cloud Build builds the image.

## 1. Budget and spend cap (console)

| Budget | Scope | Amount | Thresholds | Savings |
|---|---|---|---|---|
| Alert budget, alerts only | Billing account, all services | $20 per month | 50 %, 90 %, 100 % | Both savings boxes cleared, so that the education credit does not hide the spend |
| Spend cap enforcement | The project, Cloud Run only | $10 per month | 50 %, 80 %, 100 %; Cloud Run is paused at 100 % | Not applicable |

The spend cap can only be created after the project exists (step 2). It takes effect a few minutes after the cap is crossed, not instantly.

## 2. Project

```cmd
gcloud auth login
gcloud projects create <PROJECT_ID>
gcloud billing accounts list
gcloud billing projects link <PROJECT_ID> --billing-account=<ACCOUNT_ID>
gcloud config set project <PROJECT_ID>
gcloud config set run/region europe-west1
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

## 3. Build folder

```cmd
xcopy data\text deploy\trial\data\text\ /E /I /Y
cd deploy\trial
dir /a /b
```
Run the deploy only from the folder that contains `Dockerfile`. From any other folder, `--source .` uploads that whole folder and builds it with Buildpacks.

## 4. Deploy the CPU service

```cmd
gcloud run deploy di502-trial --source . --cpu 4 --memory 8Gi --cpu-boost --max-instances 1 --concurrency 4 --timeout 300 --no-allow-unauthenticated
```
The first build took about 10 minutes. The service scales to zero and costs nothing while idle.

## 5. Deploy the GPU service

Set `MODEL=qwen2.5:7b` in `Dockerfile`, then run:
```cmd
gcloud run deploy di502-trial-gpu --source . --gpu 1 --gpu-type nvidia-l4 --no-gpu-zonal-redundancy --cpu 4 --memory 16Gi --no-cpu-throttling --max-instances 1 --concurrency 4 --timeout 300 --no-allow-unauthenticated
```
No quota request was needed; the L4 GPU was granted on the first deployment in `europe-west1`. The build took under 13 minutes.

Set `MODEL` back to `qwen2.5:1.5b` before you redeploy the CPU service from source.

## 6. Access

Both services are private. Open each one through an authenticated proxy, in a separate CMD window for each:
```cmd
gcloud run services proxy di502-trial --region europe-west1 --port 8080
gcloud run services proxy di502-trial-gpu --region europe-west1 --port 8081
```
Then open http://localhost:8080 or http://localhost:8081. On first use, gcloud installs the `cloud-run-proxy` component.

## 7. Redeploy without rebuilding

Deleting a service keeps its image. To find the image and redeploy it:
```cmd
gcloud artifacts docker images list europe-west1-docker.pkg.dev/<PROJECT_ID>/cloud-run-source-deploy
gcloud run deploy di502-trial-gpu --image <IMAGE> <the same flags as step 5, without --source>
```

## 8. Tear down

Delete the GPU service right after each session, because it costs about $1.05 per hour while an instance is up:
```cmd
gcloud run services delete di502-trial-gpu --region europe-west1
```
When the trial ends, delete everything:
```cmd
gcloud run services delete di502-trial --region europe-west1
gcloud artifacts repositories delete cloud-run-source-deploy --location europe-west1
```

## Cost reference (europe-west1, GPU service as configured in step 5)

L4 without zonal redundancy $0.0001867/s, plus 4 vCPU × $0.000018/s, plus 16 GiB × $0.000002/s, comes to $0.000291/s, or about $1.05 per hour. Source: https://cloud.google.com/run/pricing, read on 06/11/2026.
