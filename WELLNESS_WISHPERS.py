from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore

# Set app window size
Window.size = (412, 720)

# Theme Colors
primary_blue = (0.1, 0.3, 0.7, 1)  # Darker Blue for buttons
light_blue = (0.4, 0.6, 0.9, 1)  # Lighter Blue for accents

# Initialize Firebase
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')  # Replace with your service account key file
firebase_admin.initialize_app(cred)
auth = firebase_admin.auth
db = firestore.client()

# Custom RadioButton class (using Image as a visual for now)
class RadioButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(RadioButton, self).__init__(**kwargs)
        self.source = 'radio_button_off.png'  # Replace with your off image path
        self.allow_stretch = True
        self.group = kwargs.get('group')
        self.active = False

    def on_press(self):
        self.source = 'radio_button_on.png'  # Replace with your on image path
        self.active = True

        # Deactivate other buttons in the same group
        if self.group:
            for child in self.parent.children:
                if isinstance(child, RadioButton) and child.group == self.group and child is not self:
                    child.active = False
                    child.source = 'radio_button_off.png'

        super(RadioButton, self).on_press()

    def on_release(self):
        self.source = 'radio_button_off.png'  # Replace with your off image path
        super(RadioButton, self).on_release()

# Shared elements for all screens
class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.name = kwargs.get('name')
        self.transition = FadeTransition()

        # White Background
        self.background = Rectangle(
            pos=self.pos,
            size=self.size,
            color=(1, 1, 1, 1)
        )
        self.canvas.before.add(self.background)

        # Logo Image
        self.logo = Image(
            source=r"C:\Users\harsh\Downloads\Wellness.png",  # Replace with your logo path
            size_hint=(None, None),
            width=400,
            height=600,
            pos_hint={'center_x': 0.5, 'top': 0.75}
        )
        self.add_widget(self.logo)

        # App Title
        self.app_title = Label(
            text="Wellness Whispers",
            font_size=24,
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, None),
            height=40,
            pos_hint={'center_x': 0.5, 'top': 0.6}
        )
        self.add_widget(self.app_title)

        # Privacy Policy and About
        self.info_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, 0.2),
            padding=10
        )
        self.add_widget(self.info_layout)

        # Privacy Policy
        privacy_button = Button(
            text="Privacy Policy",
            size_hint=(1, None),
            height=30,
            background_color=primary_blue,
            pos_hint={'center_x': 0.5}
        )
        self.info_layout.add_widget(privacy_button)

        # About
        about_button = Button(
            text="About Us",
            size_hint=(1, None),
            height=30,
            background_color=primary_blue,
            pos_hint={'center_x': 0.5}
        )
        self.info_layout.add_widget(about_button)

        # Swipe down instruction label
        self.swipe_label = Label(
            text="Swipe down to Login",
            font_size=18,
            bold=False,
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, None),
            height=30,
            pos_hint={'center_x': 0.5, 'y': 0.1}
        )
        self.add_widget(self.swipe_label)

        # Show login screen on swipe down
        self.bind(on_touch_down=self.handle_touch_down)

    def handle_touch_down(self, instance, touch):
        if touch.y < self.height * 0.2:
            self.manager.current = 'login'

    def on_size(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.name = 'login'
        self.transition = FadeTransition()

        # App Title
        self.app_title = Label(
            text="Wellness Whispers",
            font_size=24,
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, None),
            height=40,
            pos_hint={'center_x': 0.5, 'top': 0.9}
        )
        self.add_widget(self.app_title)

        # Card Layout
        self.card_layout = BoxLayout(
            orientation='vertical',
            padding=30,
            spacing=20,
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.card_layout)

        # Add card shape
        with self.card_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.card_rect = RoundedRectangle(
                pos=self.card_layout.pos,
                size=self.card_layout.size,
                radius=[20]
            )

        # Input Fields
        layout = GridLayout(cols=1, spacing=10, padding=20)
        self.email_input = TextInput(
            hint_text="Email",
            multiline=False,
            size_hint=(1, None),
            height=40,
            padding=[10, 10]
        )
        layout.add_widget(self.email_input)
        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=40,
            padding=[10, 10]
        )
        layout.add_widget(self.password_input)
        self.card_layout.add_widget(layout)

        # Login Button
        login_button = Button(
            text="Log In",
            size_hint=(1, None),
            height=40,
            background_color=primary_blue
        )
        login_button.bind(on_press=self.login_pressed)
        self.card_layout.add_widget(login_button)

        # Lower Buttons
        bottom_layout = BoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint=(1, None),
            height=50
        )

        signup_button = Button(
            text="Sign Up",
            size_hint=(0.5, 1),
            background_color=primary_blue
        )
        signup_button.bind(on_press=self.signup_pressed)
        bottom_layout.add_widget(signup_button)

        forget_button = Button(
            text="Forgot Password?",
            size_hint=(0.5, 1),
            background_color=primary_blue
        )
        forget_button.bind(on_press=self.forget_pressed)
        bottom_layout.add_widget(forget_button)

        self.card_layout.add_widget(bottom_layout)

    def login_pressed(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print(f"User logged in: {user.uid}")
            self.manager.current = 'questionnaire'  # Navigate to questionnaire screen
        except Exception as e:
            print(f"Error during login: {e}")

    def signup_pressed(self, instance):
        self.manager.current = 'signup'

    def forget_pressed(self, instance):
        self.manager.current = 'forget'

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        self.name = 'signup'

        # App Title
        self.app_title = Label(
            text="Wellness Whispers",
            font_size=24,
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, None),
            height=40,
            pos_hint={'center_x': 0.5, 'top': 0.9}
        )
        self.add_widget(self.app_title)

        # Card Layout
        self.card_layout = BoxLayout(
            orientation='vertical',
            padding=30,
            spacing=20,
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.card_layout)

        # Add card shape
        with self.card_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.card_rect = RoundedRectangle(
                pos=self.card_layout.pos,
                size=self.card_layout.size,
                radius=[20]
            )

        # Back Button
        back_button = Button(
            text="",
            size_hint=(0.1, None),
            height=40,
            background_color=primary_blue,
            pos_hint={'x': 0.05, 'y': 0.9}
        )
        back_button.bind(on_press=self.back_to_login_pressed)
        self.add_widget(back_button)

        # Draw arrow over the button
        with back_button.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            Line(points=(back_button.x + back_button.width * 0.4, back_button.y + back_button.height * 0.6,
                         back_button.x + back_button.width * 0.6, back_button.y + back_button.height * 0.4,
                         back_button.x + back_button.width * 0.4, back_button.y + back_button.height * 0.2),
                  width=2)

        # Input Fields
        layout = GridLayout(cols=1, spacing=10, padding=20)
        self.email_input = TextInput(
            hint_text="Email",
            multiline=False,
            size_hint=(1, None),
            height=40,
            padding=[10, 10]
        )
        layout.add_widget(self.email_input)
        self.password_input = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=40,
            padding=[10, 10]
        )
        layout.add_widget(self.password_input)
        self.confirm_password_input = TextInput(
            hint_text="Confirm Password",
            multiline=False,
            password=True,
            size_hint=(1, None),
            height=40,
            padding=[10, 10]
        )
        layout.add_widget(self.confirm_password_input)
        self.card_layout.add_widget(layout)

        # Signup Button
        signup_button = Button(
            text="Sign Up",
            size_hint=(1, None),
            height=40,
            background_color=primary_blue
        )
        signup_button.bind(on_press=self.signup_pressed)
        self.card_layout.add_widget(signup_button)

    def signup_pressed(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if not self.validate_inputs(email, password, confirm_password):
            return

        try:
            user = auth.create_user(email=email, password=password)
            print(f"User created: {user.uid}")

            # Store user data in the database (Firestore or Realtime Database)
            user_data = {
                'email': email,
                # ... other fields you want to store ...
            }
            db.collection('users').document(user.uid).set(user_data)

            self.manager.current = 'login'  # Navigate back to login screen
        except Exception as e:
            print(f"Error during signup: {e}")

    def validate_inputs(self, email, password, confirm_password):
        # ... (Implement your validation logic) ...
        if not all([email, password, confirm_password]):
            print("Please fill in all fields.")
            return False
        if password != confirm_password:
            print("Passwords do not match.")
            return False
        # ... (Add more validation checks as needed) ...
        return True

    def back_to_login_pressed(self, instance):
        self.manager.current = 'login'

class ForgetPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super(ForgetPasswordScreen, self).__init__(**kwargs)
        self.name = 'forget'

        # App Title
        self.app_title = Label(
            text="Wellness Whispers",
            font_size=24,
            bold=True,
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, None),
            height=40,
            pos_hint={'center_x': 0.5, 'top': 0.9}
        )
        self.add_widget(self.app_title)

        # Card Layout
        self.card_layout = BoxLayout(
            orientation='vertical',
            padding=30,
            spacing=20,
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.card_layout)

        # Add card shape
        with self.card_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.card_rect = RoundedRectangle(
                pos=self.card_layout.pos,
                size=self.card_layout.size,
                radius=[20]
            )

        # Back Button
        back_button = Button(
            text="",
            size_hint=(0.1, None),
            height=40,
            background_color=primary_blue,
            pos_hint={'x': 0.05, 'y': 0.9}
        )
        back_button.bind(on_press=self.back_to_login_pressed)
        self.add_widget(back_button)

        # Draw arrow over the button
        with back_button.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            Line(points=(back_button.x + back_button.width * 0.4, back_button.y + back_button.height * 0.6,
                         back_button.x + back_button.width * 0.6, back_button.y + back_button.height * 0.4,
                         back_button.x + back_button.width * 0.4, back_button.y + back_button.height * 0.2),
                  width=2)

        # Input Field
        layout = GridLayout(cols=1, spacing=10, padding=20)
        self.email_input = TextInput(
            hint_text="Email",
            multiline=False,
            size_hint=(1, None),
            height=40,
            padding=[10, 10]
        )
        layout.add_widget(self.email_input)
        self.card_layout.add_widget(layout)

        # Reset Button
        reset_button = Button(
            text="Reset Password",
            size_hint=(1, None),
            height=40,
            background_color=primary_blue
        )
        reset_button.bind(on_press=self.reset_pressed)
        self.card_layout.add_widget(reset_button)

    def reset_pressed(self, instance):
        email = self.email_input.text

        try:
            auth.send_password_reset_email(email)
            print(f"Password reset email sent to: {email}")
            # ... (handle success, e.g., navigate to a confirmation screen) ...
        except Exception as e:
            print(f"Error sending password reset email: {e}")

    def back_to_login_pressed(self, instance):
        self.manager.current = 'login'

