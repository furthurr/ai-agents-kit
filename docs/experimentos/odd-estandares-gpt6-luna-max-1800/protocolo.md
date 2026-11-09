# ODD histórico vs ajustado — GPT-6 Luna max, 1.800 segundos

Cohorte nueva autorizada tras dos timeouts en la R1 con límite de600s. Ambos
tratamientos se ejecutan de nuevo, tres repeticiones por brazo, sin reutilizar
resultados parciales. Igual baseline, tarea Alta, agentes, permisos, oráculos,
modelo `openai/gpt-6-luna` y variante CLI `max`. El único cambio buscado es un
timeout de **1.800s por invocación para ambos brazos**, incluida la preflight.
No forzar temperatura; el host indica que el modelo no la soporta.

Verificar perfiles por contenido, referencia43+9, configuración y freeze antes
de comparaciones. Conservar preflights, llamadas, errores y resultados por intento.
Hasta dos procesos concurrentes; parar las siguientes repeticiones si aparece error
API, timeout o fallo de carga. Fallo funcional ordinario se conserva, sin corregir
el tratamiento ni reintentar selectivamente. No alterar ni completar retroactivamente
el lote de600s. No incluir preflights ni checks externos en costes de conversación.

Reportar funcionalidad, cargas de skills, documentación, tiempos y tokens expuestos;
razonamiento privado no se guarda. Tokens comparables=input+cache-read/write+output,
reasoning separado, no factura. Suma de tiempos no es wall-clock ni tiempo humano.
Tres repeticiones/un proyecto no demuestran generalización. No mezclar con Gemini ni
con la cohorte anterior. Permisos no son aislamiento de sistema operativo. No instalar
agentes, modificar fuentes canónicas, hacer commits ni cambiar el plan del Escritorio.
