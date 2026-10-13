# Comparação de qualidade das skills do AIWorkbench

Data: 13 de outubro de 2026. Escopo: as 15 skills locais na versão 1.1.0 e os recursos, validadores e casos de avaliação do pacote. A análise compara conteúdo e mecanismos observáveis; não é uma comparação experimental de desempenho entre agentes.

Este é o diagnóstico histórico da versão 1.1.0. A revisão 1.2.0 aplica as correções de formato, conteúdo e infraestrutura; consulte [o relatório atual](../evals/reports/latest.md) e [os testes independentes](../evals/reports/forward-tests.md) para a evidência e os limites da revisão.

## Conclusão

O pacote tem uma base organizada para uso assistido: descrições com limites, instruções curtas, arquivos portáteis e verificação explícita. A revisão anterior melhorou essa base. Ainda falta conhecimento operacional suficiente e evidência de eficácia para classificá-lo como um pacote de alta qualidade comprovada. Os exemplos externos mais úteis combinam escopo concreto, instruções que resolvem dificuldades reais, recursos específicos e avaliações executadas.

Não atribuo uma nota numérica ao pacote: sua rubrica atual não define os níveis 0–4 com exemplos, e não há ensaios comportamentais para sustentar uma nota de eficácia.

## Referências examinadas

