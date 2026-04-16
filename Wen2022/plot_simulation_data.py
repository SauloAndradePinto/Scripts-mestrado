#!/usr/bin/env python3
"""
Script para extrair e plotar dados de simulação CFD do arquivo de log.
Cria 4 gráficos:
1. Número de partículas vs iteração
2. Uso de memória vs iteração  
3. Norma L∞ do divergente vs iteração (escala log)
4. Norma L2 do divergente vs iteração (escala log)
"""

import re
import matplotlib.pyplot as plt
import numpy as np

def extract_simulation_data(log_file_path):
    """
    Extrai dados da simulação do arquivo de log.
    
    Returns:
        tuple: (iterations, particles, memory, loo_divergent, l2_divergent, total_cells, cells_iterations, time_steps, time_step_iterations)
    """
    iterations = []
    particles = []
    memory = []
    loo_divergent = []
    l2_divergent = []
    total_cells = []
    cells_iterations = []
    time_steps = []
    time_step_iterations = []
    
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
    
    # Processar linha por linha para manter correspondência
    current_iteration = None
    temp_particles = None
    temp_memory = None
    temp_loo = None
    temp_l2 = None
    
    for i, line in enumerate(lines):
        # Procurar por iteração
        if 'ct =' in line:
            match = re.search(r'ct\s*=\s*(\d+)', line)
            if match:
                # Salvar dados da iteração anterior se existirem
                if current_iteration is not None:
                    any_value = False
                    if temp_particles is not None:
                        particles.append(temp_particles)
                        any_value = True
                    if temp_memory is not None:
                        memory.append(temp_memory)
                        any_value = True
                    if temp_loo is not None:
                        loo_divergent.append(temp_loo)
                        any_value = True
                    if temp_l2 is not None:
                        l2_divergent.append(temp_l2)
                        any_value = True

                    # Só adiciona iteração se houver ao menos um valor registrado
                    if any_value:
                        iterations.append(current_iteration)
                
                # Nova iteração
                current_iteration = int(match.group(1))
                # Reset dos dados para a nova iteração
                temp_particles = None
                temp_memory = None
                temp_loo = None
                temp_l2 = None
        
        # Procurar por dados relacionados à iteração atual
        if current_iteration is not None:
            # Log: "Number of particles = 0" ou "Number of particles =           0" (após "DPM: Operations")
            if 'Number of particles' in line and '=' in line:
                match = re.search(r'Number of particles\s*=\s*(\d+)', line)
                if match:
                    temp_particles = int(match.group(1))
            
            elif 'Memory usage' in line:
                # Captura valor e unidade (Mb/GB/Gb/MiB/GiB) e normaliza para GB
                match = re.search(r'Memory\s+usage\s*:\s*([\d.]+)\s*([MG])(?:i)?[bB]', line, flags=re.IGNORECASE)
                if match:
                    value = float(match.group(1))
                    unit = match.group(2).upper()
                    # Converte para GB se necessário
                    temp_memory = value if unit == 'G' else value / 1024.0
            
            elif 'Loo divergent =' in line:
                match = re.search(r'Loo divergent\s*=\s*([\d.E+-]+)', line)
                if match:
                    temp_loo = float(match.group(1))
            
            elif 'L2  divergent =' in line:
                match = re.search(r'L2\s+divergent\s*=\s*([\d.E+-]+)', line)
                if match:
                    temp_l2 = float(match.group(1))
        
        # Extrair dados de células totais (independente da estrutura de iteração)
        if 'number of total cells before:' in line:
            match = re.search(r'number of total cells before:\s*(\d+)', line)
            if match:
                # Encontrar a iteração mais próxima antes desta linha
                closest_iteration = None
                for j in range(i, -1, -1):
                    if 'ct =' in lines[j]:
                        ct_match = re.search(r'ct\s*=\s*(\d+)', lines[j])
                        if ct_match:
                            closest_iteration = int(ct_match.group(1))
                            break
                
                if closest_iteration is not None:
                    total_cells.append(int(match.group(1)))
                    cells_iterations.append(closest_iteration)
        
        # Extrair dados de time step (independente da estrutura de iteração)
        if 'Time step' in line and 'Seconds' in line:
            match = re.search(r'Time step\s*:\s*([\d.]+)\s*Seconds', line)
            if match:
                # Encontrar a iteração mais próxima antes desta linha
                closest_iteration = None
                for j in range(i, -1, -1):
                    if 'ct =' in lines[j]:
                        ct_match = re.search(r'ct\s*=\s*(\d+)', lines[j])
                        if ct_match:
                            closest_iteration = int(ct_match.group(1))
                            break
                
                if closest_iteration is not None:
                    time_steps.append(float(match.group(1)))
                    time_step_iterations.append(closest_iteration)
    
    # Salvar dados da última iteração
    if current_iteration is not None:
        any_value = False
        if temp_particles is not None:
            particles.append(temp_particles)
            any_value = True
        if temp_memory is not None:
            memory.append(temp_memory)
            any_value = True
        if temp_loo is not None:
            loo_divergent.append(temp_loo)
            any_value = True
        if temp_l2 is not None:
            l2_divergent.append(temp_l2)
            any_value = True
        
        if any_value:
            iterations.append(current_iteration)
    
    print(f"Encontrados {len(iterations)} iterações (com dados associados)")
    print(f"Encontrados {len(particles)} valores de partículas")
    print(f"Encontrados {len(memory)} valores de memória")
    print(f"Encontrados {len(loo_divergent)} valores L∞ divergent")
    print(f"Encontrados {len(l2_divergent)} valores L2 divergent")
    print(f"Encontrados {len(total_cells)} valores de células totais")
    print(f"Encontrados {len(time_steps)} valores de time step")
    
    # Garantir que todos os arrays usados nos gráficos principais tenham o mesmo tamanho.
    # Como o log atual não possui \"Number of particles =\", não usamos partículas para definir min_length.
    if len(iterations) == 0:
        print("Erro: Nenhum dado válido encontrado (sem iterações com dados associados)!")
        return [], [], [], [], [], [], [], [], []

    lengths_for_min = [len(iterations)]
    if len(memory) > 0:
        lengths_for_min.append(len(memory))
    if len(loo_divergent) > 0:
        lengths_for_min.append(len(loo_divergent))
    if len(l2_divergent) > 0:
        lengths_for_min.append(len(l2_divergent))

    min_length = min(lengths_for_min)
    
    iterations = iterations[:min_length]
    memory = memory[:min_length]
    loo_divergent = loo_divergent[:min_length]
    l2_divergent = l2_divergent[:min_length]
    # Alinha partículas com as iterações (um valor por iteração; log pode ter "Number of particles = 0" ou "=           0")
    particles = particles[:min_length]
    
    print(f"Dados ajustados para {min_length} pontos")
    
    return iterations, particles, memory, loo_divergent, l2_divergent, total_cells, cells_iterations, time_steps, time_step_iterations

