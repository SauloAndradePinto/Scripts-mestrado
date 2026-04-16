import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import pandas as pd
import re

# Configurar matplotlib para usar LaTeX
plt.rcParams['text.usetex'] = False  # Usar False se LaTeX não estiver instalado, True se estiver
plt.rcParams['mathtext.fontset'] = 'stix'  # Usar fonte matemática

# Diretório com os arquivos de sonda
probe_dir = 'output4/probe_points'

# Parâmetro de leitura dos arquivos
# Número de linhas a pular no início do arquivo (0 = começar da primeira linha)
# Padrão: 1 (pula a linha de cabeçalho VARIABLES=...)
linha_inicio_leitura = 30000

# Linha final (1-indexada, inclusive) para limitar a leitura do arquivo.
# Se None, lê até o fim do arquivo.
linha_fim_leitura = 40000

# Parâmetros de normalização
D = 0.0825
deslocamento = -0.4125
U_c = 2.1865

# Carregar dados experimentais (já normalizados)
exp_dir = 'DadosExp'
exp_dir2 = 'DadosExp2'  # Dados experimentais para a segunda figura (flutuações)
exp_dir3 = 'DadosExp3'  # Dados experimentais para a terceira figura (flutuações v')
exp_dir4 = 'DadosExp4'  # Dados experimentais para a quarta figura (u'v'/Uc²)

# Mapeamento entre superfícies e arquivos experimentais (primeira figura - média)
exp_files_map = {
    'surf00001': 'exp_xd004.csv',  # x/D=0.04
    'surf00002': 'exp_xd1.csv',    # x/D=1
    'surf00003': 'exp_xd2.csv',    # x/D=2
    'surf00004': 'exp_xd3.csv',    # x/D=3
    'surf00005': 'exp_xd4.csv',    # x/D=4
    'surf00006': 'exp_xd5.csv',    # x/D=5
    'surf00007': 'exp_xd10.csv',   # x/D=10
    'surf00008': 'exp_xd15.csv'    # x/D=15
}

# Mapeamento entre superfícies e arquivos experimentais (segunda figura - flutuações)
exp_files_map2 = {
    'surf00001': 'exp2_xd004.csv',  # x/D=0.04
    'surf00002': 'exp2_xd1.csv',    # x/D=1
    'surf00003': 'exp2_xd2.csv',    # x/D=2
    'surf00004': 'exp2_xd3.csv',    # x/D=3
    'surf00005': 'exp2_xd4.csv',    # x/D=4
    'surf00006': 'exp2_xd5.csv',    # x/D=5
    'surf00007': 'exp2_xd10.csv',   # x/D=10
    'surf00008': 'exp2_xd15.csv'    # x/D=15
}

# Mapeamento entre superfícies e arquivos experimentais (terceira figura - flutuações v')
exp_files_map3 = {
    'surf00001': 'exp3_xd004.csv',  # x/D=0.04
    'surf00002': 'exp3_xd1.csv',    # x/D=1
    'surf00003': 'exp3_xd2.csv',    # x/D=2
    'surf00004': 'exp3_xd3.csv',    # x/D=3
    'surf00005': 'exp3_xd4.csv',    # x/D=4
    'surf00006': 'exp3_xd5.csv',    # x/D=5
    'surf00007': 'exp3_xd10.csv',   # x/D=10
    'surf00008': 'exp3_xd15.csv'    # x/D=15
}

# Mapeamento entre superfícies e arquivos experimentais (quarta figura - u'v'/Uc²)
exp_files_map4 = {
    'surf00001': 'exp4_xd004.csv',  # x/D=0.04
    'surf00002': 'exp4_xd1.csv',    # x/D=1
    'surf00003': 'exp4_xd2.csv',    # x/D=2
    'surf00004': 'exp4_xd3.csv',    # x/D=3
    'surf00005': 'exp4_xd4.csv',    # x/D=4
    'surf00006': 'exp4_xd5.csv',    # x/D=5
    'surf00007': 'exp4_xd10.csv',   # x/D=10
    'surf00008': 'exp4_xd15.csv'    # x/D=15
}

