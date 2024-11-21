
library(forecast)
library(tidyverse)

set.seed(123)

servidor1 <- data.frame(
  data = seq(as.Date("2024-06-01"), as.Date("2024-11-01"), by = "month"),
  custo = c(0, 0, 0.15, 0.25, 1.08, 1.45)
)


meses_previsao <- 9

ts_data <- ts(servidor1$custo, frequency = 12)


modelo <- tslm(ts_data ~ trend)
modelo


previsao <- forecast(modelo, h = meses_previsao)


previsao


datas_futuras <- seq(max(servidor1$data) + 1, by = "month", length.out = length(previsao$mean))
resultados_df <- data.frame(
  data = datas_futuras,
  custo = as.numeric(previsao$mean),
  tipo = "Previsão"
)

dados_historicos <- servidor1
dados_historicos$tipo <- "Real"

# Combinando dados históricos e previsões
dados_completos <- rbind(
  dados_historicos,
  resultados_df
)

dados_completos$servidor <- "Servidor 1"

cores <- c("Real" = "#2196F3", "Previsão" = "#FF9800")

ggplot(dados_completos, 
       aes(x = data, y = custo, fill = tipo)) +
  geom_bar(stat = "identity", position = "dodge", width = 15) +
  scale_fill_manual(values = cores) +
  theme_minimal() +
  labs(title = "Custos AWS - Servidor 1",
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





# Calculando preço da LAMBDA:

# Roda a cada 10 segundos, ou seja, 360 vezes por hora. Um mes tem aproximadamente 720 horas
total_execucoes = 360 * 720
# Cada csv tem 435 Bytes
tamanho_total_dados = 435 * total_execucoes
# arredondando para mb
tamanho_total_dados <- round(tamanho_total_dados / (1024^2), 2)

# A LAMBDA cobra por uso de RAM por segundo (GB-segundo)

#informações do cloudWatch
memoria_alocada = 0.5 #0.5 GB ou seja 512 mb
duracao_media = 0.2 #segundos

duracao_gb_segundos = total_execucoes * duracao_media * memoria_alocada
duracao_gb_segundos

preco_gb_segundo = 0.0000166667

preco_lambda = duracao_gb_segundos * preco_gb_segundo
preco_lambda

#custos aws:
custo_leitura_s3 = 0.0004 # por 1000
custo_gravacao_s3 = 0.005 # por 1000
custo_leitura_total =  (total_execucoes / 1000)  * custo_leitura_s3
custo_gravacao_total = (total_execucoes / 1000)  * custo_gravacao_s3

custo_leitura_total
custo_gravacao_total

custo_s3 = custo_gravacao_total + custo_leitura_total
custo_s3

custo_total = custo_s3 + preco_lambda
custo_total




