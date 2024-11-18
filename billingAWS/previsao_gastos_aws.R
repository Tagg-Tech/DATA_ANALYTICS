
meses_aws1 <- c("Setembro", "Outubro", "Novembro")
custos_aws1 <- c(1.13, 1.89, 1.18)


meses_aws2 <- c("Agosto", "Setembro", "Outubro", "Novembro")
custos_aws2 <- c(0.12, 0.27, 1.10, 1.40)


tempo_aws1 <- c(9, 10, 11)  
tempo_aws2 <- c(8, 9, 10, 11)  


df_aws1 <- data.frame(Tempo = tempo_aws1, Custo = custos_aws1)
df_aws2 <- data.frame(Tempo = tempo_aws2, Custo = custos_aws2)


modelo_aws1 <- lm(Custo ~ Tempo, data = df_aws1)
modelo_aws2 <- lm(Custo ~ Tempo, data = df_aws2)


summary(modelo_aws1)
summary(modelo_aws2)



tempo_previsao <- data.frame(Tempo = 11.5) 
previsao_aws1 <- predict(modelo_aws1, tempo_previsao)
previsao_aws2 <- predict(modelo_aws2, tempo_previsao)

cat("Previsão AWS 1 (Novembro Completo):", previsao_aws1, "\n")
cat("Previsão AWS 2 (Novembro Completo):", previsao_aws2, "\n")



if (!require(ggplot2)) install.packages("ggplot2")
library(ggplot2)


ggplot(df_aws1, aes(x = Tempo, y = Custo)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE, color = "blue") +
  labs(title = "Regressão Linear - AWS 1", x = "Tempo (mês)", y = "Custo ($)") +
  theme_minimal()

ggplot(df_aws2, aes(x = Tempo, y = Custo)) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE, color = "red") +
  labs(title = "Regressão Linear - AWS 2", x = "Tempo (mês)", y = "Custo ($)") +
  theme_minimal()




