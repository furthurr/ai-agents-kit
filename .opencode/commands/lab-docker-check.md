---
description: Comprueba el perfil Docker local usando solo una prueba fija y confiable, sin modelos
---

Desde la raíz del repositorio ejecuta:
`python3 .agent-lab/sdd-escalation/docker_smoke.py`.

Este script lanza únicamente una prueba fija de Python en la imagen oficial ya
descargada y fijada por digest, no código de candidatos. No invoca modelos ni
requiere sus credenciales. Resume los checks y el resultado guardado en
`.agent-lab/sdd-escalation/runtime/smoke-result.json`.

Si el motor está detenido, indica que se abra Docker Desktop; no cambies opciones
globales, no aceptes licencias, no pidas contraseñas ni reemplaces la imagen/host
para hacer pasar el check. No montes el repo, el socket Docker o pruebas reservadas.
No describas esta prueba como validación completa del sandbox de agentes: la
frontera de herramientas OpenCode y la ejecución de candidatos siguen pendientes.
