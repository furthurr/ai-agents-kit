# Tratamientos y procedencia

Los tres brazos usan el mismo modelo solicitado y el mismo transporte Antigravity
de OpenCode. Identidades temporales distintas impiden confundir una skill global
homónima con el tratamiento previsto. No se edita `canonical/`, `adapters/` ni
`generated/` para este experimento.

| Brazo | Agente temporal | Skill primaria | Fuente |
|---|---|---|---|
| Developer | `g3-developer` | `g3d-developer` | `generated/opencode/agents/developer.md` y skill `developer` |
| SDD | `g3-sdd` | `g3s-sdd-spec` | `generated/opencode/agents/sdd.md` y skill `sdd-spec` con referencias |
| ODD experimental | `g3-odd` | `g3o-odd-workflow` | Tratamiento B de la investigación anterior, con identidad propia |

Cada perfil contiene las once skills MAS bajo su namespace para conservar sus
referencias, aunque los permisos de invocación se limitan a la skill primaria y
los dominios data-api/ui-design. El perfil ODD añade su skill experimental. Los
enlaces entre nombres se adaptan mecánicamente sin importar reglas de un método
a otro. La traza debe contener el cuerpo esperado íntegro de la skill primaria;
el nombre cargado o una frase de confirmación no son prueba suficiente.

Los prompts finales y todas las referencias se preservan bajo `profiles/` de la
raíz temporal, con hashes congelados. El fichero fuente de ODD es
[tratamiento-b.md](../odd-vs-sdd-2026-11-04/tratamiento-b.md), que documenta la
adaptación de Gentle AI y excluye Engram/RDD/delegación. No se implementa aquí
el agente del plan del Escritorio: se ensaya el procedimiento conservado, no una
versión nueva de producto presentada como si ya estuviera validada.

En S08, los tres reciben las mismas dos reglas, T1 implementada con un test verde
y T2 pendiente. Developer recibe `WORK.md`; SDD su spec Tiny y ODD su registro
Specs/Tasks/Log. Se prueba recuperación desde una sesión nueva, no equivalencia
de todas las formas de persistencia ni pérdida de contexto real.

El namespace y los prompts son entradas del experimento, no instrucciones de
instalación. Las credenciales las utiliza el host, no se leen/copían al perfil.
