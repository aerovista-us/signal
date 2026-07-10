Got it. Here’s how I’d tighten this up fast, based on what we’ve built so far on NXCore (Traefik + Docker labels + Porkbun DNS-01 + internal CA/Tailscale).

# Highest-impact insights (fix order that unblocks everything)

1. **Stop mixing “file” routers with app labels.**
   Keep **all per-app routers/middlewares/services in Docker labels** only. Reserve `file` provider for **static** TLS defaults, middleware templates, and catch-alls. This alone removes most of the duplicate/override confusion you’re seeing.

2. **One resolver name everywhere.**
   Pick a single resolver key (e.g., `letsencrypt`) and **declare it once** in `traefik-static.yml`. Every router label must reference exactly that: `traefik.http.routers.X.tls.certresolver=letsencrypt`. If the name differs by even one character, Traefik silently falls back and you’ll chase phantom TLS errors.

3. **Your TLS error smells like SNI/Host mismatch, not a bad cert.**
   The `tlsv1 unrecognized name` typically happens when you curl an IP or the wrong hostname. Traefik routes by **Host rule + SNI**. So tests must include `-H 'Host: app.example.com'` against the `websecure` entrypoint. (Self-signed/internal CA domains need the same.)

4. **API “connection reset” is usually entrypoint exposure or security mismatch.**
   Decide: API via **internal network only** (preferred) or exposed on 8080 with `--api.insecure=true` (temporary). Right now you’re likely hitting the wrong address/port, or it’s bound only to the docker network.

5. **Normalize labels: one `labels:` block per service.**
   Traefik only reads the final effective set. Duplicate `labels:` nodes get merged weirdly or overwritten. Consolidate to one block per service, and ensure `traefik.enable=true` is present for the ones you want routed.

---

# Minimal known-good baseline (copy/adapt)

## `traefik-static.yml` (only static + resolvers here)

```yaml
entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

api:
  dashboard: true
  insecure: false  # set true only for temporary local debugging

providers:
  docker:
    exposedByDefault: false
  file:
    filename: /etc/traefik/dynamic/dynamic.yml
    watch: true

log:
  level: INFO

accessLog: {}

certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@your-domain.tld
      storage: /letsencrypt/acme.json
      dnsChallenge:
        provider: porkbun   # ← your environment must export PORKBUN_SECRET_API_KEY etc.
        delayBeforeCheck: 0
      # For first runs, consider:
      # caServer: https://acme-staging-v02.api.letsencrypt.org/directory
```

## `dynamic.yml` (safe defaults only; no app routers here)

```yaml
http:
  middlewares:
    https-redirect:
      redirectScheme:
        scheme: https
        permanent: true

  routers:
    catchall-redirect:
      rule: "HostRegexp(`{any:.+}`)"
      entryPoints: ["web"]
      middlewares: ["https-redirect"]
      service: noop

  services:
    noop:
      loadBalancer:
        servers:
          - url: "http://127.0.0.1:65535"
```

## Traefik service in `compose-traefik.yml`

```yaml
services:
  traefik:
    image: traefik:v3.1
    command: 
      - --providers.docker=true
      - --providers.file.filename=/etc/traefik/dynamic/dynamic.yml
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
    ports:
      - "80:80"
      - "443:443"
      # expose 8080 only if you truly need it outside:
      # - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik/traefik-static.yml:/etc/traefik/traefik.yml:ro
      - ./traefik/dynamic.yml:/etc/traefik/dynamic/dynamic.yml:ro
      - ./letsencrypt:/letsencrypt
      - ./certs:/certs:ro
    environment:
      - PORKBUN_API_KEY=xxxx
      - PORKBUN_SECRET_API_KEY=xxxx
    networks:
      - traefik
    healthcheck:
      test: ["CMD", "traefik", "healthcheck", "--ping"]
      interval: 10s
      timeout: 3s
      retries: 10
      start_period: 10s

networks:
  traefik:
    external: true
```

## Example app (Portainer) — labels only, one block

```yaml
services:
  portainer:
    image: portainer/portainer-ce:2.21.5
    command: -H unix:///var/run/docker.sock
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    networks: [traefik]
    labels:
      - traefik.enable=true
      - traefik.docker.network=traefik

      - traefik.http.routers.portainer.rule=Host(`portainer.your-domain.tld`)
      - traefik.http.routers.portainer.entrypoints=websecure
      - traefik.http.routers.portainer.tls.certresolver=letsencrypt

      - traefik.http.services.portainer.loadbalancer.server.port=9000

volumes:
  portainer_data: {}
```

---

# Precise fixes for your list

## 1.1 Fix Compose structure (duplicate labels / malformed YAML)

