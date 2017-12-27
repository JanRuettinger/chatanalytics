# coding: utf-8
import pandas as pd
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def preprocess_data(data_raw):
    os_format = check_os(data_raw)

    if os_format == "Android":
        df = preprocess_android(data_raw)
        print("Android preprocessing done")

    elif os_format == "iOS":
        df = preprocess_ios(data_raw)
        print("iOS preprocessing done")

    else:
        print("Error")

    # Check if all lists have the same size
    if check_list_sizes(df):
        print("All lists have the same size!")
    else:
        print("Error: lists have different sizes")

    return df

def open_data(filename):
    # Open whatsapp chat backup
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data_raw = f.read()
            return data_raw
    except:
        return False


def check_os(data_raw):
    '''Check if chat is from Android or iOS client'''

    # Check if data contains android format
    if bool(re.search('\d+.\d+.\d+,\s\d+:\d+ -', data_raw)):
        # Chat is from Android phone
        return "Android"
    else:
        return "iOS"

def preprocess_android(data_raw):
    # ANDROID Split text into messages
    split = re.split('(\d+.\d+.\d+,\s\d+:\d+\s-\s)', data_raw)
    del split[0]
    data_date_message = [split[i]+split[i+1] for i in range(len(split)) if i % 2 == 0]

    # ANDROID Delete all status messages like "Jan has left" or "Jan has changed his security code." except "<image omitted>"
    copied_list = list(data_date_message)
    for e in copied_list:
        if e.count(':') < 2:  # status messages have less than 2 colons
            data_date_message.remove(e)

    # ANDROID Split each message into a date, a sender and a message text
    dates = []
    senders = []
    messages = []
    for e in data_date_message:
        date = re.findall('(^\d+.\d+.\d+,\s\d+:\d+)\s-', e)
        dates.append(date[0])

        sender = re.findall('^\d+.\d+.\d+,\s\d+:\d+\s-\s([^:]+):.*', e)
        senders.append(sender[0])

        message = re.findall('^\d+.\d+.\d+,\s\d+:\d+\s-\s[^:]+:\s(.*)', e)
        messages.append(message[0])

    # ANDROID Create pandas dataframe
    df = pd.DataFrame({'sender': senders, 'date': dates, 'message': messages})

    # ANDROID Convert dates from string to datetime format
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%y, %H:%M')

    return df

