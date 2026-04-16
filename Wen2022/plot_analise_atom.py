#!/usr/bin/env python3
"""
Script para plotar dados das figuras 6a, 6b, 7a, 7b, 9a, 9b e 10.
Utiliza os arquivos Fig6a_A1.csv, Fig6a_A2.csv, Fig6a_A3.csv, Fig6a_A4.csv,
Fig6b_A1.csv, Fig6b_A2.csv, Fig6b_A3.csv, Fig6b_A4.csv,
Fig7a_A1.csv, Fig7a_A2.csv, Fig7a_A3.csv, Fig7a_A4.csv,
Fig7b_A1.csv, Fig7b_A2.csv, Fig7b_A3.csv, Fig7b_A4.csv,
fig9a_0_pi2.csv, fig9a_pi2_pi.csv, fig9a_pi_3pi2.csv, fig9a_3pi2_2pi.csv,
fig9b_0_pi2.csv, fig9b_pi2_pi.csv, fig9b_pi_3pi2.csv, fig9b_3pi2_2pi.csv,
fig10_A1.csv, fig10_A2.csv, fig10_A3.csv, fig10_A4.csv
da pasta Dados_Sim_Wen.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def read_csv_european_format(file_path):
    """
    Lê um arquivo CSV com formato europeu (ponto e vírgula como separador,
    vírgula como separador decimal).
    
    Args:
        file_path: Caminho para o arquivo CSV
        
    Returns:
        DataFrame com os dados lidos
    """
    # Ler o arquivo CSV com ponto e vírgula como separador
    # e vírgula como separador decimal
    df = pd.read_csv(file_path, sep=';', decimal=',', header=None)
    
    # Nomear as colunas
    df.columns = ['X', 'Y']
    
    return df

def plot_fig6a():
    """
    Cria o gráfico da figura 6a usando os arquivos Fig6a_A1 a Fig6a_A4.
    """
    # Caminho da pasta com os dados
    data_folder = 'Dados_Sim_Wen'
    
    # Lista de arquivos a serem plotados
    files = ['Fig6a_A1.csv', 'Fig6a_A2.csv', 'Fig6a_A3.csv', 'Fig6a_A4.csv']
    
    # Labels para cada série de dados
    labels = ['Wen et al. (2022) A1', 'Wen et al. (2022) A2', 'Wen et al. (2022) A3', 'Wen et al. (2022) A4']
    
    # Marcadores para cada série
    markers = ['s', 'o', '^', 'D']  # quadrado, círculo, triângulo, losango
    
    # Cores para cada série
    colors = ['black', 'red', 'green', 'purple']
    
    # Criar a figura
    plt.figure(figsize=(10, 6))
    
    # Plotar cada arquivo
    for i, (file, label, marker, color) in enumerate(zip(files, labels, markers, colors)):
        file_path = os.path.join(data_folder, file)
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo {file_path} não encontrado!")
            continue
        
        # Ler os dados
        try:
            df = read_csv_european_format(file_path)
            print(f"Dados carregados de {file}: {len(df)} pontos")
            
            # Plotar os dados
            plt.plot(df['X'], df['Y'], marker=marker, linestyle='-', label=label, 
                    color=color, markersize=6, linewidth=1.5, alpha=0.7)
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
            continue
    
    # Configurar o gráfico
    plt.xlabel(r'Diâmetro da gota ($\mu$m)', fontsize=12)
    plt.ylabel('PDF (-)', fontsize=12)
    plt.title('Figura 6a', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Definir limites dos eixos
    plt.xlim(0, 200)
    plt.ylim(0, 0.4)
    
    # Configurar os ticks dos eixos
    # Eixo X: intervalos de 50
    x_ticks = np.arange(0, 201, 50)
    plt.xticks(x_ticks)
    
    # Eixo Y: intervalos de 0.2
    y_ticks = np.arange(0, 0.41, 0.2)
    plt.yticks(y_ticks)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar a figura
    output_file = 'fig6a.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nFigura salva em '{output_file}'")
    
    # Mostrar o gráfico
    plt.show()

def plot_fig6b():
    """
    Cria o gráfico da figura 6b usando os arquivos Fig6b_A1 a Fig6b_A4.
    """
    # Caminho da pasta com os dados
    data_folder = 'Dados_Sim_Wen'
    
    # Lista de arquivos a serem plotados
    files = ['Fig6b_A1.csv', 'Fig6b_A2.csv', 'Fig6b_A3.csv', 'Fig6b_A4.csv']
    
    # Labels para cada série de dados
    labels = ['Wen et al. (2022) A1', 'Wen et al. (2022) A2', 'Wen et al. (2022) A3', 'Wen et al. (2022) A4']
    
    # Marcadores para cada série
    markers = ['s', 'o', '^', 'D']  # quadrado, círculo, triângulo, losango
    
    # Cores para cada série
    colors = ['black', 'red', 'green', 'purple']
    
    # Criar a figura
    plt.figure(figsize=(10, 6))
    
    # Plotar cada arquivo
    for i, (file, label, marker, color) in enumerate(zip(files, labels, markers, colors)):
        file_path = os.path.join(data_folder, file)
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo {file_path} não encontrado!")
            continue
        
        # Ler os dados
        try:
            df = read_csv_european_format(file_path)
            print(f"Dados carregados de {file}: {len(df)} pontos")
            
            # Plotar os dados
            plt.plot(df['X'], df['Y'], marker=marker, linestyle='-', label=label, 
                    color=color, markersize=6, linewidth=1.5, alpha=0.7)
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
            continue
    
    # Configurar o gráfico
    plt.xlabel(r'Diâmetro da gota ($\mu$m)', fontsize=12)
    plt.ylabel(r'Volume ($10^{-9}$ m$^3$)', fontsize=12)
    plt.title('Figura 6b', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Definir limites dos eixos
    plt.xlim(0, 300)
    plt.ylim(0, 10)
    
    # Configurar os ticks dos eixos
    # Eixo X: intervalos de 50
    x_ticks = np.arange(0, 301, 50)
    plt.xticks(x_ticks)
    
    # Eixo Y: intervalos de 2
    y_ticks = np.arange(0, 11, 2)
    plt.yticks(y_ticks)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar a figura
    output_file = 'fig6b.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nFigura salva em '{output_file}'")
    
    # Mostrar o gráfico
    plt.show()

def plot_fig7a():
    """
    Cria o gráfico da figura 7a usando os arquivos Fig7a_A1 a Fig7a_A4.
    """
    # Caminho da pasta com os dados
    data_folder = 'Dados_Sim_Wen'
    
    # Lista de arquivos a serem plotados
    files = ['Fig7a_A1.csv', 'Fig7a_A2.csv', 'Fig7a_A3.csv', 'Fig7a_A4.csv']
    
    # Labels para cada série de dados
    labels = ['Wen et al. (2022) A1', 'Wen et al. (2022) A2', 'Wen et al. (2022) A3', 'Wen et al. (2022) A4']
    
    # Marcadores para cada série
    markers = ['s', 'o', '^', 'D']  # quadrado, círculo, triângulo, losango
    
    # Cores para cada série
    colors = ['black', 'red', 'green', 'purple']
    
    # Criar a figura
    plt.figure(figsize=(10, 6))
    
    # Plotar cada arquivo
    for i, (file, label, marker, color) in enumerate(zip(files, labels, markers, colors)):
        file_path = os.path.join(data_folder, file)
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo {file_path} não encontrado!")
            continue
        
        # Ler os dados
        try:
            df = read_csv_european_format(file_path)
            print(f"Dados carregados de {file}: {len(df)} pontos")
            
            # Plotar os dados
            plt.plot(df['X'], df['Y'], marker=marker, linestyle='-', label=label, 
                    color=color, markersize=6, linewidth=1.5, alpha=0.7)
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
            continue
    
    # Configurar o gráfico
    plt.xlabel(r'Distância radial, $r/D_l$ (-)', fontsize=12)
    plt.ylabel(r'$D_{32}$ ($\mu$m)', fontsize=12)
    plt.title('Figura 7a', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Definir limites dos eixos
    plt.xlim(0, 4)
    plt.ylim(50, 150)
    
    # Configurar os ticks dos eixos
    # Eixo X: intervalos de 0.5
    x_ticks = np.arange(0, 4.5, 0.5)
    plt.xticks(x_ticks)
    
    # Eixo Y: intervalos de 25
    y_ticks = np.arange(50, 151, 25)
    plt.yticks(y_ticks)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar a figura
    output_file = 'fig7a.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nFigura salva em '{output_file}'")
    
    # Mostrar o gráfico
    plt.show()

def plot_fig7b():
    """
    Cria o gráfico da figura 7b usando os arquivos Fig7b_A1 a Fig7b_A4.
    """
    # Caminho da pasta com os dados
    data_folder = 'Dados_Sim_Wen'
    
    # Lista de arquivos a serem plotados
    files = ['Fig7b_A1.csv', 'Fig7b_A2.csv', 'Fig7b_A3.csv', 'Fig7b_A4.csv']
    
    # Labels para cada série de dados
    labels = ['Wen et al. (2022) A1', 'Wen et al. (2022) A2', 'Wen et al. (2022) A3', 'Wen et al. (2022) A4']
    
    # Marcadores para cada série
    markers = ['s', 'o', '^', 'D']  # quadrado, círculo, triângulo, losango
    
    # Cores para cada série
    colors = ['black', 'red', 'green', 'purple']
    
    # Criar a figura
    plt.figure(figsize=(10, 6))
    
    # Plotar cada arquivo
    for i, (file, label, marker, color) in enumerate(zip(files, labels, markers, colors)):
        file_path = os.path.join(data_folder, file)
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo {file_path} não encontrado!")
            continue
        
        # Ler os dados
        try:
            df = read_csv_european_format(file_path)
            print(f"Dados carregados de {file}: {len(df)} pontos")
            
            # Plotar os dados
            plt.plot(df['X'], df['Y'], marker=marker, linestyle='-', label=label, 
                    color=color, markersize=6, linewidth=1.5, alpha=0.7)
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
            continue
    
    # Configurar o gráfico
    plt.xlabel(r'Distância radial, $r/D_l$ (-)', fontsize=12)
    plt.ylabel(r'$D_{10}$ ($\mu$m)', fontsize=12)
    plt.title('Figura 7b', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Definir limites dos eixos
    plt.xlim(0, 4)
    plt.ylim(0, 140)
    
    # Configurar os ticks dos eixos
    # Eixo X: intervalos de 0.5
    x_ticks = np.arange(0, 4.5, 0.5)
    plt.xticks(x_ticks)
    
    # Eixo Y: intervalos de 20
    y_ticks = np.arange(0, 141, 20)
    plt.yticks(y_ticks)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar a figura
    output_file = 'fig7b.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nFigura salva em '{output_file}'")
    
    # Mostrar o gráfico
    plt.show()

def plot_fig9a():
    """
    Cria o gráfico da figura 9a usando os arquivos fig9a_0_pi2.csv, fig9a_pi2_pi.csv,
    fig9a_pi_3pi2.csv e fig9a_3pi2_2pi.csv.
    """
    # Caminho da pasta com os dados
    data_folder = 'Dados_Sim_Wen'
    
    # Lista de arquivos a serem plotados
    files = ['fig9a_0_pi2.csv', 'fig9a_pi2_pi.csv', 'fig9a_pi_3pi2.csv', 'fig9a_3pi2_2pi.csv']
    
    # Labels para cada série de dados (baseados nos intervalos de ângulo)
    labels = ['Wen et al. (2022) 0-π/2', 'Wen et al. (2022) π/2-π', 
              'Wen et al. (2022) π-3π/2', 'Wen et al. (2022) 3π/2-2π']
    
    # Marcadores para cada série
    markers = ['s', 'o', '^', 'D']  # quadrado, círculo, triângulo, losango
    
    # Cores para cada série
    colors = ['black', 'red', 'green', 'purple']
    
    # Criar a figura
    plt.figure(figsize=(10, 6))
    
    # Plotar cada arquivo
    for i, (file, label, marker, color) in enumerate(zip(files, labels, markers, colors)):
        file_path = os.path.join(data_folder, file)
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo {file_path} não encontrado!")
            continue
        
        # Ler os dados
        try:
            df = read_csv_european_format(file_path)
            print(f"Dados carregados de {file}: {len(df)} pontos")
            
            # Plotar os dados (sem linhas, apenas marcadores)
            plt.plot(df['X'], df['Y'], marker=marker, linestyle='', label=label, 
                    color=color, markersize=6, alpha=0.7)
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
            continue
    
    # Configurar o gráfico
    plt.xlabel(r'Tempo ($10^{-3}$ s)', fontsize=12)
    plt.ylabel(r'$D_{32}$ ($\mu$m)', fontsize=12)
    plt.title('Figura 9a', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar a figura
    output_file = 'fig9a.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nFigura salva em '{output_file}'")
    
    # Mostrar o gráfico
    plt.show()

def plot_fig9b():
    """
    Cria o gráfico da figura 9b usando os arquivos fig9b_0_pi2.csv, fig9b_pi2_pi.csv,
    fig9b_pi_3pi2.csv e fig9b_3pi2_2pi.csv.
    """
    # Caminho da pasta com os dados
    data_folder = 'Dados_Sim_Wen'
    
    # Lista de arquivos a serem plotados
    files = ['fig9b_0_pi2.csv', 'fig9b_pi2_pi.csv', 'fig9b_pi_3pi2.csv', 'fig9b_3pi2_2pi.csv']
    
    # Labels para cada série de dados (baseados nos intervalos de ângulo)
    labels = ['Wen et al. (2022) 0-π/2', 'Wen et al. (2022) π/2-π', 
              'Wen et al. (2022) π-3π/2', 'Wen et al. (2022) 3π/2-2π']
    
    # Marcadores para cada série
    markers = ['s', 'o', '^', 'D']  # quadrado, círculo, triângulo, losango
    
    # Cores para cada série
    colors = ['black', 'red', 'green', 'purple']
    
    # Criar a figura
    plt.figure(figsize=(10, 6))
    
    # Plotar cada arquivo
    for i, (file, label, marker, color) in enumerate(zip(files, labels, markers, colors)):
        file_path = os.path.join(data_folder, file)
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo {file_path} não encontrado!")
            continue
        
        # Ler os dados
        try:
            df = read_csv_european_format(file_path)
            print(f"Dados carregados de {file}: {len(df)} pontos")
            
            # Plotar os dados (sem linhas, apenas marcadores)
            plt.plot(df['X'], df['Y'], marker=marker, linestyle='', label=label, 
                    color=color, markersize=6, alpha=0.7)
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
            continue
    
    # Configurar o gráfico
    plt.xlabel(r'Tempo ($10^{-3}$ s)', fontsize=12)
    plt.ylabel(r'$D_{10}$ ($\mu$m)', fontsize=12)
    plt.title('Figura 9b', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar a figura
    output_file = 'fig9b.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nFigura salva em '{output_file}'")
    
    # Mostrar o gráfico
    plt.show()

def plot_fig10():
    """
    Cria o gráfico da figura 10 usando os arquivos fig10_A1.csv, fig10_A2.csv,
    fig10_A3.csv e fig10_A4.csv.
    """
    # Caminho da pasta com os dados
    data_folder = 'Dados_Sim_Wen'
    
    # Lista de arquivos a serem plotados
    files = ['fig10_A1.csv', 'fig10_A2.csv', 'fig10_A3.csv', 'fig10_A4.csv']
    
    # Labels para cada série de dados
    labels = ['Wen et al. (2022) A1', 'Wen et al. (2022) A2', 'Wen et al. (2022) A3', 'Wen et al. (2022) A4']
    
    # Marcadores para cada série
    markers = ['s', 'o', '^', 'D']  # quadrado, círculo, triângulo, losango
    
    # Cores para cada série
    colors = ['black', 'red', 'green', 'purple']
    
    # Criar a figura
    plt.figure(figsize=(10, 6))
    
    # Plotar cada arquivo
    for i, (file, label, marker, color) in enumerate(zip(files, labels, markers, colors)):
        file_path = os.path.join(data_folder, file)
        
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo {file_path} não encontrado!")
            continue
        
        # Ler os dados
        try:
            df = read_csv_european_format(file_path)
            print(f"Dados carregados de {file}: {len(df)} pontos")
            
            # Plotar os dados (sem linhas, apenas marcadores)
            plt.plot(df['X'], df['Y'], marker=marker, linestyle='', label=label, 
                    color=color, markersize=6, alpha=0.7)
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")
            continue
    
    # Configurar o gráfico
    plt.xlabel('Period number', fontsize=12)
    plt.ylabel('Total Chi-square value (-)', fontsize=12)
    plt.title('Figura 10', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar a figura
    output_file = 'fig10.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nFigura salva em '{output_file}'")
    
    # Mostrar o gráfico
    plt.show()

def main():
    """
    Função principal.
    """
    print("Plotando dados da figura 6a...")
    print("=" * 50)
    
    plot_fig6a()
    
    print("\n" + "=" * 50)
    print("Plotando dados da figura 6b...")
    print("=" * 50)
    
    plot_fig6b()
    
    print("\n" + "=" * 50)
    print("Plotando dados da figura 7a...")
    print("=" * 50)
    
    plot_fig7a()
    
    print("\n" + "=" * 50)
    print("Plotando dados da figura 7b...")
    print("=" * 50)
    
    plot_fig7b()
    
    print("\n" + "=" * 50)
    print("Plotando dados da figura 9a...")
    print("=" * 50)
    
    plot_fig9a()
    
    print("\n" + "=" * 50)
    print("Plotando dados da figura 9b...")
    print("=" * 50)
    
    plot_fig9b()
    
    print("\n" + "=" * 50)
    print("Plotando dados da figura 10...")
    print("=" * 50)
    
    plot_fig10()
    
    print("=" * 50)
    print("Processamento concluído!")

if __name__ == "__main__":
    main()

