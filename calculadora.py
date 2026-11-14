"""Regras e estado da calculadora, sem dependência da interface gráfica."""

from decimal import Decimal, InvalidOperation


OPERATORS = {"+", "-", "*", "/"}
MAX_HISTORY = 10
MAX_DISPLAY_LENGTH = 16


def parse_number(value: str) -> Decimal:
    """Converte uma entrada para Decimal e rejeita valores inválidos ou infinitos."""
    try:
        number = Decimal(value)
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError("Digite um número válido.") from error

    if not number.is_finite():
        raise ValueError("Digite um número finito.")
    return number


def format_number(value: Decimal) -> str:
    """Formata resultados em no máximo MAX_DISPLAY_LENGTH caracteres."""
    if value == 0:
        return "0"
    formatted = format(value, "f")
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    if len(formatted) <= MAX_DISPLAY_LENGTH:
        return formatted

    for precision in range(15, 0, -1):
        compact = format(value, f".{precision}g")
        if len(compact) <= MAX_DISPLAY_LENGTH:
            return compact

    compact = format(value, ".1e")
    if len(compact) <= MAX_DISPLAY_LENGTH:
        return compact
    raise ValueError("O resultado não pode ser exibido.")


def calculate(left: Decimal, operator: str, right: Decimal) -> Decimal:
    """Executa uma operação básica, informando operadores e divisões inválidos."""
    if operator not in OPERATORS:
        raise ValueError("Operação inválida.")
    if not left.is_finite() or not right.is_finite():
        raise ValueError("Os operandos devem ser números finitos.")
    if operator == "+":
        result = left + right
    elif operator == "-":
        result = left - right
    elif operator == "*":
        result = left * right
    else:
        if right == 0:
            raise ZeroDivisionError("Não é possível dividir por zero.")
        result = left / right

    if not result.is_finite():
        raise ValueError("O resultado não é um número finito.")
    return result


class Calculator:
    """Estado de uma calculadora sequencial com histórico recente."""

    def __init__(self) -> None:
        self.display = "0"
        self.history: list[str] = []
        self._accumulator: Decimal | None = None
        self._operator: str | None = None
        self._waiting_for_operand = False
        self._just_calculated = False

    def input_digit(self, digit: str) -> None:
        if digit not in "0123456789" or len(digit) != 1:
            raise ValueError("Entrada de dígito inválida.")
        if self._waiting_for_operand or self._just_calculated:
            self.display = digit
            self._waiting_for_operand = False
            self._just_calculated = False
        elif self.display == "0":
            self.display = digit
        elif len(self.display) < MAX_DISPLAY_LENGTH:
            self.display += digit

    def input_decimal(self) -> None:
        if self._waiting_for_operand or self._just_calculated:
            self.display = "0."
            self._waiting_for_operand = False
            self._just_calculated = False
        elif "." not in self.display and len(self.display) < MAX_DISPLAY_LENGTH:
            self.display += "."

    def set_operator(self, operator: str) -> None:
        if operator not in OPERATORS:
            raise ValueError("Operação inválida.")
        if self._waiting_for_operand:
            raise ValueError("Não é permitido inserir operadores consecutivos.")

        current = parse_number(self.display)
        if self._operator is not None and not self._waiting_for_operand:
            result = calculate(self._accumulator, self._operator, current)
            self.display = format_number(result)
            self._accumulator = result
        elif self._accumulator is None or self._just_calculated:
            self._accumulator = current

        self._operator = operator
        self._waiting_for_operand = True
        self._just_calculated = False

    def calculate(self) -> str:
        if self._operator is None or self._accumulator is None:
            return self.display

        right = self._accumulator if self._waiting_for_operand else parse_number(self.display)
        result = calculate(self._accumulator, self._operator, right)
        expression = (
            f"{format_number(self._accumulator)} {self._operator} "
            f"{format_number(right)} = {format_number(result)}"
        )
        self.display = format_number(result)
        self.history.insert(0, expression)
        del self.history[MAX_HISTORY:]
        self._accumulator = None
        self._operator = None
        self._waiting_for_operand = False
        self._just_calculated = True
        return self.display

    def backspace(self) -> None:
        if self._waiting_for_operand or self._just_calculated:
            return
        self.display = self.display[:-1] or "0"
        if self.display == "-":
            self.display = "0"

    def clear(self) -> None:
        self.display = "0"
        self.history.clear()
        self._accumulator = None
        self._operator = None
        self._waiting_for_operand = False
        self._just_calculated = False
