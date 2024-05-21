import sys, time, os

instrucoesDoTp = {"i":("addi","lw","sw","bne"),"r":("add","sub","xor","sll")}
funcPara_i_3Bits = {'addi':'000','lw':'010','sw':'010','bne':'001'}
funcPara_r_3Bits = {'add':'000','sub':'000','xor':'100','sll':'001'}

def processarLinhaPrincipal(linha, debug=False, extended=False):
    if linha == "":
        return
    espaco = ""
    if debug:
        espaco = " "
    inst = ""
    completo = []
    res = ""
    for digito in linha:
        if digito != " " and digito != ",":
            inst += digito
        elif inst:
            completo.append(inst)
            inst = ""
    if inst:
        completo.append(inst)

    if debug and extended:
        print("instrucao completa:", completo)
    
    # caso I
    if completo[0] in instrucoesDoTp["i"]:
        if completo[0] == "lw" or completo[0] == "sw":
            if len(completo) < 3:
                print("instrucao invalida para o formato", completo[0])
                return
            registradorSetarOff = completo[-1].split("(")[1].strip(")")
            
            paraSetar = funcComplementoDeDois(reg(registradorSetarOff))
            
            res += paraSetar + espaco
            res+=reg(completo[1]) + espaco
            res+= funcPara_i_3Bits[completo[0]] + espaco
            res+=reg(registradorSetarOff) + espaco
        elif completo[0] == "bne":
            if len(completo) < 4:
                print("instrucao invalida para o formato", completo[0])
                return
            
            endRecebeComp = completo[-1]
            
            
            enderecoAtual = 4  
            enderecoDesejado = int(endRecebeComp) * 4  
            paraSetar = enderecoDesejado - enderecoAtual  
            paraSetar = funcComplementoDeDois(paraSetar)  
            
            
            res += paraSetar + espaco
            res += reg(completo[2]) + espaco
            res += reg(completo[1]) + espaco
            res += funcPara_i_3Bits[completo[0]] + espaco
        else:
            if len(completo) < 3:
                print("nstrucao invalida para o formato", completo[0])
                return
            res += funcComplementoDeDois(completo[-1]) + espaco
            res+=reg(completo[2]) + espaco
            res+= funcPara_i_3Bits[completo[0]] + espaco
            res+=reg(completo[1]) + espaco

        res+='0010011'

    
    else:
        if completo[0] == 'sub':
            res+="0100000" + espaco
        else:
            res+="0000000" + espaco
        res+=reg(completo[3]) + espaco
        res+=reg(completo[2]) + espaco
        res+=funcPara_r_3Bits[completo[0]] + espaco
        res+=reg(completo[1]) + espaco
        res+='0110011'
    if "-f" in sys.argv:
        with open(sys.argv[3],"a") as file:
            file.write(res+"\n")
    else:
        print(res)




def funcComplementoDeDois(numeroParametro,bits=12):
    
    numeroParametro = int(numeroParametro)
    if numeroParametro < 0:
        return bin((1 << bits) + numeroParametro)[2:]
    else:
        numeroParametro = bin(numeroParametro)[2:]
    c = bits
    for i in numeroParametro:
        c-=1
    return c*'0'+str(numeroParametro)

def reg(reg):
    
    reg = int(reg.strip('x'), 16)
    
    c = 5
    for i in range(len(bin(reg)[2:])):
        c-=1
    return c*'0'+bin(reg)[2:]



def main():
    if len(sys.argv) >= 4:
        if os.path.isfile(sys.argv[3]):
            os.remove(sys.argv[3])
    with open(sys.argv[1],"r") as file:
        alli = file.readlines()
        if "-de" in sys.argv[-1]:
            for linha in alli:
                processarLinhaPrincipal(linha.strip("\n"),True,True)
            return
        if "-d" in sys.argv[-1]:
            for linha in alli:
                processarLinhaPrincipal(linha.strip("\n"),True)
            return
        for linha in alli:
            processarLinhaPrincipal(linha.strip("\n"))
start = time.time()
main()
print("\nexecutado em: %s s" % (time.time()-start))
