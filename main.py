"""Interface gráfica da calculadora usando FreeSimpleGUI."""

import FreeSimpleGUI as sg

from calculadora import Calculator


def create_window() -> sg.Window:
    sg.theme("DarkBlue3")
    button_size = (5, 2)
    layout = [
        [sg.Input("0", key="-DISPLAY-", justification="right", font=("Arial", 24),
                  readonly=True, expand_x=True, size=(18, 1))],
        [
            sg.Button("7", size=button_size), sg.Button("8", size=button_size),
            sg.Button("9", size=button_size), sg.Button("/", size=button_size),
        ],
        [
            sg.Button("4", size=button_size), sg.Button("5", size=button_size),
            sg.Button("6", size=button_size), sg.Button("*", size=button_size),
        ],
        [
            sg.Button("1", size=button_size), sg.Button("2", size=button_size),
            sg.Button("3", size=button_size), sg.Button("-", size=button_size),
        ],
        [
            sg.Button("0", size=button_size), sg.Button(".", size=button_size),
            sg.Button("=", size=button_size), sg.Button("+", size=button_size),
        ],
        [sg.Button("C — limpar display e histórico", key="C", expand_x=True),
         sg.Button("←", key="BACKSPACE", size=button_size)],
        [sg.Text("Histórico recente", font=("Arial", 12, "bold"))],
        [sg.Listbox([], key="-HISTORY-", size=(34, 6), expand_x=True)],
    ]
    return sg.Window(
        "Calculadora",
        layout,
        finalize=True,
        resizable=False,
        element_justification="center",
        margins=(16, 16),
    )


def main() -> None:
    calculator = Calculator()
    window = create_window()
    try:
        while True:
            event, _values = window.read()
            if event in (sg.WIN_CLOSED, "Exit"):
                break

            try:
                if isinstance(event, str) and event in "0123456789" and len(event) == 1:
                    calculator.input_digit(event)
                elif event == ".":
                    calculator.input_decimal()
                elif event in ("+", "-", "*", "/"):
                    calculator.set_operator(event)
                elif event == "=":
                    calculator.calculate()
                elif event == "BACKSPACE":
                    calculator.backspace()
                elif event == "C":
                    calculator.clear()
            except ZeroDivisionError:
                sg.popup_error("Erro: Divisão por zero", title="Erro")
            except ValueError:
                sg.popup_error("Erro: Expressão inválida", title="Erro")

            window["-DISPLAY-"].update(calculator.display)
            window["-HISTORY-"].update(calculator.history)
    finally:
        window.close()


if __name__ == "__main__":
    main()
