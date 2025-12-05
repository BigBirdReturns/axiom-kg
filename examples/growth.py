#!/usr/bin/env python3
"""
Axiom: From Seed to Forest

This demo shows the core thesis:
- Store minimal structure
- Derive everything else
- Audit every operation

Watch 6 concepts and 3 relations expand into a million derivable queries.
"""

import sys
import os
import random

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from axiom import (
    Space, 
    Node, 
    SemanticID, 
    RelationType,
    MAJOR_CATEGORIES,
)


def print_header(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_section(num: int, title: str) -> None:
    print(f"\n[{num}] {title}\n")


# =============================================================================
# PART 1: THE SEED
# =============================================================================

def demonstrate_seed():
    """Plant a minimal seed and watch it derive."""
    
    print_header("AXIOM: FROM SEED TO FOREST")
    
    # Create the empty space
    space = Space()
    
    # -------------------------------------------------------------------------
    print_section(1, "PLANTING THE SEED: Minimal structure")
    # -------------------------------------------------------------------------
    
    # Some entities (major category 1)
    animal = space.add(Node(
        id=SemanticID.create(1, 1, 1, 1),
        label="animal"
    ))
    
    feline = space.add(Node(
        id=SemanticID.create(1, 1, 2, 1),
        label="feline"
    ))
    
    canine = space.add(Node(
        id=SemanticID.create(1, 1, 3, 1),
        label="canine"
    ))
    
    vehicle = space.add(Node(
        id=SemanticID.create(1, 2, 1, 1),
        label="vehicle"
    ))
    
    car = space.add(Node(
        id=SemanticID.create(1, 2, 2, 1),
        label="car"
    ))
    
    # The ambiguous one
    jaguar = space.add(Node(
        id=SemanticID.create(1, 1, 2, 2),
        label="jaguar"
    ))
    
    # Establish taxonomic relations
    space.add_relation(feline, RelationType.IS_A, animal)
    space.add_relation(canine, RelationType.IS_A, animal)
    space.add_relation(car, RelationType.IS_A, vehicle)
    
    print(f"   Stored nodes:     {space.node_count}")
    print(f"   Stored relations: {space.relation_count}")
    print(f"   This is ALL we store.")
    
    # -------------------------------------------------------------------------
    print_section(2, "DERIVATION: Growing knowledge from structure")
    # -------------------------------------------------------------------------
    
    # Derive siblings (computed from coordinates, not stored)
    siblings = space.derive_siblings(feline)
    print(f"   Q: What's related to 'feline'?")
    print(f"   A: {[s.label for s in siblings]}")
    print(f"      (DERIVED from shared type coordinates)")
    
    # Derive category members
    entities = space.derive_category(1)
    print(f"\n   Q: What entities exist?")
    print(f"   A: {[e.label for e in entities]}")
    print(f"      (DERIVED from major category)")
    
    # Derive path (reasoning through structure)
    print(f"\n   Q: How is 'feline' related to 'animal'?")
    path = space.derive_path(feline, animal)
    if path:
        path_str = " → ".join(
            p.label if isinstance(p, Node) else str(p) 
            for p in path
        )
        print(f"   A: {path_str}")
        print(f"      (DERIVED by traversing relations)")
    
    # Derive semantic distance
    print(f"\n   Q: How far is 'feline' from 'car'?")
    dist = feline.id.distance(car.id)
    print(f"   A: Distance = {dist}")
    print(f"      (DERIVED from coordinate geometry)")
    
    # -------------------------------------------------------------------------
    print_section(3, "FORKING: Explicit ambiguity handling")
    # -------------------------------------------------------------------------
    
    # "jaguar" is ambiguous - fork it
    fork, branches = space.create_fork(jaguar, ["animal", "car"])
    
    print(f"   '{jaguar.label}' has forked into:")
    for branch in branches:
        print(f"      • {branch.label} ({branch.id.code})")
    
    # Connect the branches to their proper parents
    jaguar_animal = branches[0]
    jaguar_car = branches[1]
    space.add_relation(jaguar_animal, RelationType.IS_A, feline)
    space.add_relation(jaguar_car, RelationType.IS_A, car)
    
    # Derive tension
    tension = space.derive_tension(jaguar)
    print(f"\n   Tension at '{jaguar.label}': {tension:.2f}")
    print(f"      (High tension = needs disambiguation)")
    
    # -------------------------------------------------------------------------
    print_section(4, "AUDIT TRAIL: Cryptographic proof")
    # -------------------------------------------------------------------------
    
    print(f"   Total operations logged: {len(space.audit)}")
    print(f"   Chain integrity valid:   {space.audit.verify()}")
    print(f"\n   Last 5 entries:")
    for entry in space.audit.last(5):
        print(f"      [{entry.hash[:12]}...] {entry.action}: {entry.args[:3]}")
    
    # -------------------------------------------------------------------------
    print_section(5, "THE POINT")
    # -------------------------------------------------------------------------
    
    print(f"""   We stored:  {space.node_count} nodes, {space.relation_count} relations
   We derived: siblings, categories, paths, distances, tension, forks
   
   The STRUCTURE is tiny.
   The DERIVATION SPACE is infinite.
   
   • Add a new concept? It finds its coordinates.
   • Query a relationship? Derived from position.
   • Detect ambiguity? Visible in fork structure.
   • Audit the reasoning? Every step is logged.
   
   This is the seed. The tree grows from here.""")
    
    return space


# =============================================================================
# PART 2: THE FOREST
# =============================================================================

def demonstrate_scale():
    """Show how derivation scales."""
    
    print_header("SCALING: THE SEED BECOMES A FOREST")
    
    space = Space()
    
    print_section(6, "ADDING 1,000 CONCEPTS...")
    
    # Add 1000 concepts with proper coordinates
    for i in range(1000):
        major = random.randint(1, 8)
        type_ = random.randint(1, 16)
        subtype = random.randint(1, 16)
        instance = i + 1
        
        node = Node(
            id=SemanticID.create(major, type_, subtype, instance),
            label=f"concept_{i}"
        )
        
        # Sparse relations (~10%)
        if i > 0 and random.random() < 0.1:
            other = random.choice(space.nodes())
            node.add_relation(RelationType.SIMILAR_TO, other)
        
        space.add(node)
    
    print(f"   Stored nodes:     {space.node_count}")
    print(f"   Stored relations: {space.relation_count}")
    
    # Pick a random concept to test
    test = random.choice(space.nodes())
    siblings = space.derive_siblings(test)
    category = space.derive_category(test.id.major)
    
    print(f"\n   Test node: {test.label} ({test.id.code})")
    print(f"   Category:  {test.id.category_name}")
    print(f"   Derived siblings: {len(siblings)}")
    print(f"   Derived category members: {len(category)}")
    
    # -------------------------------------------------------------------------
    print_section(7, "DERIVATION SPACE")
    # -------------------------------------------------------------------------
    
    n = space.node_count
    stored = n + space.relation_count
    derivable = n * n  # pairwise queries
    ratio = derivable / stored
    
    print(f"   Sibling queries possible:  {n:,}")
    print(f"   Category queries possible: 8")
    print(f"   Path queries possible:     {derivable:,}")
    print(f"   Tension queries possible:  {n:,}")
    print(f"\n   Total derivable: ~{derivable:,}")
    print(f"   Total stored:    {stored:,}")
    print(f"\n   RATIO: {ratio:,.0f}x more derivable than stored")
    
    # -------------------------------------------------------------------------
    print_header("THE THESIS")
    # -------------------------------------------------------------------------
    
    print("""
   RAG stores chunks and retrieves them.
   Embeddings encode similarity, not structure.
   Transformers bake knowledge into weights.
   
   Axiom DERIVES. It doesn't retrieve. It doesn't guess.
   
   Knowledge should not be stored.
   It should be derivable from minimal structure.
   
   Like mathematics: axioms and derivation rules.
   Like DNA: instructions, not organisms.
   Like a seed: the potential for the tree.
   
   This is that seed.
""")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    demonstrate_seed()
    demonstrate_scale()
