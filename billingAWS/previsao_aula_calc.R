library(forecast)
library(tidyverse)
set.seed(123)

df <- data.frame(
  data = seq(as.Date("2024-01-01"), as.Date("2024-10-01"), by ="month"),
  custo = c(57, 65, 80, 47, 57, 90, 58, 85, 52, 67)
)


meses_previsao <- 5


ts_data <- ts(df$custo, frequency = 12)


modelo <- tslm(ts_data ~trend)

modelo

#Aqui o modelo pega a coluna que contem os custos e define cada dado como de um "periodo" dentro do total de 12 
#Simbolizando os meses do ano
previsao <- forecast(modelo, h = meses_previsao)

previsao


datas_futuras <- seq(max(df$data) + 1, by = "month", length.out = length(previsao$mean))
resultados_df <- data.frame(
  data = datas_futuras,
  custo = as.numeric(previsao$mean),
  tipo = "Previsão"
)



dados_historicos <- df
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

