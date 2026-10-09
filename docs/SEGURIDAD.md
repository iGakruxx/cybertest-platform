# 🔐 Seguridad, alcance y autorización

## Principio rector

La presencia de una ruta, puerta de enlace o respuesta de red **no equivale** a autorización para escanear un activo. CYBERTEST es para auditorías defensivas con permiso documentado.

## Controles implementados

- 🎯 Los trabajos activos requieren CIDR privado, justificación y permiso explícito.
- 🧱 Los adaptadores usan listas de argumentos con `create_subprocess_exec`, no shell.
- ⏱️ Los procesos tienen timeout y cancelación explícita.
- 🧾 La evidencia conserva herramienta, argumentos, salida y hash SHA-256.
- 🕵️ Los marcadores comunes de secretos se redactan antes de persistir evidencia.
- 🌐 La API se ejecuta en `127.0.0.1`.

## Autorización por etapa

| Etapa | Requisito |
|---|---|
| Reconocimiento local pasivo | Punto de conexión autorizado. |
| Descubrimiento activo | CIDR privado y permiso de descubrimiento activo. |
| Enumeración autenticada | Credenciales de sólo lectura y autorización específica. |
| Validación ofensiva | Aprobación por auditoría y por activo; límites de parada. |

## Límites deliberados

No se implementan automatización de exploits, persistencia, extracción de datos, ransomware, propagación, movimiento lateral ni consola de shell. Un hallazgo de alto riesgo debe convertirse en un procedimiento manual revisable, no en una ejecución automática.

## Divulgación responsable

No publiques IP, evidencias, credenciales, tokens ni informes de clientes. Para reportar un defecto de seguridad, usa un canal privado e incluye una reproducción mínima sin datos sensibles.
