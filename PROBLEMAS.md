# Problemas Conhecidos e Soluções

Documento de rastreamento de riscos do add-on.

**Legenda de Status:**
- `Pendente`
- `Decidido`
- `Em andamento`
- `Corrigido`
- `Não será feito`

---

## Tabela de Problemas

| ID | Problema | O que pode causar | Solução Final / Decisão | Status |
|----|----------|-------------------|--------------------------|--------|
| 01 | Scale e Rotation não aplicados | Tolerância e profundidade ficam completamente erradas | Botão no topo do add-on para aplicar Scale + Rotation. Ter caixa de configuração (engrenagem) para definir tamanho/unidades | Decidido |
| 02 | Quantidade muito alta de polígonos | Boolean trava o Blender ou demora minutos | Limite máximo de 500k polígonos por objeto. Decimate feito junto com o botão de preparação. Valor máximo configurável na engrenagem | Decidido |
| 03 | Faces invertidas (normals erradas) | Boolean não corta, apaga tudo ou deixa só uma linha | Fazer Recalculate Outside automaticamente no botão de preparação | Decidido |
| 04 | Malha não manifold | Boolean falha ou gera geometria quebrada | Tentar Make Manifold no botão de preparação. Mostrar barra de progresso com etapas (ex: 1/5, 2/5...) | Decidido |
| 05 | Modificadores não aplicados | Resultado do Boolean fica inconsistente | Aplicar todos os modificadores **antes** do Decimate. Ordem definida no botão de preparação | Decidido |
| 06 | Tolerância no sentido errado | Macho fica maior que o furo (não encaixa) | Sempre expandir o cortador apenas no objeto **fêmea**. Usuário só indica qual é macho e qual é fêmea | Decidido |
| 07 | Unidades da cena erradas (metros vs mm) | Tolerância de 0.2 vira 200mm | Detectar unidade da cena e avisar / forçar trabalho em milímetros | Decidido |
| 08 | Objetos já se interpenetrando | Boolean imprevisível e geometria podre | Avisar o usuário **e perguntar** se quer continuar mesmo assim | Decidido |
| 09 | Parede fina demais após o corte | Peça quebra fácil ou não imprime direito | Não será resolvido automaticamente pelo software. Depende da experiência do usuário | Não será feito |
| 10 | Direção de inserção errada | Ombro entra para fora em vez de dentro | Preview visual claro da direção de inserção + confirmação do usuário | Decidido |
| 11 | Falta de Draft Angle | Peça trava na hora de montar | Ter opção de Draft Angle (1°~3°) configurável na caixa de engrenagem | Decidido |
| 12 | Sem backup dos originais | Usuário perde o trabalho se der errado | Duplicar e esconder os objetos originais automaticamente antes de qualquer corte | Decidido |
| 13 | Destruição de UVs / Vertex Groups / Materials | Modelo texturizado ou com weight paint fica estragado | Baixa prioridade (modelos serão sem textura). No máximo aviso leve | Decidido |
| 14 | Cortador não atravessa completamente | Corte incompleto ou ilhas de geometria | Garantir que o cortador seja longo o suficiente nas duas direções | Decidido |
| 15 | Cavidade profunda sem drenagem | Resina fica presa e racha a peça | Resolver no fatiador de resina. Add-on não precisa criar furo de drenagem | Não será feito |
| 16 | Pino fraco ou mal posicionado + ímãs | Pino quebra ou não alinha as peças | Sistema de pinos com opção para ímã. Tolerância separada para o furo do ímã. Posicionamento manual | Decidido |
| 17 | Boolean gera topologia ruim (n-gons) | Problemas na impressão e visualização | Depois do Boolean, **perguntar** se o usuário quer fazer a limpeza da região do corte | Decidido |
| 18 | Solver do Boolean instável | Resultado diferente entre Fast e Exact | Tentar primeiro Exact. Se falhar, usar Fast como fallback + avisar qual foi usado | Decidido |
| 19 | Usuário seleciona os objetos na ordem errada | Troca macho e fêmea → tolerância invertida | Ainda em discussão | Pendente |
| 20 | Usuário está em Edit Mode | Add-on não encontra os objetos corretamente | Pendente | Pendente |
| 21 | Selecionou só 1 objeto ou mais de 2 | Add-on quebra ou corta o objeto errado | Pendente | Pendente |
| 22 | Objeto selecionado não é Mesh | Erro ou crash | Pendente | Pendente |
| 23 | Usuário não entende o valor da tolerância | Coloca valor absurdo | Pendente | Pendente |
| 24 | Aplica o add-on várias vezes sem querer | Geometria fica destruída | Pendente | Pendente |
| 25 | Não salva o arquivo antes de rodar | Perde horas de trabalho | Pendente | Pendente |
| 26 | Coloca o pino em área muito fina | Pino ou parede quebra | Pendente | Pendente |
| 27 | Espera resultado perfeito na primeira vez | Frustração | Pendente | Pendente |
| 28 | Corta em cima de detalhes importantes | Destrói detalhes da peça | Pendente | Pendente |
| 29 | Usa profundidade de inserção absurda | Ombro some ou quase não entra | Pendente | Pendente |
| 30 | Esquece de aplicar o resultado e exporta | Exporta geometria errada | Pendente | Pendente |
| 31 | Trabalha com objetos em coleções ocultas | Corta objeto errado | Pendente | Pendente |
| 32 | Acha que o add-on substitui teste de impressão | Frustração com o encaixe real | Pendente | Pendente |
| 33+ | Outros problemas técnicos e de uso | — | Ainda não discutidos individualmente | Pendente |

---

## Ordem do Botão de Preparação (Decidida)

1. Aplicar Scale + Rotation
2. Aplicar todos os modificadores
3. Verificar polígonos → Decimate se necessário (máx 500k)
4. Recalculate Outside (normals)
5. Merge by Distance
6. Verificar / tentar Make Manifold

Mostrar barra de progresso com o passo atual (ex: 3/6 - Corrigindo Normals).

---

## Observações

Atualizado com as decisões da conversa até o Problema 18.
