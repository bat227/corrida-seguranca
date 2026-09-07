import streamlit as st
import random
import time

# Configuração da página web com tema hacker Matrix otimizado
st.set_page_config(page_title="Corrida pela Segurança", page_icon="🛡️", layout="centered")

# CSS Corrigido para evitar conflitos visuais e sumiço de textos
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c !important; }
    h1, h2, h3, h4, h5, h6, p, span, label { color: #ffffff !important; }
    .stButton>button { 
        background-color: #002200 !important; 
        color: #00ff00 !important; 
        border: 1px solid #00ff00 !important;
        font-weight: bold;
    }
    .stButton>button:hover { 
        background-color: #00ff00 !important; 
        color: #000000 !important; 
    }
    code { background-color: #1a1a1a !important; color: #00ff00 !important; }
    div[data-testid="stMetricValue"] { color: #00ff00 !important; }
    </style>
""", unsafe_allow_html=True)

# Banco de dados ampliado com 25 perguntas sobre Segurança e LGPD
LISTA_PERGUNTAS = [
    {"pergunta": "O tratamento de dados pessoais pode ocorrer para o cumprimento de obrigação legal?", "opcoes": ["Sim, é uma das bases legais válidas da LGPD.", "Não, precisa sempre de consentimento absoluto.", "Apenas se o titular for menor de idade."], "correta": 0},
    {"pergunta": "Se formulários de clientes forem descartados no lixo comum sem fragmentar, ocorre infração?", "opcoes": ["Não, desde que o lixo seja recolhido no mesmo dia.", "Sim, configura descarte inadequado e risco de vazamento.", "Não, pois papéis físicos não entram no escopo digital."], "correta": 1},
    {"pergunta": "Deixar o computador de trabalho desbloqueado ao ir almoçar viola qual pilar da Segurança?", "opcoes": ["Disponibilidade.", "Integridade.", "Confidencialidade."], "correta": 2},
    {"pergunta": "O que caracteriza um ataque de 'Phishing'?", "opcoes": ["Um vírus que bloqueia os arquivos do computador exigindo resgate.", "E-mails ou mensagens falsas que imitam instituições reais para roubar dados.", "Um acesso físico não autorizado ao servidor da empresa."], "correta": 1},
    {"pergunta": "Qual das seguintes opções é considerada um 'Dado Pessoal Sensível' segundo a LGPD?", "opcoes": ["Número de telefone celular.", "Origem racial/étnica, convicção religiosa ou dados de saúde.", "Endereço comercial da empresa."], "correta": 1},
    {"pergunta": "Qual é a função principal da ANPD?", "opcoes": ["Criar códigos de programação.", "Fiscalizar e aplicar sanções a quem descumprir a LGPD.", "Vender antivírus."], "correta": 1},
    {"pergunta": "O que significa o pilar da 'Integridade' na Segurança?", "opcoes": ["Garantir disponibilidade contínua.", "Garantir que a informação não seja alterada sem autorização.", "Garantir sigilo absoluto."], "correta": 1},
    {"pergunta": "Qual destas práticas ajuda a mitigar Engenharia Social?", "opcoes": ["Instalar apenas um firewall potente.", "Realizar treinamentos periódicos com os funcionários.", "Aumentar a velocidade dos servidores."], "correta": 1},
    {"pergunta": "No contexto da LGPD, quem é o 'Controlador'?", "opcoes": ["Quem toma as decisões sobre o tratamento dos dados.", "O profissional de TI.", "O cliente."], "correta": 0},
    {"pergunta": "O que é criptografia?", "opcoes": ["Apagar dados do servidor físico.", "Técnica de embaralhar dados para proteção.", "Uma senha simples compartilhada."], "correta": 1},
    {"pergunta": "O que caracteriza um ataque de Ransomware?", "opcoes": ["Espionar a câmera do usuário sem que ele saiba.", "Sequestrar arquivos criptografando-os e exigir um resgate financeiro.", "Enviar anúncios repetitivos na tela do navegador."], "correta": 1},
    {"pergunta": "Qual é o principal risco de usar redes Wi-Fi públicas sem VPN para trabalhar?", "opcoes": ["A bateria do notebook descarregar mais rápido.", "Intercepção de tráfego e roubo de dados por criminosos na mesma rede.", "O sinal cair devido ao excesso de usuários."], "correta": 1},
    {"pergunta": "O que é a autenticação de dois fatores (2FA)?", "opcoes": ["Uma regra de criar duas senhas textuais parecidas.", "Uma camada extra de segurança que exige um código além da senha.", "Digitar a senha duas vezes seguidas para confirmar."], "correta": 1},
    {"pergunta": "Compartilhar senhas de sistemas com colegas de equipe é aceitável se for urgente?", "opcoes": ["Sim, o trabalho em equipe justifica a agilidade.", "Não, as credenciais são de uso pessoal e intransferível.", "Sim, contanto que seja enviado por WhatsApp."], "correta": 1},
    {"pergunta": "Quem é o Encarregado pelo Tratamento de Dados Pessoais (DPO) na LGPD?", "opcoes": ["O dono da empresa.", "O canal de comunicação entre a empresa, os titulares e a ANPD.", "O auditor fiscal do governo."], "correta": 1},
    {"pergunta": "Qual pilar da segurança garante que os sistemas estejam acessíveis quando necessários?", "opcoes": ["Disponibilidade.", "Confidencialidade.", "Autenticidade."], "correta": 0},
    {"pergunta": "Qual é o prazo geral estipulado para comunicar incidentes de segurança relevantes à ANPD?", "opcoes": ["Prazo razoável, geralmente interpretado como até 2 dias úteis.", "Imediatamente em até 2 horas do ocorrido.", "30 dias corridos."], "correta": 0},
    {"pergunta": "O que representa o princípio do 'Privacy by Design'?", "opcoes": ["Criar telas bonitas para políticas de privacidade.", "Pensar na proteção de dados desde a concepção de um projeto ou sistema.", "Contratar designers para auditar o banco de dados."], "correta": 1},
    {"pergunta": "Qual a melhor postura ao receber um e-mail com anexo suspeito de um remetente desconhecido?", "opcoes": ["Abrir para verificar se é um vírus real.", "Ignorar ou reportar à equipe de segurança sem abrir o anexo.", "Encaminhar para toda a lista de contatos."], "correta": 1},
    {"pergunta": "Anexar uma planilha com CPFs de clientes por engano em um e-mail externo viola a LGPD?", "opcoes": ["Não, se o destinatário prometer apagar o e-mail.", "Sim, configura um incidente de segurança e vazamento de dados.", "Não, pois o CPF é considerado um dado público."], "correta": 1},
    {"pergunta": "Qual é a base legal correta para coletar dados médicos de um colaborador em um exame admissional?", "opcoes": ["Legítimo interesse do patrão.", "Cumprimento de obrigação legal ou regulatória pelo controlador.", "Consentimento livre e revogável."], "correta": 1},
    {"pergunta": "O que descreve a Engenharia Social?", "opcoes": ["Manipulação psicológica de pessoas para que executem ações ou revelem segredos.", "Construção de infraestruturas físicas de TI.", "Programação de algoritmos de redes sociais."], "correta": 0},
    {"pergunta": "Uma senha considerada forte deve conter quais características?", "opcoes": ["Apenas letras maiúsculas organizadas em ordem alfabética.", "Combinação de letras maiúsculas, minúsculas, números e caracteres especiais.", "O nome do usuário seguido do ano de nascimento."], "correta": 1},
    {"pergunta": "Qual o papel do 'Operador' de dados segundo as regras da LGPD?", "opcoes": ["Realizar o tratamento de dados pessoais em nome e seguindo ordens do Controlador.", "Definir as finalidades da coleta dos dados.", "Fiscalizar as ações da ANPD."], "correta": 0},
    {"pergunta": "Se um cliente solicitar a exclusão de seus dados da base da empresa, o que deve ser feito?", "opcoes": ["Apagar na hora, exceto se houver obrigação legal ou regulatória para mantê-los.", "Recusar a exclusão sob qualquer hipótese.", "Cobrar uma taxa de remoção de dados do cliente."], "correta": 0}
]

CASAS_ESPECIAIS = {
    3: {"msg": "⚠️ Alerta de Invasão! (Volte 2 casas)", "efeito": -2, "char": "smith"},
    6: {"msg": "🛡️ Conexão Segura! (Avance 2 casas)", "efeito": 2, "char": "morfeu"},
    9: {"msg": "🚨 Brecha detectada pela ANPD! (Volte 3 casas)", "efeito": -3, "char": "smith"},
    12: {"msg": "💼 Protocolo correto de dados! (Avance 1 casa)", "efeito": 1, "char": "trinity"}
}

CASA_FINAL = 15

# Inicialização segura do Estado da Sessão
if 'posicao' not in st.session_state:
    st.session_state.posicao = 0
    st.session_state.pontos = 1000
    st.session_state.nome = ""
    st.session_state.jogando = False
    st.session_state.tempo_inicio = 0.0
    st.session_state.mostrar_quiz = False
    st.session_state.quiz_atual = None
    st.session_state.log_evento = ""
    st.session_state.quizzes_respondidos = 0
    st.session_state.quizzes_acertados = 0
    st.session_state.game_over = False
    st.session_state.ultimo_personagem = "morfeu"

st.title("🟢 Corrida pela Segurança Digital")

# Estrutura principal com blocos perfeitamente alinhados e identados
if not st.session_state.jogando:
    col_char, col_text = st.columns(2)
    with col_char:
        st.code("  😎 MORFEU\n   [=======]\n   | O   O |\n   |   v   |\n   \\ ===== /", language="markdown")
    with col_text:
        st.write("### 🕶️ Morfeu diz:")
        st.write("*'Esta é a sua última chance. Escolha a pílula vermelha, registre-se na Matrix da Segurança e veja até onde vai a toca do coelho...'*")
    
    with st.expander("🧠 Documentação de Engenharia de Software (ISO 12207)"):
        st.markdown("* **Qualidade:** Divisão estruturada. \n* **Mitigação:** Uso de *Tailoring*.\n* **Manutenibilidade:** Dados isolados.")
    
    nome_input = st.text_input("👤 Codinome Hacker:")
    if st.button("🚀 Tomar a Pílula Vermelha"):
        if nome_input:
            st.session_state.nome = nome_input
            st.session_state.posicao = 0
            st.session_state.pontos = 1000
            st.session_state.quizzes_respondidos = 0
            st.session_state.quizzes_acertados = 0
            st.session_state.tempo_inicio = time.time()
            st.session_state.jogando = True
            st.session_state.log_evento = "Acessando mainframe..."
            st.rerun()

elif st.session_state.pontos <= 0:
    st.error(f"🚨 CONEXÃO INTERROMPIDA! Agente Smith baniu o Sr. {st.session_state.nome}!")
    if st.button("🔄 Hackear Novamente"):