# Leitura dos arquivos .dat aplicando limites de linhas
def ler_probe_dat(file_path):
    """
    Lê os arquivos de sonda aplicando:
    - skiprows=linha_inicio_leitura
    - max_rows=(linha_fim_leitura-linha_inicio_leitura) quando linha_fim_leitura não é None
    """
    if linha_fim_leitura is None:
        return np.loadtxt(file_path, skiprows=linha_inicio_leitura)

    max_rows = int(linha_fim_leitura - linha_inicio_leitura)
    if max_rows <= 0:
        raise ValueError(
            f"linha_fim_leitura deve ser maior que linha_inicio_leitura. "
            f"Recebido: linha_inicio_leitura={linha_inicio_leitura}, linha_fim_leitura={linha_fim_leitura}"
        )
    return np.loadtxt(file_path, skiprows=linha_inicio_leitura, max_rows=max_rows)

# Função para processar uma superfície e retornar os dados
def processar_superficie(surf_name):
    """Processa os arquivos de uma superfície e retorna os dados normalizados"""
    
    # Buscar todos os arquivos da superfície
    pattern = os.path.join(probe_dir, f'{surf_name}_sonda*.dat')
    dat_files = sorted(glob.glob(pattern))
    
    if len(dat_files) == 0:
        print(f"Nenhum arquivo encontrado para {surf_name}")
        return None
    
    print(f"Processando {len(dat_files)} arquivos de {surf_name}...")
    
    # Lista para armazenar posições e médias de velocidade
    positions = []
    mean_velocities = []
    
    for file_path in dat_files:
        # Ler o arquivo a partir da linha especificada
        data = ler_probe_dat(file_path)
        
        # Extrair coluna 5 (yc) - posição (deve ser constante no arquivo)
        yc = data[:, 4]  # índice 4 = coluna 5 (0-indexed)
        position = yc[0]  # pegar o primeiro valor (todos devem ser iguais)
        
        # Extrair coluna 7 (u) - componente de velocidade
        u = data[:, 6]  # índice 6 = coluna 7 (0-indexed)
        
        # Calcular a média da velocidade
        mean_u = np.mean(u)
        
        positions.append(position)
        mean_velocities.append(mean_u)
    
    # Converter para arrays numpy
    positions = np.array(positions)
    mean_velocities = np.array(mean_velocities)
    
    # Ordenar por posição (caso os arquivos não estejam ordenados)
    sort_idx = np.argsort(positions)
    positions = positions[sort_idx]
    mean_velocities = mean_velocities[sort_idx]
    
    # Normalização do eixo x: r/D
    # onde r corresponde à coordenada y (yc) e D = 0.0825
    positions_normalized = (positions - deslocamento) / D
    
    # Centralizar os dados normalizados em 0 (subtrair a média)
    centro = np.mean(positions_normalized)
    positions_normalized_centered = positions_normalized - centro
    
    # Normalização do eixo y: U/U_c
    mean_velocities_normalized = mean_velocities / U_c
    
    return {
        'name': surf_name,
        'x': positions_normalized_centered,
        'y': mean_velocities_normalized
    }

