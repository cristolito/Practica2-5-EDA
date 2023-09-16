import math
import flet as ft
class Cajero:
    def __init__(self) -> None:
        self.coins = [100, 50, 20, 10, 5, 1, 0.5, 0.2, 0.01]

    def calcular_cambio(self,price, cash):
        change = cash - price
        change_coins = {}

        if change == 0:
            return None
        else: 
            for coin in self.coins:
                if change >= coin:
                    num_coins = math.trunc(round(change / coin,2))
                    change_coins[coin] = num_coins
                    change = change - (num_coins * coin)
                else: change_coins[coin] = 0

        return change_coins
    
class TorresHanoi:
    def __init__(self) -> None:
        self.movimientos = []

    def moverTorre(self,altura,origen, destino, intermedio):
        if altura >= 1:
            self.moverTorre(altura-1,origen,intermedio,destino)
            self.moverDisco(origen,destino)
            self.moverTorre(altura-1,intermedio,destino,origen)

    def moverDisco(self,desde,hacia):
        self.movimientos.append(f"Mover disco de torre {desde} a la torre {hacia}")
    
def main(page: ft.Page):
    def changeInterface(e):
        page.controls.clear()
        input_1.value = ""
        input_2.value = ""
        input_3.value = ""
        input_4.value = ""
        if menu_options.value == "Cajero":
            title.value = "Cajero"
            input_1.label = "Cantidad a pagar"
            input_2.label = "Pago recibido"
            input_2.visible=True
            input_3.visible=False
            input_4.visible=False
            btn_cal.text="Cobrar"
            btn_cal.on_click=handle_sale_btn
        else:
            title.value = "Torres de Hanoi"
            input_1.label="Número de Discos"
            input_2.visible=True
            input_2.label = "Origen"
            input_3.visible=True
            input_3.label = "Destino"
            input_4.visible=True
            input_4.label = "Intermedio"
            btn_cal.text="Mostrar movimientos"
            btn_cal.on_click=handle_hanoi_btn
        page.add(container,ft.Text())

    def handle_sale_btn(e):
        page.controls.pop(1) 
        cambio = cajero.calcular_cambio(float(input_1.value), float(input_2.value))
        if cambio is not None:
            result = ft.Column([
                ft.Text(f"Cambio a devolver: {float(input_2.value) - float(input_1.value):.2f} pesos"),
                ft.Text("Desglose del cambio:")
            ],spacing=2)
            for coin, cantidad in cambio.items():
                if coin >= 1:
                    result.controls.append(ft.Text(f"{cantidad} monedas de {coin} pesos"))
                else:
                    centavos = int(coin * 100)
                    result.controls.append(ft.Text(f"{cantidad} monedas de {centavos} centavos"))
        else: result.controls.append(ft.Text("No hay cambio que devolver"))
        page.add(result)

    def handle_hanoi_btn(e):
        page.controls.pop(1) 
        torres_hanoi.moverTorre(int(input_1.value),input_2.value,input_3.value,input_4.value)
        container = ft.Column([ft.Text(f"Los movimientos necesarios a realizar para lograrlo en la menor cantidad de movimientos son {len(torres_hanoi.movimientos)}:")],spacing=4)
        result = ft.Column(spacing=2,scroll=ft.ScrollMode.ALWAYS, height=200, width=300)
        for movimiento in torres_hanoi.movimientos:
            result.controls.append(
                ft.Text(f"{movimiento}")
            )
        container.controls.append(result)

        torres_hanoi.movimientos.clear()
        page.add(container)

    cajero = Cajero()
    torres_hanoi = TorresHanoi()
    input_1 = ft.TextField(label="Cantidad a pagar", width=300)
    input_2 = ft.TextField(label="Pago recibido", width=300)
    input_3 = ft.TextField(label="Destino", width=300, visible=False)
    input_4 = ft.TextField(label="Intermedio", width=300,visible=False)
    menu_options = ft.Dropdown(options=[
        ft.dropdown.Option("Cajero"),
        ft.dropdown.Option("Hanoi")
    ], width=250,value="Cajero", on_change=changeInterface)
    btn_cal = ft.ElevatedButton("Cobrar", on_click=handle_sale_btn)
    title = ft.Text("Cajero",size=20,weight="bold")

    container = ft.Container(
        ft.Column([
            menu_options, title, input_1, input_2, input_3,input_4, btn_cal]),alignment=ft.alignment.center,
            margin=25)

    page.add(container,ft.Text())

ft.app(target=main)