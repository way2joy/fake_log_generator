# load packages
library(dplyr)
library(ggplot2)

# read file
raw_logs <- read.csv('./single_fake_logs.csv', 
                     stringsAsFactors = FALSE, 
                     col.names = c('cid', 'datetime'))
str(raw_logs)

# Calculates session intervals
raw_logs <- tbl_df(raw_logs)
raw_logs$datetime <- as.POSIXct(raw_logs$datetime, 
                                format = '%Y-%m-%d %H:%M:%S', 
                                tz = 'UTC')
interval_logs <- 
  raw_logs %>%
  group_by(cid) %>%
  mutate(next_datetime = lead(datetime),
         interval_days = as.integer(difftime(next_datetime, 
                                            datetime, 
                                            unit = 'days'))) %>%
  filter(interval_days > 0 & !is.na(interval_days)) %>%
  mutate(interval_number = row_number(datetime),
         last_lapse = as.integer(difftime(as.POSIXct('2015-03-31 23:59:59',
                                                     format = '%Y-%m-%d %H:%M:%S',
                                                     tz = 'UTC'),
                                          max(next_datetime),
                                          unit = 'days')),
         churn = as.integer(last_lapse > 8))

# Calculates the rate of churn users
cnt_churn <- 
  interval_logs %>%
  ungroup %>%
  filter(churn == TRUE) %>%
  summarise(cnt_churn = n_distinct(cid))

as.integer(cnt_churn) / length(unique(interval_logs$cid))

# Calculates the means of intervals
rr_logs <- 
  interval_logs %>%
  group_by(cid) %>%
  summarise(mean_interval = mean(interval_days),
            risk_ratio = max(last_lapse) / mean_interval,
            churn = max(churn))

# Fit logistic regression
fit <- glm(churn ~ risk_ratio, data = rr_logs, family = binomial())

# Draws curve
df_curve = data.frame(risk_ratio = rr_logs$risk_ratio, 
                      p_churn = predict(fit, type="response"))
plot(df_curve$risk_ratio, df_curve$p_churn, xlim = c(0, 5), type = 'p', cex = .1)

ggplot(df_curve, aes(risk_ratio, p_churn)) + 
  geom_line() +
  xlab('Risk Ratio') +
  ylab('Probability of Churn') +
  xlim(0, 5) +
  ylim(0, 1) +
  annotate("text", x = 4, y = 0.1, label = "Prop.Churn==over(1, 1 + exp(9.3552 - 4.6795 %*% RR))", parse = TRUE, size = 5) +
  theme_bw(base_size = 12, base_family = "")

ggsave(file='single_churn_curve.png')
