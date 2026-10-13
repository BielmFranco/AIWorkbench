# Sources

- [OpenAI: Create a skill](https://developers.openai.com/api/reference/python/resources/skills/methods/create)
- [OpenAI: Skills and progressive disclosure](https://developers.openai.com/api/docs/guides/tools-skills)
- [OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills)
- [OpenAI: Using skills to accelerate OSS maintenance](https://developers.openai.com/blog/skills-agents-sdk)
- [Anthropic: Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Anthropic: Equipping agents](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Anthropic: Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Anthropic: Agent evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Google DeepMind: Closing the knowledge gap with agent skills](https://developers.googleblog.com/closing-the-knowledge-gap-with-agent-skills/)
- [SkillsBench: paired skill evaluation across tasks](https://arxiv.org/abs/2602.12670)
- [SWE-Skills-Bench: preliminary paired evaluation in software engineering](https://arxiv.org/abs/2603.15401)

AIWorkbench applies these sources but is not endorsed by OpenAI or Anthropic.

## Maintenance record

The 2026-10-13 revision uses the public Agent Skills metadata contract, focused worked examples inspired by the inspected OpenAI/Anthropic/Vercel procedures, and paired evaluation principles from the papers above. Domain procedures are authored for AIWorkbench; they are not copied upstream API specifications. Recheck primary documentation whenever a dependency, tool protocol or product surface changes, and retain the source date and compatibility evidence when updating version-dependent instructions.

The evaluation infrastructure's Windows process lifetime handling follows [Microsoft's Job Objects documentation](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) and [extended job limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information). This controls descendant lifetime; it is not a filesystem or network sandbox.
