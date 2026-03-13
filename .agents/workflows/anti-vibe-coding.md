---
description: Engenharia de Prompt e Desenvolvimento "Anti-Vibe Coding" (Akita Way) — Fluxo obrigatório antes de entregar qualquer produto ao usuário.
---

# Skill: Anti-Vibe Coding (Akita Way)

> **Regra zero:** Este fluxo é **obrigatório** antes de qualquer entrega de código funcional.  
> Se eu (Antigravity) tentar pular etapas, o usuário deve me parar e apontar qual fase foi violada.

---

## Princípios Fundamentais

1. **Disciplina > Intuição**  
   Não confiar na intuição da IA. Usar disciplina técnica para estruturar o problema **antes** de gerar qualquer linha de código.

2. **Anti-Vibe Coding**  
   Nunca aceitar uma resposta da IA sem antes analisar, validar e entender se ela faz sentido dentro do contexto do sistema.

3. **Planejamento Antes da Execução**  
   A IA acelera a implementação, mas o **design da arquitetura**, a **definição dos serviços** e os **requisitos** são definidos pelo humano.

---

## O Fluxo de Trabalho (4 Fases)

### Fase 1 — Fundação e Estrutura

1. **Definir o Domínio do Problema**
   - Quais componentes são necessários (DB, APIs externas, serviços, hardware)?
   - Qual é o escopo exato da entrega?
   - Quais são as entradas e saídas esperadas?

2. **Criar/Atualizar o CLAUDE.MD (Spec que Evolui)**
   - Localização: raiz do projeto (`CLAUDE.MD`)
   - Conteúdo obrigatório:
     - Stack tecnológica escolhida
     - Variáveis de ambiente
     - Estrutura de diretórios
     - Responsabilidade de cada serviço/módulo
   - **Regra:** Toda decisão de design e regra de negócio deve ser registrada neste arquivo **conforme evolui**. Ele é a fonte de verdade viva do projeto.

3. **Validação com o Usuário**
   - Apresentar a arquitetura proposta ao usuário **antes** de escrever implementação.
   - O usuário aprova, ajusta ou rejeita. Só então segue-se para a Fase 2.

---

### Fase 2 — Desenvolvimento com TDD

1. **Testes Primeiro, Sempre**
   - Antes de qualquer implementação, escrever os testes unitários e/ou de integração para a feature solicitada.
   - O código de produção só é escrito **depois** que os testes existem e falham (Red → Green → Refactor).

2. **Recusa Ativa**
   - Se a IA (eu) tentar sugerir implementação sem os respectivos testes, o usuário deve **recusar** e exigir os testes primeiro.
   - Se a IA alucinar ou divergir do plano, o usuário toma o controle: para a IA, desativa sugestão automática e edita manualmente.

3. **Cobertura Mínima**
   - Todo módulo novo deve ter pelo menos:
     - Teste de caminho feliz (happy path)
     - Teste de entrada inválida / edge case
     - Teste de integração se o módulo se comunica com outro serviço

---

### Fase 3 — Segurança e Isolamento

1. **AI-Jail (Sandboxing)**
   - Não executar a IA diretamente na máquina local de forma desenfreada.
   - Preferir Docker Containers para isolar o ambiente de execução quando possível.

2. **Modelo de Permissões**
   - Monitorar cada comando que a IA tenta executar no terminal.
   - Comandos destrutivos (delete, format, drop, rm) **nunca** são auto-aprovados.

---

### Fase 4 — Refatoração Multisserviço

1. **Contexto Compartilhado (Monorepo)**
   - Manter a estrutura de monorepo para que a IA tenha visão global de todos os serviços.
   - Refatorações que afetam múltiplos pontos do sistema devem ser planejadas em conjunto.

2. **Testes Cruzados**
   - Se um serviço altera estrutura de dados, o teste de integração entre consumidor e provedor deve falhar imediatamente.
   - Nunca fazer merge/deploy sem que todos os testes cruzados passem.

---

## Checklist de Entrega (Obrigatório)

Antes de entregar **qualquer** produto ao usuário, validar:

- [ ] **CLAUDE.MD** está atualizado com a decisão de design atual?
- [ ] **Arquitetura** foi apresentada e aprovada pelo usuário?
- [ ] **Testes** foram escritos antes da implementação?
- [ ] **Testes passam** no ambiente local?
- [ ] **Nenhum comando destrutivo** foi executado sem aprovação?
- [ ] **Documentação** reflete o estado real do código?

---

## Lembretes

- **"One-Shot Prompt" é um mito.** O processo é iterativo: Planejamento → Documentação → TDD → Implementação → Refatoração → Deploy.
- **Documentação é Código.** Se algo mudou na arquitetura, atualizar o CLAUDE.MD **antes** de prosseguir.
- **Não busque atalhos.** A técnica não é sobre "criar algo em 10 minutos". É sobre construir um sistema robusto e manutenível.
