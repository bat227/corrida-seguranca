import streamlit as st
import random
import time

# Configuração da página web com tema hacker Matrix otimizado
st.set_page_config(page_title="Corrida pela Segurança", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown { color: #ffffff !important; }
    .stButton>button { background-color: #003300 !important; color: #00ff00 !important; border: 1px solid #00ff00 !important; }
    .stButton>button:hover { background-color: #00ff00 !important; color: #000000 !important; }
    code { background-color: #111111 !important; color: #00ff00 !important; }
    div[data-testid="stMetricValue"] { color: #00ff00 !important; }
    </style>
""", unsafe_allow_html=True)

# Banco de dados estático e leve de perguntas
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
    {"pergunta": "O que é criptografia?", "opcoes": ["Apagar dados do servidor físico.", "Técnica de embaralhar dados para proteção.", "Uma senha simples compartilhada."], "correta": 1}
]

CASAS_ESPECIAIS = {
    3: {"msg": "⚠️ Alerta de Invasão! (Volte 2 casas)", "efeito": -2, "char": "smith"},
    6: {"msg": "🛡️ Conexão Segura! (Avance 2 casas)", "efeito": 2, "char": "morfeu"},
    9: {"msg": "🚨 Brecha detectada pela ANPD! (Volte 3 casas)", "efeito": -3, "char": "smith"},
    12: {"msg": "💼 Protocolo correto de dados! (Avance 1 casa)", "efeito": 1, "char": "trinity"}
}

CASA_FINAL = 15

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
            st.session_state.tempo_inicio = time.time()
            st.session_state.jogando = True
            st.session_state.log_evento = "Acessando mainframe..."
            st.rerun()
else:
    if st.session_state.game_over or st.session_state.pontos <= 0:
        st.error(f"🚨 CONEXÃO INTERROMPIDA! Agente Smith baniu o Sr. {st.session_state.nome}!")
        if st.button("🔄 Hackear Novamente"):
            st.session_state.posicao = 0
            st.session_state.pontos = 1000
            st.session_state.jogando = False
            st.rerun()

    elif st.session_state.posicao >= CASA_FINAL:
        tempo_total = round(time.time() - st.session_state.tempo_inicio, 2)
        st.success(f"🏆 MAINAFRAME SUCEDIDO! Concluído por {st.session_state.nome} em {tempo_total}s!")
        st.write(f"Aproveitamento: {st.session_state.quizzes_acertados}/{st.session_state.quizzes_respondidos} acertos.")
        if st.button("🔄 Reiniciar"):
            st.session_state.posicao = 0
            st.session_state.pontos = 1000
            st.session_state.jogando = False
            st.rerun()
    else:
        # Diálogos leves
        if st.session_state.ultimo_personagem == "morfeu": st.write("😎 **Morfeu:** *'Confie no seu treinamento.'*")
        elif st.session_state.ultimo_personagem == "trinity": st.write("👩‍💻 **Trinity:** *'Firewalls limpos.'*")
        else: st.write("🕴️ **Agente Smith:** *'Vou apagar seus pacotes.'*")

        col1, col2, col3 = st.columns(3)
        col1.metric("Hacker", st.session_state.nome)
        col2.metric("Nível", f"{st.session_state.posicao}/{CASA_FINAL}")
        col3.metric("Integridade", f"{st.session_state.pontos} pts")

        trilha = [". "] * (CASA_FINAL + 1)
        if st.session_state.posicao <= CASA_FINAL: trilha[st.session_state.posicao] = "🟢 "
        st.code("Root_ | " + "".join(trilha) + " | _Admin", language="markdown")

        if st.session_state.log_evento: st.text(st.session_state.log_evento)

        if not st.session_state.mostrar_quiz:
            if st.button("🎲 Jogue o Dado"):
                dado = random.randint(1, 4)
                st.session_state.posicao += dado
                st.session_state.log_evento = f"Dado: +{dado} camadas. Destino: nível {st.session_state.posicao}."
                if st.session_state.posicao in CASAS_ESPECIAIS:
                    ev = CASAS_ESPECIAIS[st.session_state.posicao]
                    st.session_state.posicao += ev["efeito"]
                    st.session_state.pontos += (ev["efeito"] * 100)
                    st.session_state.log_evento += f"\n{ev['msg']}"
                    st.session_state.ultimo_personagem = ev["char"]
                    if st.session_state.posicao < 0: st.session_state.posicao = 0
                if st.session_state.posicao < CASA_FINAL:
                    st.session_state.mostrar_quiz = True
                    st.session_state.quiz_atual = random.choice(LISTA_PERGUNTAS)
                st.rerun()
        else:
            st.write(f"❓ **{st.session_state.quiz_atual['pergunta']}**")
            resposta = st.radio("Escolha a chave:", st.session_state.quiz_atual['opcoes'])
            if st.button("Injetar Resposta"):
                st.session_state.quizzes_respondidos += 1
                idx = st.session_state.quiz_atual['opcoes'].index(resposta)
                if idx == st.session_state.quiz_atual['correta']:
                    st.session_state.quizzes_acertados += 1
                    st.session_state.pontos += 200
                    st.session_state.posicao += 1
                    st.session_state.log_evento = "🎉 Sucesso! +200 Integridade e +1 nível bônus!"
                    st.session_state.ultimo_personagem = random.choice(["morfeu", "trinity"])
                else:
                    st.session_state.pontos -= 150
                    st.session_state.game_over = (st.session_state.pontos <= 0)
                    st.session_state.log_evento = "❌ Falha! -150 de integridade."
                    st.session_state.ultimo_personagem = "smith"
                st.session_state.mostrar_quiz = False
                st.rerun()

st.write("---")
col_l, col_r = st.columns(2)
with col_r:
    if st.button("❌ ABORTAR_MISSÃO"):
        st.session_state.posicao = 0
        st.session_state.pontos = 1000
        st.session_state.jogando = False
        st.session_state.mostrar_quiz = False
        st.session_state.game_over = False
        st.session_state.ultimo_personagem = "morfeu"
        st.rerun()
