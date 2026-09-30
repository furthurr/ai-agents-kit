# Notación EARS — Referencia Completa

## Patrones estándar

| Patrón | Forma | Uso |
|--------|-------|-----|
| Ubicuo | `EL SISTEMA DEBERÁ <r>` | Comportamiento siempre activo |
| Evento | `CUANDO <trigger> EL SISTEMA DEBERÁ <r>` | Respuesta a un evento |
| Estado | `MIENTRAS <estado> EL SISTEMA DEBERÁ <r>` | Comportamiento durante un estado |
| Error | `SI <condición> ENTONCES EL SISTEMA DEBERÁ <r>` | Manejo de errores |
| Opcional | `DONDE <feature/config> EL SISTEMA DEBERÁ <r>` | Comportamiento configurable |

## Extensiones propias

| Patrón | Forma | Uso |
|--------|-------|-----|
| Anti-regresión | `EL SISTEMA DEBERÁ SEGUIR <r>` | Garantía de no regresión (bugfix) |

## Notas

1. Los criterios se escriben en **español** (WHEN→CUANDO, WHILE→MIENTRAS,
   IF/THEN→SI/ENTONCES, WHERE→DONDE, SHALL→DEBERÁ). Convención propia.
2. El patrón **Anti-regresión** no existe en EARS estándar; se añade para bugfix.
3. Un requisito = un comportamiento testable. Sujeto siempre "EL SISTEMA".
4. Sin adjetivos vagos ("rápido", "fácil", "robusto").

## Composición

Los patrones se pueden combinar:
- `MIENTRAS <estado> CUANDO <evento> EL SISTEMA DEBERÁ <r>` (Estado + Evento)
- `DONDE <config> SI <error> ENTONCES EL SISTEMA DEBERÁ <r>` (Opcional + Error)
