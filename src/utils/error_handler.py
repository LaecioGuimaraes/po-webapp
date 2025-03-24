def handle_error(e, data=None):
    return {
        "dados": {
            "parametros": data["dados"]["parametros"] if data and "dados" in data and "parametros" in data["dados"] else None,
            "resultado": {
                "decisao": [],
                "Z": None,
                "grafico": False,
                "imagem": None
            },
            "mensagem": {
                "sucesso": False,
                "texto": f"Erro: {str(e)}"
            }
        }
    }, 500