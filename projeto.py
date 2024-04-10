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

  return f'./data/{imagens[action]}'

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
        r = max(0, min(int(r), 255))
        g = max(0, min(int(g), 255))
        b = max(0, min(int(b), 255))

      imagem_rgb[i][j] = (r, g, b)

  return imagem_rgb

def conversao_RGB_HSB():
  os.system('cls' if os.name == 'nt' else 'clear')
  
  selected = selecionar_imagem()
  imagem = cv2.imread(f'data/{selected}')
  # rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
  rgb = imagem
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
      
      hsb[i][j] = (h, s, v)
    

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

      nova_imagem[i][j] = (novoH, novoS, novoV)

  final = conversao_HSB_RGB(nova_imagem)
  
  cv2.imshow('Imagem Original', img)
  cv2.imshow('Imagem Final', final)
  
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  return 0

def atribuir_saturacao():
  os.system('cls' if os.name == 'nt' else 'clear')

  hsb, imagem_original = conversao_RGB_HSB()
  hsb_destino, imagem_destino = conversao_RGB_HSB()

  for i in range(0, hsb.shape[0]):
    for j in range(0, hsb.shape[1]):
      hsb_destino[i][j][1] = hsb[i][j][1]


  imagem_final = conversao_HSB_RGB(hsb_destino)

  cv2.imshow('Imagem Original', imagem_original)
  cv2.imshow('Imagem Destino', imagem_destino)
  cv2.imshow('Imagem Destino HSB', hsb_destino)
  cv2.imshow('Imagem Destino com saturação original', imagem_final)

  cv2.waitKey(0)
  cv2.destroyAllWindows()

  return 0

# Função para aplicar correlação em uma imagem com um filtro específico
def correlacao_gauss_box(imagem, filtro):
    # Obtém as dimensões da imagem e do filtro
    altura, largura, _ = imagem.shape

    m, n = filtro.shape
    
    # Calcula o padding necessário
    altura_borda = m // 2
    largura_borda = n // 2
    
    # Cria uma nova imagem para armazenar o resultado da correlação
    imagem_resultante = np.zeros_like(imagem)
    
    # Aplica a correlação para cada canal de cor (R, G, B)
    for c in range(3):
        # Preenche a imagem com o valor do padding
        img_bordada = np.pad(imagem[:,:,c], ((altura_borda, altura_borda), (largura_borda, largura_borda)), mode='constant')
        
        # Correlação
        for i in range(altura):
            for j in range(largura):
                imagem_resultante[i, j, c] = np.sum(img_bordada[i:i+m, j:j+n] * filtro)
    
    # Garante que os valores estejam dentro do intervalo [0, 255]
    imagem_resultante = np.clip(imagem_resultante, 0, 255)
    imagem_resultante = imagem_resultante.astype(np.uint8)
    
    return imagem_resultante

# Função para aplicar a correlação m x n sobre um canal de cor
def correlacao_sobel(img, filtro):
    altura, largura = img.shape
    m, n = filtro.shape
    borda_vertical = m // 2
    borda_horizontal = n // 2

    # Adicionando borda à imagem para tratamento de bordas
    img_bordada = cv2.copyMakeBorder(img, borda_vertical, borda_vertical, borda_horizontal, borda_horizontal, cv2.BORDER_CONSTANT)

    # Inicializando imagem resultado
    img_resultado = np.zeros_like(img, dtype=np.float32)

    # Aplicando a correlação
    for i in range(altura):
        for j in range(largura):
            regiao = img_bordada[i:i+m, j:j+n]
            img_resultado[i, j] = np.sum(regiao * filtro)

    return img_resultado

# Função para expandir histograma
def expandir_histograma(img):
    min_val = np.min(img)
    max_val = np.max(img)
    img_expandida = (img - min_val) * (255.0 / (max_val - min_val))
    return img_expandida.astype(np.uint8)


def aplicar_correlacao():
  os.system('cls' if os.name == 'nt' else 'clear')

  imagem = selecionar_imagem()
  filtro, zeros = selecionar_filtro()

  # Carregar filtros a partir dos arquivos de texto
  with open(filtro, 'r') as file:
    filtro_escolhido = np.array([[float(num) for num in line.split(' ')] for line in file.readlines()], dtype=np.float32)

  # Carrega a imagem
  imagem_escolhida = cv2.imread(imagem)

  # Aplicar a correlação com o filtro escolhido
  if 'sobel-horizontal' in filtro:
    canal_r, canal_g, canal_b = cv2.split(imagem_escolhida)
    
    # Aplicando a correlação e valor absoluto para cada canal
    resultado_r_horizontal = np.abs(correlacao_sobel(canal_r, filtro_escolhido))
    resultado_g_horizontal = np.abs(correlacao_sobel(canal_g, filtro_escolhido))
    resultado_b_horizontal = np.abs(correlacao_sobel(canal_b, filtro_escolhido))

    # Expandindo histograma
    resultado_r_horizontal_expandido = expandir_histograma(resultado_r_horizontal)
    resultado_g_horizontal_expandido = expandir_histograma(resultado_g_horizontal)
    resultado_b_horizontal_expandido = expandir_histograma(resultado_b_horizontal)

    # Juntando os canais novamente
    resultado_final = cv2.merge((resultado_r_horizontal_expandido, resultado_g_horizontal_expandido, resultado_b_horizontal_expandido))

  elif 'sobel-vertical' in filtro:
    canal_r, canal_g, canal_b = cv2.split(imagem_escolhida)
    
    # Aplicando a correlação e valor absoluto para cada canal
    resultado_r_vertical = np.abs(correlacao_sobel(canal_r, filtro_escolhido))
    resultado_g_vertical = np.abs(correlacao_sobel(canal_g, filtro_escolhido))
    resultado_b_vertical = np.abs(correlacao_sobel(canal_b, filtro_escolhido))

    # Expandindo histograma
    resultado_r_vertical_expandido = expandir_histograma(resultado_r_vertical)
    resultado_g_vertical_expandido = expandir_histograma(resultado_g_vertical)
    resultado_b_vertical_expandido = expandir_histograma(resultado_b_vertical)

    # Juntando os canais novamente
    resultado_final = cv2.merge((resultado_r_vertical_expandido, resultado_g_vertical_expandido, resultado_b_vertical_expandido))

  else:
    resultado_final = correlacao_gauss_box(imagem_escolhida, filtro_escolhido)
    
  # Redimensionar as imagens resultantes para as dimensões desejadas
  resultado_final = cv2.resize(resultado_final, (800, 600))
  imagem_escolhida = cv2.resize(imagem_escolhida, (800, 600))

  # Exibindo resultados
  cv2.imshow('Imagem original', imagem_escolhida)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  cv2.imshow('Imagem com filtro escolhido', resultado_final)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


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