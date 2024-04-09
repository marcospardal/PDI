import os
import cv2
import numpy as np
import math

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
      j = 0
      for info in info_linha:
        linha.append(int(info))

      matriz.append(linha)

  size = len(matriz[0])
  # [altura, largura] = imagem.shape
  # nova_imagem = [[0 for _ in range(altura + 2 - size + 1)] for _ in range(largura + 2 - size + 1)]

  altura, largura, _ = imagem.shape
  filtro_altura, filtro_largura = 5, 5
  
  # Calcula o padding para manter o mesmo tamanho da imagem de saída
  padding_vertical = filtro_altura // 2
  padding_horizontal = filtro_largura // 2
  
  # Adiciona o padding à imagem original
  imagem_com_padding = np.pad(imagem, ((padding_vertical, padding_vertical), (padding_horizontal, padding_horizontal), (0, 0)), mode='constant')
  
  # Inicializa uma matriz para armazenar a imagem filtrada
  imagem_filtrada = np.zeros_like(imagem)
  
  # Aplica o filtro à imagem
  for i in range(altura):
    for j in range(largura):
      for c in range(3):
        regiao = imagem_com_padding[i:i+filtro_altura, j:j+filtro_largura, c]
        imagem_filtrada[i, j, c] = np.sum(regiao * matriz)


  cv2.imshow('Imagem Original', imagem)
  cv2.imshow('Imagem Filtro Programa', imagem_filtrada)
  cv2.imshow('Imagem Filtro OpenCV', cv2.GaussianBlur(imagem, (5, 5), 0))

  cv2.waitKey(0)
  cv2.destroyAllWindows()

def conversao_HSB_RGB(hsb):
  os.system('cls' if os.name == 'nt' else 'clear')

  imagem_rgb = np.empty_like(hsb)

  for i in range(0, hsb.shape[0]):
    for j in range(0, hsb.shape[1]):
      [h, s, b] = hsb[i][j]

      if (s == 0):
        r = b
        g = b
        b = b
      else:
        sectorPos = h / 60.0
        sectorNumber = int(math.floor(sectorPos))
        fractionalSector = sectorPos - sectorNumber

        p = b * (1.0 - s)
        q = b * (1.0 - (s * fractionalSector))
        t = b * (1.0 - (s * (1 - fractionalSector)))

        match (sectorNumber):
          case 0:
            r = b
            g = t
            b = p
          case 1:
            r = q
            g = b
            b = p
          case 2:
            r = p
            g = b
            b = t
          case 3:
            r = p
            g = q
            b = b
          case 4:
            r = t
            g = p
            b = b
          case 5:
            r = b
            g = p
            b = q
          case 6:
            r = b
            g = t
            b = p

      imagem_rgb[i][j] = np.array([r, g, b], dtype=np.uint32)

  return imagem_rgb

def conversao_RGB_HSB():
  os.system('cls' if os.name == 'nt' else 'clear')
  
  selected = selecionar_imagem()
  imagem = cv2.imread(f'data/{selected}')
  rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
  hsb = np.empty_like(rgb)

  for i in range(0, rgb.shape[0]):
    for j in range(0, rgb.shape[1]):
      [r, g, b] = rgb[i][j]

      maxRGB = max(r, g, b)
      minRGB = min(r, g, b)
      delta = maxRGB - minRGB
      
      # Calcula o brilho (Value)
      v = maxRGB
      
      # Calcula a saturação (Saturation)
      if maxRGB == 0:
        s = 0
      else:
        s = 1.0 - (minRGB / maxRGB)
      
      h = 0
      if maxRGB == r:
        if (g >= b):
          h = 60 * ((g - b) / delta)
        else:
          h = 60 * ((g - b) / delta) + 360
      elif maxRGB == g:
        h = 60 * ((b - r) / delta) + 120
      elif maxRGB == b:
        h = 60 * ((r - g) / delta) + 240
      
      hsb[i][j] = [h, s, v]
    

  return hsb, rgb

def filtro_saturacao_brilho():
  os.system('cls' if os.name == 'nt' else 'clear')

  hue_value = int(input('Adicione o valor do aditivo da matriz\n'))
  saturation_value = int(input('Adicione o fator do filtro de saturação\n'))
  bright_value = int(input('Adicione o fator do filtro de brilho\n'))

  hsb, img = conversao_RGB_HSB()

  nova_imagem = np.empty_like(hsb)

  for i in range(0, nova_imagem.shape[0]):
    for j in range(0, nova_imagem.shape[1]):
      [h, s, v] = hsb[i][j]
      novoH = (h + hue_value)

      novoS = s * saturation_value
      novoV = v * bright_value

      nova_imagem[i][j] = np.array([novoH, novoS, novoV])

  final = conversao_HSB_RGB(nova_imagem)
  
  cv2.imshow('Imagem Original', img)
  cv2.imshow('Imagem Final', final)
  
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  return 0

def atribuir_saturacao():
  os.system('cls' if os.name == 'nt' else 'clear')

  hsv_original, imagem_original = conversao_RGB_HSB()
  hsv_destino, imagem_destino = conversao_RGB_HSB()

  saturacao_origem = hsv_original[:,:,1]
  hsv_destino[:,:,1] = saturacao_origem

  cv2.imshow('Imagem Original', imagem_original)
  cv2.imshow('Imagem Destino', imagem_destino)
  cv2.imshow('Imagem Destino com saturação original', hsv_destino)


  cv2.waitKey(0)
  cv2.destroyAllWindows()

  return 0

exit = False

while exit == False:
  match print_menu():
    case 1:
      hsv, img = conversao_RGB_HSB()
      cv2.imshow('Imagem Original', img)
      cv2.imshow('Imagem HSB Programa', hsv)

      cv2.waitKey(0)
      cv2.destroyAllWindows()

      print('Conversão de volta para rgb')

      convertendo_rgb = conversao_HSB_RGB(hsv)
      cv2.imshow('Imagem Original', img)
      cv2.imshow('Imagem Programa', convertendo_rgb)

      cv2.waitKey(0)
      cv2.destroyAllWindows()
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