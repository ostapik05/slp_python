import pandas as pd


def split_date_column(data, date_column, new_prefix=None):
    data[date_column] = pd.to_datetime(data[date_column])
    year_name = "year" if new_prefix is None else f"{new_prefix}Year"
    month_name = "month" if new_prefix is None else f"{new_prefix}Month"
    day_name = "day" if new_prefix is None else f"{new_prefix}Day"
    day_of_week_name = "weekDay" if new_prefix is None else f"{new_prefix}WeekDay"
    hour_name = "hour" if new_prefix is None else f"{new_prefix}Hour"
    minute_name = "minute" if new_prefix is None else f"{new_prefix}Minute"
    data[year_name] = data[date_column].dt.year.astype(int)
    data[month_name] = data[date_column].dt.month.astype(int)
    data[day_name] = data[date_column].dt.day.astype(int)
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    data[day_of_week_name] = data[date_column].dt.dayofweek.map(day_names)
    # data[day_of_week_name] = data[date_column].dt.dayofweek.astype(int)
    if data[date_column].dt.time.nunique() > 1:
        data[hour_name] = data[date_column].dt.hour.astype(int)
        data[minute_name] = data[date_column].dt.minute.astype(int)
    data.drop(columns=[date_column], inplace=True)


def combine_dataframes_on_columns(df1, df2, columns):
    combined_df = pd.merge(df1, df2, left_on=[col[0] for col in columns], right_on=[col[1] for col in columns],
                           how='outer', suffixes=('_left', '_right'))
    combined_df = combined_df.drop_duplicates(subset=[col[0] for col in columns], keep='first')
    combined_df.columns = combined_df.columns.str.replace('_left|_right', '', regex=True)
    return combined_df


def change_naps(df, column):
    df[column] = df[column].apply(lambda x: "With nap" if pd.notna(x) and x != "" else "Without nap")


def remove_column_by_name(df, column_name):
    if column_name in df.columns:
        df.drop(columns=[column_name], inplace=True)


def remove_columns_by_names(df, column_names):
    for column_name in column_names:
        if column_name in df.columns:
            df.drop(columns=[column_name], inplace=True)

def remove_rows_with_empty_cells(df):
    return df.dropna(how='any')


def combine_columns(df, col1, col2, new_col):
    df[new_col] = pd.to_datetime(df[col1].astype(str) + '-' + df[col2].astype(str).str.zfill(2),
                                 format="%d-%m", errors='coerce')


def scale(row, hour_name, minute_name, is_two_days, middle):
    complex_hour = row[hour_name] + row[minute_name] / 60
    if is_two_days and complex_hour < middle:
        complex_hour += 24
    return round(complex_hour, 2)


def scale_hour_minute(df, hour_name, minute_name, new_hour_name, is_two_days=False, middle=15):
    df[new_hour_name] = df.apply(lambda row: scale(row, hour_name, minute_name, is_two_days, middle), axis=1)
    return df


def round_all_columns(df):
    numeric_cols = df.select_dtypes(include='number').columns
    df[numeric_cols] = df[numeric_cols].apply(lambda x: x.round().astype(int))
    return df