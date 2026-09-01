# Compatibility

| Surface | Distribution | Invocation |
| --- | --- | --- |
| Codex | `$CODEX_HOME/skills` or `~/.codex/skills` | `$skill-name <pedido>` |
| Claude Code | `~/.claude/skills` | `/skill-name <pedido>` |
| claude.ai | ZIP upload in Settings > Features when enabled | Natural request or UI |
| Anthropic API | Skills API upload | Returned skill ID |
| OpenAI API | Skills API directory or ZIP upload when available | API-dependent |
| ChatGPT | ZIP where custom Skills are enabled | Account-dependent |

Custom skills may not synchronize across product surfaces. Local installers never upload credentials.
