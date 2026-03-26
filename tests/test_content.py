from __future__ import annotations

from euclidyne_web.claims import CLAIMS
from euclidyne_web.facts import FACTS
from euclidyne_web.lab_registry import LAB_ENTRIES, LAB_GROUPS
from euclidyne_web.page_builders import build_home_page, build_references_page
from euclidyne_web.sources import SOURCE_ENTRIES


def test_lab_registry_references_known_claims_sources_and_related_labs():
    claim_ids = {claim["id"] for claim in CLAIMS}
    source_ids = {entry.id for entry in SOURCE_ENTRIES}
    lab_slugs = {entry.slug for entry in LAB_ENTRIES}

    for lab in LAB_ENTRIES:
        assert set(lab.claim_ids) <= claim_ids
        assert set(lab.source_ids) <= source_ids
        assert set(lab.related_labs) <= lab_slugs


def test_claims_reference_known_labs_and_sources():
    lab_slugs = {entry.slug for entry in LAB_ENTRIES}
    source_ids = {entry.id for entry in SOURCE_ENTRIES}

    for claim in CLAIMS:
        assert set(claim["lab_slugs"]) <= lab_slugs
        assert set(claim["source_ids"]) <= source_ids


def test_facts_reference_known_labs_and_sources():
    lab_slugs = {entry.slug for entry in LAB_ENTRIES} | {"home"}
    source_ids = {entry.id for entry in SOURCE_ENTRIES}

    for fact in FACTS:
        assert set(fact["lab_slugs"]) <= lab_slugs
        assert fact["source_id"] in source_ids


def test_home_page_and_references_page_are_internally_consistent():
    home = build_home_page()
    references = build_references_page()

    assert len(home["atlas_groups"]) == len(LAB_GROUPS)
    assert sum(home["claim_status_counts"].values()) == len(CLAIMS)
    assert len(references["claims"]) == len(CLAIMS)
    assert len(references["facts"]) == len(FACTS)
    assert len(references["sources"]) == len(SOURCE_ENTRIES)
