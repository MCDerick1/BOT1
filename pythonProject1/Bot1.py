import telebot
bot = telebot.TeleBot("7751480776:AAEco5EqGJbHjWYHNTJxH2eIyDPCfS3kVSY")
tasks = {}
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Команды:\n"
                          "/addtask - добавить задачу\n"
                          "/showtasks - показать задачи\n"
                          "/deltask - удалить задачу")
@bot.message_handler(commands=['addtask'])
def add_task(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Введите текст задачи:")
    bot.register_next_step_handler(msg, process_task_step)
def process_task_step(message):
    chat_id = message.chat.id
    task_text = message.text
    if chat_id not in tasks:
        tasks[chat_id] = []
    tasks[chat_id].append(task_text)
    bot.send_message(chat_id, f'Задача "{task_text}" добавлена!')
@bot.message_handler(commands=['showtasks'])
def show_tasks(message):
    chat_id = message.chat.id
    if chat_id not in tasks or not tasks[chat_id]:
        bot.send_message(chat_id, "У вас пока нет задач!")
        return
    tasks_list = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(tasks[chat_id])])
    bot.send_message(chat_id, f"Ваши задачи:\n{tasks_list}")
@bot.message_handler(commands=['deltask'])
def delete_task(message):
    chat_id = message.chat.id
    if chat_id not in tasks or not tasks[chat_id]:
        bot.send_message(chat_id, "У вас пока нет задач для удаления!")
        return
    tasks_list = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(tasks[chat_id])])
    msg = bot.send_message(chat_id, f"Ваши задачи:\n{tasks_list}\n\nВведите номер задачи для удаления:")
    bot.register_next_step_handler(msg, process_delete_step)
def process_delete_step(message):
    chat_id = message.chat.id
    try:
        task_num = int(message.text)
        if 1 <= task_num <= len(tasks[chat_id]):
            removed_task = tasks[chat_id].pop(task_num - 1)
            bot.send_message(chat_id, f'Задача "{removed_task}" удалена!')
        else:
            bot.send_message(chat_id, "Неверный номер задачи!")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите номер задачи цифрами!")
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)