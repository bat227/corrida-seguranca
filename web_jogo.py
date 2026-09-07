import streamlit as st
import random
import time

# Configuração da página web
st.set_page_config(page_title="Corrida pela Segurança", page_icon="🛡️", layout="centered")

# ==========================================
# BANCO DE DADOS EXPANDIDO (MÓDULO FLIPPITY)
# ==========================================
if 'perguntas' not in st.session_state:
    st.session_state.perguntas = [
        {
            "pergunta": "O tratamento de dados pessoais pode ocorrer para o cumprimento de obrigação legal?",
            "opcoes": ["Sim, é uma das bases legais válidas da LGPD.", "Não, precisa sempre de consentimento absoluto.", "Apenas se o titular for menor de idade."],
            "correta": 0
        },
        {
            "pergunta": "Se formulários de clientes forem descartados no lixo comum sem fragmentar, ocorre infração?",
            "opcoes": ["Não, desde que o lixo seja recolhido no mesmo dia.", "Sim, configura descarte inadequado e risco de vazamento.", "Não, pois papéis físicos não entram no escopo digital."],
            "correta": 1
        },
        {
            "pergunta": "Deixar o computador de trabalho desbloqueado ao ir almoçar viola qual pilar da Segurança?",
            "opcoes": ["Disponibilidade.", "Integridade.", "Confidencialidade."],
            "correta": 2
        },
        {
            "pergunta": "O que caracteriza um ataque de 'Phishing'?",
            "opcoes": ["Um vírus que bloqueia os arquivos do computador exigindo resgate.", "E-mails ou mensagens falsas que imitam instituições reais para roubar dados.", "Um acesso físico não autorizado ao servidor da empresa."],
            "correta": 1
        },
        {
            "pergunta": "Qual das seguintes opções é considerada um 'Dado Pessoal Sensível' segundo a LGPD?",
            "opcoes": ["Número de telefone celular.", "Origem racial/étnica, convicção religiosa ou dados de saúde.", "Endereço comercial da empresa."],
            "correta": 1
        },
        {
            "pergunta": "Qual é a função principal da ANPD (Autoridade Nacional de Proteção de Dados)?",
            "opcoes": ["Criar os códigos de programação dos sistemas do governo.", "Fiscalizar e aplicar sanções a empresas que descumprirem a LGPD.", "Vender softwares de antivírus corporativos."],
            "correta": 1
        },
        {
            "pergunta": "O que significa o pilar da 'Integridade' na Segurança da Informação?",
            "opcoes": ["Garantir que a informação esteja disponível sempre que necessário.", "Garantir que a informação não seja alterada ou corrompida por pessoas não autorizadas.", "Garantir que apenas pessoas autorizadas vejam a informação."],
            "correta": 1
        },
        {
            "pergunta": "Qual destas práticas ajuda a mitigar o risco de Engenharia Social nas empresas?",
            "opcoes": ["Instalar apenas um firewall de rede potente.", "Realizar treinamentos periódicos de conscientização com os funcionários.", "Aumentar a velocidade da internet dos servidores."],
            "correta": 1
        },
        {
            "pergunta": "No contexto da LGPD, quem é a figura do 'Controlador'?",
            "opcoes": ["A pessoa ou empresa a quem competem as decisões sobre o tratamento dos dados.", "O funcionário de TI que digita o código do sistema.", "O cliente dono dos dados pessoais."],
            "correta": 0
        },
        {
            "pergunta": "O que é criptografia de chave pública/privada?",
            "opcoes": ["Um método para apagar permanentemente os dados do servidor físico.", "Uma técnica de embaralhar dados para que apenas quem tem a chave correta possa ler.", "Uma senha simples que todos os funcionários compartilham."],
            "correta": 1
        }
    ]

