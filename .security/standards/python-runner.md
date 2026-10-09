# Estándar de seguridad — runner Python local

## Fuente

- OWASP Application Security Verification Standard (ASVS), versión 5.0.0.
- CWE-284: Improper Access Control.
- CWE-693: Protection Mechanism Failure.
- CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition.

Fuentes consultadas el 2026-10-07:

- https://owasp.org/www-project-application-security-verification-standard/
- https://cwe.mitre.org/data/definitions/284.html
- https://cwe.mitre.org/data/definitions/693.html
- https://cwe.mitre.org/data/definitions/367.html

## Criterios aplicados al alcance F07

- Separar código candidato no confiable del almacén/oráculo de evaluación.
- No tratar separación de carpetas como control de acceso; validar el boundary del SO.
- Integridad de evidencia: impedir que la entrega altere estado, fixtures, criterios o resultados.
- Rutas/archivos: proteger against symlink/path replacement y TOCTOU; usar ownership explícito.
- Revisar outputs RPC con esquemas, límites y errores sanitizados.

Es una revisión dirigida al runner/evaluador F07. No afirma cumplimiento ASVS completo.
