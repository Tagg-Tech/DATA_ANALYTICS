library(forecast)
library(tidyverse)

servidor1 <- data.frame(
  data = seq(as.Date("2024-06-01"), as.Date("2024-11-01"), by = "month"),
  custo = c(0, 0, 0.15, 0.25, 1.08, 1.45)
)

servidor2 <- data.frame(
  data = seq(as.Date("2024-06-01"), as.Date("2024-11-01"), by = "month"),
  custo = c(0, 0, 0, 1.2, 2.0, 1.3)
)

fazer_previsao <- function(dados) {
  meses_previsao <- 9
  ts_data <- ts(dados$custo, frequency = 12) 
  
  #Aqui o modelo pega a coluna que contem os custos e define cada dado como de um "periodo" dentro do total de 12 
  #Simbolizando os meses do ano
  
  modelo <- tslm(ts_data ~ trend)
  #tslm = Time Series lm 
  #Trend representa o tempo (meses no caso)
  # tslm 
  
  previsao <- forecast(modelo, h = meses_previsao)
  return(previsao)
}

# Função para prever custos
prever_custos <- function(servidor, nome_servidor) {
  previsao <- fazer_previsao(servidor)
  
  # Criar dataframe com previsões
  datas_futuras <- seq(max(servidor$data) + 1, by = "month", length.out = length(previsao$mean))
  resultados_df <- data.frame(
    data = datas_futuras,
    custo = as.numeric(previsao$mean), # Apenas as previsões
    tipo = "Previsão"
  )
  
  # Preparar dados históricos
  dados_historicos <- servidor
  dados_historicos$tipo <- "Real"
  
  # Combinar dados históricos e previsões
  dados_completos <- rbind(
    dados_historicos,
    resultados_df
  )
  
  dados_completos$servidor <- nome_servidor
  return(dados_completos)
}


# Fazer previsões para ambos os servidores
previsoes_servidor1 <- prever_custos(servidor1, "Servidor 1")
previsoes_servidor2 <- prever_custos(servidor2, "Servidor 2")

# Combinar resultados
todas_previsoes <- rbind(previsoes_servidor1, previsoes_servidor2)

# Nova função para plotar resultados em barras
plotar_previsoes_barras <- function(previsoes, servidor) {
  # Definir cores
  cores <- c("Real" = "#2196F3", "Previsão" = "#FF9800")
  
  # Criar o gráfico
  ggplot(previsoes %>% filter(servidor == !!servidor), 
         aes(x = data, y = custo, fill = tipo)) +
    geom_bar(stat = "identity", position = "dodge", width = 15) +
    scale_fill_manual(values = cores) +
    theme_minimal() +
    labs(title = paste("Custos AWS -", servidor),
         subtitle = "Valores reais e previsões",
         x = "Data",
         y = "Custo Total ($)",
         fill = "Tipo de Dado") +
    scale_x_date(date_breaks = "1 month", 
                 date_labels = "%b %Y",
                 expand = expansion(mult = c(0.02, 0.02))) +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1),
      legend.position = "top",
      panel.grid.major.x = element_blank(),
      panel.grid.minor.x = element_blank()
    )
}

# Plotar os gráficos
plotar_previsoes_barras(todas_previsoes, "Servidor 1")
plotar_previsoes_barras(todas_previsoes, "Servidor 2")


# Salvar os gráficos
ggsave("previsao_servidor1.png", plot1, width = 10, height = 6)
ggsave("previsao_servidor2.png", plot2, width = 10, height = 6)