# Função para processar uma superfície e calcular a norma das flutuações u'
def processar_superficie_fluctuacao(surf_name):
    """Processa os arquivos de uma superfície e retorna U'(RMS)/U_c
    onde U'(RMS) = sqrt(mean(u'²)) e u' = u - média(u)"""
    
    # Buscar todos os arquivos da superfície
    pattern = os.path.join(probe_dir, f'{surf_name}_sonda*.dat')
    dat_files = sorted(glob.glob(pattern))
    
    if len(dat_files) == 0:
        print(f"Nenhum arquivo encontrado para {surf_name}")
        return None
    
    print(f"Processando flutuações de {len(dat_files)} arquivos de {surf_name}...")
    
    # Lista para armazenar posições e normas das flutuações
    positions = []
    rms_fluctuations = []
    
    for file_path in dat_files:
        # Ler o arquivo a partir da linha especificada
        data = ler_probe_dat(file_path)
        
        # Extrair coluna 5 (yc) - posição (deve ser constante no arquivo)
        yc = data[:, 4]  # índice 4 = coluna 5 (0-indexed)
        position = yc[0]  # pegar o primeiro valor (todos devem ser iguais)
        
        # Extrair coluna 7 (u) - componente de velocidade
        u = data[:, 6]  # índice 6 = coluna 7 (0-indexed)
        
        # Calcular a média da velocidade neste ponto
        mean_u = np.mean(u)
        
        # Calcular a flutuação u' = u - média(u)
        u_prime = u - mean_u
        
        # Calcular u' ao quadrado
        u_prime_squared = u_prime**2
        
        # Calcular U'(RMS) = raiz quadrada da média de u' ao quadrado
        # U'(RMS) = sqrt(mean(u'²))
        U_prime_RMS = np.sqrt(np.mean(u_prime_squared))
        
        positions.append(position)
        rms_fluctuations.append(U_prime_RMS)
    
    # Converter para arrays numpy
    positions = np.array(positions)
    rms_fluctuations = np.array(rms_fluctuations)
    
    # Ordenar por posição (caso os arquivos não estejam ordenados)
    sort_idx = np.argsort(positions)
    positions = positions[sort_idx]
    rms_fluctuations = rms_fluctuations[sort_idx]
    
    # Normalização do eixo x: r/D
    # onde r corresponde à coordenada y (yc) e D = 0.0825
    positions_normalized = (positions - deslocamento) / D
    
    # Centralizar os dados normalizados em 0 (subtrair a média)
    centro = np.mean(positions_normalized)
    positions_normalized_centered = positions_normalized - centro
    
    # Normalização do eixo y: u'/U_c (norma das flutuações)
    rms_fluctuations_normalized = rms_fluctuations / U_c
    
    return {
        'name': surf_name,
        'x': positions_normalized_centered,
        'y': rms_fluctuations_normalized
    }

# Função para processar uma superfície e calcular a norma das flutuações v'
def processar_superficie_fluctuacao_v(surf_name):
    """Processa os arquivos de uma superfície e retorna v'(RMS)/U_c
    onde v'(RMS) = sqrt(mean(v'²)) e v' = v - média(v). Coluna v = coluna 8 (índice 7)."""
    
    pattern = os.path.join(probe_dir, f'{surf_name}_sonda*.dat')
    dat_files = sorted(glob.glob(pattern))
    
    if len(dat_files) == 0:
        print(f"Nenhum arquivo encontrado para {surf_name}")
        return None
    
    print(f"Processando flutuações v' de {len(dat_files)} arquivos de {surf_name}...")
    
    positions = []
    rms_fluctuations_v = []
    
    for file_path in dat_files:
        data = ler_probe_dat(file_path)
        yc = data[:, 4]
        position = yc[0]
        v = data[:, 7]   # coluna 8 = v (índice 7)
        mean_v = np.mean(v)
        v_prime = v - mean_v
        v_prime_squared = v_prime**2
        v_prime_RMS = np.sqrt(np.mean(v_prime_squared))
        positions.append(position)
        rms_fluctuations_v.append(v_prime_RMS)
    
    positions = np.array(positions)
    rms_fluctuations_v = np.array(rms_fluctuations_v)
    sort_idx = np.argsort(positions)
    positions = positions[sort_idx]
    rms_fluctuations_v = rms_fluctuations_v[sort_idx]
    positions_normalized = (positions - deslocamento) / D
    centro = np.mean(positions_normalized)
    positions_normalized_centered = positions_normalized - centro
    rms_fluctuations_v_normalized = rms_fluctuations_v / U_c
    
    return {
        'name': surf_name,
        'x': positions_normalized_centered,
        'y': rms_fluctuations_v_normalized
    }

# Função para processar uma superfície e calcular (u'*v')/(Uc*Uc)
def processar_superficie_uv_correlation(surf_name):
    """Processa os arquivos de uma superfície e retorna (u'*v')/(Uc*Uc)
    onde u' = u - mean(u), v' = v - mean(v), e (u'*v') = mean(u'*v') no tempo."""
    
    pattern = os.path.join(probe_dir, f'{surf_name}_sonda*.dat')
    dat_files = sorted(glob.glob(pattern))
    
    if len(dat_files) == 0:
        print(f"Nenhum arquivo encontrado para {surf_name}")
        return None
    
    print(f"Processando (u'v') de {len(dat_files)} arquivos de {surf_name}...")
    
    positions = []
    uv_correlation = []
    
    for file_path in dat_files:
        data = ler_probe_dat(file_path)
        yc = data[:, 4]
        position = yc[0]
        u = data[:, 6]   # coluna 7
        v = data[:, 7]   # coluna 8
        mean_u = np.mean(u)
        mean_v = np.mean(v)
        u_prime = u - mean_u
        v_prime = v - mean_v
        # (u'*v') = média temporal do produto
        mean_uv_prime = np.mean(u_prime * v_prime)
        positions.append(position)
        uv_correlation.append(mean_uv_prime)
    
    positions = np.array(positions)
    uv_correlation = np.array(uv_correlation)
    sort_idx = np.argsort(positions)
    positions = positions[sort_idx]
    uv_correlation = uv_correlation[sort_idx]
    positions_normalized = (positions - deslocamento) / D
    centro = np.mean(positions_normalized)
    positions_normalized_centered = positions_normalized - centro
    # Normalização: (u'*v')/(Uc*Uc)
    uv_correlation_normalized = uv_correlation / (U_c * U_c)
    
    return {
        'name': surf_name,
        'x': positions_normalized_centered,
        'y': uv_correlation_normalized
    }

