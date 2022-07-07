lista_etiquetas=[]
lista_valores=[]
extendido_forzado=[]
etiquetas_extendido={}
etiquetas_instruccion={}
instr_incorr={}
error6_op={}
error5_op={}
error3_eti={}
error8_rel={}
error7_instr={}
cursor_memoria=0
bandera_ORG=False
bandera_exito=True
archivo_instr=open("lista_instrucciones.csv",'r')
instrucciones=archivo_instr.readlines()
archivo_instr.close()

archivo_instr_completo=open("instrucciones.csv",'r')
instrucciones_completas=archivo_instr_completo.readlines()
archivo_instr_completo.close()

for lectura in instrucciones_completas:
  linea=lectura.split(',')
  if(linea[2]=='0' and linea[5]!='0'):
    extendido_forzado.append(linea[0])

def es_Letra(character):
  asci=ord(character) ## se obtiene el codigo ascii
  if((asci>=97 and asci <=122) or (asci >=65 and asci<=90)):
    return True
  else:
    return False
def es_caracter(character):
  asci=ord(character) ## se obtiene el codigo ascii
  if((asci>=33 and asci <=126)):
    return True
  else:
    return False
##si el primer caracter es una letra entonces debe ser una variable
def esOperandoVariable(operando):
  return es_Letra(operando[0])

##para ver si una instruccion es relativa
def esRelativa(instruccion):
  for linea in instrucciones_completas:
     celdas=linea.split(',')
     aux=celdas[7].rstrip()
     if(aux!='0'):
       if(celdas[0].upper()==instruccion.upper()):
         return True
  return False

def esInherente(instruccion):
  for linea in instrucciones_completas:
     celdas=linea.split(',')
     aux=celdas[6].rstrip()
     if(aux!='0'):
       if(celdas[0].upper()==instruccion.upper()):
         return True
  return False

##para parsear el operando a numero int
def numero_en_operando(operando):
  if(operando[0]=='$'):
    number=operando[1:]
    aux="0x"+number
    numero=int(aux,16)
  return numero

##para verificar si NO es una instruccion valida
def no_en_Lista(instruccion):
  for instr in instrucciones:
    rees=instr.rstrip(instr[-1])
    if(instruccion.upper() == rees.upper()):
      return False
  return True

##sabiendo cuantos bits hay se puede mover el cursor en las direcciones de memoria
def cuantos_Bits(operando):
  if(operando[0]=='$'):
    longitud=len(operando)-1
    return longitud*4
  else:
    ##es asi porque cuando no lleva '$' no puede simplemente ser contada la cantidad de bits por caracteres
    longitudH=len(hex(int(operando)))-2
    return longitudH*4

##para saber si ya se reviso dicha etiqueta
def is_in_Etiquetas(operando):
  for etiqueta in lista_etiquetas:
    if(operando.upper()==etiqueta.upper()):
      return True
  return False

def que_Direccionamiento(instruccion, operando):
  ##-2 no es inherente y no hay operando
  ##-1 no es instruccion valida
  ##1 es Inmediato
  ##2 es Directo
  ##3 es Indexado x
  ##4 es Indexado y
  ##5 es Extendido
  ##6 es Inherente
  ##7 es Relativo
  #10 es Relativo que aun no veo

  if(instruccion==""):
    return 0

  if(no_en_Lista(instruccion)):
    return -1

  elif(esInherente(instruccion)):
    return 6

  elif(not operando):
    return -2
  
  elif(operando[0]=='#'):
    return 1

  elif(esRelativa(instruccion)):
    aux_bool= is_in_Etiquetas(operando)
    if(not aux_bool):
      return 10
    else:
      return 7

  elif(operando.find(',')>=0):
    if(operando.find('X')>=0):
      return 3
    elif(operando.find('Y')>=0):
      return 4

  else:
    ## Es para saber si la instruccion no tiene direccionamiento directo
    bandera_estado=instruccion in extendido_forzado
    if(bandera_estado):
      return 5
      
    elif(esOperandoVariable(operando)):
      
      ##Si no se encuentra entonces es etiqueta por ver y se usa extendido
      aux_bool= operando in lista_etiquetas
      if(not aux_bool):
        return 5
      else:
        idx=lista_etiquetas.index(operando)
        valor=lista_valores[idx]
        if(valor<=255):
         return 2
        else:
          return 5
    else:
      bits=cuantos_Bits(operando)
      if(bits<=8):
        return 2
      elif(bits>8):
        return 5

def valueToOpcode(valor):
  hexadecimal=hex(valor)
  hexString=""
  if(valor<=15):
    hexString="0x0"+str(hexadecimal)[-1]
  elif(valor<=255):
    hexString="0x"+str(hexadecimal)[-2:]
  elif(valor<=4095):
    hexString="0x0"+str(hexadecimal)[-3:]
  else:
    hexString=str(hexadecimal)
  return hexString

def search(list, coincidencia):
    for i in range(len(list)):
        if list[i].upper() == coincidencia.upper():
            return i
    return -1



#####################################################
##      CODIGO    PRINCIPAL              ############
##################################################### 

