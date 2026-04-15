# Required Libraries
library(readxl)
library(tidyverse)
library(janitor)
library(stringr)

# Helper functions

# Cleans BMI dataset and extracts 5–17 years estimates
clean_bmi_5_17 <- function(file_path, sheet_name) {
  read_excel(
    path = file_path,
    sheet = sheet_name,
    skip = 7,
    col_names = TRUE
  ) %>%
    clean_names() %>%
    remove_empty("cols") %>%
    rename(category = 1) %>%
    filter(!is.na(category)) %>%
    mutate(
      sex_group = case_when(
        category == "Persons" ~ "Persons",
        category == "Males" ~ "Males",
        category == "Females" ~ "Females",
        TRUE ~ NA_character_
      )
    ) %>%
    fill(sex_group, .direction = "down") %>%
    filter(
      category %in% c("Underweight", "Normal", "Overweight", "Obese", "Overweight / Obese")
    ) %>%
    mutate(
      bmi_5_17_years = as.numeric(.[[ncol(.) - 1]]),
      bmi_group = paste0(sex_group, "_", str_replace_all(category, " / ", "_"))
    ) %>%
    select(bmi_group, bmi_5_17_years)
}

# Cleans fruit and vegetable consumption dataset and derives 5–17 years estimates
clean_fruit_veg_5_17 <- function(file_path, sheet_name) {
  raw <- read_excel(
    path = file_path,
    sheet = sheet_name,
    skip = 8,
    col_names = FALSE
  ) %>%
    remove_empty("cols") %>%
    set_names(c(
      "category",
      "age_2_3",
      "age_4_8",
      "age_9_11",
      "age_12_13",
      "age_14_17",
      "age_2_4",
      "age_15_17",
      "total_2_17_years"
    )) %>%
    filter(!is.na(category)) %>%
    mutate(
      across(
        c(age_2_3, age_4_8, age_9_11, age_12_13, age_14_17, age_2_4, age_15_17, total_2_17_years),
        as.numeric
      ),
      sex_group = case_when(
        category == "Persons" ~ "Persons",
        category == "Males" ~ "Males",
        category == "Females" ~ "Females",
        TRUE ~ NA_character_
      )
    ) %>%
    fill(sex_group, .direction = "down")
  
  value_cols <- c(
    "age_2_3",
    "age_4_8",
    "age_9_11",
    "age_12_13",
    "age_14_17",
    "age_2_4",
    "age_15_17",
    "total_2_17_years"
  )
  cleaned <- raw %>%
    mutate(
      section_heading = if_else(
        if_all(all_of(value_cols), is.na),
        category,
        NA_character_
      )
    ) %>%
    fill(section_heading, .direction = "down") %>%
    filter(
      !if_all(all_of(value_cols), is.na),
      category != sex_group
    ) %>%
    mutate(
      age_5_17 = total_2_17_years - age_2_4
    ) %>%
    select(category, sex_group, section_heading, age_5_17)
  
  persons_5_17 <- cleaned %>%
    filter(sex_group == "Persons") %>%
    select(category, section_heading, age_5_17) %>%
    filter(
      !str_starts(section_heading, "Number"),
      !str_starts(section_heading, "Average")
    ) %>%
    rename(persons_5_17 = age_5_17)
  
  males_5_17 <- cleaned %>%
    filter(sex_group == "Males") %>%
    select(category, section_heading, age_5_17) %>%
    filter(
      !str_starts(section_heading, "Number"),
      !str_starts(section_heading, "Average")
    ) %>%
    rename(males_5_17 = age_5_17)
  
  females_5_17 <- cleaned %>%
    filter(sex_group == "Females") %>%
    select(category, section_heading, age_5_17) %>%
    filter(
      !str_starts(section_heading, "Number"),
      !str_starts(section_heading, "Average")
    ) %>%
    rename(females_5_17 = age_5_17)
  
  persons_5_17 %>%
    left_join(males_5_17, by = c("category", "section_heading")) %>%
    left_join(females_5_17, by = c("category", "section_heading")) %>%
    arrange(section_heading, category)
}

