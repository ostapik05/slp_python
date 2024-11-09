import matplotlib.pyplot as plt
import seaborn as sns
from labs.lab8.bll.DataFrameUtils import *
import logging
logger = logging.getLogger(__name__)


def plot_steps_vs_calories(activity_source):
    activity = activity_source.copy()
    split_date_column(activity, "date")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=activity.reset_index(), x="steps", y="calories", hue="weekDay",
                    palette="viridis")
    return plt


def plot_rem_and_bed_time(sleep_source):
    sleep = sleep_source.copy()
    split_date_column(sleep, "start", "start")
    round_all_columns(sleep)
    scale_hour_minute(sleep, "startHour", "startMinute", "startHourComplex",
                      True, 15)
    sleep['totalSleepTime'] = sleep['deepSleepTime'] + sleep['shallowSleepTime'] + sleep['wakeTime'] + sleep['REMTime']
    plt.figure(figsize=(10, 6))
    sns.regplot(data=sleep, x="REMTime", y="startHourComplex", scatter=False, color="blue",
                label="REM by at the time of falling asleep")
    sns.scatterplot(data=sleep.reset_index(), x="REMTime", y="startHourComplex",
                    hue="totalSleepTime", palette="viridis", hue_order="Total Sleep Time")
    plt.title("REM Time vs. Bed Time")
    plt.xlabel("REM Time (minutes)")
    plt.ylabel("Bed Time (in 2 days)")
    plt.legend()
    return plt


def plot_sleep_activity_relationships (activity_source, sleep_source):
    activity = activity_source.copy()
    sleep = sleep_source.copy()
    split_date_column(activity, "date")
    change_naps(sleep, "naps")
    split_date_column(sleep, "start", "start")
    columns = [("year", "startYear"), ("month", "startMonth"), ("day", "startDay")]
    activity_sleep = combine_dataframes_on_columns(activity, sleep, columns)
    activity_sleep['totalSleepTime'] = activity_sleep['deepSleepTime'] + activity_sleep['shallowSleepTime'] + \
                                       activity_sleep['wakeTime'] + activity_sleep['REMTime']
    activity_sleep = remove_rows_with_empty_cells(activity_sleep)
    remove_columns_list = ['weekDay', 'date', 'stop', 'start', 'startWeekDay']
    remove_columns_by_names(activity_sleep, remove_columns_list)
    round_all_columns(activity_sleep)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=activity_sleep.reset_index(), x="totalSleepTime", y="steps", legend="full",
                    hue="naps", palette="viridis")
    sns.regplot(data=activity_sleep[activity_sleep["naps"] == 0], x="totalSleepTime", y="steps",
                scatter=False, color="blue", label="No naps", ci=None)
    sns.regplot(data=activity_sleep[activity_sleep["naps"] == 1], x="totalSleepTime", y="steps",
                scatter=False, color="green", label="With naps", ci=None)
    plt.title("Sleep Time vs. Daily Steps")
    plt.xlabel("Sleep Time")
    plt.ylabel("Daily Steps")
    plt.legend()
    return plt


def plot_steps_by_date(activity_source):
    activity = activity_source.copy()
    plt.figure(figsize=(10, 6))
    activity['date'] = pd.to_datetime(activity['date'])
    sns.scatterplot(data=activity.reset_index(), x="date", y="steps", marker='o', s = 10)
    plt.title("Steps taken")
    plt.xlabel("Date")
    plt.ylabel("Steps")
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())
    return plt


def plot_steps_by_years(activity_source):
    activity = activity_source.copy()
    activity['date'] = pd.to_datetime(activity['date'])
    activity['year'] = activity['date'].dt.year
    years = activity['year'].unique()
    num_years = len(years)
    fig, axs = plt.subplots(num_years, 1, figsize=(10, 6 * num_years))
    for i, year in enumerate(years):
        ax = axs[i] if num_years > 1 else axs
        year_data = activity[activity['year'] == year]
        sns.scatterplot(data=year_data.reset_index(), x="date", y="steps", marker='o', s=10, ax=ax)
        ax.set_title(f"Steps taken in {year}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Steps")
        ax.tick_params(axis='x', rotation=45)
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
        ax.set_xlim(pd.Timestamp(f'{year}-01-01'), pd.Timestamp(f'{year}-12-31'))

    plt.tight_layout()
    return plt


