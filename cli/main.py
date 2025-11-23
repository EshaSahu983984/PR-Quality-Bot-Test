import argparse
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.validator_runner import run_validations

def main():
    parser = argparse.ArgumentParser(description="EV2/OneBranch YAML Code Review Tool")
    parser.add_argument("yaml_path", help="Path to YAML file to validate")
    args = parser.parse_args()

    errors = run_validations(args.yaml_path)
    if errors:
        print("\n Validation Issues Found:\n")
        for err in errors:
            print(f" {err}")
        sys.exit(1)  # Exit with non-zero to fail pipeline    
    else:
        print("YAML passed all validations!")
        sys.exit(0)
        
if __name__ == "__main__":
    main()