* Make **one** `labels:` block per service.
* Ensure consistent indentation (2 spaces) and valid YAML.
* Make sure each routed service has:

  * `traefik.enable=true`
  * `traefik.docker.network=traefik`
  * router rule, entrypoints, `tls.certresolver=letsencrypt`
  * a `service.loadbalancer.server.port`
* Remove application routers from `dynamic/`; keep them in labels.

**Quick validators**

```bash
# Fast YAML sanity:
docker compose -f compose-traefik.yml config >/dev/null

# Print fully-resolved compose (great for spotting dupes/merges):
docker compose -f compose-traefik.yml config
```

## 1.2 Let’s Encrypt resolver

* Confirm the block `certificatesResolvers.letsencrypt.acme` exists in `traefik-static.yml`.
* Use **exact** resolver name in labels: `...tls.certresolver=letsencrypt`.
* For first issuance, optionally use staging CA to avoid rate limits:
  `caServer: https://acme-staging-v02.api.letsencrypt.org/directory`
  (then swap to prod and re-issue).

**ACME file & perms**

```bash
mkdir -p ./letsencrypt
touch ./letsencrypt/acme.json
chmod 600 ./letsencrypt/acme.json
```

## 1.3 Traefik API connectivity

* If you **must** reach the dashboard externally:

  * Temporarily set `api.insecure=true` *and* map `8080:8080`, or
  * Expose via labels on `websecure` with auth.
* If internal only, **don’t** publish 8080. Use:

  ```bash
  docker exec -it traefik sh -c 'wget -qO- http://127.0.0.1:8080/api/rawdata' | head
  ```
* Also verify docker network:

  ```bash
  docker network inspect traefik | jq '.[0].Containers | keys'
  ```

## 1.4 SSL/TLS errors

* The error strongly suggests **wrong Host/SNI** in your curl:

  ```bash
  curl -i https://portainer.your-domain.tld \
    --resolve portainer.your-domain.tld:443:127.0.0.1
  # or when hitting via tailscale/ip:
  curl -i https://127.0.0.1 --header 'Host: portainer.your-domain.tld' -k
  ```
* Check certs if using custom `/certs/*.pem`:

  ```bash
  openssl x509 -in ./certs/fullchain.pem -noout -text | sed -n 's/ *Subject: //p; s/ *DNS://p'
  ```

  Ensure SANs include exactly the host you’re testing.

## 1.5 Restart & validate

```bash
# Restart traefik cleanly
docker compose -f compose-traefik.yml down
docker compose -f compose-traefik.yml up -d

# Tail logs at DEBUG for a minute to watch ACME + routing:
docker logs -f traefik | sed -n '1,200p'
# (temporarily set log.level=DEBUG in traefik-static.yml)

# Smoke tests (examples)
curl -sSk https://portainer.your-domain.tld -D- | head
curl -s http://localhost:80 -H 'Host: portainer.your-domain.tld' -I
curl -s https://localhost -H 'Host: portainer.your-domain.tld' -k -I
```

---

# Common gotchas we’ve hit before (worth checking now)

* **Multiple `providers.file` fragments** pointing at different files—keep one, and have it include a single `dynamic.yml`.
* **`traefik.enable=false` left over** from a copy; the router will never appear.
* **Forgot `traefik.docker.network=traefik`**—Traefik can’t reach the container IP on the correct network.
* **Using IPs in tests without `Host:`**—SNI mismatch leads to the TLS error you saw.
* **ACME DNS creds missing at runtime**—`PORKBUN_*` must be env-vars in the *Traefik* container.
* **Permissions**—`acme.json` must be `600` or Traefik refuses to write.
* **Mixed case/typos**—`certResolver` vs `certresolver` (labels are lowercase keys).

---

# Quick triage checklist (10 minutes)

1. `docker compose -f compose-traefik.yml config` → no YAML errors.
2. `grep -R 'certresolver' -n` → every router uses `letsencrypt`.
3. `docker logs traefik | tail -n 100` → no “resolver not found” errors.
4. `docker network inspect traefik` → all routed services attached.
5. `curl -I -H 'Host: portainer.your-domain.tld' https://127.0.0.1 -k` → 200/302 expected.
6. Flip ACME to **staging**, confirm issuance, then back to prod.

---

# Optional: make it bulletproof

* **Profiles**: put Traefik + core apps under a `core` profile; experimental stuff under `lab`.
* **Healthchecks** for every service; gate exposure with `depends_on: condition: service_healthy`.
* **Yamllint pre-commit** and a tiny `yq` script to enforce single `labels:` per service.
* **`traefik.yml` vs args**: keep all static config in the file; avoid drift between file and `command:` flags.
* **CA chain**: if you’re mixing internal CA + Let’s Encrypt, be sure clients have the internal root installed, and use distinct hostnames so you don’t confuse which cert should answer.

If you want, paste one of the broken `compose-*.yml` files and I’ll normalize the labels and router bits inline so you can drop-in replace.
