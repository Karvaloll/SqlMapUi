from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from functools import partial
from command_dict import result_dict, sqlmap_path
from help import help_dict
from help import tamper_list
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.config import Config
from kivy.core.clipboard import Clipboard
import subprocess
from loguru import logger

logger.add("comands.log", format="[{time:YYYY-MM-DD at HH:mm}] \n {message}\n", rotation="50 MB")

Config.set('graphics', 'minimum_width', 1024)
Config.set('graphics', 'minimum_height', 850)
Config.set('kivy', 'keyboard_mode', 'system')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

rezult_global_dict = result_dict


class TabbedPanelMain(TabbedPanel):
    pass


class ErrorPage(FloatLayout):
    cancel = ObjectProperty(None)

    def put_error_message(self, message: str) -> None:
        self.error_lable.text = message


class ResultPage(FloatLayout):
    cancel = ObjectProperty(None)

    def put_result_message(self, message: str) -> None:
        self.result_lable.text = message

    def copy_result_out(self) -> None:
        Clipboard.copy(self.result_lable.text)
        logger.info(self.result_lable.text)

    def execute_command(self) -> None:
        logger.info(self.result_lable.text)
        subprocess.run(self.result_lable.text, shell=True)


class LoadHelpString(FloatLayout):
    cancel = ObjectProperty(None)

    def put_text_message(self, target_key: str) -> None:
        self.help_lable.text = help_dict[target_key]


class HttpProtokolAuth(FloatLayout):
    global rezult_global_dict
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_option = ''

    def option_http_protokol_auth(self, checkbox_value: str, option: str) -> None:
        if checkbox_value:
            self.save_option = option
            rezult_global_dict['--auth-type'] = True

    def save_http_protokol_auth_option(self) -> None:
        if rezult_global_dict['--auth-type']:
            rezult_global_dict['--auth-type'] = self.save_option


class Technique(FloatLayout):
    global rezult_global_dict
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_option = ''
        self.option_dict = {}

    def option_techniques(self, checkbox_value: str, option: str) -> None:
        self.option_dict[option] = checkbox_value

    def save_techniques_option(self) -> None:
        for key, value in self.option_dict.items():
            if value:
                self.save_option += key
        if rezult_global_dict['--technique']:
            rezult_global_dict['--technique'] = self.save_option


