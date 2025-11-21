# Other / Unclear Ontology Proposal

This outlines a fallback taxonomy to replace the catch-all "Other / Unclear" sector used in `osf_globe.html`. It can be applied when purpose text does not clearly map to the primary nine sectors.

## Cross-cutting capacity & ops
* Keywords: infrastructure, platform maintenance, tooling, internal systems, operations, finance, accounting, HR, compliance, audit, security, risk management, data stewardship.
* Rationale: Distinguishes back-office capacity building and operational resilience from programmatic work.

## Philanthropy & field support
* Keywords: regranting, intermediary, donor collaborative, pooled fund, fiscal sponsorship, landscape scan, field mapping, ecosystem support, TA/technical assistance for grantees.
* Rationale: Captures meta-grantmaking and field-strengthening efforts that enable others to deliver programs.

## Convenings & networks
* Keywords: conference, convening, summit, forum, workshop series, network building, cohort, alliance, consortium, community of practice.
* Rationale: Separates relationship-building and knowledge exchange from direct service or advocacy.

## Cross-sector innovation & pilots
* Keywords: pilot, prototype, innovation, lab, experiment, incubator, accelerator, sandbox, cross-sector collaboration, multi-stakeholder.
* Rationale: Identifies exploratory work that intentionally spans multiple sectors without a dominant theme.

## Emergency & relief
* Keywords: emergency, relief, rapid response, contingency, crisis, disaster, humanitarian, urgent support.
* Rationale: Tags time-bound support that cuts across sectors but is driven by immediacy rather than thematic fit.

## Administration-only
* Keywords: rent, utilities, office equipment, basic administration, bookkeeping, payroll services, insurance, registration fees.
* Rationale: Flags purely administrative expenditures that are neither programmatic nor strategic capacity-building.

## Unclassifiable / insufficient detail
* Criteria: purpose text is blank or too vague to infer intent; retain as true catch-all.
* Rationale: Maintains a minimal bucket for genuinely indeterminate cases after all other rules are attempted.

## Implementation notes
* Apply these buckets only after exhausting the primary sector regexes in `SECTOR_RULES` and the nudge/spawn rule set.
* Limit to one fallback tag per grant to preserve clarity; prefer the first matched bucket in the above order.
* Keep color mapping simple (e.g., reuse `Other / Unclear` hue) unless UI design introduces distinct colors for these subtypes.
* In the globe implementation, these buckets activate **only when no primary sector matched**, so existing Media & Journalism (or any
  other primary sector) grants stay untouched while ambiguous purposes are re-bucketed.
