import streamlit as st
import matplotlib.pyplot as plt
import os
def salvar_dados(nome, serie, nota1, nota2, nota3):
    with open('dados_alunos.txt', 'a') as f:
        f.write(f"{nome},{serie},{nota1},{nota2},{nota3}\n")
def ler_dados():
    alunos = []
    if os.path.exists('dados_alunos.txt'):
        with open('dados_alunos.txt', 'r') as f:
            for linha in f:
                dados = linha.strip().split(',')
                nome = dados[0]
                serie = dados[1]
                n1 = float(dados[2])
                n2 = float(dados[3])
                n3 = float(dados[4])
                x = n1 + n2 + n3
                media = x / 3
                alunos.append({
                    'nome': nome,
                    'serie': serie,
                    'media': media
                })

    return alunos
def calcular_medias_por_serie(alunos):
    medias_por_serie = {}
    for aluno in alunos:
        serie = aluno['serie']
        media = aluno['media']
        if serie not in medias_por_serie:
            medias_por_serie[serie] = []
        medias_por_serie[serie].append(media)
    return medias_por_serie
def exibir_grafico(medias, serie):
    fig, ax = plt.subplots()
    ax.bar(range(len(medias)), medias)
    ax.set_xlabel('Alunos')
    ax.set_ylabel('Média')
    ax.set_title(f'Distribuição das Médias - Série {serie}')
    st.pyplot(fig)
def main():
    st.title("Análise de Notas")
    st.header("Cadastrar Aluno")
    nome = st.text_input("Nome do aluno")
    serie = st.selectbox("Série", ["1D", "2D", "3D"])
    nota1 = st.number_input("Nota 1", 0.0, 10.0, step=0.1)
    nota2 = st.number_input("Nota 2", 0.0, 10.0, step=0.1)
    nota3 = st.number_input("Nota 3", 0.0, 10.0, step=0.1)
    if st.button("Salvar"):
        if nome.strip() != "":
            salvar_dados(nome, serie, nota1, nota2, nota3)
            st.success("Aluno cadastrado com sucesso!")
        else:
            st.error("Por favor, preencha o nome do aluno.")
    st.header("Relatórios")
    alunos = ler_dados()
    medias_por_serie = calcular_medias_por_serie(alunos)
    if alunos:
        for serie, medias in medias_por_serie.items():
            media_geral = sum(medias) / len(medias)
            st.write(f"Média geral da série {serie}: {media_geral:.2f}")
        serie_selecionada = st.selectbox("Selecione uma série para ver o gráfico:", list(medias_por_serie.keys()))
        exibir_grafico(medias_por_serie[serie_selecionada], serie_selecionada)
    else:
        st.write("Nenhum aluno cadastrado ainda.")
main()
