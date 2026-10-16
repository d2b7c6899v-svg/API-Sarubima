from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp

# Demo data only: it resets when the app closes.
PRODUCTS = [
    {"name": "Tomatoes", "price": 180, "quantity": 20, "farmer": "Demo Farmer"},
    {"name": "Carrots", "price": 240, "quantity": 12, "farmer": "Demo Farmer"},
]
CART = []
GREEN = (0.10, 0.38, 0.22, 1)
LIGHT = (0.92, 0.97, 0.92, 1)
DARK = (0.08, 0.16, 0.10, 1)

def label(text, size=16, color=DARK, height=dp(40), bold=False):
    return Label(text=text, font_size=dp(size), color=color, size_hint_y=None,
                 height=height, bold=bold, halign="left", valign="middle")

def button(text, callback, height=dp(48)):
    b = Button(text=text, size_hint_y=None, height=height, font_size=dp(16),
               background_normal="", background_color=GREEN, color=(1,1,1,1))
    b.bind(on_release=callback)
    return b

def field(hint):
    return TextInput(hint_text=hint, multiline=False, size_hint_y=None,
                     height=dp(46), padding=[dp(12), dp(12)], font_size=dp(16))

class BaseScreen(Screen):
    def start_layout(self, title):
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
        root.add_widget(label(title, 24, GREEN, dp(54), True))
        self.add_widget(root)
        return root
    def back_button(self, root):
        root.add_widget(button("← Home", lambda *_: setattr(self.manager, "current", "home")))

class HomeScreen(BaseScreen):
    def on_enter(self):
        self.clear_widgets()
        root = self.start_layout("API Sarubima")
        root.add_widget(label("Farmers and customers, connected directly.", 16, DARK, dp(56)))
        root.add_widget(button("I am a Farmer", lambda *_: setattr(self.manager, "current", "farmer")))
        root.add_widget(button("I am a Customer", lambda *_: setattr(self.manager, "current", "market")))
        root.add_widget(label("Prototype only • No real payments or delivery", 12, DARK, dp(44)))

class FarmerScreen(BaseScreen):
    def on_enter(self):
        self.clear_widgets()
        root = self.start_layout("Farmer Dashboard")
        root.add_widget(label("Add produce for customers", 16, DARK, dp(32)))
        self.product = field("Product name (e.g. Pumpkin)")
        self.price = field("Price per kg in LKR (e.g. 150)")
        self.qty = field("Quantity in kg (e.g. 20)")
        self.farmer = field("Farmer name")
        for widget in (self.product, self.price, self.qty, self.farmer):
            root.add_widget(widget)
        self.status = label("", 13, GREEN, dp(38))
        root.add_widget(self.status)
        root.add_widget(button("Add Product", self.add_product))
        root.add_widget(button("Open Customer Market", lambda *_: setattr(self.manager, "current", "market")))
        self.back_button(root)
    def add_product(self, *_):
        name = self.product.text.strip()
        farmer = self.farmer.text.strip() or "Local Farmer"
        try:
            price, qty = int(self.price.text), int(self.qty.text)
            if not name or price <= 0 or qty <= 0: raise ValueError
        except ValueError:
            self.status.text = "Enter a name and positive price/quantity."
            return
        PRODUCTS.insert(0, {"name": name, "price": price, "quantity": qty, "farmer": farmer})
        self.status.text = f"Added {name} — Rs. {price}/kg"
        self.product.text = self.price.text = self.qty.text = ""

class MarketScreen(BaseScreen):
    def on_enter(self):
        self.clear_widgets()
        root = self.start_layout("Fresh Market")
        root.add_widget(label("Produce from local farmers", 16, DARK, dp(34)))
        self.items = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.items.bind(minimum_height=self.items.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.items)
        root.add_widget(scroll)
        self.status = label("", 13, GREEN, dp(32))
        root.add_widget(self.status)
        root.add_widget(button("View Basket", lambda *_: self.open_basket()))
        self.back_button(root)
        self.refresh()
    def refresh(self):
        self.items.clear_widgets()
        for i, p in enumerate(PRODUCTS):
            card = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(3),
                             size_hint_y=None, height=dp(126))
            card.add_widget(label(f"{p['name']} — Rs. {p['price']}/kg", 17, GREEN, dp(32), True))
            card.add_widget(label(f"Farmer: {p['farmer']} • Stock: {p['quantity']} kg", 12, DARK, dp(26)))
            card.add_widget(button("Add 1 kg to Basket", lambda btn, idx=i: self.add(idx), dp(36)))
            self.items.add_widget(card)
    def add(self, index):
        p = PRODUCTS[index]
        CART.append({"name": p["name"], "price": p["price"], "qty": 1})
        total = sum(x["price"] * x["qty"] for x in CART)
        self.status.text = f"Basket: {len(CART)} item(s) • Rs. {total}"
    def open_basket(self):
        self.manager.get_screen("basket").refresh()
        self.manager.current = "basket"

class BasketScreen(BaseScreen):
    def on_enter(self):
        self.refresh()
    def refresh(self):
        self.clear_widgets()
        root = self.start_layout("My Basket")
        total = 0
        if not CART:
            root.add_widget(label("Your basket is empty.", 16))
        else:
            for item in CART:
                amount = item["price"] * item["qty"]
                total += amount
                root.add_widget(label(f"{item['name']} × {item['qty']} kg — Rs. {amount}", 15))
            root.add_widget(label(f"Total: Rs. {total}", 20, GREEN, dp(44), True))
        root.add_widget(button("Clear Basket", self.clear))
        root.add_widget(button("Back to Market", lambda *_: setattr(self.manager, "current", "market")))
        self.back_button(root)
    def clear(self, *_):
        CART.clear()
        self.refresh()

class SarubimaApp(App):
    title = "API Sarubima"
    def build(self):
        Window.clearcolor = LIGHT
        manager = ScreenManager()
        manager.add_widget(HomeScreen(name="home"))
        manager.add_widget(FarmerScreen(name="farmer"))
        manager.add_widget(MarketScreen(name="market"))
        manager.add_widget(BasketScreen(name="basket"))
        return manager

if __name__ == "__main__":
    SarubimaApp().run()
