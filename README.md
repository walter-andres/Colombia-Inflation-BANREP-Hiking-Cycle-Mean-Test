# Colombian inflation before vs. after a BANREP interest‑rate hiking cycle

**Question.** *Is the average monthly inflation rate in Colombia significantly different before and after a Banco de la República (BANREP) interest‑rate increase (hiking) cycle?*

**Answer (short).** **Yes.** Average monthly inflation is significantly **higher after** the post‑pandemic hiking cycle than before it (Welch *t*, Student *t*, and Mann–Whitney U all reject H₀, p < 0.01 in the primary test; the result survives a cleaner symmetric‑window robustness design with a medium effect size).

## Design

| Component | Definition |
|---|---|
| **Dependent variable (Y)** | Colombian monthly inflation = month‑over‑month % change of the **IPC** (Índice de Precios al Consumidor, base 2018, DANE). |
| **Independent variable (X)** | Categorical **monetary‑policy regime** (`Before` / `After`), built from the **BANREP policy rate** (Tasa de política monetaria). The source file provides the rate at **end‑of‑month** frequency — the end‑of‑month monthly conversion of the daily series. |
| **Cycle** | The post‑pandemic tightening, detected data‑driven: rate trough **1.75 %** (held to Sep‑2021) → first hike **Oct‑2021** → peak **13.25 %** (May‑2023). |
| **Method** | Two‑sample mean‑difference test (Welch & Student *t* + Levene & Shapiro–Wilk assumption checks + Mann–Whitney U + Cohen's *d*), with two robustness checks: symmetric 24‑month windows and a **seasonal paired test** (same calendar month, 2024 vs 2019). |

## Key results

| Analysis | Mean before | Mean after | Diff | Welch *p* | Decision (α=.05) |
|---|---|---|---|---|---|
| Full‑sample split at cycle start | 0.44 %/mo | 0.65 %/mo | −0.22 p.p. | 0.0015 | Reject H₀ |
| Symmetric 24‑month windows | 0.27 %/mo | 0.50 %/mo | −0.23 p.p. | 0.018 | Reject H₀ |
| Seasonal paired (2024 vs 2019) | 0.29 %/mo | 0.40 %/mo | +0.11 p.p. | 0.089 | Fail to reject |

The elevated‑rate regime coincides with structurally higher realized monthly inflation. This is an association across policy regimes, **not** a causal estimate of the rate's effect on inflation.

## Revalidation with the **daily** policy rate (`analysis_daily_revalidation.ipynb`)

The result is re‑derived from **Data2 — the daily policy rate** (`Tasa de política monetaria, Dato diario`), converted to monthly frequency by **monthly average** (preferred) and **end‑of‑month** (alternative). Inflation is independently reconstructed from the daily file's IPC *index level*. **The original finding is confirmed.**

| Source / conversion | Cycle start | Mean before | Mean after | Welch *p* | Decision |
|---|---|---|---|---|---|
| Monthly file (EoM) — primary | 2021‑10 | 0.44 % | 0.65 % | 0.0015 | Reject H₀ |
| **Daily → monthly average** | 2021‑10 | 0.43 % | 0.65 % | **0.0008** | Reject H₀ |
| Daily → end‑of‑month | 2021‑10 | 0.43 % | 0.65 % | 0.0008 | Reject H₀ |
| Daily average — 24m windows | 2021‑10 | 0.27 % | 0.49 % | 0.023 | Reject H₀ |

Validation of the daily→monthly build: derived inflation vs. DANE `variación mensual` **corr = 0.9999** (max diff 0.02 p.p.); rebuilt end‑of‑month rate reproduces the monthly file **exactly**; monthly‑average vs. end‑of‑month rate **corr = 0.999**, same cycle dates. The conversion method is immaterial to the conclusion.

## Repository layout

```
.
├── analysis.ipynb                    # primary analysis — monthly source file (start here)
├── analysis_daily_revalidation.ipynb # revalidation from the DAILY policy rate
├── data/
│   ├── datos.csv          # monthly policy rate + IPC monthly inflation (BANREP/DANE)
│   ├── datos_daily.csv    # DAILY policy rate + end-of-month IPC index level
│   └── informacion.csv    # series metadata / descriptions
├── fig_timeseries.png              # policy rate vs. inflation, cycle shaded
├── fig_distributions.png           # inflation by regime (boxplot) + window means
├── fig_seasonal.png                # seasonally matched monthly inflation
├── fig_daily_rate_conversions.png  # daily rate + monthly-average + end-of-month overlay
├── fig_daily_distributions.png     # daily-derived inflation by regime
├── requirements.txt
└── README.md
```

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
# or open analysis.ipynb in Jupyter / VS Code / Cursor and Run All
```

## Data source

Banco de la República (policy rate; monthly `Dato fin de mes` and daily `Dato diario`) and DANE (IPC). Downloaded July 2026. Monthly sample **Feb‑1998 → Jun‑2026**; daily sample **13‑Feb‑1998 → 26‑Jul‑2026**.
