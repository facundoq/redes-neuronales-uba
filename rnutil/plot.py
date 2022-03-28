import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



def plot_regresion_lineal_univariada(w,b,x,y,x_label,y_label,title=""):
    # genero una ventana de dibujo con una sola zona de dibujo (1,1)
    f,ax_data=plt.subplots(1,1)
    # dibujo el conjunto de datos como pares x,y y color azul
    ax_data.scatter(x, y, color="blue")
    # establezco el titulo principal
    f.suptitle(f"{title}")
    # Dibujo la recta dada por los parámetros del modelo (w,b)
    x_pad = 10
    min_x, max_x = x.min() - x_pad, x.max() + x_pad
    ax_data.plot([min_x, max_x], [min_x * w + b, max_x * w + b], color="red",label=f"w={w:.5f}, b={b:.5f}")
    # agrego una leyenda con la etiqueta del parametro `label`
    ax_data.legend()
    # Establezco las etiquetas de los ejes x e y
    ax_data.set_xlabel(x_label)
    ax_data.set_ylabel(y_label)


def add_legends(ax_data,mx,my,b,mean_error):
    model = patches.Patch(color='red', label='Modelo: y=x1*{:.2f}+x2*{:.2f}+{:.2f}'.format(mx,my,b))
    data = patches.Patch(color='blue', label='Datos')
    handles=[model,data]
    label='$E = \\frac{1}{n}  \sum_i^n E_i = $  %.2f' % (mean_error)
    error_patch = patches.Patch(color='black', label=label)
    handles.append(error_patch)
    ax_data.legend(handles=handles,fontsize=8)

def mean_error(w,b,x1,x2,y):
    y_pred = w[0]*x1+w[1]*x2+b
    return np.mean( (y_pred-y)**2)
def plot_regresion_lineal(w,b,x1,x2,y,x1_label,x2_label,y_label,title=""):
    # genero una ventana de dibujo con una sola zona de dibujo (1,1)
    # que permita graficos en 3D
    figure = plt.figure(figsize=(10, 10), dpi=100)
    ax_data = figure.add_subplot(1, 1, 1, projection='3d')

    #dibujo el dataset en 3D (x1,x2,y)
    # x1=x[:,0]
    # x2=x[:,1]
    
    ax_data.scatter(x1,x2, y, color="blue")
    figure.suptitle(title)

    # Dibujo el plano dado por los parametros del modelo (w,b)
    # Este codigo probablemente no sea facil de entender
    # si no tenes experiencia con calculos en 3D
    detail = 0.05
    # genero coordenadas x,y de a pares, las llamo xx e yy
    xr = np.arange(x1.min(), x1.max(), detail)
    yr = np.arange(x2.min(), x2.max(), detail)
    xx, yy = np.meshgrid(xr, yr)
    # calculo las coordenadas z en base a xx, yy, y el modelo (w,b)
    zz = xx * w[0] + yy * w[1] + b
    # dibujo la superficie dada por los puntos (xx,yy,zz)
    surf = ax_data.plot_surface(xx, yy, zz, cmap='Reds', alpha=0.5, linewidth=0, antialiased=True)

    # Establezco las etiquetas de los ejes
    ax_data.set_xlabel(x1_label)#"x1 (Horas estudiadas)")
    ax_data.set_ylabel(x2_label)#"x2 (Promedio)")
    ax_data.set_zlabel(y_label)#"y (Nota)")
    # Establezco el titulo del grafico
    ax_data.set_title(title)
    add_legends(ax_data,w[0],w[1],b,mean_error(w,b,x1,x2,y))




# imprime los puntos para un dataset bidimensional junto con la frontera de decisión del modelo
def plot_regresion_logistica2D(modelo, x, y,title="",detail=0.1):

    assert x.shape[1]==2,f"x debe tener solo dos variables de entrada (tiene {x.shape[1]})"
    # nueva figura
    plt.figure()
    # gráfico con la predicción aprendida
    x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
    y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, detail),
                         np.arange(y_min, y_max, detail))

    Z = np.c_[xx.ravel(), yy.ravel()]

    Z = modelo.predict(Z)
    Z = Z.argmax(axis=1)  # para Keras
    titulo = f"{title}: regiones de cada clase"
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.3)  # ,  cmap='RdBu')
    plt.colorbar()
    plt.title(titulo)

    # puntos con las clases
    plt.scatter(x[:, 0], x[:, 1], c=y)


def plot_loss(loss_history):
    plt.figure()
    epochs = np.arange(1,len(loss_history)+1)
    plt.plot(epochs,loss_history)
    plt.xlabel("Época")
    plt.ylabel("Error")
    