# Cleans overweight and obesity dataset and aggregates ages 6–13
clean_table_s7 <- function(file_path, sheet_name) {
  raw <- read_excel(
    path = file_path,
    sheet = sheet_name,
    skip = 3,
    col_names = FALSE
  ) %>%
    remove_empty("cols") %>%
    select(1:12)
  
  names(raw) <- c(
    "age",
    "survey_year",
    "underweight_pct",
    "underweight_ci",
    "normal_weight_pct",
    "normal_weight_ci",
    "overweight_not_obese_pct",
    "overweight_not_obese_ci",
    "obese_pct",
    "obese_ci",
    "overweight_obese_pct",
    "overweight_obese_ci"
  )
  
  final <- raw %>%
    filter(!is.na(age)) %>%
    mutate(
      sex_group = case_when(
        age %in% c("All children", "Boys", "Girls") ~ age,
        TRUE ~ NA_character_
      )
    ) %>%
    fill(sex_group, .direction = "down") %>%
    filter(
      !age %in% c("All children", "Boys", "Girls"),
      age != "Age",
      !is.na(survey_year)
    ) %>%
    select(
      sex_group,
      age,
      survey_year,
      underweight_pct,
      normal_weight_pct,
      overweight_not_obese_pct,
      obese_pct,
      overweight_obese_pct
    ) %>%
    mutate(
      survey_year = as.numeric(survey_year),
      underweight_pct = as.numeric(underweight_pct),
      normal_weight_pct = as.numeric(normal_weight_pct),
      overweight_not_obese_pct = as.numeric(overweight_not_obese_pct),
      obese_pct = as.numeric(obese_pct),
      overweight_obese_pct = as.numeric(overweight_obese_pct)
    )
  
  final %>%
    filter(age %in% c("6–7", "8–9", "10–11", "12–13")) %>%
    group_by(sex_group, survey_year) %>%
    summarise(
      underweight_6_13 = sum(underweight_pct, na.rm = TRUE),
      normal_6_13 = sum(normal_weight_pct, na.rm = TRUE),
      overweight_not_obese_6_13 = sum(overweight_not_obese_pct, na.rm = TRUE),
      obese_6_13 = sum(obese_pct, na.rm = TRUE),
      overweight_obese_6_13 = sum(overweight_obese_pct, na.rm = TRUE),
      .groups = "drop"
    )
}

# Cleans two-column proportion datasets (category and 5–17 value)
clean_two_col_proportions <- function(file_path, sheet_name) {
  read_excel(
    path = file_path,
    sheet = sheet_name,
    skip = 7,
    col_names = FALSE
  ) %>%
    remove_empty("cols") %>%
    select(1, last_col()) %>%
    set_names(c("category", "value_5_17")) %>%
    mutate(
      section_heading = if_else(is.na(value_5_17), category, NA_character_)
    ) %>%
    fill(section_heading, .direction = "down") %>%
    filter(!is.na(value_5_17)) %>%
    mutate(
      value_5_17 = as.numeric(str_replace_all(as.character(value_5_17), "#", ""))
    ) %>%
    select(category, section_heading, value_5_17)
}

# Cleans and restructures sleep dataset for 5–17 years
clean_sleep_proportions <- function(file_path, sheet_name) {
  clean_two_col_proportions(file_path, sheet_name) %>%
    filter(!str_detect(category, regex("^Total persons$", ignore_case = TRUE))) %>%
    mutate(
      section_clean = case_when(
        str_detect(section_heading, "weeknight") ~ "Weeknight",
        str_detect(section_heading, "weekend") ~ "Weekend night",
        str_detect(section_heading, "per night") ~ "Per night",
        TRUE ~ section_heading
      ),
      category = paste(section_clean, category)
    ) %>%
    select(category, value_5_17)
}

# Cleans National Health Survey estimates for persons all ages
clean_nhsdc01_estimates <- function(file_path, sheet_name) {
  raw <- read_excel(
    path = file_path,
    sheet = sheet_name,
    skip = 5,
    col_names = FALSE
  ) %>%
    remove_empty("cols")
  
  colnames(raw) <- c(
    "category",
    "y2001",
    "y2004_05",
    "y2007_08",
    "y2011_12",
    "y2014_15",
    "y2017_18",
    "y2022"
  )
  
  raw %>%
    filter(!is.na(category)) %>%
    slice(1:21) %>%
    mutate(
      section_heading = if_else(
        if_all(starts_with("y"), is.na),
        category,
        NA_character_
      )
    ) %>%
    fill(section_heading, .direction = "down") %>%
    filter(!if_all(starts_with("y"), is.na)) %>%
    mutate(across(
      starts_with("y"),
      ~ as.numeric(str_replace_all(as.character(.), "[^0-9.]", ""))
    )) %>%
    mutate(
      section_heading = str_trim(str_remove_all(section_heading, "\\(.*?\\)"))
    ) %>%
    {
      names(.) <- gsub("^y", "", names(.))
      .
    }
}

