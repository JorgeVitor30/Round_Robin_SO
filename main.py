from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from time import sleep

class Process:
  def __init__(self, name, burst_time):
    self.name = name
    self.burst_time = burst_time
    self.remaining_time = burst_time
    self.init_time = datetime.now()
    self.wait_times = []  # TEMPO MÉDIO DE ESPERA
    self.start = datetime.now()
    self.finish = 0  # TEMPO MÉDIO DE RETORNO
    self.finished = False

  def execute(self, quantum):
    self.wait_times.append(datetime.now() - self.init_time)
    
    if quantum > self.remaining_time:
      sleep(1/self.remaining_time)
    else:
      sleep(1/quantum)
      
    self.remaining_time -= quantum
    self.init_time = datetime.now()

    if self.remaining_time <= 0:
      self.finish = datetime.now() - self.start
      self.finished = True
      return self.finished

    return self.finished
      

  def get_wait_time(self):
    return sum(self.wait_times, timedelta(0, 0))

class RoundRobin:
  def __init__(self, quantum, processes, troughput):
    self.troughput = troughput
    self.quantum = quantum
    self.processes = processes
    self.concluded = []
    self.return_time = dict()

  def escalonamento(self):
    while self.processes:
      current_process = self.processes.pop()  # Remove o primeiro processo da lista
      if self.execute_process(current_process):
        self.concluded.append(current_process)
      else:
        self.processes.insert(0, current_process)
    print(self.return_metrics())
    metrics = Metrics(self.concluded, self.troughput, self.quantum)
    return metrics.avg_return_time(), metrics.avg_wait_time(), metrics.get_troughput(), metrics.get_quantum()

  def execute_process(self, process):
    if process.execute(quantum=self.quantum):
      self.return_time[process.name] = process.finish
      return True

  def return_metrics(self):
    troughput = [x for x in self.concluded if x.finish <= self.troughput]
    for process in self.concluded:
      print(f"nome: {process.name} -Tempo de espera: {process.get_wait_time()} - Tempo de retorno: {process.finish}")
    print(f'Vazão: {len(troughput)}')

class Metrics:
  def __init__(self, concludeds, troughput, quantum) -> None:
    self.concludeds = concludeds
    self.troughput = troughput
    self.quantum = quantum

  def __avg(self, times):
    time_delta = sum(times, timedelta(0,0)) / len(times)
    return time_delta.total_seconds()

  def avg_return_time(self):
    return self.__avg([p.finish for p in self.concludeds])
  
  def avg_wait_time(self):
    return self.__avg([p.get_wait_time() for p in self.concludeds])

  def get_troughput(self):
    return len([x for x in self.concludeds if x.finish <= self.troughput])

  def get_quantum(self):
    return self.quantum
    

# TESTE 1
troughput_time = timedelta(seconds=0.02)

processes_list = [Process("P1", 200), Process("P2", 1000), Process("P3", 100)]
quantum_time = 50

scheduler = RoundRobin(quantum_time, processes_list, troughput_time)
metrics1 = scheduler.escalonamento()


# TESTE 2
troughput_time = timedelta(seconds=0.02)

processes_list = [Process("P1", 200), Process("P2", 1000), Process("P3", 100)]
quantum_time = 230

scheduler = RoundRobin(quantum_time, processes_list, troughput_time)
metrics2 = scheduler.escalonamento()


# TESTE 3
troughput_time = timedelta(seconds=0.02)

processes_list = [Process("P1", 200), Process("P2", 1000), Process("P3", 100)]
quantum_time = 130

scheduler = RoundRobin(quantum_time, processes_list, troughput_time)
metrics3 = scheduler.escalonamento()


# TESTE 4
troughput_time = timedelta(milliseconds=20000)

processes_list = [Process("P1", 200), Process("P2", 1000), Process("P3", 100)]
quantum_time = 300

scheduler = RoundRobin(quantum_time, processes_list, troughput_time)
metrics4 = scheduler.escalonamento()