# Detectar todas as superfícies disponíveis
all_files = glob.glob(os.path.join(probe_dir, 'surf*_sonda*.dat'))
surfaces = set()

for file_path in all_files:
    filename = os.path.basename(file_path)
    # Extrair o nome da superfície (ex: surf00001)
    match = re.match(r'(surf\d+)_', filename)
    if match:
        surfaces.add(match.group(1))

surfaces = sorted(list(surfaces))
print(f"\nSuperfícies encontradas: {surfaces}")

# Processar todas as superfícies
dados_superficies = []
for surf in surfaces:
    dados = processar_superficie(surf)
    if dados is not None:
        dados_superficies.append(dados)

# Ordenar: surf00008 no topo, surf00001 no fundo
dados_superficies_ordenados = []
outras_superficies = []

for dados in dados_superficies:
    if dados['name'] == 'surf00001':
        # surf00001 vai para o final
        surf00001_data = dados
    else:
        outras_superficies.append(dados)

# Ordenar outras superfícies em ordem decrescente (surf00008, surf00007, ..., surf00002)
outras_superficies.sort(key=lambda x: x['name'], reverse=True)

# Montar lista final: outras superfícies em ordem decrescente primeiro, surf00001 por último
# Isso fará com que surf00008 seja plotado no topo (axes[0]) e surf00001 no fundo (axes[-1])
dados_superficies_ordenados = outras_superficies.copy()
if 'surf00001_data' in locals():
    dados_superficies_ordenados.append(surf00001_data)

num_superficies = len(dados_superficies_ordenados)
print(f"\nGerando figura com {num_superficies} gráficos...")

# Criar figura com subplots empilhados verticalmente (formato quadrado)
fig, axes = plt.subplots(num_superficies, 1, figsize=(8, 8), sharex=True)

# Se houver apenas uma superfície, axes não será uma lista
if num_superficies == 1:
    axes = [axes]

# Mapeamento de superfícies para valores de x/D
xd_values = {
    'surf00001': 0.04,
    'surf00002': 1,
    'surf00003': 2,
    'surf00004': 3,
    'surf00005': 4,
    'surf00006': 5,
    'surf00007': 10,
    'surf00008': 15
}

# Plotar cada superfície (agora na ordem correta)
for idx, dados in enumerate(dados_superficies_ordenados):
    ax = axes[idx]
    
    # Plotar dados das sondas
    ax.plot(dados['x'], dados['y'], 'o', 
            markersize=3, label='Simulação', color='black')
    
    # Coletar valores de Y para calcular o range (incluindo dados experimentais se houver)
    y_values = dados['y'].copy()
    
    # Plotar dados experimentais se houver arquivo correspondente para esta superfície
    if dados['name'] in exp_files_map:
        exp_filename = exp_files_map[dados['name']]
        exp_file_path = os.path.join(exp_dir, exp_filename)
        
        if os.path.exists(exp_file_path):
            # Ler arquivo CSV com separador ';' e vírgula como decimal
            exp_data = pd.read_csv(exp_file_path, sep=';', decimal=',', header=None)
            exp_x = exp_data.iloc[:, 0].values
            exp_y = exp_data.iloc[:, 1].values
            
            ax.plot(exp_x, exp_y, '^', markersize=5, 
                   label=r'Fellouah $\mathit{et\ al.}$ (2009)', color='red', alpha=0.7)
            
            # Incluir dados experimentais no cálculo do range
            y_values = np.concatenate([y_values, exp_y])
    
    # Reduzir escala do eixo Y
    y_min = np.min(y_values)
    y_max = np.max(y_values)
    y_range = y_max - y_min
    # Adicionar uma margem de 10% acima e abaixo
    y_margin = y_range * 0.1
    ax.set_ylim(y_min - y_margin, y_max + y_margin)
    
    # Configurar grid
    ax.grid(True, alpha=0.3)
    
    # Adicionar legenda x/D para cada superfície
    if dados['name'] in xd_values:
        xd_val = xd_values[dados['name']]
        ax.text(0.02, 0.98, f'$x/D={xd_val}$', transform=ax.transAxes, 
                fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))