def plot_sleep_duration(activity_source, sleep_source):
    activity = activity_source.copy()
    sleep = sleep_source.copy()
    split_date_column(activity, "date")
    change_naps(sleep, "naps")
    split_date_column(sleep, "start", "start")
    split_date_column(sleep, "stop", "stop")
    remove_column_by_name(sleep, "stopYear")
    remove_column_by_name(sleep, "stopMonth")
    columns = [("year", "startYear"), ("month", "startMonth"), ("day", "startDay")]
    activity_sleep = combine_dataframes_on_columns(activity, sleep, columns)
    remove_columns_list = ['Hour', 'Minute', 'stopMonth', 'stopMonth', 'distance', 'runDistance']
    remove_columns_by_names(activity_sleep, remove_columns_list)
    activity_sleep['totalSleepTime'] = activity_sleep['deepSleepTime'] + activity_sleep['shallowSleepTime'] + \
                                       activity_sleep['wakeTime'] + activity_sleep['REMTime']

    activity_sleep = remove_rows_with_empty_cells(activity_sleep)
    round_all_columns(activity_sleep)
    scale_hour_minute(activity_sleep, "startHour", "startMinute", "startHourComplex",
                                             True, 15)
    scale_hour_minute(activity_sleep, "stopHour", "stopMinute", "stopHourComplex",
                                             True, 15)
    plt.figure(figsize=(10, 6))

    activity_sleep['date'] = pd.to_datetime(activity_sleep['date'])
    start_median_inertia = activity_sleep['startHourComplex'].rolling(window=7, min_periods=1).median()
    stop_median_inertia = activity_sleep['stopHourComplex'].rolling(window=7, min_periods=1).median()

    plt.fill_between(x=activity_sleep['date'], y1=start_median_inertia, y2=stop_median_inertia,
                     color="skyblue", alpha=0.4, label="Sleep Duration Median (Inertia)")
    plt.title("Sleep Duration by Date (with Median Inertia)")
    plt.xlabel("Date")
    plt.ylabel("Time (in 2 days combined)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())
    explanation_text = ("Hour Complex represents combined hours over approximately 48-hour windows.\n"
                        "The graph utilizes a rolling median with a window of 7 days to smooth out short-term fluctuations.")
    plt.figtext(0.5, -0.1, explanation_text, wrap=True, horizontalalignment='center', fontsize=10)
    return plt


def plot_correlation_heatmap(activity_source, sleep_source):
    activity = activity_source.copy()
    sleep = sleep_source.copy()
    split_date_column(activity, "date")
    change_naps(sleep, "naps")
    split_date_column(sleep, "start", "start")
    split_date_column(sleep, "stop", "stop")
    columns = [("year", "startYear"), ("month", "startMonth"), ("day", "startDay")]
    activity_sleep = combine_dataframes_on_columns(activity, sleep, columns)
    remove_columns_list = ['naps','Hour',"stopYear",'stopMonth', 'Minute', 'stopMonth', 'stopMonth', 'distance', 'runDistance', "weekDay", "date", "stopWeekDay", "startWeekDay"]
    remove_columns_by_names(activity_sleep, remove_columns_list)
    activity_sleep['totalSleepTime'] = activity_sleep['deepSleepTime'] + activity_sleep['shallowSleepTime'] + \
                                       activity_sleep['wakeTime'] + activity_sleep['REMTime']

    activity_sleep = remove_rows_with_empty_cells(activity_sleep)
    round_all_columns(activity_sleep)
    scale_hour_minute(activity_sleep, "startHour", "startMinute", "startHourComplex",
                      True, 15)
    scale_hour_minute(activity_sleep, "stopHour", "stopMinute", "stopHourComplex",
                      True, 15)
    plt.figure(figsize=(12, 10))
    heatmap = sns.heatmap(activity_sleep.corr(), annot=True, fmt='.2f', xticklabels=True, yticklabels=True,
                          linewidth=.1, vmin=0, vmax=1, cmap='coolwarm')
    heatmap.xaxis.tick_top()
    plt.title("Correlation Heatmap")
    plt.xlabel("Features")
    plt.ylabel("Features")
    return plt


def plot_sleep_patterns_by_day(sleep_source):
    sleep = sleep_source.copy()
    split_date_column(sleep, "date")
    sleep['totalSleepTime'] = sleep['deepSleepTime'] + sleep['shallowSleepTime'] + sleep['wakeTime'] + sleep['REMTime']
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='weekDay', y='totalSleepTime', data=sleep)
    plt.title('Sleep Patterns by Day of the Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Total Sleep Time (minutes)')
    return plt



def plot_sleep_phases_distribution(sleep_source):
    sleep = sleep_source.copy()
    sleep_phases = sleep[['deepSleepTime', 'shallowSleepTime', 'wakeTime', 'REMTime']].mean()
    plt.figure(figsize=(8, 8))
    sleep_phases.plot.pie(autopct='%1.1f%%', startangle=90)
    plt.title('Average Sleep Phases Distribution')
    plt.ylabel('')
    return plt


