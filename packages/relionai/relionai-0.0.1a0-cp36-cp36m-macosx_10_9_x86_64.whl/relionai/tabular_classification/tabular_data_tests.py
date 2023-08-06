# from datetime import datetime, date, timedelta
# from decimal import Decimal
# import random
# import string
# from pytz import timezone
# import pandas as pd
# from pyspark.sql.types import StringType, LongType, IntegerType, DoubleType, DecimalType
# import pyspark.sql.functions as F




# def eda_report(sdf):
#     report = []

#     def format_percent(ratio):
#         return str(round(ratio * 100, 2)) + "%"

#     def format_count(count_integer):
#         if count_integer is not None:
#             return "{:,}".format(count_integer)
#         else:
#             return "NA"

#     for col in sdf.columns:
#         stddev_stats_list = []
#         total_count = sdf.select(col).count()
#         distinct_count = sdf.select(col).distinct().count()
#         max_value = sdf.select(F.max(F.col(col))).collect()[0][0]
#         min_value = sdf.select(F.min(F.col(col))).collect()[0][0]
#         array_count = sdf.select(col).filter(F.col(col).like("[%,%]")).count()
#         struct_count = sdf.select(col).filter(F.col(col).like("{%,%}")).count()
#         try:
#             date_count = (
#                 sdf.select(col)
#                 .withColumn(col, F.to_date(F.col(col)))
#                 .filter(~F.col(col).isNull())
#                 .count()
#             )
#         except Exception:
#             date_count = 0
#         try:
#             mean_value = sdf.select(F.mean(F.col(col))).collect()[0][0]
#         except Exception:
#             mean_value = None

#         if date_count > 0:
#             current_date = date.today()
#             current_year = date.today().year
#             last_year = int(current_year) - 1
#             second_to_last_year = int(current_year) - 2
#             dates_sdf = (
#                 sdf.select(col)
#                 .withColumn(col, F.to_date(F.col(col)))
#                 .filter(~F.col(col).isNull())
#             )
#             num_distinct_dates_current_year = (
#                 dates_sdf.select(col)
#                 .filter(F.col(col) >= str(date(current_year, 1, 1)))
#                 .distinct()
#                 .count()
#             )
#             num_distinct_dates_last_year = (
#                 dates_sdf.select(col)
#                 .filter(F.col(col) >= str(date(last_year, 1, 1)))
#                 .filter(F.col(col) < str(date(current_year, 1, 1)))
#                 .distinct()
#                 .count()
#             )
#             num_distinct_dates_second_to_last_year = (
#                 dates_sdf.select(col)
#                 .filter(F.col(col) >= str(date(second_to_last_year, 1, 1)))
#                 .filter(F.col(col) < str(date(last_year, 1, 1)))
#                 .distinct()
#                 .count()
#             )
#             dates_over_five_years_ago_sdf = (
#                 dates_sdf.select(col)
#                 .filter(F.col(col) < str(current_date - timedelta(days=5 * 365)))
#                 .distinct()
#             )
#             num_dates_over_five_years_ago = dates_over_five_years_ago_sdf.count()
#             example_dates_over_five_years_ago = (
#                 dates_over_five_years_ago_sdf.select(col)
#                 .orderBy(col, ascending=True)
#                 .limit(5)
#                 .rdd.flatMap(lambda x: x)
#                 .collect()
#             )
#             example_dates_over_five_years_ago = list(
#                 set([str(date) for date in example_dates_over_five_years_ago])
#             )
#         na_count = (
#             sdf.select(F.when((F.col(col).isNull()), 1).otherwise(0).alias(col))
#             .filter(F.col(col) == 1)
#             .count()
#         )
#         if isinstance(sdf.schema[col].dataType, (StringType)):
#             na_count_spaces = (
#                 sdf.select(
#                     F.when((F.trim(F.col(col))) == "", 1).otherwise(0).alias(col)
#                 )
#                 .filter(F.col(col) == 1)
#                 .count()
#             )
#             na_count = na_count + na_count_spaces

