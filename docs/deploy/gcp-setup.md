# Google Cloud setup

| Set up by | Date | Related |
|---|---|---|
| Utku Uçar | 09/11/2026 | Dependencies 4; Facilities 11; Cost & Funding rows 10, 16–21; C-07; [Cloud Run trial deployment guide](cloud-run-trial-guide.md) |

The team's Google Cloud project was ready on 09/11/2026. This page records how it is set up: the project, the credit that pays for it, the spending limits and who can access what.

## Project

| Item | Value |
|---|---|
| Project name | Rag Against The Machine |
| Project ID | `rag-against-the-machine` |
| Region | `europe-west1` (has NVIDIA L4 GPUs for Cloud Run) |
| Enabled APIs | Cloud Run, Cloud Build, Artifact Registry, Cloud Storage |

## Credit

| Item | Value |
|---|---|
| Source | METU education coupon, $100, course "Data Informatics Project nov26" |
| Billing account | Billing Account for Education, owned by Utku Uçar's Google account |
| Redeemed | 07/11/2026 |
| Valid until | 04/11/2027 (after the project ends on 30/12/2026) |
| Other project on the same account | `utku-llm-deneme`, Utku Uçar's trial project from 07/11/2026. It spends the same credit and has its own limits ($20 alert, $10 Cloud Run cap). |

## Spending limits

All amounts are gross: the education credit is excluded, so the limits count the real spend.

| Budget | Type | Covers | Amount | Period | Thresholds | What happens | Emails go to |
|---|---|---|---|---|---|---|---|
| `rag-35usd-total` | Alert | The whole project | $35 | 08/11/2026 – 31/12/2026 | 50 %, 90 %, 100 % | An email is sent | Utku Uçar, Elif Yeşim Koçoğlu |
| `rag-cloudrun-cap-17-5usd` | Spend cap | Cloud Run in the project | $17.50 | Each calendar month | 50 %, 80 %, 100 % | At 100 %, Cloud Run is paused until the cap is lifted | Utku Uçar and all project Owners |

At $17.50 a month for November and December, Cloud Run cannot spend more than the $35 total. The cap takes effect a few minutes after it is crossed, not instantly.

## Access

| Member | Project role | Billing account role |
|---|---|---|
| Utku Uçar | Owner | Billing Account Administrator |
| Elif Yeşim Koçoğlu | Owner | Billing Account Viewer |
| Deniz Şenkutlu | Owner | Billing Account Viewer |
| Muhammed Batuhan Tezcan | Owner | Billing Account Viewer |

The Owner role starts only when the member accepts the email invitation. Billing Account Viewers can see costs but cannot change the billing account.

## Rules for using the project

1. Tell Elif Yeşim Koçoğlu before each deployment. She tracks spending (Cost 10).
2. Deploy with `--max-instances 1`.
3. Delete each GPU service as soon as the session ends. One L4 instance costs about $1.05 per hour while it runs.
4. Do not delete the project or change other members' roles.

## Connect from a laptop

Only members who deploy from their own laptop need this. Install the Google Cloud CLI (https://cloud.google.com/sdk/docs/install), then run in CMD:
```cmd
gcloud auth login
gcloud config set project rag-against-the-machine
gcloud config set run/region europe-west1
gcloud config list
```
The last command must show `project = rag-against-the-machine`.

## Open items

| # | Item | Owner | Due |
|---|---|---|---|
| 1 | Accept the Owner invitation | Elif Yeşim Koçoğlu, Deniz Şenkutlu, Muhammed Batuhan Tezcan | 11/11/2026 |
| 2 | The limit here is $35. A-06, C-09 and Cost & Funding still say $70 of $100. Update those pages to the agreed amount. | Utku Uçar | [TBC] |
| 3 | Mark Dependencies 4 as done on 09/11/2026. Record in Facilities 11 and Cost 10 that the credit is on Utku Uçar's billing account. | Elif Yeşim Koçoğlu | [TBC] |
| 4 | Delete all resources and logs after 30/12/2026 (Cost 16) | Elif Yeşim Koçoğlu | 31/12/2026 |
