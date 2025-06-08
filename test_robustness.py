#!/usr/bin/env python3
"""
Test script to verify shapefile download robustness improvements.
"""

import sys
import logging
from pathlib import Path

# Add the censusdis package to the path
sys.path.insert(0, '/workspaces/censusdis')

from censusdis.maps import ShapeReader

# Set up logging to see our improvement messages
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_robustness():
    """Test the robustness improvements."""
    print("Testing shapefile download robustness improvements...")
    
    # Create a shape reader (shapefile_root=None uses default cache location)
    reader = ShapeReader(shapefile_root=None, year=2020)
    
    print(f"Cache directory: {reader.shapefile_root}")
    
    # Test cache cleanup functionality
    print("\nTesting cache cleanup...")
    removed_count = reader.clear_corrupted_cache()
    print(f"Removed {removed_count} corrupted cache entries")
    
    # Test download with retry logic for a known working shapefile
    print("\nTesting download with retry logic...")
    try:
        # This should work and use our improved download logic
        gdf = reader.read_shapefile(
            shapefile_scope='us',
            geography='state', 
            timeout=30
        )
        print(f"Successfully downloaded shapefile with {len(gdf)} features")
        
    except Exception as e:
        print(f"Download failed: {e}")
        return False
        
    print("\nRobustness test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_robustness()
    sys.exit(0 if success else 1)
