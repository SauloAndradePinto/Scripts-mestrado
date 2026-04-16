import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import re

# Diretório com os arquivos de sonda da simulação Wen2022
probe_dir = "outputAtom5/probe_points"

# Parâmetros de leitura das sondas
# Número de linhas a pular no início do arquivo (0 = começar da primeira linha)
# A primeira linha é cabeçalho "VARIABLES=..."
linha_inicio_leitura = 1

# Linha final (1-indexada, inclusive) para limitar a leitura do arquivo.
# Se None, lê até o fim do arquivo.
linha_fim_leitura = None

# Parâmetros de normalização (ajuste conforme necessário para o caso Wen2022)
# Se não quiser normalizar, deixe D = 1.0, deslocamento = 0.0, U_c = 1.0
D = 0.01
deslocamento = 0.00625
U_c = 48.0


def ler_probe_dat(file_path: str) -> np.ndarray:
    """Lê arquivo de sonda `.dat` aplicando limites de linhas."""
    if linha_fim_leitura is None:
        return np.loadtxt(file_path, skiprows=linha_inicio_leitura)

    max_rows = int(linha_fim_leitura - linha_inicio_leitura)
    if max_rows <= 0:
        raise ValueError(
            f"linha_fim_leitura deve ser maior que linha_inicio_leitura. "
            f"Recebido: linha_inicio_leitura={linha_inicio_leitura}, linha_fim_leitura={linha_fim_leitura}"
        )
    return np.loadtxt(file_path, skiprows=linha_inicio_leitura, max_rows=max_rows)


def processar_superficie_media(surf_name: str):
    """Processa todos os arquivos de uma superfície e retorna U_média/U_c vs r/D."""
    pattern = os.path.join(probe_dir, f"{surf_name}_sonda*.dat")
    dat_files = sorted(glob.glob(pattern))

    if len(dat_files) == 0:
        print(f"Nenhum arquivo encontrado para {surf_name}")
        return None

    print(f"Processando média de {len(dat_files)} arquivos de {surf_name}...")

    positions = []
    mean_velocities = []

    for file_path in dat_files:
        data = ler_probe_dat(file_path)

        # Coluna 5 (índice 4) = yc (posição)
        yc = data[:, 4]
        position = yc[0]

        # Coluna 7 (índice 6) = u
        u = data[:, 6]

        mean_u = np.mean(u)
        positions.append(position)
        mean_velocities.append(mean_u)

    positions = np.array(positions)
    mean_velocities = np.array(mean_velocities)

    sort_idx = np.argsort(positions)
    positions = positions[sort_idx]
    mean_velocities = mean_velocities[sort_idx]

    # Normalização em r/D
    positions_normalized = (positions - deslocamento) / D
    centro = np.mean(positions_normalized)
    positions_normalized_centered = positions_normalized - centro

    # Normalização em U/U_c
    mean_velocities_normalized = mean_velocities / U_c

    return {
        "name": surf_name,
        "x": positions_normalized_centered,
        "y": mean_velocities_normalized,
    }


def processar_superficie_flutuacao(surf_name: str):
    """Processa todos os arquivos de uma superfície e retorna u'_RMS/U_c vs r/D."""
    pattern = os.path.join(probe_dir, f"{surf_name}_sonda*.dat")
    dat_files = sorted(glob.glob(pattern))

    if len(dat_files) == 0:
        print(f"Nenhum arquivo encontrado para {surf_name}")
        return None

    print(f"Processando flutuações de {len(dat_files)} arquivos de {surf_name}...")

    positions = []
    rms_fluctuations = []

    for file_path in dat_files:
        data = ler_probe_dat(file_path)

        yc = data[:, 4]
        position = yc[0]

        u = data[:, 6]
        mean_u = np.mean(u)
        u_prime = u - mean_u
        u_prime_squared = u_prime**2
        u_prime_rms = np.sqrt(np.mean(u_prime_squared))

        positions.append(position)
        rms_fluctuations.append(u_prime_rms)

    positions = np.array(positions)
    rms_fluctuations = np.array(rms_fluctuations)

    sort_idx = np.argsort(positions)
    positions = positions[sort_idx]
    rms_fluctuations = rms_fluctuations[sort_idx]

    positions_normalized = (positions - deslocamento) / D
    centro = np.mean(positions_normalized)
    positions_normalized_centered = positions_normalized - centro

    rms_fluctuations_normalized = rms_fluctuations / U_c

    return {
        "name": surf_name,
        "x": positions_normalized_centered,
        "y": rms_fluctuations_normalized,
    }


def detectar_superficies():
    """Retorna lista ordenada de superfícies disponíveis em `probe_dir`."""
    all_files = glob.glob(os.path.join(probe_dir, "surf*_sonda*.dat"))
    surfaces = set()

    for file_path in all_files:
        filename = os.path.basename(file_path)
        match = re.match(r"(surf\d+)_", filename)
        if match:
            surfaces.add(match.group(1))

    surfaces = sorted(list(surfaces))
    print(f"Superfícies encontradas: {surfaces}")
    return surfaces


