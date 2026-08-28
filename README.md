<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" alt="useless007 — full-stack developer, Bangkok">
</picture>

I build the whole thing — the Go or TypeScript service, the UI in front of it, and the box it
runs on. Lately most of it has a model running locally rather than behind someone else's API,
and something checking the output before anyone is asked to trust it.

### Selected work

**[nebula-guard](https://github.com/Useless007/nebula-guard)** — SSH honeypot that streams Cowrie logs through a Go agent into a local Gemma model, writes the forensics to Postgres, and pushes a Thai-language read of the intrusion to Telegram. Next.js command center on top, GPU inference on my own machine.<br>
<sub>Go · Next.js · PostgreSQL · Ollama · Docker</sub>

**[content-blueprint](https://github.com/Useless007/content-blueprint)** — Windows desktop app for content teams. Calls the Claude Code or Codex CLI you are already signed into, re-validates every structured result in Go, and ships releases with published SHA-256 sums. Nothing posts or publishes on your behalf.<br>
<sub>Go · Wails · MCP · GitHub Actions</sub>

**[bun-rag-starter](https://github.com/Useless007/bun-rag-starter)** — Graph RAG over your own documents: Redis HNSW vectors and a Neo4j knowledge graph queried together, local embeddings, answers cached and fenced so the model stays inside the source material.<br>
<sub>Bun · Elysia · Neo4j · Redis · Svelte</sub>

**[THESIS_FASTAPI_YOLO](https://github.com/Useless007/THESIS_FASTAPI_YOLO)** — Thesis. An IoT parts store with role-gated staff workflows, plus a vision service that checks each package against its order before it ships and notifies the floor when the two disagree.<br>
<sub>Python · FastAPI · YOLO</sub>

**[btc-rainbow-worker](https://github.com/Useless007/btc-rainbow-worker)** — Cron'd Worker that computes the Bitcoin power-law band from the formula instead of scraping someone's chart, with three price sources behind a fallback chain.<br>
<sub>TypeScript · Cloudflare Workers · Bun</sub>

**[zig-typist](https://github.com/Useless007/zig-typist)** — Terminal typing trainer for Thai and English layouts. Sessions append to JSON Lines, so the history stays yours and stays greppable.<br>
<sub>Zig</sub>

### Not public

The work I spend the longest on mostly lives in private repos. Short version:

**icefactory-app** — Multi-tenant plant management for an ice factory, commissioned and delivered in stages. Every query scopes to the tenant and branch on the session and never to anything the request sends, and every write lands in an append-only audit log with personal fields redacted. The tests fail if any of those rules is broken.<br>
<sub>Go · Next.js · PostgreSQL</sub>

**guess-my-song** — Guess-the-song game where every clip comes from the player's own Spotify library rather than a recommendation engine. Hono on Cloudflare Workers, one Durable Object per session, both apps behind one hostname so the cookie stays first-party and there is no CORS anywhere. A policy test fails the build if any code reaches for the endpoints the design rules out.<br>
<sub>TypeScript · Hono · Durable Objects · Astro</sub>

**pea-calculator-backup** — Electricity-meter tracker. The interesting half is the backup path: the database is encrypted locally before anything leaves the machine, the key never enters Git or the image, and the scheduled job runs the backups it missed rather than skipping them.<br>
<sub>Node.js · Docker</sub>

### Tools I reach for

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <img src="assets/stack-light.svg" alt="Go, TypeScript, Python, Zig, Java · Next.js, Svelte, Elysia, Bun, FastAPI, Fiber, Tailwind · PostgreSQL, Redis, Neo4j, SQLite, Prisma · Docker, Linux, Cloudflare Workers, GitHub Actions, Wails · Ollama, YOLO, Graph RAG, MCP">
</picture>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dist/github-contribution-grid-snake-dark.svg">
  <img src="dist/github-contribution-grid-snake.svg" alt="A snake eating this year's contribution graph">
</picture>

<sub>Bangkok · IT graduate, KMUTNB · off-hours: power-law charts, Kirby on the GBA, and a dog named Panda.</sub>

<!-- Banner and stack strip are generated locally: python3 assets/build_assets.py -->