print("PROYECTO DE ESTRUCTURAS #1 COMPILADOR \n\n")
nombre_Archivo=input("Ingrese el nombre de su archivo sin extension\n")
## Apertura archivo para lectura y escritura
archivo_Compilar=open(nombre_Archivo+".asc", 'r')
## Se crea una lista para cargar el archivo a memoria
programa=archivo_Compilar.readlines()
##Se cierra el archivo del programa
archivo_Compilar.close()


##Se lee cada linea para poderla trabajar
for linea in programa:
  ##Dentro de cada linea se separa por caracteres
  i=0
  caracter=linea[i]
  limite=len(linea)-1
  ##Primero se busca si la linea tiene comentario y en donde
  idx=linea.find('*')
  if(idx>=0):
    ##Con esto, ya no se tomaran en cuenta los comentarios
    limite=idx
  
  etiqueta=""
  while(i<limite and es_caracter(caracter)):
    etiqueta+=caracter
    i+=1
    caracter=linea[i] 

  while(i<limite and not es_caracter(caracter)):
    i+=1
    caracter=linea[i]

  ##Aqui se almacenaran los caracteres para formar el string de la instruccion
  instruccion=""
  ##Se evalua que sean letras, mayusculas o minusculas
  while(i<limite and es_Letra(caracter)):
    instruccion+=caracter
    i+=1
    caracter=linea[i]

  while(i<limite and caracter==" "):
    i+=1
    caracter=linea[i]

  ##Como hay instrucciones sin operando, hay que verificar porque termino el while anterior
  operando=""
  if(i<limite):
    while(i<limite):
      operando+=caracter
      i+=1
      caracter=linea[i]
    ##esta linea limpia los espacios del final del operando
    operando_aux=operando.split(' ')
    operando=operando_aux[0]
    if(instruccion.upper()=="BRCLR"):
      operando+=" "
      operando+=operando_aux[1]
      
  
  ###############################################
  ## Lo que sucede aqui afecta a cada linea, una vez
  ## se tiene conocimiento de que es la instruccion
  ###############################################
  instr=instruccion.upper() ##Se limpia la instruccion para que sea anti case sensitive
  if(etiqueta):
    if(instr!="EQU"):
      lista_etiquetas.append(etiqueta)
      lista_valores.append(cursor_memoria)
    if(etiqueta in etiquetas_extendido):
      etiquetas_extendido[etiqueta]=cursor_memoria
      
  if(instr=="ORG" or instr=="EQU" or instr=="FCB" or instr=="END"):
     ##Aqui ya se contabiliza el numero que esta en la directiva de ensamblador ORG
    if(instr=="ORG"):
      cursor_memoria=numero_en_operando(operando)
      bandera_ORG=True
    if(instr=="EQU"):
      lista_etiquetas.append(etiqueta)
      lista_valores.append(numero_en_operando(operando))
    if(instr=="END"):
      bandera_ORG=False
  

  else:
    direccionamiento=que_Direccionamiento(instr.lower(), operando)
    
    ## Para este punto ya tengo la informacion de todo, ahora empieza el proceso de colocar los OPCODE
    opcode=""
    #Para el operando
    opcode2=""

   ##para encontrar la instruccion y su respectivo opcode
    for linea_aux in instrucciones_completas:
     celdas=linea_aux.split(',')
     if(celdas[0].upper()==instr):
       indice_tabla=direccionamiento
       if(direccionamiento==10):
         indice_tabla=7
       opcode=celdas[indice_tabla].rstrip()
    cursor_memoria+=(len(opcode))//2
    #aqui ya tengo los opcode, solo falta el operando en hex

    ##1 es Inmediato
    ##2 es Directo
    ##3 es Indexado x
    ##4 es Indexado y
    ##5 es Extendido
    ##6 es Inherente
    ##7 es Relativo
    #10 es Relativo que aun no veo
    if(direccionamiento==1):
      #aqui quito '#' del operando
      operando_limpio=operando[1:]
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[1]=='$'):
        number=int(operando_limpio[1:],16)
        opcode2=valueToOpcode(number)
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[1]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
        cursor_memoria+=(len(opcode2)-2)//2
      else:
        opcode2=valueToOpcode(int(operando_limpio))
        cursor_memoria+=(len(opcode2)-2)//2
      
    elif(direccionamiento==2):
      operando_limpio=operando
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[0]=='$'):
        number=int(operando_limpio[1:],16)
        opcode2=valueToOpcode(number)
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
        cursor_memoria+=(len(opcode2)-2)//2
      else:
        opcode2=valueToOpcode(int(operando_limpio))
        cursor_memoria+=(len(opcode2)-2)//2
      
    elif(direccionamiento==3):
      #aqui quito ',X' del operando
      operando_limpio=operando[:-2]
      operando_limpio3=" "
      #Hay una instruccion especial con doble operando
      if(instr=="BRCLR" or instr=="BSET"):
        operando_aux=operando.split(",")
        operando_aux2=operando_aux[2].split(" ")
        if(instr=="BRCLR"):
          operando_limpio3=operando_aux2[1]
        operando_limpio2=operando_aux2[0][1:]
        operando_limpio=operando_aux[0]
      
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
      
      elif(operando[0]=='$'):
        opcode2="0x"+(operando_limpio[1:])
      
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
      
      else:
        opcode2=valueToOpcode(int(operando_limpio))
      
      if(instr=="BRCLR" or instr=="BSET"):
        
        if(esOperandoVariable(operando_limpio2)):
          idxAux=search(lista_etiquetas,operando_limpio2)
          valAux=lista_valores[idxAux]
          opcode2+=valueToOpcode(valAux)[2:]
        
        elif(operando[0]=='$'):
          opcode2+=(operando_limpio2[1:])
        
        elif(operando[0]=='\''):
          int_ascii=ord(operando_limpio2[1:])
          opcode2+=valueToOpcode(int_ascii)[2:]
        
        else:
          opcode2+=valueToOpcode(int(operando_limpio2))[2:]
          

        cursor_memoria+=(len(opcode2)-2)//2
        if(es_caracter(operando_limpio3[0])):
        
          if(esOperandoVariable(operando_limpio3)):
            idxAux=search(lista_etiquetas,operando_limpio3)
            valAux=lista_valores[idxAux]
            cursor_memoria+=1
            diferencia_cursor=cursor_memoria-valAux
        ##para estos casos siempre sera una 
        ##referencia backward, asi que el 
        ##operando es el complemento a 2 de 
        ##la diferencia, se hara en hexadecimal
            opcode2+=valueToOpcode(256-diferencia_cursor)[2:]
            if(diferencia_cursor>256):
              print("ERROR, excedente de referencia")
          else:
            print("Error, solo pueden ser etiquetas")
      else:
        cursor_memoria+=(len(opcode2)-2)//2

        
    elif(direccionamiento==4):
      #aqui quito ',Y' del operando
      operando_limpio=operando[:-2]
      operando_limpio3=" "
      #Hay una instruccion especial con doble operando
      if(instr=="BRCLR" or instr=="BSET"):
        operando_aux=operando.split(",")
        operando_aux2=operando_aux[2].split(" ")
        if(instr=="BRCLR"):
          operando_limpio3=operando_aux2[1]
        operando_limpio2=operando_aux2[0][1:]
        operando_limpio=operando_aux[0]
      
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
    
      elif(operando[0]=='$'):
        opcode2="0x"+(operando_limpio[1:])
    
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
    
      else:
        opcode2=valueToOpcode(int(operando_limpio))
    
      if(instr=="BRCLR" or instr=="BSET"):
        if(esOperandoVariable(operando_limpio2)):
          idxAux=search(lista_etiquetas,operando_limpio2)
          valAux=lista_valores[idxAux]
          opcode2+=valueToOpcode(valAux)[2:]
      
        elif(operando[0]=='$'):
          opcode2+=(operando_limpio2[1:])
      
        elif(operando[0]=='\''):
          int_ascii=ord(operando_limpio2[1:])
          opcode2+=valueToOpcode(int_ascii)[2:]
      
        else:
          opcode2+=valueToOpcode(int(operando_limpio2))[2:]
          

        cursor_memoria+=(len(opcode2)-2)//2
        if(es_caracter(operando_limpio3[0])):
        
          if(esOperandoVariable(operando_limpio3)):
            idxAux=search(lista_etiquetas,operando_limpio3)
            valAux=lista_valores[idxAux]
            cursor_memoria+=1
            diferencia_cursor=cursor_memoria-valAux
        ##para estos casos siempre sera una 
        ##referencia backward, asi que el 
        ##operando es el complemento a 2 de 
        ##la diferencia, se hara en hexadecimal
            opcode2+=valueToOpcode(256-diferencia_cursor)[2:]
            if(diferencia_cursor>256):
              print("ERROR, excedente de referencia")
          else:
            print("Error, solo pueden ser etiquetas")
      else:
        cursor_memoria+=(len(opcode2)-2)//2
     
    elif(direccionamiento==5):
      operando_limpio=operando
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
        if(len(opcode2)<=4):
          opcode2="0x00"+opcode2[-2:]
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[0]=='$'):
        number=int(operando_limpio[1:],16)
        opcode2=valueToOpcode(number)
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
        cursor_memoria+=(len(opcode2)-2)//2
      else:
        opcode2=valueToOpcode(int(operando_limpio))
        cursor_memoria+=(len(opcode2)-2)//2
      
    elif(direccionamiento==6):
      
      opcode2=""

    elif(direccionamiento==7):
      operando_limpio=operando
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        cursor_memoria+=1
        diferencia_cursor=cursor_memoria-valAux
        ##para estos casos siempre sera una 
        ##referencia backward, asi que el 
        ##operando es el complemento a 2 de 
        ##la diferencia, se hara en hexadecimal
        opcode2=valueToOpcode(256-diferencia_cursor)
      
    elif(direccionamiento==10):
      etiquetas_extendido[operando]=0
      cursor_memoria+=1
      