# Configurar labels dos eixos (apenas uma vez para toda a figura)
# Eixo y (lado esquerdo, centralizado)
fig.supylabel(r'$U/U_c$', fontsize=12)

# Eixo x (apenas no último subplot)
axes[-1].set_xlabel(r'$r/D$', fontsize=12)

# Criar uma única legenda para toda a figura
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
            markersize=5, label='Caso 3', linestyle='None'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='red', 
            markersize=5, label=r'Fellouah $\mathit{et\ al.}$ (2009)', linestyle='None', alpha=0.7)
]
fig.legend(handles=legend_elements, loc='upper right', fontsize=10, 
           bbox_to_anchor=(0.98, 0.98))

plt.tight_layout()

# Salvar o gráfico
output_file = 'velocity_profile_u_mean_all.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nGráfico salvo em: {output_file}")

# Mostrar o gráfico
plt.show()

print(f"\nProcessamento concluído!")

# ============================================================================
# Segunda figura: Norma das flutuações u'/U_c
# ============================================================================

print("\n" + "="*60)
print("Gerando figura das flutuações u'/U_c...")
print("="*60)

# Processar todas as superfícies para calcular flutuações
dados_superficies_fluctuacao = []
for surf in surfaces:
    dados = processar_superficie_fluctuacao(surf)
    if dados is not None:
        dados_superficies_fluctuacao.append(dados)

# Ordenar: surf00008 no topo, surf00001 no fundo
dados_fluctuacao_ordenados = []
outras_superficies_fluctuacao = []

for dados in dados_superficies_fluctuacao:
    if dados['name'] == 'surf00001':
        surf00001_data_fluctuacao = dados
    else:
        outras_superficies_fluctuacao.append(dados)

# Ordenar outras superfícies em ordem decrescente
outras_superficies_fluctuacao.sort(key=lambda x: x['name'], reverse=True)

# Montar lista final
dados_fluctuacao_ordenados = outras_superficies_fluctuacao.copy()
if 'surf00001_data_fluctuacao' in locals():
    dados_fluctuacao_ordenados.append(surf00001_data_fluctuacao)

num_superficies_fluctuacao = len(dados_fluctuacao_ordenados)
print(f"\nGerando figura com {num_superficies_fluctuacao} gráficos de flutuações...")

# Criar figura com subplots empilhados verticalmente (formato quadrado)
fig2, axes2 = plt.subplots(num_superficies_fluctuacao, 1, figsize=(8, 8), sharex=True)

# Se houver apenas uma superfície, axes não será uma lista
if num_superficies_fluctuacao == 1:
    axes2 = [axes2]

# Plotar cada superfície
for idx, dados in enumerate(dados_fluctuacao_ordenados):
    ax = axes2[idx]
    
    # Plotar dados das flutuações: U'(RMS)/U_c
    # dados['y'] contém os valores de U'(RMS) normalizados por U_c
    ax.plot(dados['x'], dados['y'], 'o', 
            markersize=3, label='3', color='black')
    
    # Plotar dados experimentais se houver arquivo correspondente para esta superfície
    if dados['name'] in exp_files_map2:
        exp_filename = exp_files_map2[dados['name']]
        exp_file_path = os.path.join(exp_dir2, exp_filename)
        
        if os.path.exists(exp_file_path):
            # Ler arquivo CSV com separador ';' e vírgula como decimal
            exp_data = pd.read_csv(exp_file_path, sep=';', decimal=',', header=None)
            exp_x = exp_data.iloc[:, 0].values
            exp_y = exp_data.iloc[:, 1].values
            
            ax.plot(exp_x, exp_y, '^', markersize=5, 
                   label=r'Fellouah $\mathit{et\ al.}$ (2009)', color='red', alpha=0.7)
    
    # Escala fixa do eixo Y: 0 a 0.3
    ax.set_ylim(0, 0.3)
    
    # Configurar grid
    ax.grid(True, alpha=0.3)
    
    # Adicionar legenda x/D para cada superfície
    if dados['name'] in xd_values:
        xd_val = xd_values[dados['name']]
        ax.text(0.02, 0.98, f'$x/D={xd_val}$', transform=ax.transAxes, 
                fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', 
                facecolor='wheat', alpha=0.5))

