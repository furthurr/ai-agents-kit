# Diagnóstico HTTP complementario: corrección de contexto

Este diagnóstico se ejecutó después de terminar las cuatro inferencias, sin feedback
al modelo y sin cambiar calificaciones congeladas, candidatos, oráculos o soluciones.

1. Primer intento: `diagnostico-http.json`. El script usó `Client` fuera del runner
   Django sin permitir `testserver` en `ALLOWED_HOSTS`. Dio400 HTML en las cuatro
   soluciones, incluso con CSRF desactivado. **No interpretar esos400 como defecto
   de los productos ni como errores del proveedor.** Se conserva el JSON íntegro.
2. Corrección: el único cambio al código ejecutado fue configurar, dentro del proceso
   diagnóstico, `settings.ALLOWED_HOSTS = ['testserver']`. No se editó configuración
   de las soluciones. Segundo intento: `diagnostico-http-corregido.json`.
3. Corregido: Client normal devuelve401 JSON en4/4; con `enforce_csrf_checks=True`
   devuelve401 en ambos controles y ajustadoR2, y403 HTML en ajustadoR1. El código
   de esta última solución deja que middleware CSRF intercepte antes del chequeo
   de autenticación. Es un límite real de fidelidad del contrato401 que los nueve
   oráculos congelados no detectan. No es un403 de inferencia ni prueba un baneo.

Fuente corregida: `diagnostico-http.py`, SHA256
`28626b95e89b587df8cf41d5fd95b6e60a42bece1f10f8fb9d3af626a61f410c`.
La fuente v1 se reconstruye retirando exclusivamente estas tres líneas después de
`django.setup()`:

```python
from django.conf import settings
# Outside Django's test runner, testserver is not automatically allowed.
settings.ALLOWED_HOSTS = ['testserver']
```

SHA256 de v1 reconstruida:
`0b7bc430a08a95673cc643e7444045ac7bf6207d8d768bed16fd02a66ee58dea`.
Los dos intentos y sus tiempos se exportan y quedan en el laboratorio preservado.