CASAS_ESPECIAIS = {
    3: {"msg": "⚠️ Você navegou num site sem verificação de segurança! (Volte 2 casas)", "efeito": -2},
    6: {"msg": "🛡️ Você chegou aos três pilares da LGPD - pessoas, processos e tecnologia! (Avance 2 casas)", "efeito": 2},
    9: {"msg": "🚨 A ANPD fiscalizou sua empresa e verificou que a LGPD não foi aplicada! (Volte 3 casas)", "efeito": -3},
    12: {"msg": "💼 Você garantiu fácil acesso aos titulares sobre o tratamento de dados! (Avance 1 casa)", "efeito": 1}
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

st.title("🛡️ Corrida pela Segurança Digital")
st.subheader("Trabalho Acadêmico de Engenharia de Software")

# ========================================================
# TELA DE INTRODUÇÃO E IMPORTÂNCIA DA ISO 12207
# ========================================================
if not st.session_state.jogando:
    st.markdown("""
    ### 📖 Introdução ao Projeto
    Bem-vindo à **Corrida pela Segurança Digital**! Este software foi projetado e documentado como um estudo prático de **Engenharia de Software**, abordando a conscientização sobre a Lei Geral de Proteção de Dados (LGPD) e boas práticas de segurança cibernética.
    
    ### 🧠 Por que utilizamos a ISO/IEC 12207?
    A **ISO/IEC 12207** é a norma internacional de referência para os **Processos de Ciclo de Vida de Software**. A sua importância no desenvolvimento deste jogo e no mercado real se justifica por:
    
    *   **Qualidade e Estrutura:** Ela divide o projeto em etapas bem definidas (Requisitos, Design, Construção e Testes), garantindo que o software não seja apenas uma 'gambiarra', mas um sistema robusto.
    *   **Mitigação de Riscos:** Através do conceito de *Tailoring* (Adaptação), conseguimos cortar processos burocráticos pesados para entregar um protótipo perfeitamente funcional dentro do curto prazo da faculdade.
    *   **Manutenibilidade:** A estrutura isola a camada de dados (nosso banco de perguntas) da camada visual, permitindo correções rápidas no sistema sem quebrar o jogo.
    
    ---
    """)
    
    nome_input = st.text_input("👤 Digite o nome do Jogador ou Grupo da Faculdade para iniciar:")
    if st.button("🚀 Iniciar Partida"):
        if nome_input:
            st.session_state.nome = nome_input
            st.session_state.posicao = 0
            st.session_state.pontos = 1000
            st.session_state.tempo_inicio = time.time()
            st.session_state.jogando = True
            st.session_state.log_evento = "Partida iniciada! Avance até a casa final respondendo aos desafios."
            st.rerun()
        else:
            st.warning("Por favor, digite um nome para começar.")

# Tela de Jogo Ativo
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Jogador", st.session_state.nome)
    col2.metric("Posição Atual", f"Casa {st.session_state.posicao}/{CASA_FINAL}")
    col3.metric("Pontuação", f"{st.session_state.pontos} pts")

    trilha = ["_ "] * (CASA_FINAL + 1)
    if st.session_state.posicao <= CASA_FINAL:
        trilha[st.session_state.posicao] = "🤖 "
    st.code("Início | " + "".join(trilha) + " | Fim", language="markdown")

    if st.session_state.log_evento:
        st.info(st.session_state.log_evento)

    if st.session_state.posicao >= CASA_FINAL:
        tempo_total = round(time.time() - st.session_state.tempo_inicio, 2)
        st.balloons()
        st.success(f"🏆 PARABÉNS! Você concluiu a corrida em {tempo_total}s com {st.session_state.pontos} pontos!")
        
        st.write("### 📊 Leaderboard da Turma (Interacty)")
        st.write(f"1º Lugar: Grupo_Cyber_Sec - 1400 pts (35.4s)")
        st.write(f"2º Lugar: **{st.session_state.nome}** - {st.session_state.pontos} pts ({tempo_total}s) 👈")
        st.write(f"3º Lugar: Alunos_Engenharia - 850 pts (48.1s)")
        
        if st.button("🔄 Jogar Novamente"):
            st.session_state.jogando = False
            st.rerun()

    elif not st.session_state.mostrar_quiz:
        if st.button("🎲 Girar o Dado"):
            dado = random.randint(1, 4)
            st.session_state.posicao += dado
            st.session_state.log_evento = f"O dado rolou número {dado}! Você avançou para a casa {st.session_state.posicao}."
            
            if st.session_state.posicao in CASAS_ESPECIAIS:
                ev = CASAS_ESPECIAIS[st.session_state.posicao]
                st.session_state.posicao += ev["efeito"]
                st.session_state.pontos += (ev["efeito"] * 100)
                st.session_state.log_evento += f"\n{ev['msg']}"
                if st.session_state.posicao < 0: st.session_state.posicao = 0
            
            elif random.choice([True, False]) and st.session_state.posicao < CASA_FINAL:
                st.session_state.mostrar_quiz = True
                st.session_state.quiz_atual = random.choice(st.session_state.perguntas)
                
            st.rerun()
else:
    st.write("---")
    st.write(f"⚡ **[DESAFIO FLIPPITY]** {st.session_state.quiz_atual['pergunta']}")
    resposta = st.radio("Escolha uma alternativa:", st.session_state.quiz_atual['opcoes'])
    
    if st.button("Confirmar Resposta"):
        idx_resposta = st.session_state.quiz_atual['opcoes'].index(resposta)
        if idx_resposta == st.session_state.quiz_atual['correta']:
            st.session_state.pontos += 200
            st.session_state.posicao += 1
            st.session_state.log_evento = "🎉 Resposta CORRETA! Você ganhou +200 pontos e +1 casa bônus!"
        else:
            st.session_state.pontos -= 150
            st.session_state.log_evento = f"❌ Resposta INCORRETA! O sistema removeu 150 pontos."
            
        st.session_state.mostrar_quiz = False
        st.rerun()