def preprocess_ios(data_raw):
    # Chat is from iOS phone

    # Check which date format is used:
    # Option 1: 08.09.16, 09:57:35:
    # Option 2: 8/23/13, 2:14:56 PM:

    if bool(re.search('\d+.\d+.\d+,\s\d+:\d+:\d+:', data_raw)):
        ###  Option 1:  ###
        # Split text into messages
        split = re.split('(\d+.\d+.\d+,\s\d+:\d+:\d+:\s)', data_raw)
        del split[0]
        #print(len(split)) # number of seperated messages
        data_date_message = [split[i]+split[i+1] for i in range(len(split)) if i % 2 == 0]

        # Delete all status messages like "Jan has left" or "Jan has changed his security code." except "<image omitted>"
        copied_list = list(data_date_message)
        for e in copied_list:
            if e.count(':') < 4: #status messages have less than 4 colons
                data_date_message.remove(e)

        # Split each message into a date, a sender and a message text
        dates = []
        senders = []
        messages = []
        for e in data_date_message:
            date = re.findall('(^\d+.\d+.\d+,\s\d+:\d+:\d+):', e)
            dates.append(date[0])

            sender = re.findall('^\d+.\d+.\d+,\s\d+:\d+:\d+:\s([^:]+):.*', e)
            senders.append(sender[0])

            message = re.findall('.+:.+:.+:.+:\s(.*)', e)
            messages.append(message[0])

        # Create pandas dataframe
        df = pd.DataFrame({'sender': senders, 'date': dates, 'message': messages})

        # Convert dates from string to datetime format
        df['date'] = pd.to_datetime(df['date'], format='%d.%m.%y, %H:%M:%S')
        print("Option 1: 08.09.16, 09:57:35:")
        print(df)
    else:
        ### Option 2: ###
        # iOS Split text into messages
        split = re.split('(\d+/\d+/\d+,\s\d+:\d+:\d+\sA?P?M:\s)', data_raw)
        del split[0]
        # print(len(split)) # number of seperated messages
        data_date_message = [split[i]+split[i+1] for i in range(len(split)) if i % 2 == 0]

        # iOs Delete all status messages like "Jan has left" or "Jan has changed his security code." except "<image omitted>"
        copied_list = list(data_date_message)
        for e in copied_list:
            if e.count(':') < 4:   # status messages have less than 4 colons
                data_date_message.remove(e)

        # iOS Split each message into a date, a sender and a message text
        dates = []
        senders = []
        messages = []
        for e in data_date_message:
            date = re.findall('(^\d+/\d+/\d+.*\sA?P?M):', e)
            dates.append(date[0])

            sender = re.findall('[^:]*:[^:]*:[^:]*:\s([^:]+):.*', e)
            senders.append(sender[0])

            message = re.findall('.+:.+:.+:.+:\s(.*)', e)
            messages.append(message[0])

        # iOS Create pandas dataframe
        df = pd.DataFrame({'sender': senders, 'date': dates, 'message': messages})

        # Convert dates from string to datetime format
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M:%S %p')
        print("Option 2: 8/23/13, 2:14:56 PM: ")
        print(df)
    return df


def check_list_sizes(df):
    l_senders = df["sender"].count()
    l_dates = df["date"].count()
    l_messages = df["message"].count()

    if l_senders == l_dates == l_messages:
        return True
    else:
        return False

def check_language(df):
    en = len(df[df['message'].str.contains("image omitted")])
    de = len(df[df['message'].str.contains("Bild weggelassen")])

    if en > de:
        print("langauge: en")
        return "english"
    else:
        print("langauge: de")
        return "german"

# Calculate total numbers
def calculate_total_numbers(dataframe):
    result = dict()
    df = dataframe
    result['total_number_messages'] = df['message'].count()

    lng = check_language(df)
    if lng == "english":
        result['total_number_images'] = len(df[df['message'].str.contains('image omitted')])
    elif lng == "german":
        result['total_number_images'] = len(df[df['message'].str.contains('Bild weggelassen')])

    result['total_number_days'] = (df['date'].max() - df['date'].min()).days

    total_number_words = 0
    total_number_letters = 0
    for e in df['message']:
        total_number_letters += len(e)
        total_number_words += len(re.findall("[a-zA-Z_]+", e))
    result['total_number_words'] = total_number_words
    result['total_number_letters'] = total_number_letters

    return result

# # Print total numbers
# for key, value in total_numbers().items():
#     print(key + ": " + str(value))

# Calculate averages
def calculate_averages(dataframe):
    result = dict()
    df = dataframe

    total_number_words = 0
    total_number_letters = 0
    for e in df['message']:
        total_number_letters += len(e)
        total_number_words += len(re.findall("[a-zA-Z_]+", e))
    mean_words = total_number_words/df['message'].count()
    mean_messages = df['message'].count()/int((df['date'].max() - df['date'].min()).days)
    mean_letters = total_number_letters/df['message'].count()

    result['mean_messages_per_day'] = mean_messages
    result['mean_words_per_message'] = mean_words
    result['mean_letters_per_message'] = mean_letters

    return result

# # Print averages
# for key, value in averages().items():
#     print(key + ": " + str(value))

