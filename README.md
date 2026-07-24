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

## Repository layout

```
.
├── analysis.ipynb        # full, executed analysis (start here)
├── data/
│   ├── datos.csv         # monthly policy rate + IPC monthly inflation (BANREP/DANE)
│   └── informacion.csv   # series metadata / descriptions
├── fig_timeseries.png    # policy rate vs. inflation, cycle shaded
├── fig_distributions.png # inflation by regime (boxplot) + window means
├── fig_seasonal.png      # seasonally matched monthly inflation
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

Banco de la República (policy rate) and DANE (IPC), downloaded July 2026. Monthly sample **Feb‑1998 → Jun‑2026**.