cursor_memoria=0
################################################### 
###            Segunda pasada                 #####
###        Generacion Archivo lst             #####
###################################################
num_linea=0
## En caso de que el archivo exista se sobreescribe con vacio
archivo_Compilado=open(nombre_Archivo+".lst", 'w')
archivo_Compilado.write("")
archivo_Compilado.close()
## Se abre el archivo para concatenar todas las lineas
archivo_Compilado=open(nombre_Archivo+".lst", 'a')
for linea in programa:
  num_linea+=1
  archivo_Compilado.write(str(num_linea)+": ")
  ##Dentro de cada linea se separa por caracteres
  i=0
  caracter=linea[i]
  limite=len(linea)-1
  ##Primero se busca si la linea tiene comentario y en donde
  idx=linea.find('*')
  if(idx>=0):
    ##Con esto, ya no se tomaran en cuenta los comentarios
    limite=idx
  
  etiqueta=""
  while(i<limite and es_caracter(caracter)):
    etiqueta+=caracter
    i+=1
    caracter=linea[i] 

  while(i<limite and not es_caracter(caracter)):
    i+=1
    caracter=linea[i]

  ##Aqui se almacenaran los caracteres para formar el string de la instruccion
  instruccion=""
  ##Se evalua que sean letras, mayusculas o minusculas
  while(i<limite and es_Letra(caracter)):
    instruccion+=caracter
    i+=1
    caracter=linea[i]

  while(i<limite and caracter==" "):
    i+=1
    caracter=linea[i]

  ##Como hay instrucciones sin operando, hay que verificar porque termino el while anterior
  operando=""
  if(i<limite):
    while(i<limite):
      operando+=caracter
      i+=1
      caracter=linea[i]
    ##esta linea limpia los espacios del final del operando
    operando_aux=operando.split(' ')
    operando=operando_aux[0]
    if(instruccion.upper()=="BRCLR"):
      operando+=" "
      operando+=operando_aux[1]
  
  ###############################################
  ## Lo que sucede aqui afecta a cada linea, una vez
  ## se tiene conocimiento de que es la instruccion
  ###############################################
  instr=instruccion.upper() ##Se limpia la instruccion para que sea anti case sensitive
  
  if(etiqueta):
    etiqu=etiqueta.upper()
    for linea_aux2 in instrucciones_completas:
     celdas=linea_aux2.split(',')
     if(celdas[0].upper()==etiqueta):
       etiquetas_instruccion[num_linea]=etiqueta
    if(etiqu=="ORG" or etiqu=="EQU" or etiqu=="FCB" or etiqu=="END"):
      etiquetas_instruccion[num_linea]=etiqueta
      
    if(etiqueta in etiquetas_extendido):
      etiquetas_extendido[etiqueta]=cursor_memoria
    
  if(instr=="ORG" or instr=="EQU" or instr=="FCB" or instr=="END"):
     ##Aqui ya se contabiliza el numero que esta en la directiva de ensamblador ORG
    if(instr=="ORG"):
      cursor_memoria=numero_en_operando(operando)
      bandera_ORG=True
    if(instr=="END"):
      bandera_ORG=False

  else:
    direccionamiento=que_Direccionamiento(instr.lower(), operando)
    
    if(direccionamiento==-1):
      instr_incorr[num_linea]=instr
    if(direccionamiento==-2):
      error5_op[num_linea]=instr
    

    ## Para este punto ya tengo la informacion de todo, ahora empieza el proceso de colocar los OPCODE
    opcode=""
    #Para el operando
    opcode2=""

   
    for linea_aux in instrucciones_completas:
     celdas=linea_aux.split(',')
     if(celdas[0].upper()==instr):
       indice_tabla=direccionamiento
       if(direccionamiento==10):
         indice_tabla=7
       opcode=celdas[indice_tabla].rstrip()
       archivo_Compilado.write(hex(cursor_memoria)[2:])
       archivo_Compilado.write(" ("+opcode)
    cursor_memoria+=(len(opcode))//2
    #aqui ya tengo los opcode, solo falta el operando en hex
    
    ##1 es Inmediato
    ##2 es Directo
    ##3 es Indexado x
    ##4 es Indexado y
    ##5 es Extendido
    ##6 es Inherente
    ##7 es Relativo
    #10 ya no va a existir
    if(direccionamiento==1):
      #aqui quito '#' del operando
      operando_limpio=operando[1:]
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        if(idxAux>=0):
          valAux=lista_valores[idxAux]
          opcode2=valueToOpcode(valAux)
          cursor_memoria+=(len(opcode2)-2)//2
        else:
          error3_eti[num_linea]=operando
      elif(operando[1]=='$'):
        number=int(operando_limpio[1:],16)
        opcode2=valueToOpcode(number)
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[1]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
        cursor_memoria+=(len(opcode2)-2)//2
      else:
        opcode2=valueToOpcode(int(operando_limpio))
        cursor_memoria+=(len(opcode2)-2)//2

      ##si se genero un opcode demasiado largo es porque se excede de magnitud
      if(len(opcode2)>=7):
        error7_instr[num_linea]=operando
        
    elif(direccionamiento==2):
      operando_limpio=operando
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        if(idxAux>=0):
          valAux=lista_valores[idxAux]
          opcode2=valueToOpcode(valAux)
          cursor_memoria+=(len(opcode2)-2)//2
        else:
          error3_eti[num_linea]=operando
      elif(operando[0]=='$'):
        number=int(operando_limpio[1:],16)
        opcode2=valueToOpcode(number)
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
        cursor_memoria+=(len(opcode2)-2)//2
      else:
        opcode2=valueToOpcode(int(operando_limpio))
        cursor_memoria+=(len(opcode2)-2)//2
      if(len(opcode2)>=5):
        error7_instr[num_linea]=operando
        
    elif(direccionamiento==3):
      #aqui quito ',X' del operando
      operando_limpio=operando[:-2]
      operando_limpio3=" "
      #Hay una instruccion especial con doble operando
      if(instr=="BRCLR" or instr=="BSET"):
        
        operando_aux=operando.split(",")
        operando_aux2=operando_aux[2].split(" ")
        if(instr=="BRCLR"):
          operando_limpio3=operando_aux2[1]
        operando_limpio2=operando_aux2[0][1:]
        operando_limpio=operando_aux[0]
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        if(idxAux>=0):
          valAux=lista_valores[idxAux]
          opcode2=valueToOpcode(valAux)
        else:
          error3_eti[num_linea]=operando
      elif(operando[0]=='$'):
        opcode2="0x"+(operando_limpio[1:])
      
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
      
      else:
        opcode2=valueToOpcode(int(operando_limpio))
        
      if(len(opcode2)>=5):
        error7_instr[num_linea]=operando
        
      if(instr=="BRCLR" or instr=="BSET"):
        
        if(esOperandoVariable(operando_limpio2)):
          idxAux=search(lista_etiquetas,operando_limpio2)
          if(idxAux>=0):
            valAux=lista_valores[idxAux]
            opcode2+=valueToOpcode(valAux)[2:]
          else:
            error3_eti[num_linea]=operando
        
        elif(operando[0]=='$'):
          opcode2+=(operando_limpio2[1:])
        
        elif(operando[0]=='\''):
          int_ascii=ord(operando_limpio2[1:])
          opcode2+=valueToOpcode(int_ascii)[2:]
        
        else:
          opcode2+=valueToOpcode(int(operando_limpio2))[2:]
        if(len(opcode2)>=7):
          error7_instr[num_linea]=operando
        

        cursor_memoria+=(len(opcode2)-2)//2
        if(es_caracter(operando_limpio3[0])):
          if(esOperandoVariable(operando_limpio3)):
            idxAux=search(lista_etiquetas,operando_limpio3)


            if(idxAux>=0):
              valAux=lista_valores[idxAux]
              cursor_memoria+=1
              diferencia_cursor=cursor_memoria-valAux
          ##en esta iteracion ahora si hay que verificar
          ##si es referencia forward o backward
              if(cursor_memoria>valAux):
                opcode2+=valueToOpcode(256-diferencia_cursor)[2:]
              else:
                diferencia=valAux-cursor_memoria
                opcode2+=valueToOpcode(diferencia)[2:]
              if(len(opcode2)>=9):
                error7_instr[num_linea]=operando
        
          else:
            error3_eti[num_linea]=operando
      else:
        cursor_memoria+=(len(opcode2)-2)//2
        
        
    elif(direccionamiento==4):
      #aqui quito ',Y' del operando
      operando_limpio=operando[:-2]
      operando_limpio3=" "
      #Hay una instruccion especial con doble operando
      if(instr=="BRCLR" or instr=="BSET"):

        operando_aux=operando.split(",")
        operando_aux2=operando_aux[2].split(" ")
        if(instr=="BRCLR"):
          operando_limpio3=operando_aux2[1]
        operando_limpio2=operando_aux2[0][1:]
        operando_limpio=operando_aux[0]
      
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        if(idxAux>=0):
          valAux=lista_valores[idxAux]
          opcode2=valueToOpcode(valAux)
        else:
          error3_eti[num_linea]=operando
      elif(operando[0]=='$'):
        opcode2="0x"+(operando_limpio[1:])
        
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
        
      else:
        opcode2=valueToOpcode(int(operando_limpio))
        
      if(len(opcode2)>=5):
        error7_instr[num_linea]=operando
        
      if(instr=="BRCLR" or instr=="BSET"):
        
        if(esOperandoVariable(operando_limpio2)):
          idxAux=search(lista_etiquetas,operando_limpio2)
          if(idxAux>=0):
            valAux=lista_valores[idxAux]
            opcode2+=valueToOpcode(valAux)[2:]
          else:
            error3_eti[num_linea]=operando
        elif(operando[0]=='$'):
          opcode2+=(operando_limpio2[1:])
          
        elif(operando[0]=='\''):
          int_ascii=ord(operando_limpio2[1:])
          opcode2+=valueToOpcode(int_ascii)[2:]
        else:
          opcode2+=valueToOpcode(int(operando_limpio2))[2:]
          
        if(len(opcode2)>=7):
          error7_instr[num_linea]=operando
        
        cursor_memoria+=(len(opcode2)-2)//2
        if(es_caracter(operando_limpio3[0])):
          if(esOperandoVariable(operando_limpio3)):
            idxAux=search(lista_etiquetas,operando_limpio3)
            if(idxAux>=0):
              valAux=lista_valores[idxAux]
              cursor_memoria+=1
              diferencia_cursor=cursor_memoria-valAux
          ##en esta iteracion ahora si hay que verificar
          ##si es referencia forward o backward
              if(cursor_memoria>valAux):
                opcode2+=valueToOpcode(256-diferencia_cursor)[2:]
              else:
                diferencia=valAux-cursor_memoria
                opcode2+=valueToOpcode(diferencia)[2:]
              if(len(opcode2)>=9):
                error7_instr[num_linea]=operando
        
          else:
            error3_eti[num_linea]=operando
      else:
        cursor_memoria+=(len(opcode2)-2)//2
        
    elif(direccionamiento==5):
      operando_limpio=operando
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        if(idxAux>=0):
          valAux=lista_valores[idxAux]
          opcode2=valueToOpcode(valAux)
        else:
          error3_eti[num_linea]=operando
        if(len(opcode2)<=4):
          opcode2="0x00"+opcode2[-2:]
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[0]=='$'):
        opcode2="0x"+(operando_limpio[1:])
        cursor_memoria+=(len(opcode2)-2)//2
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
        cursor_memoria+=(len(opcode2)-2)//2
      else:
        opcode2=valueToOpcode(int(operando_limpio))
        cursor_memoria+=(len(opcode2)-2)//2
      if(len(opcode2)>=7):
        error7_instr[num_linea]=operando
        
    elif(direccionamiento==6):
      archivo_Compilado.write(")")
      if(operando):
        error6_op[num_linea]=instr
    elif(direccionamiento==7):
      operando_limpio=operando
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        if(idxAux>=0):
          valAux=lista_valores[idxAux]
          cursor_memoria+=1
          diferencia_cursor=cursor_memoria-valAux
          if(diferencia_cursor>256):
            error8_rel[num_linea]=operando
        ##en esta iteracion ahora si hay que verificar
        ##si es referencia forward o backward
          if(cursor_memoria>valAux):
            opcode2=valueToOpcode(256-diferencia_cursor)
          else:
            diferencia=valAux-cursor_memoria
            if(diferencia>256):
              error8_rel[num_linea]=operando
            opcode2=valueToOpcode(diferencia)
        else:
          error3_eti[num_linea]=operando
      if(len(opcode2)>=5):
        error7_instr[num_linea]=operando
        
    elif(direccionamiento==10):
      ##ya no deberia entrar este direccionamiento
      error3_eti[num_linea]=operando
    if(opcode2!=""):
      archivo_Compilado.write(opcode2[2:]+")") 
  archivo_Compilado.write("\t\t:\t"+linea+"\n")   
