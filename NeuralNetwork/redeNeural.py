import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.utils import np_utils
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization

#X e Y de treinamento servem para treinar. X->entradas de treinamento e Y->saídas de treinamento. O mesmo vale para X e Y de teste
(X_treinamento, y_treinamento), (X_teste, y_teste) = mnist.load_data()#Base de dados do MNIST
plt.imshow(X_treinamento[0], cmap = 'gray')#Mostrando as imagens de teste na tela(Plots)
plt.title('Classe '+str(y_treinamento[0]))#Atribui a imagem da saída correta o nome de Classe(olhar em Plots)

#Convertendo para um formato de o tensorFlow é capaz de trabalhar
previsores_treinamento = X_treinamento.reshape(X_treinamento.shape[0], 28, 28, 1)#Parametro1-> quantidade de dados(imagens), Parametro 2->altura das imagens, Parametro 3-> largura das imagens, Parametro 4->Quantidade de canais que serão utilizados nas imagens
previsores_teste = X_teste.reshape(X_teste.shape[0], 28, 28, 1)
#Modificando o tipo de dado para float32
previsores_treinamento = previsores_treinamento.astype('float32')
previsores_teste = previsores_teste.astype('float32')
#Aplicando técnica para facilitar o processamento, deixando os valores preenchidos no vetor de imagens em uma escala entre 0 e 1
previsores_treinamento /= 255
previsores_teste /= 255
#Convertendo para variaveis do tipo dummy(0 1 0) . . . 2
classe_treinamento = np_utils.to_categorical(y_treinamento, 10)#O último parametro é o número de classes que queremos fazer a transformação
classe_teste = np_utils.to_categorical(y_teste, 10)

#Estrutura da rede neural convolucional
classificador = Sequential()
#Camada de Convolução
#Conv2D representra a camda de convolução(conjunto de mapa de características) e seus parametros são:
#1-> quantidade de kernels que serão testados para descobrir qual o melhor deles
#2-> tamanho da matriz kernel
#3-> input_shape representa o formato de entrada da nossa imagem de entrada(28,28,1(quantidade de canais))
#4-> função relu que será aplicada na matriz de características
classificador.add(Conv2D(32, (3,3), input_shape=(28,28,1), activation='relu'))
#Camada de normalização->Aplicando normalização nos mapas de características(deixa os valores do mapa entre 0 e 1, para assim melhorar ainda mais o desempenho da IA)
classificador.add(BatchNormalization())
#Camada de Pooling
classificador.add(MaxPooling2D(pool_size = (2,2)))#pool_size representa o tamanho da matriz que vai extrair os maiores valores da matriz de características
#Camada de Flattening-> só deve ser adicionada ao final das camdas, quando já tivermos adicionado todas as camadas de convolução que iremos utilizar
#classificador.add(Flatten())
#Criando melhorias para a rede neural(adicionando mais camadas)
#Camada de convolução
classificador.add(Conv2D(32, (3,3), activation='relu'))
#Camada de normalização->Aplicando normalização nos mapas de características(deixa os valores do mapa entre 0 e 1, para assim melhorar ainda mais o desempenho da IA)
classificador.add(BatchNormalization())
#Camada de Pooling
classificador.add(MaxPooling2D(pool_size = (2,2)))#pool_size representa o tamanho da matriz que vai extrair os maiores valores da matriz de características
#Camada de Flattening
classificador.add(Flatten())
#Camada oculta 1
classificador.add(Dense(units = 128, activation='relu'))#units é a quantidade de neurônios da camada oculta 1
#Camada de dropout
classificador.add(Dropout(0.2))#Zerando 20% das entradas
#Camada oculta 2
classificador.add(Dense(units = 128, activation='relu'))
#Camada de dropout
classificador.add(Dropout(0.2))#Zerando 20% das entradas
#Camada de saída
classificador.add(Dense(units = 10, activation = 'softmax'))

#Compilando a rede neural convolucional
classificador.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

#Treinando a rede neural
classificador.fit(previsores_treinamento, classe_treinamento, batch_size = 128, epochs = 5, validation_data = (previsores_teste, classe_teste))#validation_data serve para inserir os dados de teste logo após o treinamento de uma época. Dessa forma é possível visualizar o resultados da base de dados de teste já na execução do treinamento de cada época. OBS: Olhar o valor de vall_accuracy no prompt para ter o valor da precisão dos dados de teste
#Validation_data substitui essa função:
resultado = classificador.evaluate(previsores_teste, classe_teste)
