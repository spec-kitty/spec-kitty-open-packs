# Data Model: Analyze report

## Finding (carrier `analysis-findings/v1`, unchanged schema)

| Field | Rule |
|---|---|
| `id` | category prefix + number, stable across reruns on unchanged artifacts |
| `severity` | `low` / `medium` / `high` / `critical` only |
| `category` | one of the categories below |
| `summary` | one line; inferred findings start with `Inferred:` |

## Categories and id prefixes

| Category | Prefix | Source |
|---|---|---|
| duplication | D | existing pass A |
| ambiguity | B | existing pass B |
| underspecification | U | existing pass C |
| charter | K | existing pass D |
| coverage | C | existing pass E |
| inconsistency | I | existing pass F |
| finalize-validation | V | step 2a (#246) |
| wp-readiness | W | per-WP review (#237) |
| requirement-quality | Q | requirement quality and EARS (#247) |
| scenario | S | scenario audit (#247) |

## Severity map (new sources)

| Source | Severity |
|---|---|
| validation refusal | critical |
| validation could not run (old CLI, missing, no JSON, resolution error) | high |
| passing run: `tasks_md_stale`, non-empty `would_modify` | high |
| passing run: warnings | medium |
| passing run: collapsed lane | low |
| WP missing or orphaned; WP prompt missing a template section that implementation needs | high (blocker) |
| WP prompt without profile load first; oversized; overbroad; weak requirement mapping | medium or low (quality improvement) |
| untestable or ambiguous requirement | high when it changes what gets built, else medium |
| EARS / observable-behaviour wording | low or medium |
| scenario gap (missing edge, surprising accepted/rejected) | medium, high when it touches a security or data-loss path |

## Per-WP readiness row

`WP id | prompt file | in tasks.md | blockers (finding ids) | quality improvements (finding ids)`

## Scenario audit row (one table per user story)

`kind (accepted / rejected / missing edge / surprising accepted / surprising rejected) | scenario | location (spec.md / plan.md / tasks.md line)`
