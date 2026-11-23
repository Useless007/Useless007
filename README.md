<!-- gen:header -->
<img src="assets/header.svg" alt="useless007, full-stack developer in Thailand">
<!-- /gen:header -->

I build the whole thing: the service in Go, Rust or TypeScript, the UI in front of it, and the box
it runs on. Lately most of it has a model running locally rather than behind someone else's API,
and a check on its output before anyone has to trust it.

<!-- gen:rr -->
<a href="https://github.com/Useless007/rr-stack"><img src="assets/rr-stack.svg" alt="rr-stack: React Router + Rust (Axum), typed from the database to the screen. The same title field lights up in postgres, rust, openapi.json, typescript, react router, then bun run check exits 0."></a>
<!-- /gen:rr -->

**[rr-stack](https://github.com/Useless007/rr-stack)** is a starter for apps that AI agents write
and people review. `bun run check` exits 0 only when the SQL, the Rust API, the OpenAPI contract
and the React code agree, on Linux, macOS and Windows. Open the [live demo](https://rrstack.vercel.app),
or start a project with [`create-rr-stack`](https://www.npmjs.com/package/create-rr-stack):

```bash
bun create rr-stack my-app
```

### Selected work

<!-- gen:work -->
<p>
<a href="https://github.com/Useless007/nebula-guard"><img src="assets/card-nebula-guard.svg" width="49%" alt="nebula-guard: SSH honeypot. A Go agent feeds Cowrie logs to a local Gemma model and sends a Thai read of each intrusion to Telegram. (Go, Next.js, PostgreSQL, Ollama, Docker)"></a>
<a href="https://github.com/Useless007/content-blueprint"><img src="assets/card-content-blueprint.svg" width="49%" alt="content-blueprint: Windows app for content teams. It drives the Claude Code or Codex CLI you already use, re-checks every result in Go and never publishes for you. (Go, Wails, MCP, GitHub Actions)"></a>
<a href="https://github.com/Useless007/bun-rag-starter"><img src="assets/card-bun-rag-starter.svg" width="49%" alt="bun-rag-starter: Graph RAG over your own documents. Redis HNSW vectors and a Neo4j graph answer together, from local embeddings, inside the sources. (Bun, Elysia, Neo4j, Redis, Svelte)"></a>
<a href="https://github.com/Useless007/THESIS_FASTAPI_YOLO"><img src="assets/card-THESIS_FASTAPI_YOLO.svg" width="49%" alt="THESIS_FASTAPI_YOLO: Thesis. An IoT parts store where a YOLO model checks each package against its order before it ships. (Python, FastAPI, YOLO)"></a>
<a href="https://github.com/Useless007/btc-rainbow-worker"><img src="assets/card-btc-rainbow-worker.svg" width="49%" alt="btc-rainbow-worker: Cron Worker that computes the Bitcoin power-law band from the formula, with three price sources behind a fallback chain. (TypeScript, Cloudflare Workers, Bun)"></a>
<a href="https://github.com/Useless007/zig-typist"><img src="assets/card-zig-typist.svg" width="49%" alt="zig-typist: Terminal typing trainer for Thai and English layouts. Each session appends to a JSON Lines file you can grep. (Zig)"></a>
</p>
<!-- /gen:work -->

### Not public

The work I spend the longest on lives in private repos. Short version:

<!-- gen:private -->
<img src="assets/private.svg" alt="icefactory-app: Multi-tenant plant management for an ice factory, delivered in stages. Every query scopes to the tenant and branch on the session, never to what the request sends. Every write lands in an append-only audit log, and the tests fail if either rule breaks. (Go, Next.js, PostgreSQL). guess-my-song: Guess-the-song game built from the player's own Spotify library. Hono on Cloudflare Workers, one Durable Object per session, and one hostname for both apps, so the cookie stays first-party and there is no CORS. (TypeScript, Hono, Durable Objects, Astro). pea-calculator-backup: Electricity-meter tracker. The app encrypts the database before it leaves the machine, the key never enters Git or the image, and the scheduler runs the backups it missed. (Node.js, Docker).">
<!-- /gen:private -->

### Tools I reach for

<!-- gen:tools -->
<img src="assets/stack.svg" alt="Go, Rust, TypeScript, Python, Zig, Java; React Router, Next.js, Svelte, Astro, Axum, Elysia, Hono, Bun, FastAPI, Fiber, Tailwind; PostgreSQL, SQLx, Redis, Neo4j, SQLite, Prisma; Docker, Linux, Cloudflare Workers, Vercel, GitHub Actions, Wails; Ollama, YOLO, Graph RAG, MCP">
<!-- /gen:tools -->

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="dist/github-contribution-grid-snake-dark.svg">
  <img src="dist/github-contribution-grid-snake.svg" alt="A snake eating this year's contribution graph">
</picture>

<sub>ITI, KMUTNB Prachinburi. Off hours: power-law charts, Kirby on the GBA, and a dog named Panda.</sub>

<!-- Every SVG in assets/ and the gen: blocks above come from: python3 assets/build_assets.py -->
