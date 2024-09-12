import types
import os
import telebot
API_TOKEN = '7267544351:AAH2hSDFBg_8bdxYBm58PolK26jKQbowHng'
bot = telebot.TeleBot(API_TOKEN)
API_TOKEN = os.getenv('API_TOKEN')
# القاموس لتخزين بيانات البوت الرئيسي
summaries = {
    "🖥️ قسم علوم الحاسوب": {},
    "🔐 قسم الأمن السيبراني": {},
    "📊 قسم نظم المعلومات": {},
}

# التعامل مع أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    itembtn = types.InlineKeyboardButton('✨ بدء ✨', callback_data='start')
    markup.add(itembtn)
    welcome_text = """🌟 مرحباً بك في بوت الملخصات الجامعية 🌟
    
    🔹 مطور البوت: قاسم الشميري
    
    اضغط على "بدء" لاختيار التخصص والملخصات.
    """
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

# التعامل مع الزر الخاص ببدء
@bot.callback_query_handler(func=lambda call: call.data == 'start')
def choose_department(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for department in summaries.keys():
        markup.add(types.InlineKeyboardButton(department, callback_data=department))
    bot.edit_message_text("💡 *اختر القسم*:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

# التعامل مع اختيار القسم
@bot.callback_query_handler(func=lambda call: call.data in summaries.keys())
def choose_year(call):
    department = call.data
    markup = types.InlineKeyboardMarkup(row_width=2)
    years = ['سنة أولى', 'سنة ثانية', 'سنة ثالثة', 'سنة رابعة']
    for year in years:
        markup.add(types.InlineKeyboardButton(f'📚 {year}', callback_data=f'{department}:{year}'))
    bot.edit_message_text(f"📅 *اختر السنة في {department}:*", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

# التعامل مع اختيار السنة
@bot.callback_query_handler(func=lambda call: ':' in call.data and not call.data.count(':') == 1)
def choose_term(call):
    department, year = call.data.split(':')
    if year not in summaries[department]:
        bot.send_message(call.message.chat.id, "السنة غير متاحة. حاول مرة أخرى.", parse_mode='Markdown')
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    terms = ['ترم أول', 'ترم ثاني']
    for term in terms:
        markup.add(types.InlineKeyboardButton(f'📖 {term}', callback_data=f'{department}:{year}:{term}'))
    bot.edit_message_text(f"📅 *اختر الترم في {year}:*", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

# التعامل مع اختيار الترم
@bot.callback_query_handler(func=lambda call: ':' in call.data and call.data.count(':') == 2)
def choose_subject(call):
    department, year, term = call.data.split(':')
    if term not in summaries[department][year]:
        bot.send_message(call.message.chat.id, "الترم غير متاح. حاول مرة أخرى.", parse_mode='Markdown')
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    for subject in summaries[department][year][term].keys():
        markup.add(types.InlineKeyboardButton(subject, callback_data=f'{department}:{year}:{term}:{subject}'))
    bot.edit_message_text(f"📚 *اختر المادة في {term}:*", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

# التعامل مع اختيار المادة
@bot.callback_query_handler(func=lambda call: ':' in call.data and call.data.count(':') == 3)
def choose_summary_or_quizzes(call):
    department, year, term, subject = call.data.split(':')
    if subject not in summaries[department][year][term]:
        bot.send_message(call.message.chat.id, "المادة غير متاحة. حاول مرة أخرى.", parse_mode='Markdown')
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('📄 ملخصات', callback_data=f'{department}:{year}:{term}:{subject}:ملخصات'))
    markup.add(types.InlineKeyboardButton('❓ كويزات', callback_data=f'{department}:{year}:{term}:{subject}:كويزات'))
    bot.edit_message_text(f"📚 *اختر الخيار في {subject}:*", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

# التعامل مع اختيار ملخصات أو كويزات
@bot.callback_query_handler(func=lambda call: ':' in call.data and call.data.count(':') == 4)
def choose_summary_or_quiz(call):
    department, year, term, subject, choice = call.data.split(':')
    
    if choice == 'ملخصات':
        if 'ملخص' in summaries[department][year][term][subject]:
            file_url = summaries[department][year][term][subject]['ملخص']
            bot.send_message(call.message.chat.id, "🔄 جارٍ تحميل الملخص...", parse_mode='Markdown')
            bot.send_document(call.message.chat.id, file_url)
        else:
            bot.send_message(call.message.chat.id, "⚠️ ملخص غير متاح. حاول مرة أخرى.", parse_mode='Markdown')
    elif choice == 'كويزات':
        markup = types.InlineKeyboardMarkup(row_width=2)
        quizzes = summaries[department][year][term][subject]['أسئلة']
        for quiz in quizzes.keys():
            markup.add(types.InlineKeyboardButton(quiz, callback_data=f'{department}:{year}:{term}:{subject}:{quiz}'))
        bot.edit_message_text(f"❓ *اختر الكويز في {subject}:*", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

# التعامل مع اختيار كويز
@bot.callback_query_handler(func=lambda call: ':' in call.data and call.data.count(':') == 5)
def send_quiz(call):
    department, year, term, subject, quiz_name = call.data.split(':')
    file_url = summaries[department][year][term][subject]['أسئلة'][quiz_name]
    bot.send_message(call.message.chat.id, f"🔄 جارٍ تحميل {quiz_name}...", parse_mode='Markdown')
    bot.send_document(call.message.chat.id, file_url)

# بدء البوت
bot.polling()
