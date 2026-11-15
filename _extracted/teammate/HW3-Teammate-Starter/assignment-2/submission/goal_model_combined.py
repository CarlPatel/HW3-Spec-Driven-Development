"""Combined model. Explicit duplicate merges and interpretations are in goal_catalog.py."""
from model_support import build_model, main

def build():
    return build_model('combined')

if __name__ == '__main__':
    main('combined')
