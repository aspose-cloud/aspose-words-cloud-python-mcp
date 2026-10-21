# Security Policy

## Reporting a vulnerability

Please report a suspected vulnerability privately. Do not open a public issue for it.

1. Use GitHub's private vulnerability reporting:
   <https://github.com/aspose-cloud/aspose-words-cloud-python-mcp/security/advisories/new>
2. Or email shahzad.latif@aspose.com with the version you are using (the release tag), what you found, and the steps to reproduce it.
   Do not include real credentials or customer files.

Every report is read and the reporter gets a reply. There is no guaranteed response time.

## Supported versions

Only the latest release receives fixes, and a fix ships as a new release. [`CHANGELOG.md`](CHANGELOG.md) lists every release.

## How Aspose.Words Cloud MCP Server handles credentials and data

- **Credentials** are read from the environment (`ASPOSE_CLIENT_ID` and `ASPOSE_CLIENT_SECRET`) and never accepted as a
  tool parameter. The server exchanges them for a short-lived access token that is kept in memory and refreshed
  before it expires. Nothing is written to disk.
- **TLS certificate validation is never disabled.**
- **Logging:** the server code does not write credentials, tokens or request or response bodies to any log.
- **Local files:** when `ASPOSE_FILES_PATH` is set, the server reads and writes only bare filenames inside that folder;
  paths with directories, absolute paths and `..` are rejected. Always set it. If it is unset, the server uses the path
  it is given as it is.
- **Files you send** to a tool are uploaded to Aspose Cloud Storage and processed by Aspose Cloud, under Aspose's own terms.
- **No network port:** the server talks to your MCP client over standard input and output.

## Secrets in this repository

Secrets are never committed. If you find one in this repository or its history, report it as above.
