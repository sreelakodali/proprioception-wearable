library(stats)
library(PMCMRplus)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(ggplot2)
library(ggpubr)
library(coin)


set.seed(123)


#data <- read.csv("C:\\Users\\kyosh\\Desktop\\Sreela_Analysis_20230205\\sreelaData.csv")
data <- read.csv("/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/Rcode/Sreela_Analysis_20230205/CSVForR/sreelaData_without28.csv")

data <- data %>%
  convert_as_factor(Subject, Haptic, Visual)




summary_stats <- data %>%
  group_by(Haptic, Visual) %>%
  get_summary_stats(ABSError, type = "mean_sd")
data %>%
  group_by(Haptic, Visual) %>%
  identify_outliers(ABSError)
data %>%
  group_by(Haptic,Visual) %>%
  shapiro_test(ABSError)
ggqqplot(data, "ABSError", ggtheme = theme_bw()) +
  facet_grid(Haptic ~ Visual, labeller = "label_both")
bxp <- ggboxplot(
  data, x = "Haptic", y = "ABSError",
  color = "Visual", palette = "jco"
)
bxp

res.aov <- anova_test(
  data = data, dv = ABSError, wid = Subject,
  within = c(Haptic, Visual), effect.size = "pes"
)
get_anova_table(res.aov, correction = 'GG')




one.way <- data %>%
  group_by(Visual) %>%
  anova_test(dv = ABSError, wid = Subject, within = Haptic) %>%
  get_anova_table() %>%
  adjust_pvalue(method = "bonferroni")
one.way


# Pairwise comparisons between treatment groups
pwc <- data %>%
  group_by(Visual) %>%
  pairwise_t_test(
    ABSError ~ Haptic, paired = TRUE,
    p.adjust.method = "bonferroni"
  )
pwc


# get summary stats
d<-data %>%
  group_by(Haptic) %>%
  get_summary_stats(ABSError, type = "mean_sd")
d











one.way2 <- data %>%
  group_by(Visual) %>%
  anova_test(dv = ABSError, wid = Subject, within = Haptic) %>%
  get_anova_table() %>%
  adjust_pvalue(method = "bonferroni")
one.way2


# Pairwise comparisons between treatment groups
pwc2 <- data %>%
  group_by(Visual) %>%
  pairwise_t_test(
    ABSError ~ Haptic, paired = TRUE,
    p.adjust.method = "bonferroni"
  )
pwc2

# get summary stats
d2<-data %>%
  group_by(Visual) %>%
  get_summary_stats(ABSError, type = "mean_sd")
d2



