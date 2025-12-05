"""
Tests for Axiom core functionality.
Run with: python -m pytest tests/ -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from axiom import (
    SemanticID,
    SemanticIDError,
    Node,
    Space,
    RelationType,
    Fork,
    AuditLog,
    DeterministicWrapper,
    Strategy,
    MAJOR_CATEGORIES,
)


class TestSemanticID:
    """Test semantic coordinate system."""
    
    def test_create_valid(self):
        sid = SemanticID.create(1, 2, 3, 4)
        assert sid.major == 1
        assert sid.type_ == 2
        assert sid.subtype == 3
        assert sid.instance == 4
        assert sid.code == "01-02-03-0004"
    
    def test_parse_valid(self):
        sid = SemanticID.parse("05-10-15-0999")
        assert sid.major == 5
        assert sid.type_ == 10
        assert sid.subtype == 15
        assert sid.instance == 999
    
    def test_parse_invalid_format(self):
        with pytest.raises(SemanticIDError):
            SemanticID.parse("invalid")
    
    def test_major_out_of_range(self):
        with pytest.raises(SemanticIDError):
            SemanticID.create(0, 1, 1, 1)
        with pytest.raises(SemanticIDError):
            SemanticID.create(9, 1, 1, 1)
    
    def test_shares_category(self):
        a = SemanticID.create(1, 1, 1, 1)
        b = SemanticID.create(1, 2, 3, 4)
        c = SemanticID.create(2, 1, 1, 1)
        
        assert a.shares_category(b)
        assert not a.shares_category(c)
    
    def test_shares_type(self):
        a = SemanticID.create(1, 2, 1, 1)
        b = SemanticID.create(1, 2, 3, 4)
        c = SemanticID.create(1, 3, 1, 1)
        
        assert a.shares_type(b)
        assert not a.shares_type(c)
    
    def test_distance(self):
        base = SemanticID.create(1, 2, 3, 1)
        same = SemanticID.create(1, 2, 3, 1)
        cousin = SemanticID.create(1, 2, 3, 2)
        sibling = SemanticID.create(1, 2, 4, 1)
        relative = SemanticID.create(1, 3, 1, 1)
        stranger = SemanticID.create(2, 1, 1, 1)
        
        assert base.distance(same) == 0
        assert base.distance(cousin) == 1
        assert base.distance(sibling) == 2
        assert base.distance(relative) == 3
        assert base.distance(stranger) == 4
    
    def test_category_name(self):
        for major, name in MAJOR_CATEGORIES.items():
            sid = SemanticID.create(major, 1, 1, 1)
            assert sid.category_name == name


class TestNode:
    """Test node functionality."""
    
    def test_create_node(self):
        node = Node(
            id=SemanticID.create(1, 1, 1, 1),
            label="test"
        )
        assert node.label == "test"
        assert node.id.code == "01-01-01-0001"
    
    def test_add_relation(self):
        a = Node(id=SemanticID.create(1, 1, 1, 1), label="a")
        b = Node(id=SemanticID.create(1, 1, 1, 2), label="b")
        
        a.add_relation(RelationType.IS_A, b)
        
        assert b.id.code in a.get_relations(RelationType.IS_A)
        assert a.relation_count() == 1
    
    def test_serialization(self):
        node = Node(
            id=SemanticID.create(1, 2, 3, 4),
            label="test",
            metadata={"key": "value"}
        )
        
        data = node.to_dict()
        restored = Node.from_dict(data)
        
        assert restored.id == node.id
        assert restored.label == node.label
        assert restored.metadata == node.metadata


class TestSpace:
    """Test semantic space functionality."""
    
    def test_add_and_get(self):
        space = Space()
        node = Node(id=SemanticID.create(1, 1, 1, 1), label="test")
        
        space.add(node)
        
        assert space.get(node.id) == node
        assert space.get("01-01-01-0001") == node
    
    def test_add_duplicate_fails(self):
        space = Space()
        node = Node(id=SemanticID.create(1, 1, 1, 1), label="test")
        
        space.add(node)
        
        with pytest.raises(ValueError):
            space.add(node)
    
    def test_find_by_label(self):
        space = Space()
        space.add(Node(id=SemanticID.create(1, 1, 1, 1), label="Apple"))
        space.add(Node(id=SemanticID.create(1, 1, 1, 2), label="apple"))
        space.add(Node(id=SemanticID.create(1, 1, 1, 3), label="Banana"))
        
        # Case insensitive
        results = space.find_by_label("apple")
        assert len(results) == 2
        
        # Case sensitive
        results = space.find_by_label("Apple", case_sensitive=True)
        assert len(results) == 1
    
    def test_derive_siblings(self):
        space = Space()
        # Same type (1, 1, X, X)
        a = space.add(Node(id=SemanticID.create(1, 1, 1, 1), label="a"))
        b = space.add(Node(id=SemanticID.create(1, 1, 2, 1), label="b"))
        c = space.add(Node(id=SemanticID.create(1, 1, 3, 1), label="c"))
        # Different type
        d = space.add(Node(id=SemanticID.create(1, 2, 1, 1), label="d"))
        
        siblings = space.derive_siblings(a)
        labels = [s.label for s in siblings]
        
        assert "b" in labels
        assert "c" in labels
        assert "d" not in labels
        assert "a" not in labels
    
    def test_derive_category(self):
        space = Space()
        space.add(Node(id=SemanticID.create(1, 1, 1, 1), label="entity1"))
        space.add(Node(id=SemanticID.create(1, 2, 1, 1), label="entity2"))
        space.add(Node(id=SemanticID.create(2, 1, 1, 1), label="action1"))
        
        entities = space.derive_category(1)
        actions = space.derive_category(2)
        
        assert len(entities) == 2
        assert len(actions) == 1
    
    def test_derive_path(self):
        space = Space()
        a = space.add(Node(id=SemanticID.create(1, 1, 1, 1), label="a"))
        b = space.add(Node(id=SemanticID.create(1, 1, 1, 2), label="b"))
        c = space.add(Node(id=SemanticID.create(1, 1, 1, 3), label="c"))
        
        space.add_relation(a, RelationType.IS_A, b)
        space.add_relation(b, RelationType.IS_A, c)
        
        path = space.derive_path(a, c)
        
        assert path is not None
        assert len(path) == 3
        assert path[0] == a
        assert path[-1] == c
    
    def test_create_fork(self):
        space = Space()
        original = space.add(Node(
            id=SemanticID.create(1, 1, 1, 1),
            label="jaguar"
        ))
        
        fork, branches = space.create_fork(original, ["animal", "car"])
        
        assert len(branches) == 2
        assert branches[0].label == "jaguar:animal"
        assert branches[1].label == "jaguar:car"
        assert fork.source_id == original.id
        assert len(fork.branches) == 2
    
    def test_derive_tension(self):
        space = Space()
        
        # Node with no forks, no relations = tension 1.0
        stable = space.add(Node(id=SemanticID.create(1, 1, 1, 1), label="stable"))
        tension = space.derive_tension(stable)
        assert tension == 1.0
        
        # Node with fork but no relations = high tension
        ambiguous = space.add(Node(id=SemanticID.create(1, 1, 1, 2), label="ambiguous"))
        space.create_fork(ambiguous, ["a", "b"])
        tension = space.derive_tension(ambiguous)
        assert tension > 1.0
    
    def test_derivation_ratio(self):
        space = Space()
        
        # Add 100 nodes with ~10 relations
        for i in range(100):
            node = Node(id=SemanticID.create(1, 1, 1, i+1), label=f"n{i}")
            space.add(node)
        
        # Ratio should be nodes^2 / (nodes + relations)
        # With 100 nodes and 0 relations: 10000 / 100 = 100x
        assert space.derivation_ratio == 100.0


class TestAuditLog:
    """Test audit logging."""
    
    def test_append_and_verify(self):
        log = AuditLog()
        
        log.append("TEST", "arg1", "arg2")
        log.append("TEST2", "arg3")
        
        assert len(log) == 2
        assert log.verify()
    
    def test_chain_linkage(self):
        log = AuditLog()
        
        e1 = log.append("FIRST")
        e2 = log.append("SECOND")
        
        assert e2.prev_hash == e1.hash
        assert e1.prev_hash == AuditLog.GENESIS_HASH
    
    def test_tamper_detection(self):
        log = AuditLog()
        
        log.append("TEST")
        log.append("TEST2")
        
        # Tamper with an entry
        log._entries[0] = log._entries[0].__class__(
            index=0,
            timestamp=log._entries[0].timestamp,
            action="TAMPERED",  # Changed!
            args=log._entries[0].args,
            prev_hash=log._entries[0].prev_hash,
            hash=log._entries[0].hash  # Hash no longer matches
        )
        
        assert not log.verify()


class TestDeterministicWrapper:
    """Test the wrapper interface."""
    
    def test_handle_new_concept(self):
        wrapper = DeterministicWrapper()
        
        decision = wrapper.handle("Apple", {"major": 1, "type": 1, "subtype": 1})
        
        assert decision.strategy == Strategy.CREATE_NODE
        assert decision.result.label == "Apple"
    
    def test_handle_existing_concept(self):
        wrapper = DeterministicWrapper()
        
        # First time creates
        d1 = wrapper.handle("Apple", {"major": 1, "type": 1, "subtype": 1})
        # Second time returns existing
        d2 = wrapper.handle("Apple")
        
        assert d1.strategy == Strategy.CREATE_NODE
        assert d2.strategy == Strategy.RETURN_EXISTING
    
    def test_decisions_logged(self):
        wrapper = DeterministicWrapper()
        
        wrapper.handle("A", {"major": 1, "type": 1, "subtype": 1})
        wrapper.handle("B", {"major": 1, "type": 1, "subtype": 1})
        
        assert len(wrapper.decisions) == 2
        assert wrapper.audit.verify()


# Run with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
