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
| 19 | Usuário seleciona os objetos na ordem errada | Troca macho e fêmea → tolerância invertida e peça não encaixa | Forçar escolha clara (botões ou cores) de qual é o Macho e qual é a Fêmea | Pendente |
| 20 | Usuário está em Edit Mode | Add-on não encontra os objetos corretamente ou falha | Detectar modo e avisar / forçar Object Mode | Pendente |
| 21 | Selecionou só 1 objeto ou mais de 2 | Add-on quebra ou corta o objeto errado | Validar rigorosamente: exatamente 2 objetos mesh selecionados | Pendente |
| 22 | Objeto selecionado não é Mesh | Erro ou crash ao tentar Boolean em Curve/Empty/etc | Verificar tipo do objeto e recusar se não for Mesh | Pendente |
| 23 | Usuário não entende o valor da tolerância | Coloca 2.0 pensando que é pouco, ou 0.02 e fica apertado demais | Mostrar exemplos claros na interface ("0.15~0.25mm recomendado para resina") | Pendente |
| 24 | Aplica o add-on várias vezes sem querer | Geometria fica destruída e cheia de cortes extras | Desabilitar o botão após uso + exigir confirmação forte | Pendente |
| 25 | Não salva o arquivo antes de rodar | Perde horas de trabalho se der ruim | Aviso obrigatório: "Salve o arquivo antes de continuar" | Pendente |
| 26 | Coloca o pino em área muito fina | Pino ou a parede ao redor quebra na impressão ou montagem | Verificar espessura local antes de criar o pino e avisar | Pendente |
| 27 | Espera resultado perfeito na primeira vez | Fica frustrado e acha que o add-on é ruim | Deixar bem claro no README e na interface que **teste de impressão é obrigatório** | Pendente |
| 28 | Corta em cima de detalhes importantes | Destrói rosto, costura, logo ou detalhe da roupa | Preview do corte + aviso visual da região afetada | Pendente |
| 29 | Usa profundidade de inserção absurda | Ombro some dentro da blusa ou quase não entra | Limitar valores mínimos e máximos + preview em tempo real | Pendente |
| 30 | Esquece de aplicar o resultado e exporta | Exporta a peça ainda com modificadores ou geometria antiga | Avisar no final e oferecer botão de "Preparar para exportação" | Pendente |
| 31 | Trabalha com objetos em coleções ocultas | Add-on não enxerga ou corta o objeto errado | Verificar visibilidade e avisar se algum objeto estiver hidden | Pendente |
| 32 | Acha que o add-on substitui teste real de impressão | Imprime a peça final direto e se frustra com o encaixe | Mensagem clara: "Sempre imprima um teste da região do encaixe primeiro" | Pendente |
| 33 | Objeto tem Scale negativo | Boolean e normals ficam completamente invertidos | Detectar scale negativo e avisar / corrigir | Pendente |
| 34 | Objeto está muito longe da origem do mundo | Problemas de precisão de ponto flutuante no Boolean | Avisar se a distância da origem for muito grande | Pendente |
| 35 | Tem Subdivision Surface ou Multires ativo | Boolean demora eternamente ou trava | Detectar e avisar fortemente para aplicar ou desativar | Pendente |
| 36 | Tem Shape Keys no objeto | Boolean pode corromper ou ignorar as shape keys | Detectar shape keys e avisar o usuário | Pendente |
| 37 | Tem Geometry Nodes complexo | Resultado imprevisível ou erro | Detectar Geometry Nodes e exigir que seja aplicado antes | Pendente |
| 38 | Usuário tenta cortar o personagem inteiro de uma vez | Resultado caótico e difícil de controlar | Orientar a isolar apenas as duas partes que vão se encaixar | Pendente |
| 39 | Muda a tolerância depois de já ter cortado | Fica com geometria inconsistente e não sabe o que fazer | Deixar claro que tolerância só vale antes do corte + opção de desfazer | Pendente |
| 40 | Quer que a junta fique 100% invisível | Frustração garantida (tolerância sempre cria uma linha) | Explicar que sempre vai existir uma linha de emenda | Pendente |
| 41 | Imprime as duas peças com orientações muito diferentes | Uma peça fica dimensionalmente diferente da outra | Avisar sobre manter orientação semelhante na impressão | Pendente |
| 42 | Lixa agressivamente uma das faces de encaixe | Destrói a tolerância que o add-on criou | Recomendar lixar o mínimo possível na superfície de contato | Pendente |
| 43 | Usa resinas diferentes nas duas peças | Shrinkage diferente → encaixe muda | Avisar para usar a mesma resina e mesmas configurações | Pendente |
| 44 | Espera que o pino seja estrutural (aguente pose) | Pino quebra quando tenta articular a peça | Deixar claro que o pino é só de alinhamento/montagem, não estrutural | Pendente |
| 45 | Esquece qual lado é macho e qual é fêmea dias depois | Tenta montar errado e força a peça | Nomear automaticamente os objetos (ex: Blusa_Femea / Ombro_Macho) | Pendente |
| 46 | Tem Custom Split Normals ou Auto Smooth forte | Sombreamento fica estranho após o corte | Avisar e oferecer limpeza de custom normals na região | Pendente |
| 47 | Trabalha com dados vinculados (linked/instanced) | Não consegue modificar ou gera erro | Detectar e avisar para fazer Make Single User | Pendente |
| 48 | Acha que 0.2mm de tolerância é o mesmo para todas as resinas | Encaixe fica apertado ou frouxo dependendo da resina | Deixar presets por tipo de resina (e deixar claro que ainda precisa testar) | Pendente |

---

## Observações Finais (Modo Pessimista Real)

O usuário leigo vai:

- Selecionar os objetos na ordem errada
- Colocar valor de tolerância absurdo
- Rodar o add-on sem salvar o arquivo
- Esperar resultado perfeito de primeira
- Culpar o add-on quando o problema for falta de teste de impressão
- Tentar cortar o personagem inteiro de uma vez
- Lixar demais e destruir a tolerância
- Usar resinas diferentes e não entender por que não encaixou
- Achar que o pino serve para articular a figura
- Esquecer qual lado é macho e qual é fêmea

**Conclusão realista:**  
Mesmo com todas as proteções possíveis, o add-on **não consegue impedir** o usuário de cometer erros de julgamento. O máximo que ele pode fazer é avisar, dificultar o erro e educar.

Prioridade máxima de proteção:  
**01, 06, 07, 12, 19, 20, 21, 23, 25, 27, 32, 33, 35, 45**

Atualizar sempre que descobrir mais um jeito do usuário se auto-sabotar.