#         if isinstance(
#             sdf.schema[col].dataType, (LongType, IntegerType, DoubleType, DecimalType)
#         ):
#             na_count_nan = (
#                 sdf.select(F.when((F.isnan(F.col(col))), 1).otherwise(0).alias(col))
#                 .filter(F.col(col) == 1)
#                 .count()
#             )
#             na_count = na_count + na_count_nan
#             negative_count = sdf.select(col).filter(F.col(col) < 0).count()
#             zero_count = sdf.select(col).filter(F.col(col) == 0).count()
#             col_stddev = (
#                 sdf.withColumn(col, F.col(col).cast("double"))
#                 .agg({col: "stddev"})
#                 .collect()[0][0]
#             )
#             for stddev_multiple in [
#                 (2, "two"),
#                 (5, "five"),
#                 (10, "ten"),
#                 (50, "fifty"),
#                 (100, "one hundred"),
#             ]:
#                 if not col_stddev:
#                     continue
#                 outliers_stdev_sdf = sdf.select(col).filter(
#                     F.col(col) > (stddev_multiple[0] * col_stddev)
#                 )
#                 num_outliers_stddev = outliers_stdev_sdf.count()
#                 percent_outliers_stddev = format_percent(
#                     num_outliers_stddev / total_count
#                 )
#                 example_outliers_stddev_list = (
#                     outliers_stdev_sdf.select(col)
#                     .orderBy(col, ascending=True)
#                     .limit(5)
#                     .rdd.flatMap(lambda x: x)
#                     .collect()
#                 )
#                 example_outliers_stddev_set = set(
#                     [format_count(example) for example in example_outliers_stddev_list]
#                 )
#                 stddev_stats_list.append(
#                     [
#                         stddev_multiple[1],
#                         num_outliers_stddev,
#                         percent_outliers_stddev,
#                         example_outliers_stddev_set,
#                     ]
#                 )
#         else:
#             negative_count = None
#             zero_count = None
#         percent_na = format_percent(na_count / total_count)
#         if negative_count:
#             percent_negative = format_percent(negative_count / total_count)
#             percent_zero = format_percent(zero_count / total_count)
#         else:
#             percent_negative = None
#             percent_zero = None
#         report.append("Column name: " + str(col))
#         report.append("Column type: " + str(sdf.schema[col].dataType))
#         report.append(
#             "Total values: "
#             + format_count(total_count)
#             + " ("
#             + format_percent(distinct_count / total_count)
#             + " unique)"
#         )
#         report.append(
#             "Total NULL values: "
#             + format_count(na_count)
#             + " ("
#             + str(percent_na)
#             + ")"
#         )
#         if percent_negative and percent_zero:
#             report.append(
#                 "Total negative values: "
#                 + format_count(negative_count)
#                 + " ("
#                 + str(percent_negative)
#                 + ")"
#             )
#             report.append(
#                 "Total Zero values: "
#                 + format_count(zero_count)
#                 + " ("
#                 + str(percent_zero)
#                 + ")"
#             )
#         report.append("Highest value: " + str(max_value))
#         report.append("Lowest value: " + str(min_value))
#         if mean_value is not None:
#             report.append("Mean value: " + str(mean_value))
#         for outlier_stats in stddev_stats_list:
#             if outlier_stats[1] > 0:
#                 report.append(
#                     f"Outlier values {outlier_stats[0]} times stddev: "
#                     f" {format_count(outlier_stats[1])} ({outlier_stats[2]})"
#                     f" e.g. {outlier_stats[3]}"
#                 )
#         if array_count > 0:
#             report.append(f"Number of array_type values: {format_count(array_count)}")
#         if struct_count > 0:
#             report.append(f"Number of json_type values: {format_count(struct_count)}")
#         if date_count > 0:
#             report.append(f"Number of valid date_type values: {format_count(date_count)}")
#             report.append(
#                 f"Number of distinct dates in year {current_year}:"
#                 f" {format_count(num_distinct_dates_current_year)}"
#             )
#             report.append(
#                 f"Number of distinct dates in year {last_year}:"
#                 f" {format_count(num_distinct_dates_last_year)}"
#             )
#             report.append(
#                 f"Number of distinct dates in year {second_to_last_year}:"
#                 f" {format_count(num_distinct_dates_second_to_last_year)}"
#             )
#             report.append(
#                 f"Number of distinct valid date_type values from over five years ago: {format_count(num_dates_over_five_years_ago)}"
#                 " e.g."
#                 f" {example_dates_over_five_years_ago}"
#             )
#         report.append(
#             sdf.groupBy(col)
#             .agg(F.count(F.lit(1)).alias("_count"))
#             .sort(F.desc("_count"))
#             .withColumn(
#                 "_percent",
#                 ((F.col("_count") * F.lit(100)) / F.lit(total_count)).cast(
#                     DecimalType(8, 3)
#                 ),
#             )
#             .withColumn("_count", F.format_number(F.col("_count"), 0))
#             ._jdf.showString(5, int(False), False)
#         )
#     return "\n".join(report)