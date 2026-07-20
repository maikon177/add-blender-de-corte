# Add Blender de Corte (Irregular Joint Maker)

Add-on para Blender focado em criar **encaixes irregulares** com tolerância para impressão em resina (SLA).

Desenvolvido especialmente para separar peças de personagens (ex: ombro da blusa) de forma limpa, com inserção parcial e pinos de alinhamento.

---

## Objetivo

Permitir que o usuário:
- Escolha exatamente onde vai acontecer o corte irregular
- Defina a profundidade de inserção (quanto a peça entra dentro da outra)
- Escolha onde criar o pino de encaixe
- Aplique tolerância correta (fêmea recebe a folga)
- Tenha o máximo de proteção contra erros comuns de Boolean + impressão em resina

---

## Como funciona o encaixe (conceito)

| Parte              | Ação                                      | Tolerância          |
|--------------------|-------------------------------------------|---------------------|
| **Blusa (Fêmea)**  | Boolean Difference com cortador **maior** | Recebe a folga      |
| **Ombro (Macho)**  | Boolean Difference + entra na blusa       | Tamanho original    |
| **Pino**           | Criado no macho + furo correspondente     | Tolerância própria  |

---

## Funcionalidades Planejadas

### Núcleo
- [ ] Seleção manual da região de corte (loop ou faces)
- [ ] Definição de profundidade de inserção
- [ ] Posicionamento manual do pino de encaixe
- [ ] Tolerância configurável (principal + pino)
- [ ] Preview visual antes de aplicar

### Proteções (Fail-safe)
- [ ] Verificar e aplicar Scale/Rotation automaticamente
- [ ] Checar quantidade de polígonos (aviso se muito alto)
- [ ] Recalcular normals (faces invertidas)
- [ ] Verificar se é manifold
- [ ] Aplicar todos os modificadores antes do Boolean
- [ ] Detectar interpenetração prévia entre objetos
- [ ] Checar unidades da cena (forçar ou avisar mm)
- [ ] Backup automático dos objetos originais
- [ ] Garantir que o cortador atravessa completamente a peça
- [ ] Aviso sobre destruição de UVs / Vertex Groups / Materials

### Melhorias de Qualidade
- [ ] Opção de Draft Angle (ângulo de saída)
- [ ] Verificação de parede fina após o corte
- [ ] Opção de furo de drenagem (para resina)
- [ ] Relatório final (manifold, faces, tolerância aplicada)

---

## Status Atual

**Fase:** Planejamento e documentação  
Nenhum código funcional ainda. Estamos definindo a arquitetura à prova de falhas.

---

## Estrutura do Projeto

- `README.md` → Visão geral e funcionalidades
- `PROBLEMAS.md` → Lista completa de problemas conhecidos + soluções + status

---

## Autor

Desenvolvido em conjunto com Grok (xAI)
