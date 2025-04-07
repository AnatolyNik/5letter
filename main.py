from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from embed_words_txt import words_from_txt

# Настройка цветов
COLORS = {
    "background": get_color_from_hex("#f5f5f5"),
    "primary": get_color_from_hex("#6200ee"),
    "primary_light": get_color_from_hex("#bb86fc"),
    "text_dark": get_color_from_hex("#121212"),
    "text_light": get_color_from_hex("#ffffff"),
    "error": get_color_from_hex("#cf6679"),
    "success": get_color_from_hex("#03dac6"),
    "warning": get_color_from_hex("#ffc107"),
}
Font_size_input = 26

class WordFilterApp(App):
    def build(self):
        Window.clearcolor = COLORS["background"]
        self.words = words_from_txt
        self.layout = BoxLayout(
            orientation="vertical", 
            padding=30,
            spacing=20,  # Увеличенный spacing
        )

        # Заголовок
        self.title_label = Label(
            text="5 Букв", 
            font_size=Font_size_input,
            bold=True,
            color=COLORS["text_dark"],
            size_hint=(1, 0.01),
        )
        self.layout.add_widget(self.title_label)

        # Поле ввода для букв, которых НЕТ в слове
        self.not_in_word_input = TextInput(
            hint_text="Буквы, которых нет в слове (например: абв)",
            multiline=False,
            size_hint=(1, 0.1),
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS["error"],
            hint_text_color=(0.5, 0.5, 0.5, 0.7),
            padding=5,
            font_size=Font_size_input,
        )
        self.layout.add_widget(self.not_in_word_input)

        # Поле ввода для букв, которые ЕСТЬ в слове (шрифт 32 вместо 16)
        self.in_word_input = TextInput(
            hint_text="Буквы, которые есть в слове (например: гд)",
            multiline=False,
            size_hint=(1, 0.1),
            background_color=(1, 1, 1, 0.9),
            foreground_color=COLORS["success"],
            hint_text_color=(0.5, 0.5, 0.5, 0.7),
            padding=5,
            font_size=Font_size_input,
        )
        self.layout.add_widget(self.in_word_input)

        # Поля ввода для букв на своих местах
        self.letter_box = BoxLayout(orientation='vertical', spacing=20, size_hint=(1, 0.2))
        self.letter_box.add_widget(
            Label(
                text="Буквы на своих местах", 
                font_size=Font_size_input,
                color=COLORS["text_dark"],
                size_hint=(1, 0.5),
            )
        )

        self.letter_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 1))
        self.letter_inputs = []
        for i in range(5):
            text_input = TextInput(
                text='',
                multiline=False,
                size_hint=(None, 1),
                width=50,
                background_color=(1, 1, 1, 0.9),
                foreground_color=COLORS["warning"],
                font_size=Font_size_input,
                halign="center",
            )
            text_input.bind(text=self.update_letter)
            text_input.index = i
            self.letter_inputs.append(text_input)
            self.letter_layout.add_widget(text_input)
        self.letter_box.add_widget(self.letter_layout)
        self.layout.add_widget(self.letter_box)

        # Кнопка фильтрации
        self.filter_button = Button(
            text="Найти слова",
            size_hint=(1, 0.15),
            background_color=COLORS["primary"],
            color=COLORS["text_light"],
            font_size=Font_size_input,
            bold=True,
        )
        self.filter_button.bind(on_press=self.animate_button)
        self.filter_button.bind(on_release=self.filter_words)
        self.layout.add_widget(self.filter_button)

        # Область результатов с прокруткой
        self.scroll_view = ScrollView(size_hint=(1, 0.6))
        self.results_layout = GridLayout(cols=1, spacing=15, size_hint_y=None)  # Увеличен spacing
        self.results_layout.bind(minimum_height=self.results_layout.setter("height"))
        self.scroll_view.add_widget(self.results_layout)
        self.layout.add_widget(self.scroll_view)

        return self.layout

    def animate_button(self, instance):
        anim = Animation(opacity=0.6, duration=0.1) + Animation(opacity=1, duration=0.1)
        anim.start(instance)

    def update_letter(self, instance, value):
        if len(value) > 1:
            instance.text = value[:1].upper()

    def filter_words(self, instance):
        not_in_word = list(self.not_in_word_input.text.strip().lower())
        in_word = list(self.in_word_input.text.strip().lower())
        letters = [input.text.lower() for input in self.letter_inputs]

        filtered_words = [
            word for word in self.words
            if len(word) == 5
            and not any(letter in word for letter in not_in_word)
            and all(letter in word for letter in in_word)
            and all(word[i] == letter for i, letter in enumerate(letters) if letter)
        ]

        self.results_layout.clear_widgets()

        if not filtered_words:
            self.results_layout.add_widget(
                Label(
                    text="Нет подходящих слов!", 
                    color=COLORS["error"],
                    font_size=32,
                    size_hint_y=None,
                    height=60,
                )
            )
        else:
            for word in filtered_words[:15]:
                self.results_layout.add_widget(
                    Label(
                        text=word.upper(),
                        color=COLORS["text_dark"],
                        font_size=36,
                        bold=True,
                        size_hint_y=None,
                        height=70,
                    )
                )

if __name__ == "__main__":
    WordFilterApp().run()
