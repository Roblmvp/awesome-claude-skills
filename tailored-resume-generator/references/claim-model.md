# Resume Claim Model

Classify every assertion before drafting. Preserve a stable evidence identifier so every employer-facing statement can be traced.

| Status                                 | Meaning                                                         | Employer-facing eligibility                                                  |
| -------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `verified_candidate_fact`              | Supported by an identified authoritative candidate source       | Eligible                                                                     |
| `candidate_confirmed_fact`             | Explicitly confirmed by the candidate                           | Eligible                                                                     |
| `approximate_candidate_confirmed_fact` | Candidate explicitly confirms that a value is approximate       | Eligible only with approximation language                                    |
| `transferable_experience`              | Supported adjacent experience relevant to a requirement         | Eligible only when labeled transferable/adjacent; never claim direct mastery |
| `job_requirement`                      | Stated by the employer                                          | Ineligible as a candidate claim                                              |
| `inferred_possibility`                 | Plausible but not evidenced                                     | Ineligible; ask for confirmation if material                                 |
| `unknown`                              | Missing or unresolved information                               | Ineligible; retain as unknown                                                |
| `prohibited_unsupported_claim`         | Contradicted, fabricated, or presented without required support | Prohibited                                                                   |

An eligible record includes `text`, `status`, and a nonempty `evidence_id`. Approximate facts also include `approximate: true`. Transferable records include `label: "transferable experience"`. Requirements, possibilities, unknowns, and prohibited claims belong in the gap analysis, never the resume.
