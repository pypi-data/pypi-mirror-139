# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 09:22:20 2021

@author: Héber
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np 
from math import *        

class funcao_pertinencia:
   
    intervalo = []
    nome = ''
    valor_pertinencia = 0.0

    def novaFP(intervalo, nome):
        fp = funcao_pertinencia()
        
        if len(intervalo) == 2:
            u = intervalo[0]
            o = intervalo[1]
            fp.intervalo = intervalo
            fp.nome = nome
            return fp
            
        elif len(intervalo) == 3:
            a = intervalo[0]
            m = intervalo[1]
            b = intervalo[2]
            
            if a <= m and m <= b:
                fp.intervalo = intervalo
                fp.nome = nome
                return fp
            else:
                print('O intervalo definido para a função de pertinência {} é inválido'.format(nome))
                return 0
        elif len(intervalo) == 4:
            a = intervalo[0]
            m = intervalo[1]
            n = intervalo[2]
            b = intervalo[3]
            
            if a <= m and m <= n and n <= b:
                fp.intervalo = intervalo
                fp.nome = nome
                return fp
            else:
                print('O intervalo definido para a função de pertinência {} é inválido'.format(nome))
                return 0
        else:
            return 0
    
    def pertinencia_max(self, c, x, maxi):
        pert = self.pertinencia(c, x)
        if(pert > maxi):
            return maxi
        else:
            return pert

    def pertinencia_max_prod(self, c, x, maxi):
        if maxi == 0:
            return 0
        peso = 1 / maxi
        pert = self.pertinencia(c, x)
        return pert / peso

            
    def pertinencia(self, c, x):
        if len(c) == 2:
            return self.pertinenciaGaussiana(c, x)
        elif len(c) == 3:
            return self.pertinenciaTri(c, x)
        elif len(c) == 4:
            return self.pertinenciaTrap(c, x)
    
    def pertinenciaGaussiana(self, c, x):
        m = c[0]
        o = c[1]
        pert = exp(-((x-m)**2) / (o**2))
        return pert
    
    def pertinenciaTri(self, c, x):
        a = c[0]
        m = c[1]
        b = c[2]
        
        if x < a:
            return 0
        elif a < x and x <= m:
            return (x - a) / (m - a)
        elif m < x and x <= b:
            return (b - x) / (b - m) 
        elif x > b:
            return 0
        elif x==m:
            return 1
        else:
            return 0
    
    def pertinenciaTrap(self, c, x):
        a = c[0]
        m = c[1]
        n = c[2]
        b = c[3]
        
        if x <= a:
            if x == 0 and a == 0:
                return 1
            else:
                return 0
        elif  a < x and x <= m:
            return (x - a) / (m - a)
        elif m < x and x <= n:
            return 1
        elif n < x and x <= b:
            return (b - x) / (b - n) 
        elif x > b:
            return 0
        else:
            return 0
         
        
    def plot(self,C, label, u, style):
        passo = 101
        i = u[0]
        valor = []
        intervalo = np.linspace(u[0]+0.01, u[1], passo)
        
        for i in intervalo:
            valor.append(self.pertinencia(C, i))
                
        plt.plot(intervalo, valor, style, label = label)
        plt.legend()


    def maior(self, cA, cB):
        m = cA[0]
        if(len(cA)==3):
            m = cA[2]
        elif(len(cA)==4):
            m = cA[3]
        elif(len(cA)==2):
            m = cA[1]*3.2
            print('MAIOR GAUSSIANA: ',m)
        
        if(len(cB)==3):
            if(cB[2]>m):
                m = cB[2]
        elif(len(cB)==4):
            if(cB[3]>m):
                m = cB[3]
        elif(len(cB)==2):
            m = (cB[1]*3.2)
            print('MAIOR GAUSSIANA: ',m)
        return m
        
    def menor(self, cA, cB):
        
        m = cA[0]
        
        if cB[0] < m:
            m = cB[0]
        
        return m