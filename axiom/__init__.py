"""
Axiom: Semantic Coordinates for Derivable Knowledge

Store the minimal structure from which all answers can be derived.
Like mathematics stores axioms, not equations.
Like DNA stores instructions, not organisms.

This is the seed. The tree grows from here.
"""

__version__ = "0.1.0"

from .core import (
    # Categories
    MAJOR_CATEGORIES,
    
    # Core types
    SemanticID,
    SemanticIDError,
    Node,
    Fork,
    RelationType,
    
    # The space
    Space,
    AuditLog,
    AuditEntry,
    
    # The wrapper
    Strategy,
    Decision,
    DeterministicWrapper,
    
    # Helpers
    create_space,
    create_wrapper,
    quick_node,
)

__all__ = [
    # Version
    "__version__",
    
    # Categories
    "MAJOR_CATEGORIES",
    
    # Core types
    "SemanticID",
    "SemanticIDError", 
    "Node",
    "Fork",
    "RelationType",
    
    # The space
    "Space",
    "AuditLog",
    "AuditEntry",
    
    # The wrapper
    "Strategy",
    "Decision",
    "DeterministicWrapper",
    
    # Helpers
    "create_space",
    "create_wrapper",
    "quick_node",
]
