#!/usr/bin/env python3
"""
Script para plotar Drop half-length vs time a partir do arquivo R_5n.txt
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Caminho do arquivo (relativo ao diretório onde o script está)
script_dir = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(script_dir, 'R_5n.txt')
arquivo_4n = os.path.join(script_dir, 'R_4n.txt')
arquivo_6n = os.path.join(script_dir, 'R_6n.txt')
arquivo_zheng = os.path.join(script_dir, 'Zheng.csv')
arquivo_fuster512 = os.path.join(script_dir, 'Fuster512.csv')
arquivo_fuster1024 = os.path.join(script_dir, 'Fuster1024.csv')
arquivo_fuster2048 = os.path.join(script_dir, 'Fuster2048.csv')

# Lê os dados do arquivo
# Pula a primeira linha (cabeçalho) e lê as colunas separadas por ponto e vírgula
dados = []
with open(arquivo, 'r') as f:
    linhas = f.readlines()
    for linha in linhas:
        linha = linha.strip()
        # Ignora linhas vazias e comentários
        if linha and not linha.startswith('#'):
            partes = linha.split(';')
            if len(partes) >= 3:
                try:
                    ct = int(partes[0].strip())
                    time = float(partes[1].strip())
                    R = float(partes[2].strip())
                    dados.append([time, R])
                except ValueError:
                    continue

# Converte para arrays numpy
dados = np.array(dados)
time = dados[:, 0]
drop_half_length = dados[:, 1]

# Lê os dados do arquivo R_4n.txt
dados_4n = []
with open(arquivo_4n, 'r') as f:
    linhas = f.readlines()
    for linha in linhas:
        linha = linha.strip()
        # Ignora linhas vazias e comentários
        if linha and not linha.startswith('#'):
            partes = linha.split(';')
            if len(partes) >= 3:
                try:
                    ct = int(partes[0].strip())
                    time_4n = float(partes[1].strip())
                    R_4n = float(partes[2].strip())
                    dados_4n.append([time_4n, R_4n])
                except ValueError:
                    continue

# Converte para arrays numpy
dados_4n = np.array(dados_4n)
time_4n = dados_4n[:, 0]
drop_half_length_4n = dados_4n[:, 1]

# Lê os dados do arquivo R_6n.txt
dados_6n = []
with open(arquivo_6n, 'r') as f:
    linhas = f.readlines()
    for linha in linhas:
        linha = linha.strip()
        # Ignora linhas vazias e comentários
        if linha and not linha.startswith('#'):
            partes = linha.split(';')
            if len(partes) >= 3:
                try:
                    ct = int(partes[0].strip())
                    time_6n = float(partes[1].strip())
                    R_6n = float(partes[2].strip())
                    dados_6n.append([time_6n, R_6n])
                except ValueError:
                    continue

# Converte para arrays numpy
dados_6n = np.array(dados_6n)
time_6n = dados_6n[:, 0]
drop_half_length_6n = dados_6n[:, 1]

# Lê os dados do arquivo Zheng.csv
dados_zheng = []
with open(arquivo_zheng, 'r') as f:
    linhas = f.readlines()
    for linha in linhas:
        linha = linha.strip()
        if linha:
            # Substitui vírgula por ponto para decimais e separa por ponto e vírgula
            partes = linha.split(';')
            if len(partes) >= 2:
                try:
                    time_zheng = float(partes[0].strip().replace(',', '.'))
                    R_zheng = float(partes[1].strip().replace(',', '.'))
                    dados_zheng.append([time_zheng, R_zheng])
                except ValueError:
                    continue

# Converte para arrays numpy
dados_zheng = np.array(dados_zheng)
time_zheng = dados_zheng[:, 0]
drop_half_length_zheng = dados_zheng[:, 1]

# Lê os dados do arquivo Fuster512.csv
dados_fuster512 = []
with open(arquivo_fuster512, 'r') as f:
    linhas = f.readlines()
    for linha in linhas:
        linha = linha.strip()
        if linha:
            # Substitui vírgula por ponto para decimais e separa por ponto e vírgula
            partes = linha.split(';')
            if len(partes) >= 2:
                try:
                    time_fuster512 = float(partes[0].strip().replace(',', '.'))
                    R_fuster512 = float(partes[1].strip().replace(',', '.'))
                    dados_fuster512.append([time_fuster512, R_fuster512])
                except ValueError:
                    continue

# Converte para arrays numpy
dados_fuster512 = np.array(dados_fuster512)
time_fuster512 = dados_fuster512[:, 0]
drop_half_length_fuster512 = dados_fuster512[:, 1]

# Lê os dados do arquivo Fuster1024.csv
dados_fuster1024 = []
with open(arquivo_fuster1024, 'r') as f:
    linhas = f.readlines()
    for linha in linhas:
        linha = linha.strip()
        if linha:
            # Substitui vírgula por ponto para decimais e separa por ponto e vírgula
            partes = linha.split(';')
            if len(partes) >= 2:
                try:
                    time_fuster1024 = float(partes[0].strip().replace(',', '.'))
                    R_fuster1024 = float(partes[1].strip().replace(',', '.'))
                    dados_fuster1024.append([time_fuster1024, R_fuster1024])
                except ValueError:
                    continue

# Converte para arrays numpy
dados_fuster1024 = np.array(dados_fuster1024)
time_fuster1024 = dados_fuster1024[:, 0]
drop_half_length_fuster1024 = dados_fuster1024[:, 1]

# Lê os dados do arquivo Fuster2048.csv
dados_fuster2048 = []
with open(arquivo_fuster2048, 'r') as f:
    linhas = f.readlines()
    for linha in linhas:
        linha = linha.strip()
        if linha:
            # Substitui vírgula por ponto para decimais e separa por ponto e vírgula
            partes = linha.split(';')
            if len(partes) >= 2:
                try:
                    time_fuster2048 = float(partes[0].strip().replace(',', '.'))
                    R_fuster2048 = float(partes[1].strip().replace(',', '.'))
                    dados_fuster2048.append([time_fuster2048, R_fuster2048])
                except ValueError:
                    continue

# Converte para arrays numpy
dados_fuster2048 = np.array(dados_fuster2048)
time_fuster2048 = dados_fuster2048[:, 0]
drop_half_length_fuster2048 = dados_fuster2048[:, 1]

# Cria a figura
plt.figure(figsize=(10, 6))
plt.plot(time_4n, drop_half_length_4n, 'purple', linestyle='', marker='v', markersize=6, markevery=1, label='4 níveis de refinamento')
plt.plot(time, drop_half_length, 'b', linestyle='', marker='o', markersize=6, markevery=1, label='5 níveis de refinamento')
plt.plot(time_6n, drop_half_length_6n, 'orange', linestyle='', marker='p', markersize=6, markevery=1, label='6 níveis de refinamento')
plt.plot(time_zheng, drop_half_length_zheng, 'r', linestyle='', marker='^', markersize=6, markevery=2, label='Zheng et al')
plt.plot(time_fuster512, drop_half_length_fuster512, 'c', linestyle='', marker='s', markersize=6, markevery=2, label='Fuster 512')
plt.plot(time_fuster1024, drop_half_length_fuster1024, 'g', linestyle='', marker='d', markersize=6, markevery=2, label='Fuster 1024')
plt.plot(time_fuster2048, drop_half_length_fuster2048, 'm', linestyle='', marker='*', markersize=6, markevery=2, label='Fuster 2048')
plt.xlabel('Tempo (s)', fontsize=12)
plt.ylabel(r'r$_{max}$/a', fontsize=12)
plt.xlim(0, 16)
plt.ylim(1, 1.7)
#plt.title('Drop half-length vs time', fontsize=14, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Salva a figura
figura_path = os.path.join(script_dir, 'drop_half_length_vs_time.png')
plt.savefig(figura_path, dpi=300, bbox_inches='tight')
print(f"Figura salva como '{figura_path}'")
print(f"Total de pontos plotados (R_4n.txt): {len(time_4n)}")
print(f"Total de pontos plotados (R_5n.txt): {len(time)}")
print(f"Total de pontos plotados (R_6n.txt): {len(time_6n)}")
print(f"Total de pontos plotados (Zheng.csv): {len(time_zheng)}")
print(f"Total de pontos plotados (Fuster512.csv): {len(time_fuster512)}")
print(f"Total de pontos plotados (Fuster1024.csv): {len(time_fuster1024)}")
print(f"Total de pontos plotados (Fuster2048.csv): {len(time_fuster2048)}")

# Mostra a figura
plt.show()

