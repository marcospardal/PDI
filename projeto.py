import os
import time
import cv2
import numpy as np

def print_menu():
  os.system('cls' if os.name == 'nt' else 'clear')
  print('1 - Conversão RGB - HSB - RGB')
  print('2 - Filtro de saturação e brilho')
  print('3 - Atribuição de saturação')
  print('4 - Aplicar Correlação')
  print('5 - Sair')

  option = int(input('Selecione uma opção...\n'))

  return option

def selecionar_imagem():
  imagens = os.listdir('./data')
  action = -1

  os.system('cls' if os.name == 'nt' else 'clear')
  while action < 0 or action >= len(imagens):
    for i in range(0, len(imagens)):
      print(f'{i} - {imagens[i]}')
    
    action = int(input('Digite o número da imagem escolhida\n'))

  return imagens[action]

def selecionar_filtro():
  filtros = os.listdir('./filtros')
  action = -1

  os.system('cls' if os.name == 'nt' else 'clear')
  while action < 0 or action >= len(filtros):
    for i in range(0, len(filtros)):
      print(f'{i} - {filtros[i]}')
    
    action = int(input('Digite o número do filtro escolhido\n'))

  adiciona = int(input('Adicionar zeros? (1 - Sim, 2 - Nao)\n'))

  return f'./filtros/{filtros[action]}', True if adiciona == 1 else False

def sum_matriz(matriz):
  sum_r = 0
  sum_g = 0
  sum_b = 0

  for i in range(len(matriz[0])):
    for j in range(len(matriz[0])):
      sum_r += matriz[i][j][0]
      sum_g += matriz[i][j][1]
      sum_b += matriz[i][j][2]

  return [sum_r, sum_b, sum_g]

def aplicar_correlacao():
  os.system('cls' if os.name == 'nt' else 'clear')

  imagem = selecionar_imagem()
  filtro, zeros = selecionar_filtro()

  imagem = cv2.imread(f'data/{imagem}')
  i = 0
  j = 0
  matriz = []

  with open(filtro, 'r') as arquivo_filtro:
    for linha in arquivo_filtro:
      info_linha = linha.split(' ')
      linha = []
      for info in info_linha:
        linha.append(int(info))

      matriz.append(linha)

  size = len(matriz[0])
  # [altura, largura] = imagem.shape
  # nova_imagem = [[0 for _ in range(altura + 2 - size + 1)] for _ in range(largura + 2 - size + 1)]

  altura, largura, _ = imagem.shape
  filtro_altura, filtro_largura = [5, 5]
  
  # Calcula o padding para manter o mesmo tamanho da imagem de saída
  padding_vertical = filtro_altura // 2
  padding_horizontal = filtro_largura // 2
  
  # Adiciona o padding à imagem original
  imagem_com_padding = np.pad(imagem, ((padding_vertical, padding_vertical), (padding_horizontal, padding_horizontal), (0, 0)), mode='constant')
  
  # Inicializa uma matriz para armazenar a imagem filtrada
  imagem_filtrada = np.zeros_like(imagem)
  
  # Aplica o filtro à imagem
  for y in range(altura):
    for x in range(largura):
      for canal in range(3):  # Loop através dos canais RGB
        regiao = imagem_com_padding[y:y+filtro_altura, x:x+filtro_largura, canal]
        pixel_filtrado = np.sum(regiao * matriz)
        imagem_filtrada[y, x, canal] = pixel_filtrado


  cv2.imshow('Imagem Original', imagem)
  cv2.imshow('Imagem Filtro Programa', imagem_filtrada)
  cv2.imshow('Imagem Filtro OpenCV', cv2.GaussianBlur(imagem, (5, 5), 0))

  cv2.waitKey(0)
  cv2.destroyAllWindows()


def conversao_RGB_HSB():
  os.system('cls' if os.name == 'nt' else 'clear')
  
  selected = selecionar_imagem()
  imagem = cv2.imread(f'data/{selected}')
  rgb = imagem
  hsb = np.empty_like(rgb)

  for i in range(0, rgb.shape[0]):
    for j in range(0, rgb.shape[1]):
      [r, g, b] = rgb[i][j]

      # Encontra qual a cor dominante e a cor menos destacada
      maxRGB = max(r, g, b)
      minRGB = min(r, g, b)
      # Cálculo do delta
      delta = maxRGB - minRGB
      h = 0
      s = 0
      v = maxRGB

      match maxRGB:
        # Caso Max = R
        case int(r):
          h = 60 * (((g - b) / delta))
        # Caso Max = G
        case int(g):
          h = 60 * (((b - r) / delta)) + 120
        # Caso Max = B
        case int(b):
          h = 60 * (((r - g) / delta)) + 240

      # Cálculo de S, igual a 0 caso max igual a 0
      if maxRGB == 0:
        s = 0
      # Caso seja diferente de 0
      else:
        s = delta / maxRGB

      hsb[i][j] = np.array([h, s, v])
     

  cv2.imshow('Imagem Original', rgb)
  cv2.imshow('Imagem HSB Programa', hsb)
  convertida = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
  cv2.imshow('Imagem HSB OpenCV', convertida)

  cv2.waitKey(0)
  cv2.destroyAllWindows()

def filtro_saturacao_brilho():
  return 0

def atribuir_saturacao():
  return 0

exit = False

while exit == False:
  match print_menu():
    case 1:
      conversao_RGB_HSB()
    case 2:
      filtro_saturacao_brilho()
    case 3:
      atribuir_saturacao()
    case 4:
      aplicar_correlacao()
    case 5:
      exit = True
    case _:
      print('Opção inválida!')
      print_menu()