# Contributing

Aspose.Words Cloud MCP Server is built and released by an automated build system, and this repository is a published copy of
each release. `main` is replaced on every release, so a pull request cannot be merged here.

## How to help

Open an issue. The most useful ones say:

- the server version (the release tag you installed) and the MCP client you use;
- the tool you called and the arguments, with any file names changed to something harmless;
- what you expected, and what came back, including the error code (`bad_input`, `auth_failure`, `server_error` or
  `rate_limited`).

Never paste credentials, tokens or real customer files into an issue.

## Where an issue belongs

- A tool that behaves wrongly, a missing tool, or wrong documentation: this repository.
- A problem in Aspose Cloud's REST API itself (a call that hangs, a 5xx error, behaviour that differs from its documentation):
  Aspose's forum at <https://forum.aspose.cloud> is the place, and an issue here with a link to it helps us follow up.
- A security problem: do not open an issue. Follow [`SECURITY.md`](SECURITY.md).

## Changes to the code

Maintainers make changes in the build system and the next release brings them here. If you have a fix in mind,
describe it in an issue, with a patch if you have one, and a maintainer will carry it over.
