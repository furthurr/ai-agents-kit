# Adaptación de la tarea a Genera Android

> **Evidencia anonimizada:** identificadores y fragmentos originales han sido sustituidos u omitidos. Las métricas son históricas; no acreditan una ejecución nueva sobre los fixtures. Véase [alcance y límites](../../PRIVACIDAD-MOVIL.md).

El ZIP histórico `mobile-android.zip` (paquete
`com.example.mobilefixture`) ya no está disponible en disco. Para conservar el
experimento se usó el único proyecto Android real disponible:

| Elemento | Valor |
|---|---|
| ZIP | `~/.local/share/ai-agents-kit/fixtures/mobile-android.zip` |
| SHA-256 | `b4b88f8740807c89eed8b1becd0d192d9c39e88fb78673ff74899f5e0160ade8` |
| Paquete | `mx.com.bancadigital.crm` |
| Módulo | `:core:domain` (`testBuildType = "release"`) |

## Qué se cambió

- Todas las apariciones de `com.example.mobilefixture` pasaron a
  `mx.com.bancadigital.crm` en la tarea y el oráculo.
- Las rutas `com/example/mobilefixture` pasaron a `mx/com/bancadigital/crm`.
- La suite original pasó de `com.example.mobilefixture.domain.util.*` a
  `mx.com.bancadigital.crm.domain.util.*`.

**No** se cambiaron reglas de negocio, nombres de clases, firmas ni expectativas
del oráculo.

## Validación previa del oráculo

Sobre una copia limpia de Genera se escribió una implementación de referencia
de `FixtureSource1Impl` y se ejecutó:

```bash
./gradlew :core:domain:testReleaseUnitTest \
  --tests "mx.com.bancadigital.crm.domain.use_case.prospect.OracleSearchProspectsTest"
```

Resultado: **BUILD SUCCESSFUL** (10/10 pruebas del oráculo) y la suite original
`mx.com.bancadigital.crm.domain.util.*` también **BUILD SUCCESSFUL**.

## Archivos

- [tarea-1-media-baja-genera.md](tarea-1-media-baja-genera.md)
- [OracleSearchProspectsTest.kt](OracleSearchProspectsTest.kt)
- Hashes: [../referencia/genera-sha256.txt](../referencia/genera-sha256.txt)