def create_plots(iterations, particles, memory, loo_divergent, l2_divergent, total_cells, cells_iterations, time_steps, time_step_iterations):
    """
    Cria os 6 gráficos solicitados.
    """
    # Configurar a figura com 6 subplots (2x3)
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Análise da Simulação CFD', fontsize=16, fontweight='bold')
    
    # Gráfico 1: Número de partículas
    if particles and len(particles) == len(iterations):
        ax1.plot(iterations, particles, 'bo', markersize=2)
        ax1.set_xlabel('Iteração')
        ax1.set_ylabel('Número de Partículas')
        ax1.set_title('Número de Partículas vs Iteração')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, max(iterations))
    else:
        ax1.text(0.5, 0.5, 'Nenhum dado de partículas encontrado',
                 ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('Número de Partículas vs Iteração')
    
    # Gráfico 2: Uso de memória
    ax2.plot(iterations, memory, 'ro', markersize=2)
    ax2.set_xlabel('Iteração')
    ax2.set_ylabel('Uso de Memória (Gb)')
    ax2.set_title('Uso de Memória vs Iteração')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, max(iterations))
    
    # Gráfico 3: Norma L∞ do divergente (escala log)
    ax3.semilogy(iterations, loo_divergent, 'go', markersize=2)
    ax3.set_xlabel('Iteração')
    ax3.set_ylabel('L∞ Divergent (escala log)')
    ax3.set_title('Norma L∞ do Divergente vs Iteração')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, max(iterations))
    
    # Gráfico 4: Norma L2 do divergente (escala log)
    ax4.semilogy(iterations, l2_divergent, 'mo', markersize=2)
    ax4.set_xlabel('Iteração')
    ax4.set_ylabel('L2 Divergent (escala log)')
    ax4.set_title('Norma L2 do Divergente vs Iteração')
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0, max(iterations))
    
    # Gráfico 5: Número total de células
    if total_cells and cells_iterations:
        ax5.plot(cells_iterations, total_cells, 'co', markersize=2)
        ax5.set_xlabel('Iteração')
        ax5.set_ylabel('Número Total de Células')
        ax5.set_title('Número Total de Células vs Iteração')
        ax5.grid(True, alpha=0.3)
        ax5.set_xlim(0, max(cells_iterations))
    else:
        ax5.text(0.5, 0.5, 'Nenhum dado de células encontrado', 
                ha='center', va='center', transform=ax5.transAxes)
        ax5.set_title('Número Total de Células vs Iteração')
    
    # Gráfico 6: Time step
    if time_steps and time_step_iterations:
        ax6.plot(time_step_iterations, time_steps, 'o', color='orange', markersize=2)
        ax6.set_xlabel('Iteração')
        ax6.set_ylabel('Time Step (Segundos)')
        ax6.set_title('Time Step vs Iteração')
        ax6.grid(True, alpha=0.3)
        ax6.set_xlim(0, max(time_step_iterations))
    else:
        ax6.text(0.5, 0.5, 'Nenhum dado de time step encontrado', 
                ha='center', va='center', transform=ax6.transAxes)
        ax6.set_title('Time Step vs Iteração')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Salvar a figura
    plt.savefig('simulation_analysis.png', dpi=300, bbox_inches='tight')
    print("Gráficos salvos em 'simulation_analysis.png'")
    
    # Mostrar os gráficos
    plt.show()

def main():
    """
    Função principal que executa a análise.
    """
    log_file = 'log'
    
    print("Extraindo dados do arquivo de log...")
    iterations, particles, memory, loo_divergent, l2_divergent, total_cells, cells_iterations, time_steps, time_step_iterations = extract_simulation_data(log_file)
    
    # Verificar se temos dados suficientes
    if len(iterations) == 0:
        print("Erro: Nenhuma iteração encontrada no arquivo de log!")
        return
    
    print(f"\nDados extraídos:")
    print(f"Iterações: {iterations}")
    print(f"Partículas: {particles}")
    print(f"Memória: {memory}")
    print(f"L∞ Divergent: {loo_divergent}")
    print(f"L2 Divergent: {l2_divergent}")
    print(f"Células totais: {total_cells}")
    print(f"Iterações das células: {cells_iterations}")
    print(f"Time steps: {time_steps}")
    print(f"Iterações dos time steps: {time_step_iterations}")
    
    print("\nCriando gráficos...")
    create_plots(iterations, particles, memory, loo_divergent, l2_divergent, total_cells, cells_iterations, time_steps, time_step_iterations)
    
    print("\nAnálise concluída!")

if __name__ == "__main__":
    main()
