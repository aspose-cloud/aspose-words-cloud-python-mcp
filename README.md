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

pip install git+https://github.com/aspose-cloud/aspose-storage-cloud-python-mcp.git@v1.0.5 git+https://github.com/aspose-cloud/aspose-words-cloud-python-mcp.git@v2.0.1
```

This installs the `aspose-words-mcp` command into your virtual environment. The first package is the shared file-tool library (upload, download, list, delete) that every Aspose Cloud MCP server depends on; it is not on PyPI, so it is installed from GitHub in the same command.

### 2. Configure your AI client

Three environment variables are required. The first two come from your Aspose Cloud dashboard's Applications page; the third is a folder you create on your own computer (see [Your files folder](#your-files-folder-aspose_files_path) below):

| Variable | Value |
|---|---|
| `ASPOSE_CLIENT_ID` | Your application's Client ID |
| `ASPOSE_CLIENT_SECRET` | Your application's Client Secret |
| `ASPOSE_FILES_PATH` | Full path of the folder on your computer where your input files are placed and results are saved |

Credentials are never passed as a tool parameter - the server resolves them once at launch from
these environment variables, exchanges them for a short-lived OAuth2 token, and caches/refreshes it
transparently.

#### Your files folder (`ASPOSE_FILES_PATH`)

Create a folder on your computer (for example `C:\Users\you\Documents\aspose-files` on Windows, or
`/home/you/aspose-files` on macOS/Linux) and set `ASPOSE_FILES_PATH` to its full path. It is the one
place this server reads your files from and writes results to:

- **Input:** put the document you want processed in that folder, then ask your assistant to upload it with
  `storage_upload_file`, giving only the bare filename (for example `report.docx`). The upload sends it to
  your Aspose Cloud Storage, where the processing tools read it. Subfolders and full paths are rejected.
- **Output:** `storage_download_file` saves a result from Cloud Storage back into the same folder, and its
  reply contains the full local path of the saved file.
- The file and folder arguments of the other tools name locations in your Aspose Cloud Storage, not your
  computer.

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
        "ASPOSE_CLIENT_SECRET": "your-client-secret",
        "ASPOSE_FILES_PATH": "C:\\Users\\you\\Documents\\aspose-files"
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
        "ASPOSE_CLIENT_SECRET": "your-client-secret",
        "ASPOSE_FILES_PATH": "/home/you/aspose-files"
      }
    }
  }
}
```

---

## Available tools

| Tool | What it does | Read-only | Dry-run |
|---|---|---|---|
| `words_get_document_bookmarks` | Retrieves the list of bookmarks and their common information from a specified Word document stored in Aspose Cloud. | yes | - |
| `words_get_comments` | Retrieves all comments from a specified Word document stored in Aspose Cloud. | yes | - |
| `words_compare_document` | Compares a source Word document with another document and produces a new file that highlights the differences. | no | yes |
| `words_download_document` | Exports a document stored in Aspose Cloud to the specified output format, optionally saving the result to a given path. | yes | - |
| `words_convert_to_format` | Converts a supplied document to a specified format and returns the converted file (or saves it to a given storage path). | yes | - |
| `words_save_document_as` | The tool converts a Word document stored in Aspose Cloud to a chosen output format using the supplied save‑options and writes the resulting file to the specified storage… | no | yes |
| `words_get_document_properties` | Retrieves the full set of document properties from a Word file stored in Aspose Cloud. | yes | - |
| `words_get_available_fonts` | Retrieves the list of fonts that are available for processing Aspose.Words documents. | yes | - |
| `words_get_document_statistics` | Retrieves statistical information (e.g., word, character, paragraph, and page counts) for a specified Word document stored in Aspose Cloud. | yes | - |
| `words_replace_text` | Replaces all occurrences of a specified text pattern in a Word document stored in Aspose Cloud and optionally saves the modified document under a new name. | no | yes |
| `words_create_document` | Creates a new Word document in Aspose Cloud storage with a filename and format inferred from its extension. | no | yes |

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
