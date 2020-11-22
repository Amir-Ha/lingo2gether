from lingo2gether.command_utils import CommandUtils


class Command:
    # key = "/command" value = commandFunction
    commands_dict = {
        '/teachme': CommandUtils.teach_me,
        '/help': CommandUtils.print_help,
        '/start': CommandUtils.print_help,
        '/forget': CommandUtils.command_forget,
        '/translate': CommandUtils.translate,
        '/stopme': CommandUtils.stopMe,
        '/resume': CommandUtils.resume,
        '/memorize': CommandUtils.command_specialize,
        '/showvocabulary': CommandUtils.show_vocabulary,
        '/quiz': CommandUtils.quiz
    }

    @staticmethod
    def execute(command_name, *args, **vargs):
        if command_name in Command.commands_dict.keys():
            return Command.commands_dict[command_name](*args, **vargs)
        return "Command doesn't recognized. You can use /help command for more infromations."