class QuestionnaireScreen(Screen):
    def __init__(self, **kwargs):
        super(QuestionnaireScreen, self).__init__(**kwargs)

        # Layout for the questions
        self.question_layout = GridLayout(cols=1, spacing=10, padding=20)
        self.add_widget(self.question_layout)

        # Questions (replace with your actual questions)
        self.question1 = Label(text="Question 1: How often do you feel stressed?")
        self.question_layout.add_widget(self.question1)
        self.answer1_group = GridLayout(cols=3, spacing=10)
        self.question_layout.add_widget(self.answer1_group)
        self.answer1_rarely = RadioButton(group='question1', text="Rarely")
        self.answer1_group.add_widget(self.answer1_rarely)
        self.answer1_sometimes = RadioButton(group='question1', text="Sometimes")
        self.answer1_group.add_widget(self.answer1_sometimes)
        self.answer1_often = RadioButton(group='question1', text="Often")
        self.answer1_group.add_widget(self.answer1_often)

        self.question2 = Label(text="Question 2: Do you have trouble sleeping?")
        self.question_layout.add_widget(self.question2)
        self.answer2_group = GridLayout(cols=2, spacing=10)
        self.question_layout.add_widget(self.answer2_group)
        self.answer2_yes = RadioButton(group='question2', text="Yes")
        self.answer2_group.add_widget(self.answer2_yes)
        self.answer2_no = RadioButton(group='question2', text="No")
        self.answer2_group.add_widget(self.answer2_no)

        # ... (Add more questions and answers in a similar way) ...

        # Submit Button
        self.submit_button = Button(text="Submit Answers", size_hint=(1, None), height=40, background_color=primary_blue)
        self.submit_button.bind(on_press=self.submit_answers)
        self.question_layout.add_widget(self.submit_button)

        # Score Label
        self.score_label = Label(text="", font_size=20, bold=True)
        self.question_layout.add_widget(self.score_label)

    def submit_answers(self, instance):
        answers = {
            'question1': self.answer1_rarely.active if self.answer1_rarely.active else (
                self.answer1_sometimes.active if self.answer1_sometimes.active else (
                    self.answer1_often.active if self.answer1_often.active else None
                )
            ),
            'question2': self.answer2_yes.active if self.answer2_yes.active else (
                self.answer2_no.active if self.answer2_no.active else None
            ),
            # ... (Collect answers for other questions) ...
        }

        # Calculate score (replace with your actual logic)
        score = 0
        if answers['question1'] == 'Often':
            score += 3
        elif answers['question1'] == 'Sometimes':
            score += 1
        if answers['question2'] == 'Yes':
            score += 2
        # ... (Add scoring logic for other questions) ...

        self.score_label.text = f"Your Score: {score}"