# Cleans long-term health conditions dataset with hierarchical structure
clean_nhsdc03_sheet <- function(file_path, sheet_name) {
  year_cols <- c("2001", "2004_05", "2007_08", "2011_12", "2014_15", "2017_18", "2022")
  
  raw <- read_excel(
    path = file_path,
    sheet = sheet_name,
    skip = 5,
    col_names = FALSE,
    trim_ws = FALSE
  ) %>%
    remove_empty("cols") %>%
    select(1:8)
  
  names(raw) <- c("category", year_cols)
  
  raw <- raw %>%
    filter(!is.na(category)) %>%
    mutate(
      category = as.character(category),
      category = str_squish(category),
      all_years_blank = if_all(all_of(year_cols), is.na)
    )
  
  n <- nrow(raw)
  section_heading_vec <- rep(NA_character_, n)
  section_subheading_vec <- rep(NA_character_, n)
  
  current_section <- NA_character_
  current_subheading <- NA_character_
  previous_data_category <- NA_character_
  
  for (i in seq_len(n)) {
    current_category <- raw$category[i]
    current_blank <- raw$all_years_blank[i]
    
    clean_label <- str_trim(str_remove_all(current_category, "\\(.*?\\)"))
    clean_label_lower <- str_to_lower(clean_label)
    
    if (current_blank) {
      if (clean_label_lower %in% c("persons", "males", "females", "persons all ages")) {
        next
      }
      
      if (
        is.na(current_section) ||
        (!is.na(previous_data_category) && str_detect(previous_data_category, regex("^total\\b", ignore_case = TRUE)))
      ) {
        current_section <- clean_label
        current_subheading <- NA_character_
      } else {
        current_subheading <- clean_label
      }
    } else {
      section_heading_vec[i] <- current_section
      section_subheading_vec[i] <- current_subheading
      previous_data_category <- clean_label
      
      if (
        !is.na(current_subheading) &&
        str_detect(clean_label, regex("^total\\b", ignore_case = TRUE))
      ) {
        current_subheading <- NA_character_
      }
    }
  }
  
  raw %>%
    mutate(
      section_heading = section_heading_vec,
      section_subheading = section_subheading_vec
    ) %>%
    filter(!all_years_blank) %>%
    mutate(
      category = str_trim(str_remove_all(category, "\\(.*?\\)")),
      section_heading = str_trim(str_remove_all(section_heading, "\\(.*?\\)")),
      section_subheading = str_trim(str_remove_all(section_subheading, "\\(.*?\\)")),
      across(
        all_of(year_cols),
        ~ as.numeric(str_replace_all(as.character(.), "[^0-9.]", ""))
      )
    ) %>%
    select(category, all_of(year_cols), section_heading, section_subheading)
}

# Cleans nutrition mean intake dataset with section headings and units
clean_means_table <- function(file_path, sheet_name) {
  read_excel(
    path = file_path,
    sheet = sheet_name,
    skip = 5,
    col_names = FALSE,
    trim_ws = FALSE
  ) %>%
    remove_empty("cols") %>%
    select(1:11) %>%
    set_names(c(
      "category",
      "unit",
      "age_2_4",
      "age_5_11",
      "age_12_17",
      "age_18_29",
      "age_30_49",
      "age_50_64",
      "age_65_74",
      "age_75_plus",
      "age_2_17"
    )) %>%
    filter(!is.na(category)) %>%
    mutate(row_id = row_number()) %>%
    {
      footnote_row <- which(str_detect(str_to_lower(.$category), "^footnotes$"))
      if (length(footnote_row) > 0) slice(., 1:(min(footnote_row) - 1)) else .
    } %>%
    select(-row_id) %>%
    mutate(
      category = str_squish(as.character(category)),
      unit = str_squish(as.character(unit)),
      unit = na_if(unit, ""),
      all_value_cols_blank = if_all(
        c(age_2_4, age_5_11, age_12_17, age_18_29, age_30_49, age_50_64, age_65_74, age_75_plus, age_2_17),
        is.na
      ),
      section_heading = if_else(all_value_cols_blank, category, NA_character_)
    ) %>%
    fill(section_heading, .direction = "down") %>%
    filter(!all_value_cols_blank) %>%
    mutate(
      category = str_trim(str_remove_all(category, "\\(.*?\\)")),
      section_heading = str_trim(str_remove_all(section_heading, "\\(.*?\\)")),
      unit = str_trim(str_remove_all(unit, "\\(.*?\\)"))
    ) %>%
    mutate(across(
      c(age_2_4, age_5_11, age_12_17, age_18_29, age_30_49, age_50_64, age_65_74, age_75_plus, age_2_17),
      ~ as.numeric(str_replace_all(as.character(.), "[^0-9.]", ""))
    )) %>%
    mutate(
      age_5_17 = rowMeans(cbind(age_5_11, age_12_17), na.rm = TRUE)
    ) %>%
    select(category, unit, section_heading, age_5_17)
}

