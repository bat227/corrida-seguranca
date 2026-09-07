import streamlit as st
import random
import time

# Configuração da página web e tema forçado escuro
st.set_page_config(page_title="Corrida pela Segurança", page_icon="🛡️", layout="centered")

# Injeção de CSS para forçar o fundo inteiramente preto e estilo hacker Matrix
st.markdown("""
    <style>
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #003300 !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
    }
    .stButton>button:hover {
        background-color: #00ff00 !important;
        color: #000000 !important;
    }
    code {
        background-color: #111111 !important;
        color: #00ff00 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #00ff00 !important;
    }
    div[data-testid="stNotification"] {
        background-color: #051a05 !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
    }
    /* Estilização especial para o botão de abortar missão no rodapé */
    div.element-container:has(button:contains("ABORT_MISSION")) button {
        background-color: #220000 !important;
        color: #ff3333 !important;
        border: 1px solid #ff3333 !important;
    }
    div.element-container:has(button:contains("ABORT_MISSION")) button:hover {
        background-color: #ff3333 !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# BANCO DE DADOS EXPANDIDO (MÓDULO FLIPPITY)
# ==========================================
if 'perguntas' not in st.session_state:
    st.session_state.perguntas = [
        {"pergunta": "O tratamento de dados pessoais pode ocorrer para o cumprimento de obrigação legal?", "opcoes": ["Sim, é uma das bases legais válidas da LGPD.", "Não, precisa sempre de consentimento absoluto.", "Apenas se o titular for menor de idade."], "correta": 0},
        {"pergunta": "Se formulários de clientes forem descartados no lixo comum sem fragmentar, ocorre infração?", "opcoes": ["Não, desde que o lixo seja recolhido no mesmo dia.", "Sim, configura descarte inadequado e risco de vazamento.", "Não, pois papéis físicos não entram no escopo digital."], "correta": 1},
        {"pergunta": "Deixar o computador de trabalho desbloqueado ao ir almoçar viola qual pilar da Segurança?", "opcoes": ["Disponibilidade.", "Integridade.", "Confidencialidade."], "correta": 2},
        {"pergunta": "O que caracteriza um ataque de 'Phishing'?", "opcoes": ["Um vírus que bloqueia os arquivos do computador exigindo resgate.", "E-mails ou mensagens falsas que imitam instituições reais para roubar dados.", "Um acesso físico não autorizado ao servidor da empresa."], "correta": 1},
        {"pergunta": "Qual das seguintes opções é considerada um 'Dado Pessoal Sensível' segundo a LGPD?", "opcoes": ["Número de telefone celular.", "Origem racial/étnica, convicção religiosa ou dados de saúde.", "Endereço comercial da empresa."], "correta": 1},
        {"pergunta": "Qual é a função principal da ANPD (Autoridade Nacional de Proteção de Dados)?", "opcoes": ["Criar os códigos de programação dos sistemas do governo.", "Fiscalizar e aplicar sanções a empresas que descumprirem a LGPD.", "Vender softwares de antivírus corporativos."], "correta": 1},
        {"pergunta": "O que significa o pilar da 'Integridade' na Segurança da Informação?", "opcoes": ["Garantir que a informação esteja disponível sempre que necessário.", "Garantir que a informação não seja alterada ou corrompida por pessoas não autorizadas.", "Garantir que apenas pessoas autorizadas vejam a informação."], "correta": 1},
        {"pergunta": "Qual destas práticas ajuda a mitigar o risco de Engenharia Social nas empresas?", "opcoes": ["Instalar apenas um firewall de rede potente.", "Realizar treinamentos periódicos de conscientização com os funcionários.", "Aumentar a velocidade da internet dos servidores."], "correta": 1},
        {"pergunta": "No contexto da LGPD, quem é a figura do 'Controlador'?", "opcoes": ["A pessoa ou empresa a quem competem as decisões sobre o tratamento dos dados.", "O funcionário de TI que digita o código do sistema.", "O cliente dono dos dados pessoais."], "correta": 0},
        {"pergunta": "O que é criptografia de chave pública/privada?", "opcoes": ["Um método para apagar permanentemente os dados do servidor físico.", "Uma técnica de embaralhar dados para que apenas quem tem a chave correta possa ler.", "Uma senha simples que todos os funcionários compartilham."], "correta": 1}
    ]

CASAS_ESPECIAIS = {
    3: {"msg": "⚠️ Alerta de Invasão! Você navegou num site sem verificação de segurança! (Volte 2 casas)", "efeito": -2, "char": "smith"},
    6: {"msg": "🛡️ Conexão Segura! Você chegou aos três pilares da LGPD - pessoas, processos e tecnologia! (Avance 2 casas)", "efeito": 2, "char": "morfeu"},
    9: {"msg": "🚨 Brecha detectada! A ANPD fiscalizou sua empresa e aplicou sanções! (Volte 3 casas)", "efeito": -3, "char": "smith"},
    12: {"msg": "💼 Protocolo correto! Você garantiu fácil acesso aos titulares sobre o tratamento de dados! (Avance 1 casa)", "efeito": 1, "char": "trinity"}
}

CASA_FINAL = 15

# GERENCIAMENTO DE ESTADO
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

# ========================================================
# EXECUÇÃO DO FLUXO DO JOGO
# ========================================================
if not st.session_state.jogando:
    col_char, col_text = st.columns(2)
    with col_char:
        st.code("  😎 MORFEU\n   [=======]\n   | O   O |\n   |   v   |\n   \\ ===== /", language="markdown")
    with col_text:
        st.write("### 🕶️ Morfeu diz:")
        st.info("'Esta é a sua última chance. Depois disso, não há retorno. Escolha a pílula vermelha, registre-se na Matrix da Segurança e veja até onde vai a toca do coelho...'")
    
    st.markdown("""
    ### 🧠 Por que utilizamos a ISO/IEC 12207?
    A **ISO/IEC 12207** é a norma internacional de referência para os **Processos de Ciclo de Vida de Software**. A sua importância no desenvolvimento deste jogo se justifica por:
    
    *   **Qualidade e Estrutura:** Ela divide o projeto em etapas bem definidas (Requisitos, Design, Construção e Testes).
    *   **Mitigação de Riscos:** Através do conceito de *Tailoring* (Adaptação), entregamos um protótipo funcional dentro do prazo.
    *   **Manutenibilidade:** Separa os dados das perguntas da camada visual, permitindo correções rápidas sem quebrar o jogo.
    ---
    """)
    
    nome_input = st.text_input("👤 Digite o seu codinome Hacker para se infiltrar:")
    if st.button("🚀 Tomar a Pílula Vermelha"):
        if nome_input:
            st.session_state.nome = nome_input
            st.session_state.posicao = 0
            st.session_state.pontos = 1000
            st.session_state.tempo_inicio = time.time()
            st.session_state.jogando = True
            st.session_state.log_evento = f"Conexão estabelecida, {nome_input}. Entrando na Matrix corporativa..."
            st.session_state.quizzes_respondidos = 0
            st.session_state.quizzes_acertados = 0
            st.session_state.game_over = False
            st.rerun()
        else:
            st.warning("É preciso digitar um codinome para descriptografar o acesso.")

else:
    if st.session_state.game_over or st.session_state.pontos <= 0:
        col_char, col_text = st.columns(2)
        with col_char:
            st.code("  🕴️ AGENTE SMITH\n    _______\n   / _   _ \\\n  | (O) (O) |\n  |    |    |\n   \\  ___  /\n    \\_____/", language="markdown")
        with col_text:
            st.error("🚨 CONEXÃO INTERROMPIDA PELOS AGENTES!")
            st.write("### 🕴️ Agente Smith diz:")
            st.warning(f"'Ouve isso, Sr. {st.session_state.nome}? É o som do inevitável. Suas brechas na LGPD destruíram o Mainframe. É o fim de sua linha corporativa.'")
        if st.button("🔄 Hackear Mainframe Novamente"):
            st.session_state.posicao = 0
            st.session_state.pontos = 1000
            st.session_state.jogando = False
            st.rerun()

    elif st.session_state.posicao >= CASA_FINAL:
        tempo_total = round(time.time() - st.session_state.tempo_inicio, 2)
        st.balloons()
        st.success(f"🏆 SISTEMA TOTALMENTE DOMINADO! Você cruzou o Mainframe em {tempo_total}s com {st.session_state.pontos} pontos!")
        
        col_char, col_text = st.columns(2)
        with col_char:
            st.code("  😎 NEO (VOCÊ)\n    _______\n   /       \\\n  |  O   O  |\n  |    ^    |\n   \\  ===  /\n    \\_____/", language="markdown")
        with col_text:
            st.write("### ⚡ Oráculo emite o Relatório:")
            if st.session_state.quizzes_respondidos > 0:
                if st.session_state.quizzes_acertados == st.session_state.quizzes_respondidos:
                    st.subheader("🌟 NOTA: 10/10 - VOCÊ É O ESCOLHIDO!")
                    st.markdown("Incrível! Você enxergou as linhas de código da LGPD e salvou a empresa sem cometer erros de privacidade.")
                else:
                    st.subheader(f"📊 NOTA: {st.session_state.quizzes_acertados} de {st.session_state.quizzes_respondidos} patches aplicados.")