# Configurar labels dos eixos (apenas uma vez para toda a figura)
# Eixo y (lado esquerdo, centralizado)
fig2.supylabel(r"$u'/U_c$", fontsize=12)

# Eixo x (apenas no último subplot)
axes2[-1].set_xlabel(r'$r/D$', fontsize=12)

# Criar uma única legenda para toda a figura
legend_elements2 = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
            markersize=5, label='Caso 3', linestyle='None'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='red', 
            markersize=5, label=r'Fellouah $\mathit{et\ al.}$ (2009)', linestyle='None', alpha=0.7)
]
fig2.legend(handles=legend_elements2, loc='upper right', fontsize=10, 
           bbox_to_anchor=(0.98, 0.98))

plt.tight_layout()

# Salvar o gráfico
output_file2 = 'velocity_profile_u_fluctuation_all.png'
plt.savefig(output_file2, dpi=300, bbox_inches='tight')
print(f"\nGráfico salvo em: {output_file2}")

# Mostrar o gráfico
plt.show()

print(f"\nProcessamento das flutuações concluído!")

# ============================================================================
# Terceira figura: Norma das flutuações v'/U_c
# ============================================================================

print("\n" + "="*60)
print("Gerando figura das flutuações v'/U_c...")
print("="*60)

# Processar todas as superfícies para calcular flutuações de v
dados_superficies_fluctuacao_v = []
for surf in surfaces:
    dados = processar_superficie_fluctuacao_v(surf)
    if dados is not None:
        dados_superficies_fluctuacao_v.append(dados)

# Ordenar: surf00008 no topo, surf00001 no fundo
dados_fluctuacao_v_ordenados = []
outras_superficies_fluctuacao_v = []

for dados in dados_superficies_fluctuacao_v:
    if dados['name'] == 'surf00001':
        surf00001_data_fluctuacao_v = dados
    else:
        outras_superficies_fluctuacao_v.append(dados)

outras_superficies_fluctuacao_v.sort(key=lambda x: x['name'], reverse=True)
dados_fluctuacao_v_ordenados = outras_superficies_fluctuacao_v.copy()
if 'surf00001_data_fluctuacao_v' in locals():
    dados_fluctuacao_v_ordenados.append(surf00001_data_fluctuacao_v)

num_superficies_v = len(dados_fluctuacao_v_ordenados)
print(f"\nGerando figura com {num_superficies_v} gráficos de flutuações v'...")

fig3, axes3 = plt.subplots(num_superficies_v, 1, figsize=(8, 8), sharex=True)

if num_superficies_v == 1:
    axes3 = [axes3]

for idx, dados in enumerate(dados_fluctuacao_v_ordenados):
    ax = axes3[idx]
    ax.plot(dados['x'], dados['y'], 'o',
            markersize=3, label='Caso 3', color='black')

    if dados['name'] in exp_files_map3:
        exp_filename = exp_files_map3[dados['name']]
        exp_file_path = os.path.join(exp_dir3, exp_filename)

        if os.path.exists(exp_file_path):
            exp_data = pd.read_csv(exp_file_path, sep=';', decimal=',', header=None)
            exp_x = exp_data.iloc[:, 0].values
            exp_y = exp_data.iloc[:, 1].values
            ax.plot(exp_x, exp_y, '^', markersize=5,
                    label=r'Fellouah $\mathit{et\ al.}$ (2009)', color='red', alpha=0.7)

    # Limites dos eixos: X de -4 a 4, Y de 0 a 0.15
    ax.set_xlim(-4, 4)
    ax.set_ylim(0, 0.15)
    ax.grid(True, alpha=0.3)

    if dados['name'] in xd_values:
        xd_val = xd_values[dados['name']]
        ax.text(0.02, 0.98, f'$x/D={xd_val}$', transform=ax.transAxes,
                fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round',
                facecolor='wheat', alpha=0.5))

