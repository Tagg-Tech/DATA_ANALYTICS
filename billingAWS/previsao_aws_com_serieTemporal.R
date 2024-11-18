# Carregando bibliotecas necessárias
library(forecast)
library(tidyverse)

# Dados do primeiro servidor
servidor1 <- data.frame(
  data = seq(as.Date("2024-06-01"), as.Date("2024-11-01"), by = "month"),
  vpc = c(0, 0, 0.08, 0.12, 0.70, 0.80),
  ec2 = c(0, 0, 0.05, 0.08, 0.25, 0.50),
  compute = c(0, 0, 0.02, 0.05, 0.13, 0.15)
)

# Dados do segundo servidor
servidor2 <- data.frame(
  data = seq(as.Date("2024-06-01"), as.Date("2024-11-01"), by = "month"),
  vpc = c(0, 0, 0, 0.2, 0.3, 0.8),
  ec2 = c(0, 0, 0, 0.8, 1.4, 0.3),
  compute = c(0, 0, 0, 0.2, 0.3, 0.2)
)

# Função para fazer previsão usando regressão linear
fazer_previsao <- function(dados, servico, meses_previsao = 9) {
  ts_data <- ts(dados[[servico]], frequency = 12)
  modelo <- tslm(ts_data ~ trend)
  previsao <- forecast(modelo, h = meses_previsao)
  return(previsao)
}


# Função para calcular previsões para todos os serviços
prever_todos_servicos <- function(servidor, nome_servidor) {
  servicos <- c("vpc", "ec2", "compute")
  resultados <- list()
  
  for(servico in servicos) {
    previsao <- fazer_previsao(servidor, servico)
    resultados[[servico]] <- previsao
  }
  
  # Criar dataframe com resultados
  datas_futuras <- seq(max(servidor$data), by = "month", length.out = 10)
  
  resultados_df <- data.frame(
    data = datas_futuras,
    vpc = c(tail(servidor$vpc, 1), resultados$vpc$mean),
    ec2 = c(tail(servidor$ec2, 1), resultados$ec2$mean),
    compute = c(tail(servidor$compute, 1), resultados$compute$mean)
  )
  
  # Calcular total mensal
  resultados_df$total <- rowSums(resultados_df[, c("vpc", "ec2", "compute")])
  resultados_df$tipo <- "Previsão"
 
  
  # Preparar dados históricos
  dados_historicos <- servidor
  dados_historicos$total <- rowSums(dados_historicos[, c("vpc", "ec2", "compute")])
  dados_historicos$tipo <- "Real"
  
  
  
  # Combinar dados históricos e previsões
  dados_completos <- rbind(
    dados_historicos,
    resultados_df[, names(dados_historicos)]
  )
  
  dados_completos$servidor <- nome_servidor
  return(dados_completos)
}




# Fazer previsões para ambos os servidores
previsoes_servidor1 <- prever_todos_servicos(servidor1, "Servidor 1")
previsoes_servidor2 <- prever_todos_servicos(servidor2, "Servidor 2")



# Combinar resultados
todas_previsoes <- rbind(previsoes_servidor1, previsoes_servidor2)

# Nova função para plotar resultados em barras
plotar_previsoes_barras <- function(previsoes, servidor) {
  # Definir cores
  cores <- c("Real" = "#2196F3", "Previsão" = "#FF9800")
  
  # Criar o gráfico
  ggplot(previsoes %>% filter(servidor == !!servidor), 
         aes(x = data, y = total, fill = tipo)) +
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
plot1 <- plotar_previsoes_barras(todas_previsoes, "Servidor 1")
plot2 <- plotar_previsoes_barras(todas_previsoes, "Servidor 2")

# Para visualizar os gráficos, execute:
print(plot1)
print(plot2)

ggsave("previsao_servidor1.png", plot1, width = 10, height = 6)
ggsave("previsao_servidor2.png", plot2, width = 10, height = 6)
