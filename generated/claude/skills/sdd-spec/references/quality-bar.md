# Quality Bar — agnóstica a la tecnología

Cargar en **Fase 2 (Design)**, **Implementación** y **Fase 4**. No cargar en Fase 1.
Redactar y aplicar **sin** nombres de framework en el núcleo del checklist; el stack concreto sale del steering.

## Checklist

1. **Capas:** UI no conoce persistencia concreta; dominio no importa frameworks de UI.
2. **DI:** composition root único; repos/servicios/puertos inyectados.
3. **Singletons:** prohibido singleton de infraestructura (repos, storage, network) salvo justificación explícita en `design.md`.
4. **I/O:** fuera del hilo/loop de UI cuando la plataforma lo permita (leer steering).
5. **Errores:** tipados o `Result`; no `catch` vacío; log en fallos de infraestructura.
6. **Persistencia encapsulada:** un solo módulo/adaptador toca storage/BD; UI y domain no llaman APIs crudas de persistencia.
7. **RNF auto-audit:** antes de cerrar, verificar 3–5 RNF críticos del propio spec (búsqueda en código).
8. **Testing adaptativo:** comportamiento nuevo/modificado usa TDD focalizado y bugfix usa regresión; caracterización protege refactors. «Sin test nuevo» solo sin cambio observable o con excepción explícita y verificación alternativa. TDD estricto solo por petición.
9. **PBT:** solo si hay invariante algebraico y el modo lo permite (ver `testing.md`).
10. **Proporcionalidad design (`standard`):** techo orientativo ~250 líneas; 1 flowchart + 1 sequence; C4/ER solo en `deep` o si hay BD interna real.
11. **Tipos:** sin `any` / tipos opacos cuando el lenguaje lo permita (steering).
12. **Código mínimo:** GREEN mínimo correcto; no crear abstracciones, mocks o capas anticipadas solo para satisfacer tests.

## Integración

- **Fase 2:** el design debe satisfacer este bar; citar excepciones en `design.md` si las hay.
- **Implementación:** revisar este bar antes de marcar waves de UI/datos como `[x]`.
- **Fase 4:** spot-check explícito (lista corta en `verification.md`).
