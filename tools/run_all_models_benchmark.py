#!/usr/bin/env python3
"""Orquestador para ejecutar benchmarks multi-modelo en secuencia:
  1. MAI-Code-1.1-Flash (github-copilot) - Tareas 1 y 2
  2. GPT 6.1 Terra (openai) - Tareas 1 y 2
"""
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / 'tools/real_android_multimodel_benchmark.py'

MODELS = [
    {
        'name': 'MAI-Code-1.1-Flash (Copilot)',
        'model_id': 'github-copilot/mai-code-1.1-flash',
        'root': '/tmp/real-android-benchmark-mai',
        'output_dir': REPO / 'docs/experimentos/real-android-mai-flash-2026-11-08'
    },
    {
        'name': 'GPT 6.1 Terra (OpenAI)',
        'model_id': 'openai/gpt-6.1-terra',
        'root': '/tmp/real-android-benchmark-gpt6',
        'output_dir': REPO / 'docs/experimentos/real-android-gpt6-terra-2026-11-08'
    }
]

def main():
    print("==================================================================")
    print(" INICIANDO BATERÍA COMPLETA DE PRUEBAS MULTI-MODELO (T1 y T2)")
    print(" Modelos: MAI-Code (Copilot), GPT 6.1 Terra (OpenAI)")
    print("==================================================================")

    for idx, item in enumerate(MODELS, 1):
        name = item['name']
        model_id = item['model_id']
        root = item['root']
        output_dir = item['output_dir']

        print(f"\n[{idx}/3] >>> INICIANDO FASE MODELO: {name} <<<")
        print(f"Modelo: {model_id} | Root: {root} | Salida: {output_dir}")

        cmd = [
            sys.executable, str(SCRIPT),
            '--model', model_id,
            '--tasks', '1', '2',
            '--root', str(root),
            '--output-dir', str(output_dir)
        ]

        started = time.time()
        res = subprocess.run(cmd)
        elapsed = time.time() - started
        print(f"[{idx}/3] Fase completada para {name}. Returncode: {res.returncode}. Duración: {elapsed:.1f}s")
        if res.returncode != 0:
            print(f"ALERTA: El proceso para {name} terminó con código {res.returncode}")

    print("\n==================================================================")
    print(" TODAS LAS FASES DE BENCHMARK HAN FINALIZADO EXITOSAMENTE.")
    print("==================================================================")

if __name__ == '__main__':
    main()
