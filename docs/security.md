# Security Notes

**Author: HAMAILI Ahmed-Imad**

This project is a local portfolio demo, but it is structured around security principles that would matter in a real IoT platform.

## Current security mechanisms

- Devices are registered before telemetry is accepted.
- Device keys are hashed in the database.
- Invalid or unknown devices are ignored by the MQTT consumer.
- Payloads are validated before storage.
- Services run in isolated Docker containers.
- Sensitive runtime configuration is externalized through environment variables.
- Prometheus and Grafana are separated from the application API.

## Known demo limitations

- MQTT anonymous access is enabled for local development.
- Device keys are stored in a demo JSON file for the simulator.
- There is no user authentication yet for dashboard access.
- TLS is not configured in the local Compose environment.
- Grafana uses local demo credentials.

## Production hardening ideas

- Enable Mosquitto authentication and ACLs.
- Use TLS for MQTT and HTTP traffic.
- Add JWT/OIDC authentication for users.
- Rotate device keys and store secrets in a dedicated secret manager.
- Add rate limiting and audit logs.
- Use network policies when deployed on Kubernetes.
- Move Grafana credentials to Docker secrets or a vault.