# Calculate several activity stats
def calculate_activity(df):
    result = dict()

    result['activity_over_day'] = df.groupby(df['date'].dt.hour)['message'].count()
    result['activity_over_week'] = df.groupby(df['date'].dt.dayofweek)['message'].count()
    result['activity_over_year'] = df.groupby(df['date'].dt.month)['message'].count()
    result['activity_members_messages'] = df.groupby('sender')['message'].count()

    if check_language(df) == 'english':
        result['acitivity_members_images'] = df[df['message'].str.contains('image omitted', regex=True)].groupby('sender')['message'].count()
    else:
        result['acitivity_members_images'] = df[df['message'].str.contains('Bild weggelassen', regex=True)].groupby('sender')['message'].count()
    print(result)
    return result

# # Print activity stats
# for key, value in activity().items():
#    print(key + ": " + str(value))

#activity_result = activity()

#fig1, (plt_1, plt_2, plt_3) = plt.subplots(3, 1)

def make_plots(results, path):
    activity_result = results

    # Plot 1
    fig1 = plt.figure()
    plt.title("Activity over the week")
    x = activity_result['activity_over_week'].index.values
    y = activity_result['activity_over_week']
    x_labels = ["Mon", "Tun", "Wed", "Thu", "Fri", "Sat", "Sun"]
    plt.xticks(x, x_labels, rotation='vertical')
    plt.ylabel("Number of messages")
    plt.xlabel("Day of the week")
    plt.bar(x, y)
    plt.tight_layout()
    fig1.savefig(path + '/plot1')

    # Plot 2
    fig2 = plt.figure()
    plt.title("Activity over the day")
    x = activity_result['activity_over_day'].index.values
    y = activity_result['activity_over_day']
    plt.ylabel("Number of messages")
    plt.xlabel("Hour of the day")
    plt.plot(x, y)
    plt.tight_layout()
    fig2.savefig(path + '/plot2')

    # Plot 3
    fig3 = plt.figure()
    plt.title("Activity over the year")
    x = activity_result['activity_over_year'].index.values
    y = activity_result['activity_over_year']
    x_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    plt.xticks(x, x_labels, rotation='vertical')
    plt.ylabel("Number of messages")
    plt.xlabel("Month of the year")
    plt.bar(x, y)
    plt.tight_layout()
    fig3.savefig(path + '/plot3')

    # Plot 4
    fig4 = plt.figure()
    plt.title("Activity per member (messages)")
    labels = activity_result['activity_members_messages'].index.values
    sizes = activity_result['activity_members_messages']
    percent = 100.*sizes/sizes.sum()
    #patches, texts, dummy = plt.pie(sizes, autopct='%1.1f%%', startangle=90, radius=1.0)
    patches, texts = plt.pie(sizes, startangle=90, radius=1.0)
    labels_legend = ['{0} - {1:1.1f} %'.format(i,j) for i,j in zip(labels, percent)]
    lgd = plt.legend(patches, labels_legend, loc='best', bbox_to_anchor=(-0.1, 1.),
               fontsize=8)
    #plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, radius=1.0)
    plt.tight_layout()
    fig4.savefig(path + '/plot4', bbox_extra_artists=(lgd,), bbox_inches='tight')

    # Plot 5
    fig5 = plt.figure()
    plt.title("Activity per member (images)")
    #plt.sca(plt_5)
    labels = activity_result['acitivity_members_images'].index.values
    sizes = activity_result['acitivity_members_images']
    percent = 100.*sizes/sizes.sum()
    # patches, texts, dummy = plt.pie(sizes, autopct='%1.1f%%', startangle=90, radius=1.0)
    patches, texts= plt.pie(sizes, startangle=90, radius=1.0)
    labels_legend = ['{0} - {1:1.1f} %'.format(i,j) for i,j in zip(labels, percent)]
    lgd = plt.legend(patches, labels_legend, loc='best', bbox_to_anchor=(-0.1, 1.),
               fontsize=8)
    #plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, radius=1.0)
    plt.tight_layout()
    fig5.savefig(path + '/plot5', bbox_extra_artists=(lgd,), bbox_inches='tight')

