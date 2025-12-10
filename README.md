# axiom-kg v0.2

**Semantic coordinates for derivable knowledge.**

Knowledge should not be stored. It should be derivable.

## What Changed in v0.2

v0.1 was a geometry engine. v0.2 reads the world.

Nine adapters that parse existing structured schemas into axiom-kg coordinates:

| Adapter | Schema | Pain Point Solved |
|---------|--------|-------------------|
| `SchemaOrgAdapter` | JSON-LD / Schema.org | Cross-site reasoning for ASW mesh |
| `OpenAPIAdapter` | OpenAPI / Swagger | API deduplication, breaking change detection |
| `RSSAdapter` | RSS / Atom | Track topic drift across news sources |
| `ICalAdapter` | iCalendar | Scheduling conflicts across calendars |
| `PackageAdapter` | npm, pip, cargo | Dependency graph across repos |
| `FHIRAdapter` | HL7 FHIR | Patient record matching without centralization |
| `XBRLAdapter` | XBRL | Structural comparison of financial filings |
| `EPUBAdapter` | EPUB / OPF | Publishing graph, author relationships |
| `AkomaNtosoAdapter` | Akoma Ntoso | Legal citation graph, amendment tracking |

## Installation

```bash
pip install axiom-kg
```

Or from source:
```bash
git clone https://github.com/BigBirdReturns/axiom-kg
cd axiom-kg
pip install -e .
```

## Quick Start

### Parse a Schema.org site (ASW)

```python
from axiom.adapters import SchemaOrgAdapter

adapter = SchemaOrgAdapter()

# Compare two AI-Structured Web sites
diff = adapter.compare_sites(
    "https://bitsnbytes.ai/ai.json",
    "https://structuredweb.org/ai.json"
)

print(f"Shared types: {diff['shared_types']}")
print(f"Potential forks: {diff['potential_forks']}")
```

### Compare two OpenAPI specs

```python
from axiom.adapters import OpenAPIAdapter

adapter = OpenAPIAdapter()

diff = adapter.compare_specs("api_v1.yaml", "api_v2.yaml")

print(f"Breaking changes: {len(diff['breaking_changes'])}")
for change in diff['breaking_changes']:
    print(f"  - {change['type']}: {change.get('endpoint', change.get('schema'))}")
```

### Find scheduling conflicts

```python
from axiom.adapters import ICalAdapter

adapter = ICalAdapter()

# Merge multiple calendars
all_events, conflicts = adapter.merge_calendars(
    "work.ics",
    "personal.ics",
    "team.ics"
)

print(f"Found {len(conflicts)} conflicts:")
for c in conflicts:
    print(f"  {c['event_a']} overlaps {c['event_b']}")
```

### Track news coverage drift

```python
from axiom.adapters import RSSAdapter

adapter = RSSAdapter()

# Compare two news sources
diff = adapter.compare_feeds(
    "https://example.com/rss/tech",
    "https://other.com/feed/technology"
)

print(f"Shared topics: {diff['shared_topics']}")
print(f"Similar stories: {len(diff['similar_stories'])}")
```

### Organization-wide dependency analysis

```python
from axiom.adapters import PackageAdapter
from pathlib import Path

adapter = PackageAdapter()

# Find all package.json files
manifests = list(Path("repos/").glob("**/package.json"))

graph = adapter.build_dependency_graph(manifests)

print(f"Projects: {len(graph['projects'])}")
print(f"Unique deps: {graph['unique_deps']}")
print("Most common:")
for dep in graph['most_common'][:5]:
    print(f"  {dep['name']}: used by {dep['used_by']} projects")
```

### Patient record matching (FHIR)

```python
from axiom.adapters import FHIRAdapter

adapter = FHIRAdapter()

# Parse FHIR bundles from two hospitals
nodes_a = adapter.parse("hospital_a_bundle.json")
nodes_b = adapter.parse("hospital_b_bundle.json")

# Find potential duplicates
all_nodes = nodes_a + nodes_b
duplicates = adapter.find_duplicate_patients(all_nodes)

for dup in duplicates:
    print(f"Potential match ({dup['match_score']:.0%}):")
    print(f"  A: {dup['patient_a']['name']} ({dup['patient_a']['birth_date']})")
    print(f"  B: {dup['patient_b']['name']} ({dup['patient_b']['birth_date']})")
```

## The Core Idea

Every adapter does the same thing:

1. **Parse** a domain-specific schema
2. **Assign** semantic coordinates (SemanticID)
3. **Return** Nodes that can be compared, derived, audited

The coordinates come from the schema's own structure. Schema.org types map to major categories. OpenAPI endpoints map to action coordinates. FHIR resources map to healthcare coordinates.

Once everything is in coordinates:
- **Distance** = conceptual similarity
- **Forks** = explicit disagreement
- **Derivation** = inferred relationships
- **Audit** = cryptographic trail

## The 927x Claim

From v0.1: A knowledge graph with 927 derivable relationships stored only 1 seed concept.

v0.2 extends this: Adapters derive coordinates from existing schemas. You don't manually map concepts. The structure is already there.

## Architecture

```
axiom-kg/
├── axiom/
│   ├── __init__.py          # Package exports
│   ├── core.py              # Geometry engine (unchanged from v0.1)
│   └── adapters/
│       ├── __init__.py      # Adapter exports
│       ├── base.py          # BaseAdapter, JSONAdapter, XMLAdapter
│       ├── schemaorg.py     # Schema.org / JSON-LD
│       ├── openapi.py       # OpenAPI / Swagger
│       ├── rss.py           # RSS / Atom feeds
│       ├── ical.py          # iCalendar
│       ├── package.py       # npm, pip, cargo
│       ├── fhir.py          # HL7 FHIR
│       ├── xbrl.py          # XBRL financial
│       ├── epub.py          # EPUB metadata
│       └── akn.py           # Akoma Ntoso legal
├── examples/
├── tests/
└── README.md
```

## Writing Your Own Adapter

```python
from axiom.adapters import BaseAdapter
from axiom.core import Node, SemanticID

class MyAdapter(BaseAdapter):
    DOMAIN_NAME = "mydomain"
    
    def parse(self, source):
        nodes = []
        
        # Your parsing logic here
        data = self.load_data(source)
        
        for item in data:
            # Assign coordinates based on domain structure
            sem_id = self.create_id(
                major=1,      # Entity
                type_=item["category"],
                subtype=1
            )
            
            node = Node(
                id=sem_id,
                label=item["name"],
                metadata=item
            )
            nodes.append(node)
        
        return nodes
```

## Related Projects

- **[AI-Structured Web](https://structuredweb.org)**: Protocol for machine-first websites. axiom-kg provides the semantic layer.
- **[Screen Ghost](https://github.com/BigBirdReturns/ScreenGhost)**: UI automation capture. axiom-kg provides the coordinate system.
- **[GhostBox](https://github.com/BigBirdReturns/ghostbox)**: Integrated stack with attention geometry.

## Philosophy

> "The semantic baseline is the coordinate system you inherit from your domain. Axiom-kg doesn't ship with universal ontology because there isn't one. It ships with adapters for building domain-specific ones."

Schemas already exist. Standards already exist. We're not inventing a new way to describe the world. We're making existing descriptions computable.

## License

MIT

## Author

Jonathan Sandhu / Sandhu Consulting Group

---

*This is how it's done.*
