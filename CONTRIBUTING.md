# Contribuindo

1. Mantenha cada skill focada e com gatilhos discriminantes.
2. Escreva decisões e exemplos específicos do domínio; mantenha cada skill portátil, sem links para fora da própria pasta.
3. Atualize os casos correspondentes em `evals/cases/`, incluindo pedidos próximos que não devem ativar a skill.
4. Instale `requirements-dev.txt`; execute os validadores, `python -m unittest discover -s tests -v` e `python scripts/run_evals.py`. O formato portátil usa `metadata.version`; recursos são opcionais e precisam ser úteis e acessíveis.
5. Compare a skill com uma execução sem ela antes de afirmar ganho de qualidade. Registre modelo, configuração, rastros, resultados e custo. `run_evals.py` valida especificações e não executa o agente.
6. Declare testes não executados e mudanças de comportamento.

Casos novos devem seguir `shared/schemas/eval-case.schema.json`, usar fixtures próprias e distinguir seleção, implementação e entregas de projeto. Teste o avaliador com controles corretos, incorretos e alternativas válidas antes de confiar em uma taxa de acerto. A CI executa somente verificações determinísticas; ensaios com provedor são explícitos e limitados.

Não inclua segredos, dados privados ou resultados inventados.
