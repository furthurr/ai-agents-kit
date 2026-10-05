# 5. Flujos y secuencias

## 5.1 Render y validación de reproducibilidad

El render normal escribe en `generated/`. Para cada plataforma, el renderer
retira el subárbol de salida existente antes de copiar skills y emitir agentes;
este comportamiento es una fuente del riesgo registrado como `ARQ-001`
(`../tools/render.py:74-116`).

```mermaid
sequenceDiagram
  actor Contributor as Contribuidor
  participant Render as Renderer
  participant Manifest as Inventario
  participant Canonical as Fuentes canónicas
  participant Adapters as Adapters de plataforma
  participant Generated as Salida generada
  participant Validate as Validador
  participant Temp as Árbol temporal

  Contributor->>Render: render
  Render->>Manifest: leer skills, agents, platforms
  loop cada plataforma declarada
    Render->>Adapters: leer platform.json y adapters
    Render->>Canonical: leer SKILL.md y cuerpos de agentes
    Render->>Generated: eliminar salida anterior de esa plataforma
    Render->>Generated: copiar skills y escribir agentes transformados
  end
  Contributor->>Validate: validate
  Validate->>Manifest: leer inventario
  Validate->>Canonical: revisar archivos y tokens
  Validate->>Adapters: revisar presencia, filenames y reglas host
  Validate->>Temp: renderizar en directorio temporal
  Validate->>Generated: calcular hashes de salida actual
  Validate->>Temp: comparar hashes por plataforma
  Validate-->>Contributor: resultado y errores, si los hay
```

El validador ejecuta primero controles del manifest/adapters/tokens/orfandad y
solo si no hay errores compara la salida generada contra un render temporal
(`../tools/validate.py:219-245`). La comparación temporal protege `generated/`
durante la validación, pero no cambia el comportamiento destructivo del render
normal.

## 5.2 Instalación en un host

```mermaid
sequenceDiagram
  actor User as Usuario
  participant Installer as Instalador de plataforma
  participant Preflight as Preflight
  participant Generated as Salida generada
  participant Dest as Configuración del usuario
  participant Backup as Backup local

  User->>Installer: ejecutar instalación
  Installer->>Preflight: --check-source
  alt artefactos requeridos ausentes
    Preflight-->>Installer: error
    Installer-->>User: abortar antes de copiar
  else origen completo
    alt --dry-run
      Installer-->>User: listar operaciones; no copiar ni verificar destino
    else instalación normal
      opt destino con contenido y sin --force
        Installer->>Backup: copiar contenido previo, salvo --force
      end
      Installer->>Generated: leer skills/agentes generados
      Installer->>Dest: copiar archivos
      Installer->>Preflight: --check-installed
      alt destino incompleto
        Preflight-->>Installer: error; no declarar éxito
        Installer-->>User: informar instalación incompleta
      else destino verificado
        Installer-->>User: confirmar y recomendar reiniciar el host
      end
    end
  end
```

Las opciones dry-run, force, backup y preflight se describen en
`../docs/instalacion.md:53-60, 99-127`; el wrapper Copilot muestra el
orden concreto en `../scripts/install/copilot.sh:56-70, 90-101, 113-135`.

## 5.3 Importación de una instalación modificada

El flujo de backup/import lee directorios instalados, filtra por el manifest y
los adapters, y copia los elementos declarados a `imports/<plataforma>/<fecha>/`.
El resultado se revisa y promociona manualmente; no se escribe de vuelta en las
fuentes canónicas automáticamente (`../tools/import_installed.py:16-55`,
`../docs/instalacion.md:170-189`).

```mermaid
sequenceDiagram
  actor User as Usuario
  participant Wrapper as Wrapper de importación
  participant Importer as Importer
  participant Installed as Directorios instalados
  participant Imports as Área de imports
  participant Canonical as Fuentes y adapters

  User->>Wrapper: importar (opcional --dry-run)
  Wrapper->>Importer: plataforma + rutas instaladas
  Importer->>Canonical: leer manifest y filename adapters
  Importer->>Installed: enumerar contenido instalado
  Importer->>Importer: ignorar elementos no declarados
  opt no es dry-run y hay archivos declarados
    Importer->>Imports: copiar para revisión
  end
  Importer-->>User: mostrar faltantes/elementos ignorados
  User->>Canonical: promover manualmente solo cambios aprobados
```
