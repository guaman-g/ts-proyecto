from django.http import HttpResponse

from django.template import Template,Context
from django.template.loader import get_template
from django.shortcuts import render


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, integrate, Eq, solve
import random

def Inicio(request):
   return render(request, "index.html", {})

def Congruencial (request):
    return render(request, "congruencial.html", {})
 
def Congruencialr (request):
    x0 = int(request.POST["numero"])
    a = int(request.POST["multiplicador"])
    c = int(request.POST["incremento"])
    m = int(request.POST["modulo"])
    n = int(request.POST["iteraciones"])   
    x = [1] * n
    r = [0.1] * n  
    for i in range(0, n):
      x[i] = ((a*x0)+c) % m
      x0 = x[i]
      r[i] = x0 / m
    # llenamos nuestro DataFrame
    d = {'Xn': x, 'ri': r }
    df = pd.DataFrame(data=d)
    html = df.to_html(classes='table table-sm table-warning')
    x1=df['ri']
    plt.plot(x1)            #grafico
    plt.title("Gráfico")
    plt.xlabel("Serie")
    plt.ylabel("Aleatorios")
    plt.savefig('static/img/MetodoCongruencialLineal/imagen.png')
    plt.close()    
    return render(request, "congruencialr.html", {'tabla':html})

def Congruencialm (request):
    return render(request, "congruencialm.html", {})

def Congruencialmr (request):
    Xn = int(request.POST["numero"])
    a = int(request.POST["multiplicador"])
    m = int(request.POST["modulo"])
    n = int(request.POST["iteraciones"])   
    x = [1] * n
    r = [0.1] * n  
    for i in range(0, n):
      x[i] = (a*Xn) % m
      Xn = x[i]
      r[i] = Xn / m
    # llenamos nuestro DataFrame
    d = {'Xn': x, 'ri': r }
    df = pd.DataFrame(data=d)
    html = df.to_html(classes='table table-sm table-warning')
    x1=df['ri']
    plt.plot(x1)            #grafico
    plt.title("Gráfico")
    plt.xlabel("Serie")
    plt.ylabel("Aleatorios")
    plt.savefig('static/img/MetodoCongruencialLineal/imagen.png')
    plt.close()    
    return render(request, "congruencialmr.html", {'tabla':html})

def LineaEspera(request):
    return render(request, "lineaespera.html", {})

def LineaEsperar(request):
    landa = float(request.POST["landa"])
    nu = float(request.POST["niu"])
    numClientes = int(request.POST["nclientes"])

    i = 0
    indice = ['Cliente','ALL','ASE','TILL','TISE','TIRLL','TIISE','TIFSE','TIESP','TIESA']
    Clientes = np.arange(numClientes)
    dfLE = pd.DataFrame(index=Clientes, columns=indice).fillna(0.000)
    np.random.seed(100)
    for i in Clientes:
       if i == 0:
            dfLE['Cliente'][i] = 'cliente'+str(i+1)
            dfLE['ALL'][i] = random.random()
            dfLE['ASE'][i] = random.random()
            dfLE['TILL'][i] = -landa*np.log(dfLE['ALL'][i])
            dfLE['TISE'][i] = -nu*np.log(dfLE['ASE'][i])
            dfLE['TIRLL'][i] = dfLE['TILL'][i]
            dfLE['TIISE'][i] = dfLE['TIRLL'][i]
            dfLE['TIFSE'][i] = dfLE['TIISE'][i] + dfLE['TISE'][i]
            dfLE['TIESA'][i] = dfLE['TIESP'][i] + dfLE['TISE'][i]
       else :
            dfLE['Cliente'][i] = 'cliente '+str(i+1)
            dfLE['ALL'][i] = random.random()
            dfLE['ASE'][i] = random.random()
            dfLE['TILL'][i] = -landa*np.log(dfLE['ALL'][i])
            dfLE['TISE'][i] = -nu*np.log(dfLE['ASE'][i])
            dfLE['TIRLL'][i] = dfLE['TILL'][i] + dfLE['TIRLL'][i-1]
            dfLE['TIISE'][i] = max(dfLE['TIRLL'][i],dfLE['TIFSE'][i-1])
            dfLE['TIFSE'][i] = dfLE['TIISE'][i] + dfLE['TISE'][i]
            dfLE['TIESP'][i] = dfLE['TIISE'][i] - dfLE['TIRLL'][i]
            dfLE['TIESA'][i] = dfLE['TIESP'][i] + dfLE['TISE'][i]
       
    nuevas_columnas = pd.core.indexes.base.Index(["Cliente n","a_llegada","a_servicio","ti_llegada","ti_servicio",
         "ti_exac_llegada","ti_ini_servicio","ti_fin_servicio",
         "ti_espera","ti_en_sistema"])
    dfLE.columns = nuevas_columnas
    html = dfLE.to_html(classes='table table-sm table-warning')

    plt.figure(figsize=[8,8])
    plt.grid(True)
    plt.title("Grafico")
    plt.plot(dfLE['a_llegada'],label='Aleatorio llegada')
    plt.plot(dfLE['a_servicio'],label='Aleatorio servicio')
    plt.plot(dfLE['ti_llegada'],label='Tiempo de llegada')
    plt.plot(dfLE['ti_servicio'],label='Tiempo de servicio')
    plt.plot(dfLE['ti_exac_llegada'],label='Tiempo exacto de llegada')
    plt.plot(dfLE['ti_ini_servicio'],label='Tiempo de inicio de servicio')
    plt.plot(dfLE['ti_fin_servicio'],label='Tiempo fin de servicio')
    plt.plot(dfLE['ti_espera'],label='Tiempo de espera')
    plt.plot(dfLE['ti_en_sistema'],label='Tiempo en el sistema')
    plt.legend(loc=2)
    plt.savefig('static/img/MetodoLineaDeEspera/imagen.png')
    plt.close()
    dfLE.plot()

    return render(request, "lineaesperar.html", {'tabla':html})

