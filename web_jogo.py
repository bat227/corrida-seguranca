import streamlit as st
import random
import time

# Configuração da página web com tema hacker Matrix otimizado
st.set_page_config(page_title="Corrida pela Segurança", page_icon="🛡️", layout="centered")

# CSS Corrigido para evitar conflitos visuais e sumiço de textos
st.markdown("""
    <style>
    .stApp { background-color: #0c0c0c !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, div { color: #ffffff !important; }
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
    
    /* Configurações extras para garantir contraste no modo Matrix */
    .stRadio label { color: #ffffff !important; font-size: 16px; }
    div[data-testid="stMarkdownContainer"] p { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# Banco de dados com perguntas sobre Segurança e LGPD
LISTA_PERGUNTAS = [
    {"pergunta": "O tratamento de dados pessoais pode ocorrer para o cumprimento de obrigação legal?", "opcoes": ["Sim, é uma das bases legais válidas da LGPD.", "Não, precisa sempre de consentimento absoluto.", "Apenas se o titular for menor de idade."], "correta": 0},
    {"pergunta": "Se formulários de clientes forem descartados no lixo comum sem fragmentar, ocorre infração?", "opcoes": ["Não, desde que o lixo seja recolhido no mesmo dia.", "Sim, configura descarte inadequado e risco de vazamento.", "Não, pois papéis físicos não entram no escopo digital."], "correta": 1},
    {"pergunta": "Deixar o computador de trabalho desbloqueado ao ir almoçar viola qual pilar da Segurança?", "opcoes": ["Disponibilidade.", "Integridade.", "Confidencialidade."], "correta": 2},
    {"pergunta": "O que caracteriza um ataque de 'Phishing'?", "opcoes": ["Um vírus que bloqueia os arquivos do computador exigindo resgate.", "E-mails ou mensagens falsas que imitam instituições reais para roubar dados.", "Um acesso físico não autorizado ao servidor da empresa."], "correta": 1},
    {"pergunta": "Qual das seguintes opções é considerada um 'Dado Pessoal Sensível' segundo a LGPD?", "opcoes": ["Número de telefone celular.", "Origem racial/étnica, convicção religiosa ou dados de saúde.", "Endereço comercial da empresa."], "correta": 1}
]

CASAS_ESPECIAIS = {
    3: {"msg": "⚠️ Alerta de Invasão! (Volte 2 casas)", "efeito": -2},
    6: {"msg": "🛡️ Conexão Segura! (Avance 2 casas)", "efeito": 2},
    9: {"msg": "🚨 Brecha detectada pela ANPD! (Volte 3 casas)", "efeito": -3},
    12: {"msg": "💼 Protocolo correto de dados! (Avance 1 casa)", "efeito": 1}
}

CASA_FINAL = 15

# Inicialização das variáveis internas de estado do Streamlit
if 'posicao' not in st.session_state:
    st.session_state.posicao = 0
if 'pontos' not in st.session_state:
    st.session_state.pontos = 1000
if 'nome' not in st.session_state:
    st.session_state.nome = "Anônimo"
if 'pergunta_atual' not in st.session_state:
    st.session_state.pergunta_atual = random.choice(LISTA_PERGUNTAS)

# 1. Cabeçalho Principal
st.title("🛡️ Corrida pela Segurança")

# 2. Botão de Reinicialização (Fomatado na ordem da sua imagem)
if st.button("🔄 Hackear Novamente"):
    st.session_state.posicao = 0
    st.session_state.pontos = 1000
    st.session_state.pergunta_atual = random.choice(LISTA_PERGUNTAS)
    st.rerun()

# 3. Informações de Status do Jogador
st.write(f"**Jogador:** {st.session_state.nome}")
st.write(f"**Posição Atual:** Casa {st.session_state.posicao} / {CASA_FINAL}")

# 4. Bloco de Pontuação Hacking
st.metric(label="Pontuação Hacking", value=st.session_state.pontos)

# Divisor visual para separar o cabeçalho estático das perguntas dinâmicas
st.markdown("---")

# 5. Fluxo de Execução do Quiz (Abaixo da pontuação)
if st.session_state.posicao >= CASA_FINAL:
    st.balloons()
    st.success("🏆 Parabéns! Você superou todas as vulnerabilidades e invadiu o sistema com segurança!")
else:
    p = st.session_state.pergunta_atual
    
    st.subheader("💻 Desafio de Segurança Detectado:")
    st.markdown(f"**{p['pergunta']}**")
    
    # Campo de escolha múltipla
    resposta_selecionada = st.radio("Selecione sua ação:", p["opcoes"], key="quiz_radio_options")
    
    if st.button("Confirmar Resposta 🔐"):
        indice = p["opcoes"].index(resposta_selecionada)
        
        if indice == p["correta"]:
            st.success("✅ Acesso Permitido! Resposta correta.")
            passos = random.randint(1, 3)
            st.session_state.posicao += passos
            st.session_state.pontos += 100
            
            # Validação de casas especiais do tabuleiro
            if st.session_state.posicao in CASAS_ESPECIAIS:
                evento = CASAS_ESPECIAIS[st.session_state.posicao]
                st.warning(evento["msg"])
                st.session_state.posicao += evento["efeito"]
                
            if st.session_state.posicao < 0:
                st.session_state.posicao = 0
        else:
            st.error("❌ Resposta Incorreta! Integridade do sistema comprometida.")
            st.session_state.pontos -= 150
            if st.session_state.pontos < 0:
                st.session_state.pontos = 0
        
        # Sorteia uma nova pergunta e atualiza a interface
        st.session_state.pergunta_atual = random.choice(LISTA_PERGUNTAS)
        time.sleep(1.5)
        st.rerun()
