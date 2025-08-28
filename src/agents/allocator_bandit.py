"""
Allocator (bandit simples): escolhe expert pelo maior 'confidence' (placeholder).
"""
from typing import List, Dict, Any

def choose(votes: List[Dict[str,Any]]) -> Dict[str,Any]:
    return max(votes, key=lambda v: v.get("confidence",0.0))