def plot_nap_days_per_month(sleep_source):
    sleep = sleep_source.copy()
    split_date_column(sleep, "start", "start")
    remove_column_by_name(sleep, "stopYear")
    remove_column_by_name(sleep, "stopMonth")
    columns = [("year", "startYear"), ("month", "startMonth"), ("day", "startDay")]
    sleep['napDays'] = sleep['naps'].apply(lambda x: "Yes" if x else "No")
    activity_sleep = remove_rows_with_empty_cells(sleep)
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(x=activity_sleep['startMonth'], hue=activity_sleep['napDays'])
    ax.set_title("Days with naps")
    ax.set(xlabel='Month', ylabel='Naps')
    ax.legend_.remove()
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%M'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())
    return plt

def plot_monthly_activity_summary(activity):
    activity['date'] = pd.to_datetime(activity['date'])
    monthly_steps = activity.groupby(activity['date'].dt.to_period('M'))['steps'].sum()
    monthly_steps.index = monthly_steps.index.astype(str)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=monthly_steps.index, y=monthly_steps.values, palette="coolwarm")
    plt.title('Total Steps Taken Each Month')
    plt.xlabel('Month')
    plt.ylabel('Total Steps')
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())
    plt.xticks(rotation=45)
    return plt

def plot_monthly_sleep_patterns(sleep):
    sleep['start'] = pd.to_datetime(sleep['start'])
    sleep['stop'] = pd.to_datetime(sleep['stop'])

    sleep['month'] = sleep['start'].dt.month
    sleep['totalSleepTime'] = sleep['deepSleepTime'] + sleep['shallowSleepTime'] + sleep['wakeTime'] + sleep['REMTime']

    plt.figure(figsize=(12, 6))
    sns.boxplot(x='month', y='totalSleepTime', data=sleep)
    plt.title('Monthly Sleep Patterns')
    plt.xlabel('Month')
    plt.ylabel('Total Sleep Time (minutes)')
    return plt

def plot_rem_sleep_vs_steps(activity, sleep):
    sleep['start'] = pd.to_datetime(sleep['start'])
    sleep['stop'] = pd.to_datetime(sleep['stop'])
    sleep['date'] = sleep['start'].dt.date
    activity['date'] = pd.to_datetime(activity['date']).dt.date

    combined_df = pd.merge(sleep, activity, on='date', how='inner')
    split_date_column(combined_df, "date")
    remove_rows_with_empty_cells(combined_df)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=combined_df, x='REMTime', y='steps', hue='weekDay', palette='viridis')
    sns.regplot(data=combined_df, x='REMTime', y='steps', scatter=False, color='blue')
    plt.title('Correlation Between REM Sleep Time and Steps Taken')
    plt.xlabel('REM Sleep Time (minutes)')
    plt.ylabel('Steps')
    return plt



def plot_calories_vs_sleep_time(activity_source, sleep_source):
    activity = activity_source.copy()
    sleep = sleep_source.copy()
    split_date_column(activity, "date")
    change_naps(sleep, "naps")
    split_date_column(sleep, "start", "start")
    split_date_column(sleep, "stop", "stop")
    remove_column_by_name(sleep, "stopYear")
    remove_column_by_name(sleep, "stopMonth")
    columns = [("year", "startYear"), ("month", "startMonth"), ("day", "startDay")]
    activity_sleep = combine_dataframes_on_columns(activity, sleep, columns)
    remove_columns_list = ['Hour', 'Minute', 'stopMonth', 'stopMonth', 'distance', 'runDistance']
    remove_columns_by_names(activity_sleep, remove_columns_list)
    activity_sleep['totalSleepTime'] = activity_sleep['deepSleepTime'] + activity_sleep['shallowSleepTime'] + \
                                       activity_sleep['wakeTime'] + activity_sleep['REMTime']

    activity_sleep = remove_rows_with_empty_cells(activity_sleep)
    round_all_columns(activity_sleep)
    scale_hour_minute(activity_sleep, "startHour", "startMinute", "startHourComplex",
                      True, 15)
    scale_hour_minute(activity_sleep, "stopHour", "stopMinute", "stopHourComplex",
                      True, 15)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='totalSleepTime', y='calories', data=activity_sleep)
    plt.title('Calories Burned vs. Total Sleep Time')
    plt.xlabel('Total Sleep Time (minutes)')
    plt.ylabel('Calories Burned')
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.AutoDateLocator())
    return plt