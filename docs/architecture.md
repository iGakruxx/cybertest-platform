# Arquitectura y plan de evolución

## Flujo de trabajo

`borrador -> alcance aprobado -> reconocimiento local -> descubrimiento activo autorizado -> enumeración -> evaluación -> validación -> informe`

Un trabajo almacena inicio, finalización, estado y error. El orquestador conserva su tarea asíncrona y, al cancelar, termina el subproceso en vez de dejarlo huérfano. Los resultados parciales y las evidencias ya confirmadas no se eliminan al fallar un trabajo.

## Interfaces de módulo

- Los adaptadores reciben modelos o valores validados, y devuelven `ProcessResult`; jamás una cadena de shell.
- La política es el único lugar que concede capacidades activas u ofensivas.
- Las evidencias se crean mediante `save_text`, que redacta marcadores de secretos y calcula el hash.
- Los informes sólo consumen registros normalizados de la base de datos.

## Riesgos y controles

| Riesgo | Control actual |
|---|---|
| Alcance implícito | CIDR privado explícito y permiso por alcance |
| Inyección de comandos | `asyncio.create_subprocess_exec` con listas de argumentos |
| Escaneo excesivo | Sólo `nmap -sn`, reintentos y timeout limitados |
| Procesos huérfanos | Terminación al cancelar o superar timeout |
| Secretos en evidencias | Redacción básica y almacenamiento local |
| Hallazgos sobredimensionados | El inventario no crea vulnerabilidades ni confirma explotación |

## Próximas fases

1. Parseadores XML de Nmap y modelos de servicios/puertos.
2. Adaptadores TLS/SSH/HTTP con categorías no intrusivas.
3. Correlación CVE con caché, fecha de consulta y estados `possible`, `confirmed`, `false_positive`.
4. Alembic, autenticación local y cifrado de secretos.
5. UI React accesible y exportación PDF mediante plantilla revisada.
6. Validación ofensiva aislada, sin movimiento lateral, habilitada sólo por autorización de auditoría y activo.
