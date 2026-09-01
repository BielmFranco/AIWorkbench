![AIWorkbench](assets/aiworkbench-banner.png)

# AIWorkbench

Skills profissionais para agentes de codificação projetarem, implementarem, revisarem e evoluírem software com critérios verificáveis.

[![Baixar ZIP](https://img.shields.io/badge/Baixar-ZIP-7c3aed?style=for-the-badge)](https://github.com/BielmFranco/AIWorkbench/archive/refs/heads/main.zip)
[![Licença MIT](https://img.shields.io/badge/Licen%C3%A7a-MIT-111827?style=for-the-badge)](LICENSE)

> Status: desenvolvimento inicial. Validações automatizadas comprovadas serão publicadas em `evals/reports/`.

## Instalação

```bash
git clone https://github.com/BielmFranco/AIWorkbench.git
cd AIWorkbench
```

### Codex

```powershell
.\scripts\install.ps1 -Target codex
```

```bash
./scripts/install.sh codex
```

O comando instala todas as skills. Depois, invoque diretamente no prompt:

```text
$full-stack-architect projete a arquitetura deste produto
```

### Claude Code

```powershell
.\scripts\install.ps1 -Target claude
```

```bash
./scripts/install.sh claude
```

O comando instala todas as skills. Depois, invoque diretamente:

```text
/full-stack-architect projete a arquitetura deste produto
```

### ChatGPT, OpenAI API ou Anthropic API

Gere arquivos ZIP portáveis:

```bash
python scripts/package_skills.py --all
```

Os 15 pacotes serão criados em `dist/`. Faça upload pela interface ou Skills API disponível no produto e na sua conta. O instalador não envia credenciais nem publica arquivos externamente.

Para instalar apenas uma skill, adicione seu nome ao comando:

```powershell
.\scripts\install.ps1 -Target codex -Skill premium-ui-designer
```

## Catálogo

O projeto inclui 15 skills cobrindo produto, liderança técnica, arquitetura, engenharia full-stack, frontend, UI premium, design systems, UX, agentes, prompts, RAG, evals, segurança, performance e revisão/refatoração.

Consulte [arquitetura](docs/architecture.md), [roteamento](docs/routing.md), [padrão de qualidade](docs/quality-standard.md) e [compatibilidade](docs/compatibility.md).

## Validação

```bash
python scripts/validate.py
python scripts/run_evals.py
```

## Licença

[MIT](LICENSE)
