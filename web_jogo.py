import streamlit as st
import random

# Configuração da página web com estilo hacker Matrix
st.set_page_config(page_title="ISO 12207: Corrida do Ciclo de Vida", page_icon="💾", layout="centered")

# CSS personalizado para o tema escuro Matrix e botões visíveis
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: #ffffff !important; }
    .stButton>button { 
        background-color: #002200 !important; 
        color: #00ff00 !important; 
        border: 1px solid #00ff00 !important;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover { 
        background-color: #00ff00 !important; 
        color: #000000 !important; 
    }
    code { background-color: #1a1a1a !important; color: #00ff00 !important; }
    div[data-testid="stMetricValue"] { color: #00ff00 !important; }
    .stRadio label { color: #ffffff !important; font-size: 16px; }
    div[data-testid="stMarkdownContainer"] p { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# Banco de dados com 50 perguntas exclusivas sobre a ISO/IEC 12207
BANCO_PERGUNTAS = [
    {"pergunta": "Por que a ISO 12207 foi inventada?", "opcoes": ["Para unificar as linguagens de programação.", "Para acabar com o caos e padronizar os processos do ciclo de vida do software.", "Para tabelar o preço de venda de sistemas."], "correta": 1},
    {"pergunta": "Para que serve a ISO 12207?", "opcoes": ["Como um guia que define o que fazer desde a concepção até o descarte do software.", "Para criar códigos de inteligência artificial de forma automática.", "Para monitorar o uso de Wi-Fi nas empresas."], "correta": 0},
    {"pergunta": "Qual cuidado (precaução) devemos ter ao adotar a norma?", "opcoes": ["Ela deve ser copiada de forma rígida, sem nenhuma alteração.", "Ela diz 'o que' fazer, mas não 'como'. Deve ser adaptada ao projeto.", "Ela só pode ser aplicada se a empresa usar a linguagem C++."], "correta": 1},
    {"pergunta": "O que caracteriza o erro da burocracia excessiva ao aplicar a norma?", "opcoes": ["Gerar toneladas de relatórios e documentos que não trazem valor real ao produto.", "Diminuir a quantidade de testes de segurança.", "Aumentar demais o salário dos programadores."], "correta": 0},
    {"pergunta": "Os processos de Aquisição e Fornecimento pertencem a qual categoria?", "opcoes": ["Processos Técnicos.", "Processos de Acordo (Contratuais).", "Processos Organizacionais."], "correta": 1},
    {"pergunta": "Qual processo lida com a infraestrutura e o treinamento corporativo de funcionários?", "opcoes": ["Processos Organizacionais.", "Processos de Gerenciamento Técnico.", "Processos de Implementação."], "correta": 0},
    {"pergunta": "Qual a função do processo de Análise de Requisitos?", "opcoes": ["Escrever as linhas de código do sistema.", "Descobrir, detalhar e documentar o que o software precisa fazer.", "Apagar as bases de dados antigas."], "correta": 1},
    {"pergunta": "O processo de Projeto da Arquitetura do Software define:", "opcoes": ["O plano de marketing para o lançamento.", "A estrutura interna, módulos, componentes e interfaces do sistema.", "O valor das licenças comerciais."], "correta": 1},
    {"pergunta": "O que é feito no processo de Implementação?", "opcoes": ["A tradução do design do software em linhas de código executável.", "A entrega do manual impresso para o cliente.", "A alteração de preços do contrato."], "correta": 0},
    {"pergunta": "O que define o processo de Manutenção?", "opcoes": ["O ato de formatar os computadores da empresa.", "Modificações feitas no software após a entrega para corrigir erros ou atualizar funções.", "A desativação permanente do sistema."], "correta": 1},
    {"pergunta": "O que significa o termo 'Tailoring' na ISO 12207?", "opcoes": ["Eliminar a fase de engenharia para entregar o produto mais rápido.", "Adaptar a norma selecionando apenas os processos adequados ao seu projeto.", "Mudar os ícones visuais do sistema."], "correta": 1},
    {"pergunta": "Qual a diferença conceitual entre Verificação e Validação?", "opcoes": ["Verificação checa se o código cumpre a especificação técnica; Validação checa se atende ao usuário.", "São exatamente a mesma atividade técnica.", "Verificação é o teste em nuvem e Validação é o teste local."], "correta": 0},
    {"pergunta": "O Gerenciamento de Configuração serve para:", "opcoes": ["Controlar versões de arquivos (como o Git) e o histórico de modificações.", "Organizar as mesas físicas do escritório de desenvolvimento.", "Mudar o brilho da tela do software."], "correta": 0},
    {"pergunta": "A Gestão de Riscos está inserida em qual grupo da norma?", "opcoes": ["Processos de Acordo.", "Processos de Gerenciamento Técnico.", "Processos Técnicos."], "correta": 1},
    {"pergunta": "Qual processo cuida da desativação definitiva e aposentadoria de um software?", "opcoes": ["Processo de Operação.", "Processo de Descarte (Retirement).", "Processo de Manutenção."], "correta": 1},
    {"pergunta": "A norma ISO 12207 proíbe expressamente o uso de frameworks ágeis como o Scrum?", "opcoes": ["Sim, ela obriga o uso do desenvolvimento Cascata.", "Não, ela é neutra e pode ser integrada tanto a métodos ágeis quanto tradicionais.", "Sim, ela não permite alterações diárias no escopo."], "correta": 1},
    {"pergunta": "O processo de Operação cuida de qual etapa?", "opcoes": ["Do uso cotidiano do software em produção pelos usuários finais e suporte técnico.", "Do desenho inicial do banco de dados.", "Da assinatura das promessas de pagamento."], "correta": 0},
    {"pergunta": "Qual problema a falta de padronização gerava na engenharia antes de 1995?", "opcoes": ["Códigos sem fontes modernas.", "Prazos estourados, custos descontrolados e falhas graves de comunicação.", "A quebra física de mouses e teclados."], "correta": 1},
    {"pergunta": "Seguir a norma garante que um sistema saia 100% sem erros de código?", "opcoes": ["Sim, pois ela elimina falhas de lógica automaticamente.", "Não, nenhuma norma apaga 100% dos bugs, mas ela eleva drasticamente a qualidade.", "Sim, porque ela impede a digitação de códigos errados."], "correta": 1},
    {"pergunta": "Quem se beneficia com a linguagem comum estabelecida pela norma?", "opcoes": ["Apenas o time de programação júnior.", "Todos os envolvidos (compradores, fornecedores, desenvolvedores e gerentes).", "Apenas o sector financeiro da empresa."], "correta": 1},
    {"pergunta": "Qual processo técnico avalia se os objetivos de negócio foram atingidos no ambiente real?", "opcoes": ["Processo de Validação.", "Processo de Codificação.", "Processo de Aquisição."], "correta": 0},
    {"pergunta": "O processo de Garantia da Qualidade do Software serve para:", "opcoes": ["Garantir de forma independente que os processos e produtos estão seguindo os planos estipulados.", "Aumentar a velocidade dos downloads.", "Escrever relatórios de vendas para os diretores."], "correta": 0},
    {"pergunta": "O que avalia o processo de Auditoria?", "opcoes": ["A conformidade do produto em relação a contratos e requisitos técnicos definidos.", "O horário de entrada e saída dos funcionários.", "O layout do site do cliente."], "correta": 0},
    {"pergunta": "Qual processo foca no monitoramento do progresso em relação aos planos técnicos e prazos?", "opcoes": ["Processo de Avaliação e Controle Técnico.", "Processo de Descarte.", "Processo de Suprimento."], "correta": 0},
    {"pergunta": "O Gerenciamento de Informação da norma assegura:", "opcoes": ["A criação de anúncios na internet.", "Que dados importantes do projeto fiquem disponíveis e protegidos para quem precisa.", "O apagamento de e-mails antigos."], "correta": 1},
    {"pergunta": "O processo de Definição de Modelos de Ciclo de Vida pertence a qual categoria?", "opcoes": ["Processos Organizacionais.", "Processos Técnicos.", "Processos Contratuais."], "correta": 0},
    {"pergunta": "A melhoria contínua dos processos da empresa é escopo de qual processo?", "opcoes": ["Processo de Gerenciamento de Modelo de Processo Organizacional.", "Processo de Implementação.", "Processo de Operação."], "correta": 0},
    {"pergunta": "O gerenciamento de recursos humanos da engenharia é tratado em qual item?", "opcoes": ["Processo de Gerenciamento de Recursos Humanos da Organização.", "Processo de Design de Interfaces.", "Processo de Testes Automatizados."], "correta": 0},
    {"pergunta": "O processo de Integração de Software tem como meta:", "opcoes": ["Combinar os módulos e componentes de código já testados para formar o sistema completo.", "Separar o código em arquivos individuais sem conexão.", "Mudar a linguagem de programação no meio do projeto."], "correta": 0},
    {"pergunta": "O que define a fase de Concepção na engenharia de sistemas?", "opcoes": ["A desativação do sistema.", "O estudo de viabilidade e nascimento da ideia do produto.", "A correção de bugs críticos."], "correta": 1},
    {"pergunta": "A norma ISO 12207 é mantida por quais entidades internacionais?", "opcoes": ["ISO e IEC.", "W3C e Google.", "Microsoft e Apple."], "correta": 0},
    {"pergunta": "Qual processo lida diretamente com reclamações e chamados de suporte dos usuários?", "opcoes": ["Processo de Operação.", "Processo de Design.", "Processo de Aquisição."], "correta": 0},
    {"pergunta": "Em projetos ágeis, os processos da ISO 12207 ocorrem de qual forma?", "opcoes": ["Eles não ocorrem.", "De maneira cíclica, incremental e adaptada em iterações curtas.", "Apenas no último dia antes da entrega final."], "correta": 1},
    {"pergunta": "Qual documento formal inicia as atividades do Processo de Aquisição?", "opcoes": ["Uma solicitação de proposta (RFP) ou especificação de necessidades.", "O código-fonte em Python.", "O recibo de descarte do sistema anterior."], "correta": 0},