| Origem e recurso | Característica observada | Aplicação ao AIWorkbench |
| --- | --- | --- |
| [OpenAI: Playwright](https://github.com/openai/skills/blob/main/skills/.curated/playwright/SKILL.md) | Define pré-requisito, sequência de interação, comandos, atualização de referências de elementos e recuperação de referências obsoletas. | Associar instruções a condições observáveis, inclusive quando uma ação falha. |
| [OpenAI Agents SDK: code-change-verification](https://github.com/openai/openai-agents-python/blob/main/.agents/skills/code-change-verification/SKILL.md) | Especifica quais mudanças exigem a verificação, como executá-la e quais falhas impedem concluir. É uma skill de um repositório específico. | Manter princípios portáteis, mas acrescentar referências para procedimentos concretos de cada ambiente quando necessário. |
| [Anthropic: skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | Inclui comparação com baseline, resultados por critério, tempo e tokens, leitura de rastros e avaliação da ativação da skill. | Construir o executor e os avaliadores, além das especificações dos casos. |
| [Anthropic: frontend-design](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | Relaciona decisões visuais ao conteúdo e ao brief; orienta revisão do plano e crítica de telas renderizadas. | Ensinar julgamento visual por exemplos e critérios ligados ao produto. |
| [Vercel Engineering: React best practices](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md) e [regra de operações independentes](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/async-parallel.md) | Organiza regras por impacto e contém exemplos de código incorreto e corrigido com condição de aplicação. | Adicionar exemplos de falha, solução e exceções nas referências técnicas pertinentes. |
| [Google Gemini: gemini-api-dev](https://github.com/google-gemini/gemini-skills/blob/main/skills/gemini-api-dev/SKILL.md) | Traz exemplos de SDK e orienta consultar documentação atual. O repositório informa que não é um produto Google oficialmente suportado. | Registrar fontes e condições de atualização para conteúdo dependente de APIs e versões. |

São exemplos selecionados em repositórios dos mantenedores, acessados na data acima. Não representam uma auditoria de todos os pacotes dessas organizações. A autoria institucional não garante que toda regra deva ser copiada: requisitos próprios do produto e do ambiente precisam continuar prevalecendo.

## Qualidade observada no pacote

| Dimensão | Avaliação documental | Evidência |
| --- | --- | --- |
| Escopo e seleção | Base útil; acerto de seleção desconhecido | Descrições incluem propósito e exclusões, mas ainda não há medidas de ativação correta. |
| Estrutura e distribuição | Base portátil; conformidade incompleta | Links externos à pasta foram removidos, mas todas as skills têm `version` no nível superior do frontmatter. |
| Orientação operacional | Parcial | Guias têm entre 404 e 500 bytes e descrevem métodos, sem exemplos completos de contratos, dados ou falhas. Brevidade por si só não é um defeito; a lacuna é a falta de material que resolva decisões difíceis. |
| Exemplos | Parcial | Há um pequeno exemplo narrativo por skill. O arquivo `examples/cases.md` não é apontado em `SKILL.md`, cujo bloco de exemplos contém apenas invocações. |
| Entregas | Genéricas | As 15 skills compartilham o mesmo template de handoff, inclusive arquitetura, UI, segurança e avaliação. |
| Recuperação | Genérica | A seção comum manda parar quando evidência ou verificação for insuficiente, sem distinguir uma lacuna declarável de um bloqueio real. |
| Avaliação | Especificações iniciais; eficácia desconhecida | Existem 120 casos, um único contexto e critérios idênticos para todos os casos positivos e adversariais de cada suite. |
| Segurança | Princípios úteis; controles não exercitados | Autorizações e conteúdo não confiável são citados; não há fixtures executáveis de negação, idempotência ou recuperação. |
| Manutenção | Parcial | Há versões e documentação de contribuição; faltam níveis ancorados da rubrica e evidência de atualização por fonte. |

As contagens acima foram obtidas diretamente dos arquivos locais. Não provam que as skills falham em uso; mostram quais afirmações de qualidade ainda não podem ser sustentadas.

## Achados prioritários

### 1. Corrigir a conformidade do frontmatter

A [especificação Agent Skills](https://agentskills.io/specification) reserva `metadata` para propriedades adicionais, como versão. O [validador de referência](https://github.com/agentskills/agentskills/blob/main/skills-ref/src/skills_ref/validator.py) rejeita campos superiores fora de sua lista permitida. As 15 skills atuais usam `version: 1.1.0` no nível superior; os validadores locais exigem essa forma.

Ação: migrar para `metadata.version`, usar um parser YAML real e validar contra o padrão. Verificar tipos, comprimentos, nomes, campos extras e metadados de interface separadamente. O fato de um host tolerar um campo extra não comprova portabilidade.

### 2. Transformar casos em avaliações executáveis e justas

`run_evals.py` declara corretamente `not_run`, mas não executa um agente. `grader: [schema, rubric, outcome]` nomeia categorias sem ligar a funções de avaliação. Os contextos não fornecem repositórios, dados ou ferramentas simuladas que permitam reproduzir os casos.

Há também inadequação entre tarefa e critério: uma solicitação para projetar um agente recebe critérios de exercício de falhas e verificação de estado final, assim como uma solicitação de implementação. A avaliação pode penalizar uma resposta de projeto adequada ou aceitar uma implementação incompleta.

Ação: separar testes de seleção dos testes de execução. Cada caso precisa de inputs reais ou fixtures, produto esperado e condições verificáveis específicas. Comparar sem skill, com versão anterior e com candidata quando isso for útil, mantendo modelo, permissões e orçamento equivalentes. Guardar saídas, rastros e decisões dos avaliadores. Critérios subjetivos precisam de revisão humana calibrada.

### 3. Trocar apoio genérico por conhecimento reutilizável

Criar exemplos de entrada, decisão, saída e verificação nos domínios em que isso evita erros reais. Links em `SKILL.md` devem dizer quando ler cada exemplo. Templates devem orientar o tipo de entrega pertinente; não é necessário exigir um relatório com sete seções para uma mudança simples.

Concentrar scripts em trabalho repetitivo comprovado. Os 15 `verify.py` atuais apenas verificam arquivos do próprio pacote; eles não validam tarefas do usuário. Essa função deve permanecer claramente rotulada e pode ser centralizada na manutenção do catálogo.

### 4. Reduzir instruções que criam atrito

Os validadores exigem as mesmas seções e arquivos para todas as skills. Isso estimula repetição e faz a presença de um heading parecer evidência de qualidade. O verificador de descrições exige frases literais em inglês, que não demonstram seleção correta.

Ação: exigir os elementos do formato e os recursos realmente referenciados. Avaliar seleção com pedidos reais em português e inglês. Reescrever recuperação para continuar o trabalho independente quando faltar uma ferramenta e declarar o limite, interrompendo apenas a parte que depende do bloqueio.

Também revisar regras absolutas: a skill de agentes repete conteúdo não confiável e exige aprovação para ações irreversíveis sem considerar explicitamente a autorização já existente; a skill de UI exige um avaliador separado mesmo quando ele não está disponível. Essas condições devem respeitar o contexto e o escopo solicitado.

## Próxima melhoria para cada uma das 15 skills

| Skill | Recurso que mais ajudaria o uso | Como comprovar a melhoria |
| --- | --- | --- |
| senior-software-engineer | Exemplo completo de mudança com contrato, concorrência/retry e teste de regressão. | Repositório mínimo com bug reproduzível; verificar comportamento e compatibilidade após o patch. |
| code-review-and-refactoring-expert | Exemplo de finding com localização, condição e impacto; exemplo de refatoração com caracterização de comportamento. | Diff com defeitos conhecidos e alternativas válidas; medir defeitos encontrados, falsos positivos e preservação do comportamento. |
| tech-lead | Plano preenchido com marcos, dependências, responsáveis, critérios de saída e decisão de rollout. | Caso com restrições e dependências conhecidas; conferir completude e viabilidade por uma rubrica ancorada. |
| full-stack-architect | ADR e fluxo de falha preenchidos, com propriedade de dados, consistência e premissas de capacidade. | Caso com requisitos conflitantes; verificar cobertura dos requisitos e coerência da recuperação. |
| frontend-experience-engineer | Fluxo verificável em navegador com estados, teclado, foco e erro de rede. | Interface e servidor local controlados; conferir interação e renderização em viewports definidos. |
| premium-ui-designer | Exemplos renderizados comentados, com critérios ligados ao brief e ao conteúdo. | Comparação cega de telas com brief equivalente; avaliar legibilidade, hierarquia, adequação e estados. |
| design-system-architect | Token e contrato de componente preenchidos, incluindo tema, estados e migração. | Consumidores de exemplo que testem compatibilidade, temas e interação acessível. |
| ux-product-designer | Protocolo de tarefa e exemplo de análise que diferencie observação, hipótese e decisão. | Dados de pesquisa fornecidos; verificar fidelidade às evidências e recuperação nos fluxos. |
| ai-agent-engineer | Contrato de ferramenta e máquina de estados com timeout, retry, idempotência e escalonamento. | Ferramentas locais simuladas; verificar estado final, duplicidade, negação e recuperação. |
| context-and-prompt-engineer | Prompt, schema e casos preenchidos, incluindo instruções injetadas e corte de contexto. | Executar inputs fixos e adversariais; medir schema válido, tarefa correta e custo. |
| rag-knowledge-engineer | Corpus pequeno com perguntas rotuladas, ACLs, revisão, exclusão e citações esperadas. | Verificar recuperação separadamente da resposta e testar acesso indevido e conteúdo removido. |
| ai-evaluation-engineer | Runner real e avaliadores que detectem resultados certos, errados e válidos por caminhos alternativos. | Controles positivos e negativos para os próprios avaliadores; relatório de trials e variância. |
| security-and-guardrails-engineer | Ameaça reproduzível com condição de exploração e controle verificável. | Testes de autorização negativa, limites de ferramenta e ausência de segredos em logs. |
| performance-and-reliability-engineer | Protocolo de benchmark preenchido e análise de medições reais. | Carga comparável antes/depois, distribuição de latência, recursos, erros e correção. |
| ai-product-strategist | Matriz de evidências e experimento preenchidos, com baseline e regra de decisão. | Caso com informações incompletas; avaliar separação entre evidência e suposição e viabilidade do teste. |

Nenhuma dessas melhorias exige transformar cada skill em uma enciclopédia. Acrescentar um recurso deve resolver uma dificuldade observada, e o recurso deve ser carregado somente no cenário relevante.

## Critério de liberação proposto

1. Passar a validação do formato oficial e de portabilidade.
2. Executar alguns casos reais e difíceis de cada skill, com comparações equivalentes. Expandir a cobertura a partir de falhas observadas; não usar a contagem fixa de oito casos como prova de suficiência.
3. Não regredir casos críticos de escopo, autorização e veracidade da evidência.
4. Demonstrar ganho em um resultado relevante ou em eficiência, com limite aceitável na outra dimensão. Definir esses limites antes das execuções.
5. Publicar modelo, host, data, configuração, trials, critérios, resultados e limitações.

Começar por senior-software-engineer, code-review-and-refactoring-expert, ai-agent-engineer e ai-evaluation-engineer cria os mecanismos de implementação, revisão e medição que as demais áreas poderão reutilizar.

## O que os estudos permitem concluir

O [SkillsBench v4](https://arxiv.org/abs/2602.12670v4), revisado em junho de 2026, relata ganho médio de 16,6 pontos percentuais em sua avaliação agregada e melhor resultado para pacotes focados com até três módulos. A conclusão útil é testar eficácia em condições pareadas e manter o conteúdo relevante. Esse resultado não é uma previsão para o AIWorkbench.

O [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) apresenta resultados preliminares nos quais muitas skills não melhoraram o sucesso e algumas aumentaram bastante o custo. Seu desenho e escopo diferem do SkillsBench; os resultados não devem ser tratados como diretamente intercambiáveis. Eles reforçam que reputação, tamanho e número de regras são insuficientes para comprovar benefício.

O [experimento publicado pelo Google](https://developers.googleblog.com/closing-the-knowledge-gap-with-agent-skills/) testa uma lacuna concreta de atualização de SDK em 117 prompts. Esse foco em um erro observável é uma referência útil para criar testes do nosso pacote.

O pacote está adequado para uso assistido e iteração com revisão humana. Alta qualidade comprovada depende das execuções e das evidências descritas acima.
