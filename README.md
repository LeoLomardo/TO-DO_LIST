# Flask Clean Architecture Example

Este projeto demonstra uma estrutura simples seguindo os principios de Clean Architecture e SOLID usando Flask e SQLite.

## Estrutura
- `app/` – aplicação Flask e blueprints de rotas
- `domain/` – entidades e interfaces de repositórios
- `use_cases/` – casos de uso (regras de negócio)
- `infra/` – implementação dos repositórios e configuração do banco
- `tests/` – testes unitários usando Pytest

Funcionalidades disponíveis:
- Criar tarefa
- Listar tarefas
- Alternar status (concluir/reabrir)
- Excluir tarefa
- Registrar e fazer login de usuário
- Tarefas associadas ao usuário logado

## Executando

```bash
pip install flask pytest
python main.py
```

Abra `http://localhost:5000` em seu navegador para acessar a interface web.

## Testes

```bash
pytest -q
```
