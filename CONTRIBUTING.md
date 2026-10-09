# 🤝 Contribuir a CYBERTEST

¡Gracias por mejorar una herramienta de auditoría responsable! 🛡️

## Antes de enviar cambios

1. Crea una rama descriptiva, por ejemplo `feat/inventario-activos`.
2. Sigue la [guía de instalación](docs/INSTALACION.md).
3. Mantén la separación entre políticas, adaptadores, almacenamiento e interfaz.
4. Nunca añadas credenciales, evidencias reales, capturas o datos de clientes.

## Calidad mínima

```bash
pytest -q
cd ui && npm run build
```

Todo adaptador externo debe usar argumentos estructurados, timeout, errores controlados y política de alcance. Las capacidades activas deben probar que se bloquean fuera de un alcance autorizado.

## Estilo

- 🐍 Python: tipado claro, módulos pequeños y pruebas para lógica crítica.
- ⚛️ TypeScript: componentes accesibles y compilación estricta.
- 📝 Documentación: español claro, con privilegios y límites explícitos.

## Conducta responsable

No se aceptan cambios que automaticen daño, exfiltración, persistencia, ransomware, propagación o acciones fuera de alcance.
