#!/usr/bin/env python3
"""
Exemplo mínimo de entrada para o projeto.
"""
import argparse
from src.analysis import example_workflow

def main():
    parser = argparse.ArgumentParser(description="Geology discontinuities analysis - example")
    parser.add_argument("--sample", action="store_true", help="Run example workflow with sample data")
    args = parser.parse_args()

    if args.sample:
        example_workflow()
    else:
        print("Nenhuma opção fornecida. Use --sample para rodar um exemplo.")

if __name__ == "__main__":
    main()
