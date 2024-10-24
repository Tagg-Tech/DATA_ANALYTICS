# Criando um vetor com os nomes
nomes <- c("AUTOPISTA FERNÃO DIAS", "AUTOPISTA FERNÃO DIAS", "AUTOPISTA FERNÃO DIAS", "AUTOPISTA LITORAL SUL", "CONCEBRA", "CONCEBRA", "CONCEBRA", "CONCEBRA", "ECO101", "ECOPONTE", "ECORIOMINAS", "ECORIOMINAS", "ECOSUL", "RIOSP")

# Contando a frequência de cada nome
frequencia_nomes <- table(nomes)
frequencia_nomes

# Carregando a biblioteca wordcloud
library(wordcloud)

# Criando a nuvem de palavras
wordcloud(names(frequencia_nomes), 
          freq = frequencia_nomes, 
          min.freq = 1,
          max.words=20,
          rot.per = 0.2,
          scale = c(3, 0), 
          random.order=FALSE, 
          colors=brewer.pal(8, "Dark2")
)

# essas são as concessionárias com maiores chances de uso excessivo dos servidores
#(pois a velocidade média atual dos carros estava abaixo da velocidade livre esperada)
