from __future__ import annotations

# Week 1 scaffold.
# Week 2+ will add lightweight dev-only protections for endpoints like POST /assets/seed,
# using environment flags or shared secret headers if needed.

def is_dev() -> bool:
    return True
