import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
# cambio la font para que se vean los titulos más proporcionados
rcParams.update({'font.size': 6})

df = pd.read_csv('examenes.csv', header=False)
x = df['examen0']
y = df['examen1']
z = df['examen2']
w = df['examen3']
d = df['diagnostico'].apply(lambda x: 'g' if x == 'sano' else 'r')

# # EX0 vs EX1
plt.subplot(321)
plt.scatter(x, y, color=d)
fit = np.polyfit(x, y, 2)
p = np.poly1d(fit)
plt.plot(x, p(x))
plt.title('Examen0 vs Examen1')
# EX0 vs EX2
plt.subplot(322)
plt.scatter(x, z, color=d)
fit = np.polyfit(x, z, 2)
p = np.poly1d(fit)
plt.plot(x, p(z))
plt.title('Examen0 vs Examen2')
# EX0 vs EX3
plt.subplot(323)
plt.scatter(x, w, color=d)
fit = np.polyfit(x, w, 2)
p = np.poly1d(fit)
plt.plot(x, p(x))
plt.title('Examen0 vs Examen3')
# EX1 vs EX2
plt.subplot(324)
plt.scatter(y, z, color=d)
fit = np.polyfit(y, z, 2)
p = np.poly1d(fit)
plt.plot(y, p(y))
plt.title('Examen1 vs Examen2')
# EX1 vs EX3
plt.subplot(325)
plt.scatter(y, w, color=d)
fit = np.polyfit(y, w, 2)
p_bueno = np.poly1d(fit)
plt.plot(y, p_bueno(y))
plt.title('Examen1 vs Examen3')
# EX2 vs EX3
plt.subplot(326)
plt.scatter(z, w, color=d)
fit = np.polyfit(z, w, 2)
p = np.poly1d(fit)
plt.plot(z, p(z))
plt.title('Examen2 vs Examen3')

# mostramos los 6 graficos al principio
plt.show()


mejor_x = y
mejor_y = w
# Elejimos y, w q son examen 1 vs 3

nuevos = pd.read_csv('pacientes_nuevos.csv', header=False)
x = nuevos['examen1']
y = nuevos['examen3']
n = nuevos['id']
# el criterio es que si el exmane 3 está bajo la curva de aproximación
# va a ser sano

# Cambio la font nuevamente para que se vea el título
rcParams.update({'font.size': 15})
for i in range(len(x)):
    plt.scatter(mejor_x, mejor_y, color=d)
    plt.plot(mejor_x, p_bueno(mejor_x))
    y_curva = p_bueno(x[i])
    y_real = y[i]
    if y_real > y_curva:
        print('Paciente %s está enfermo' % n[i])
    else:
        print('Paciente %s está sano' % n[i])
    plt.title('Diagnóstico según ajuste')
    plt.plot(x[i], y[i], 'ko')
    # Mostramos cada grafico a la vez que se imprime el diagnóstico
    plt.show()
