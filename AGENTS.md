# Aspose.Words Cloud MCP Server - Agent Guide

Guidance for AI agents connected to this MCP server.

## Core rules

1. **Credentials are never a tool parameter.** They're resolved once at server launch from the
   `ASPOSE_CLIENT_ID`/`ASPOSE_CLIENT_SECRET` environment variables. Never ask the user to pass a
   credential into a tool call, and never accept one if offered.
2. **This server bundles Aspose Storage Cloud's core-4 tools** (`storage_upload_file`,
   `storage_download_file`, `storage_list_files`, `storage_delete_file`) so you can complete a full
   workflow without a second server connection: upload a file, call a `words_*` tool against it
   by filename, then download the result.
3. **One product per server.** This server only understands DOCX, DOC, RTF, ODT. Route a request for
   a different file format to that format's own Aspose Cloud MCP server
   (`aspose-<product>-cloud-python-mcp` under [github.com/aspose-cloud](https://github.com/aspose-cloud))
   rather than attempting it here.
4. **Every mutating tool supports a dry-run.** Pass `dry_run=true` to preview a destructive or
   costly operation before committing to it - use this when the user's intent is ambiguous.
5. **Tool errors are structured**, not raw exceptions (bad input / auth failure / server error /
   rate limited). Surface the real reason to the user rather than retrying blindly.

## Tools at a glance

- `words_get_document_bookmarks` - Get a Word document's bookmarks
- `words_compare_document` - Compare a Cloud-stored Word document against another and produce a tracked-changes result
- `words_download_document` - Download an existing Cloud-stored Word document in a given format
- `words_convert_to_format` - Convert a local Word document to another format
- `words_save_document_as` - Save a Cloud-stored Word document in another format via explicit save options
- `words_get_document_properties` - Get a Word document's built-in and custom properties
- `words_get_document_statistics` - Get a Word document's statistics (word/page/paragraph counts, etc.)
- `words_replace_text` - Replace text within a Cloud-stored Word document
- `words_create_document` - Create a new, blank Word document in Aspose Cloud Storage
