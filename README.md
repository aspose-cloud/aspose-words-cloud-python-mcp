# Aspose.Words Cloud MCP Server

Word document processing — convert, create, compare, replace text, and read properties/statistics/bookmarks.

An [MCP](https://modelcontextprotocol.io) server exposing Aspose.Words Cloud's REST API as typed,
agent-callable tools. Also bundles Aspose Storage Cloud's core file operations
(`storage_upload_file`/`storage_download_file`/`storage_list_files`/`storage_delete_file`), so a
client connected to only this server can complete a full upload -> process -> download workflow with
no second server connection.

Handles: DOCX, DOC, RTF, ODT.

---

## Requirements

- Python 3.11 or later
- An [Aspose Cloud](https://dashboard.aspose.cloud/) account (free evaluation tier available) - you'll
  need a **Client ID** and **Client Secret** from your dashboard's Applications page
- An MCP-compatible AI client (Claude Desktop, Claude Code, VS Code, Cursor, Cline, Windsurf, etc.)

---

## Setup

### 1. Create a virtual environment and install

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install git+https://github.com/aspose-cloud/aspose-words-cloud-python-mcp.git
```

This installs the `aspose-words-mcp` command into your virtual environment.

### 2. Configure your AI client

Two environment variables are required - both come from your Aspose Cloud dashboard's Applications page:

| Variable | Value |
|---|---|
| `ASPOSE_CLIENT_ID` | Your application's Client ID |
| `ASPOSE_CLIENT_SECRET` | Your application's Client Secret |

Credentials are never passed as a tool parameter - the server resolves them once at launch from
these environment variables, exchanges them for a short-lived OAuth2 token, and caches/refreshes it
transparently.

#### Claude Desktop

Config file location:

| Platform | Path |
|---|---|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "words": {
      "command": "C:\\path\\to\\.venv\\Scripts\\aspose-words-mcp.exe",
      "env": {
        "ASPOSE_CLIENT_ID": "your-client-id",
        "ASPOSE_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

On macOS/Linux, use `/path/to/.venv/bin/aspose-words-mcp` instead. Fully quit and restart Claude Desktop after
editing.

#### VS Code (`.vscode/mcp.json`), Cursor (`~/.cursor/mcp.json`), Cline, Windsurf

Same shape, under a `"servers"` key instead of `"mcpServers"` for VS Code:

```json
{
  "servers": {
    "words": {
      "type": "stdio",
      "command": "/path/to/.venv/bin/aspose-words-mcp",
      "env": {
        "ASPOSE_CLIENT_ID": "your-client-id",
        "ASPOSE_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

---

## Available tools

| Tool | What it does | Read-only | Dry-run |
|---|---|---|---|
| `words_get_document_bookmarks` | Get a Word document's bookmarks | yes | - |
| `words_compare_document` | Compare a Cloud-stored Word document against another and produce a tracked-changes result | no | yes |
| `words_download_document` | Download an existing Cloud-stored Word document in a given format | yes | - |
| `words_convert_to_format` | Convert a local Word document to another format | yes | - |
| `words_save_document_as` | Save a Cloud-stored Word document in another format via explicit save options | no | yes |
| `words_get_document_properties` | Get a Word document's built-in and custom properties | yes | - |
| `words_get_document_statistics` | Get a Word document's statistics (word/page/paragraph counts, etc.) | yes | - |
| `words_replace_text` | Replace text within a Cloud-stored Word document | no | yes |
| `words_create_document` | Create a new, blank Word document in Aspose Cloud Storage | no | yes |

Every mutating tool marked "yes" under **Dry-run** accepts a `dry_run=true` parameter to preview
the change without applying it.

Tool errors use a fixed taxonomy (bad input / auth failure / server error / rate limited), returned
as structured MCP tool errors - never a silent failure or a raw exception message.

---

## Part of the Aspose Cloud MCP family

One MCP server per Aspose Cloud product, published under [github.com/aspose-cloud](https://github.com/aspose-cloud).
This server depends on [`aspose-storage-core-mcp`](https://github.com/aspose-cloud/aspose-storage-cloud-python-mcp)
for its bundled storage tools — that repo is a shared library, not a standalone server (there's no
real Aspose Cloud API route for storage on its own; every real storage call goes through some
product's own gateway, this one included).

---

## License

MIT (see [`LICENSE`](LICENSE)) — covers only this repository's own MCP wrapper/integration code.
It does **not** cover, and grants no rights to, the Aspose Cloud product or API themselves, which
remain governed entirely by [Aspose's own product and usage terms](https://purchase.aspose.cloud/policies).
A valid Aspose Cloud account and subscription/credentials are required to actually call the API,
regardless of this code's license.
