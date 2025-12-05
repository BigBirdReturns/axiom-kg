# Axiom

**Semantic coordinates for derivable knowledge.**

Store the minimal structure from which all answers can be derived.

```
Stored:    6 nodes, 3 relations
Derived:   siblings, categories, paths, distances, tension, forks
Ratio:     927x more derivable than stored
```

---

## The Problem

Every AI knowledge system makes the same mistake: they store answers instead of structure.

- **RAG** stores chunks and retrieves them. The retrieval is a guess.
- **Embeddings** encode similarity, not structure. You can find "near" things but cannot derive new things.
- **Transformers** bake knowledge into weights. You cannot inspect it, update it, or derive from it.

When these systems fail, they fail silently. They cannot explain why. They cannot be audited. They cannot be fixed without retraining.

## The Insight

Knowledge should not be stored. It should be **derivable**.

Like mathematics: you don't store every equation. You store axioms and derivation rules. Everything else is generated on demand.

Like DNA: you don't store the organism. You store the instructions for building it.

Like a seed: the tree is not in the seed. The *potential* for the tree is in the seed.

## The Solution

Axiom is a semantic coordinate system. Every concept gets a position in knowledge space:

```
MM-TT-SS-XXXX
│  │  │  │
│  │  │  └── Instance (unique concept)
│  │  └───── Subtype (within type)
│  └──────── Type (within category)
└─────────── Major category (the 8 axioms)
```

From coordinates alone, you can derive:
- **Siblings** — concepts that share a type
- **Categories** — all concepts of a kind
- **Distance** — how far apart two concepts are
- **Paths** — how concepts connect through relations

You store a few nodes and relations. You derive everything else.

## Quick Example

```python
from axiom import Space, Node, SemanticID, RelationType

# Create the space
space = Space()

# Add some concepts with coordinates
animal = space.add(Node(
    id=SemanticID.create(1, 1, 1, 1),  # Entity > Living > Animal > 1
    label="animal"
))

feline = space.add(Node(
    id=SemanticID.create(1, 1, 2, 1),  # Entity > Living > Feline > 1
    label="feline"
))

jaguar = space.add(Node(
    id=SemanticID.create(1, 1, 2, 2),  # Entity > Living > Feline > 2
    label="jaguar"
))

# Add one relation
space.add_relation(feline, RelationType.IS_A, animal)

# Now derive
siblings = space.derive_siblings(feline)
# Returns: [animal, jaguar] — computed from coordinates, not stored

distance = feline.id.distance(jaguar.id)
# Returns: 1 — they share subtype, computed from geometry

path = space.derive_path(feline, animal)
# Returns: [feline, animal] — traversed the relation
```

## Handling Ambiguity

When a concept has multiple meanings, Axiom makes it explicit:

```python
# "jaguar" is ambiguous
fork, branches = space.create_fork(jaguar, ["animal", "car"])

# Now we have:
# - jaguar:animal (01-01-02-0003)
# - jaguar:car (01-01-02-0004)

# Each branch can have its own relations
space.add_relation(branches[0], RelationType.IS_A, feline)
space.add_relation(branches[1], RelationType.IS_A, car)

# Tension tells you something needs disambiguation
tension = space.derive_tension(jaguar)
# Returns: 3.0 — high tension, multiple forks
```

## The Audit Trail

Every operation is logged with cryptographic signatures:

```python
# Check the audit log
for entry in space.audit.last(5):
    print(f"[{entry.hash[:12]}] {entry.action}: {entry.args}")

# Verify chain integrity
assert space.audit.verify()  # True if untampered
```

## The Wrapper Pattern

Axiom implements [deterministic wrappers](https://fakesoap.com/deterministic-wrappers) — a pattern for making AI systems accountable:

```python
from axiom import DeterministicWrapper, Strategy

wrapper = DeterministicWrapper()

# The wrapper constrains the system to explicit strategies
decision = wrapper.handle("jaguar", context={"domain": "automotive"})

# Decision contains:
# - strategy: Strategy.CREATE_NODE or RETURN_EXISTING or CREATE_FORK
# - result: the node(s)
# - audit_hash: cryptographic proof of what happened
```

Instead of allowing arbitrary outputs, the system must:
1. Select from a finite set of strategies
2. Apply the strategy deterministically
3. Log everything with cryptographic proof

The neural component (if any) provides intelligence.
The wrapper provides accountability.

## Installation

```bash
pip install axiom-kg
```

Or from source:

```bash
git clone https://github.com/bigbirdreturns/axiom-kg
cd axiom-kg
pip install -e .
```

## Run the Demo

```bash
python examples/growth.py
```

Output:
```
======================================================================
AXIOM: FROM SEED TO FOREST
======================================================================

[1] PLANTING THE SEED: Minimal structure

   Stored nodes:     6
   Stored relations: 3
   This is ALL we store.

[2] DERIVATION: Growing knowledge from structure

   Q: What's related to 'feline'?
   A: ['animal', 'canine', 'jaguar']
      (DERIVED from shared type coordinates)

...

[7] DERIVATION SPACE

   Total derivable: ~1,000,000
   Total stored:    1,079

   RATIO: 927x more derivable than stored
```

## The 8 Categories

Everything derives from 8 major categories:

| Code | Category | What it covers |
|------|----------|----------------|
| 1 | Entity | Things that exist |
| 2 | Action | Things that happen |
| 3 | Property | Qualities of things |
| 4 | Relation | Connections between things |
| 5 | Location | Where things are |
| 6 | Time | When things happen |
| 7 | Quantity | How much/many |
| 8 | Abstract | Ideas, concepts, patterns |

## Relation Types

Start with 8, grow to 128:

- `IS_A` — taxonomic (feline is_a animal)
- `PART_OF` — mereological (wheel part_of car)
- `HAS_PROPERTY` — attributive (fire has_property hot)
- `CAUSES` — causal (rain causes wetness)
- `LOCATED_IN` — spatial (paris located_in france)
- `OCCURS_AT` — temporal (meeting occurs_at tuesday)
- `SIMILAR_TO` — analogical (wolf similar_to dog)
- `CONTRADICTS` — oppositional (hot contradicts cold)

## Why "Axiom"?

In mathematics, axioms are the minimal statements from which everything else can be derived. You don't store theorems — you derive them from axioms.

Axiom applies this principle to knowledge systems:
- Store the coordinates (where concepts are)
- Store the relations (how they connect)
- Derive everything else (what they mean together)

## Project Status

**v0.1.0** — The seed.

This is a reference implementation in Python. It demonstrates the pattern. For production use cases requiring performance, a Rust implementation is planned.

Current:
- ✅ Semantic coordinate system
- ✅ Derivation rules (siblings, categories, paths, tension)
- ✅ Fork mechanism for ambiguity
- ✅ Cryptographic audit logging
- ✅ Deterministic wrapper interface

Planned:
- ⬜ Persistence layer
- ⬜ Query language
- ⬜ REST API
- ⬜ Rust core

## Related Work
- [FakeSoap](https://fakesoap.com) — cultural criticism and power structure analysis

## License

MIT

## Author

Jonathan Sandhu ([@bigbirdreturns](https://github.com/bigbirdreturns))

---

*The system derives. It doesn't retrieve. It doesn't guess.*
*It knows how to know.*
