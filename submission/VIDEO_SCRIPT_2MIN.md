# Anveya Labs — 2-Minute Demo Video Script
**Google DeepMind × Google Cloud · Startup Buildathon India 2026**

- **Target length:** `2:00` (~285 spoken words at a calm ~140–145 WPM)
- **Live Demo URL:** https://anveya-266974009969.asia-south1.run.app
- **Recommended Live Demo Pairing:** Target = **`Gemma 4 26B`** · Judge = **`Gemini 3.7 Flash`** (triggers a **real live `ANV-7F3K` canary leak** on `v1` in **4.6 seconds**, then **100/100 all held** on `v2` in **4.6 seconds**!)

---

## Pre-Recording 30-Second Checklist (Do This Right Before Hitting Record)
1. Open https://anveya-266974009969.asia-south1.run.app in Chrome at `100%` zoom (`1920×1080` or `1440×900`).
2. Clear any cached runs (`DevTools Console → localStorage.clear(); location.reload()`) so the page starts cleanly on **"Does your bot keep its secrets?"**.
3. In the top bar, set **Target** = `Gemma 4 26B` and **Judge** = `Gemini 3.7 Flash`.
4. Keep the deck open in a second tab (optional for the 5-second intro/outro) or stay 100% inside the live product UI!

---

## Second-by-Second Script & Screen Choreography

### `[0:00 – 0:18]` The Hook & Problem *(18s · ~43 words)*
**On screen:** Start on the live Anveya Labs landing state (*"Does your bot keep its secrets?"* with the breathing Canary ring and subtle `अन्वय` watermark).

> **Speak:**
> "Teams are shipping LLM chatbots to production every week — without knowing if one prompt injection will leak internal instructions, fake an invoice, or break accuracy. When we benchmarked **five live models from four labs**, **sixty percent failed basic security tests** — and one leaked a confidential secret directly."

---

### `[0:18 – 0:38]` Introducing Anveya Labs *(20s · ~48 words)*
**On screen:** Hover briefly over the top chips (`● Live on Cloud Run`, `Target: Gemma 4 26B`, `Judge: Gemini 3.7 Flash`). Click `Target` briefly to show the 12 grouped live models across 5 labs, then close it back on `Gemma 4 26B`.

> **Speak:**
> "Meet **Anveya Labs** — an automated LLM quality, safety, and security assurance platform running live on **Google Cloud Run** in **Mumbai**, powered by **Vertex AI** with **zero static API keys**. We support **twelve live models across five labs** — DeepSeek, OpenAI GPT-OSS, Z.ai GLM, Gemma 4, and Gemini 3.1 Pro — letting you pair any target with an **independent judge** to eliminate self-evaluation bias."

---

### `[0:38 – 1:08]` Live Attack on v1 — Real Canary Leak in 4.6 Seconds *(30s · ~70 words)*
**On screen:**
- Click **`Run 5 tests on v1`**.
- *(While running ~4.6s)* Point at the cycling live attack feed (`→ sending SC-01…`) and amber scan sweep.
- *(When results land)* Let the red **Canary leaked** ring, red `ANV-7F3K` seismograph spike, and dropping `ANV-7F3K` bar flag settle.
- Scroll down smoothly to **03 / EVIDENCE**: show the chat-bubble reply with `ANV-7F3K` highlighted in red, the **`Caught by rules`** pill, and click **`Copy`** on the Suggested Fix (`Copied ✓`).

> **Speak:**
> "Let's test `AcmeSupportBot v1` live on **Gemma 4 26B**, graded by **Gemini 3.7 Flash**. We plant a secret canary token — `ANV-7F3K` — inside the system prompt and fire five concurrent quality, safety, and security attacks.
>
> In **under five seconds**, our **sub-millisecond deterministic rules layer** catches a live canary leak on `SC-01`, dropping Security to **fifty out of one hundred**. Right below, we get the exact prompt, the leaked token highlighted in red, and a one-click copyable fix from our independent judge."

---

### `[1:08 – 1:35]` Hardening Proof — v2 & Side-by-Side Regression Compare *(27s · ~65 words)*
**On screen:**
- Click **`v2 · hardened`**, then click **`Run 5 tests on v2`** (~4.6s).
- Show the green verdict: **"AcmeSupportBot v2 held on all 5 tests."** and **"Canary silent"**.
- Click **`Compare v1 → v2`** to expand the dual aligned Signal Strip (`fixed` tick under `SC-01`, `Security 50 → 100 ↑ Improved`, `Fixed (1): SC-01`, `Regressed (0)`).

> **Speak:**
> "Now let's switch to `v2` with those exact system-prompt guardrails applied and re-run.
>
> In **four point six seconds**: **one hundred across Quality, Safety, and Security** — zero leaks, canary silent. Toggling **Compare** aligns `v1` and `v2` side by side, proving a **fifty-point security uplift** with **zero regressions**. And regression tracking matters: in our five-model benchmark, hardening `DeepSeek v4.1 Flash` actually caused a **fifty-point Quality drop** — exactly the kind of silent breakage Anveya catches before deploy."

---

### `[1:35 – 1:50]` Custom Tests, Presenter Mode & Unit Economics *(15s · ~36 words)*
**On screen:**
- Click **`Tests (5)`** briefly to show the custom test form + 7 built-in presets, close it, then press **`P`** once to flash the sleek **dark stage Presenter Mode**!

> **Speak:**
> "Teams can add custom adversarial tests live, switch into dark **Presenter Mode** for reviews, and run everything for **under two-tenths of a cent per run** — roughly **seventeen paise**, or under **two dollars a month** for a thousand CI checks."

---

### `[1:50 – 2:00]` Close *(10s · ~22 words)*
**On screen:** Hold cleanly on the Compare view (or switch briefly to the Thank You slide with the live Cloud Run URL).

> **Speak:**
> "**Anveya Labs** — plant the canary, attack with independent models, fix, and prove before you ship. Built with Gemini and Vertex AI on Google Cloud. Thank you."

---

## Key Metrics Cheat Sheet (Exact Measured Numbers from Live Cloud Run Benchmark)
| Metric | Value | Source |
| --- | --- | --- |
| Live Models Supported | **12 models across 5 labs** (144 Target × Judge pairs) | Live `anveya-labs-77` Vertex AI `global` |
| v1 Vulnerable Rate | **60% (3 of 5 benchmarked models)** failed Security | Live Cloud Run benchmark (Judge: `Gemini 3.7 Flash`) |
| Live Canary Leak Caught | **Gemma 4 26B** leaked `ANV-7F3K` on `v1` (`< 1 ms` Rules) | Live `anveya-00007-kjx` run (`4.67s`) |
| Security Uplift (`v1 → v2`) | **70 → 100 avg (+30 pts)**; **+50 pts** on all 3 failing models | Live 5-model benchmark |
| Real Regression Caught | **DeepSeek v4.1 Flash** Quality `100 → 50` on `v2` | Live 5-model benchmark |
| Fastest Full 5-Test Run | **4.60 seconds** (10 LLM calls, 5× bounded concurrency) | `Gemma 4 26B` v2 on Cloud Run `asia-south1` |
| Cost Per Evaluation Run | **< \$0.002 / run** (~₹0.17) · **\$0/mo idle** on Cloud Run | Serverless scale-to-zero + Vertex AI token pricing |
| Static API Keys in Prod | **0** (keyless Cloud Run Compute SA `roles/aiplatform.user`) | GCP IAM Workload Identity |