class ScoreboardScreen(Screen):
    def __init__(self, **kwargs):
        super(ScoreboardScreen, self).__init__(**kwargs)

        # Layout for the scoreboard (adjust as needed)
        self.scoreboard_layout = GridLayout(cols=1, spacing=10, padding=20)
        self.add_widget(self.scoreboard_layout)

        # ... (Add widgets for displaying scores from the database) ...

        self.load_scores()

    def load_scores(self):
        try:
            # Query Firestore to get scores (adjust the query to fit your data structure)
            # docs = db.collection('scores').stream()  # Replace 'scores' with your collection name
            docs = db.collection('users').stream()

            for doc in docs:
                # Display scores on the scoreboard
                user_data = doc.to_dict()
                score_label = Label(text=f"User: {user_data.get('email')} - Score: {user_data.get('score', 'Not available')}")
                self.scoreboard_layout.add_widget(score_label)
        except Exception as e:
            print(f"Error loading scores: {e}")

class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition(direction='left'))
        sm.add_widget(BaseScreen(name='intro'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(ForgetPasswordScreen(name='forget'))
        sm.add_widget(QuestionnaireScreen(name='questionnaire'))
        sm.add_widget(ScoreboardScreen(name='scoreboard'))  # Add if you have a ScoreboardScreen
        return sm

if __name__ == '__main__':
    MyApp().run()