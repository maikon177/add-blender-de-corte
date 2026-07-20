# Problemas Conhecidos e Soluções

Documento de rastreamento de riscos do add-on.

Atualize a coluna **Status** conforme formos resolvendo.

**Legenda de Status:**
- `Pendente`
- `Em andamento`
- `Corrigido`
- `Não será feito`

---

## Tabela de Problemas

| ID | Problema | O que pode causar | Solução Proposta | Status |
|----|----------|-------------------|------------------|--------|
| 01 | Scale e Rotation não aplicados | Tolerância e profundidade ficam completamente erradas | Verificar e aplicar automaticamente Scale + Rotation antes de qualquer operação | Pendente |
| 02 | Quantidade muito alta de polígonos | Boolean trava o Blender ou demora minutos | Contar faces e avisar o usuário (sugerir Remesh temporário se > 300k~500k faces) | Pendente |
| 03 | Faces invertidas (normals erradas) | Boolean gera resultado invertido ou sujo | Detectar e forçar Recalculate Outside | Pendente |
| 04 | Malha não manifold | Boolean falha ou gera geometria quebrada | Verificar manifold + tentar Make Manifold (ou avisar claramente) | Pendente |
| 05 | Modificadores não aplicados | Resultado do Boolean fica inconsistente | Forçar aplicação de todos os modificadores antes de começar | Pendente |
| 06 | Tolerância no sentido errado | Macho fica maior que o furo (não encaixa) | Sempre expandir o cortador apenas no objeto **fêmea** | Pendente |
| 07 | Unidades da cena erradas (metros vs mm) | Tolerância de 0.2 vira 200mm | Detectar unidade da cena e avisar / forçar mm | Pendente |
| 08 | Objetos já se interpenetrando | Boolean imprevisível e geometria podre | Detectar interpenetração prévia e avisar o usuário | Pendente |
| 09 | Parede fina demais após o corte | Peça quebra fácil ou não imprime direito | Verificar espessura mínima na região do corte após o Boolean | Pendente |
| 10 | Direção de inserção errada | Ombro entra para fora em vez de dentro | Preview visual claro da direção + confirmação | Pendente |
| 11 | Falta de Draft Angle | Peça trava na hora de montar (difícil encaixar) | Opção de criar leve ângulo de saída (1°~3°) | Pendente |
| 12 | Sem backup dos originais | Usuário perde o trabalho se der errado | Duplicar e esconder os objetos originais automaticamente | Pendente |
| 13 | Destruição de UVs / Vertex Groups / Materials | Modelo texturizado ou com weight paint fica estragado | Avisar o usuário antes de executar o Boolean | Pendente |
| 14 | Cortador não atravessa completamente | Corte incompleto ou ilhas de geometria | Garantir que o cortador seja longo o suficiente em ambas as direções | Pendente |
| 15 | Cavidade profunda sem drenagem | Resina fica presa e racha a peça depois | Opção de criar furo de drenagem automático | Pendente |
| 16 | Pino fraco ou mal posicionado | Pino quebra ou não alinha as peças | Controle de diâmetro + posicionamento manual + tolerância própria | Pendente |
| 17 | Boolean gera topologia ruim (n-gons) | Problemas na impressão e na visualização | Limpeza básica na região do corte após o Boolean | Pendente |
| 18 | Solver do Boolean instável | Resultado diferente entre Fast e Exact | Usar Exact com fallback para Fast + aviso | Pendente |

---

## Observações

- Prioridade alta: IDs 01, 02, 03, 05, 06, 07, 12
- Esses são os que mais quebram o fluxo do usuário na prática.
- Atualizar este arquivo sempre que um problema for resolvido ou novo for descoberto.
