"""Promotion layer: SourceCandidate -> Source Registry.

First vertical slice: the promote_new path only (approved + unique candidate ->
new Source + PromotionEvent audit record), on SQLite-backed transactional storage
(see docs/promotion_storage_design.md) with the JSON Schemas as validation contracts.

This package is DETERMINISTIC code. No LLM reasoning participates in the promotion
path (gates, mapping, safety derivation, transaction). See docs/promotion_workflow.md.

NOT yet implemented (out of scope for this slice): merge_into_existing,
update_existing, reject/retire, deactivate cascade, and crash recovery/reconciliation.
"""

__version__ = "0.1.0-slice"