class Tamper(BoxLayout):
    global rezult_global_dict
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None
        self.save_option = ''
        self.option_dict = {}

    def option_tamper(self, instance: str, checkbox_name: str, notuse: str, checkbox_value: str) -> None:
        self.option_dict[checkbox_name] = checkbox_value

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def select_tamper(self) -> None:
        for i in tamper_list:
            anc_check = AnchorLayout(size_hint=(0.2, 1), anchor_x='left', anchor_y='center')
            check = CheckBox()
            check.bind(active=partial(self.option_tamper, check.active, i))
            anc_help = AnchorLayout(size_hint=(0.1, 1), anchor_x='center', anchor_y='center')
            button = Button(background_color=(0, 0, 1), text='?')
            button.bind(on_release=partial(self.show_help_string, i))
            anc_lable = AnchorLayout(size_hint=(0.7, 1), anchor_x='right', anchor_y='center')
            label = Label(text=i)
            anc_check.add_widget(check)
            anc_help.add_widget(button)
            anc_lable.add_widget(label)
            tamper_layout = BoxLayout(size_hint=(0.33, 0.04), spacing=3)
            tamper_layout.add_widget(anc_check)
            tamper_layout.add_widget(anc_help)
            tamper_layout.add_widget(anc_lable)
            self.tamper_page.add_widget(tamper_layout)

    def show_help_string(self, target_key: str, notused: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def save_temper_option(self) -> None:
        for key, value in self.option_dict.items():
            if value:
                self.save_option += key + ','
        self.save_option = self.save_option[:-1]
        if rezult_global_dict['--tamper']:
            rezult_global_dict['--tamper'] = self.save_option


class SaveString(FloatLayout):
    global rezult_global_dict
    save_value = ''
    dict_key = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def clear_input_target(self) -> None:
        self.save_input_text.text = ''

    def paste_in_input_text(self) -> None:
        self.save_input_text.paste()

    def save_text(self) -> None:
        if rezult_global_dict[self.dict_key]:
            if self.dict_key == '-D':
                rezult_global_dict[self.dict_key] = '[$]' + self.save_input_text.text
            elif self.dict_key == '-T':
                rezult_global_dict[self.dict_key] = '[$]' + self.save_input_text.text
            elif self.dict_key == '-C':
                rezult_global_dict[self.dict_key] = '[$]' + self.save_input_text.text
            elif self.dict_key == '-X':
                rezult_global_dict[self.dict_key] = '[$]' + self.save_input_text.text
            elif self.dict_key == '-U':
                rezult_global_dict[self.dict_key] = '[$]' + self.save_input_text.text
            else:
                rezult_global_dict[self.dict_key] = self.save_input_text.text


class RequestsPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def request_page_to_dict(checkbox_value: str, dict_key: str) -> None:
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def show_files_path(self, key: str) -> None:
        content = LoadFilePath(cancel=self.dismiss_popup, dict_key=key)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def add_input_text(self, dict_key: str) -> None:
        content_text = SaveString(cancel=self.dismiss_popup, dict_key=dict_key)
        self._popup = Popup(title="Добавить", content=content_text,size_hint=(0.6, 0.4))
        self._popup.open()

    def http_protokol_auth(self) -> None:
        content_text = HttpProtokolAuth(cancel=self.dismiss_popup)
        self._popup = Popup(title="Выбор", content=content_text, size_hint=(0.6, 0.4))
        self._popup.open()


class LoadFilePath(FloatLayout):
    global rezult_global_dict
    cancel = ObjectProperty(None)
    dict_key = ObjectProperty(None)

    def selected_file_target(self, filename: str) -> None:
        rezult_global_dict[self.dict_key] = filename[0]


class LoadPath(FloatLayout):
    global rezult_global_dict
    cancel = ObjectProperty(None)
    dict_key = ObjectProperty(None)

    def selected_path_target(self, path: str) -> None:
        rezult_global_dict[self.dict_key] = path


class LoadFileTarget(FloatLayout):
    cancel = ObjectProperty(None)
    field_url = ObjectProperty(None)

    def selected_file_target(self, filename: str) -> None:
        self.field_url.text = filename[0]


class OptimisationPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def optimisation_page_to_dict(checkbox_value: str, dict_key: str) -> None:
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def add_input_text(self, dict_key: str) -> None:
        content_text = SaveString(cancel=self.dismiss_popup, dict_key=dict_key)
        self._popup = Popup(title="Добавить", content=content_text, size_hint=(0.6, 0.4))
        self._popup.open()


class InjectionPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def injection_page_to_dict(checkbox_value: str, dict_key: str) -> None:
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def add_input_text(self, dict_key: str) -> None:
        content_text = SaveString(cancel=self.dismiss_popup, dict_key=dict_key)
        self._popup = Popup(title="Добавить", content=content_text, size_hint=(0.6, 0.4))
        self._popup.open()

    def tamper(self) -> None:
        content_text = Tamper(cancel=self.dismiss_popup)
        self._popup = Popup(title="Выбор", content=content_text, size_hint=(0.99, 0.9))
        self._popup.open()


class DetectionPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def detection_page_to_dict(checkbox_value: str, dict_key: str):
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def add_input_text(self, dict_key) -> None:
        content_text = SaveString(cancel=self.dismiss_popup, dict_key=dict_key)
        self._popup = Popup(title="Добавить", content=content_text, size_hint=(0.6, 0.4))
        self._popup.open()


class EnumerationPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def enumeration_page_to_dict(checkbox_value: str, dict_key: str) -> None:
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def show_files_path(self, key: str) -> None:
        content = LoadFilePath(cancel=self.dismiss_popup, dict_key=key)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def add_input_text(self, dict_key: str) -> None:
        content_text = SaveString(cancel=self.dismiss_popup, dict_key=dict_key)
        self._popup = Popup(title="Добавить", content=content_text, size_hint=(0.6, 0.4))
        self._popup.open()


class BrootFuncPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def broot_func_page_to_dict(checkbox_value: str, dict_key: str) -> None:
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def show_files_path(self, key: str) -> None:
        content = LoadFilePath(cancel=self.dismiss_popup, dict_key=key)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


class TechniquesPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def techniques_page_to_dict(checkbox_value: str, dict_key: str) -> None:
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def add_input_text(self, dict_key: str) -> None:
        content_text = SaveString(cancel=self.dismiss_popup, dict_key=dict_key)
        self._popup = Popup(title="Добавить", content=content_text, size_hint=(0.6, 0.4))
        self._popup.open()

    def technique(self) -> None:
        content_text = Technique(cancel=self.dismiss_popup)
        self._popup = Popup(title="Выбор", content=content_text, size_hint=(0.4, 0.4))
        self._popup.open()

    def show_files_path(self, key: str) -> None:
        content = LoadFilePath(cancel=self.dismiss_popup, dict_key=key)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


class AccessPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def access_page_to_dict(checkbox_value: str, dict_key: str) -> None:
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def add_input_text(self, dict_key: str) -> None:
        content_text = SaveString(cancel=self.dismiss_popup, dict_key=dict_key)
        self._popup = Popup(title="Добавить", content=content_text, size_hint=(0.6, 0.4))
        self._popup.open()

    def show_files_path(self, key: str) -> None:
        content = LoadFilePath(cancel=self.dismiss_popup, dict_key=key)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


class GeneralPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def general_page_to_dict(checkbox_value: str, dict_key: str) -> None:
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def add_input_text(self, dict_key: str) -> None:
        content_text = SaveString(cancel=self.dismiss_popup, dict_key=dict_key)
        self._popup = Popup(title="Добавить", content=content_text, size_hint=(0.6, 0.4))
        self._popup.open()

    def show_files_path(self, key: str) -> None:
        content = LoadFilePath(cancel=self.dismiss_popup, dict_key=key)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_path(self, key: str) -> None:
        content = LoadPath(cancel=self.dismiss_popup, dict_key=key)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


class MiscellaneousPage(StackLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None

    @staticmethod
    def miscellaneous_page_to_dict(checkbox_value: str, dict_key: str) -> None:
        if checkbox_value:
            rezult_global_dict[dict_key] = True
        else:
            rezult_global_dict[dict_key] = False

    def show_help_string(self, target_key: str) -> None:
        content_help = LoadHelpString(cancel=self.dismiss_popup)
        self._popup = Popup(title="Подсказка", content=content_help, size_hint=(0.6, 0.4))
        self._popup.open()
        content_help.put_text_message(target_key)

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def add_input_text(self, dict_key: str) -> None:
        content_text = SaveString(cancel=self.dismiss_popup, dict_key=dict_key)
        self._popup = Popup(title="Добавить", content=content_text, size_hint=(0.6, 0.4))
        self._popup.open()

    def show_files_path(self, key: str) -> None:
        content = LoadFilePath(cancel=self.dismiss_popup, dict_key=key)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_path(self, key: str) -> None:
        content = LoadPath(cancel=self.dismiss_popup, dict_key=key)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


class MainContainer(BoxLayout):
    global rezult_global_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._popup = None
        self.target_type = '-u'

    def dismiss_popup(self) -> None:
        self._popup.dismiss()

    def show_files_target(self) -> None:
        content = LoadFileTarget(cancel=self.dismiss_popup, field_url=self.input_target)
        self._popup = Popup(title="Выбор файла", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def paste_in_input_target(self) -> None:
        self.input_target.text = ''
        self.input_target.paste()

    def clear_input_target(self) -> None:
        self.input_target.text = ''

    def show_error(self, message: str) -> None:
        error_content = ErrorPage(cancel=self.dismiss_popup)

        self._popup = Popup(title="Ошибка", content=error_content, size_hint=(0.3, 0.2))
        self._popup.open()
        error_content.put_error_message(message)

    def show_rezult(self, message: str) -> None:
        result_content = ResultPage(cancel=self.dismiss_popup)
        self._popup = Popup(title="Командв SQLMap", content=result_content, size_hint=(0.9, 0.5))
        self._popup.open()
        result_content.put_result_message(message)

    def change_lablle_on_target(self) -> None:
        get_spiner_target_data = self.spiner_target_data.text

        if get_spiner_target_data == 'URL':
            self.target_type = '-u'
            self.lable_on_target.text = 'Целевой URL (например, "http://www.site.com/vuln.php?id=1")'
        elif get_spiner_target_data == 'DIRECT':
            self.target_type = '-d'
            self.lable_on_target.text = 'Строка подключения для прямого соединения с базой данных'
        elif get_spiner_target_data == 'LOGFILE':
            self.target_type = '-l'
            self.lable_on_target.text = 'Парсить цель(и) из файлов логов Burp или WebScarab'
        elif get_spiner_target_data == 'BULKFILE':
            self.target_type = '-m'
            self.lable_on_target.text = 'Сканировать множество целей, заданных в текстовом файле'
        elif get_spiner_target_data == 'REQUESTFILE':
            self.target_type = '-r'
            self.lable_on_target.text = 'Загрузить HTTP запросы из файла'
        elif get_spiner_target_data == 'GOOGLEDORK':
            self.target_type = '-g'
            self.lable_on_target.text = 'Обработать результаты дорков Google как целевых URL'
        elif get_spiner_target_data == 'CONFIGFILE':
            self.target_type = '-c'
            self.lable_on_target.text = 'Загрузить опции из конфигурационного файла INI'

    @staticmethod
    def search_quotation_mark(string: str) -> str:
        rezult_string = ''
        if string.find('[$]') == 0:
            rezult_string += f" {string[3:]}"
        elif string.find('"') == -1:
            rezult_string += f'="{string}"'
        else:
            rezult_string += f"='{string}'"
        return rezult_string

    def get_rezult(self, ) -> None:
        result_string = f'{sqlmap_path} '
        for key_rez, value_rez in rezult_global_dict.items():
            if value_rez != False and value_rez != True:
                result_string += f'{key_rez}{self.search_quotation_mark(value_rez)} '
            elif value_rez:
                result_string += f'{key_rez} '
        self.show_rezult(result_string)

    def target_get_link(self) -> bool:
        rezult_global_dict['-u'] = False
        rezult_global_dict['-d'] = False
        rezult_global_dict['-l'] = False
        rezult_global_dict['-m'] = False
        rezult_global_dict['-r'] = False
        rezult_global_dict['-g'] = False
        rezult_global_dict['-c'] = False
        if self.input_target.text == 'Введите адрес или Ctrl+V' or self.input_target.text == '':
            self.show_error('Не указано поле цели')
        else:
            rezult_global_dict[self.target_type] = '[$]' + self.input_target.text
            return True

    def create_sqlmap_command(self) -> None:
        if self.target_get_link():
            self.get_rezult()


class Sqlmap_uiApp(App):
    def build(self):
        return MainContainer()


if __name__ == '__main__':
    Sqlmap_uiApp().run()