# Cleans simplified mean intake dataset without section headings or units
clean_means_table_simple <- function(file_path, sheet_name) {
  read_excel(
    path = file_path,
    sheet = sheet_name,
    skip = 5,
    col_names = FALSE,
    trim_ws = FALSE
  ) %>%
    remove_empty("cols") %>%
    select(1:10) %>%
    set_names(c(
      "category",
      "age_2_4",
      "age_5_11",
      "age_12_17",
      "age_18_29",
      "age_30_49",
      "age_50_64",
      "age_65_74",
      "age_75_plus",
      "age_2_17"
    )) %>%
    filter(!is.na(category)) %>%
    mutate(
      category = str_squish(as.character(category))
    ) %>%
    filter(
      !if_all(
        c(age_2_4, age_5_11, age_12_17, age_18_29, age_30_49, age_50_64, age_65_74, age_75_plus, age_2_17),
        is.na
      )
    ) %>%
    mutate(
      category = str_trim(str_remove_all(category, "\\(.*?\\)"))
    ) %>%
    mutate(across(
      c(age_2_4, age_5_11, age_12_17, age_18_29, age_30_49, age_50_64, age_65_74, age_75_plus, age_2_17),
      ~ as.numeric(str_replace_all(as.character(.), "[^0-9.]", ""))
    )) %>%
    mutate(
      age_5_17 = rowMeans(cbind(age_5_11, age_12_17), na.rm = TRUE)
    ) %>%
    select(category, age_5_17)
}

# BMI
bmi_5_17 <- clean_bmi_5_17(
  file_path = "4364055001do016_20172018.xls",
  sheet_name = "Table 16.1_Estimates"
)

View(bmi_5_17)

write_csv(
  bmi_5_17,
  "processed/bmi_5_17.csv"
)



# Fruits and vegetables consumption

table_17_1_combined_5_17 <- clean_fruit_veg_5_17(
  file_path = "4364055001do017_20172018_1.xls",
  sheet_name = "Table 17.1_Estimates"
)

table_17_1_combined_5_17 <- table_17_1_combined_5_17 %>%
  mutate(
    section_heading = str_remove_all(section_heading, "\\([abc]\\)"),
    category = str_remove_all(category, "\\([abc]\\)")
  )

View(table_17_1_combined_5_17)

write_csv(
  table_17_1_combined_5_17,
  "processed/fruits_and_veg_consumption_5_17.csv"
)



# Overweight and obesity, ages 6 to 13
table_s7_6_13 <- clean_table_s7(
  file_path = "aihw-phe-274-supplementary-tables (1).xlsx",
  sheet_name = "Table S7"
)

View(table_s7_6_13)

write_csv(
  table_s7_6_13,
  "processed/overweight_2010_2016.csv"
)



# Physical inactivity
table_1_1_physical_inactivity <- clean_two_col_proportions(
  file_path = "MPASDC03.xlsx",
  sheet_name = "Table 1.1_Proportions"
) %>%
  mutate(
    category = str_remove_all(category, "\\(.*?\\)")
  )

View(table_1_1_physical_inactivity)

write_csv(
  table_1_1_physical_inactivity,
  "processed/physical_inactivity.csv"
)



# Sleep
table_1_1_sleep_final <- clean_sleep_proportions(
  file_path = "MPASDC04.xlsx",
  sheet_name = "Table 1.1_Proportions"
)

