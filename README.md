# routemap

Static analyzer that generates a visual map of API routes from Express or FastAPI codebases.

---

## Installation

```bash
pip install routemap
```

## Usage

Point `routemap` at your project directory and it will scan your codebase and output a visual route map.

```bash
routemap ./my-fastapi-app
```

**Example output:**

```
GET    /users              → handlers/users.py:get_users
POST   /users              → handlers/users.py:create_user
GET    /users/{id}         → handlers/users.py:get_user_by_id
DELETE /users/{id}         → handlers/users.py:delete_user
GET    /products           → handlers/products.py:list_products
POST   /auth/login         → handlers/auth.py:login
```

You can also export the map as JSON or HTML:

```bash
routemap ./my-express-app --format html --output routes.html
routemap ./my-fastapi-app --format json --output routes.json
```

### Supported Frameworks

- **FastAPI** (Python)
- **Express** (Node.js)

### Options

| Flag | Description |
|------|-------------|
| `--format` | Output format: `text`, `json`, or `html` (default: `text`) |
| `--output` | Write output to a file instead of stdout |
| `--depth` | Max directory depth to scan (default: `5`) |

## License

MIT © routemap contributors