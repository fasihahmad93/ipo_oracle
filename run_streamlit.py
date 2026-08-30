#!/usr/bin/env python
"""Quick launcher script for the Streamlit frontend."""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Get the project root
    project_root = Path(__file__).resolve().parent
    app_file = project_root / "src" / "streamlit_frontend" / "app.py"
    
    if not app_file.exists():
        print(f"Error: App file not found at {app_file}")
        sys.exit(1)
    
    print(f"Starting IPO Oracle Streamlit frontend...")
    print(f"App file: {app_file}")
    print(f"Access the app at: http://localhost:8501")
    print()
    
    # Run streamlit
    try:
        subprocess.run(
            ["streamlit", "run", str(app_file)],
            cwd=str(project_root),
        )
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting Streamlit: {e}")
        sys.exit(1)
