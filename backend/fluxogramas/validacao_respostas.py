from decimal import Decimal, InvalidOperation

def normalizar_numero(valor):
    if valor is None:
        return None

    if isinstance(valor, Decimal):
        return valor

    if isinstance(valor, (int, float)):
        return Decimal(str(valor))

    if isinstance(valor, str):
        valor = valor.strip().replace(",", ".")

        try:
            return Decimal(valor)
        except InvalidOperation:
            return None

    return None


def criar_mensagem_erro_contextual(resposta_usuario, resposta_correta):
    if resposta_usuario < resposta_correta:
        return (
            "Sua resposta ficou abaixo do esperado. "
            "Revise o cálculo e confira se algum valor ficou faltando."
        )

    if resposta_usuario > resposta_correta:
        return (
            "Sua resposta ficou acima do esperado. "
            "Revise o cálculo e veja se algum valor foi somado ou multiplicado a mais."
        )

    return "Resposta incorreta. Revise o raciocínio utilizado."


def validar_resposta_numerica(resposta_usuario, resposta_correta, tolerancia=0.1):
    usuario = normalizar_numero(resposta_usuario)
    correta = normalizar_numero(resposta_correta)
    margem = normalizar_numero(tolerancia)

    if usuario is None:
        return {
            "correta": False,
            "mensagem": "A resposta precisa ser um número válido."
        }

    if correta is None:
        return {
            "correta": False,
            "mensagem": "A resposta correta cadastrada está inválida."
        }

    diferenca = abs(usuario - correta)

    if diferenca <= margem:
        return {
            "correta": True,
            "mensagem": "Resposta correta."
        }

    return {
        "correta": False,
        "mensagem": criar_mensagem_erro_contextual(usuario, correta)
    }