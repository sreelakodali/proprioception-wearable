library(stats)
library(PMCMRplus)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(ggplot2)
library(ggpubr)
library(coin)
library(ez)

set.seed(123)


#data <- read.csv("C:\\Users\\kyosh\\Desktop\\Sreela_Analysis_20230205\\sreelaData.csv")
data <- read.csv("/Users/Sreela/Documents/School/Stanford/Year3_2/PIEZO2/JND_Study/bleData/OverallData_JNDV2.csv")

data <- data %>%
  convert_as_factor(Subject, nPoints, Ref)


summary_stats <- data %>%
  group_by(nPoints, Ref) %>%
  get_summary_stats(JND, type = "mean_sd")
data %>%
  group_by(nPoints, Ref) %>%
  identify_outliers(JND)
data %>%
  group_by(nPoints,Ref) %>%
  shapiro_test(JND)
ggqqplot(data, "JND", ggtheme = theme_bw()) +
  facet_grid(nPoints ~ Ref, labeller = "label_both")
bxp <- ggboxplot(
  data, x = "nPoints", y = "JND",
  color = "Ref", palette = "jco"
)
bxp

res.aov <- anova_test(
  data = data, dv = JND, wid = Subject,
  within = c(nPoints, Ref), effect.size = "pes"
)
get_anova_table(res.aov, correction = 'GG')


one.way <- data %>%
  group_by(Ref) %>%
  anova_test(dv = JND, wid = Subject, within = nPoints) %>%
  get_anova_table() %>%
  adjust_pvalue(method = "bonferroni")
one.way


# Pairwise comparisons between treatment groups
pwc <- data %>%
  group_by(Ref) %>%
  pairwise_t_test(
    JND ~ nPoints, paired = TRUE,
    p.adjust.method = "bonferroni"
  )
pwc


# get summary stats
d<-data %>%
  group_by(Ref) %>%
  get_summary_stats(JND, type = "mean_sd")
d


one.way2 <- data %>%
  group_by(nPoints) %>%
  anova_test(dv = JND, wid = Subject, within = Ref) %>%
  get_anova_table() %>%
  adjust_pvalue(method = "bonferroni")
one.way2


# Pairwise comparisons between treatment groups
pwc2 <- data %>%
  group_by(nPoints) %>%
  pairwise_t_test(
    JND ~ Ref, paired = TRUE,
    p.adjust.method = "bonferroni"
  )
pwc2

# get summary stats
d2<-data %>%
  group_by(nPoints) %>%
  get_summary_stats(JND, type = "mean_sd")
d2


# Perform the two-way repeated measures ANOVA
res.aov <- ezANOVA(
  data = data, 
  dv = JND, 
  wid = Subject,
  within = c(nPoints, Ref),
  detailed = TRUE, 
  type = 3
)

# Print the ANOVA results
print(res.aov)