# TESTE 5
troughput_time = timedelta(milliseconds=20000)

processes_list = [Process("P1", 200), Process("P2", 1000), Process("P3", 100)]
quantum_time = 350

scheduler = RoundRobin(quantum_time, processes_list, troughput_time)
metrics5 = scheduler.escalonamento()


# TESTE 6
troughput_time = timedelta(milliseconds=20000)

processes_list = [Process("P1", 200), Process("P2", 1000), Process("P3", 100)]
quantum_time = 500

scheduler = RoundRobin(quantum_time, processes_list, troughput_time)
metrics6 = scheduler.escalonamento()



#-=-=-=-===============------------------------=-=-=

dados = {
  "quantum": [metrics3[3], metrics2[3], metrics1[3], metrics4[3], metrics5[3], metrics6[3]],
  "tempo_medio_retorno": [metrics3[0], metrics2[0], metrics1[0], metrics4[0], metrics5[0], metrics6[0]],
  "tempo_medio_espera": [metrics3[1], metrics2[1], metrics1[1], metrics4[1], metrics5[1], metrics6[1]],
  "vazao": [metrics3[2], metrics2[2], metrics1[2], metrics4[2], metrics5[2], metrics6[2]]
}

print(dados)

dados_ordenados = sorted(zip(dados['tempo_medio_retorno'], dados['tempo_medio_espera'], dados['quantum']))

tempo_medio_retorno_ordenado, tempo_medio_espera_ordenado, quantum_ordenado = zip(*dados_ordenados)

# Linhas conectando os pontos
plt.plot(tempo_medio_retorno_ordenado, quantum_ordenado, color='blue', alpha=0.5, label='Tempo Médio de Retorno')
plt.plot(tempo_medio_espera_ordenado, quantum_ordenado, color='green', alpha=0.5, label='Tempo Médio de Espera')

# Pontos nos dados
plt.scatter(tempo_medio_retorno_ordenado, quantum_ordenado, color='blue', alpha=0.5)
plt.scatter(tempo_medio_espera_ordenado, quantum_ordenado, color='green', alpha=0.5)

plt.title('Relação entre Quantum e Tempos Médios')
plt.xlabel('Tempo Médio')
plt.ylabel('Quantum')
plt.legend()
plt.grid(True)
plt.show()


import numpy as np

scale_factor = 1.5  # Ajuste conforme necessário


scaled_avg_return_times = [val / scale_factor for val in sorted(dados['tempo_medio_retorno'], reverse=True)]
scaled_avg_wait_times = [val / scale_factor for val in sorted(dados['tempo_medio_espera'], reverse=True)]

# Configurações do gráfico
bar_width = 0.35
index = np.arange(len(dados['quantum']))

# Plotagem do gráfico de barras agrupadas
plt.figure(figsize=(10, 6))
bars1 = plt.bar(index - bar_width/2, scaled_avg_wait_times, width=bar_width, color='blue', label='Tempo Médio de Espera')
bars2 = plt.bar(index + bar_width/2, scaled_avg_return_times, width=bar_width, color='green', label='Tempo Médio de Retorno')

# Configurações adicionais do gráfico
plt.xlabel('Quantum')
plt.ylabel('Tempo Médio')
plt.title('Comparação entre Tempo Médio de Retorno e Espera por Quantum')
plt.xticks(index, sorted(dados['quantum']))
plt.legend()
plt.tight_layout()
plt.show()


import plotly.graph_objects as go


fig = go.Figure()

# Adicionando os pontos de dispersão
fig.add_trace(go.Scatter(x=dados['quantum'], y=dados['vazao'], mode='markers', name='Vazão x Quantum', marker=dict(size=10)))

# Adicionando títulos e rótulos aos eixos
fig.update_layout(title='Relação entre Vazão e Quantum',
                  xaxis_title='Quantum',
                  yaxis_title='Vazão')

# Exibindo o gráfico
fig.show()