fig3.supylabel(r"$v'/U_c$", fontsize=12)
axes3[-1].set_xlabel(r'$r/D$', fontsize=12)

legend_elements3 = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='black',
            markersize=5, label='Caso 3', linestyle='None'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='red',
            markersize=5, label=r'Fellouah $\mathit{et\ al.}$ (2009)', linestyle='None', alpha=0.7)
]
fig3.legend(handles=legend_elements3, loc='upper right', fontsize=10,
            bbox_to_anchor=(0.98, 0.98))

plt.tight_layout()

output_file3 = 'velocity_profile_v_fluctuation_all.png'
plt.savefig(output_file3, dpi=300, bbox_inches='tight')
print(f"\nGráfico salvo em: {output_file3}")

plt.show()

print(f"\nProcessamento das flutuações v' concluído!")

# ============================================================================
# Quarta figura: (u'*v')/(Uc*Uc) vs r/D
# ============================================================================

print("\n" + "="*60)
print("Gerando figura (u'*v')/(Uc*Uc)...")
print("="*60)

dados_superficies_uv = []
for surf in surfaces:
    dados = processar_superficie_uv_correlation(surf)
    if dados is not None:
        dados_superficies_uv.append(dados)

dados_uv_ordenados = []
outras_superficies_uv = []
for dados in dados_superficies_uv:
    if dados['name'] == 'surf00001':
        surf00001_data_uv = dados
    else:
        outras_superficies_uv.append(dados)

outras_superficies_uv.sort(key=lambda x: x['name'], reverse=True)
dados_uv_ordenados = outras_superficies_uv.copy()
if 'surf00001_data_uv' in locals():
    dados_uv_ordenados.append(surf00001_data_uv)

num_superficies_uv = len(dados_uv_ordenados)
print(f"\nGerando figura com {num_superficies_uv} gráficos (u'*v')/(Uc*Uc)...")

fig4, axes4 = plt.subplots(num_superficies_uv, 1, figsize=(8, 8), sharex=True)

if num_superficies_uv == 1:
    axes4 = [axes4]

for idx, dados in enumerate(dados_uv_ordenados):
    ax = axes4[idx]
    ax.plot(dados['x'], dados['y'], 'o',
            markersize=3, label='Caso 3', color='black')

    if dados['name'] in exp_files_map4:
        exp_filename = exp_files_map4[dados['name']]
        exp_file_path = os.path.join(exp_dir4, exp_filename)
        if os.path.exists(exp_file_path):
            exp_data = pd.read_csv(exp_file_path, sep=';', decimal=',', header=None)
            exp_x = exp_data.iloc[:, 0].values
            exp_y = exp_data.iloc[:, 1].values
            ax.plot(exp_x, exp_y, '^', markersize=5,
                    label=r'Fellouah $\mathit{et\ al.}$ (2009)', color='red', alpha=0.7)

    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.02, 0.02)
    ax.grid(True, alpha=0.3)

    if dados['name'] in xd_values:
        xd_val = xd_values[dados['name']]
        ax.text(0.02, 0.98, f'$x/D={xd_val}$', transform=ax.transAxes,
                fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round',
                facecolor='wheat', alpha=0.5))

fig4.supylabel(r"$(u'v')/U_c^2$", fontsize=12)
axes4[-1].set_xlabel(r'$r/D$', fontsize=12)

legend_elements4 = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='black',
            markersize=5, label='Caso 3', linestyle='None'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='red',
            markersize=5, label=r'Fellouah $\mathit{et\ al.}$ (2009)', linestyle='None', alpha=0.7)
]
fig4.legend(handles=legend_elements4, loc='upper right', fontsize=10,
            bbox_to_anchor=(0.98, 0.98))

plt.tight_layout()

output_file4 = 'velocity_profile_uv_correlation_all.png'
plt.savefig(output_file4, dpi=300, bbox_inches='tight')
print(f"\nGráfico salvo em: {output_file4}")

plt.show()

print(f"\nProcessamento (u'*v')/(Uc*Uc) concluído!")
