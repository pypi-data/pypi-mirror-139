from __future__ import annotations
from typing import Set, Tuple, Dict, Optional

from octofludb.nomenclature import (
    uidgen,
    P,
    make_property,
    make_uri,
    make_date,
    make_country_uri,
    make_usa_state_uri,
    make_literal,
    make_integer,
)
from octofludb.util import safeAdd
from octofludb.hash import chksum
from rdflib.term import Node
import re
import octofludb.domain_identifier as identifier
import octofludb.domain_flu as flu
import octofludb.domain_animal as animal
from octofludb.util import log
from octofludb.colors import bad
import octofludb.domain_geography as geo


def make_maybe_add(
    g: Set[Tuple[Node, Node, Node]], meta: Dict[str, Optional[str]], sid: Optional[Node]
):
    def maybe_add(p, key, formatter=lambda x: make_literal(x, infer=False)):
        if key in meta and meta[key] is not None:
            safeAdd(g, sid, p, formatter(meta[key]))

    return maybe_add


def make_gb_meta_triples(
    gb_meta: dict, only_influenza_a: bool = True
) -> Tuple[Set[Tuple[Node, Node, Node]], str]:
    """
    Add genbank triples

    Parameters
    ----------
    g : rdflib Graph object
    gb_meta : Genbank metadata dictionary from Bio.Entrez
    only_influenza_a : bool

    Returns
    -------
    string containing any raised error or warning message
    """

    g: Set[Tuple[Node, Node, Node]] = set()  # triples

    error_entry = ""

    try:
        accession = str(gb_meta["GBSeq_primary-accession"])
    except:
        log(bad("Bad Genbank Entry"))
        return (g, "Unknown\tNo primary accession")

    if only_influenza_a:
        # ignore this entry if the organism is not specified
        if "GBSeq_organism" not in gb_meta:
            return (g, f"{accession}\tNo organsim specified")
        # ignore this entry if the organism is not an Influenza virus
        if not bool(re.match("Influenza [ABCD] virus", gb_meta["GBSeq_organism"])):
            return (g, f"{accession}\tNot influenza")

    gid = make_uri(accession)
    safeAdd(g, gid, P.gb, make_literal(accession, infer=False))

    maybe_add = make_maybe_add(g, gb_meta, gid)

    maybe_add(P.gb_locus, "GBSeq_locus")
    maybe_add(P.gb_length, "GBSeq_length", formatter=make_integer)
    maybe_add(P.gb_strandedness, "GBSeq_strandedness")
    maybe_add(P.gb_moltype, "GBSeq_moltype")
    maybe_add(P.gb_topology, "GBSeq_topology")
    maybe_add(P.gb_division, "GBSeq_division")
    maybe_add(P.gb_update_date, "GBSeq_update-date", formatter=make_date)
    maybe_add(P.gb_create_date, "GBSeq_create-date", formatter=make_date)
    maybe_add(P.gb_definition, "GBSeq_definition")
    maybe_add(P.gb_primary_accession, "GBSeq_primary_accession")
    maybe_add(P.gb_accession_version, "GBSeq_accession-version")
    maybe_add(P.gb_source, "GBSeq_source")
    maybe_add(P.gb_organism, "GBSeq_organism")
    maybe_add(P.gb_taxonomy, "GBSeq_taxonomy")

    # usually an entry has sequence, but there are weird exceptions
    if "GBSeq_sequence" in gb_meta:
        seq = gb_meta["GBSeq_sequence"].upper()
        safeAdd(g, gid, P.dnaseq, make_literal(seq, infer=False))
        safeAdd(g, gid, P.chksum, make_literal(chksum(seq), infer=False))

    strain = None
    host = None
    date = None
    country = None

    igen = uidgen(base=accession + "_feat_")
    for feat in gb_meta["GBSeq_feature-table"]:
        fid = next(igen)
        safeAdd(g, gid, P.has_feature, fid)
        safeAdd(g, fid, P.name, make_literal(feat["GBFeature_key"], infer=False))

        maybe_add = make_maybe_add(g, feat, fid)
        maybe_add(P.gb_location, "GBFeature_location")
        #  maybe_add(P.gb_key, "GBFeature_intervals") # for laters

        if "GBFeature_quals" in feat:
            for qual in feat["GBFeature_quals"]:
                if not ("GBQualifier_name" in qual and "GBQualifier_value" in qual):
                    continue
                key = qual["GBQualifier_name"]
                val = qual["GBQualifier_value"]

                if key == "translation":
                    g.add((fid, P.proseq, make_literal(val, infer=False)))
                    g.add((fid, P.chksum, make_literal(chksum(val), infer=False)))
                elif key == "strain":
                    try:
                        strain = identifier.p_strain.parse(val)
                    except:
                        log(bad("Bad strain name: ") + val)
                        error_entry = f"{val}\tBad strain name"
                        strain = val
                elif key == "collection_date":
                    date = make_date(val)
                elif key == "host":
                    host = val
                elif key == "country":
                    country = re.sub(":.*", "", val)
                elif key == "gene":
                    try:
                        segment_name = flu.p_segment.parse_strict(val)
                        # attach the segment_name to the top-level genbank record, not the feature
                        safeAdd(
                            g,
                            gid,
                            P.segment_name,
                            make_literal(segment_name, infer=False),
                        )
                    except:
                        pass
                    # attach the original, unparsed gene name to the feature
                    safeAdd(g, fid, make_property(key), make_literal(val, infer=True))
                else:
                    safeAdd(g, fid, make_property(key), make_literal(val, infer=True))

    # link strain information
    if strain:
        sid = make_uri(strain)
        safeAdd(g, sid, P.has_segment, gid)
        safeAdd(g, sid, P.strain_name, make_literal(strain, infer=False))
        if host:
            safeAdd(g, sid, P.host, make_literal(animal.clean_host(host), infer=False))
        if date:
            safeAdd(g, sid, P.date, date)
        if country:
            code = geo.country_to_code(country)
            country_uri = make_country_uri(country)
            safeAdd(g, sid, P.country, country_uri)
            if code is None:
                # if this is an unrecognized country (e.g., Kosovo) then state
                g.add((country_uri, P.name, make_literal(country, infer=False)))
            if code == "USA":
                fields = strain.split("/")
                for field in fields[1:]:
                    # If this looks like a US state, add it
                    code = geo.state_to_code(field)
                    if code:
                        safeAdd(g, sid, P.state, make_usa_state_uri(code))
                    # If this looks like an A0 number, add it
                    try:
                        A0 = identifier.p_A0.parse_strict(field)
                        safeAdd(g, sid, P.barcode, make_literal(A0, infer=False))
                    except:
                        pass
    else:
        locus = gb_meta["GBSeq_locus"]
        log(bad("Missing strain: ") + locus)
        error_entry = f"{locus}\tNo strain name"

    return (g, error_entry)