def Montecarlo(request):
    return render(request, "montecarlo.html", {})

def Montecarlor(request):
    TLlegada = request.POST["TiempoDeLlegada"]
    PLlegada = request.POST["Probabilidad_Tiempo"]
    TServicio = request.POST["TiempoDeServicio"]
    PServicio = request.POST["Probabilidad_Servicio"]
    

    x0 = int(request.POST["Xn"])     #semilla        Xn
    a =  int(request.POST["a"])      #multiplicador  a
    c =  int(request.POST["c"])      #incremento     c
    m =  int(request.POST["m"])      #modulo         m
    num =  int(request.POST["n"])      #iteracciones   n
    n = num * 2

    Tiempo_Lleganda = llenarDatosVacios(TLlegada)
    Probabilidad_Llegada = llenarDatosVacios(PLlegada)
    Tiempo_Servicio = llenarDatosVacios(TServicio)
    Probabilidad_Servicio = llenarDatosVacios(PServicio)

    num_Element_Tiempo_Lleganda = len(Tiempo_Lleganda)
    num_Element_Tiempo_Servicio = len(Tiempo_Servicio)

    ProbabilidadAcumuladaLlegada = []
    i=0
    while i < num_Element_Tiempo_Lleganda:
        if len(ProbabilidadAcumuladaLlegada) == 0:
            ProbabilidadAcumuladaLlegada.append(Probabilidad_Llegada[i])
        else:
            ProbabilidadAcumuladaLlegada.append(round(Probabilidad_Llegada[i]+ProbabilidadAcumuladaLlegada[i-1],2))
        i = i+1
    
    ProbabilidadAcumuladaServicio = []    
    J = 0    
    while J < num_Element_Tiempo_Servicio:
        if len(ProbabilidadAcumuladaServicio) == 0:
            ProbabilidadAcumuladaServicio.append(Probabilidad_Servicio[J])
        else:
            ProbabilidadAcumuladaServicio.append(round(Probabilidad_Servicio[J]+ProbabilidadAcumuladaServicio[J-1],2))
        J = J+1
       
    df = pd.DataFrame()    
    df['TiempoLlegada'] = Tiempo_Lleganda  
    df['Probabilidad'] = Probabilidad_Llegada  
    df['ProbabilidadAcumulada'] = ProbabilidadAcumuladaLlegada
    ProbabilidadAcumuladaLlegada
    ProbabilidadAcumuladaLlegada.pop()
    ProbabilidadAcumuladaLlegada.insert(0,0)
    df['Menor'] = ProbabilidadAcumuladaLlegada
    df['Mayor'] = df['ProbabilidadAcumulada']
    tablaLlegada = df.to_html(classes='table table-sm table-warning')

    df2 = pd.DataFrame()    
    df2['TiempoServicio'] = Tiempo_Servicio 
    df2['Probabilidad'] = Probabilidad_Servicio  
    df2['ProbabilidadAcumulada'] = ProbabilidadAcumuladaServicio
    ProbabilidadAcumuladaServicio.pop()
    ProbabilidadAcumuladaServicio.insert(0,0)
    df2['Menor'] = ProbabilidadAcumuladaServicio
    df2['Mayor'] = df2['ProbabilidadAcumulada']
    tablaServicio = df2.to_html(classes='table table-sm table-warning')

    x = [1] * n
    r = [0.1] * n  
    for i in range(0, n):
        x[i] = ((a*x0)+c) % m
        x0 = x[i]
        r[i] = x0 / m

    aleatorio_Llegada = r[:len(r)//2]
    aleatorio_Servicio = r[len(r)//2:]

    df_Result = pd.DataFrame()
    df_Result['Aleatorio Llegada'] = aleatorio_Llegada
    df_Result['Aleatorio Servicio'] = aleatorio_Servicio

    Menor = df['Menor'].tolist()
    Mayor = df['Mayor'].tolist()
    tiempo_Llegada = []
    k = 0               # Realiza la pregunta de en que intervalo se encuantra el numero aleatorio y asigna el tiemo de llegada
    while k < n/2:
        z = 0
        while z < num_Element_Tiempo_Lleganda:
            if aleatorio_Llegada[k] > Menor[z] and aleatorio_Llegada[k] < Mayor[z]:
                tiempo_Llegada.append(Tiempo_Lleganda[z])
            z = z + 1
        k = k + 1

    Menor = df2['Menor'].tolist()     
    Mayor = df2['Mayor'].tolist()    
    tiempo_Servicio = []    
    k = 0              
    while k < n/2:
        z = 0
        while z < num_Element_Tiempo_Servicio:
            if aleatorio_Servicio[k] > Menor[z] and aleatorio_Servicio[k] < Mayor[z]:
                tiempo_Servicio.append(Tiempo_Servicio[z])
            z = z + 1
        k = k + 1 

    df_Result['Tiempo Llegada'] = tiempo_Llegada
    df_Result['Tiempo Servicio'] = tiempo_Servicio

    i = 0
    dfLE = pd.DataFrame()
    cliente,AleatorioLlegada,AleatorioServicio,TiempoDeLlegada,TiempoDeServicio,HoraExactaDeLlegada,HoraDeInicioServicio,HoraFinServicio,TiempoDeEspera,TiempoEnSistema = [],[],[],[],[],[],[],[],[],[]
    while i < n/2:
        if i == 0:
            cliente.append('cliente'+str(i+1))  
            AleatorioLlegada.append(df_Result['Aleatorio Llegada'][i]) 
            AleatorioServicio.append(df_Result['Aleatorio Servicio'][i]) 
            TiempoDeLlegada.append(df_Result['Tiempo Llegada'][i]) 
            TiempoDeServicio.append(df_Result['Tiempo Servicio'][i])
            HoraExactaDeLlegada.append(TiempoDeLlegada[i]) 
            HoraDeInicioServicio.append(HoraExactaDeLlegada[i]) 
            HoraFinServicio.append(HoraDeInicioServicio[i]+TiempoDeServicio[i])
            TiempoDeEspera.append(0)
            TiempoEnSistema.append(TiempoDeServicio[i])
            i = i+1
        else :
            cliente.append('cliente'+str(i+1))  
            AleatorioLlegada.append(df_Result['Aleatorio Llegada'][i]) 
            AleatorioServicio.append(df_Result['Aleatorio Servicio'][i]) 
            TiempoDeLlegada.append(df_Result['Tiempo Llegada'][i]) 
            TiempoDeServicio.append(df_Result['Tiempo Servicio'][i])
            HoraExactaDeLlegada.append(TiempoDeLlegada[i]+HoraExactaDeLlegada[i-1]) 
            HoraDeInicioServicio.append(max(HoraExactaDeLlegada[i],HoraFinServicio[i-1]))
            HoraFinServicio.append(HoraDeInicioServicio[i]+TiempoDeServicio[i])
            TiempoDeEspera.append(HoraDeInicioServicio[i]-HoraExactaDeLlegada[i]) 
            TiempoEnSistema.append(TiempoDeEspera[i]+TiempoDeServicio[i]) 
            i = i+1
        
    dfLE = pd.DataFrame()
    dfLE['Cliente'] = cliente
    dfLE['Aleatorio Llegada'] = AleatorioLlegada
    dfLE['Aleatorio Servicio'] = AleatorioServicio
    dfLE['Tiempo Llegada'] = TiempoDeLlegada
    dfLE['Tiempo Servicio'] = TiempoDeServicio
    dfLE['Hora Exacta Llegada'] = HoraExactaDeLlegada
    dfLE['Hora Inicio Servicio'] = HoraDeInicioServicio
    dfLE['Hora Fin Servicio'] = HoraFinServicio
    dfLE['Tiempo De Espera'] = TiempoDeEspera
    dfLE['Tiempo En Sistema'] = TiempoEnSistema
    html = dfLE.to_html(classes='table table-sm table-warning')
   
    return render(request, "montecarlor.html", {'tablaLlegada':tablaLlegada,'tablaServicio':tablaServicio,'html':html})
def llenarDatosVacios(listaStr):
    sentence = listaStr 
    new = sentence.replace(' ','')

    li = new.split(",")
    #quita los elementos vacios de la lista y los remplaza por ceros
    num_Element = len(li) 
    i = 0
    while i < num_Element:
        if li[i] == '':
            li.remove("")
            li.insert(i, '0')
        i = i+1  
    lista_Llena = list(map(float, li))
    return lista_Llena

def Grafico(request):
    return render(request, "grafico.html", {})

def Graficor(request):
    cantidad_Muestra = int(request.POST["cantidad_Muestra"])
    i = 1
    lista = []
    while(i <= cantidad_Muestra):
        datosInput = float(request.POST["input"+str(i)])
        lista.append(datosInput)
        i = i + 1
    df = pd.DataFrame()
    df['Muestra'] = lista   
    x=df['Muestra'] 
    plt.figure(figsize=(10,5))
    plt.hist(x,bins=8,color='#C7A48F')
    plt.axvline(x.mean(),color='#8D4D99',label='Media')
    plt.axvline(x.median(),color='#70AD5C',label='Mediana')
    plt.axvline(x.mode()[0],color='#703838',label='Moda')

    plt.xlabel('Total')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.savefig('static/img/MediaModaMediana/imagen.png')
    plt.close()
    media = x.mean()
    mediana = x.median()
    moda = x.mode()[0]
    return render(request, "graficor.html", {'media':media, 'mediana':mediana, 'moda':moda})

def Exponencial(request):
    return render(request, "exponencial.html", {})

def Exponencialr(request):
    landa = int(request.POST["landa"])
    R = int(request.POST["iteracion"])
    lista = []
    i = 0
    while i < R:
        r = random.uniform(0, 1)                #genera un numero ramdom entre cero y uno
        lista.append(r)                         #llena las listas
        i = i+1
        
    df = pd.DataFrame()    
    df['Numeros Randoms'] = lista
    dfexp = df['Numeros Randoms']
    # calculamos a todos los elementos la inversa
    exp_x = dfexp.values*(-1/landa)*np.log(dfexp)
    # anexamos al Datafram dfMCL
    df["Variable Exponencial"] = exp_x
    # Mostramos el resultado
    df.head()
    #tablaExpo = df.to_html(classes='table table-sm table-secondary')
    tablaExpo = df.to_html(classes='table table-sm table-warning')
    dfgrafico = df.filter(items=['Número Aleatorio','Variable Exponencial'])
    dfgrafico.plot(figsize=(50,15))


    #plt.plot(x1)            #grafico
    plt.title("Gráfico Exponencial")
    #plt.xlabel("Serie")
    #plt.ylabel("Aleatorios")
    plt.savefig('static/img/Exponencial/imagen.png')
    plt.close()

    
    return render(request, "exponencialr.html", {'tabla':tablaExpo})
def Simulacion(request):
    return render(request, "simulacion.html", {})

def Simulacionr(request):
    return render(request, "montecarlor.html", {})
    
 