archivo_Compilado.close()

cursor_memoria=0
################################################### 
###            Tercera pasada                 #####
###        Generacion Archivo s19             #####
###################################################
contador_16=0
bandera_Inicio=True
## En caso de que el archivo exista se sobreescribe con vacio
codigo_Objeto=open(nombre_Archivo+".s19", 'w')
codigo_Objeto.write("")
codigo_Objeto.close()
## Se abre el archivo para concatenar todas las lineas
codigo_Objeto=open(nombre_Archivo+".s19", 'a')
for linea in programa:
  ##Dentro de cada linea se separa por caracteres
  i=0
  caracter=linea[i]
  limite=len(linea)-1
  ##Primero se busca si la linea tiene comentario y en donde
  idx=linea.find('*')
  if(idx>=0):
    ##Con esto, ya no se tomaran en cuenta los comentarios
    limite=idx
  
  etiqueta=""
  while(i<limite and es_caracter(caracter)):
    etiqueta+=caracter
    i+=1
    caracter=linea[i] 

  while(i<limite and not es_caracter(caracter)):
    i+=1
    caracter=linea[i]

  ##Aqui se almacenaran los caracteres para formar el string de la instruccion
  instruccion=""
  ##Se evalua que sean letras, mayusculas o minusculas
  while(i<limite and es_Letra(caracter)):
    instruccion+=caracter
    i+=1
    caracter=linea[i]

  while(i<limite and caracter==" "):
    i+=1
    caracter=linea[i]

  ##Como hay instrucciones sin operando, hay que verificar porque termino el while anterior
  operando=""
  if(i<limite):
    while(i<limite):
      operando+=caracter
      i+=1
      caracter=linea[i]
    ##esta linea limpia los espacios del final del operando
    operando_aux=operando.split(' ')
    operando=operando_aux[0]
    if(instruccion.upper()=="BRCLR"):
      operando+=" "
      operando+=operando_aux[1]
  
  ###############################################
  ## Lo que sucede aqui afecta a cada linea, una vez
  ## se tiene conocimiento de que es la instruccion
  ###############################################
  instr=instruccion.upper() ##Se limpia la instruccion para que sea anti case sensitive
  

  if(instr=="ORG" or instr=="EQU" or instr=="FCB" or instr=="END"):
     ##Aqui ya se contabiliza el numero que esta en la directiva de ensamblador ORG
    if(instr=="ORG"):
      cursor_memoria=numero_en_operando(operando)
      if(bandera_Inicio):
        codigo_Objeto.write("<"+hex(cursor_memoria)[2:]+"> ")
        bandera_Inicio=False
      else:
        codigo_Objeto.write("\n<"+hex(cursor_memoria)[2:]+"> ")
      bandera_ORG=True
    if(instr=="END"):
      bandera_ORG=False

  
  else:
    direccionamiento=que_Direccionamiento(instr.lower(), operando)
    
    

    ## Para este punto ya tengo la informacion de todo, ahora empieza el proceso de colocar los OPCODE
    opcode=""
    #Para el operando
    opcode2=""

   
    for linea_aux in instrucciones_completas:
     celdas=linea_aux.split(',')
     if(celdas[0].upper()==instr):
       indice_tabla=direccionamiento
       if(direccionamiento==10):
         indice_tabla=7
       bandera_Paridad=False
       opcode=celdas[indice_tabla].rstrip()
       ##para que solo se ejecute una vez
       
       
         

    ##Con esta pequeña secuencia se separa al opcode en pares
    for letra in opcode:
      codigo_Objeto.write(letra)
      if(bandera_Paridad):
        codigo_Objeto.write(" ")
        cursor_memoria+=1
        if(contador_16<15):
          contador_16+=1
        else:
          contador_16=0
          codigo_Objeto.write("\n<"+hex(cursor_memoria)[2:]+"> ")
        bandera_Paridad=False
        
      else:
        bandera_Paridad=True
    #aqui ya tengo los opcode, solo falta el operando en hex
    
    ##1 es Inmediato
    ##2 es Directo
    ##3 es Indexado x
    ##4 es Indexado y
    ##5 es Extendido
    ##6 es Inherente
    ##7 es Relativo
    #10 ya no va a existir
    if(direccionamiento==1):
      #aqui quito '#' del operando
      operando_limpio=operando[1:]
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
      elif(operando[1]=='$'):
        number=int(operando_limpio[1:],16)
        opcode2=valueToOpcode(number)
      elif(operando[1]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
      else:
        opcode2=valueToOpcode(int(operando_limpio))
      
        
    elif(direccionamiento==2):
      operando_limpio=operando
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
      elif(operando[0]=='$'):
        number=int(operando_limpio[1:],16)
        opcode2=valueToOpcode(number)
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
      else:
        opcode2=valueToOpcode(int(operando_limpio))
      
      
    elif(direccionamiento==3):
      #aqui quito ',X' del operando
      operando_limpio=operando[:-2]
      operando_limpio3=" "
      #Hay una instruccion especial con doble operando
      if(instr=="BRCLR" or instr=="BSET"):
        operando_aux=operando.split(",")
        operando_aux2=operando_aux[2].split(" ")
        if(instr=="BRCLR"):
          operando_limpio3=operando_aux2[1]
        operando_limpio2=operando_aux2[0][1:]
        operando_limpio=operando_aux[0]
      
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
        
      elif(operando[0]=='$'):
        opcode2="0x"+(operando_limpio[1:])
        
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
        
      else:
        opcode2=valueToOpcode(int(operando_limpio))
        
      if(instr=="BRCLR" or instr=="BSET"):
        
        if(esOperandoVariable(operando_limpio2)):
          idxAux=search(lista_etiquetas,operando_limpio2)
          valAux=lista_valores[idxAux]
          opcode2+=valueToOpcode(valAux)[2:]
          
        elif(operando[0]=='$'):
          opcode2+=(operando_limpio2[1:])
          
        elif(operando[0]=='\''):
          int_ascii=ord(operando_limpio2[1:])
          opcode2+=valueToOpcode(int_ascii)[2:]
          
        else:
          opcode2+=valueToOpcode(int(operando_limpio2))[2:]
          

        cursor_memoria+=(len(opcode2)-2)//2
        if(es_caracter(operando_limpio3[0])):
          if(esOperandoVariable(operando_limpio3)):
            idxAux=search(lista_etiquetas,operando_limpio3)
            valAux=lista_valores[idxAux]
            cursor_memoria+=1
            diferencia_cursor=cursor_memoria-valAux
          ##en esta iteracion ahora si hay que verificar
          ##si es referencia forward o backward
            if(cursor_memoria>valAux):
              opcode2+=valueToOpcode(256-diferencia_cursor)[2:]
            else:
              diferencia=valAux-cursor_memoria
              opcode2+=valueToOpcode(diferencia)[2:]
      else:
        cursor_memoria+=(len(opcode2)-2)//2
      cursor_memoria-=(len(opcode2)-2)//2
    elif(direccionamiento==4):
      #aqui quito ',Y' del operando
      operando_limpio=operando[:-2]
      operando_limpio3=" "
      #Hay una instruccion especial con doble operando
      if(instr=="BRCLR" or instr=="BSET"):
        operando_aux=operando.split(",")
        operando_aux2=operando_aux[2].split(" ")
        if(instr=="BRCLR"):
          operando_limpio3=operando_aux2[1]
        operando_limpio2=operando_aux2[0][1:]
        operando_limpio=operando_aux[0]
      
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
      
      elif(operando[0]=='$'):
        opcode2="0x"+(operando_limpio[1:])
      
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
      
      else:
        opcode2=valueToOpcode(int(operando_limpio))
      
      if(instr=="BRCLR" or instr=="BSET"):
        
        if(esOperandoVariable(operando_limpio2)):
          idxAux=search(lista_etiquetas,operando_limpio2)
          valAux=lista_valores[idxAux]
          opcode2+=valueToOpcode(valAux)[2:]
        
        elif(operando[0]=='$'):
          opcode2+=(operando_limpio2[1:])
        
        elif(operando[0]=='\''):
          int_ascii=ord(operando_limpio2[1:])
          opcode2+=valueToOpcode(int_ascii)[2:]
        
        else:
          opcode2+=valueToOpcode(int(operando_limpio2))[2:]
          

        cursor_memoria+=(len(opcode2)-2)//2
        if(es_caracter(operando_limpio3[0])):
          if(esOperandoVariable(operando_limpio3)):
            idxAux=search(lista_etiquetas,operando_limpio3)
            valAux=lista_valores[idxAux]
            cursor_memoria+=1
            diferencia_cursor=cursor_memoria-valAux
          ##en esta iteracion ahora si hay que verificar
          ##si es referencia forward o backward
            if(cursor_memoria>valAux):
              opcode2+=valueToOpcode(256-diferencia_cursor)[2:]
            else:
              diferencia=valAux-cursor_memoria
              opcode2+=valueToOpcode(diferencia)[2:]
      else:
        cursor_memoria+=(len(opcode2)-2)//2
        
      cursor_memoria-=(len(opcode2)-2)//2
    elif(direccionamiento==5):
      operando_limpio=operando
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        opcode2=valueToOpcode(valAux)
        if(len(opcode2)<=4):
          opcode2="0x00"+opcode2[-2:]
      elif(operando[0]=='$'):
        number=int(operando_limpio[1:],16)
        opcode2=valueToOpcode(number)
      elif(operando[0]=='\''):
        int_ascii=ord(operando_limpio[1:])
        opcode2=valueToOpcode(int_ascii)
      else:
        opcode2=valueToOpcode(int(operando_limpio))
    elif(direccionamiento==7):
      operando_limpio=operando
      if(esOperandoVariable(operando_limpio)):
        idxAux=search(lista_etiquetas,operando_limpio)
        valAux=lista_valores[idxAux]
        cursor_memoria+=1
        diferencia_cursor=cursor_memoria-valAux
        ##en esta iteracion ahora si hay que verificar
        ##si es referencia forward o backward
        if(cursor_memoria>valAux):
          opcode2=valueToOpcode(256-diferencia_cursor)
        else:
          diferencia=valAux-cursor_memoria
          opcode2=valueToOpcode(diferencia)
        cursor_memoria-=1
    if(opcode2!=""):
      bandera_Paridad=False
      for i in range(2,len(opcode2)):
        codigo_Objeto.write(opcode2[i].upper())
        if(bandera_Paridad):
          codigo_Objeto.write(" ")
          cursor_memoria+=1
          if(contador_16<15):
             contador_16+=1
          else:
             contador_16=0
             codigo_Objeto.write("\n<"+hex(cursor_memoria)[2:]+"> ")
          bandera_Paridad=False
        else:
          bandera_Paridad=True
      
codigo_Objeto.close()

################################################### 
###            Identificacion                 #####
###             de errores                    #####
###################################################


if(error3_eti):
  ##Este error se verifica en la segunda pasada
  bandera_exito=False
  for eti_i in error3_eti:
    print("ERROR 1/2/3: En linea:"+str(eti_i))
    print("Constante/Variable/Etiqueta inexistente: "+error3_eti[eti_i])

if(instr_incorr):
  ##Este error se verifica en la segunda pasada
  bandera_exito=False
  for instr_i in instr_incorr:
    print("ERROR 004: En linea:"+str(instr_i))
    print("Mnemonico inexistente: "+instr_incorr[instr_i])

if(error5_op):
  ##Este error se verifica en la segunda pasada
  bandera_exito=False
  for op_i in error5_op:
    print("ERROR 005: En linea:"+str(op_i))
    print("Instruccion carece de operando: "+error5_op[op_i])


if(error6_op):
  ##Este error se verifica en la segunda pasada
  bandera_exito=False
  for op_i in error6_op:
    print("ERROR 006: En linea:"+str(op_i))
    print("Instruccion no lleva operandos: "+error6_op[op_i])

if(error7_instr):
  ##Este error se verifica en la segunda pasada
  bandera_exito=False
  for instr_i in error7_instr:
    print("ERROR 007: En linea:"+str(instr_i))
    print("Magnitud de operando erronea: "+error7_instr[instr_i])

if(error8_rel):
  ##Este error se verifica en la segunda pasada
  bandera_exito=False
  for rel_i in error8_rel:
    print("ERROR 008: En linea:"+str(rel_i))
    print("Salto relativo muy lejano: "+error8_rel[rel_i])

if(etiquetas_instruccion):
  ##Este error se verifica en la segunda pasada
  bandera_exito=False
  for etiq_instr in etiquetas_instruccion:
    print("ERROR 009: En linea:"+str(etiq_instr))
    print("Se esperaba un espacio antes de: "+etiquetas_instruccion[etiq_instr])

if(bandera_ORG):
  ##Este error se esta verificando en cada pasada
  bandera_exito=False
  print("ERROR 010: No se encuentra END")
if(bandera_exito):
  print("El archivo ha sido compilado con exito")