def ordenar_superficies(dados_superficies):
    """Ordena superfícies para que a maior (ex: surf00008) fique no topo e a menor no fundo."""
    if not dados_superficies:
        return []

    outras_superficies = []
    primeira_superficie = None

    for dados in dados_superficies:
        if primeira_superficie is None:
            primeira_superficie = dados
        else:
            outras_superficies.append(dados)

    outras_superficies.sort(key=lambda x: x["name"], reverse=True)

    ordenadas = outras_superficies.copy()
    if primeira_superficie is not None:
        ordenadas.append(primeira_superficie)

    return ordenadas


def plotar_perfil_medio(dados_superficies_ordenados):
    num_superficies = len(dados_superficies_ordenados)
    if num_superficies == 0:
        print("Nenhuma superfície para plotar perfil médio.")
        return

    fig, axes = plt.subplots(num_superficies, 1, figsize=(8, 8), sharex=True)
    if num_superficies == 1:
        axes = [axes]

    # Mapeamento surf -> rótulo em x/D_G (apenas 6 superfícies)
    label_map = {
        "surf00001": r"$x/D_G=0,5$",
        "surf00002": r"$x/D_G=1,0$",
        "surf00003": r"$x/D_G=1,5$",
        "surf00004": r"$x/D_G=2,0$",
        "surf00005": r"$x/D_G=2,5$",
        "surf00006": r"$x/D_G=3,0$",
    }

    # Escala comum de Y para todos os subgráficos (mesma escala em cima e embaixo)
    all_y = np.concatenate([dados["y"] for dados in dados_superficies_ordenados])
    y_min_global = np.min(all_y)
    y_max_global = np.max(all_y)
    y_range_global = y_max_global - y_min_global
    y_margin_global = 0.1 * y_range_global if y_range_global > 0 else 0.05

    for idx, dados in enumerate(dados_superficies_ordenados):
        ax = axes[idx]
        ax.plot(dados["x"], dados["y"], "o", markersize=3, color="black", label="Simulação")

        ax.set_ylim(y_min_global - y_margin_global, y_max_global + y_margin_global)
        ax.grid(True, alpha=0.3)

        # Legenda no canto INFERIOR esquerdo do subplot (primeira figura)
        label = label_map.get(dados["name"], dados["name"])

        # Legenda no canto SUPERIOR esquerdo do subplot (segunda figura)
        ax.text(
            0.02,
            0.98,
            label,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

    fig.supylabel(r"$U/U_c$", fontsize=12)
    axes[-1].set_xlabel(r"$r/D_G$", fontsize=12)

    fig.tight_layout()
    output_file = "velocity_profile_Wen2022_u_mean_all.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Gráfico de perfil médio salvo em: {output_file}")


def plotar_flutuacao(dados_flutuacao_ordenados):
    num_superficies = len(dados_flutuacao_ordenados)
    if num_superficies == 0:
        print("Nenhuma superfície para plotar flutuações.")
        return

    fig, axes = plt.subplots(num_superficies, 1, figsize=(8, 8), sharex=True)
    if num_superficies == 1:
        axes = [axes]

    label_map = {
        "surf00001": r"$x/D_G=0,5$",
        "surf00002": r"$x/D_G=1,0$",
        "surf00003": r"$x/D_G=1,5$",
        "surf00004": r"$x/D_G=2,0$",
        "surf00005": r"$x/D_G=2,5$",
        "surf00006": r"$x/D_G=3,0$",
    }

    # Escala comum de Y para todos os subgráficos (mesma escala em cima e embaixo)
    all_y = np.concatenate([dados["y"] for dados in dados_flutuacao_ordenados])
    y_min_global = np.min(all_y)
    y_max_global = np.max(all_y)
    y_range_global = y_max_global - y_min_global
    y_margin_global = 0.1 * y_range_global if y_range_global > 0 else 0.05

    for idx, dados in enumerate(dados_flutuacao_ordenados):
        ax = axes[idx]
        ax.plot(dados["x"], dados["y"], "o", markersize=3, color="black", label="Simulação")

        ax.set_ylim(y_min_global - y_margin_global, y_max_global + y_margin_global)
        ax.grid(True, alpha=0.3)

        label = label_map.get(dados["name"], dados["name"])

        ax.text(
            0.02,
            0.02,
            label,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="bottom",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

    fig.supylabel(r"$u'/U_c$", fontsize=12)
    axes[-1].set_xlabel(r"$r/D$", fontsize=12)

    fig.tight_layout()
    output_file = "velocity_profile_Wen2022_u_fluctuation_all.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Gráfico de flutuações salvo em: {output_file}")


def main():
    surfaces = detectar_superficies()

    # Perfil médio
    dados_superficies = []
    for surf in surfaces:
        dados = processar_superficie_media(surf)
        if dados is not None:
            dados_superficies.append(dados)

    dados_superficies_ordenados = ordenar_superficies(dados_superficies)
    plotar_perfil_medio(dados_superficies_ordenados)

    # Flutuações
    dados_flutuacao = []
    for surf in surfaces:
        dados = processar_superficie_flutuacao(surf)
        if dados is not None:
            dados_flutuacao.append(dados)

    dados_flutuacao_ordenados = ordenar_superficies(dados_flutuacao)
    plotar_flutuacao(dados_flutuacao_ordenados)


if __name__ == "__main__":
    main()

