print("Starting script...")

try:
    import pandas as pd
    print("Pandas imported successfully")
except ImportError as e:
    print(f"Pandas import failed: {e}")

try:
    import numpy as np
    print("Numpy imported successfully")
except ImportError as e:
    print(f"Numpy import failed: {e}")

try:
    from sklearn.ensemble import RandomForestClassifier
    print("Sklearn imported successfully")
except ImportError as e:
    print(f"Sklearn import failed: {e}")

try:
    import joblib
    print("Joblib imported successfully")
except ImportError as e:
    print(f"Joblib import failed: {e}")

print("All imports completed!")
