        else:
            st.write(f"❓ **{st.session_state.quiz_atual['pergunta']}**")
            
            # Cria um botão para cada opção da pergunta atual
            for idx, opcao in enumerate(st.session_state.quiz_atual["opcoes"]):
                if st.button(opcao, key=f"op_{idx}"):
                    st.session_state.quizzes_respondidos += 1
                    
                    if idx == st.session_state.quiz_atual["correta"]:
                        st.session_state.quizzes_acertados += 1
                        st.session_state.pontos += 200
                        st.session_state.log_evento = "🟢 Resposta correta! +200 pontos de Integridade."
                    else:
                        st.session_state.pontos -= 200
                        # Modificado: Agora reduz 2 níveis em vez de 1 (Garante que não fica menor que 0)
                        st.session_state.posicao = max(0, st.session_state.posicao - 2)
                        st.session_state.log_evento = "🔴 Resposta incorreta! -200 pontos e voltou 2 níveis."
                    
                    # Fecha o quiz para permitir jogar o dado de novo
                    st.session_state.mostrar_quiz = False
                    st.session_state.quiz_atual = None
                    st.rerun()
