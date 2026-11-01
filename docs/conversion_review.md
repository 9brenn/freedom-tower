# Independent conversion review

Reviewed tools/prepare.py and /workspace/conversion/reports/converted-xml.

Passed static checks:
- No duplicate archetype hashes across converted YTYP files.
- All nine placed CMloInstanceDef archetypes resolve to included YTYP definitions: lobby, garage, four apartments, three offices.
- Default furniture/decoration set names in three changed office YMAPs hash to existing set names in corresponding MLO archetypes.
- All entity origins, including optional entity sets, are inside repaired finite MLO bounds.
- Skipped hei_* vanilla replacement YMAPs contain no references to custom-named archetypes. Existing vanilla dependency manifests remain appropriate for their unchanged archetype names.
- Four corrected custom physics dictionary references match supplied YBN filenames; other local custom MLO physics names already matched.
- All six original source YMF files have empty MapDataGroups/HDTxdBindingArray/old imapDependencies, so regenerated manifest does not discard populated records in those sections.

No new blocking issue found in this review. Static parsing/readback does not establish actual in-game texture parenting, map collision replacement behavior, performance, portal visibility, or all asset streaming. Source gtxd.meta is absent and game runtime testing remains required.