View(table_1_1_sleep_final)

write_csv(
  table_1_1_sleep_final,
  "processed/sleep_weekend_week.csv"
)



# National Health Survey, persons all ages
table_1_1_est_clean <- clean_nhsdc01_estimates(
  file_path = "NHSDC01.xlsx",
  sheet_name = "Table 1.1_Estimates"
)

table_1_1_est_clean <- table_1_1_est_clean %>%
  mutate(
    category = str_remove_all(category, "\\(.*?\\)")
  )

View(table_1_1_est_clean)

write_csv(
  table_1_1_est_clean,
  "processed/National_Health_Survey_Persons_All_Ages.csv"
)



# National Health Survey, long term conditions
table_3_1_estimates_persons <- clean_nhsdc03_sheet(
  file_path = "NHSDC03.xlsx",
  sheet_name = "Table 3.1_Estimates Persons"
)

table_3_5_estimates_males <- clean_nhsdc03_sheet(
  file_path = "NHSDC03.xlsx",
  sheet_name = "Table 3.5_Estimates Males"
)

table_3_9_estimates_females <- clean_nhsdc03_sheet(
  file_path = "NHSDC03.xlsx",
  sheet_name = "Table 3.9_Estimates Females"
)

View(table_3_1_estimates_persons)
View(table_3_5_estimates_males)
View(table_3_9_estimates_females)

write_csv(
  table_3_1_estimates_persons,
  "processed/National_Health_Survey_Long_Term_Persons.csv"
)
write_csv(
  table_3_5_estimates_males,
  "processed/National_Health_Survey_Long_Term_Males.csv"
)
write_csv(
  table_3_9_estimates_females,
  "processed/National_Health_Survey_Long_Term_Females.csv"
)



# NNPAS nutrition

table_1_1_means_persons <- clean_means_table(
  file_path = "NNPASDC01.xlsx",
  sheet_name = "Table 1.1_Means Persons"
)

table_1_3_means_males <- clean_means_table(
  file_path = "NNPASDC01.xlsx",
  sheet_name = "Table 1.3_Means Males"
)

table_1_5_means_females <- clean_means_table(
  file_path = "NNPASDC01.xlsx",
  sheet_name = "Table 1.5_Means Females"
)

View(table_1_1_means_persons)
View(table_1_3_means_males)
View(table_1_5_means_females)

nnpas_nutrition_persons <- table_1_1_means_persons %>%
  rename(avg_person = age_5_17)

nnpas_nutrition_males <- table_1_3_means_males %>%
  rename(avg_males = age_5_17)

nnpas_nutrition_females <- table_1_5_means_females %>%
  rename(avg_females = age_5_17)

combined_means_5_17 <- nnpas_nutrition_persons %>%
  left_join(
    nnpas_nutrition_males,
    by = c("category", "unit", "section_heading")
  ) %>%
  left_join(
    nnpas_nutrition_females,
    by = c("category", "unit", "section_heading")
  )

View(combined_means_5_17)

write_csv(
  combined_means_5_17,
  "processed/NNPAS_Nutrition.csv"
)



# NNPAS foods and beverages
table_5_1_persons <- clean_means_table_simple(
  file_path = "NNPASDC05.xlsx",
  sheet_name = "Table 5.1_Means Persons"
)

table_5_3_males <- clean_means_table_simple(
  file_path = "NNPASDC05.xlsx",
  sheet_name = "Table 5.3_Means Males"
)

table_5_5_females <- clean_means_table_simple(
  file_path = "NNPASDC05.xlsx",
  sheet_name = "Table 5.5_Means Females"
)

View(table_5_1_persons)
View(table_5_3_males)
View(table_5_5_females)

nnpas_foods_persons <- table_5_1_persons %>%
  rename(avg_person_g = age_5_17)

nnpas_foods_males <- table_5_3_males %>%
  rename(avg_males_g = age_5_17)

nnpas_foods_females <- table_5_5_females %>%
  rename(avg_females_g = age_5_17)

combined_table_5 <- nnpas_foods_persons %>%
  left_join(nnpas_foods_males, by = "category") %>%
  left_join(nnpas_foods_females, by = "category")

View(combined_table_5)

write_csv(
  combined_table_5,
  "processed/NNPAS_Foods_and_Beverages.csv"
)