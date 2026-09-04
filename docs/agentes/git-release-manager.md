# Git & Release Manager

## Resumen

| Campo | Información |
|---|---|
| ID | `git-release-manager` |
| Skills | [`git-commit`](../../canonical/skills/git-commit/SKILL.md) + [`release-management`](../../canonical/skills/release-management/SKILL.md) |
| Propósito | Gestionar commits, push, versionado, tags y CHANGELOG |
| Alcance | Operaciones de Git y release; no desarrollo de producto |

Este agente reúne dos procedimientos relacionados, pero no idénticos:

- `git-commit` cubre estado, diff, commits Conventional Commits y push.
- `release-management` cubre versión SemVer, CHANGELOG y tags anotados.

## Cuándo usar cada skill

| Petición | Skill |
|---|---|
| Revisar estado o diff | `git-commit` |
| Preparar un commit | `git-commit` |
| Hacer push | `git-commit` |
| Preparar una versión | `release-management` |
| Subir versión o build number | `release-management` |
| Generar CHANGELOG | `release-management` |
| Crear tag anotado | `release-management` |
| Release que también requiere commit | Ambas, en el orden correspondiente |

## Cómo trabaja

### Commits y push

1. Inspecciona `status`, diff, historial, rama y archivos sensibles.
2. Resume los cambios y propone un mensaje Conventional Commits en español.
3. Detecta posibles secretos por nombre y contenido del diff.
4. Espera confirmación antes de hacer `git commit`.
5. Pregunta por separado antes de hacer push.

### Releases

1. Detecta la tecnología y el archivo real de versión.
2. Lee tags, historial y, si existe, el contexto de `.release/`.
3. Propone el bump SemVer y el CHANGELOG.
4. Espera confirmación antes de editar la versión o CHANGELOG.
5. Tras otra confirmación, crea el commit, tag y push según el alcance aprobado.

Android, iOS y Flutter tienen soporte directo. Para otras tecnologías, la skill
investiga las convenciones oficiales y puede generar un perfil reutilizable antes
de continuar.

## Ejemplos de uso

```text
@git-release-manager Revisa los cambios y prepara un commit documental, pero no
lo ejecutes todavía.
```

```text
@git-release-manager Prepara la release patch: detecta la versión actual, propone
el bump y genera el CHANGELOG antes de modificar archivos.
```

## Artefactos y resultados

- Un commit con mensaje y ámbito coherentes.
- Un `CHANGELOG.md` o la ubicación definida por el proyecto.
- Un tag anotado `vX.Y.Z` o la convención del proyecto.
- Un perfil `.release/` cuando el proyecto necesita contexto persistente.
- Informe exacto de comandos ejecutados, rama, hash y remote.

## Límites y confirmaciones

- Nunca hace commit, push, tag, release ni cambios de versión sin confirmación explícita.
- Las acciones destructivas requieren doble confirmación.
- No modifica UI, lógica de negocio, datos ni código ajeno a versionado.
- No incluye archivos sensibles sin autorización inequívoca; recomienda excluirlos.
- No usa `release-management` para un commit cotidiano ni `git-commit` para decidir
  una versión.
